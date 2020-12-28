from django.db import models

class Account(models.Model):
    username = models.TextField()
    password = models.TextField()

class Secret(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    secret = models.TextField()

class Session(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
