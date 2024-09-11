class GenerateJwt:
    def __init__(self, meeting_id: str, contact_id: int = None, ui_config = None, config = None):
        self.meeting_id = meeting_id
        self.contact_id = contact_id
        self.ui_config = ui_config
        self.config = config

    def prepare(self):
        generateJwt = {}
        generateJwt.update({
            "meeting_id": self.meeting_id,
            "contact_id": self.contact_id
        })
            
        if(self.config != None):
                 generateJwt.update({"config": self.config})
        if(self.ui_config != None):
                 generateJwt.update({"ui_config": self.ui_config})
        return generateJwt