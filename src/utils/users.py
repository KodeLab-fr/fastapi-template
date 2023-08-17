from pydantic import BaseModel


# PYDANTIC
class UserBase(BaseModel):
    username: str

    def __init__(self, username: str):
        super().__init__(username=username)

    def __repr__(self):
        return f"<UserBase(username={self.username})>"

    def __str__(self):
        return f"<UserBase(username={self.username})>"
