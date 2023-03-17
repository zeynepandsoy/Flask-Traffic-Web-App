from traffic_app.models import Query
from traffic_app import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# -------------------------
# Flask-Marshmallow Schemas
# See https://marshmallow-sqlalchemy.readthedocs.io/en/latest/#generate-marshmallow-schemas
# -------------------------

class QuerySchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class. Inherits all the attributes from the Event class."""

    class Meta:
        model = Query
        include_fk = True
        load_instance = True
        sqla_session = db.session
        #include_relationships = True