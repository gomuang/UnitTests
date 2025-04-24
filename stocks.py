import requests
import pygal
import lxml
import os
import webbrowser 
from datetime import datetime

API_KEY = "L0WWWUGT9503R1300"
BASE_URL = "https://www.alphavantage.co/query"

#get company symbol from user
def user_input():
    # Display application header to clearly identify the program to the user
    print("Stock Data Visualizer")
    print("---------------------")

    # STOCK SYMBOL COLLECTION AND VALIDATION
    # Loop continues until a valid stock symbol is provided
    while True:
        # Get input, remove whitespace with strip(), and convert to uppercase for consistency
        symbol = input("\nEnter the stock symbol you are looking for: ").strip().upper()
        
        # Check if the symbol is empty (user just pressed Enter)
        if not symbol:
            print("Error: Stock symbol cannot be empty. Please enter a valid stock symbol.")
        # Check if the symbol contains only alphabetic characters
        # This is important as stock symbols typically only use letters
        elif not symbol.isalpha():
            print("Error: Stock symbol should only contain letters. Please enter a valid stock symbol.")
        # If all validation checks pass, exit the loop
        else:
            break
    
    # CHART TYPE SELECTION AND VALIDATION
    # Loop continues until a valid chart type selection is made
    while True:
        # Display the chart type options to the user
        print("\nChart Types")
        print("-------------")
        print("1. Bar")
        print("2. Line")
        
        try:
            # Get the user's selection and remove any whitespace
            chart_type = input("\nEnter the chart type you want (1, 2): ").strip()
            # Convert the string input to an integer for comparison
            chart_type = int(chart_type)
            
            # Validate that the selection is one of the available options
            if chart_type not in [1, 2]:
                print("Error: Please enter a number 1 or 2.")
            else:
                # Valid selection made, exit the loop
                break
        except ValueError:
            # This exception handler catches cases where the input cannot be converted to an integer
            # For example, if the user enters text like "bar" instead of "1"
            print("Error: Please enter a number 1 or 2.")

    # TIME SERIES SELECTION AND VALIDATION
    # Loop continues until a valid time series option is selected
    while True:
        # Display the time series options to the user
        print("\nTime Series")
        print("-------------")
        print("1. Intraday")  # Data at 60-minute intervals
        print("2. Daily")     # Daily data points
        print("3. Weekly")    # Weekly data points
        print("4. Monthly")   # Monthly data points
        
        try:
            # Get the user's selection and remove any whitespace
            time_series = input("\nEnter the time series you want (1, 2, 3, 4): ").strip()
            # Convert the string input to an integer for comparison
            time_series = int(time_series)
            
            # Validate that the selection is one of the available options
            if time_series not in [1, 2, 3, 4]:
                print("Error: Please enter a number 1, 2, 3, or 4.")
            else:
                # Valid selection made, exit the loop
                break
        except ValueError:
            # This exception handler catches cases where the input cannot be converted to an integer
            print("Error: Please enter a number 1, 2, 3, or 4.")

    # MAPPING TIME SERIES SELECTION TO API FUNCTION NAME
    # Alpha Vantage API requires specific function names for different time series
    time_series_map = {
        1: "TIME_SERIES_INTRADAY",  # For intraday data (typically with a 60min interval)
        2: "TIME_SERIES_DAILY",     # For daily data
        3: "TIME_SERIES_WEEKLY",    # For weekly data
        4: "TIME_SERIES_MONTHLY"    # For monthly data
    }

    # Get the corresponding API function name based on the user's selection
    # This will be used when constructing the API request
    time_series_function = time_series_map.get(time_series)

    # DATE RANGE COLLECTION AND VALIDATION
    # Initialize date variables
    start_date = None
    end_date = None

    # Get and validate the start date
    while True:
        try:
            # Get the start date as a string and remove any whitespace
            start_date = input("\nEnter the start date (YYYY-MM-DD): ").strip()
            # Convert the string to a datetime object for validation and comparison
            # This also verifies that the date format is correct
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            # If we reach this point, the date format is valid, so exit the loop
            break
        except ValueError:
            # This exception is raised if the date format is incorrect or if the date is invalid
            # (e.g., February 30th or text instead of a date)
            print("Error: Please enter a valid date in the format YYYY-MM-DD.")
    
    # Get and validate the end date
    while True:
        try:
            # Get the end date as a string and remove any whitespace
            end_date = input("\nEnter the end date (YYYY-MM-DD): ").strip()
            # Convert the string to a datetime object for validation and comparison
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            
            # Check that the end date is not before the start date
            # This is a logical validation to ensure the date range makes sense
            if end_date < start_date:
                print("Error: End date cannot be before start date. Please enter a valid end date.")
            else:
                # If the end date is valid and after the start date, exit the loop
                break
        except ValueError:
            # This exception is raised if the date format is incorrect or if the date is invalid
            print("Error: Please enter a valid date in the format YYYY-MM-DD.")

    # Return all collected and validated inputs as a dictionary
    # This makes it easy to pass all the data to other functions
    return {
        "symbol": symbol,                              # Stock symbol (e.g., "AAPL" for Apple)
        "chart_type": chart_type,                      # Chart type (1 for Bar, 2 for Line)
        "time_series_function": time_series_function,  # API function name
        "start_date": start_date,                      # Start date as datetime object
        "end_date": end_date,                          # End date as datetime object
        "time_series_option": time_series              # Original time series selection (1-4)
    }

#get data from the Alpha Vantage API
def fetch_data(user_input):
    # Build a dictionary of parameters to send to the Alpha Vantage API
    # These parameters tell the API what data we're requesting
    params = {
        "function": user_input["time_series_function"],  # Which time series to retrieve (daily, weekly, etc.)
        "symbol": user_input["symbol"],                  # The stock ticker symbol
        "apikey": API_KEY,                               # Authentication key for API access
        "month": "{}-{:02}".format(user_input["start_date"].year, user_input["start_date"].month), # Month to pull data from
        "outputsize": "full"                             # Request entire data so it does not cut off
    }
    
    # For intraday data (option 1), we need to also specify how frequently we want data points
    # This adds a parameter requesting data at 60-minute intervals
    # Also need to specify that we want the entire month of data to be pulled
    if user_input["time_series_option"] == 1:
        params["interval"] = "60min"
    
    try:
        # Make the HTTP GET request to the Alpha Vantage API
        response = requests.get(BASE_URL, params=params)
        
        # Parse the JSON response into a Python dictionary
        data = response.json()
        print("Done.")
        
        # Return the data for further processing
        return data
        
    except requests.exceptions.RequestException as e:
        # This catches any errors related to the request itself
        print(" Failed.")
        print(f"Error fetching data: {e}")
        return None
   
#function to retrieve the open, high, low, and close
def get_stock_data(data):
    # Get the keys since we won't know what the time series will be called in the dictionary
    keys = list(data.keys())
    #grab the time series key since we
    time_series_data = keys[1]
    
    #declare variables to hold separated data points
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []
    
    #access the time series data using the time_series_data key
    time_series = data.get(time_series_data)

    # only use data that falls between the start and end dates
    # filter for intraday (uses timestamp with time)
    if inputs["time_series_option"] == 1:
        filtered_time_series = {
            timestamp: values for timestamp, values in time_series.items()
            if inputs["start_date"] < datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") < inputs["end_date"]
        }
    # filter for all others (uses timestamp with just date)
    else:
        filtered_time_series = {
            timestamp: values for timestamp, values in time_series.items()
            if inputs["start_date"] < datetime.strptime(timestamp, "%Y-%m-%d") < inputs["end_date"]
        }
    
    #iterate through the time series data and add stock data points associated with that time stamp to their lists
    for timestamp, values in filtered_time_series.items():
        open_price = values.get('1. open')
        open_prices.append(int(float(open_price)))
        high_price = values.get('2. high')
        high_prices.append(int(float(high_price)))
        low_price = values.get('3. low')
        low_prices.append(int(float(low_price)))
        close_price = values.get('4. close')
        close_prices.append(int(float(close_price)))

    return filtered_time_series, open_prices, high_prices, low_prices, close_prices

def get_chart_type(chart_type):
    if chart_type == 1:
        bar_chart = pygal.Bar()
        if inputs["time_series_option"] == 1:
            bar_chart.title = f'Intraday Stock Data for {inputs["symbol"]} from {inputs["start_date"]} to {inputs["end_date"]}'
        elif inputs["time_series_option"] == 2:
            bar_chart.title = f'Daily Stock Data for {inputs["symbol"]} from {inputs["start_date"]} to {inputs["end_date"]}'
        elif inputs["time_series_option"] == 3:
            bar_chart.title = f'Weekly Stock Data for {inputs["symbol"]} from {inputs["start_date"]} to {inputs["end_date"]}'
        elif inputs["time_series_option"] == 4:
            bar_chart.title = f'Monthly Stock Data for {inputs["symbol"]} from {inputs["start_date"]} to {inputs["end_date"]}'
        bar_chart.x_labels = dates
        bar_chart.x_label_rotation = 90 # rotate labels so they fit better
        bar_chart.add('Open', open_prices)
        bar_chart.add('High', high_prices)
        bar_chart.add('Low', low_prices)
        bar_chart.add('Close', close_prices)
        return bar_chart
    else:
        line_chart = pygal.Line()
        if inputs["time_series_option"] == 1:
            line_chart.title = f'Intraday Stock Data for {inputs["symbol"]} from {inputs["start_date"]} to {inputs["end_date"]}'
        elif inputs["time_series_option"] == 2:
            line_chart.title = f'Daily Stock Data for {inputs["symbol"]} from {inputs["start_date"]} to {inputs["end_date"]}'
        elif inputs["time_series_option"] == 3:
            line_chart.title = f'Weekly Stock Data for {inputs["symbol"]} from {inputs["start_date"]} to {inputs["end_date"]}'
        elif inputs["time_series_option"] == 4:
            line_chart.title = f'Monthly Stock Data for {inputs["symbol"]} from {inputs["start_date"]} to {inputs["end_date"]}'
        line_chart.x_labels = dates
        line_chart.x_label_rotation = 90 # rotate labels so they fit better
        line_chart.add('Open', open_prices)
        line_chart.add('High', high_prices)
        line_chart.add('Low', low_prices)
        line_chart.add('Close', close_prices)
        return line_chart

if __name__ == "__main__":
    inputs = user_input()
    stock_data = fetch_data(inputs)
    time_series, open_prices, high_prices, low_prices, close_prices = get_stock_data(stock_data)
    dates = time_series.keys()

    chart = get_chart_type(inputs['chart_type'])
    chart.render_to_file('chart.svg')
    
