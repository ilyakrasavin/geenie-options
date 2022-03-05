from sys import argv
from matplotlib import ticker
import requests
import pandas as pd
import numpy as np
import os



def main(ticker):

    # Captures the Equity page to retrieve Expiration Dates

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    ticker = ticker

    req = requests.get('http://query1.finance.yahoo.com/v7/finance/options/' + ticker, headers = headers)


    # Decode the response
    dates = pd.read_json(req.content.decode())

    # Translate Unix Timestamps into Python TimeDate 
    dates_unix = dates.optionChain[1][0]['expirationDates']
    dates_timedate = pd.to_datetime(dates_unix, origin='unix', unit = 's')

    # Convert to Human-readable form
    dates_human = []
    for i, each in enumerate(dates_timedate):
        dates_human.append(str(each.year) + '-' + str(each.month) + '-' + str(each.day))


    # Request Option chains for each corresponding Expiration Date (Human-Readable)

    all_exp = {}
    for i, exp_date in enumerate(dates_unix):
        all_exp[dates_human[i]] = pd.read_json(requests.get('http://query1.finance.yahoo.com/v7/finance/options/' + ticker + '?date=' + str(exp_date), headers = headers).content.decode())


    # Convert the format from Dictionaries to Pandas Dataframes
    # Each Chain can now be accessed by quering 'YY-MM-DD' Expiration date in the Dictionary

    for each in all_exp:
        all_exp[each] = pd.DataFrame.from_dict(all_exp[each].optionChain.result[0], orient='index')

    # For each one of the Expiration Dates (Folder)
    # Retrieve and save the corresponding chains (Concatenated CALLS & PUTS) - Append a Type Column

    for each in dates_human:

        puts = pd.DataFrame.from_records(all_exp[each].loc['options'][0][0]['puts'])
        puts['Type'] = "P"
        calls = pd.DataFrame.from_records(all_exp[each].loc['options'][0][0]['calls'])
        calls['Type'] = "C"
        
        outname = req.headers['date'] + '.csv'

        outdir = './Data/' + ticker + '/' + str(each) + '/'
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        puts.append(calls).to_csv(outdir + outname)


if __name__ == '__main__':

    # Automation : In case they notice patterns...
    # Option 1 : Make n requests per day at set times
    # Option 2 : Make n requests per dat at set times +- some small epsilon
    # Option 3 : Make n requests per day at randomized times??


    main(argv[1])



