import requests
import pandas as pd
import threading as th

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def data_preprocessing(df):
    df_dict=df.to_dict()
    # Removing \n and trailing spaces
    for key in df_dict.keys() :
        new_key = key.replace(" \n", "").rstrip()
        df_dict[new_key] = df_dict.pop(key)
    # Removing ',' and converting the string to float
    remove_hyphen = (lambda x: 0.0 if x == '-' else x)
    key_list = ['PREV. CLOSE', 'IEP', 'CHNG', '%CHNG', 'FINAL', 'VALUE', 'FFM CAP', 'NM 52W H', 'NM 52W L']
    for key in key_list:
        df_dict[key] = {k: float(remove_hyphen(v.replace(",", ""))) for k, v in df_dict[key].items()}
    df_dict['FINAL QUANTITY'] = {k: int(remove_hyphen(v.replace(",", ""))) for k, v in df_dict['FINAL QUANTITY'].items()}
    df = pd.DataFrame.from_dict(df_dict)
    return df

def get_mdata():
    url = 'https://www.nseindia.com/api/equity-stockIndices?csv=true&index=NIFTY%20100'
    #get request
    response = requests.get(url, headers=HEADERS)
    # create csv file and write the response content
    with open('./data/nifty100.csv', 'wb') as f:
        f.write(response.content)  
        
    # clean data
    df = pd.read_csv('./data/nifty100.csv')
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.strip() if type(x) == str else x)
    df.to_csv('./data/nifty100.csv', index=False)

def get_pre_mdata():
    url = 'https://www.nseindia.com/api/market-data-pre-open?key=NIFTY&csv=true'
    #get request   
    response = requests.get(url, headers=HEADERS)
    with open ('./data/preopen.csv', 'wb') as f:
        f.write(response.content)
        
    # clean data
    df = pd.read_csv('./data/preopen.csv')
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.strip() if type(x) == str else x)
    df.to_csv('./data/preopen.csv', index=False)
        
def screen_mdata():
    # read the csv file
    df = pd.read_csv('./data/nifty100.csv')
    
    cipla_df = df[df['SYMBOL \n'] == 'CIPLA']
    print(cipla_df[['SYMBOL \n', 'LTP \n', '%CHNG \n']])
        
def screen_pre_mdata():
    # read the csv file            
    df = pd.read_csv('./data/preopen.csv')
    df = data_preprocessing(df)
    print(df)
    # condition %CHNG should be greater than 1%
    new_df = df[df['%CHNG'].abs() >= 1]
    #quantity traded should be more than 50000
    new_df = new_df[new_df['FINAL QUANTITY'] >= 50000]
    print(new_df)