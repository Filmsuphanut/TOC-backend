from scraping import Scraping
import time
import datetime
import os
import pandas as pd

sc = Scraping()

def web_sp(Scraping):
    return Scraping.scrap()

def web_sp_graph(Scraping):
    return Scraping.scrap_inves()


while(True):

    current_time = datetime.datetime.now().time()
    scraping_time = datetime.time(0,15, 0)

    if(scraping_time.minute == current_time.minute):
    #if(True):
    
        print("Scraping at : ",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        data = None
        while data is None:
            try:
                data = web_sp(sc)
            except:
                print("Error")

        data = None
        while data is None:
            try:
                data = web_sp_graph(sc)
                print("******************************************************")
                print("Success ! ! ")
                print("/n/n/n")
            except:
                print("Error")




