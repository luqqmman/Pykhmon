from routeros_api import HotspotApi
from nanoid import generate

from wifiqr import generate_qr

hotspot = HotspotApi('10.10.10.1', 'admin', 'supersecure', 'hotspot-bangkit')

name = 'valarqvin'
password = generate(size=10)
uptime = '1h'

if hotspot.add_user(name, password, uptime):
    print('success')
    generate_qr('10.10.10.2', name, password)
else:
    print('fail')


