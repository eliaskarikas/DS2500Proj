#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 14:33:29 2021

@author: eliaskarikas
"""

import pandas as pd
import regex as rx
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import datetime as dt


alldata = "owid-covid-data.csv"
testing = "covid-19-testing-policy.csv"
contact = "covid-contact-tracing.csv"
face = "face-covering-policies-covid.csv"
school = "school-closures-covid.csv"
work = "workplace-closures-covid.csv"
travel = "international-travel-covid.csv"

data = pd.read_csv(alldata)
testingpd = pd.read_csv(testing)
contactpd = pd.read_csv(contact)
facepd = pd.read_csv(face)
schoolpd = pd.read_csv(school)
workpd = pd.read_csv(work)
travelpd = pd.read_csv(travel)
#travelpd["Day"]= pd.to_datetime(travelpd['Day'])
#travelpd['Day']=travelpd['Day'].astype(str)

# combining testing & contact set
testcont = pd.merge(testingpd, contactpd, how = 'left', 
                    on=['Entity','Code','Day'])
# Replacing nas with 0 
testcont["contact_tracing"]= testcont["contact_tracing"].fillna(0)
# combining school & workplace sets
schoolwork = pd.merge(workpd, schoolpd, how = 'left', 
                    on=['Entity','Code','Day'])
# Replacing nas with 0 
schoolwork["school_closures"] = schoolwork["school_closures"].fillna(0)


# Simplifying overall data set, to case data, & deaths
cases = data[data.columns[0:15]]
cases['population'] = data['population']
cases['HDI'] = data['human_development_index']
cases = cases.dropna(how='any')
cases = cases.rename(columns={"date": "Day", "iso_code":"Code","location":"Entity"})

cases1a = pd.merge(cases,travelpd, how='left',on=['Entity','Code','Day'])

cases1 = pd.merge(cases,schoolwork, how='left',on=['Entity','Code','Day'])

cases2 = pd.merge(cases1a,testcont, how='left',on=['Entity','Code','Day'])

cases2b = pd.merge(cases2,facepd, how='left',on=['Entity','Code','Day'])

#cases2b['Day']=cases2b['Day'].astype(str)

cases3 = pd.merge(cases2b,schoolwork,how='left',on=['Entity','Code','Day'])
#cases3['new_cases'].pct_change()
#dropping some columns of redundant data to get a better look at corr
casesdrop = cases3.drop(["new_cases_smoothed","new_deaths_smoothed",
                         "new_cases_smoothed_per_million","total_deaths_per_million",
                         "new_deaths_per_million","total_cases_per_million",
                         "new_cases_per_million"],axis=1)

# dropping any nas after merge
casesdrop = casesdrop.dropna(how='any')

date1 = casesdrop[casesdrop['Day'] == '2021-03-15']
date1 = date1[date1['HDI'] > .8 ]
date1['pop_pct'] = date1['total_cases']/date1['population']
date1['totalcases'] = date1['total_cases'].sum()
date1['pct_total'] = date1['total_cases']/date1['totalcases']
date1 = date1.sort_values(by='pop_pct',ascending=False)

date = date1.head(15)

casesdrop['total_cases'] = casesdrop['total_cases'].pct_change()
casesdrop['total_deaths'] = casesdrop['total_deaths'].pct_change()

# creating correlation array 
corrdf = casesdrop.corr()
corrdf.to_numpy()
# creating list of column names to better see on scatterplot
columnam = ['cases','new','deaths','new','population','travel','testing','tracing','coverings','work','school']

# focusing on first 5 columns in data set
a = casesdrop[0:5]

# generating subplots to more easily graph multiple variables at once.
fig, (ax1) = plt.subplots(1)


# creating heatmap of correlation b/w policy and case rates
#sns.heatmap(corrdf,annot=True, fmt='.2f',cmap='RdYlGn',xticklabels=columnam,yticklabels=columnam)
# issues: doesn't work linearly, covid cases continualy increase, 
# ofc there would be no signif correlation
# thoughts: want pct change in data instead


#days = cases['date'].str.replace('[{}]'.format(string.punctuation), '')
#cases["date1"] = cases['date'].str.replace('[^\w\s]','')
#days = cases[cases["date"] 20 "2020-12-31"]

# limiting rows in a df to certain amount, to easily manipulate
testcases = (cases.head(100))

# creating 
#datanz = casesdrop[(casesdrop['Entity']=='Costa Rica')]
#datanz = casesdrop[(casesdrop['Entity']=='Trinidad and Tobago')]
datanz = casesdrop[(casesdrop['Entity']=='New Zealand')]

datanz['total_cases'] = datanz['total_cases'].pct_change()
casesdrop['total_deaths'] = casesdrop['total_deaths'].pct_change()

dep = datanz.corr(method='kendall')
#datanz['total_cases'] = datanz['total_cases'].pct_change()
#datanz = casesdrop[(casesdrop['Entity']=='Ireland')|(casesdrop['Entity']=='New Zealand')|(casesdrop['Entity']=='Costa Rica')]

new = casesdrop[casesdrop['international_travel_controls'] == 3.0]
#africa = casesdrop[casesdrop['continent']=='Africa']
#sns.scatterplot(y = africa['new_cases'].pct_change(),x = africa['Day'],hue = africa['school_closures'])

#a_plot = sns.scatterplot(y = datanz['total_cases'],x = datanz['Day'],hue = datanz['workplace_closures'],palette='deep', ax=ax1)
#a_plot = sns.scatterplot(y = datanz['new_cases'],x = datanz['Day'],hue = datanz['workplace_closures'],palette='deep', ax=ax1)
#a_plot = sns.scatterplot(y = datanz['new_cases'],x = datanz['Day'],hue = datanz['facial_coverings'],palette='deep', ax=ax1)
#a_plot = sns.scatterplot(y = casesdrop['total_cases'],x = casesdrop['Day'],hue = casesdrop['facial_coverings'],palette='deep', ax=ax1)
#a_plot = sns.scatterplot(y = datanz['new_cases'],x = datanz['Day'],hue = datanz['international_travel_controls'],palette='deep', ax=ax1)
a_plot = sns.scatterplot(y = date['total_cases'],x = date['pop_pct'],hue = date['Entity'],palette='deep', ax=ax1)

#a_plot.set(ylim=(0, 310000))
#a_plot.set_xlim(-30, 450) 
#new_ticks = [i.get_text() for i in a_plot.get_xticklabels()]
#plt.xticks(range(0, len(new_ticks), 10), new_ticks[::10])
a_plot.set_title( "Cases by Population % (3/15/21)")  
"""
#sns.scatterplot(y = new['total_cases'],x = new['Day'],hue = new['continent'],ax=ax2)
#sns.scatterplot(y = new['total_deaths'],x = new['Day'],hue = new['continent'],ax=ax3)
h = casesdrop['facial_coverings']
corrdatanz = datanz.corr()

#sns.pairplot(a)
#sns.heatmap(corrdf,annot=True, fmt='.2f',cmap='RdYlGn',ax=ax1,xticklabels=columnam, yticklabels=columnam)

sns.heatmap(dep,annot=True, fmt='.2f',cmap='RdYlGn',ax=ax1,xticklabels=columnam, yticklabels=columnam)
def countrydf(df,country):
    return df[df['Entity']==country]
"""
def continentdf(df,country):
    return df[df['continent']==country]

def correaltionfinder(df,num,corr,cont,search):
    """ Gives data on countries that fit correlation metrics
    num indicates the relationship want to find corr for [5] travel, [6] testing,
    [7] tracing, [8] face masks, [9] workplace closures, [10] school closures
    corr is from -1 to 1 cont [1] continent, [2] country
    Search = continentdf OR countrydf"""
    
    countrylst = []
    lsit = []
    for row in range(len(df)):
        if df.iloc[row][cont] not in countrylst:
            countrylst.append(df.iloc[row][cont])
            newdf = search(df,df.iloc[row][cont])
            corrdf = newdf.corr()
            nmp = corrdf.to_numpy()
            if nmp[0][num] < corr:
                lsit.append(df.iloc[row][cont])
                
    return(lsit)
    

"""
def scatterplot(rowx,rowy):
    return sns.scatterplot(x = rowx,y=rowy)
# all column headers, for reference
#print(list(cases.columns.values))

#questions want to know to be answered by our data
    # continent differences
    #
    # haversine formula to see what companies are most like eachother in policy and cases

def moving_avg(df, col_name, hours):
    ''' Function: moving_avg        
    Parameters: dataframe with one row per timestamp,
                column name we're interested in,
                number of hours over which to calculate
    Returns: Nothing, modifies given dataframe
    '''
    
    
def plot_moving_avg(df, cols):
    ''' Function: plot_moving_avg
        Parameters: dataframe to plot, with moving avg columns in it
        Returns: nothing, just renders the plot (the overall numbers,
                  so we can compare to moving averages)    '''
        f, ax = plt.subplots(figsize = (6, 9))
        for col in cols:        
            sns.barplot(data = df, x = "Hour", y = col, label = col)    
            mvg_avg_cols = [col for col in df.columns if MOVING_AVG in col]    
            for ma in mvg_avg_cols:        
                sns.lineplot(data = df[ma], label = ma)    
                ax.legend(ncol = 1, loc = "upper right", frameon = True)    
                ax.set(xlim = (0, 24), ylabel = "", xlabel = "Hour of the Day")

def make_linreg(df, col, value, col2):
    ''' Function: make_linreg
        Parameters: dataframe, column to focus on, value we like
        Returns: modified dataframe, linreg stats    ''' 
        lin = df.loc[df[col] == value].reset_index()
        # Plot the linear regression    
        sns.regplot(x =lin.index,                
                    y = lin[col2])    
        plt.title(col + " " + str(value))   
        # Compute the linear regression  and return it     
        lr = stats.linregress(x = lin.index,
                              y = lin[col2])    
        return lin, lr
        
"""
