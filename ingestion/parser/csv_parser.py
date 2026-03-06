import pandas as pd

def parse_get_csv(file_path: str, document_type: str) -> dict:
    df = pd.read_csv(file_path)

    # norm col name
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    summary = {
        "row_count": len(df),
        "columns": list(df.columns),
        "document_type": document_type,
        "raw_text": df.to_string(index=False), # will pass this to gemini
        "sample": df.head(10).to_dict(orient="records")
    }

    return summary