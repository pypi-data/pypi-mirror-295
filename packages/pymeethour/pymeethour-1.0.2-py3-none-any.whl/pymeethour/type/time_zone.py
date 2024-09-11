class time_zone:
    def __init__(self,success,message,timezone):
        self.success = success
        self.message = message
        self.timezone = timezone

    def prepare(self):
        return {
            "success": self.success,
            "message": self.message,
            "timezone": self.timezone
        }