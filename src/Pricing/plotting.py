from sys import argv
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime
import numpy as np

import subprocess

# Helper Class
class PlottingHelper:

    # Constructs and returns the horzontal axis containing Date of Expiration values.
    # Traverses directories and selects dates based on the mode chosen.
    
    # Modes: Exact, Range, Quarterly(Regular), Weeklies
    def getDoeAxis(self, ticker, mode, args):

        # Read in all Expirations available for the corresponding Ticker
        pathk = "../../Data/" + str(ticker) + "/"
        expirations_all = os.listdir(path = pathk)

        # Collects valid expirations as per the mode chosen
        valid_expirations = []
        today_y = datetime.datetime.today().strftime('%y')
        today_m = datetime.datetime.today().strftime('%m')
        today_d = datetime.datetime.today().strftime('%d')


        # Range + (30D / 60D / 90D / 180D / 1Y / 1Y6M / 2Y / Max) as String
        # Defaults to MAX range on ambiguos/uninitialized range arguments
        if (mode == 'range'):

            match args:

                # Expirations within one month away from today (Uses the same date)
                case '30D':
                    
                    # Collect valid expirations
                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference <= 30 and dayDifference >= 0:
                            valid_expirations.append(each)
                    
                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()
        
                    return valid_expirations_sorted


                # Expirations within two months away from today (Uses the same date)
                case '60D':

                    # Collect valid expirations
                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference <= 60 and dayDifference >= 0:
                            valid_expirations.append(each)

                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()

                    return valid_expirations_sorted

                # Expirations within three months away from today (Uses the same date)
                case '90D':

                    # Collect valid expirations
                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference <= 90 and dayDifference >= 0:
                            valid_expirations.append(each)
                    
                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()

                    return valid_expirations_sorted                   

                # Expirations within six month away from today (Uses the same date)
                case '180D':

                    # Collect valid expirations
                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference <= 180 and dayDifference >= 0:
                            valid_expirations.append(each)
                    
                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()

                    return valid_expirations_sorted
                
                # Expirations within one year away from today (Uses the same date)
                case '1Y':

                    # Collect valid expirations
                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference <= 365 and dayDifference >= 0:
                            valid_expirations.append(each)
                    
                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()

                    return valid_expirations_sorted


                # Expirations within one month away from today
                case '1Y6M':

                    # Collect valid expirations
                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference <= 548 and dayDifference >= 0:
                            valid_expirations.append(each)
                    
                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()

                    return valid_expirations_sorted                    


                # Expirations within one month away from today
                case '2Y':

                    # Collect valid expirations
                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference <= 730 and dayDifference >= 0:
                            valid_expirations.append(each)
                    
                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()

                    return valid_expirations_sorted                          

                # Expirations within one month away from today
                case '3Y':

                    # Collect valid expirations
                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference <= 1095 and dayDifference >= 0:
                            valid_expirations.append(each)
                    
                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()

                    return valid_expirations_sorted  

                # Use all available Expiration Dates Past Today
                case 'MAX':

                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference >= 0:
                            valid_expirations.append(each)

                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()
        
                    return valid_expirations_sorted

                # Defaults to Maximum
                # !!! MAX CODE REPEATED !!!
                case _:

                    for each in expirations_all:

                        # Take the difference in days
                        dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                        # Add expirations in the current month past today
                        if each not in valid_expirations and dayDifference >= 0:
                            valid_expirations.append(each)

                    # Sort the Expirations for Axis Arrangement Consistency
                    valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
                    valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()
        
                    return valid_expirations_sorted



        # Exact + Args: date in Y-M-D format
        # Chosen by a user from the menu list

        if (mode == 'exact') and (args != 0):
            
            for each in expirations_all:

                if each not in valid_expirations and each == args:
                    valid_expirations.append(each)
        
            return pd.to_datetime(valid_expirations)


        # Quarterlies
        if (mode == 'quarterly'): 

            for each in expirations_all:

                # Take the difference in days
                dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                if each not in valid_expirations and dayDifference >= 0 and self.isQuarterly(each):
                    valid_expirations.append(each)

            valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
            valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()
        
            return valid_expirations_sorted


        # Weeklies
        if (mode == 'weekly'): 

            for each in expirations_all:

                # Take the difference in days
                dayDifference = (pd.to_datetime(each) - datetime.datetime.today()).days

                if each not in valid_expirations and dayDifference >= 0 and self.isWeekly(each):
                    valid_expirations.append(each)

            valid_expirations_sorted = pd.to_datetime(valid_expirations).sort_values()
            valid_expirations_sorted = valid_expirations_sorted.to_pydatetime()
        
            return valid_expirations_sorted

    

    # Third friday can be between 14th (Month starts on Friday) and 21st (Month starts on Monday) of the month
    def isThirdFriday(self, doe_string):
        stringDT = pd.to_datetime(doe_string)
        return (stringDT.weekday() == 4 and stringDT.day > 14 and stringDT.day <= 21)


    # January - 1 / February - 2 / March - 3
    # Third fridays of which months?
    def getCycle(self, doe_string):
        yield

    # Assure is a regular cycle option
    def isQuarterly(self, doe_string):
        return self.isThirdFriday(doe_string)

    # Not expiring on the third friday
    def isWeekly(self, doe_string):
        return not (self.isThirdFriday(doe_string))


# Main Plotting Facility Class
class PlottingMain:

    # Plots specified metrics for ATM options of Given Expiration Dates

    # Expected Input:
    # o_type: Contract Type: C / P / B (for C & P)
    # DOE Type: Exact, Range, Quarterly, Weeklies + ARGS as a LIST
    # metric: string
    # atm_price: as float

    def plotDoeATM(ticker, o_type, doe_type, metric, atm_price):

        # Helper Instance Initialized
        plotHelper = PlottingHelper()

        axis_type, axis_range = doe_type

        # Get X axis
        doe_axis = plotHelper.getDoeAxis(ticker, axis_type, axis_range)

        data_axis = dict()

        # Retrieve data from the latest file of a corresponding Expiration Date
        for each in doe_axis:

            indir = '../../Data/' + ticker + '/' + str(each.year) + '-' + str(each.month) + '-' + str(each.day) + '/'
            list = os.listdir(path = indir)

            list_paths = [indir + filename for filename in list]

            newest = max(list_paths, key = os.path.getctime)

            # Reads in the CSV for the corresponding DOEs:
            data = pd.read_csv(newest, sep = ',')
            data = data[data.Type == o_type][data.strike == atm_price][metric]

            data_axis[str(each.year) + '-' + str(each.month) + '-' + str(each.day)] = data

        # Construct Both axes
        list_axis = []
        list_values = []
        
        # Check for missing data values
        # Select the ones that are present
        for doe_data_idx in [str(each.year) + '-' + str(each.month) + '-' + str(each.day) for each in doe_axis]:

            # Handling empty lists of values
            if(len(data_axis[doe_data_idx].values) != 0):
                list_axis.append(doe_data_idx)
                list_values.append(data_axis[doe_data_idx].iloc[0])


        # Produce the plot
        plt.figure(figsize = (40, 20))
        plt.plot(list_axis, list_values)

        plt.rc('xtick', labelsize=35) 
        plt.rc('ytick', labelsize=35)

        plt.legend([metric], fontsize = 35)

        imagename = ticker + '-' + str(datetime.datetime.today().year) + '-' + (str(datetime.datetime.today().month)) + '-' + str(datetime.datetime.today().day) + '-' + str(datetime.datetime.today().hour) + str(datetime.datetime.today().minute) + str(datetime.datetime.today().second)

        plt.savefig('../../Images/' + imagename + '.jpeg', dpi = 'figure', bbox_inches='tight')

        # Print is captured by the Bot (Should be made a return statement for autonomous functioning)
        print(imagename + '.jpeg')



    # Plots Multiple Curves (Different Expiration Dates) for the specified strike range
    def plotDoeStrike(ticker, o_type, strike_range, doe_mode, metric):

        plottingHelper = PlottingHelper()

        doe_mode = doe_mode[0] 
        doe_args = doe_mode[1]

        # Get DOE axes (Used for data retrieval)
        doe_axis = plottingHelper.getDoeAxis(ticker, doe_mode, doe_args)

        # Retrieve the Strike_range Axis / values for the chosen option type
        data_axis = dict()

        strike_axis_ticks = []

        # Traverse the expiration axis

        data_strikes = dict()

        # Retrieve Data for Each expiration (Bounded by Strike ranges)
        for each in doe_axis:

            indir = '../../Data/' + ticker + '/' + str(each.year) + '-' + str(each.month) + '-' + str(each.day) + '/'
            list = os.listdir(path = indir)

            list_paths = [indir + filename for filename in list]

            newest = max(list_paths, key = os.path.getctime)

            # Reads in the CSV for the corresponding DOEs:
            data = pd.read_csv(newest, sep = ',')
            
            data = data[data.Type == o_type][data.strike >= int(strike_range[0])][data.strike <= int(strike_range[1])]

            strike_axis_ticks.append(len(data))

            data_axis[str(each.year) + '-' + str(each.month) + '-' + str(each.day)] = data[metric]
            data_strikes[str(each.year) + '-' + str(each.month) + '-' + str(each.day)] = data.strike



        # Produce the plots

        i = 0

        plt.figure(figsize = (50, 20))

        # For each expiration
        for each1 in [str(each.year) + '-' + str(each.month) + '-' + str(each.day) for each in doe_axis]:

            # Handling empty lists of values
            if(len(data_axis[each1].values) != 0):
                # list_axis.append(each1)
                # list_values.append(data_axis[each1].iloc[0])
                plt.plot(data_strikes[each1], data_axis[each1], linewidth = 3)

            i = i + 1


        plt.rc('xtick', labelsize=48) 
        plt.rc('ytick', labelsize=48)

        plt.legend(data_strikes.keys(), fontsize = 35)

        imagename = ticker + '-' + str(datetime.datetime.today().year) + '-' + (str(datetime.datetime.today().month)) + '-' + str(datetime.datetime.today().day) + '-' + str(datetime.datetime.today().hour) + str(datetime.datetime.today().minute) + str(datetime.datetime.today().second) + '::' + str(strike_range[0]) + '-' + str(strike_range[1])

        plt.savefig('../../Images/' + imagename + '.jpeg', dpi = 'figure', bbox_inches='tight')
        # Plot metrics (X DOE curves + corresponding values)

        print(imagename + '.jpeg')


# Calls Corresponding plotting facilities
def main(ticker_passed, mode, opt_type, doe_type, doe_args, metric, atm_price_or_rangeBottom, range_upper = 0):
    
    # Make a Data Request
    subprocess.run(['python3', '../Requests/request_automatic.py', ticker_passed])

    if mode == '1':    
        PlottingMain.plotDoeATM(ticker_passed, opt_type, [doe_type, doe_args], metric, float(atm_price_or_rangeBottom))

    elif mode == '2':
        PlottingMain.plotDoeStrike(ticker_passed, opt_type, [float(atm_price_or_rangeBottom), float(range_upper)], [doe_type, doe_args], metric)



# Resolves the Program calls: Plotting Mode & Corresponding arguments
if __name__ == '__main__':

    # ATM data for Specified DOE
    if(argv[2] == '1'):
        main(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7])

    # DOE Curves for Specified Strike Ranges
    elif(argv[2] == '2'):
        main(argv[1], argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8])


