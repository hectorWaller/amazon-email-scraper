thonpython
import pandas as pd

def export_results(records, output_path):
    """Write records to CSV and Excel."""
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)

    excel_path = output_path.with_suffix(".xlsx")
    df.to_excel(excel_path, index=False)