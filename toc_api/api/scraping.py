from bs4 import BeautifulSoup, Comment
import regex as re
from selenium import webdriver
import pandas as pd
import time
import os

class Scraping:

    def __init__(self):
        self.website = ["https://www.kasikornbank.com/en/rate/pages/foreign-exchange.aspx",
        "https://www.scb.co.th/th/personal-banking/foreign-exchange-rates.html",
        "https://www.bangkokbank.com/th-TH/Personal/Other-Services/View-Rates/Foreign-Exchange-Rates",
        "https://exchangerate.krungthai.com/#/counterRate",
        "https://www.krungsri.com/th/exchangerate/Todayrates"]

        self.inves_website = ['https://th.investing.com/currencies/sgd-thb-historical-data',
        'https://th.investing.com/currencies/inr-thb-historical-data',
        'https://th.investing.com/currencies/sek-thb-historical-data',
        'https://th.investing.com/currencies/usd-thb-historical-data',
        'https://th.investing.com/currencies/rub-thb-historical-data',
        'https://th.investing.com/currencies/dkk-thb-historical-data',
        'https://th.investing.com/currencies/jpy-thb-historical-data',
        'https://th.investing.com/currencies/aed-thb-historical-data',
        'https://th.investing.com/currencies/cny-thb-historical-data',
        'https://th.investing.com/currencies/twd-thb-historical-data',
        'https://th.investing.com/currencies/gbp-thb-historical-data',
        'https://th.investing.com/currencies/idr-thb-historical-data',
        'https://th.investing.com/currencies/brl-thb-historical-data',
        'https://th.investing.com/currencies/php-thb-historical-data',
        'https://th.investing.com/currencies/aud-thb-historical-data',
        'https://th.investing.com/currencies/zar-thb-historical-data',
        'https://th.investing.com/currencies/myr-thb-historical-data',
        'https://th.investing.com/currencies/nzd-thb-historical-data',
        'https://th.investing.com/currencies/nok-thb-historical-data',
        'https://th.investing.com/currencies/krw-thb-historical-data',
        'https://th.investing.com/currencies/eur-thb-historical-data',
        'https://th.investing.com/currencies/cad-thb-historical-data',
        'https://th.investing.com/currencies/hkd-thb-historical-data',
        'https://th.investing.com/currencies/chf-thb-historical-data',
        'https://th.investing.com/currencies/sar-thb-historical-data']

        self.currency_list = ['SGD',
                        'INR',
                        'SEK',
                        'USD',
                        'RUB',
                        'DKK',
                        'JPY',
                        'AED',
                        'CNY',
                        'TWD',
                        'GBP',
                        'IDR',
                        'BRL',
                        'PHP',
                        'AUD',
                        'ZAR',
                        'MYR',
                        'NZD',
                        'NOK',
                        'KRW',
                        'EUR',
                        'CAD',
                        'HKD',
                        'CHF',
                        'SAR']

    def browser_get(self,url):
        self.browser.get(url)
        time.sleep(5)##########
        html = self.browser.page_source
        soup = BeautifulSoup(html, features="html.parser")
        return soup


    def get_inveswebsite(self,currency):
        currency = str(currency).lower()
        return "https://th.investing.com/currencies/"+currency+"-thb-historical-data"


    def remove_tag(self,html_str):
        TAG_RE = re.compile(r'<[^>]+>')
        text = TAG_RE.sub('!@', html_str)
        mylist = re.split(r'!@', text)
        clear_lst = []
        for clear_text in mylist:
            if (clear_text not in "\n") and (clear_text not in " ") and (clear_text not in ""):
                clear_lst.append(clear_text)
        return clear_lst
    #https://www.guru99.com/python-regular-expressions-complete-tutorial.html

    ######### start browser
    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')  
        options.add_argument('ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')  
             
        # executable_path param is not needed if you updated PATH

        module_dir = os.path.dirname(__file__)
        browser = webdriver.Chrome(options=options, executable_path= str(module_dir)+'/99.0.4844.51/chromedriver_win32/chromedriver.exe')
        return browser

    def end_browser(self,browser):
        browser.quit()

    def kasikorn(self,url): 
        soup = self.browser_get(url)


        #clean soup data
        # data = soup.find('div',{"id" : "divTableRate"}).find('tbody').find_all('tr')
        data = re.findall("<tr>(.+?)</tr>",re.findall("<tbody>(.+?)</tbody>",str(soup))[0])
        #re_find_all(r'<tr>',r'</tr>',re_find(r'<tbody>',r'</tbody>',str(soup)))
        lst_rows = []
        for index,value in enumerate(data):
            lst = self.remove_tag(str(value))
            lst2 = lst[2:]
            lst_buy = [lst2[3],lst2[1],lst2[0],"-",lst2[2]]
            lst_sell = [lst2[5],lst2[4],lst2[4],lst2[4]]
            lst_rows.append([lst[0].replace(" ",""),lst_buy,lst_sell])
        
        return lst_rows
        #return soup

    def scb(self,url): 
        soup = self.browser_get(url)
        
        #clean soup data
        #data = re_find_all(r'<tr data-list-template="" style="">',r'</tr>',re_find(r'<table class="table-rate" data-table="">',r'</table>',str(soup)))

        remove = re.compile(r'\n')
        d = remove.sub('', str(soup))
        data = re.findall('<tr data-list-template="" style="">(.+?)</tr>',re.findall('<table class="table-rate" data-table="">(.+?)</table>',str(d))[0])

        lst_rows = []
        for index,value in enumerate(data):
            lst = self.remove_tag(str(value))
            lst2 = lst[2:]
            lst_buy = [lst2[5],lst2[3],lst2[4],"-",lst2[2]]
            lst_sell = [lst2[1],lst2[0],lst2[0],"-"]
            lst_rows.append([lst[0],lst_buy,lst_sell])
        return lst_rows
        #return soup

    def bangkok(self,url):
        soup = self.browser_get(url)

        #clean soup data
        # data = soup.find('table',{"class" : "table-primary table-foreign-exchange-rates blue"}).find('tbody').find_all('tr')
        #data = re_find_all(r'<tr>',r'</tr>',re_find(r'<tbody>',r'</tbody>',re_find(r'<table class="table-primary table-foreign-exchange-rates blue">',r'</table>',str(soup))))
        #data = re.findall
        remove = re.compile(r'\n')
        d = remove.sub('', str(soup))
        data = re.findall('<table class="table-primary table-foreign-exchange-rates blue">(.+?)</table>',str(d))
        data = re.findall('<tbody>(.+?)</tbody>',data[0])
        data = re.findall('<tr>(.+?)</tr>',data[0])

        lst_rows = []
        for index,value in enumerate(data):
            clear_lst = self.remove_tag(str(value))
            clear_lst = [x.replace(" ", "") for x in clear_lst]
            while(len(clear_lst) < 7):
                clear_lst.append('-')
            lst2 = clear_lst[2:]
            lst_buy = [lst2[0],'-','-',lst2[2],lst2[3]]
            lst_sell = [lst2[1],"-",lst2[4],lst2[4]]
            lst_rows.append([clear_lst[0],lst_buy,lst_sell])
        return lst_rows
    #return soup

    def krungthai(self,url):
        soup = self.browser_get(url)

        #clean soup data
        #data = soup.find('table',{"id" : "cur-table-1"}).find('tbody').find_all('tr',{"class" : "ng-scope"})
        #data = re_find_all(r'<!-- ngIf: rate.isShow -->',r'<!-- end ngIf: rate.isShow -->',re_find(r'<tbody>',r'</tbody>',re_find(r'<table cellspacing="0" class="cur-table table table-bordered border-bottom-0" id="cur-table-1" style="table-layout: fixed; min-width: 688px;" width="100%">',r'</table>',str(soup))))
        remove = re.compile(r'\n')
        d = remove.sub('', str(soup))
        data = re.findall('<table cellspacing="0" class="cur-table table table-bordered border-bottom-0" id="cur-table-1" style="table-layout: fixed; min-width: 688px;" width="100%">(.+?)</table>',str(d))
        data = re.findall('<tbody>(.+?)</tbody>',str(data))
        data = re.findall('<!-- ngIf: rate.isShow -->(.+?)<!-- end ngIf: rate.isShow -->',str(data))
        
        lst_rows = []
        for index,value in enumerate(data):
            if index != 8 :
                clear_lst = self.remove_tag(str(value))
                clear_lst = [x.replace(" ", "") for x in clear_lst]
                clear_lst = [x.replace("Unq", "-") for x in clear_lst]
                lst2 = clear_lst[2:]
                lst_buy = [lst2[3],lst2[0],'-','-',lst2[1]]
                lst_sell = [lst2[4],lst2[2],'-','-']
                lst_rows.append([clear_lst[0],lst_buy,lst_sell])
        return lst_rows
    #return soup

    def krungsri(self,url):
        soup = self.browser_get(url)

        #clen soup data
        #data = soup.find('div',{"class" : "table-scroll"}).find('tbody').find_all('tr')
        #data = re_find_all(r'important">',r'</tr>',re_find(r'<tbody>',r'</tbody>',re_find(r'<div class="table-scroll">',r'</div>',str(soup))))
        remove = re.compile(r'\n')
        d = remove.sub('', str(soup))
        data = re.findall('<div class="table-scroll">(.+?)</div>',str(d))
        data = re.findall('<tbody>(.+?)</tbody>',str(data))
        data = re.findall('important">(.+?)</tr>',str(data))
        data = ["<"+d for d in data]
        
        lst_rows = []
        for index,value in enumerate(data):
            lst = self.remove_tag(str(value))
            remove = re.compile(r'\s|\xa0|\*')
            lst = [remove.sub('', x) for x in lst]
            lst = [x.replace("UNQ.", "-") for x in lst]
            lst2 = lst[-5:]
            lst_buy = [lst2[0],lst2[2],'-','-',lst2[3]]
            lst_sell = [lst2[1],lst2[4],lst2[4],lst2[4]]
            lst_rows.append([lst[1],lst_buy,lst_sell])
        return lst_rows
    #return soup

    def investing(self,website):
        soup = self.browser_get(website)

        data = re.findall('<tr>(.+?)</tr>',
                re.findall('<tbody>(.+?)</tbody>',
                re.findall('<table class="genTbl closedTbl historicalTbl" id="curr_table" tablesorter="">(.+?)</table>',
                re.findall('<div id="results_box">(.+?)</div>',re.sub(r'\n',"",str(soup)))[0])[0])[0])
        return data

    def get_currency(self,all_bank_data):
        currency_list = []
        for d in all_bank_data:
            for index,currency in enumerate(d):
                if index >= 3 :
                    currency_list.append(currency[0])
                else:#USD
                    if index == 0:
                        currency[0] = 'USD1'
                    if index == 1:
                        currency[0] = 'USD5'
                    if index == 2:
                        currency[0] = 'USD50'
                    currency_list.append(currency[0])

        #return list(set([x for x in currency_list if currency_list.count(x) == len(all_bank_data)]))
        return list(set(currency_list))


    def pack_bank_to_json(self,currency_list,all_bank_data,path):
        
        ############## all currency without usd1,5-20,50-100
        for currency in currency_list:
            ##########
            bank_name = {0 : 'ธนาคารกสิกรไทย',1 : 'ธนาคารไทยพาณิชย์',2 : 'ธนาคารกรุงเทพ',3 : 'ธนาคารกรุงไทย',4 : 'ธนาคารกรุงศรีอยุธยา'}

            bank = pd.DataFrame()
            bank = bank.reindex(columns=['ธนาคาร'])
            #bank.columns = pd.MultiIndex.from_product(bank.columns])

            buy_rate = ['ธนบัตร', 'ตั๋วเงิน', 'เช็คเดินทาง','ตั๋วแลกเงิน&ดราฟ','โอนเงินทางโทรเลข/โอนเงิน']
            br = pd.DataFrame()
            br = br.reindex(columns=buy_rate)
            br.columns = pd.MultiIndex.from_product([["ราคาที่ธนาคารรับซื้อ"], br.columns])

            sell_rate = ['ธนบัตร', 'เช็คเดินทาง', 'ตั๋วแลกเงิน&ดราฟ','โอนเงินทางโทรเลข/โอนเงิน']
            sr = pd.DataFrame()
            sr = sr.reindex(columns=sell_rate)
            sr.columns = pd.MultiIndex.from_product([["ราคาที่ธนาคารขาย"], sr.columns])

            result = pd.concat([br,sr], axis=1, join='inner')
            result = pd.concat([bank,result], axis=1, join='inner')##########################
            

            for index,bank in enumerate(all_bank_data):
                data_list = []
                get_cur = False      
                for currency_data in bank:
                    if currency_data[0] == currency:
                        data_list = [bank_name[index]]+currency_data[1]+currency_data[2]
                        result.loc[len(result)] = data_list
                        get_cur = True
                        break
                if get_cur == False:
                    #print(bank_name[index],currency)
                    result.loc[len(result)] = [bank_name[index]]+['-','-','-','-','-']+['-','-','-','-']
                        
            #result.to_csv('bank_buy_sell_rate/'+str(currency)+'.csv',index=False)
            result.to_json(path+str(currency)+'.json',force_ascii=False)


    def pack_inves_to_json(self,data,path,cur):

        col = ['Date', 'Price', 'Open','High','Low','Change(%)']
        df = pd.DataFrame()
        df = df.reindex(columns = col)

        for i,d in enumerate(data):
            dd = self.remove_tag(str(d))
            df.loc[len(df)] = dd

        df.to_json(path+'thb-'+cur+'.json',force_ascii=False)



    def scrap(self):
        #start_browser

        self.browser = self.start_browser()
        time.sleep(2)

        kasi_data = self.kasikorn(self.website[0])
        scb_data = self.scb(self.website[1])
        bangkok_data = self.bangkok(self.website[2])
        krungthai_data = self.krungthai(self.website[3])
        krungsri_data = self.krungsri(self.website[4])
        self.end_browser(self.browser)

        all_bank_data = [kasi_data.copy(),scb_data.copy(),bangkok_data.copy(),krungthai_data.copy(),krungsri_data.copy()]
        currency_list = self.get_currency(all_bank_data)

        #to json
        module_dir = os.path.dirname(__file__)
        path = str(module_dir)+'/data/'

        ban = ['KHR','QAR','BHD','VND','BND','OMR','LAK','MMK']
        
        currency_list = [item for item in self.currency_list if item not in ban]

        self.pack_bank_to_json(currency_list,all_bank_data,path)



    def scrap_inves(self):
        self.browser = self.start_browser()

        module_dir = os.path.dirname(__file__)
        path = str(module_dir)+'/data/'

        for cur in self.currency_list:

            website = self.get_inveswebsite(str(cur))
            print("scraping : ",website)

            data = None
            while data is None:
                try:
                    data = self.investing(website)
                except:
                    continue

            self.pack_inves_to_json(data,path,cur)

        self.end_browser(self.browser)

        return "SUCCESS"
