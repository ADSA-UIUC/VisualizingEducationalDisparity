import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def format_data(data,year,threshold):
	'''
	This function returns a dataset with countries as rows, and 
	indicators (e.g population, attendance rate, etc) as columns.

	The year parameter specifies which year that information comes from.
	(I noticed that 2010 and 2015 have a decent amount of data).

	Many of the countries don't have much data, so I included a threshold.
	If the threshold is 800, for instance, that means every country
	included in the dataset must have a non-empty value for at least 800 out
	of ~3600 attributes.
	
	'''
	country_names = data["Country Name"].unique()
	country_names = country_names[25:]
	country_names = country_names.tolist()
	countries = []
	for i in range(len(country_names)):
		d = data[data["Country Name"] == country_names[i]]
		if len(d[str(year)][d[str(year)]==d[str(year)]]) > threshold:
			countries.append(country_names[i])

	indicators = data["Indicator Name"].unique().tolist()

	indicator_list = []

	for i in countries:
		d = data[data["Country Name"] == i]
		valid_ind = d["Indicator Name"][d[str(year)]==d[str(year)]].tolist()
		for i in range(len(valid_ind)):
			indicator_list.append(valid_ind[i])
		indicator_set = set(indicator_list)
		indicator_list = list(indicator_set)

	index_list = []
	for i in indicator_list:
		index_list.append(indicators.index(i))

	data_subset = data[data["Country Name"].isin(countries)]
	curr_year = data_subset[str(year)]
	row_list = []
	for i in range(len(countries)):
		row = curr_year[i*len(indicators):(i+1)*len(indicators)]
		row = row.tolist()
		row_subset = []
		for i in index_list:
			row_subset.append(row[i])
		row_list.append(row_subset)

	df = pd.DataFrame(row_list)
	df.columns = indicator_list
	df.index = countries

	return df


directory = "../education-statistics/EdStatsData.csv"
data = pd.read_csv(directory,sep=",")
df = format_data(data,2015,800)



