from api.models.base_model import BaseModel

class Story(BaseModel):
    """
    Story model class
    """
    title = ""
    summary = ""
    content = ""
    category = ""  # resolved, coldcase, update
    votes = 0

