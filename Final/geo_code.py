#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 10:39:28 2021

@author: robertomoreno
"""

# THIS IS ONLY THE GEOPANDAS CODE PART ! 
# In order to run correctly, merge with the datacleaning.py file 

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt 
import PIL
import io


# Total Cases dataframe
world_covid = cases[["location", "date", "total_cases"]]
world_covid = world_covid.set_index("location")

# Dropping irrelevant names (continents, cities, etc.)
world_covid = world_covid.drop(["Africa", "Asia", "Europe", "European Union", 
                                "Hong Kong", "International", "Kosovo", 
                                "Macao", "North America", "Northern Cyprus",
                                "Oceania", "South America", "Taiwan", "World"])

world_covid = world_covid.pivot_table("total_cases", "location", "date")  
world_covid = world_covid.fillna(0) 

# Total Cases Throughout the World on a Certain Date  
print(world_covid["2021-03-26"].sum()) 

# Cases Per Million People dataframe 
world_per_milli = cases[["location", "date", "new_cases_per_million"]] 
world_per_milli = world_per_milli.pivot_table("new_cases_per_million", "location", "date")
world_per_milli = world_per_milli.fillna(0)  
# Transposition of dataframe with dates as rows
world_per_milli = world_per_milli.T  
world_per_milli.plot(y=["Africa", "Asia", "Europe", "North America", 
                        "South America", "Oceania"], use_index=True)  

# Creating a dataframe with countries' shapes
world_map = gpd.read_file("World_Countries_Generalized/World_Countries__Generalized_.shp") 
world_map = world_map.drop(["FID", "ISO", "COUNTRYAFF", "AFF_ISO"], axis = 1)


# Making country names the same in both dataframes
world_map.replace("Brunei Darussalam", "Brunei", inplace = True)
world_map.replace("Cabo Verde", "Cape Verde", inplace = True)
world_map.replace("Côte d'Ivoire", "Cote d'Ivoire", inplace = True)
world_map.replace("Czech Republic", "Czechia", inplace = True)
world_map.replace("Congo DRC", "Democratic Republic of Congo", inplace = True)
world_map.replace("Faroe Islands", "Faeroe Islands", inplace = True)
world_map.replace("Micronesia", "Micronesia (country)", inplace = True) 
world_map.replace("Cyprus", "Cyprus", inplace = True)
world_map.replace("Palestinian Territory", "Palestine", inplace = True)
world_map.replace("Russian Federation", "Russia", inplace = True)
world_map.replace("Timor-Leste", "Timor", inplace = True)
world_map.replace("Vatican City", "Vatican", inplace = True) 


# Merging the data
merged = world_map.join(world_covid, on = "COUNTRY", how = "right")

# Creating the Geopandas GIF 
img_frames = []

for date in merged.columns.to_list()[4:]:
    WORLDPLOT = merged.plot(column = date,
                            cmap = "OrRd",
                            figsize = (10, 10),
                            legend = True,
                            scheme = "user_defined",
                            classification_kwds = {"bins": [100, 500, 1000, 
                                                            5000, 10000, 50000,
                                                            100000, 500000, 
                                                            1000000]},
                            edgecolor = "black",
                            linewidth = 0.4)
    
    WORLDPLOT.set_title("Total Confirmed Coronavirus Cases " + date)
    WORLDPLOT.set_axis_off() 
    WORLDPLOT.get_legend().set_bbox_to_anchor((0.18, 0.6)) 

    
  
