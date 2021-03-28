#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 14:33:29 2021

@author: eliaskarikas
"""

import pandas as pd

alldata = "owid-covid-data.csv"
testing = "covid-19-testing-policy.csv"
contact = "covid-contact-tracing.csv"
face = "face-covering-policies-covid.csv"
school = "school-closures-covid.csv"
work = "workplace-closures-covid.csv"

data = pd.read_csv(alldata)
testingpd = pd.read_csv(testing)
contactpd = pd.read_csv(contact)
facepd = pd.read_csv(face)
schoolpd = pd.read_csv(school)
workpd = pd.read_csv(work)

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
cases = cases.fillna(0)

# limiting rows in a df to certain amount, to easily manipulate
testcases = (cases.head(100))

# all column headers, for reference
print(list(cases.columns.values))
