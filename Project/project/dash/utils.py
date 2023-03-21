from pydantic import BaseModel


class Token(BaseModel):
    token: str = ''


API_URL = 'http://localhost:3012/'
token = Token()


def get_auth_header():
    return {'Authorization': f'Bearer {token.token}'}
