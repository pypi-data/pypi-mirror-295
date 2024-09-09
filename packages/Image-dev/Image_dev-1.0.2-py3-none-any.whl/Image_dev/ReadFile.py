from pandas import read_csv, read_excel

def read(path):
    try:
        if path.endswith('.xlsx') or path.endswith('.xls'):
            df= read_excel(path, dtype=str, keep_default_na=False, na_values='')
        elif path.endswith('.txt'):
            df= read_csv(path, dtype=str, keep_default_na=False, na_values='', sep='\t')
        elif path.endswith('.csv'):
            df= read_csv(path, dtype=str, keep_default_na=False, na_values='')
    except :
        df= read_csv(path, dtype=str, keep_default_na=False, na_values='', sep='\t')
    finally:
        return df
