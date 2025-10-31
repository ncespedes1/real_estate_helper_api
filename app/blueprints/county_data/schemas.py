from app.extensions import ma
from app.models import County_data

class County_dataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = County_data
        include_fk = True


county_data_schema = County_dataSchema()
counties_data_schema = County_dataSchema(many=True)