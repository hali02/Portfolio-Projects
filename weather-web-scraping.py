##import libraries

import os

from bs4 import BeautifulSoup
from selenium import webdriver

import time
import datetime

def rendering(url):
    
        #install homebrew before running script
        cService = webdriver.ChromeService(executable_path='/opt/homebrew/bin/chromedriver')
        driver = webdriver.Chrome(service = cService)
        driver.get(url)                                          # load the web page from the URL
        ##print(4)
        time.sleep(1)                                            # wait for the web page to load
        ##print(1)
        render = driver.page_source                              # get the page source HTML
        ##print(2)
        driver.quit()                                            # quit ChromeDriver
        ##print(3)
        return render


##get list of dates ready
date_range_list = []

start = datetime.datetime.strptime('2023-10-20', '%Y-%m-%d')
end = datetime.datetime.strptime('2023-11-08', '%Y-%m-%d')
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    date_range_list.append(date.strftime('%Y-%m-%d'))

##prepare csv files to write data into
outfile = 'weather_data-10994.csv'

#with open(outfile, 'w') as f:
    # write column headers for each paramter into the file for later use
    f.write('date,'
            'actual_high_temp,histavg_high_temp,record_high_temp,'
            'actual_low_temp,histavg_low_temp,record_low_temp,'
            'actual_avg_temp,histavg_avg_temp,record_avg_temp,'
            'actual_precip,histavg_precip,record_precipitation\n')

##start webscraping
base_url = 'https://www.wunderground.com/history/daily/us/ny/harrison/KHPN/date/{}'
    
for date in date_range_list:

    search_url = base_url.format(date)

    wunderground_page = rendering(search_url)

    wunderground_soup = BeautifulSoup(wunderground_page, 'html.parser')

    soup_container = wunderground_soup.find('lib-city-history-summary')
    soup_data = soup_container.find_all('tbody', class_='ng-star-inserted')

    
    row = []
    for i, dat in enumerate(soup_data):
        # loops through High Temp, Low Temp, etc.
        for j, d in enumerate(dat.find_all('tr', class_='ng-star-inserted')):
            # loops through Actual, Historic Avg., Record
            for k in d.find_all('td', class_='ng-star-inserted'):
                tmp = k.text
                tmp = tmp.strip('  ') # remove any extra spaces
                        
                row.append(tmp)

    f = open(outfile, 'a')
    f.write(date + ',') # write the date of the recorded data into the file
    f.write(','.join(row[:12])) # write just the temperature and precipitation data into the file
    f.write('\n') # new line, in case you want to append more rows to the same file later on
    f.close()
