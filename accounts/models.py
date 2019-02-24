from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    minimum = models.IntegerField(default=0)
    current = models.IntegerField(default=1000000)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.current < self.minimum:
            raise Exception("Current cannot be smaller that min")

        super().save(*args, **kwargs)

    def make_withdrawl(self, value):
        if self.current >= self.minimum:
            self.current -= value
            self.save()
        return self.current

    def __str__(self):
        return "{}: {}  ({})".format(
            self.user, self.current, self.minimum
        )


class Transaction(models.Model):
    holder = models.ForeignKey(Account, models.SET_NULL, null=True, blank=True)
    transaction = models.IntegerField()
    balance = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.holder, self.transaction)
