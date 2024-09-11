class RecordingsList:
    def __init__(self, filter_by: str,limit: int = None,page: int = None):
        self.filter_by = filter_by
        self.limit = limit
        self.page = page

    def prepare(self):
        recordingList = {}
        recordingList.update({
            "filter_by": self.filter_by
        })
        if(self.limit != None):
                 recordingList.update({"limit": self.limit})
        if(self.page != None):
                 recordingList.update({"page": self.page})
        return recordingList
