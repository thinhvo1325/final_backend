from typing import Any
from fastapi import HTTPException
def handler_response(code: int, data: Any, message: str):
    """
    Handler for the response from the server.
    """
    return {
            "code": code,
            "message": message,
            "data": data
    }

def response_return(code: int, data: Any, message: str):
    if code == 200:
        return {
            "code": code,
            "message": message,
            "data": data
    }
    else:
        raise HTTPException(status_code=code, detail=message)