import yfinance as yf
import pandas as pd

TICKERS = [
    # Originais
    "XOM", "CVX", "SHEL", "BP", "TTE", "COP", "PBR", "EQNR",
    "E", "REP", "OXY", "DVN", "HES", "MRO", "VLO", "PSX",
    "MPC", "SLB", "HAL",
    # Adicionadas para ampliar margem DMU
    "IMO", "CNQ", "SU", "YPF", "EC", "BKR", "FTI", "WMB"
]

DATA_DIR = "./data"


def collect_data():
    records = []

    for ticker in TICKERS:
        print(f"Coletando: {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            bs = stock.balance_sheet
            inc = stock.income_stmt

            total_assets = None
            if bs is not None and not bs.empty:
                for label in ["Total Assets", "TotalAssets"]:
                    if label in bs.index:
                        total_assets = bs.loc[label].iloc[0]
                        break

            operating_expenses = None
            if inc is not None and not inc.empty:
                for label in ["Total Expenses", "Operating Expense", "Operating Expenses", "Total Operating Expenses"]:
                    if label in inc.index:
                        operating_expenses = inc.loc[label].iloc[0]
                        break

            employees = info.get("fullTimeEmployees", None)
            total_revenue = info.get("totalRevenue", None)
            ebitda = info.get("ebitda", None)

            records.append({
                "ticker": ticker,
                "empresa": info.get("shortName", ticker),
                "totalAssets": total_assets,
                "operatingExpenses": operating_expenses,
                "fullTimeEmployees": employees,
                "totalRevenue": total_revenue,
                "ebitda": ebitda,
            })

        except Exception as e:
            print(f"  ERRO em {ticker}: {e}")
            records.append({
                "ticker": ticker,
                "empresa": ticker,
                "totalAssets": None,
                "operatingExpenses": None,
                "fullTimeEmployees": None,
                "totalRevenue": None,
                "ebitda": None,
            })

    raw_df = pd.DataFrame(records)
    raw_df.to_csv(f"{DATA_DIR}/raw_data.csv", index=False)
    print(f"\nDados brutos salvos em {DATA_DIR}/raw_data.csv ({len(raw_df)} DMUs)")

    required_cols = ["totalAssets", "operatingExpenses", "fullTimeEmployees", "totalRevenue", "ebitda"]
    processed_df = raw_df.dropna(subset=required_cols).copy()

    # Garantir que todos os valores numéricos sejam positivos
    for col in required_cols:
        processed_df = processed_df[processed_df[col] > 0]

    processed_df.to_csv(f"{DATA_DIR}/processed_data.csv", index=False)

    print(f"Dados limpos salvos em {DATA_DIR}/processed_data.csv ({len(processed_df)} DMUs válidas)")
    print(f"DMUs removidas por dados incompletos/inválidos: {len(raw_df) - len(processed_df)}")
    print("\nDMUs válidas:")
    print(processed_df[["ticker", "empresa"]].to_string(index=False))

    return processed_df


if __name__ == "__main__":
    collect_data()
