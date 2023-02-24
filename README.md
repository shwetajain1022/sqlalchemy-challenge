# SQLAlchemy Challenge

----
 To help with long holiday vacation in Honolulu, Hawaii, we decided trip planning based on climate analysis about the area. The following sections outline the steps to accomplish this task.

## Table of Contents

- Part 1: Analyse and Explore the Climate Data(#Analyse and Explore the Climate Data)
-- Precipitation Analysis(#Precipitation Analysis)
-- Station Analysis(#Station Analysis)
- Part 2: Design Your Climate App(#Design Your Climate App)

## Part 1: Analyse and Explore the Climate Data(#Analyse and Explore the Climate Data)
--------------------------------------------------------------------------------------------
Used SQLAlchemy ORM queries, Pandas, and Matplotlib to completed analysis. To analyse and explore the climate data,did the following steps:
1. Updated climate_starter.ipynb to finish the work and used hawaii.sqlite to complete climate analysis and data exploration.
1. Used the SQLAlchemy create_engine() function to connect to hawaii SQLite database
1. Used the SQLAlchemy automap_base() function to reflect your tables into classes
1. Saved references to the classes named station and measurement 
1. Linked Python to the database by creating a SQLAlchemy session 
1. Closed your session at the end of your notebook 

## Precipitation Analysis
----
1. Found the most recent date from the Measurement table using SQLAlchemy.ORM.
1. Using this date and dateutil.relativedelta library, 1 year before's date 
1. Performed a query to retrieve the data and precipitation scores based on the previous 12 months of precipitation data using session.query command
1. Saved the query results as a Pandas DataFrame and set the index to the date column
1. Using Matplotlib generated precipitation line graph based on date.

## Station Analysis
----
1. Designed a query to calculate the total number stations in the dataset based on Station class
1. Designed a query to find the list of most active stations using Groupby() function and func.count() function in descending orfder. 
1. Refining the previous query used limit(1) function to get the most active station
1. Using the most active station id from the previous step, calculate the lowest, highest, and average temperature for that station id. func.min(), func.max() and func.avg() functions was used to find the the summary based on the station id.  
1. Using the most active station id, Queried the last 12 months of temperature observation data for most active station id and plotted the results as a histogram

----
## Part 2: Design Your Climate Appa(#Design Your Climate App)
--------------------------------------------------------------------------------------------
Designed the API routes using Flask:
To do so, use Flask to create your routes as follows:

1. (base URL) / - homepage which list all the available routes.
1. /api/v1.0/precipitation route which converts the Jsonify query results (last one year's precipitation data)to a dictionary by using date as the key and prcp as the value. 
It returns the JSON representation of your dictionary onto the browser.
1. /api/v1.0/stations route returns a JSON list of stations from the station dataset.
1. /api/v1.0/tobs route returns Jsonify results query of which contains dates and temperature observations of the most-active station for the previous year of data.
1. /api/v1.0/<start> route returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start.
1. /api/v1.0/<start>/<end> route returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
