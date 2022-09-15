#Created by Mohd Azhar Amrie - 12/9/2022

#Import library
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

#Set the base URL
baseurl = 'http://books.toscrape.com/catalogue/'

#Set the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

#Define an array to store links
booklinks = []

for x in range(1, 51):
    r = requests.get(f'http://books.toscrape.com/catalogue/page-{x}.html')
    soup = BeautifulSoup(r.content, 'html.parser')
    booklist = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    for item in booklist:
        for link in item.find_all('a', href=True):
            booklinks.append(baseurl + link['href'])
            break

#Define an array to store every book details            
listbuku = []

for link in booklinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    name = soup.find('h1').text
    price = soup.find('p', class_='price_color').text
    stock = soup.find('p', class_='instock availability').text.strip()

    buku = {
        'Book Title': name,
        'Price': price,
        'Stock Status': stock
    }

    listbuku.append(buku)
    
df = pd.DataFrame(listbuku)
print(df.head(10))

#Saving data into excel file - set your path
df.to_excel(r'C:\Users\Azhar Amrie\Desktop\scraped-book.xlsx', index=False, header=True)

print('')
print('')
print(' =========== SAVED SUCCESSFULLY ===========')
print('')
print('')

