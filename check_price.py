import time
import requests
from bs4 import BeautifulSoup
import datetime
import os
import csv
import smtplib


# --- Email alert function ---
def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login('user@gmail.com', 'xxxxxxxxx')
    subject = "Price Alert: Christmas Nutcracker below 15€!"
    body = "The Christmas Countdown Wooden Nutcracker Soldier is below 15€. Check it now on Amazon: https://www.amazon.de/-/en/TWIDDLERS-Christmas-Nutcracker-Traditional-Decoration/dp/B0DDYBZC76/ref=sr_1_6?crid=1PEZI5UXOOM&dib=eyJ2IjoiMSJ9.wYM6q3Aevr8XSCUMo5JYLKdABUVjHGvZIz2zV1tuTpQszrOQ8ZI3liyJlhf9myO9CUxIc20JqF3Su8FS9P6b2qiD1eeWlSuyY7OT43wyqBUTbYvzMcpBMEkMWGzjFSl_RFD8Crjig4q3yYu5IO-BGgvRKj6TooC4BEpx4mIMwkmb4b1ZNOadZbep6-V9k-P7xzxI_R0uIlM_UP7due_JjPPed_A-Emtd-utr7FDe5lF6hVuxWvHyIp8i_6WRlirYVzNziYM-Zfsy7bTt_tSi4JP4RbB2NPdpsEJCGAbgWbc.U4EbBmlry8VUiCNRZigW2McLSFyq8plz4XYFQjsnoeM&dib_tag=se&keywords=nussknacker%2Bdeko&qid=1762432600&sprefix=nussknack%2Bdek%2Caps%2C338&sr=8-6&th=1"
    msg = f"Subject: {subject}\n\n{body}".encode('utf-8')
    server.sendmail('user@gmail.com', 'user@gmail.com', msg)
    server.quit()


# --- Price checking function ---
def check_price():
    try:
        
        url ="https://www.amazon.de/-/en/TWIDDLERS-Christmas-Nutcracker-Traditional-Decoration/dp/B0DDYBZC76/ref=sr_1_6?crid=1PEZI5UXOOM&dib=eyJ2IjoiMSJ9.wYM6q3Aevr8XSCUMo5JYLKdABUVjHGvZIz2zV1tuTpQszrOQ8ZI3liyJlhf9myO9CUxIc20JqF3Su8FS9P6b2qiD1eeWlSuyY7OT43wyqBUTbYvzMcpBMEkMWGzjFSl_RFD8Crjig4q3yYu5IO-BGgvRKj6TooC4BEpx4mIMwkmb4b1ZNOadZbep6-V9k-P7xzxI_R0uIlM_UP7due_JjPPed_A-Emtd-utr7FDe5lF6hVuxWvHyIp8i_6WRlirYVzNziYM-Zfsy7bTt_tSi4JP4RbB2NPdpsEJCGAbgWbc.U4EbBmlry8VUiCNRZigW2McLSFyq8plz4XYFQjsnoeM&dib_tag=se&keywords=nussknacker%2Bdeko&qid=1762432600&sprefix=nussknack%2Bdek%2Caps%2C338&sr=8-6&th=1"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"}
        page = requests.get(url, headers = headers)
        
        soup1 = BeautifulSoup(page.content, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

        title_tag = soup2.find(id="productTitle")
            if title_tag:
                title = title_tag.get_text(strip=True)
            else:
                title = "Unknown title"

        price_container = soup2.find("span", class_="a-price")
        whole = price_container.find("span", class_="a-price-whole").get_text(strip=True).replace(".", "")
        fraction = price_container.find("span", class_="a-price-fraction").get_text(strip=True)
        price = float(f"{whole}.{fraction}")

        today = datetime.date.today()
        formatted_date = today.strftime("%d/%m/%Y")
        print(f"Price on {formatted_date}: {price}€")

        # csv setup
        file_path = 'AmazonWebScraperDataset.csv'
        header = ['Title', 'Price (€)', 'Date']
        data = [title, price, formatted_date]
        
        # create file if it doesn't exist
        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a+', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(data)
    
        # alert if price below threshold
        if price < 15.00:
            print(f"Price dropped! Current price: {price}€")
            send_mail()
            print("Email Sent!")

    except Exception as e:
        print("⚠️ Error:", e)


if __name__ == "__main__":
    while True:
        check_price()
        time.sleep(86400) # run every 24 hours
        