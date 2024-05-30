from django.db import models

class Session(models.Model):
    session_name = models.CharField(max_length=64)
    mikrotik_IP = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    hotspot_server_name = models.CharField(max_length=64)
    DNS_name = models.CharField(max_length=64)


class Profile(models.Model):
    name = models.CharField(max_length=64)
    uptime = models.CharField(max_length=8)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Voucher(models.Model):
    #qr = models.ImageField()
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
