from api.models.base_model import BaseModel

class Comment(BaseModel):
    """
    Comment model class
    """
    story_id = ""
    username = ""
    text = ""

