class Payloads:
    """ """

    def __init__(self):
        self.payloads = [
            {
                "event_type": "save_meeting_recording",
                "event_id": "evt_7af36fce24ec30d2da27de29ead5a9a0",
                "timestamp": "2024-05-09T10:41:09Z",
                "data": {
                    "meeting_id": "MHR240416944",
                    "customer": {
                        "name": "Padmanabha",
                        "email": "padmanabham2005@gmail.com",
                    },
                    "recording_type": "Custom",
                    "recording_name": "MHR240430125504-1714552910.mp4",
                    "recording_path":
                    "https://meethour-recording.s3.amazonaws.com/recordings/125504/MHR240430125504/1714552910/MHR240430125504-1714552910.mp4?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIASTOG4L4UPVPXO6CP%2F20240509%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240509T104109Z&X-Amz-SignedHeaders=host&X-Amz-Expires=604800&X-Amz-Signature=8814bbcc9240a138f466f307ac4826a28d4013d3865e2402c06a8618c2d4e324",
                    "recording_date": "2024-05-09 10:41:06",
                    "status": 1,
                    "duration": "0:03:5",
                    "duration_format": "HH:mm:ss",
                    "recording_size": 6,
                    "recording_size_unit": "MB",
                    "recording_expiry": "2024-05-16 10:41:09",
                    "time_zone": "UTC",
                },
            },
            {
                "event_type": "join_meeting",
                "event_id": "evt_4e9443ddbdcb60eb15a00ca347bd9632",
                "timestamp": "2024-05-24T14:05:37Z",
                "data": {
                    "meeting_id": "MHR2405241977",
                    "attendee": {
                        "name": "syam",
                        "email": "syam.prasad@mailinator.com"
                    },
                    "login_datetime": "2024-05-24 14:03:14",
                    "user_agent": "chrome",
                    "access_type": "app",
                    "ip": "183.82.99.179",
                    "location": {
                        "country_name": "India",
                        "country_code": "IN",
                        "city": "Prakashamnagar",
                        "postal": "500016",
                        "latitude": 17.4427,
                        "longitude": 78.4751,
                        "state": "Telangana",
                    },
                },
            },
            {
                "event_type": "exit_meeting",
                "event_id": "evt_b53f85d54ccd3a3669034fce77d75f9d",
                "timestamp": "2024-05-24T14:05:37Z",
                "data": {
                    "meeting_id": "MHR2405241977",
                    "attendee": {
                        "name": "syam",
                        "email": "syam.prasad@mailinator.com"
                    },
                    "logout_datetime": "2024-05-24 14:04:08",
                    "user_agent": "chrome",
                    "access_type": "app",
                    "ip": "183.82.99.179",
                    "location": {
                        "country_name": "India",
                        "country_code": "IN",
                        "city": "Prakashamnagar",
                        "postal": "500016",
                        "latitude": 17.4427,
                        "longitude": 78.4751,
                        "state": "Telangana",
                    },
                },
            },
            {
                "event_type": "Unknown_event",
                "event_id": "ukn_b53f85d54ccd3a3669034fce77d98gp4d",
                "timestamp": "2024-05-24T14:05:37Z",
                "data": {},
            },
        ]

    def get_payloads(self):
        """ """
        return self.payloads
