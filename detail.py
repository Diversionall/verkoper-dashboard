def prepare_data(df):
    import pandas as pd
    df.columns = df.columns.str.strip()

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["Relevante Marktprijs"] = pd.to_numeric(df["Relevante Marktprijs"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")
    df["Klantbezoeken"] = pd.to_numeric(df["Klantbezoeken"], errors="coerce")

    df.dropna(subset=["price", "Relevante Marktprijs"], inplace=True)

    return df

def calculate_price_diff(df):
    # Match renamed column in app.py
    df["Prijsverschil"] = df["price"] - df["Relevante_Marktprijs"]
    return df
