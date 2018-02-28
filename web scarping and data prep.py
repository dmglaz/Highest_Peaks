import re
import requests
import csv
from os import getcwd
from bs4 import BeautifulSoup as bs

header = ["name","country","difficulty","elevation (feet)","elevation (meters)","latitude","longitude","nearest major airport","year first climbed","continent"]
numerical_header = ["elevation (feet)","elevation (meters)","latitude","longitude","year first climbed"]
with open(getcwd() + "\\data.txt",'w') as file:
    csv_write = csv.DictWriter(file,fieldnames=header,delimiter=",",lineterminator='\n')
    csv_write.writeheader()

    # from the main page that contains the continent list crawl through the continent and into the peaks
    site_url = 'https://www.peakware.com'
    site = requests.get(site_url + "/peaks.php")
    continent_table = bs(site.text, 'lxml').find_all(name="ul", id='contList')[0].find_all(name='li')
    for continent in continent_table:
        continent_url = continent.find_all(name='a')[0].get('href')
        continent_peaks_page = requests.get(site_url+'/'+continent_url)
        peak_links = bs(continent_peaks_page.text, 'lxml').find_all(name="ul", id='peakList')[0].find_all(name='a')
        for i,link in enumerate(peak_links):
            #for each link to a peak in a continent initialize a record
            peak_to_save = {'name': link.text.encode('utf-8'), "country": None ,"difficulty": None, "elevation (feet)": None,
                           "elevation (meters)": None, "latitude": None, "longitude": None, "nearest major airport": None,
                           "year first climbed": None, "continent": None}

            peak_page = requests.get(site_url + '/' + link['href'])
            peak_info = bs(peak_page.text, 'lxml').find_all(name="div", id='overview')[0].find_all(name="tr")

            #for every item of data in the peak's page we check if the item is relevant
            # e.g in the header list, if it is we add the item's value to the peak_to_save
            for data in peak_info:
                item = data.th.text[:-1].encode('utf-8').lower()
                value = data.td.text.encode('utf-8')
                if item in header:
                    try:
                        value = value.replace(",", "")
                        if item in numerical_header:
                            if item == "year first climbed": #if the date of firt year is irregular date
                                value = re.findall('\d{4}', value)[0]
                            if "." in value: #if the number is a float number
                                peak_to_save[item] = float(value)
                            else:
                                peak_to_save[item] = int(value)
                        else:
                            value = value.lower()
                            if item == "country":
                                peak_to_save[item] = value.split(',')[0] #if a peak is listed with more then a single country the use the first country
                            else:
                                peak_to_save[item] = value.replace("\n","").replace("\r","")
                    except Exception:
                        print (Exception.message, item,":",value)
            print (peak_to_save)

        #----write to file----#
            if peak_to_save['elevation (meters)'] == None or  peak_to_save['elevation (feet)'] == None:
                if peak_to_save['elevation (meters)'] == None and peak_to_save['elevation (feet)'] != None:
                    peak_to_save['elevation (meters)'] = 0.3048 * peak_to_save['elevation (feet)']
                    csv_write.writerow(peak_to_save)
                elif peak_to_save['elevation (meters)'] != None and peak_to_save['elevation (feet)'] == None:
                    peak_to_save['elevation (feet)'] = 3.28 * peak_to_save['elevation (meters)']
                    csv_write.writerow(peak_to_save)
            # the last option is that both of the elevations are None, and in that case we ignore the record and dont write it to the file
            else:
                csv_write.writerow(peak_to_save)


