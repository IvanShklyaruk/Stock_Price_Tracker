from bs4 import BeautifulSoup
import requests
import time
import smtplib

# Input Any Yahoo Finance Stock Link.
STOCK_URL = "ENTER LINK HERE"
# Input Your Email
EMAIL = "ENTER EMAIL HERE"
# Input Your Email Password.
PASSWORD = "ENTER PASSWORD HERE"
# Input the Price you are Waiting for.
WANTED_PRICE = 100

# Obtains the stock price data.
def get_price():
    page = requests.get(STOCK_URL)
    soup = BeautifulSoup(page.text, 'lxml')
    price = soup.find('span', class_ = 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)').text
    print(price)
    return price

# Determines if the price is what the client is waiting for.
def track_price():
    price = float(get_price())       
    if price > WANTED_PRICE:
        diff = price - WANTED_PRICE
        print(f"It's still {diff} too expensive")
        return True
    else:
        print("Cheaper!!")
        send_email()
        return False

# Email notification is sent to the client if the stock price drops.
def send_email():
    subject = "Stock Price Has Dropped!"
    body = "Check " + STOCK_URL
    msg = f"Subject: {subject}\n\n{body}"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, EMAIL, msg)
    print("EMAIL HAS BEEN SENT!")
    server.quit()

# Infinite loop to keep the code running until the wanted price is found.
while(True):
    still_waiting = track_price()
    if still_waiting == False:
        break
    time.sleep(60)


