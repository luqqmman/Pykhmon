import requests
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MikroTikApi:
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password

    def _request(self, method, endpoint, data=None):
        url = f'http://{self.address}/rest{endpoint}'
        try:
            if method == 'GET':
                response = requests.get(url, auth=(self.username, self.password), timeout=1)
            elif method == 'POST':
                response = requests.post(url, auth=(self.username, self.password), json=data, timeout=1)
            else:
                raise ValueError(f"Method {method} not supported")

            response.raise_for_status()
            return response.json() if response.content else True
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None

    def resource(self):
        return self._request('GET', '/system/resource')


class HotspotApi(MikroTikApi):
    def __init__(self, address, username, password, servername):
        super().__init__(address, username, password)
        self.servername = servername

    def add_user(self, hot_username, hot_password, hot_uptime, hot_profile="default"):
        payload = {
            'server': self.servername,
            'profile': hot_profile,
            'name': hot_username,
            'password': hot_password,
            'limit-uptime': hot_uptime
        }
        return self._request('POST', '/ip/hotspot/user/add', data=payload)

    def add_profile(self, profile_name, shared_users=1, rate_limit="1M/1M"):
        payload = {
            'name': profile_name,
            'shared-users': shared_users,
            'rate-limit': rate_limit
        }
        return self._request('POST', '/ip/hotspot/user/profile/add', data=payload)

    def get_users(self):
        return self._request('GET', '/ip/hotspot/user')

    def get_active_users(self):
        return self._request('GET', '/ip/hotspot/active')

    def to_dict(self):
        return {
            'address': self.address,
            'username': self.username,
            'password': self.password,
            'servername': self.servername,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(address=data['address'], username=data['username'], password=data['password'], servername=data['servername'])