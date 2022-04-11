import sys
from sys import argv
from matplotlib import ticker
import requests
import pandas as pd
import numpy as np
import os

import datetime

sys.path.insert(0, '../Pricing')
import compute_greeks


# User-defined functions for Series Applications


def getGreeks(greek, type, strike, underlyingPx, iv, rho, t):
    
    t = t/365

    if type == 'C':

        if greek == 'delta':
            return compute_greeks.Call.delta(underlyingPx, strike, iv, rho, t)

        if greek == 'gamma':
            return compute_greeks.Call.gamma(underlyingPx, strike, iv, rho, t)
        
        if greek == 'vega':
            return compute_greeks.Call.vega(underlyingPx, strike, iv, rho, t)

        if greek == 'theta':
            return compute_greeks.Call.theta(underlyingPx, strike, iv, rho, t)

        if greek == 'rho':
            return compute_greeks.Call.rho(underlyingPx, strike, iv, rho, t)

    if type == 'P':

        if greek == 'delta':
            return compute_greeks.Put.delta(underlyingPx, strike, iv, rho, t)

        if greek == 'gamma':
            return compute_greeks.Put.gamma(underlyingPx, strike, iv, rho, t)
        
        if greek == 'vega':
            return compute_greeks.Put.vega(underlyingPx, strike, iv, rho, t)

        if greek == 'theta':
            return compute_greeks.Put.theta(underlyingPx, strike, iv, rho, t)

        if greek == 'rho':
            return compute_greeks.Put.rho(underlyingPx, strike, iv, rho, t)



# Time to Expiration (Days in float)
def tte(col):
    return (float(col) - float(datetime.datetime.today().strftime('%s'))) / (60*60*24)



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

    # Price of the underlying at Request time
    underlyingPx = dates.optionChain[1][0]['quote']['regularMarketPrice']

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

        puts['TTE'] = puts.apply(lambda x: tte(x.expiration), axis=1)

        puts['delta'] = puts.apply(lambda x: getGreeks('delta', 'P', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)
        puts['gamma'] = puts.apply(lambda x: getGreeks('gamma', 'P', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)
        puts['vega'] = puts.apply(lambda x: getGreeks('vega', 'P', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)
        puts['theta'] = puts.apply(lambda x: getGreeks('theta', 'P', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)
        puts['rho'] = puts.apply(lambda x: getGreeks('rho', 'P', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)

        calls = pd.DataFrame.from_records(all_exp[each].loc['options'][0][0]['calls'])
        calls['Type'] = "C"

        calls['TTE'] = calls.apply(lambda x: tte(x.expiration), axis=1)

        calls['delta'] = calls.apply(lambda x: getGreeks('delta', 'C', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)
        calls['gamma'] = calls.apply(lambda x: getGreeks('gamma', 'C', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)
        calls['vega'] = calls.apply(lambda x: getGreeks('vega', 'C', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)
        calls['theta'] = calls.apply(lambda x: getGreeks('theta', 'C', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)
        calls['rho'] = calls.apply(lambda x: getGreeks('rho', 'C', x.strike, underlyingPx, x.impliedVolatility, 0.05, x.TTE), axis = 1)


        outname = req.headers['date'] + '.csv'

        outdir = '../../Data/' + ticker + '/' + str(each) + '/'
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        puts.append(calls).to_csv(outdir + outname)


if __name__ == '__main__':

    main(argv[1])



