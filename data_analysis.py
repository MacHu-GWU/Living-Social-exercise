##encoding=UTF8
##version =Compatible to py27, py33
##autho   =Sanhe
##Date    =2014-10-17

from __future__ import print_function
import pandas as pd
from matplotlib import pyplot as plt
from collections import OrderedDict
from itertools import count

def hist(array):
    """frequency analysis"""
    res = dict()
    for i in array: 
        if i not in res: 
            res[i] = 1
        else:
            res[i] += 1
    return res

def analysis_create_date(array):
    hist_create_date = hist(array)
    od = OrderedDict( sorted(list(hist_create_date.items()), # order dict by value
                             key=lambda t: t[1],
                             reverse = True) )
    c = count()
    for k, v in od.items(): # view frequency of date
        print("[%s] %s => %s" % (c.next(), k, v))
    
    date_list = list(od.keys())
    date_list.sort()
    print(date_list) # check date range

def analysis_first_buy(array):
    hist_first_buy = hist(array)
    
    for k, v in hist_first_buy.items(): # view frequency of first_buy_day
        print("%s days = %.6f" % (k, float(v)/3000000) )
        
    ## plot bar chart
    n, bins, patches = plt.hist(array, # patches not important
                                bins = 99, # number of bins
                                normed = True, # ie the integral of the histogram will sum to 1
                                facecolor='green', # bin color
                                cumulative = True, # plot cdf rather than pdf
                                alpha= 0.75) # Transparency, 0 = blank, 1 = pure green
    print(n, bins, patches) # print bin detailed info
    plt.show()
    
def analysis_number_of_buy(array):
    hist_first_buy = hist(array)
    total = sum([k * v for k, v in hist_first_buy.items()]) # total of orders
    
    cumulative = 0.
    print("number_of_buy    how_many_customer_did    number_of_orders_they_made    cumulative_percentage")
    for k, v in hist_first_buy.items():
        cumulative += k * v
        print("{0[0]:<10}{0[1]:<10}{0[2]:<10}{0[3]:<30}".format((k, v, k*v, cumulative/total)) ) 
    print("total of orders = %s" % total) # 8936936, 5407926

def link_analysis1(data):
    """TODO
    """
    criterion1 = data["first_buy"].map(lambda x: x == 21) # first_buy criterion
    criterion2 = data["number_of_buy"].map(lambda x: x >= 2) # then buy more than 2 (2-5 is valuable customer)
    print( float(data[criterion1 & criterion2].shape[0]) / data[criterion1].shape[0])
    
def link_analysis2(data):
    """TODO
    """
    criterion1 = data["first_buy"].map(lambda x: x == 8) # first_buy criterion
    criterion2 = data["number_of_buy"].map(lambda x: (x >= 2) & (x <= 5)) # then buy more than 2-5 item
    print( float(data[criterion1 & criterion2].shape[0]) / data[criterion1].shape[0])

data = pd.read_csv("data.csv", header = None, names = ["create_date", "first_buy", "number_of_buy"])

analysis_create_date(data["create_date"].values)
analysis_first_buy(data["first_buy"].values)
analysis_number_of_buy(data["number_of_buy"].values)

link_analysis1(data)
link_analysis2(data)
