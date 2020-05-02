from pandas import pandas as pd 

def get_items(file_name):
    data = pd.read_excel(file_name)
    df = pd.DataFrame(data=data)
    return df.to_dict('records')

