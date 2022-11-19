'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime, date
import pygal
import json
import pandas

#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def date_range_calc(startDate, endDate, timeSeries):
    if timeSeries == '1':
        dateRange = pandas.date_range(startDate, endDate, freq='H').strftime('%Y-%m-%d %H:%M:%S')
        return dateRange
    else:
        dateRange = pandas.date_range(startDate, endDate, freq='D').strftime('%Y-%m-%d')
        return dateRange


def dateChecker(dateRange, data):
    emptySet = set()
    emptyList = []
    for dictValues in nested_dict_pairs_iterator(data):
        for i in dateRange:
            if dictValues[1] == i:
                if i not in emptySet:
                    emptySet.add(i)
                    emptyList.append(i)
    emptyList.reverse()
    return emptyList
 
def nested_dict_pairs_iterator(dict_obj):
    #iterate over all keys and values
    for key, value in dict_obj.items():
        #check if value is dict type
        if isinstance(value, dict):
            #iterates all dict values
            for pair in  nested_dict_pairs_iterator(value):
                yield (key, *pair)
        else:
            #if value isn't dict type, yeild
            yield (key, value)
 
#seperates the JSON data for the graph; checks if dates in the data match with the user input dates and applies the data in a list for the graph 
def dataSeperator(valueKey, data, dateRange):
    emptyDict = []
    for dictValues in nested_dict_pairs_iterator(data):
        #checks if data values exist for the user input dates
        for i in dateRange:
            if dictValues[1] == i:
                #adds the corresponding value to the emptyDict list to be returned
                if dictValues[2] == valueKey:
                    emptyDict.append(dictValues[3])
                
    emptyDict = [eval(i) for i in emptyDict]
    #data in JSON is presented in descending order when the graph needs it in ascending: reverse makes the data order correct
    emptyDict.reverse()
    return emptyDict
    
def time_series_checker(timeSeries, userSymbol):
    #Time series checker that queries the API depending on time series user input; also sets range of dates based on time series
    if timeSeries == '1':
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + userSymbol + '&outputsize=full&interval=60min&outputsize=full&apikey=BL6VYKSNVH4EJ68W'
        r = requests.get(url)
        data = r.json()
        return data
    elif timeSeries == '2':
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + userSymbol + '&outputsize=full&apikey=BL6VYKSNVH4EJ68W'
        r = requests.get(url)
        data = r.json()
        return data
    elif timeSeries == '3':
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=' + userSymbol + '&outputsize=full&apikey=BL6VYKSNVH4EJ68W'
        r = requests.get(url)
        data = r.json()
        return data
    else:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=' + userSymbol + '&outputsize=full&apikey=BL6VYKSNVH4EJ68W'
        r = requests.get(url)
        data = r.json()
        return data

def chart_creator(userSymbol, chartType, startDate, endDate, openData, highData, lowData, closeData, xDate):
    #Chart checking and applying all data into the browser chart display
    if chartType == '2':
       line_chart = pygal.Line(x_label_rotation=45)
       line_chart.title = 'Stock Data for ' + userSymbol + ': ' + startDate.strftime('%Y-%m-%d') + ' to ' + endDate.strftime('%Y-%m-%d')
       line_chart.x_labels = xDate
       line_chart.add('Open', openData)
       line_chart.add('High', highData)
       line_chart.add('Low',  lowData)
       line_chart.add('Close', closeData)
       return line_chart.render_data_uri()
    
    else:
       bar_chart = pygal.Bar(x_label_rotation=45)
       bar_chart.title = 'Stock Data for ' + userSymbol + ': ' + startDate.strftime('%Y-%m-%d') + ' ' + endDate.strftime('%Y-%m-%d')
       bar_chart.x_labels = xDate
       bar_chart.add('Open', openData)
       bar_chart.add('High', highData)
       bar_chart.add('Low',  lowData)
       bar_chart.add('Close', closeData)
       return bar_chart.render_data_uri()
