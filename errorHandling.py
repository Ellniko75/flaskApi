from flask import make_response
from dotenv import load_dotenv
import os


def IsApiKeyError(request):
    # IF THERE ARE ERRORS WITH THE API KEY IT RETURNS A RESPONSE, ELSE IT RETURNS None
    load_dotenv()
    if 'Key' not in request.headers:
        return make_response("A Key is required for access", 403)

    api_key = request.headers['Key']
    if api_key != os.getenv("API_KEY"):
        return make_response("Invalid Key", 403)

    return None
