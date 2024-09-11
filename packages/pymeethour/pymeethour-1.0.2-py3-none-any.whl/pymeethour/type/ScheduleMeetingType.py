class ScheduleMeeting:
    def __init__(
        self,
        meeting_name: str,
        passcode: str,
        meeting_time: str,
        meeting_meridiem: str,
        meeting_date: str,
        timezone: str,
        default_recording_storage: str = "Dropbox",
        send_calendar_invite: int = 0 ,
        agenda: str = None,
        attend: list = None,
        duration_hr: int  = None,
        duration_min: int = None,
        enable_pre_registration: int = None,
        endBy: str = None,
        end_date_time: str = None,
        end_times: int = None,
        groups: list[str,int] = None,
        hostusers: list = None,
        is_recurring: str = None,
        is_show_portal: int = 0,
        meeting_agenda: str = None,
        meeting_topic: str = None,
        monthlyBy: str = None,
        monthlyByDay: str = None,
        monthlyByWeekday: str = None,
        monthlyByWeekdayIndex: str = None,
        options: list = None,
        recurring_type: str = None,
        repeat_interval: int = None,
        weeklyWeekDays: int = None
    ):
        self.agenda = agenda
        self.attend = attend
        self.default_recording_storage = default_recording_storage
        self.duration_hr = duration_hr
        self.duration_min = duration_min
        self.enable_pre_registration = enable_pre_registration
        self.endBy = endBy
        self.end_date_time = end_date_time
        self.end_times = end_times
        self.groups = groups
        self.hostusers = hostusers
        self.is_recurring = is_recurring
        self.is_show_portal = is_show_portal
        self.meeting_agenda = meeting_agenda
        self.meeting_date = meeting_date
        self.meeting_meridiem = meeting_meridiem
        self.meeting_name = meeting_name
        self.meeting_time = meeting_time
        self.meeting_topic = meeting_topic
        self.monthlyBy = monthlyBy
        self.monthlyByDay = monthlyByDay
        self.monthlyByWeekday = monthlyByWeekday
        self.monthlyByWeekdayIndex = monthlyByWeekdayIndex
        self.options = options
        self.passcode = passcode
        self.recurring_type = recurring_type
        self.repeat_interval = repeat_interval
        self.send_calendar_invite = send_calendar_invite
        self.timezone = timezone
        self.weeklyWeekDays = weeklyWeekDays

    def prepare(self):
        scheduleMeeting = {} 
        scheduleMeeting.update({
            "default_recording_storage": self.default_recording_storage,
            "meeting_date": self.meeting_date,
            "meeting_meridiem": self.meeting_meridiem,
            "meeting_name": self.meeting_name,
            "meeting_time": self.meeting_time,
            "passcode": self.passcode,
            "send_calendar_invite": self.send_calendar_invite,
            "is_show_portal": self.is_show_portal,
            "timezone": self.timezone
        })
        if(self.agenda != None):
                 scheduleMeeting.update({"agenda": self.agenda})
        if(self.attend != None):
                 scheduleMeeting.update({"attend": self.attend})
        if(self.duration_hr != None):
                 scheduleMeeting.update({"duration_hr": self.duration_hr})
        if(self.duration_min != None):
                 scheduleMeeting.update({"duration_min": self.duration_min})
        if(self.enable_pre_registration != None):
                 scheduleMeeting.update({"enable_pre_registration": self.enable_pre_registration})
        if(self.endBy != None):
                 scheduleMeeting.update({"endBy": self.endBy})
        if(self.end_date_time != None):
                 scheduleMeeting.update({"end_date_time": self.end_date_time})
        if(self.end_times != None):
                 scheduleMeeting.update({"end_times": self.end_times})
        if(self.groups != None):
                 scheduleMeeting.update({"groups": self.groups})
        if(self.hostusers != None):
                 scheduleMeeting.update({"hostusers": self.hostusers})
        if(self.is_recurring != None):
                 scheduleMeeting.update({"is_recurring": self.is_recurring})
        if(self.meeting_topic != None):
                 scheduleMeeting.update({"meeting_topic": self.meeting_topic})
        if(self.monthlyBy != None):
                 scheduleMeeting.update({"monthlyBy": self.monthlyBy})
        if(self.monthlyByDay != None):
                 scheduleMeeting.update({"monthlyByDay": self.monthlyByDay})
        if(self.monthlyByWeekday != None):
                 scheduleMeeting.update({"monthlyByWeekday": self.monthlyByWeekday})
        if(self.monthlyByWeekdayIndex != None):
                 scheduleMeeting.update({"monthlyByWeekdayIndex": self.monthlyByWeekdayIndex})
        if(self.options != None):
                 scheduleMeeting.update({"options": self.options})
        if(self.recurring_type != None):
                 scheduleMeeting.update({"recurring_type": self.recurring_type})
        if(self.repeat_interval != None):
                 scheduleMeeting.update({"repeat_interval": self.repeat_interval})
        if(self.weeklyWeekDays != None):
                 scheduleMeeting.update({"weeklyWeekDays": self.weeklyWeekDays})      
        return scheduleMeeting  