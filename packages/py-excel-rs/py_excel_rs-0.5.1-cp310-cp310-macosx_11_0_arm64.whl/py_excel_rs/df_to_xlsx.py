import pandas as pd
import numpy as np

from py_excel_rs import _excel_rs

def csv_to_xlsx(buf: bytes) -> bytes:
    return _excel_rs.csv_to_xlsx(buf)

def df_to_xlsx(df: pd.DataFrame) -> bytes:
    py_list = np.vstack((df.keys().to_numpy(), df.to_numpy(dtype='object')))
    return _excel_rs.py_2d_to_xlsx(py_list)

def pg_to_xlsx(query: str, conn_string: str) -> bytes:
    
    client = _excel_rs.PyPostgresClient.new(conn_string)
    xlsx = client.get_xlsx_from_query(query)
    client.close()
    return xlsx