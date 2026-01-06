from utils import select_duckdb
import pandas as pd

df = select_duckdb("DESCRIBE restaurants;")
print(df)