from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import os
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import numpy as np
from datetime import datetime
# Create your views here.

@csrf_exempt
def say_hello(request):
    return HttpResponse("hello world")

# @csrf_exempt
# def investing(request):

#     if request.method == 'POST':
#         var = json.loads(request.body)["currency"]

#         if var == "USD1" or var == "USD5" or var == "USD50":
#             var = "USD"
        
#         module_dir = os.path.dirname(__file__)
#         file_path = "api/data/thb-"+var+".json"
#         f = open(file_path,encoding='utf-8')
#         data = json.load(f)

#         return JsonResponse(data)


# @csrf_exempt
# def graph_(request):

#     if request.method == 'POST':
#         var = json.loads(request.body)["currency"]

#         if var == "USD1" or var == "USD5" or var == "USD50":
#             var = "USD"
        
#         module_dir = os.path.dirname(__file__)
#         file_path = os.path.join(module_dir, 'data/'+str(var)+'.json')
#         f = open(file_path,encoding='utf-8')
#         data = json.load(f)

#         return JsonResponse(data)



###################################################################################################

@csrf_exempt
def compare(request):

    if request.method == 'POST':
        category = json.loads(request.body)["category"]
        currency = json.loads(request.body)["currency"]

        #print(category,currency)

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'data/thb-'+str(currency)+'.json')
        f = open(file_path,encoding='utf-8')
        data = json.load(f)
        json_record = json.dumps(data)

        csv = pd.read_json(json_record, orient = 'records')


        df = pd.DataFrame(columns=["price"])
        #df["date"] = datetime.strptime(csv["วันเดือนปี"],'%b %d, %Y')
        #df["date"] = csv["Date"]

        df["price"] = csv["Price"].round(decimals=4)
        df["currency_class"] = "Category " + str(category)
        df["date"] = "s"

        for i,d in enumerate(csv["Date"]):
        #     #print(d)
            da = datetime.strptime(str(d)[:-9],'%Y-%m-%d')
            d_ = str(da.day)+"-"+str(da.strftime("%b"))+"-"+str(da.year)[2:]
            #print(str(da.day)+"-"+str(da.strftime("%b"))+"-"+str(da.year)[2:])
            df['date'].iloc[i] = d_#str(str(da.day)+"-"+str(da.strftime("%b"))+"-"+str(da.year)[2:])
            #print(df['date'].iloc[i])

        #df.drop(columns=["date"])
        #df.rename(columns = {'date2':'date'}, inplace = True)

        send_data = df.to_dict('records')

        #print(send_data)
        return JsonResponse(send_data, safe=False)


@csrf_exempt
def detail(request,cur):
    if request.method == 'GET':
        currency = cur.upper()
        currency_realname = (cur.upper())
        if currency == 'USD1' or currency=='USD5' or currency=='USD50':
            currency = "USD"

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'data/thb-'+str(currency)+'.json')
        f = open(file_path,encoding='utf-8')
        data = json.load(f)
        json_record = json.dumps(data)

        csv = pd.read_json(json_record, orient = 'records')

        df = pd.DataFrame(columns=["price"])
        #df["date"] = datetime.strptime(csv["วันเดือนปี"],'%b %d, %Y')
        #df["date"] = csv["Date"]

        df["price"] = csv["Price"].round(decimals=2)
        df["date"] = "s"

        for i,d in enumerate(csv["Date"]):
        #     #print(d)
            da = datetime.strptime(str(d)[:-9],'%Y-%m-%d')
            d_ = str(da.day)+"-"+str(da.strftime("%b"))+"-"+str(da.year)[2:]
            #print(str(da.day)+"-"+str(da.strftime("%b"))+"-"+str(da.year)[2:])
            df['date'].iloc[i] = d_#str(str(da.day)+"-"+str(da.strftime("%b"))+"-"+str(da.year)[2:])
            #print(df['date'].iloc[i])

        #df.drop(columns=["date"])
        #df.rename(columns = {'date2':'date'}, inplace = True)

        send_data = df.to_dict('records')
        #print(send_data)

        #####################################

        file_path2 = os.path.join(module_dir, 'data/'+str(cur)+'.json')
        f2 = open(file_path2,encoding='utf-8')
        data2 = json.load(f2)
        json_record2 = json.dumps(data2)

        csv2 = pd.read_json(json_record2, orient = 'records')
        csv2.rename(columns = {
            'ธนาคาร':'bank',
            "('ราคาที่ธนาคารรับซื้อ', 'ธนบัตร')":'bank_buy_notes',
            "('ราคาที่ธนาคารรับซื้อ', 'ตั๋วเงิน')":'bank_buy_bill',
            "('ราคาที่ธนาคารรับซื้อ', 'เช็คเดินทาง')":'bank_buy_t_c',
            "('ราคาที่ธนาคารรับซื้อ', 'ตั๋วแลกเงิน&ดราฟ')":'bank_buy_d_d',
            "('ราคาที่ธนาคารรับซื้อ', 'โอนเงินทางโทรเลข/โอนเงิน')":'bank_buy_t_t',
            "('ราคาที่ธนาคารขาย', 'ธนบัตร')":'bank_sell_notes',
            "('ราคาที่ธนาคารขาย', 'เช็คเดินทาง')":'bank_sell_t_c',
            "('ราคาที่ธนาคารขาย', 'ตั๋วแลกเงิน&ดราฟ')":'bank_sell_d_d',
            "('ราคาที่ธนาคารขาย', 'โอนเงินทางโทรเลข/โอนเงิน')":'bank_sell_t_t'
        }, inplace = True)

        csv2.replace(str('-'),0,inplace=True)
        for col in csv2.iloc[:,1:]:
            csv2[col] = [round(float(x),2) for x in csv2[col]]
        
        for col in csv2.iloc[:,1:]:
            for row in range(len(csv2.index)):
                if csv2[col].iloc[row] == 0:
                    csv2[col].iloc[row] = "-"


        send_data2 = csv2.to_dict('records')
        #print(send_data2)
        send_data3 = get_detail()
        
        for d in send_data3:
            if d["currency"] == currency_realname:
                #print(currency_realname)
                send_data3 = d
                break
            #print(d)

        send = {"DETAILS":send_data3,"GRAPH":send_data,"BANK":send_data2}
        
        #print(send)
        #print(send_data)
        return JsonResponse(send, safe=False)



@csrf_exempt
def get_detail():
    currency_list = ['SGD',
                'INR',
                'SEK',
                'USD1',
                'USD5',
                'USD50',
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

    currency_name = ['Singapore',
            'India',
            'Sweden',
            'United States of America',
            'United States of America',
            'United States of America',
            'Russia',
            'Denmark',
            'Japan',
            'United Arab Emirates',
            'China',
            'Taiwan',
            'United Kingdom',
            'Indonesia',
            'Brazil',
            'Philippines',
            'Australia',
            'South Africa',
            'Malaysia',
            'New Zealand',
            'Norway',
            'South Korea',
            'European Union',
            'Canada',
            'Hong Kong',
            'Switzerland',
            'Saudi Arabia']
    currency_png = [x+".png" for x in currency_list]

    for i,c in enumerate(currency_png):
        #print(c)
        if c == "USD1.png" or c == "USD5.png" or c == "USD50.png":
            currency_png[i] = "USD.png"


    currency_description = ['Dollar',
                    'Rupee',
                    'Krona',
                    'United States dollar 1',
                    'United States dollar 5',
                    'United States dollar 50',
                    'Ruble',
                    'Krone',
                    'Yen',
                    'Dirham',
                    'Renminbi',
                    'Dollar',
                    'Pound',
                    'Rupiah',
                    'Real',
                    'Peso',
                    'Dollar',
                    'Rand',
                    'Ringgit',
                    'Dollar',
                    'Krone',
                    'Won',
                    'Euro',
                    'Dollar',
                    'Dollar',
                    'Franc',
                    'Riyal']

            
    df = pd.DataFrame(columns=["currency","name","country","description","status","price","open","high","low","change","percentage"])

    df["currency"] = currency_list
    df["name"] = currency_name
    df["country"] = currency_png
    df["description"] = currency_description

    for i in range(len(df.index)):

        cur = currency_list[i]

        if cur == "USD1" or cur == "USD5" or cur == "USD50":
            cur = "USD"

        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'data/thb-'+cur+'.json')
        f = open(file_path,encoding='utf-8')
        data = json.load(f)
        json_record = json.dumps(data)

        csv = pd.read_json(json_record, orient = 'records')

        
        if float(csv["Price"].iloc[0]) > float(csv["Open"].iloc[0]):
            status = "up"
        elif float(csv["Price"].iloc[0]) < float(csv["Open"].iloc[0]):
            status = "down"
        else:
            status = "equal"

        df["status"].iloc[i] = status
        df["price"].iloc[i] = round(csv["Price"].iloc[0], 2)
        df["open"].iloc[i] = round(csv["Open"].iloc[0], 2)
        df["high"].iloc[i] = round(csv["High"].iloc[0], 2)
        df["low"].iloc[i] = round(csv["Low"].iloc[0], 2)
        df["change"].iloc[i] = round(abs(csv["Price"].iloc[0] - csv["Price"].iloc[1]), 2)
        df["percentage"].iloc[i] = str(abs(float(csv["Change(%)"].iloc[0][:-1])))+"%"

    #print(df)

    send_data = df.to_dict('records')
    #print(send_data)

    return send_data

def currency(request):
    currency_list = ['SGD',
                'INR',
                'SEK',
                'USD1',
                'USD5',
                'USD50',
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

    currency_name = ['Singapore',
            'India',
            'Sweden',
            'United States of America',
            'United States of America',
            'United States of America',
            'Russia',
            'Denmark',
            'Japan',
            'United Arab Emirates',
            'China',
            'Taiwan',
            'United Kingdom',
            'Indonesia',
            'Brazil',
            'Philippines',
            'Australia',
            'South Africa',
            'Malaysia',
            'New Zealand',
            'Norway',
            'South Korea',
            'European Union',
            'Canada',
            'Hong Kong',
            'Switzerland',
            'Saudi Arabia']
    # currency_png = [x+".png" for x in currency_list]

    # for i,c in enumerate(currency_png):
    #     #print(c)
    #     if c == "USD1.png" or c == "USD5.png" or c == "USD50.png":
    #         currency_png[i] = "USD.png"


    currency_description = ['Dollar',
                    'Rupee',
                    'Krona',
                    'United States dollar 1',
                    'United States dollar 5',
                    'United States dollar 50',
                    'Ruble',
                    'Krone',
                    'Yen',
                    'Dirham',
                    'Renminbi',
                    'Dollar',
                    'Pound',
                    'Rupiah',
                    'Real',
                    'Peso',
                    'Dollar',
                    'Rand',
                    'Ringgit',
                    'Dollar',
                    'Krone',
                    'Won',
                    'Euro',
                    'Dollar',
                    'Dollar',
                    'Franc',
                    'Riyal']

            

    if request.method == 'GET':

        #df = pd.DataFrame(columns=["currency","name","country","description","status","price","open","high","low","change","percentage"])
        df = pd.DataFrame(columns=["currency","name","description","status","price","open","high","low","change","percentage"])
        df["currency"] = currency_list
        df["name"] = currency_name
        #df["country"] = currency_png
        df["description"] = currency_description

        for i in range(len(df.index)):

            cur = currency_list[i]

            if cur == "USD1" or cur == "USD5" or cur == "USD50":
                cur = "USD"

            module_dir = os.path.dirname(__file__)
            file_path = os.path.join(module_dir, 'data/thb-'+cur+'.json')
            f = open(file_path,encoding='utf-8')
            data = json.load(f)
            json_record = json.dumps(data)

            csv = pd.read_json(json_record, orient = 'records')

           
            if float(csv["Price"].iloc[0]) > float(csv["Open"].iloc[0]):
                status = "up"
            elif float(csv["Price"].iloc[0]) < float(csv["Open"].iloc[0]):
                status = "down"
            else:
                status = "equal"

            df["status"].iloc[i] = status
            df["price"].iloc[i] = round(csv["Price"].iloc[0], 2)
            df["open"].iloc[i] = round(csv["Open"].iloc[0], 2)
            df["high"].iloc[i] = round(csv["High"].iloc[0], 2)
            df["low"].iloc[i] = round(csv["Low"].iloc[0], 2)
            df["change"].iloc[i] = round(abs(csv["Price"].iloc[0] - csv["Price"].iloc[1]), 2)
            df["percentage"].iloc[i] = str(abs(float(csv["Change(%)"].iloc[0][:-1])))+"%"

        #print(df)

        send_data = df.to_dict('records')
        #print(send_data)

        return JsonResponse(send_data, safe=False)

@csrf_exempt
def header(request):
    currency_list = ['SGD',
                'INR',
                'SEK',
                'USD1',
                'USD5',
                'USD50',
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

    currency_name = ['Singapore',
            'India',
            'Sweden',
            'United States of America',
            'United States of America',
            'United States of America',
            'Russia',
            'Denmark',
            'Japan',
            'United Arab Emirates',
            'China',
            'Taiwan',
            'United Kingdom',
            'Indonesia',
            'Brazil',
            'Philippines',
            'Australia',
            'South Africa',
            'Malaysia',
            'New Zealand',
            'Norway',
            'South Korea',
            'European Union',
            'Canada',
            'Hong Kong',
            'Switzerland',
            'Saudi Arabia']
    currency_png = [x+".png" for x in currency_list]

    for i,c in enumerate(currency_png):
        #print(c)
        if c == "USD1.png" or c == "USD5.png" or c == "USD50.png":
            currency_png[i] = "USD.png"


    currency_description = ['Dollar',
                    'Rupee',
                    'Krona',
                    'United States dollar 1',
                    'United States dollar 5',
                    'United States dollar 50',
                    'Ruble',
                    'Krone',
                    'Yen',
                    'Dirham',
                    'Renminbi',
                    'Dollar',
                    'Pound',
                    'Rupiah',
                    'Real',
                    'Peso',
                    'Dollar',
                    'Rand',
                    'Ringgit',
                    'Dollar',
                    'Krone',
                    'Won',
                    'Euro',
                    'Dollar',
                    'Dollar',
                    'Franc',
                    'Riyal']

            

    if request.method == 'GET':

        df = pd.DataFrame(columns=["currency","name","country","description","status","price","open","high","low","change","percentage","top"])

        df["currency"] = currency_list
        df["name"] = currency_name
        df["country"] = currency_png
        df["description"] = currency_description

        for i in range(len(df.index)):

            cur = currency_list[i]

            if cur == "USD1" or cur == "USD5" or cur == "USD50":
                cur = "USD"

            module_dir = os.path.dirname(__file__)
            file_path = os.path.join(module_dir, 'data/thb-'+cur+'.json')
            f = open(file_path,encoding='utf-8')
            data = json.load(f)
            json_record = json.dumps(data)

            csv = pd.read_json(json_record, orient = 'records')

           
            if float(csv["Price"].iloc[0]) > float(csv["Open"].iloc[0]):
                status = "up"
            elif float(csv["Price"].iloc[0]) < float(csv["Open"].iloc[0]):
                status = "down"
            else:
                status = "equal"

            df["status"].iloc[i] = status
            df["price"].iloc[i] = round(csv["Price"].iloc[0], 2)
            df["open"].iloc[i] = round(csv["Open"].iloc[0], 2)
            df["high"].iloc[i] = round(csv["High"].iloc[0], 2)
            df["low"].iloc[i] = round(csv["Low"].iloc[0], 2)
            df["change"].iloc[i] = round(abs(csv["Price"].iloc[0] - csv["Price"].iloc[1]), 2)
            df["percentage"].iloc[i] = str(abs(float(csv["Change(%)"].iloc[0][:-1])))+"%"
            #print(type(float(abs(float(csv["Change(%)"].iloc[0][:-1])))))

            df["top"].iloc[i] = abs(float(csv["Change(%)"].iloc[0][:-1]))

        #print(df)
        send_d = df.sort_values(by=['top'],ascending=False)
        send_d = send_d.drop(columns=['top'])
        send_d = send_d[:10]
        send_data = send_d.to_dict('records')
        #print(send_data)

        return JsonResponse(send_data, safe=False)



@csrf_exempt
def choice(request):#no usd but usd1 usd5 usd50

    bank_name_ = {'ธนาคารกสิกรไทย' : 'kasikorn',
'ธนาคารไทยพาณิชย์' : 'scb',
'ธนาคารกรุงเทพ' : 'bangkok',
'ธนาคารกรุงไทย' : 'krungthai',
'ธนาคารกรุงศรีอยุธยา' : 'krungsri'}

    type_name = {'notes' : 'ธนบัตร',
'd_d' : 'ตั๋วแลกเงิน&ดราฟ',
't_t' : 'โอนเงินทางโทรเลข/โอนเงิน',
't_c' : 'เช็คเดินทาง',
'bill' : 'ตั๋วเงิน'}



    if request.method == 'POST':
        decision_ = json.loads(request.body)["decision"]
        currency_ = json.loads(request.body)["currency"]
        type_ = json.loads(request.body)["type"]
        amount_ = json.loads(request.body)["amount"]


        module_dir = os.path.dirname(__file__)
        file_path2 = os.path.join(module_dir, 'data/'+str(currency_)+'.json')
        f2 = open(file_path2,encoding='utf-8')
        data2 = json.load(f2)
        json_record2 = json.dumps(data2)

        csv2 = pd.read_json(json_record2, orient = 'records')
        csv2.rename(columns = {
            'ธนาคาร':'bank',
            "('ราคาที่ธนาคารรับซื้อ', 'ธนบัตร')":'bank_buy_notes',
            "('ราคาที่ธนาคารรับซื้อ', 'ตั๋วเงิน')":'bank_buy_bill',
            "('ราคาที่ธนาคารรับซื้อ', 'เช็คเดินทาง')":'bank_buy_t_c',
            "('ราคาที่ธนาคารรับซื้อ', 'ตั๋วแลกเงิน&ดราฟ')":'bank_buy_d_d',
            "('ราคาที่ธนาคารรับซื้อ', 'โอนเงินทางโทรเลข/โอนเงิน')":'bank_buy_t_t',
            "('ราคาที่ธนาคารขาย', 'ธนบัตร')":'bank_sell_notes',
            "('ราคาที่ธนาคารขาย', 'เช็คเดินทาง')":'bank_sell_t_c',
            "('ราคาที่ธนาคารขาย', 'ตั๋วแลกเงิน&ดราฟ')":'bank_sell_d_d',
            "('ราคาที่ธนาคารขาย', 'โอนเงินทางโทรเลข/โอนเงิน')":'bank_sell_t_t'
        }, inplace = True)

        csv2.replace(str('-'),0,inplace=True)

        for col in csv2:
            if col != 'bank':
                #csv2[col] = [round(float(x),2) for x in csv2[col]]
                csv2[col] = [(float(x)) for x in csv2[col]]


        # csv2['bank_buy_notes'] = [float(x) for x in csv2['bank_buy_notes']]
        # csv2['bank_buy_bill'] = [float(x) for x in csv2['bank_buy_bill']]
        # csv2['bank_buy_t_c'] = [float(x) for x in csv2['bank_buy_t_c']]
        # csv2['bank_buy_d_d'] = [float(x) for x in csv2['bank_buy_d_d']]
        # csv2['bank_buy_t_t'] = [float(x) for x in csv2['bank_buy_t_t']]
        # csv2['bank_sell_notes'] = [float(x) for x in csv2['bank_sell_notes']]
        # csv2['bank_sell_t_c'] = [float(x) for x in csv2['bank_sell_t_c']]
        # csv2['bank_sell_d_d'] = [float(x) for x in csv2['bank_sell_d_d']]
        # csv2['bank_sell_t_t'] = [float(x) for x in csv2['bank_sell_t_t']]

        # for col in csv2.iloc[:,1:]:
        #     for row in range(len(csv2.index)):
        #         csv2[col].iloc[row] = round(csv2[col].iloc[row],2)
        #         if csv2[col].iloc[row] == 0:
        #             csv2[col].iloc[row] = "-"

        taget_column = "bank_" + decision_+"_" + type_

        csv3 = csv2.copy()
        print(csv3)

        #print(csv2)
        #print(csv2[taget_column])
        if len(csv2[csv2[taget_column] != 0]) == 1:

            indx = (csv2[csv2[taget_column] != 0].index)[0]
            csv3 = csv2.iloc[indx]

        elif len(csv2[csv2[taget_column] != 0]) == 0:
            csv3 = csv2.iloc[0]
        else:
            if decision_ == "buy":
                idx = (csv2[csv2[taget_column] != 0][taget_column].idxmax())
                csv3 = csv2.iloc[idx]
                #csv3 = csv2[csv2[taget_column] != 0].iloc[csv2[taget_column]].max()
                #csv3 = csv2[csv2[taget_column] != 0].iloc[csv2[taget_column].idxmax()]
            elif decision_ == "sell":
                idx = (csv2[csv2[taget_column] != 0][taget_column].idxmin())
                csv3 = csv2.iloc[idx]
                #csv3 = csv2[csv2[taget_column] != 0].iloc[csv2[taget_column]].min()
                #csv3 = csv2[csv2[taget_column] != 0].iloc[csv2[taget_column].idxmin()]


        #csv2.replace(str('-'),0,inplace=True)

        #print(csv3)
        print(decision_,currency_,type_,amount_)
        bank_name =  str(csv3['bank']) if float(round(csv3[taget_column],2)) != 0 else "-"
        bankimg = bank_name_[csv3['bank']] if float(csv3[taget_column]) != 0 else "none"
        single_price = str(float(round(csv3[taget_column],2))) +"฿" if float(round(csv3[taget_column],2)) != 0 else "-"
        total_price = str(float(round(amount_*csv3[taget_column],2))) +"฿" if float(round(amount_*csv3[taget_column],2)) !=0 else "-"

        bestbank = {'bank_img' : bankimg,'bank_name' : bank_name
        ,'type' : str(type_name[type_]),'currency' : currency_,'amout' : float(round(amount_,2))
        ,'single_price' :single_price ,'total_price' : total_price}

        #csv2[['bank_buy_notes','bank_buy_bill','bank_buy_t_c','bank_buy_d_d','bank_buy_t_t','bank_sell_notes','bank_sell_t_c','bank_sell_d_d','bank_sell_t_t']] = csv2[['bank_buy_notes','bank_buy_bill','bank_buy_t_c','bank_buy_d_d','bank_buy_t_t','bank_sell_notes','bank_sell_t_c','bank_sell_d_d','bank_sell_t_t']].apply(lambda x: x*amount_)

        
        #csv2.replace(float(0),str('-'),inplace=True)
        for col in csv2.iloc[:,1:]:
            for row in range(len(csv2.index)):
                #csv2[col].iloc[row] = format(csv2[col].iloc[row],".2f")
                csv2[col].iloc[row] = round(csv2[col].iloc[row],2)
                if csv2[col].iloc[row] == 0:
                    csv2[col].iloc[row] = "-"

        #print(csv2)
        send = {'bestbank':bestbank,'allbank':csv2.to_dict('records')}
        return JsonResponse(send, safe=False)