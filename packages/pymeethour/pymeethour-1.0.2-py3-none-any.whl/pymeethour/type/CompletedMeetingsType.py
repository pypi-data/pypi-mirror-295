class CompletedMeetings:
    def __init__(self):
        self.limit = None
        self.page = None
        self.show_all = None

    def prepare(self):
        completeMeeting: dict= {}
        if(self.show_all != None):
                 completeMeeting.update({"show_all": self.show_all})
        if(self.limit != None):
                 completeMeeting.update({"limit": self.limit})
        if(self.page != None):
                 completeMeeting.update({"page": self.page})
        return completeMeeting
