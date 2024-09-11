class ViewMeeting:
    def __init__(self, meeting_id : int, occurrences = None, meeting_attendees = None, organizer = None):
        self.meeting_id = meeting_id
        self.occurrences = occurrences
        self. meeting_attendees = meeting_attendees
        self. organizer = organizer
    def prepare(self):
        viewmeeting = {}
        viewmeeting.update({
              "meeting_id": self.meeting_id
        })  
        if(self.occurrences != None):
                 viewmeeting.update({"occurrences": self.occurrences})
        if(self.meeting_attendees != None):
                 viewmeeting.update({"meeting_attendees": self.meeting_attendees})
        if(self.organizer != None):
                 viewmeeting.update({"organizer": self.organizer})
        return viewmeeting