from starlette import status
from starlette.responses import JSONResponse


def ok(values, message):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"values": values, "message": message})

def webhookres(value):
    return  JSONResponse(status_code=status.HTTP_200_OK, headers={"Content-Type" : "application/json"}, content=value)

def badRequest(values, message):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"values": values, "message": message})

def test():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"values": 'test value', "message": 'test'})
