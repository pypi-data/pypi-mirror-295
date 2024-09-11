import requests
class MHApiService:
    BASE_URL = 'https://api.meethour.io'
    API_VERSION = 'v1.2'

    def __init__(self):
        self.http_client = requests.Session()
        self.http_client.headers.update({'Content-Type': 'application/json'})

    @staticmethod
    def api_endpoint_url(endpoint):
        base_url = MHApiService.BASE_URL
        api_version = MHApiService.API_VERSION

        if endpoint == 'login':
            return f"{base_url}/oauth/token"
        elif endpoint == 'add_contact':
            return f"{base_url}/api/{api_version}/customer/addcontact"
        elif endpoint == 'contacts':
            return f"{base_url}/api/{api_version}/customer/contacts"
        elif endpoint == 'edit_contact':
            return f"{base_url}/api/{api_version}/customer/editcontact"
        elif endpoint == 'edit_meeting':
            return f"{base_url}/api/{api_version}/meeting/editmeeting"
        elif endpoint == 'generate_jwt':
            return f"{base_url}/api/{api_version}/getjwt"
        elif endpoint == 'schedule_meeting':
            return f"{base_url}/api/{api_version}/meeting/schedulemeeting"
        elif endpoint == 'completed_meetings':
            return f"{base_url}/api/{api_version}/meeting/completedmeetings"
        elif endpoint == 'missed_meetings':
            return f"{base_url}/api/{api_version}/meeting/missedmeetings"
        elif endpoint == 'archive_meetings':
            return f"{base_url}/api/{api_version}/meeting/archivemeeting"
        elif endpoint == 'upcoming_meetings':
            return f"{base_url}/api/{api_version}/meeting/upcomingmeetings"
        elif endpoint == 'view_meetings':
            return f"{base_url}/api/{api_version}/meeting/viewmeeting"
        elif endpoint == 'recordings_list':
            return f"{base_url}/api/{api_version}/customer/videorecordinglist"
        elif endpoint == 'time_zone':
            return f"{base_url}/api/{api_version}/getTimezone"
        elif endpoint == 'user_details':
            return f"{base_url}/api/{api_version}/customer/user_details"
        elif endpoint == 'refresh_token':
            return f"{base_url}/oauth/token"
         
        
    '''
    * postFetch() : For making Post HTTP Methods via Guzzle HTTP Client
    * @param string $token endpoint End Point types.
    * @param string $endpoint  endpoint End Point types.
    * @param array  $body API call body.
    * @param array $pathParam  endpoint End Point types.
    * @return mixed response data that we get from API
    '''
    def substitute_path_parameter(self, endpoint, path_parm):
        if(path_parm==None):
            return endpoint
        else:
            return endpoint # need to add url path_parm
    
    def get_headers(self, token):      
        if token!="":
            return {"content-type":"application/json", "Authorization":"Bearer " + token}
        else:
            return {"content-type":"application/json"}
    
    def post_fetch(self, token, endpoint, body, path_param=None):
        constructed_url = self.substitute_path_parameter(
            self.api_endpoint_url(endpoint),
            path_param
        )
        try:
            response = requests.post(constructed_url, json=body, headers=self.get_headers(token))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(error)

    '''
     * login(): To authenticate and login to get access token
     * @param Login $loginObject Grant Type. Accepts "password"
     * @return mixed response data that we get from API.
    '''
    def login(self, login_object):
        body = login_object.prepare()
        return self.post_fetch('', 'login', body)
    
    '''
     * add_contact() : To add contact in Meet Hour Database.
     * @param string $token - access token to make API calls.
     * @param AddContact $addContactObject - API call body.
     * @return mixed response data that we get from API.
    '''

    def add_contact(self, token, add_contact_object):
        body = add_contact_object.prepare()
        return self.post_fetch(token, 'add_contact', body)
    
    '''
     * contacts() : To get all the contacts available on Meet Hour account.
     * @param string $token - access token to make API calls.
     * @param ContactsList $contactsListObject - API call body.
     * @return mixed response data that we get from API.
    ''' 
    def contacts(self,token, contacts_object):
        body = contacts_object.prepare()
        return self.post_fetch(token,'contacts',body)
    
    '''
     * edit_contact() : To edit a specific contact.
     * @param string $token - access token to make API calls.
     * @param EditContact $editContactObject - API call body.
     * @return mixed response data that we get from API.
    '''
    def edit_contact(self, token, edit_contact_object):
        body = edit_contact_object.prepare()
        return self.post_fetch(token,'edit_contact',body)
    
    '''
     * edit_meeting() : To Edit a specific meeting.
     * @param string $token - access token to make API calls.
     * @param EditMeeting $editMeetingObject - API call body.
     * @return mixed response data that we get from API.
    '''
    def edit_meeting(self,token,edit_meeting_object):
        body = edit_meeting_object.prepare()
        return self.post_fetch(token,'edit_meeting',body)
    
    '''
     * generateJwt() : JWT is needed to join the meeting with user information. Usually used if Moderator is joining.
     * @param string $token - access token to make API calls.
     * @param GenerateJwt $generateJwtObject - API call body.
     * @return mixed response data that we get from API.   
    ''' 
    def generate_jwt(self,token,generate_jwt_object):
        body = generate_jwt_object.prepare()
        return self.post_fetch(token,'generate_jwt',body)
    
    ''' 
     * schedule_meeting() : Function to hit a Schedule Meeting API.
     * @param string $token - access token to make API calls.
     * @param ScheduleMeeting $scheduleMeetingObject - API call body. 
     * @return mixed response data that we get from API.
    ''' 
    def schedule_meeting(self,token,schedule_meeting_object):
        body = schedule_meeting_object.prepare()
        return self.post_fetch(token,'schedule_meeting',body)
    
    ''' 
     * completed_meetings() : To get all the Completed Meetings.
     * @param string $token - access token to make API calls.
     * @param CompletedMeetings $completedMeetings - API call body.
     * @return mixed respos$e data that we get from API.
    ''' 
    def completed_meetings(self,token,completed_meetings_object):
        body = completed_meetings_object.prepare()
        return self.post_fetch(token,'completed_meetings',body)
    
    ''' 
     * missed_meetings() : To get all the Missed Meeting.
     * @param string $token - access token to make API calls.
     * @param MissedMeetings $missedMeetingsObject - API call body.
     * @return mixed response data that we get from API.
    ''' 
    def missed_meetings(self,token,missed_meetings_object):
        body = missed_meetings_object.prepare()
        return self.post_fetch(token,'missed_meetings',body) 
    
    ''' 
     * archive_meetings() : To get archive Meeting
     * @param string $token - access token to make API calls.
     * @param ArchiveMeeting $archiveMeeting - API call body.
     * @return mixed response data that we get from API.
    ''' 
    def archive_meetings(self,token,archive_meetings_object):
        body = archive_meetings_object.prepare()
        return self.post_fetch(token,'archive_meetings',body) 
    
    '''
     * upcoming_meetings() : Function to hit a Schedule Meeting API.
     * @param string $token - access token to make API calls.
     * @param UpcomingMeetings $upcomingMeetingsObject - API call body.
     * @return mixed response data that we get from API.
    '''
    def upcoming_meetings(self,token,upcoming_meetings_object):
        body = upcoming_meetings_object.prepare()
        return self.post_fetch(token,'upcoming_meetings',body)
    
    '''
     * viewMeeting() : To get information of specific meeting.
     * @param string $token - access token to make API calls.
     * @param ViewMeeting $viewMeetingObject - API call body.
     * @return mixed response data that we get from API.
    '''
    def view_meetings(self,token,view_meetings_object):
        body = view_meetings_object.prepare()
        return self.post_fetch(token,'view_meetings',body)
    '''
     * recordingsList() : To get all the recording list.
     * @param string $token - access token to make API calls.
     * @param RecordingsList $recordingsListObject - API call body.
     * @return mixed response data that we get from API.
    '''
    def recordings_list(self,token,recordings_list_object):
        body = recordings_list_object.prepare()
        return self.post_fetch(token,'recordings_list',body)
    '''
     * getRefreshToken(): To get new token from refresh token
     * @param string $token access token to make API calls.
     * @param RefreshToken $refreshTokenObject API call body.
     * @return mixed response data that we get from API.
    '''
    def refresh_token(self,token,refresh_token_object):
        body = refresh_token_object.prepare()
        return self.post_fetch(token,'refresh_token',body)

    #timezone
    def time_zone(self,token,timezone_object):
        body = timezone_object.prepare()
        return self.post_fetch(token,'time_zone',body)
    
    #userdetails
    def user_details(self,token,userdetails_object):
        body = userdetails_object.prepare()
        return self.post_fetch(token,'user_details',body)
    
