from scraping import Scraping
import time
import datetime

sc = Scraping()

def web_sp(Scraping):
    Scraping.scrap()

def web_sp_graph(Scraping):
    return Scraping.scrap_inves()

while(True):

    current_time = datetime.datetime.now().time()
    scraping_time = datetime.time(0, 24, 0)

    if(scraping_time.minute == current_time.minute):
    #if(True):
    
        print("Scraping at : ",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        try:
            web_sp(sc)
            web_sp_graph(sc)
            print("Scraping Success !!")
        except:
            print("Error")



