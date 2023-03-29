"""Logged-in page routes."""

import re
from flask import Blueprint, redirect, render_template, url_for
from flask import(
    current_app as app,
    request,
)
from flask_login import current_user, login_required, logout_user
from sqlalchemy import func 
from traffic_app import db 
from traffic_app.models import Query
from traffic_app.schemas import QuerySchema

# -------
# Schemas
# -------

queries_schema = QuerySchema(many=True)
query_schema = QuerySchema()


# Blueprint Configuration
main_bp = Blueprint( "main_bp", __name__)

# ---------------------
# Logged in Page Routes
# ---------------------


@main_bp.route("/")
@login_required
def dashboard():
    """Logged-in User Dashboard (Homepage))"""
    # Query the database for all columns in the Query table
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
    # Replace spaces and other invalid special characters in header with underscores
    header = re.sub('[^0-9a-zA-Z\s]+', '_', header) 

    # Query the database to get the list of distinct values of selected header column
    column_obj = getattr(Query, header)
    options = db.session.query(column_obj).distinct().order_by(column_obj).all()

    # Use a new regular expression pattern to replace special characters with underscores
    #(exlude anything that is not a word character (\w), whitespace character (\s), or digit (\d))
    options = [re.sub('[^\w\s\d]+', '_', str(option[0])) for option in options] 

    return render_template('query.html', header=header, options=options)


@main_bp.route('/result/<header>/<option>')
@login_required
def result(header, option):
    """Summary statistics / results page of selected query (dropdown option)"""

    # Replace underscores with spaces in option variable 
    option = option.replace('_', ' ')

    # Query the database for the selected option
    query = db.session.query(Query).filter(getattr(Query, header) == option)
    
    # Compute basic summary statistics on traffic volume based on the chosen option
    average = int(query.with_entities(func.avg(Query.traffic_volume)).scalar())
    minimum = query.with_entities(func.min(Query.traffic_volume)).scalar()
    maximum = query.with_entities(func.max(Query.traffic_volume)).scalar()

    # Find the average value of the traffic volume column
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

 

@main_bp.route("/logout")
@login_required
def logout():
    """Logs out the user and returns them to the login page"""
    logout_user()
    return redirect(url_for("auth_bp.login"))



# ---------
# API Route
# ---------

# refer to README.md for instructions to query data from the database with different filters or parameters

@app.get("/data/")
def get_all_data():
    """Returns all data in the database"""
    # Get all columns in the Query table
    columns = [column.name for column in Query.__table__.columns]

    # Get user input
    #query_params = dict(request.args)  # only allows for one query parameter
    query_params = request.args.to_dict() # allows  multiple query parameters
    if not query_params:
        # If no query parameters are provided, return all data
        data = db.session.query(Query).all()
    else:
        # Filter data based on provided query parameters
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









