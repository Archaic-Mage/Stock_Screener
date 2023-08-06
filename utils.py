import requests
import pandas as pd
import threading as th

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

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
    
    df['%CHNG \n'] = df['%CHNG \n'].apply(lambda x: 0.0 if x == '-' else float(x))
    df['FINAL QUANTITY \n'] = df['FINAL QUANTITY \n'].apply(lambda x: 0 if x == '-' else int(x.replace(',', '')))
    print(df)
    # condition %CHNG should be greater than 1%
    new_df = df[df['%CHNG \n'].abs() >= 1]
    #quantity traded should be more than 50000
    new_df = new_df[new_df['FINAL QUANTITY \n'] >= 50000]
    print(new_df)