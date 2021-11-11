class CustomResponse:
    def __init__(self):
        self.__def_response = {
            "code": 100,
            "data": None,
            "message": None
        }

    def reset_response(self):
        self.__def_response["code"] = 100
        self.__def_response["data"] = None
        self.__def_response["message"] = None

    def get_response(self, code=200, data=None, message=None):
        self.__def_response["code"] = code
        self.__def_response["data"] = data
        self.__def_response["message"] = message
        return self.__def_response
