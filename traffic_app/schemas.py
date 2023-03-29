from traffic_app.models import Query
from traffic_app import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# -------------------------
# Flask-Marshmallow Schemas
# -------------------------

class QuerySchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of Query class."""

    class Meta:
        model = Query
        include_fk = True
        load_instance = True
        sqla_session = db.session
    