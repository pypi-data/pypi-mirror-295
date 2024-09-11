class user_details:
    def __init__(self,success,code,message,data ):
        self.success = success
        self.code = code
        self.message = message
        self.data = data

    def prepare(self):
        return {
            "success": self.success,
            "code": self.code,
            "message": self.message,
            "data": self.data
        }