import requests
import multiprocessing
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from ..models import Account, Transaction


def create_user():
    username = "user1"
    password = "bar"
    user = User.objects.create_user(
        username=username, password=password
    )
    Account.objects.create(user=user)
    return user, password


class WithDrawTests(LiveServerTestCase):
    def _withdraw_threaded(self, number):
        def withdraw(username, password):
            url = reverse("withdraw")
            url = "{}{}".format(self.live_server_url, url)
            s = requests.Session()
            auth_url = "{}/{}".format(self.live_server_url, "auth/login/")
            s.get(auth_url)
            csrftoken = s.cookies['csrftoken']
            s.post(
                auth_url,
                data={
                    "username": username,
                    "password": password,
                    "crsftoken": csrftoken
                },
                headers={'X-CSRFToken': csrftoken}
            )
            s.post(
                url,
                headers={'X-CSRFToken': s.cookies["csrftoken"]},
                cookies={
                    "crsftoken": s.cookies["csrftoken"],
                    "sessionid": s.cookies['sessionid']
                }
            )
        user, password = create_user()
        start_balance = Account.objects.get(user=user).current
        number = 15
        jobs = []
        for i in range(number):
            p = multiprocessing.Process(
                target=withdraw, args=(user.username, password)
            )

            jobs.append(p)
            p.start()
        for j in jobs:
            j.join()
        return user, start_balance

    def test_withdraw_threaded(self):
        number = 15
        user, start_balance = self._withdraw_threaded(number)
        assert Transaction.objects.count() == number
        assert Account.objects.get(user=user).current == start_balance - number

    @patch("accounts.views.LockedAtomicTransaction.__enter__")
    def test_withdraw_unthreaded(self, mock_lock):
        def func():
            return
        mock_lock.side_effect = func
        number = 15
        user, start_balance = self._withdraw_threaded(number)
        assert Transaction.objects.count() == number
        assert Account.objects.get(user=user).current != start_balance - number
