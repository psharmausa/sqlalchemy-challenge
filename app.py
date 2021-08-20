# Step 2 - Climate App
# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
# Use Flask to create your routes.

# Hints
# You will need to join the station and measurement tables for some of the queries.

# Use Flask jsonify to convert your API data into a valid JSON response object.import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references
Measurement = Base.classes.measurement
Stations = Base.classes.station


# Routes
# /

# Home page.
# List all routes that are available.

# Flask Setup
app = Flask(__name__)
# Routes
@app.route("/")
def availroute():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# /api/v1.0/precipitation

# Convert the query results to a dictionary using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.
# Return a JSON list of stations from the dataset.
# /api/v1.0/tobs

# Query the dates and temperature observations of the most active station for the last year of data.

# Return a JSON list of temperature observations (TOBS) for the previous year.


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    maxDate=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    yeaAgo = maxDate - dt.timedelta(days=365)

    past_temp = (session.query(Measurement.date, Measurement.prcp)
                .filter(Measurement.date <= maxDate)
                .filter(Measurement.date >= yearAgo)
                .order_by(Measurement.date).all())
    
    precip = {date: prcp for date, prcp in past_temp}
    
    return jsonify(precip)


# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

@app.route('/api/v1.0/<start>') 
def start(start=None):


    tobs_only = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all())
    
    tobs_df = pd.DataFrame(tobs_only)

    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)


# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


@app.route('/api/v1.0/<start>/<end>') 
def startend(start=None, end=None):

    #start = Measurement.date <= '2010-01-01'
    #end = Measurement.date >= '2017-08-23'

    tobs_only = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all())
    
    tobs_df = pd.DataFrame(tobs_only)

    tavg = tobs_df["tobs"].mean()
    tmax = tobs_df["tobs"].max()
    tmin = tobs_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)


# In[ ]:


if __name__ == '__main__':
    app.run(debug=True)


# In[62]:


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))

