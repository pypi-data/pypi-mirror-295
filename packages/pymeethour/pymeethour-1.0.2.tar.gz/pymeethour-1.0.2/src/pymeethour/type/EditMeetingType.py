from typing import List, Union

class UserObjectType:
    def __init__(self, email: str = None, first_name: str = None, last_name: str = None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
    
    def prepare(self):
        userObjects: dict= {}
        if(self.email != None):
                 userObjects.update({"email": self.email})
        if(self.first_name != None):
                 userObjects.update({"first_name": self.first_name})
        if(self.last_name != None):
                 userObjects.update({"last_name": self.last_name})
        return (userObjects)  
    
class EditMeeting:
    def __init__(
        self,
        meeting_id: str,
        attend: Union[List[int], List[UserObjectType], List[Union[int, UserObjectType]]] = None,
        agenda: str = None,
        duration_hr: int = None,
        duration_min: int = None,
        enable_pre_registration: int = None,
        end_by: str = None,
        end_date_time: str = None,
        groups: List[int] = None,
        hostusers: Union[List[int], List[UserObjectType], List[Union[int, UserObjectType]]] = None,
        instructions: str = None,
        is_recurring: int = None,
        is_show_portal: int = None,
        meeting_agenda: str = None,
        meeting_date: str = None,
        meeting_meridiem: str = None,
        meeting_name: str = None,
        meeting_time: str = None,
        meeting_topic: str = None,
        old_attend: Union[List[int], List[UserObjectType], List[Union[int, UserObjectType]]] = None,
        options: List[str] = None,
        passcode: str = None,
        recurring_type: str = None,
        repeat_interval: int = None,
        timezone: str = None
    ):
        self.attend = attend
        self.meeting_id = meeting_id
        self.agenda = agenda
        self.duration_hr = duration_hr
        self.duration_min = duration_min
        self.enable_pre_registration = enable_pre_registration
        self.end_by = end_by
        self.end_date_time = end_date_time
        self.groups = groups
        self.hostusers = hostusers
        self.instructions = instructions
        self.is_recurring = is_recurring
        self.is_show_portal = is_show_portal
        self.meeting_agenda = meeting_agenda
        self.meeting_date = meeting_date
        self.meeting_meridiem = meeting_meridiem
        self.meeting_name = meeting_name
        self.meeting_time = meeting_time
        self.meeting_topic = meeting_topic
        self.old_attend = old_attend
        self.options = options
        self.passcode = passcode
        self.recurring_type = recurring_type
        self.repeat_interval = repeat_interval
        self.timezone = timezone
    def prepare(self):
        editMeeting = {}
        editMeeting.update({
            "meeting_id" : self.meeting_id
        })
        if(self.attend != None):
                 editMeeting.update({"attend": self.attend})
        if(self.agenda != None):
                 editMeeting.update({"agenda" : self.agenda})
        if(self.duration_hr != None):
                 editMeeting.update({"duration_hr" : self.duration_hr})
        if(self.duration_min != None):
                 editMeeting.update({"duration_min" : self.duration_min})
        if(self.enable_pre_registration != None):
                 editMeeting.update({"enable_pre_registration" : self.enable_pre_registration})
        if(self.end_by != None):
                 editMeeting.update({"end_by" : self.end_by})
        if(self.end_date_time != None):
                 editMeeting.update({"end_date_time" : self.end_date_time})
        if(self.groups != None):
                 editMeeting.update({"groups" : self.groups})
        if(self.hostusers != None):
                 editMeeting.update({"hostusers" : self.hostusers})
        if(self.instructions != None):
                 editMeeting.update({"instructions" : self.instructions})
        if(self.is_recurring != None):
                 editMeeting.update({"is_recurring" : self.is_recurring})
        if(self.is_show_portal != None):
                 editMeeting.update({"is_show_portal" : self.is_show_portal})
        if(self.meeting_agenda != None):
                 editMeeting.update({"meeting_agenda" : self.meeting_agenda})
        if(self.meeting_date != None):
                 editMeeting.update({"meeting_date" : self.meeting_date})
        if(self.meeting_meridiem != None):
                 editMeeting.update({"meeting_meridiem" : self.meeting_meridiem})
        if(self.meeting_name != None):
                 editMeeting.update({"meeting_name" : self.meeting_name})
        if(self.meeting_time != None):
                 editMeeting.update({"meeting_time" : self.meeting_time})
        if(self.meeting_topic != None):
                 editMeeting.update({"meeting_topic" : self.meeting_topic})
        if(self.old_attend != None):
                 editMeeting.update({"old_attend" : self.old_attend})
        if(self.options != None):
                 editMeeting.update({"options" : self.options})
        if(self.passcode != None):
                 editMeeting.update({"passcode" : self.passcode})
        if(self.recurring_type != None):
                 editMeeting.update({"recurring_type" : self.recurring_type})
        if(self.repeat_interval != None):
                 editMeeting.update({"repeat_interval" : self.repeat_interval})
        if(self.timezone != None):
                 editMeeting.update({"timezone" : self.timezone})
        return editMeeting