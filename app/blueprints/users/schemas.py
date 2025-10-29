from app.extensions import ma
from app.models import Users

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users


user_schema = UserSchema()
users_schema = UserSchema(many=True)
login_schema = UserSchema(exclude=['role', 'id'])