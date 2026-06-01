import sys
import os
import pandas as pd

# Adiciona etapas anteriores ao path para importar módulos
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "ETAPA 3"))
sys.path.insert(0, os.path.join(BASE, "ETAPA 4"))

from dea_models import run_ccr, run_bcc, compute_scale_efficiency, get_improvement_targets
from visualization import (
    plot_efficiency_histogram,
    plot_efficiency_ranking,
    plot_ccr_vs_bcc,
    plot_benchmark_heatmap,
    plot_improvement_targets,
)

DATA_PATH = os.path.join(BASE, "ETAPA 1", "data", "processed_data.csv")
RESULTS_DIR = os.path.join(BASE, "ETAPA 3", "results")
FIGURES_DIR = os.path.join(BASE, "ETAPA 4", "figures")

INPUTS = ["totalAssets", "operatingExpenses", "fullTimeEmployees"]
OUTPUTS = ["totalRevenue", "ebitda"]

LABEL = {
    "totalAssets": "Total Assets",
    "operatingExpenses": "Operating Expenses",
    "fullTimeEmployees": "Nº Funcionários",
    "totalRevenue": "Receita Líquida",
    "ebitda": "EBITDA",
}


def separator(title=""):
    print("\n" + "=" * 65)
    if title:
        print(f"  {title}")
        print("=" * 65)


def main():
    # ── 1. Carregar dados ─────────────────────────────────────────
    separator("1. CARREGANDO DADOS")
    df = pd.read_csv(DATA_PATH).set_index("ticker")
    inputs_df = df[INPUTS].astype(float)
    outputs_df = df[OUTPUTS].astype(float)
    print(f"  DMUs carregadas: {len(df)}")
    print(f"  Inputs:  {INPUTS}")
    print(f"  Outputs: {OUTPUTS}")

    # ── 2. Modelo CCR ─────────────────────────────────────────────
    separator("2. MODELO CCR (orientação output)")
    ccr_df = run_ccr(inputs_df, outputs_df, orientation="output")
    ccr_df.to_csv(os.path.join(RESULTS_DIR, "ccr_results.csv"), index=False)
    n_eff_ccr = ccr_df["efficient"].sum()
    print(f"  Eficientes: {n_eff_ccr} / {len(ccr_df)}")
    print(f"  Score médio: {ccr_df['ccr_score'].mean():.4f}")
    print(f"  Resultados salvos em ETAPA 3/results/ccr_results.csv")

    # ── 3. Modelo BCC ─────────────────────────────────────────────
    separator("3. MODELO BCC (orientação output)")
    bcc_df = run_bcc(inputs_df, outputs_df, orientation="output")
    bcc_df.to_csv(os.path.join(RESULTS_DIR, "bcc_results.csv"), index=False)
    n_eff_bcc = bcc_df["efficient"].sum()
    print(f"  Eficientes: {n_eff_bcc} / {len(bcc_df)}")
    print(f"  Score médio: {bcc_df['bcc_score'].mean():.4f}")
    print(f"  Resultados salvos em ETAPA 3/results/bcc_results.csv")

    # ── 4. Eficiência de Escala ───────────────────────────────────
    separator("4. EFICIÊNCIA DE ESCALA")
    scale_df = compute_scale_efficiency(ccr_df, bcc_df)
    scale_df.to_csv(os.path.join(RESULTS_DIR, "scale_efficiency.csv"), index=False)
    print(scale_df[["DMU", "ccr_score", "bcc_score", "scale_efficiency", "returns_to_scale"]].to_string(index=False))

    # ── 5. Visualizações ─────────────────────────────────────────
    separator("5. GERANDO VISUALIZAÇÕES")
    plot_efficiency_histogram(ccr_df, bcc_df)
    plot_efficiency_ranking(ccr_df, bcc_df)
    plot_ccr_vs_bcc(ccr_df, bcc_df)
    plot_benchmark_heatmap(ccr_df)
    plot_improvement_targets(top_n=3)
    print(f"  Gráficos salvos em ETAPA 4/figures/")

    # ── 6. Metas de melhoria ──────────────────────────────────────
    separator("6. METAS DE MELHORIA — 3 DMUs MAIS INEFICIENTES")
    ineficientes = ccr_df[~ccr_df["efficient"]].nlargest(3, "ccr_score")
    for _, row in ineficientes.iterrows():
        targets = get_improvement_targets(row["DMU"], ccr_df, inputs_df, outputs_df)
        print(f"\n  {targets['DMU']}  (CCR = {targets['ccr_score']})")
        print(f"  Benchmarks: {row['benchmarks']}")
        for out, vals in targets["outputs"].items():
            print(f"    {LABEL[out]}: {vals['atual']:.2e} → {vals['meta']:.2e}  (+{vals['aumento_%']}%)")

    # ── 7. Relatório Final ────────────────────────────────────────
    separator("7. RELATÓRIO CONSOLIDADO")
    efic_ccr = ccr_df[ccr_df["efficient"]]["DMU"].tolist()
    efic_bcc = bcc_df[bcc_df["efficient"]]["DMU"].tolist()
    so_bcc = [d for d in efic_bcc if d not in efic_ccr]

    print(f"\n  DMUs eficientes CCR ({len(efic_ccr)}): {', '.join(efic_ccr)}")
    print(f"  DMUs eficientes BCC ({len(efic_bcc)}): {', '.join(efic_bcc)}")
    if so_bcc:
        print(f"  Eficientes só no BCC (efeito escala): {', '.join(so_bcc)}")

    benchmarks_count = {}
    for _, row in ccr_df[~ccr_df["efficient"]].iterrows():
        for b in row["benchmarks"].split(", "):
            if b and b != "-":
                benchmarks_count[b] = benchmarks_count.get(b, 0) + 1
    top_benchmarks = sorted(benchmarks_count.items(), key=lambda x: -x[1])
    print(f"\n  Benchmarks mais referenciados:")
    for dmu, count in top_benchmarks:
        print(f"    {dmu}: referência para {count} DMUs ineficientes")

    print(f"\n  Score médio CCR: {ccr_df['ccr_score'].mean():.4f}")
    print(f"  Score médio BCC: {bcc_df['bcc_score'].mean():.4f}")
    print(f"\n  Pipeline concluído com sucesso.")
    separator()


if __name__ == "__main__":
    main()
