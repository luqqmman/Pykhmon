from django.db import models
from django.core.validators import MinValueValidator


class Session(models.Model):
    session_name = models.CharField(max_length=64, unique=True)
    mikrotik_IP = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    hotspot_server_name = models.CharField(max_length=64)
    DNS_name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.session_name}: ({self.mikrotik_IP})" 


class Profile(models.Model):
    RATE_UNIT_CHOICES = [
        ('K', 'Kbps'),
        ('M', 'Mbps'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session')
    profile_name = models.CharField(max_length=64, unique=True, help_text="Nama unik untuk profil rate limit")
    download_limit_value = models.IntegerField(validators=[MinValueValidator(1)], help_text="Nilai batas kecepatan download (misalnya, 1024 untuk 1 Mbps)")
    download_limit_unit = models.CharField(max_length=1, choices=RATE_UNIT_CHOICES, help_text="Unit batas kecepatan download (Kbps, Mbps, Gbps)")
    upload_limit_value = models.IntegerField(validators=[MinValueValidator(1)], help_text="Nilai batas kecepatan upload (misalnya, 512 untuk 512 Kbps)")
    upload_limit_unit = models.CharField(max_length=1, choices=RATE_UNIT_CHOICES, help_text="Unit batas kecepatan upload (Kbps, Mbps, Gbps)")
    shared_users = models.IntegerField(validators=[MinValueValidator(1)], default=1, help_text="Jumlah maksimum pengguna yang dapat berbagi profil ini")
    description = models.TextField(blank=True, null=True, help_text="Deskripsi opsional untuk profil ini")

    def download_limit(self):
        return f"{self.download_limit_value}{self.download_limit_unit}"

    def upload_limit(self):
        return f"{self.upload_limit_value}{self.upload_limit_unit}"

    def rate_limit(self):
        return f"{self.download_limit()}/{self.upload_limit()}"

    def __str__(self):
        return self.profile_name
    

class Voucher(models.Model):
    UPTIME_UNIT_CHOICES = [
        ("s", "second"),
        ("m", "minute"),
        ("h", "hour"),
        ("d", "day"),
    ]
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='voucher_session')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    uptime_value = models.IntegerField(validators=[MinValueValidator(1)])
    uptime_unit = models.CharField(max_length=1, choices=UPTIME_UNIT_CHOICES)

    def __str__(self):
        return self.username
    
    def uptime_limit(self):
        return f"{self.uptime_value}{self.uptime_unit}"
