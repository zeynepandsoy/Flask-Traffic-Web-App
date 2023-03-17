
"""Logged-in page routes."""
# make responses json 

import sys, json
from flask import Blueprint, redirect, render_template, url_for
from flask import(
    current_app as app,
    request,
    make_response,
    jsonify,
)
from flask_login import current_user, login_required, logout_user

from sqlalchemy import func
from collections import defaultdict

from traffic_app import db
from traffic_app.models import Query
from traffic_app.schemas import QuerySchema


#from sqlalchemy import create_engine


#engine = create_engine('sqlite:///path/to/traffic.db')

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
    #response = get_queries()
    headers = [col.name for col in Query.__table__.columns if col.name not in ['traffic_volume','record_id']]
    return render_template(
        "dashboard.html",
        current_user=current_user,
        headers=headers
        #body="You are now logged in!",
        #query_list=response
    )

    #with engine.connect() as con:
        #result = con.execute(f"SELECT DISTINCT {header} FROM Query ORDER BY {header}")
        #options = [option[0] for option in result.fetchall()]

#options = db.session.query(Query).with_entities(header).distinct().order_by(header).all()
#options = [option[0] for option in options]

# is clicking on a dropdown option a GET or POST request?

@main_bp.route('/query/<header>', methods=["GET","POST"])
@login_required
def query(header):
    """Dropdown menu for query options"""
 
    options = db.session.query(Query).distinct(header).order_by(header).all()
    
    #column_obj = getattr(Query, header)
    #options = db.session.query(column_obj).distinct().order_by(column_obj).all()
    #options = [option[0] for option in options]
    
    return render_template('query.html', header=header, options=options)



@main_bp.route('/result/<header>/<option>')
@login_required
def result(header, option):
    """Summary statistics / results page of selected query (dropdown option))"""
    query = db.session.query(Query).filter(getattr(Query, header) == option)
    average = query.with_entities(func.avg(Query.traffic_volume)).scalar()
    minimum = query.with_entities(func.min(Query.traffic_volume)).scalar()
    maximum = query.with_entities(func.max(Query.traffic_volume)).scalar()
    return render_template('result.html', header=header, option=option, average=average, minimum=minimum, maximum=maximum)



@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for("auth_bp.login"))





    
