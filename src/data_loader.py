import pandas as pd
from pathlib import Path


def load_medicines():
    """
    Load the real medicine dataset.
    """

    project_root = Path(__file__).resolve().parent.parent

    csv_path = (
        project_root
        / "data"
        / "real_medicines.csv"
    )

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Medicine dataset not found: {csv_path}"
        )

    df = pd.read_csv(csv_path)

    if df.empty:
        raise ValueError(
            "The medicine dataset is empty."
        )

    return df