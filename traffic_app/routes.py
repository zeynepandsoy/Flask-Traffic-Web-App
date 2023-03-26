"""Logged-in page routes."""


import sys, json
from flask import Blueprint, redirect, render_template, url_for
from flask import(
    current_app as app,
    request,
    make_response,
    jsonify,
)
from datetime import datetime

from flask_login import current_user, login_required, logout_user

from sqlalchemy import func

from traffic_app import db
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
    headers = [col.name.replace('_', ' ') for col in Query.__table__.columns if col.name not in ['traffic_volume','rowid']]
    return render_template(
        "dashboard.html",
        current_user=current_user,
        headers=headers,
    )

@main_bp.route('/query/<header>')
@login_required
def query(header):
    """Dropdown menu for query options"""
    #options variable must contain a list of distinct values of selected header column, sorted in ascending order

    column_obj = getattr(Query, header)
    options = db.session.query(column_obj).distinct().order_by(column_obj).all()
    options = [option[0] for option in options]
    #print(type(options))
    return render_template('query.html', header=header, options=options)



@main_bp.route('/result/<header>/<option>')
@login_required
def result(header, option):
    """Summary statistics / results page of selected query (dropdown option))"""
    # Replace underscores with spaces in option value (check if below code is still necessary)
    option = option.replace('_', ' ')
    query = db.session.query(Query).filter(getattr(Query, header) == option)
    
    # Change average traffic from decimal to int
    average = int(query.with_entities(func.avg(Query.traffic_volume)).scalar())
    minimum = query.with_entities(func.min(Query.traffic_volume)).scalar()
    maximum = query.with_entities(func.max(Query.traffic_volume)).scalar()

    return render_template('result.html', header=header, option=option, average=average, minimum=minimum, maximum=maximum)


@main_bp.route("/logout")
@login_required
def logout():
    """Logs out the user and returns them to the login page"""
    logout_user()
    return redirect(url_for("auth_bp.login"))


# ROUTES THAT ALLOW PROGRAMMATIC ACCESS TO DATA (JSON RESPONSES) 

@app.get("/data/")
@login_required
def get_all_data():
    """Returns all data in the database"""
    # Get all data from the database
    data = Query.query.all()
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







