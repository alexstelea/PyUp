import requests
import urllib

UP_API_OAUTH_HOST = "https://jawbone.com/auth/oauth2/auth"
UP_API_OAUTH_TOKEN_HOST = 'https://jawbone.com/auth/oauth2/token'
UP_API_HOST = "https://jawbone.com/nudge/api"


def _build_param_dict(items):
    """
    Function which builds the dictionary for encoding the url paramters.
    :param items: A dictionary contain key,values
    :return: A cleaned dictionary used for url encoding paramters
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

        :return: The url needed to authenticate
        """
        q = dict(response_type='code', client_id=self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
        return UP_API_OAUTH_HOST + "?" + urllib.urlencode(q)

    def get_auth_code(self):
        if self.code:
            return self.code

        url = self.get_initial_connect_auth_code_url()
        res = requests.get(url)

        if res.status_code == 200:
            code = res.json()['code']
            self.code = code
            return self.code

    @property
    def get_access_token(self):
        return self.access_token

    def exchange_code_for_token(self, code):
        """
        :param code : The code we plan on exchanging for an access token
        :rtype : Access Token
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
        url = UP_API_HOST + '/users/@me/bandevents' + '?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_user_goals(access_token):
        return _url_handler(UP_API_HOST + '/users/@me/goals', access_token)

    @staticmethod
    def set_user_goal(access_token, move_steps=None, sleep_total=None, body_weight=None, body_weight_intent=None):
        """

        :param access_token:
        :param move_steps:
        :param sleep_total:
        :param body_weight:
        :param body_weight_intent:
        :return:
        """
        url = UP_API_HOST + '/users/@me/goals' + '?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token, request_type='POST')

    @staticmethod
    def get_resting_heartrate(access_token, date=None, page_token=None, start_time=None, end_time=None,
                              updated_after=None,
                              limit=None):
        """

        :param access_token:
        :param date:
        :param page_token:
        :param start_time:
        :param end_time:
        :param updated_after:
        :param limit:
        :return:
        """
        url = UP_API_HOST + '/users/@me/heartrates' + '?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_user_details(access_token):
        """
        Returns the details of the authenticated user
        :param access_token: The access token required
        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me'
        return _url_handler(url, access_token)

    @staticmethod
    def get_friends_list(access_token):
        """
        Returns the details of the authenticated user
        :param access_token: The access token required
        :return: The response or error code of the request
        """
        return _url_handler(UP_API_HOST + '/users/@me/friends', access_token)

    @staticmethod
    def get_workouts_list(access_token, date=None, page_token=None, start_time=None, end_time=None, updated_after=None,
                          limit=None):
        """
        Returns the details of the authenticated user
        :param access_token: The access token required
        :return: The response or error code of the request
        """
        url = UP_API_HOST + '/users/@me/workouts?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_workout_info(access_token, xid):
        return _url_handler(UP_API_HOST + '/users/@me/workouts/' + str(xid), access_token)

    @staticmethod
    def get_workout_graph(access_token, xid):
        return _url_handler(UP_API_HOST + '/users/@me/workouts/' + str(xid) + '/image', access_token)

    @staticmethod
    def get_workout_ticks(access_token, xid):
        return _url_handler(UP_API_HOST + '/users/@me/workouts/' + str(xid) + '/ticks', access_token)

    @staticmethod
    def get_trends(access_token, bucket_size=None, num_buckets=None, end_date=None):
        """

        :param access_token:
        :param bucket_size:
        :param num_buckets:
        :param end_date:
        :return:
        """
        url = UP_API_HOST + '/users/@me/trends' + '?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_moves_list(access_token, date=None, start_time=None, end_time=None, updated_after=None,
                       page_token=None):
        """

        :param access_token:
        :param date:
        :param start_time:
        :param end_time:
        :param updated_after:
        :param page_token:
        :return:
        """
        url = UP_API_HOST + '/users/@me/moves?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_move_info(access_token, move_xid):
        url = UP_API_HOST + '/users/@me/moves/' + move_xid
        return _url_handler(url, access_token)

    @staticmethod
    def get_move_graph(access_token, move_xid):
        url = UP_API_HOST + '/users/@me/moves/' + move_xid + "/image"
        return _url_handler(url, access_token)

    @staticmethod
    def get_move_ticks(access_token, move_xid):
        url = UP_API_HOST + '/users/@me/moves/' + move_xid + "/ticks"
        return _url_handler(url, access_token)

    @staticmethod
    def get_sleeps_list(access_token, date=None, start_time=None, end_time=None, updated_after=None,
                        page_token=None):
        """

        :param date:
        :param start_time
        :param end_time:
        :param updated_after:
        :param page_token=None
        :return:
        """
        url = UP_API_HOST + '/users/@me/sleeps?' + urllib.urlencode(_build_param_dict(locals()))
        return _url_handler(url, access_token)

    @staticmethod
    def get_generic_api_call(access_token, endpoint='/users/@me', **kwargs):
        """
        Generic method for any API call to Jawbone
        :param access_token: The access_token
        :param endpoint: Endpoint we want to go against eg '/users/@me/'
        :param kwargs: Any additional parameters
        :return: The response or error
        """
        url = UP_API_HOST + endpoint + '?' + urllib.urlencode(kwargs.items())
        return _url_handler(url, access_token)

    @staticmethod
    def revoke_access_token(access_token):
        """

        :param access_token:  The access token required
        :return:
        """

        return requests.delete(UP_API_HOST + '/users/@me/PartnerAppMembership',
                               headers=dict(Authorization="Bearer " + access_token))