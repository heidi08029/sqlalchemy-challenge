import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
station = Base.classes.station
measurement = Base.classes.measurement

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
        f"/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary"""
    # Design a query to retrieve the last 12 months of precipitation data
    first_date = '2016-08-23'
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= first_date).all()

    session.close()

    # disctionary
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list"""
    # Design a query to find the most active stations (i.e. which stations have the most rows?)
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

    session.close()

    # Create a list
    list_of_stations = list(np.ravel(active_stations))

    return jsonify(list_of_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list"""
    # Design a Query the dates and temperature observations of the most-active station for the previous year of data.
    first_date = '2016-08-23'
    station_temp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= first_date, measurement.station == "USC00519281").all()

    session.close()

    # Create a list
    list_of_station_temp = list(np.ravel(station_temp))

    return jsonify(list_of_station_temp)

if __name__ == '__main__':
    app.run(debug=True)
