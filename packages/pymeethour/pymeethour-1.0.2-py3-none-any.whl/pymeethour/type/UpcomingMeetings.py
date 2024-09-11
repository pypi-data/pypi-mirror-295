class UpcomingMeetings:
    def __init__(self, limit : int = None,page : int = None, show_all : int = None):
        self.limit = limit
        self.page = page
        self.show_all = show_all

    def prepare(self):
        upcomingMeetings: dict= {}
        if(self.limit != None):
                 upcomingMeetings.update({"limit": self.limit})
        if(self.page != None):
                 upcomingMeetings.update({"page": self.page})
        if(self.show_all != None):
                 upcomingMeetings.update({"show_all": self.show_all})
        return (upcomingMeetings)