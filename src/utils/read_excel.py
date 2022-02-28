import os
import pandas as pd

from flask import current_app


def read_excel(filename: str) -> pd.DataFrame:
    try:
        path = os.path.join(current_app.config["UPLOAD_PATH"], filename)
        df = pd.read_excel(path)
        return df

    except:
        return pd.DataFrame()
