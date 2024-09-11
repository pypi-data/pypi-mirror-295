class MissedMeetings:
    def __init__(self,limit: int = None,page: int =None,show_all: int = None ):
        self.limit = limit
        self.page = page
        self.show_all = show_all

    def prepare(self):
        missedMeetings: dict= {}
        if(self.limit != None):
                 missedMeetings.update({"limit": self.limit})
        if(self.show_all != None):
                 missedMeetings.update({"show_all": self.show_all})
        if(self.page != None):
                 missedMeetings.update({"page": self.page})
        return (
            missedMeetings
        )
