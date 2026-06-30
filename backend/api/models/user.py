from api.models.base_model import BaseModel

class User(BaseModel):
    """
    User model class
    """
    username = ""
    email = ""
    password = ""
    role = "user"  # Can be user or admin

