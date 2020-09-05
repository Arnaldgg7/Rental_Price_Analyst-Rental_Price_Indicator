# This Python file uses the following encoding: utf-8

"""
This program has been created to be scheduled and executed daily to fetch the required information from the web. Please, schedule it daily in 'Task Scheduler' of your OS and only open it to be executed manually if some error arise (see information below).

IMPORTANT: When reCAPTCHA filter blocks the program on the website due to the detection of a non-user accessing to the website, you will be issued by email to the email provided next to this paragraph (in email_error).

Then, once the program is opened with an IDE to be executed manually, do the following steps:
1. Change the following variable 'manual_execution' to 'YES', instead of the default 'NO'.
2. Increase number of seconds of the following variable 'time_recaptcha' to 120.
3. Remove the 'chome-data' folder of the current directory of this program to avoid being detected again as the same user.
5. Execute manually the program to overcome the reCAPTCHA filter in the web browser when it appears, and wait for the end of the execution.

By this way, you will be able to overcome the reCAPTCHA filter and let the program continue scraping until it finishes.

If you want to receive the monthly statistics about market house rental prices, and also the error emails when the information cannot be fetched (case aforementioned), change the email_error and the email_send variables stated next to this paragraph by your email.

"""

email_error= 'Arnaldgg7@gmail.com'
email_send= 'Arnaldgg7@gmail.com'
manual_execution= 'YES'
time_recaptcha= 100
huge_data= 1

from bs4 import BeautifulSoup
import pandas
import re
import os
import time
from random import randint
from datetime import date, timedelta
import matplotlib.pyplot as plt
import mpld3
from matplotlib import style
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from dateutil.relativedelta import relativedelta
from selenium.webdriver import Chrome, ChromeOptions
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def parking(value):
    if value == 0:
        return "No"
    else:
        return "Yes"

def error_email(email):
    day= date.today().strftime('%d-%m-%Y')
    subject= 'Execution program failed in ({}) - reCAPTCHA filter detected'.format(day)
    text= 'Execution of the Python program has failed due to the existence of a reCAPTCHA filter.<br> <strong>Please, execute manually the program and manage the captcha request in order to fetch the information required.</strong>'
    email_to= email
    email_from= 'testmailarn7@gmail.com'
    password_from= 'HoLaEmDiCArNaLd77@'
    
    msg=MIMEText(text, "html")
    msg['To']= email_to
    msg['From']= email_from
    msg['Subject']= subject
    
    gmail= smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(email_from, password_from)
    gmail.send_message(msg)

def send_email(email, price, rooms, meters, floor, parking, sqmp):
    month= date.today().strftime('%B')
    subject= 'Monthly Summary - Salou rental prices ({})'.format(month)
    text= 'Monthly statistics about evolution of rentals in Salou (Tarragona):<br> Monthly average rental price: <strong>{}€</strong><br> Average of rooms: <strong>{} rooms</strong><br> Average square meters per house: <strong>{}m2</strong><br> Most usual floor: <strong>floor {}</strong><br> Usually parking included: <strong>{}</strong><br> Square meter price average: <strong>{}€/m2</strong><br><br> Attached graphic information about available entire time range:<br> <strong>1. Price Mean evolution.<br> 2. Price Standard Deviation evolution.<br> 3. Square Meter Price evolution.<br> 4. Evolution of number of houses for rent.</strong><br><br> All plotted information is differentiated into:<br> - Houses for rent on each datetime.<br> - Rented houses, stated before on the website and then removed from website on each date due to the rental commitment.<br><br><strong>Attached extra-file with graphic information in HTML to download and manipulate interactively the data.</strong>'.format(price, rooms, meters, floor, parking, sqmp)
    email_to= email
    email_from= 'testmailarn7@gmail.com'
    password_from= 'HoLaEmDiCArNaLd77@'
    
    msg= MIMEMultipart()
    msg['To']= email_to
    msg['From']= email_from
    msg['Subject']= subject
    
    msgText=MIMEText(text, "html")
    msg.attach(msgText)
    
    html_graph= 'graph.html'
    fp1= open(html_graph, 'rb')
    p= MIMEBase('application', 'octet-stream')
    p.set_payload(fp1.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', 'fp1; filename= {}'.format(html_graph),)
    msg.attach(p)
    fp1.close()
    
    image='graph.jpg'
    fp2= open(image, 'rb')
    img= MIMEImage(fp2.read())
    fp2.close()
    img.add_header('Content-Disposition', 'fp2; filename= {}'.format(image),)
    msg.attach(img)
    
    gmail= smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(email_from, password_from)
    gmail.send_message(msg)

def remove_dot(x):
    return re.sub(r"(?<=\d)[.]", r"", x)

def fetch_number(num):
    return re.search(r"\d+", num).group()

def random_user_agent(file):
    with open(file,"r") as fp:
        users= fp.readlines()
    number= randint(0,len(users)-1)
    random_choice= users[number]
    return random_choice.strip()

def check_new_page(item):
    if i>1:
        try:
            prev= item.find('div', {'class':'pagination'})
            link= prev.find('a', {'class':'icon-arrow-left'})
            if link.find('span').text == "Anterior":
                pass
        except:
            return "End"


today= pandas.to_datetime('today').strftime('%m-%d-%Y')
l=[]
i=1
length=0
while True:
    url='https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/con-precio-hasta_1200,de-dos-dormitorios,de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas/pagina-{}.htm'.format(i)
    user_agent= random_user_agent('useragents.txt')
    webdriver='chromedriver.exe'

    options= ChromeOptions()
    options.add_argument('--user-agent={}'.format(user_agent))
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--user-data-dir=chrome-data')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)    
    driver= Chrome(webdriver, options=options)

    driver.get(url)
        
    soup= BeautifulSoup(driver.page_source, 'html.parser')
    
    if soup.find_all('div', {'class':'item-info-container'}):
        length= int(remove_dot(soup.find_all('span', {'class':'breadcrumb-info'})[-1].text))
        listData= len(l)
        print(length)
        print(listData)
        if check_new_page(soup) == "End":
            if listData < length*huge_data and i != 61:
                print("ENTRANT EN EL LOOP DE TORNAR A COMENÇAR!DADES ACTUALS:")
                print(length)
                print(listData)                
                i=1
                driver.quit()
                continue
            else:
                data="YES"
                driver.quit()
                break

    else:    
        if listData != 0 and listData >= length*huge_data:
            data="YES"
            driver.quit()
            break
        else:
            time.sleep(time_recaptcha)
            data= manual_execution
            if data=="NO":
                error_email(email_error)
                driver.quit()
                break
            driver.quit()
            continue
    
    driver.quit()
    
    all= soup.find_all('div', {'class':'item-info-container'})
    
    for item in all:
        d={}
        Articles = item.find_all('a')
        Article_num= ""
        for a in Articles:
            try:
                Article_num= re.search(r"inmueble/(\d+)/", a['href']).group(1)
            except:
                continue
        
        if Article_num != "":
            d["Article"]= Article_num
        else:
            continue
        
        try:
            Price= item.find('div', {'class':'row price-row clearfix'})
            Price= Price.find('span', {'class':'item-price h2-simulated'}).text
            Price= remove_dot(Price)
            Price= fetch_number(Price)
            d["Price"]=Price
        except:
            d["Price"]=None
        
        try:
            Parking= item.find('span', {'class':'item-parking'}).text
            if "Garaje" in Parking:
                d["Parking"]= 1
        except:
            d["Parking"]= 0
        
        for detail in item.find_all('span', {'class':'item-detail'}):
            detail=remove_dot(detail.text)
            try:
                if "hab" in detail:
                    Rooms= fetch_number(detail)
                    d["Rooms"]=Rooms
            except:
                d["Rooms"]=None
            
            try:
                if "m" in detail:
                    Meters= fetch_number(detail)
                    d["Meters"]=Meters
            except:
                d["Meters"]=None
            
            try:
                if "planta" in detail:
                    Floor= fetch_number(detail)
                    d["Floor"]=Floor
            except:
                d["Floor"]=None
        
        try:
            d["Sqmp"]= round(int(Price)/int(Meters),2)
        except:
            d["Sqmp"]=None
                
        d["Date"]=today
        
        l.append(d)
        
    i+=1


if data == "YES":
    df= pandas.DataFrame(l, columns=["Date", "Article", "Price", "Parking", "Rooms", "Meters", "Floor", "Sqmp"])
    df.set_index("Date", inplace=True)
    df["Floor"].fillna(0, inplace=True)
    df.drop_duplicates(subset=["Article"], inplace=True)

    if not os.path.isfile('database.csv'):
        df.to_csv('database.csv')
        df= pandas.read_csv('database.csv', index_col=0)
        df= df[ (df.index==today) ]
        df_out= df.drop(df.index[:],0)
        df_out.to_csv('database2.csv')
        temp_df= df_out
    else:
        df.to_csv('database.csv', mode='a', index=True, header=0)
        df= pandas.read_csv('database.csv', index_col=0)
        df= df[ (df.index==today) ]
        temp_df= pandas.read_csv('database3.csv', index_col=0)
    
    out_items= list(set(temp_df["Article"]).difference(set(df["Article"])))
    
    if len(out_items)>0:
        items=pandas.DataFrame()
        for element in out_items:
            append_data= temp_df.loc[temp_df["Article"]==element]
            df_out= items.append(append_data, ignore_index=False)
        df_out.to_csv('database2.csv', mode='a', index=True, header=0)
    
    df.to_csv('database3.csv')
    
    today= date.today()

    if ((today+timedelta(days=1)).strftime('%d')) == "12":
        style.use('seaborn-darkgrid')
        graph= plt.figure(figsize=(12,7))
        
        ax1= plt.subplot2grid((2,3),(0,0), colspan=2)
        plt.ylabel('Price (€)')
        plt.title('Price MEAN')
        
        ax2= plt.subplot2grid((2,3),(1,0), colspan=2, sharex=ax1)
        plt.xlabel('Date')
        plt.ylabel('Deviation (€)')
        plt.title('Price STD')
        
        ax3= plt.subplot2grid((2,3),(0,2))
        plt.ylabel('Price(€)')
        plt.title('Square meter price')
        
        ax4= plt.subplot2grid((2,3),(1,2), sharex=ax3)
        plt.xlabel('Date')
        plt.ylabel('Number of houses')
        plt.title('Number of houses')
        
        df= pandas.read_csv('database.csv', index_col=0, parse_dates=["Date"]).dropna(subset=["Sqmp"])
        df_out= pandas.read_csv('database2.csv', index_col=0, parse_dates=["Date"]).dropna(subset=["Sqmp"])
        if df_out.dropna().empty:
            df_out=df
        
        df["curr_mean"]= df["Price"].resample('D').mean()
        df_out["sold_mean"]= df_out["Price"].resample('D').mean()
        df["curr_std"]= df["Price"].resample('D').std()
        df_out["sold_std"]= df_out["Price"].resample('D').std()
        df["curr_sqm"]= df["Sqmp"].resample('D').mean()
        df_out["sold_sqm"]= df_out["Sqmp"].resample('D').mean()
        df["curr_num"]= df["Article"].resample('D').count()
        df_out["sold_num"]= df_out["Article"].resample('D').count()
        
        ax1.plot(df.index, df.curr_mean, c='darkblue', label='Available house rentals')
        ax1.plot(df_out.index, df_out.sold_mean, c='green', label='Rented houses')
        ax1.legend()
        ax2.plot(df.index, df.curr_std, c='darkblue', label='Available house rentals')
        ax2.plot(df_out.index, df_out.sold_std, c='green', label='Rented houses')
        ax2.legend()
        ax3.plot(df.index, df.curr_sqm, c='darkblue', label='Available house rentals')
        ax3.plot(df_out.index, df_out.sold_sqm, c='green', label='Rented houses')
        ax3.legend()
        ax4.plot(df.index, df.curr_num, c='darkblue', label='Available house rentals')
        ax4.plot(df_out.index, df_out.sold_num, c='green', label='Rented houses')
        ax4.legend()
        
        locator= mdates.AutoDateLocator(minticks=1, maxticks=10)
        formatter= mdates.ConciseDateFormatter(locator)
        
        ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        ax2.xaxis.set_major_locator(locator)
        ax2.xaxis.set_major_formatter(formatter)
        ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        ax3.yaxis.set_major_locator(ticker.MaxNLocator())
        
        ax4.xaxis.set_major_locator(locator)
        ax4.xaxis.set_major_formatter(formatter)
        ax4.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax3.get_xticklabels(), visible=False)
        plt.subplots_adjust(left=0.15, bottom=0.2, right=0.9, top=0.90, wspace=0.5, hspace=0.3)
        
        plt.savefig('graph.jpg', bbox_inches='tight')
        mpld3.save_html(graph, 'graph.html')
        
        df= df.drop(df.columns[-4:],1)
        df_out= df.drop(df.columns[-4:],1)
        
        df_exp= df.append(df_out, sort=False).dropna()
        df_exp= df_exp[ (pandas.to_datetime(today-relativedelta(months=+1)) <= df_exp.index) & (df_exp.index <= pandas.to_datetime('today')) ]
        
        email_=email_send
        price_= round(df_exp.Price.mean(),2)
        rooms_= int(df_exp.Rooms.mean())
        meters_= int(df_exp.Meters.mean())
        floor_= int(df_exp.Floor.mean())
        parking_= parking(round(df_exp.Parking.mean()))
        sqmp_= round(df_exp.Sqmp.mean(),2)
        
        send_email(email_, price_, rooms_, meters_, floor_, parking_, sqmp_)