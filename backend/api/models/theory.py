from api.models.base_model import BaseModel

class Theory(BaseModel):
    """
    Theory model class
    """
    story_id = ""
    username = ""
    title = ""
    content = ""
    likes = 0

