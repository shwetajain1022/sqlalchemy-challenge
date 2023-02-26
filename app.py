
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

def getlastyeardate(session):
    latest_date = session.query(func.max(Measurement.date)).first()[0]
    latest_date = datetime.strptime(latest_date, '%Y-%m-%d')
    last_year_date = latest_date - relativedelta(years=1)
    return last_year_date.strftime('%Y-%m-%d')
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end></br>"
    )

# Returns jsonified precipitation data for the last year with the date as the key and the value as the precipitation 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_year_date_str = getlastyeardate(session)

    """Return a list of all precipitation"""
    # Query all 
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=last_year_date_str).\
    all()

    session.close()

    all_prcp_list = []

    for date,prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp_list.append(prcp_dict)
    return jsonify(all_prcp_list)

# Returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all 
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_station_list = list(np.ravel(results))

    return jsonify(all_station_list)

# Returns jsonified data for the most active station for the last year
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement,Station).filter(Measurement.station==Station.station).all()

    #get the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).limit(1).all()[0]["station"]

    last_year_date_str = getlastyeardate(session)

    #get list of temparature and date for the most active station
    results = session.query(Station.name,Measurement.date, Measurement.tobs,).\
    filter(Measurement.station==Station.station).\
    filter(Measurement.station == most_active_station).\
    filter(Measurement.date>=last_year_date_str).\
    order_by(Measurement.tobs).all()

    session.close()

    all_tobs_list = []
    for name,date,tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = name
        tobs_dict["date"]=date
        tobs_dict["tobs"]= tobs
        all_tobs_list.append(tobs_dict)
    return jsonify(all_tobs_list)

# Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    startdate = start.replace(" ", "").lower()

    #get the list of date, minimum maximum and average of the temperature greater than equal to start date
    results = session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= startdate).group_by(Measurement.date).\
    order_by(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).all()

    #return the result as a list of dicts
    results_json = []
    for date,mintemp,maxtemp,avgtemp in results:
        temp_results = {}
        temp_results["date"]= date
        temp_results["mintemp"] = mintemp
        temp_results["maxtemp"]= maxtemp
        temp_results["avgtemp"] = avgtemp
        results_json.append(temp_results)

    return jsonify(results_json)

# Returns the min, max, and average temperatures calculated from the given start date to the given end date
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    startdate = start.replace(" ", "")
    enddate = end.replace(" ","")

    #get the list of date, minimum maximum and average of the temperature greater than equal to start date and less than equal to end date
    results = session.query(Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= startdate).\
    filter(Measurement.date <= enddate).\
    group_by(Measurement.date).\
    order_by(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).all()

    #return the result as a list of dicts
    results_json = []
    for date,mintemp,maxtemp,avgtemp in results:
        temp_results = {}
        temp_results["date"]= date
        temp_results["mintemp"] = mintemp
        temp_results["maxtemp"]= maxtemp
        temp_results["avgtemp"] = avgtemp
        results_json.append(temp_results)

    return jsonify(results_json)

#run the app using Flask
if __name__ == '__main__':
    app.run()