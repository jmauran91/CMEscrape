import csv
import xlsxwriter
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import pdb
import urllib.request as u



def scrape(url):
    # set the header to make it seem to CME that the request is human
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    header = {'User-Agent': user_agent}

    # make the request
    session = requests.Session()
    response = session.get(url, headers=header)

    # get the response into a readable form
    soup = bs(response.content, 'lxml').prettify()
    # print(soup)

    # make dataframe out of response and return
    df = pd.DataFrame(response.json())
    return df

def parse(url):
    raw = scrape(url)
    futures = {}

    ## go through the data frame
    for i in range(len(raw.values)):
        ## get the maturities and last price of Eurodollar Futures
        key = raw.values[i][3]['expirationMonth']
        val = raw.values[i][3]['last']
        ## dump these into a dictionary
        futures[key] = val
        date = raw.values[0][3]['updated']
        data = []
        data.append(date)
        data.append(futures)

    ## return the dictionary
    return data


def main():

    ### JSON FOR EURODOLLAR FUTURES
    url = "https://www.cmegroup.com/CmeWS/mvc/Quotes/Future/1/G?isProtected&_t=1657139488401"
    ### JSON FOR EURODOLLAR FUTURES
    data = parse(url)
    print(data)
    #take the dictionary from parse and write the values into
    #a csv -> excel spreadsheet
    workbook = xlsxwriter.Workbook('EDF.xlsx')
    worksheet = workbook.add_worksheet()
    row, col = 0, 1
    # write the Date of this data into excel
    worksheet.write(row, col, data[0])
    row += 2
    # now write the quotes into excel
    for i in data[1].keys():
        if data[1][i] != '-':
            numby = 100 - float(data[1][i])
            worksheet.write(row, col, i)
            worksheet.write(row, col+1, numby)
            row+=1

    workbook.close()
    print('Script complete')


if __name__ == "__main__":
    main()
