import re
import csv
from os import getcwd
from bs4 import BeautifulSoup as bs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re

data = pd.read_csv(getcwd() + "\\data.txt", encoding = "ISO-8859-1", index_col="name")

print("1. How many countries are listed?")
print(data['country'].nunique())

print("\n2. Which mountains from Israel are listed?")
print("\n".join(data[data['country'] == "israel"].index))

print("\n3. Make a histogram of the peaks heights in Europe. --> see graph")
data_of_europe = data[data["continent"] == "europe"]
data_of_europe['elevation (meters)'].plot(kind='hist',title=' 3. Make a histogram of the peaks heights in Europe.')
plt.show()

print("\n4. Which country has the highest number of peaks above 6000m?")
filter_peaks = data[data["elevation (meters)"] > 6000.0]
high_paeks_in_country = filter_peaks.groupby('country')["elevation (meters)"].count()
print("{} with {} peaks".format(high_paeks_in_country.idxmax(), high_paeks_in_country.max()))

continent_grp = data.groupby('continent')


print("\n5. Make a pie chart for the number of peaks in each continent. --> see pie graph")
pie_prep = continent_grp.size()
pie_prep.plot(kind="pie", title="number of peaks in each continent", autopct='%f',use_index=True)
plt.show()


print("\n6. Sort the continents by their average peak height.")
sorted_continent = continent_grp["elevation (meters)"].mean().sort_values()
print(sorted_continent)
print(" < ".join(sorted_continent.index))


print("\n7. Find the highest mountain in each continent.")
heighest_peaks_in_continent = continent_grp["elevation (meters)"].idxmax()
print(heighest_peaks_in_continent)


print("\n8. How many peaks are in “islands” countries? which is the highest of them?")
print('didnt find the method that returns which record contain "islands"')
print("tried: .contains, findall, find, count, match, regex - i think it due to the non conventional characters")


print("\n9. Which country has the largest number of peaks listed?")
print(data.groupby("country").size().idxmax())
print("\nAnd per continent?")
print(continent_grp.agg({"country":"max"}))

print("\n10. What is the first mountain that was climbed in each century?")
data["century_of_climb"] = np.floor(data["year first climbed"]/100)
year_of_first_climb = data.groupby('century_of_climb')["year first climbed"].min().values
filtered_data_century_of_climb = data[data["year first climbed"].isin(year_of_first_climb)]
print(filtered_data_century_of_climb[["century_of_climb","year first climbed"]].sort(columns="year first climbed"))

print("\n11. Of all the peaks with climbing difficulty “walk up”, which is the highest?")
easy_peaks = data.ix[data["difficulty"].str.lower() == "walk up"]
print(easy_peaks["elevation (meters)"].idxmax() , easy_peaks["elevation (meters)"].max() , "m")

print("\n12. How many peaks are there on the equator (no more than 1 degree away from it?)")
print(data[data["latitude"].abs()<=1].__len__())

print("\n13. Find the highest peak for each combination of continent and difficulty")
difficulties_cat = ['walk up','scramble', 'basic snow/ice climb', 'technical climb', 'major mountain expedition']
print(data.groupby(["continent","difficulty"])["elevation (meters)"].max())

