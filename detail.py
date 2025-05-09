def prepare_data(df):
    import pandas as pd
    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert numeric fields
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["Relevante Marktprijs"] = pd.to_numeric(df["Relevante Marktprijs"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")
    df["Klantbezoeken"] = pd.to_numeric(df["Klantbezoeken"], errors="coerce")

    # Drop rows with no price or market price
    df.dropna(subset=["price", "Relevante Marktprijs"], inplace=True)

    return df

def calculate_price_diff(df):
    df["Prijsverschil"] = df["price"] - df["Relevante Marktprijs"]
    return df