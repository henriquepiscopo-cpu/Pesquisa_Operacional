import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import ast
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)

RESULTS_DIR = os.path.join(_BASE, "ETAPA 3", "results")
FIGURES_DIR = os.path.join(_HERE, "figures")
DATA_PATH = os.path.join(_BASE, "ETAPA 1", "data", "processed_data.csv")

INPUTS = ["totalAssets", "operatingExpenses", "fullTimeEmployees"]
OUTPUTS = ["totalRevenue", "ebitda"]

sns.set_theme(style="whitegrid", palette="colorblind")


def load_results():
    ccr_df = pd.read_csv(f"{RESULTS_DIR}/ccr_results.csv")
    bcc_df = pd.read_csv(f"{RESULTS_DIR}/bcc_results.csv")
    return ccr_df, bcc_df


def plot_efficiency_histogram(ccr_df, bcc_df):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(ccr_df["ccr_score"], bins=10, alpha=0.6, label="CCR", color="#0072B2", edgecolor="white")
    ax.hist(bcc_df["bcc_score"], bins=10, alpha=0.6, label="BCC", color="#E69F00", edgecolor="white")
    ax.axvline(1.0, color="red", linestyle="--", linewidth=1.5, label="Fronteira eficiente (θ=1)")

    ax.set_xlabel("Score de Eficiência (θ)", fontsize=12)
    ax.set_ylabel("Nº de DMUs", fontsize=12)
    ax.set_title("Distribuição dos Scores de Eficiência — CCR vs BCC", fontsize=14, fontweight="bold")
    ax.legend()

    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/histogram_efficiency.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Histograma salvo: results/figures/histogram_efficiency.png")


def plot_efficiency_ranking(ccr_df, bcc_df):
    merged = ccr_df[["DMU", "ccr_score"]].merge(bcc_df[["DMU", "bcc_score"]], on="DMU")
    merged = merged.sort_values("ccr_score", ascending=True)

    fig, ax = plt.subplots(figsize=(11, 8))
    y = np.arange(len(merged))
    height = 0.35

    bars_ccr = ax.barh(y + height / 2, merged["ccr_score"], height, label="CCR", color="#0072B2", alpha=0.85)
    bars_bcc = ax.barh(y - height / 2, merged["bcc_score"], height, label="BCC", color="#E69F00", alpha=0.85)
    ax.axvline(1.0, color="red", linestyle="--", linewidth=1.5, label="Fronteira (θ=1)")

    ax.set_yticks(y)
    ax.set_yticklabels(merged["DMU"], fontsize=10)
    ax.set_xlabel("Score de Eficiência (θ)", fontsize=12)
    ax.set_title("Ranking de Eficiência por DMU — CCR vs BCC", fontsize=14, fontweight="bold")
    ax.legend()

    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/ranking_efficiency.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Ranking salvo: results/figures/ranking_efficiency.png")


def plot_ccr_vs_bcc(ccr_df, bcc_df):
    merged = ccr_df[["DMU", "ccr_score"]].merge(bcc_df[["DMU", "bcc_score"]], on="DMU")

    fig, ax = plt.subplots(figsize=(9, 8))

    ax.scatter(merged["ccr_score"], merged["bcc_score"], color="#0072B2", s=80, zorder=3)

    lim_min = min(merged["ccr_score"].min(), merged["bcc_score"].min()) - 0.02
    lim_max = max(merged["ccr_score"].max(), merged["bcc_score"].max()) + 0.02
    ax.plot([lim_min, lim_max], [lim_min, lim_max], "r--", linewidth=1.2, label="y = x")
    ax.axvline(1.0, color="gray", linestyle=":", linewidth=1)
    ax.axhline(1.0, color="gray", linestyle=":", linewidth=1)

    for _, row in merged.iterrows():
        ax.annotate(row["DMU"], (row["ccr_score"], row["bcc_score"]),
                    textcoords="offset points", xytext=(6, 4), fontsize=8)

    ax.set_xlabel("Score CCR (θ)", fontsize=12)
    ax.set_ylabel("Score BCC (θ)", fontsize=12)
    ax.set_title("Score CCR vs BCC por DMU", fontsize=14, fontweight="bold")
    ax.legend()

    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/ccr_vs_bcc.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Scatter CCR vs BCC salvo: results/figures/ccr_vs_bcc.png")


def plot_benchmark_heatmap(ccr_df):
    dmus = ccr_df["DMU"].tolist()
    efficient_dmus = ccr_df[ccr_df["efficient"] == True]["DMU"].tolist()
    inefficient_dmus = ccr_df[ccr_df["efficient"] == False]["DMU"].tolist()

    matrix = pd.DataFrame(0.0, index=inefficient_dmus, columns=efficient_dmus)

    for _, row in ccr_df[ccr_df["efficient"] == False].iterrows():
        lambdas = ast.literal_eval(row["lambdas"])
        for dmu, lv in lambdas.items():
            if dmu in efficient_dmus and lv > 0.001:
                matrix.loc[row["DMU"], dmu] = round(lv, 3)

    fig, ax = plt.subplots(figsize=(11, 7))
    sns.heatmap(matrix, annot=True, fmt=".2f", cmap="Blues", linewidths=0.5,
                cbar_kws={"label": "Intensidade λ"}, ax=ax)
    ax.set_title("Heatmap de Benchmarks — Intensidade dos Lambdas (CCR)", fontsize=14, fontweight="bold")
    ax.set_xlabel("DMUs Eficientes (benchmarks)", fontsize=11)
    ax.set_ylabel("DMUs Ineficientes", fontsize=11)

    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/benchmark_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Heatmap de benchmarks salvo: results/figures/benchmark_heatmap.png")


def plot_improvement_targets(top_n=3):
    ccr_df = pd.read_csv(f"{RESULTS_DIR}/ccr_results.csv")
    data_df = pd.read_csv(DATA_PATH).set_index("ticker")

    ineficientes = ccr_df[ccr_df["efficient"] == False].nlargest(top_n, "ccr_score")

    fig, axes = plt.subplots(1, top_n, figsize=(14, 5), sharey=False)

    for ax, (_, row) in zip(axes, ineficientes.iterrows()):
        dmu = row["DMU"]
        score = row["ccr_score"]

        atual = [data_df.loc[dmu, o] for o in OUTPUTS]
        meta = [v * score for v in atual]
        labels = ["Receita Líquida", "EBITDA"]

        x = np.arange(len(labels))
        w = 0.35
        ax.bar(x - w / 2, atual, w, label="Atual", color="#0072B2", alpha=0.85)
        ax.bar(x + w / 2, meta, w, label="Meta", color="#E69F00", alpha=0.85)

        ax.set_title(f"{dmu}\n(θ={score})", fontsize=11, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=9)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v/1e9:.1f}B"))
        ax.set_ylabel("USD", fontsize=9)
        if ax == axes[0]:
            ax.legend(fontsize=8)

    fig.suptitle(f"Metas de Melhoria — {top_n} DMUs Mais Ineficientes (CCR)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/improvement_targets.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Metas de melhoria salvas: results/figures/improvement_targets.png")


def main():
    ccr_df, bcc_df = load_results()

    plot_efficiency_histogram(ccr_df, bcc_df)
    plot_efficiency_ranking(ccr_df, bcc_df)
    plot_ccr_vs_bcc(ccr_df, bcc_df)
    plot_benchmark_heatmap(ccr_df)
    plot_improvement_targets(top_n=3)

    print("\nTodos os gráficos gerados em results/figures/")


if __name__ == "__main__":
    main()
