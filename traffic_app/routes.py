"""Logged-in page routes."""

import re
import sys, json
from flask import Blueprint, redirect, render_template, url_for
from flask import(
    current_app as app,
    request,
    make_response,
    jsonify,
)


from flask_login import current_user, login_required, logout_user

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from sqlalchemy import func, or_

from traffic_app import db, get_db
from traffic_app.models import Query
from traffic_app.schemas import QuerySchema

#from statistics import stdev




# -------
# Schemas
# -------

queries_schema = QuerySchema(many=True)
query_schema = QuerySchema()


# Blueprint Configuration
main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)

# ------
# Routes
# ------


@main_bp.route("/")
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    headers = [col.name for col in Query.__table__.columns if col.name not in ['traffic_volume','rowid']]
    return render_template(
        "dashboard.html",
        current_user=current_user,
        headers=headers,
    )

@main_bp.route('/query/<header>')
@login_required
def query(header):
    """Dropdown menu for query options"""
    # Replace spaces and other invalid characters in header with underscores
    #header = header.replace(' ', '_')
    #exlude special characters but not numbers
    header = re.sub('[^0-9a-zA-Z\s]+', '_', header) 
   

    #options variable must contain a list of distinct values of selected header column, sorted in ascending order

    column_obj = getattr(Query, header)
    options = db.session.query(column_obj).distinct().order_by(column_obj).all()
    #options = [option[0] for option in options]


    #below code exludes anything that is not a word character (\w), whitespace character (\s), or digit (\d)
    # Use a new regular expression pattern to exclude only special characters
    options = [re.sub('[^\w\s\d]+', '_', str(option[0])) for option in options]

    return render_template('query.html', header=header, options=options)


@main_bp.route('/result/<header>/<option>')
@login_required
def result(header, option):
    """Summary statistics / results page of selected query (dropdown option))"""

    # Replace underscores with spaces in option value (check if below code is still necessary)
    option = option.replace('_', ' ')
    # Query the database for the selected option
    query = db.session.query(Query).filter(getattr(Query, header) == option)
    
    # Compute basic summary statistics on traffic volume based on the chosen option
    average = int(query.with_entities(func.avg(Query.traffic_volume)).scalar())
    minimum = query.with_entities(func.min(Query.traffic_volume)).scalar()
    maximum = query.with_entities(func.max(Query.traffic_volume)).scalar()

    # find the average value of the traffic volume column
    average_traffic_volume = db.session.query(func.avg(Query.traffic_volume)).scalar()

    # Define the range for moderate traffic volume
    moderate_range = (average_traffic_volume - 500, average_traffic_volume + 500)

    # Determine the category based on the average traffic volume of the chosen option and the calculated range
    if average < moderate_range[0]:    # lower bound of moderate_range
        category = "relatively low"
    elif average < moderate_range[1]:    # upper bound of moderate_range
        category = "moderate"
    else:
        category = "relatively high"

    # Create a dictionary to hold the response data
    response = {
        "header": header,
        "option": option,
        "average": average,
        "minimum": minimum,
        "maximum": maximum,
        "category": category
    }
    # Render the result.html template with the response data
    return render_template('result.html', **response)

    #return render_template('result.html', header=header, option=option, average = average, minimum=minimum, maximum=maximum)




@main_bp.route("/logout")
@login_required
def logout():
    """Logs out the user and returns them to the login page"""
    logout_user()
    return redirect(url_for("auth_bp.login"))


# ROUTES THAT ALLOW PROGRAMMATIC ACCESS TO DATA (JSON RESPONSES) 
"""
@app.get("/data/")
@login_required
def get_all_data():
    #Returns all data in the database
    # Get all data from the database
    data = Query.query.all()
    # Serialize the data for the response
    data = queries_schema.dump(data)
    # Return a JSON response
    return data
"""
#Note that we pass db as a parameter to the get_all_data function using the Depends dependency injection from FastAPI, 
# which will create a new session for each request and close it afterwards.


# include error handling add ways to run in setup.py 

# refer to README.md for instructions to query data from the database with different filters or parameters
@app.get("/data/")
#@login_required
def get_all_data():
    """Returns all data in the database"""
    # Get all possible columns in the Query table
    columns = [column.name for column in Query.__table__.columns]

    # Get user input
    #query_params = dict(request.args)  # only allows for one query parameter
    query_params = request.args.to_dict() # allows  multiple query parameters
    #db = get_db()
    if not query_params:
        # If no query parameters are provided, return all data
        #data = db.Query.query.all()
        data = db.session.query(Query).all()
    else:
        # Filter data based on provided query parameters
        #query = db.query(Query)
        query = db.session.query(Query)
        for key, value in query_params.items():
            if key in columns:
                # If the key is a valid column name, filter by that column
                query = query.filter(getattr(Query, key) == value)
        data = query.all()

    # Serialize the data for the response
    data = queries_schema.dump(data)

    # Return a JSON response
    return data



"""
@app.get("/data/<date>")
@login_required
def get_data_by_date(date):
    #Returns all data in the database for a given date
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        data = Query.query.filter_by(date=date_obj).all()
        data = queries_schema.dump(data)
        return data
    except ValueError:
        return {"message": f"Invalid date format provided: {date}"}, 400


@app.get("/data/<year>/<month>/<day>")
@login_required
def get_data_by_date(year, month, day):
    #Returns all data in the database for a given date
    try:
        date_obj = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').date()
        print(date_obj)
        data = Query.query.filter_by(date=date_obj).all()
        data = queries_schema.dump(data)
        return data
    except ValueError:
        return {"message": f"Invalid date format provided: {year}/{month}/{day}"}, 400

"""




"""
   # Create a dictionary to hold the response data
    response = {
        "header": header,
        "option": option,
        "average": average,
        "minimum": minimum,
        "maximum": maximum
    }
    # Return a JSON response
    return render_template('query.html', json_data=response)
    both doesnt work
    quartiles = query.with_entities(func.percentile_cont(0.25).within_group(Query.traffic_volume).label("q1"),
                                     func.percentile_cont(0.5).within_group(Query.traffic_volume).label("q2"),
                                     func.percentile_cont(0.75).within_group(Query.traffic_volume).label("q3")).first()
    
    if average < quartiles.q1:
        category = "avg is relatively low"
    elif average > quartiles.q3:
        category = "avg is relatively high"
    else:
        category = "avg is moderate"

    result_dict = {"average": average,
                   "minimum": minimum,
                   "maximum": maximum,
                   "category": category}
    
    return jsonify(result_dict)

"""







