import urllib

import requests


UP_API_OAUTH_HOST = "https://jawbone.com/auth/oauth2/auth"
UP_API_OAUTH_TOKEN_HOST = 'https://jawbone.com/auth/oauth2/token'
UP_API_HOST = "https://jawbone.com/nudge/api"


def _build_param_dict(items):
    """
    Function which builds the dictionary for encoding the url parameters.

    :param items: A dictionary contain key,values

    :return: A cleaned dictionary used for url encoding parameters
    """
    p = {}
    for k, v in items.iteritems():
        if k is not 'self' and k is not 'access_token':
            if v:
                p[k] = v

    return p


def _url_handler(url, access_token, request_type=None):
    """
    Private method used to handle url requests for the api methods

    :param url: The url to access
    :param access_token: A valid access token
    :param request_type: Default is GET, the HTTP request type

    :return: The data of the request, or error code
    """
    try:
        if request_type is 'POST':
            res = requests.post(url, headers=dict(Authorization="Bearer " + str(access_token)))
            pass
        elif request_type is 'DELETE':
            res = requests.delete(url, headers=dict(Authorization="Bearer " + str(access_token)))
        else:
            res = requests.get(url, headers=dict(Authorization="Bearer " + str(access_token)))
        if res.status_code == 200:
            return res.json()
        return dict(status_code=res.status_code)
    except requests.ConnectionError, e:
        return dict(status_code=e.message)


class UpAPI():
    def __init__(self, scopes=None):
        self.refresh_token = ''
        self.code = ''
        self.client_id = ''
        self.app_secret = ''
        self.redirect_uri = ''
        self.scope = scopes or "basic_read extended_read move_read sleep_read"
        self.access_token = ''

    def get_initial_connect_auth_code_url(self):
        """
        Gets the initial url required for the authentication code

        :return: The url needed to authenticate
        """
        q = dict(response_type='code', client_id=self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
        return UP_API_OAUTH_HOST + "?" + urllib.urlencode(q)

    def get_auth_code(self):
        """
        Gets the authentication code from Jawbone

        :return: The authentication code
        """
        if self.code:
            return self.code

        url = self.get_initial_connect_auth_code_url()
        res = requests.get(url)

        if res.status_code == 200:
            code = res.json()['code']
            self.code = code
            return self.code

        return None

    @property
    def get_access_token(self):
        return self.access_token

    def exchange_code_for_token(self, code):
        """
        Exchanges the authentication code for an access token

        :param code (str): The code we plan on exchanging for an access token

        :return : Access Token
        """

        u = UP_API_OAUTH_TOKEN_HOST + '?client_id=' + self.client_id
        u += '&client_secret=' + self.app_secret
        u += '&grant_type=authorization_code'
        u += '&code=' + code

        res = requests.get(u)

        if res.status_code == 200:
            self.refresh_token = res.json()['refresh_token']
            self.access_token = res.json()['access_token']
            return self.access_token
        return None

    @staticmethod
    def get_band_events(access_token, date=None, start_time=None, end_time=None, created_after=None):
        """
        Returns the band hardware events generated by the UP24 bluetooth connected band.

        :param access_token (str): The valid access token
        :param date (str): Date, formatted as YYYYMMDD. If omitted, returns the information for today.
        :param start_time (int): To be used along with end_time.
        :param end_time (int): To be used with start_time.
        :param created_after (int): Epoch timestamp to list events that are created later than the timestamp.

        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/bandevents' + '?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_user_goals(access_token):
        """
        Returns the goals the user has set for UP. Currently takes no parameters and is read only.

        :param access_token (str): The valid access token

        :return: The response or error code of the request
        """
        return _url_handler(UP_API_HOST + '/users/@me/goals', access_token)

    @staticmethod
    def set_user_goal(access_token, move_steps=None, sleep_total=None, body_weight=None, body_weight_intent=None):
        """
        Updates the user goal. Note your app must have the correct scope to update the respective goal.

        :param access_token (str): The valid access token
        :param move_steps: Move goal per day in number of steps. Need scope move_write.
        :param sleep_total: Sleep goal per day in seconds. Need scope sleep_write.
        :param body_weight: Body weight goal. MUST be in metric (kg). Need scope body_write.
        :param body_weight_intent: User's desired weight management intent. 0=lose, 1=maintain, 2=gain. Need body_write.

        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/goals' + '?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token, request_type='POST')

    @staticmethod
    def get_resting_heartrate(access_token, date=None, page_token=None, start_time=None, end_time=None,
                              updated_after=None,
                              limit=None):
        """
        Returns a single resting heart rate measurement captured at a specific, non-configurable time via an UP3 device.

        :param access_token (str): The valid access token
        :param date (str): Date, formatted as YYYYMMDD. If omitted, returns the information for today.
        :param page_token (int): Timestamp used to paginate the list of events.
        :param start_time (int): To be used along with end_time.
        :param end_time (int): To be used with start_time.
        :param updated_after (int): Epoch timestamp to list events that have been updated later than the timestamp.
        :param limit (int): Maximum number of results to return

        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/heartrates' + '?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_user_details(access_token):
        """
        Returns the basic information of the user
        :param access_token (str): The access token required
        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me'
        return _url_handler(url, access_token)

    @staticmethod
    def get_friends_list(access_token):
        """
        Returns the list of unique identifiers (XIDs) of the user's friends.

        :param access_token: The access token required

        :return: The response or error code of the request
        """
        return _url_handler(UP_API_HOST + '/users/@me/friends', access_token)

    @staticmethod
    def get_workouts_list(access_token, date=None, page_token=None, start_time=None, end_time=None, updated_after=None,
                          limit=None):
        """
        Returns the list of workouts of the current user.

        :param access_token (str): The valid access token
        :param date (int): Date, formatted as YYYYMMDD. If omitted, returns the information for today.
        :param page_token (int): Timestamp used to paginate the list of workouts.
        :param start_time (int): To be used along with end_time.
        :param end_time (int): To be used with start_time.
        :param updated_after (int): Epoch timestamp to list events that are updated later than the timestamp.
        :param limit (int): Maximum number of results to return

        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/workouts?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_workout_info(access_token, xid):
        """
        Returns detailed information about the given workout.

        :param access_token (str): The valid access token
        :param xid (str): The workout xid

        :return: The response or error code of the request
        """
        return _url_handler(UP_API_HOST + '/users/@me/workouts/' + str(xid), access_token)

    @staticmethod
    def get_workout_graph(access_token, xid):
        """
        Returns the image of the given workout.

        :param access_token (str): The valid access token
        :param xid (str): The workout xid

        :return: The image of the workout or error code of the request
        """
        return _url_handler(UP_API_HOST + '/users/@me/workouts/' + str(xid) + '/image', access_token)

    @staticmethod
    def get_workout_ticks(access_token, xid):
        """
        Returns granular details for the specific Workout event.

        :param access_token (str): The valid access token
        :param xid (str): The workout xid

        :return: The response or error code of the request
        """
        return _url_handler(UP_API_HOST + '/users/@me/workouts/' + str(xid) + '/ticks', access_token)

    @staticmethod
    def get_trends(access_token, num_buckets, bucket_size=None, end_date=None):
        """
        Returns the user's trends over a period of time (e.g. 5 weeks), using the given granularity (e.g. by day).

        :param access_token (str): The valid access token
        :param num_buckets (int): Required. The number of buckets to return, starting at the given end_date and going
        backwards in time. Maximum is 100.
        :param bucket_size (str): Determines the granularity to use when aggregating the values.
        Possible values are: d (for days), w (for weeks), m (for months), y (for years). If omitted will default to days
        :param end_date (int): Date, formatted as YYYYMMDD. If omitted will default to today.

        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/trends' + '?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_moves_list(access_token, date=None, start_time=None, end_time=None, updated_after=None,
                       page_token=None):
        """
        Returns the list of moves of the current user.

        :param access_token (str):
        :param date (int): Date, formatted as YYYYMMDD. If omitted, returns the information for today.
        :param start_time (int): To be used along with end_time.
        :param end_time (int): To be used with start_time.
        :param updated_after (int): Epoch timestamp to list move events that are updated later than the timestamp.
        :param page_token (int): Timestamp used to paginate the list of moves.

        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/moves?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_move_info(access_token, move_xid):
        """
        Returns the detailed information of the given move.

        :param access_token (str): The valid access token
        :param move_xid (str): The xid of the move

        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/moves/' + str(move_xid)
        return _url_handler(url, access_token)

    @staticmethod
    def get_move_graph(access_token, move_xid):
        """
        Returns the image of the given move.

        :param access_token (str): The valid access token
        :param move_xid (str): The xid of the move

        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/moves/' + str(move_xid) + "/image"
        return _url_handler(url, access_token)

    @staticmethod
    def get_move_ticks(access_token, move_xid):
        """
        Returns granular details for the specific Move event.

        :param access_token (str): The valid access token
        :param move_xid (str): The xid of the move

        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/moves/' + move_xid + "/ticks"
        return _url_handler(url, access_token)

    @staticmethod
    def get_sleeps_list(access_token, date=None, start_time=None, end_time=None, updated_after=None,
                        page_token=None):
        """
        Returns the list of sleeps of the current user.

        :param access_token (str): The valid access token
        :param date (int): Date, formatted as YYYYMMDD. If omitted, returns the information for today.
        :param start_time (int): To be used along with end_time.
        :param end_time (int): To be used with start_time.
        :param updated_after (int): Epoch timestamp to list events that are updated later than the timestamp.
        :param page_token (int): Timestamp used to paginate the list of sleeps.

        :return:The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/sleeps?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_generic_api_call(access_token, endpoint='/users/@me', **kwargs):
        """
        Generic method for any API get call to Jawbone.

        :param access_token (str): The access_token
        :param endpoint (str): Endpoint we want to go against eg '/users/@me/'
        :param **kwargs: Any additional parameters

        :return: The response or error
        """
        url = UP_API_HOST + endpoint + '?' + urllib.urlencode(kwargs.items())
        return _url_handler(url, access_token)

    @staticmethod
    def revoke_access_token(access_token):
        """
        Disconnects user from application

        :param access_token (str): The access token required

        :return: The response of the request
        """

        return requests.delete(UP_API_HOST + '/users/@me/PartnerAppMembership',
                               headers=dict(Authorization="Bearer " + access_token))