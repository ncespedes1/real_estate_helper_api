from app.extensions import ma
from app.models import County_name_mapping

class County_name_mappingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = County_name_mapping


county_name_mapping_schema = County_name_mappingSchema()
county_name_mappings_schema = County_name_mappingSchema(many=True)