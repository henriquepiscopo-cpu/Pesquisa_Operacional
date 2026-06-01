import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)

DATA_PATH = os.path.join(_BASE, "ETAPA 1", "data", "processed_data.csv")
FIGURES_DIR = os.path.join(_HERE, "figures")

INPUTS = ["totalAssets", "operatingExpenses", "fullTimeEmployees"]
OUTPUTS = ["totalRevenue", "ebitda"]
ALL_VARS = INPUTS + OUTPUTS

LABELS = {
    "totalAssets": "Total Assets",
    "operatingExpenses": "Operating Expenses",
    "fullTimeEmployees": "Nº Funcionários",
    "totalRevenue": "Receita Líquida",
    "ebitda": "EBITDA",
}


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def descriptive_stats(df):
    print("=" * 60)
    print("ESTATÍSTICAS DESCRITIVAS")
    print("=" * 60)
    desc = df[ALL_VARS].describe().T
    desc.index = [LABELS[c] for c in desc.index]
    print(desc.to_string())
    print()


def plot_boxplots(df):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Inputs
    input_data = df[INPUTS].copy()
    input_data.columns = [LABELS[c] for c in INPUTS]
    input_norm = input_data / input_data.max()
    input_norm.boxplot(ax=axes[0])
    axes[0].set_title("Inputs (normalizados)", fontsize=13)
    axes[0].set_ylabel("Valor relativo ao máximo")
    axes[0].tick_params(axis='x', rotation=15)

    # Outputs
    output_data = df[OUTPUTS].copy()
    output_data.columns = [LABELS[c] for c in OUTPUTS]
    output_norm = output_data / output_data.max()
    output_norm.boxplot(ax=axes[1])
    axes[1].set_title("Outputs (normalizados)", fontsize=13)
    axes[1].set_ylabel("Valor relativo ao máximo")
    axes[1].tick_params(axis='x', rotation=15)

    plt.suptitle("Boxplots das Variáveis DEA", fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/boxplots.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Boxplots salvos em results/figures/boxplots.png")


def plot_correlation_heatmap(df):
    corr = df[ALL_VARS].corr()
    corr.index = [LABELS[c] for c in corr.index]
    corr.columns = [LABELS[c] for c in corr.columns]

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                square=True, linewidths=0.5, ax=ax)
    ax.set_title("Matriz de Correlação — Variáveis DEA", fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/correlation_heatmap.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("Heatmap salvo em results/figures/correlation_heatmap.png")


def detect_outliers(df):
    print("=" * 60)
    print("DETECÇÃO DE OUTLIERS (IQR)")
    print("=" * 60)
    outlier_report = {}
    for col in ALL_VARS:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower) | (df[col] > upper)]["ticker"].tolist()
        outlier_report[col] = outliers
        print(f"  {LABELS[col]}: {outliers if outliers else 'nenhum'}")
    print()
    return outlier_report


def check_dea_rule(df):
    n_dmus = len(df)
    n_inputs = len(INPUTS)
    n_outputs = len(OUTPUTS)
    min_required = 3 * (n_inputs + n_outputs)

    print("=" * 60)
    print("REGRA PRÁTICA DO DEA")
    print("=" * 60)
    print(f"  Nº de DMUs:    {n_dmus}")
    print(f"  Nº de inputs:  {n_inputs}")
    print(f"  Nº de outputs: {n_outputs}")
    print(f"  Mínimo recomendado (3 × (I + O)): {min_required}")
    if n_dmus >= min_required:
        print(f"  ✔ Regra atendida ({n_dmus} ≥ {min_required})")
    else:
        print(f"  ✘ Regra NÃO atendida ({n_dmus} < {min_required})")
    print()


def main():
    df = load_data()
    print(f"\nDados carregados: {len(df)} DMUs\n")

    descriptive_stats(df)
    plot_boxplots(df)
    plot_correlation_heatmap(df)
    detect_outliers(df)
    check_dea_rule(df)

    print("=" * 60)
    print("ANÁLISE EXPLORATÓRIA CONCLUÍDA")
    print("Gráficos salvos em results/figures/")
    print("=" * 60)


if __name__ == "__main__":
    main()
