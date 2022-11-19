from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import StockForm
from .charts import *

@app.route("/", methods=['GET', 'POST'])
@app.route("/stocks", methods=['GET', 'POST'])
def stocks():
    
    form = StockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #Get the form data to query the api
            symbol = request.form['symbol']
            chart_type = request.form['chart_type']
            time_series = request.form['time_series']
            start_date = convert_date(request.form['start_date'])
            end_date = convert_date(request.form['end_date'])

            if end_date <= start_date:
                #Generate error message as pass to the page
                err = "ERROR: End date cannot be earlier than Start date."
                chart = None
            else:
                #query the api using the form data
                err = None
                 
                #THIS IS WHERE YOU WILL CALL THE METHODS FROM THE CHARTS.PY FILE AND IMPLEMENT YOUR CODE
                data = time_series_checker(time_series, symbol)
                dateRange = date_range_calc(start_date, end_date, time_series)
                xDate = dateChecker(dateRange, data)
                
                openData = dataSeperator("1. open", data, dateRange)
                highData = dataSeperator("2. high", data, dateRange)
                lowData = dataSeperator("3. low", data, dateRange)
                closeData = dataSeperator("4. close", data, dateRange)
                print(dateRange, flush=True)
                #This chart variable is what is passed to the stock.html page to render the chart returned from the api
                chart = chart_creator(symbol, chart_type, start_date, end_date, openData, highData, lowData, closeData, xDate)

            return render_template("stock.html", form=form, template="form-template", err = err, chart = chart)
    
    return render_template("stock.html", form=form, template="form-template")
