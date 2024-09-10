from pandas import read_csv, read_excel

def read(path):
    if path.endswith('.xlsx') or path.endswith('.xls'):
        df= read_excel(path, dtype=str, keep_default_na=False, na_values=[None,''])
        return df
    elif path.endswith('.txt'):
        df= read_csv(path, dtype=str, keep_default_na=False, na_values=[None,''], sep='\t')
        return df
    elif path.endswith('.csv'):
        df= read_csv(path, dtype=str, keep_default_na=False, na_values=[None,''])
        return df