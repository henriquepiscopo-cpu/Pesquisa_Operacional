import pandas as pd
import numpy as np
import os
from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize, lpSum, value, PULP_CBC_CMD

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)

DATA_PATH = os.path.join(_BASE, "ETAPA 1", "data", "processed_data.csv")
RESULTS_DIR = os.path.join(_HERE, "results")

INPUTS = ["totalAssets", "operatingExpenses", "fullTimeEmployees"]
OUTPUTS = ["totalRevenue", "ebitda"]


def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.set_index("ticker")
    inputs_df = df[INPUTS].astype(float)
    outputs_df = df[OUTPUTS].astype(float)
    return df, inputs_df, outputs_df


def run_ccr(inputs_df, outputs_df, orientation="output"):
    dmus = inputs_df.index.tolist()
    n = len(dmus)
    records = []

    for o, dmu_o in enumerate(dmus):
        prob = LpProblem(f"CCR_{dmu_o}", LpMaximize if orientation == "output" else LpMinimize)
        lambdas = [LpVariable(f"lambda_{j}", lowBound=0) for j in range(n)]
        theta = LpVariable("theta", lowBound=0)

        if orientation == "output":
            prob += theta
            for i, inp in enumerate(INPUTS):
                prob += lpSum(lambdas[j] * inputs_df.iloc[j][inp] for j in range(n)) <= inputs_df.iloc[o][inp]
            for r, out in enumerate(OUTPUTS):
                prob += lpSum(lambdas[j] * outputs_df.iloc[j][out] for j in range(n)) >= theta * outputs_df.iloc[o][out]
        else:
            prob += theta
            for i, inp in enumerate(INPUTS):
                prob += lpSum(lambdas[j] * inputs_df.iloc[j][inp] for j in range(n)) <= theta * inputs_df.iloc[o][inp]
            for r, out in enumerate(OUTPUTS):
                prob += lpSum(lambdas[j] * outputs_df.iloc[j][out] for j in range(n)) >= outputs_df.iloc[o][out]

        prob.solve(PULP_CBC_CMD(msg=0))

        eff = value(theta)
        lam_vals = {dmus[j]: round(value(lambdas[j]), 4) for j in range(n)}
        benchmarks = [dmu for dmu, lv in lam_vals.items() if lv > 0.001 and dmu != dmu_o]

        # output orientation: efficient = theta == 1, inefficient = theta > 1
        efficient = eff <= 1.0001 if orientation == "output" else eff >= 0.9999

        records.append({
            "DMU": dmu_o,
            "ccr_score": round(eff, 4),
            "efficient": efficient,
            "benchmarks": ", ".join(benchmarks) if benchmarks else "-",
            "lambdas": str(lam_vals),
        })

    return pd.DataFrame(records)


def run_bcc(inputs_df, outputs_df, orientation="output"):
    dmus = inputs_df.index.tolist()
    n = len(dmus)
    records = []

    for o, dmu_o in enumerate(dmus):
        prob = LpProblem(f"BCC_{dmu_o}", LpMaximize if orientation == "output" else LpMinimize)
        lambdas = [LpVariable(f"lambda_{j}", lowBound=0) for j in range(n)]
        theta = LpVariable("theta", lowBound=0)

        if orientation == "output":
            prob += theta
            for i, inp in enumerate(INPUTS):
                prob += lpSum(lambdas[j] * inputs_df.iloc[j][inp] for j in range(n)) <= inputs_df.iloc[o][inp]
            for r, out in enumerate(OUTPUTS):
                prob += lpSum(lambdas[j] * outputs_df.iloc[j][out] for j in range(n)) >= theta * outputs_df.iloc[o][out]
        else:
            prob += theta
            for i, inp in enumerate(INPUTS):
                prob += lpSum(lambdas[j] * inputs_df.iloc[j][inp] for j in range(n)) <= theta * inputs_df.iloc[o][inp]
            for r, out in enumerate(OUTPUTS):
                prob += lpSum(lambdas[j] * outputs_df.iloc[j][out] for j in range(n)) >= outputs_df.iloc[o][out]

        # Restrição BCC: convexidade
        prob += lpSum(lambdas) == 1

        prob.solve(PULP_CBC_CMD(msg=0))

        eff = value(theta)
        lam_vals = {dmus[j]: round(value(lambdas[j]), 4) for j in range(n)}
        benchmarks = [dmu for dmu, lv in lam_vals.items() if lv > 0.001 and dmu != dmu_o]

        efficient = eff <= 1.0001 if orientation == "output" else eff >= 0.9999

        records.append({
            "DMU": dmu_o,
            "bcc_score": round(eff, 4),
            "efficient": efficient,
            "benchmarks": ", ".join(benchmarks) if benchmarks else "-",
            "lambdas": str(lam_vals),
        })

    return pd.DataFrame(records)


def compute_scale_efficiency(ccr_df, bcc_df):
    merged = ccr_df[["DMU", "ccr_score"]].merge(bcc_df[["DMU", "bcc_score"]], on="DMU")
    merged["scale_efficiency"] = (merged["ccr_score"] / merged["bcc_score"]).round(4)

    def classify_rts(row):
        if row["scale_efficiency"] >= 0.9999:
            return "CRS"
        elif row["bcc_score"] > row["ccr_score"]:
            return "IRS/DRS"
        else:
            return "DRS"

    merged["returns_to_scale"] = merged.apply(classify_rts, axis=1)
    return merged


def get_improvement_targets(dmu_name, ccr_df, inputs_df, outputs_df):
    row = ccr_df[ccr_df["DMU"] == dmu_name].iloc[0]
    score = row["ccr_score"]

    targets = {"DMU": dmu_name, "ccr_score": score, "inputs": {}, "outputs": {}}

    for inp in INPUTS:
        atual = inputs_df.loc[dmu_name, inp]
        targets["inputs"][inp] = {"atual": round(atual, 2), "meta": round(atual, 2)}

    for out in OUTPUTS:
        atual = outputs_df.loc[dmu_name, out]
        meta = round(atual * score, 2)  # output orientation: meta = atual * theta
        targets["outputs"][out] = {"atual": round(atual, 2), "meta": meta, "aumento_%": round((score - 1) * 100, 2)}


    return targets


def main():
    df, inputs_df, outputs_df = load_data()
    print(f"Dados carregados: {len(df)} DMUs\n")

    print("Rodando modelo CCR (orientação output)...")
    ccr_df = run_ccr(inputs_df, outputs_df, orientation="output")
    ccr_df.to_csv(f"{RESULTS_DIR}/ccr_results.csv", index=False)
    print(f"CCR concluído. Resultados salvos em results/ccr_results.csv\n")

    print("Rodando modelo BCC (orientação output)...")
    bcc_df = run_bcc(inputs_df, outputs_df, orientation="output")
    bcc_df.to_csv(f"{RESULTS_DIR}/bcc_results.csv", index=False)
    print(f"BCC concluído. Resultados salvos em results/bcc_results.csv\n")

    print("Calculando eficiência de escala...")
    scale_df = compute_scale_efficiency(ccr_df, bcc_df)
    scale_df.to_csv(f"{RESULTS_DIR}/scale_efficiency.csv", index=False)

    print("\n" + "=" * 60)
    print("RESULTADOS CCR")
    print("=" * 60)
    print(ccr_df[["DMU", "ccr_score", "efficient", "benchmarks"]].to_string(index=False))

    print("\n" + "=" * 60)
    print("RESULTADOS BCC")
    print("=" * 60)
    print(bcc_df[["DMU", "bcc_score", "efficient", "benchmarks"]].to_string(index=False))

    print("\n" + "=" * 60)
    print("EFICIÊNCIA DE ESCALA")
    print("=" * 60)
    print(scale_df[["DMU", "ccr_score", "bcc_score", "scale_efficiency", "returns_to_scale"]].to_string(index=False))

    print("\n" + "=" * 60)
    print("RESUMO GERAL")
    print("=" * 60)
    print(f"DMUs eficientes CCR: {ccr_df['efficient'].sum()} / {len(ccr_df)}")
    print(f"DMUs eficientes BCC: {bcc_df['efficient'].sum()} / {len(bcc_df)}")
    print(f"Score médio CCR:     {ccr_df['ccr_score'].mean():.4f}")
    print(f"Score médio BCC:     {bcc_df['bcc_score'].mean():.4f}")

    print("\n" + "=" * 60)
    print("METAS DE MELHORIA — 3 DMUs mais ineficientes (CCR)")
    print("=" * 60)
    ineficientes = ccr_df[~ccr_df["efficient"]].nlargest(3, "ccr_score")
    for _, row in ineficientes.iterrows():
        targets = get_improvement_targets(row["DMU"], ccr_df, inputs_df, outputs_df)
        print(f"\n{targets['DMU']} (score CCR: {targets['ccr_score']})")
        for out, vals in targets["outputs"].items():
            print(f"  {out}: atual={vals['atual']:.2e} → meta={vals['meta']:.2e} (aumento de {vals['aumento_%']}%)")


if __name__ == "__main__":
    main()
