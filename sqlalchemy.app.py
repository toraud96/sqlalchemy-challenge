import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# reflect the tables
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


# reflect an existing database into a new model

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB

    """Return a list of all passenger names"""
    # Query all passengers

    # Convert list of tuples into normal list
    begin_point = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= begin_point).\
    order_by(Measurement.date).all()

    all_names={date:prcp for date, prcp in data}

    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    results=list(np.ravel(stations))
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def sel():
    sel = [Measurement.station, 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]
    sel=session.query(*sel).filter(Measurement.station=='USC00519281').all()
    results=list(np.ravel(sel))
    return jsonify(results)

@app.route("/api/v1.0/temp/begin_point")
def stats(begin_point=None):
    temp=session.query(Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date >= begin_point).\
        order_by(Measurement.date.desc()).all()
    results=list(np.ravel(temp))
    return jsonify(results)


# @app.route("/api/v1.0/temp/<start>/<end>")
# def stats(vacay_start=None, vacay_end=None):
#     data4 = session.query(Measurement.date, Measurement.prcp).\
#         filter(Measurement.date >= vacay_start).\
#         filter(Measurement.date <= vacay_end).\
#         order_by((Measurement.date).desc()).all()
#     results=list(np.ravel(data4))
#     return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)