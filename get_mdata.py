import threading as th
from utils import *

def live_screener():
    t = th.Timer(60.0, live_screener)                             
    t.start()
    
    #get data
    get_mdata()
    print('got mdata, starting screening')
    screen_mdata()

# get_mdata()  

if __name__ == '__main__':
    
    url = 'https://www.nseindia.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    response =  requests.get(url, headers=headers)
    cookies = response.cookies
    cook = str()
    for cookie in cookies:
        cook += cookie.name + '=' + cookie.value + ';'
    HEADERS['Cookie'] = cook
    
    print(HEADERS)
    
    #pre open results 
    get_pre_mdata()
    print('got preopen data, starting screening')
    screen_pre_mdata()
    print('preopen screening done')
    
    t = th.Thread(target=live_screener, args=())                         
    t.start()
    print('Press Ctrl+C to stop')
    t.join()
    
