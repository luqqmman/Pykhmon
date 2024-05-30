import requests
import qrcode
from nanoid import generate

# URL API MikroTik dan informasi autentikasi
class Api:
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password

    def resource(self):
        # Mendapatkan daftar interface pada MikroTik
        url = f'http://{self.address}/rest/system/resource'
        response = requests.get(url, auth=(self.username, self.password))

        # Memeriksa status respons
        if response.status_code == 200:
            return response.json()
        else:
            print('Gagal memuat data:', response.status_code)
            return False


class HotspotApi(Api):
    def __init__(self, address, username, password, servername):
        super().__init__(address, username, password)
        self.servername = servername

    def add_user(self, hot_username, hot_password, hot_uptime, hot_profile="default"):
        url = f'http://{self.address}/rest/ip/hotspot/user/add'
        payload = {
            'server': self.servername,  # Nama hotspot server
            'profile': hot_profile,   # Profil pengguna (misalnya, default)
            'name': hot_username,     # Nama pengguna baru
            'password':  hot_password, # Kata sandi pengguna baru
            'limit-uptime': hot_uptime    # Batas waktu (misalnya, 1 jam)
        }
        response = requests.post(url, auth=(self.username, self.password), json=payload)
        print(response.content)
        return response.status_code == 200
    
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

"""
    def test_voucher(self, hot_server, hot_ssid, hot_security, hot_user, hot_uptime):
        url = f'{self.address}/ip/hotspot/user/add'
        hot_password = generate(size=10)

        payload = {
            'server': hot_server,  # Nama hotspot server
            'profile': 'default',   # Profil pengguna (misalnya, default)
            'name': hot_user,     # Nama pengguna baru
            'limit-uptime': hot_uptime,    # Batas waktu (misalnya, 1 jam)
            'password':  hot_password # Kata sandi pengguna baru
        }

        response = requests.post(url, auth=(hot_user, hot_password), data=payload)

        if response.status_code == 200:
            print('Pengguna berhasil ditambahkan')
            generate_qr(hot_ssid, hot_password, hot_security)
        else:
            print('Gagal menambahkan pengguna:', response.content)
"""
