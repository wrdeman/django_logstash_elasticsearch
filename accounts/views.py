import logging
from django.http import HttpResponse
from django.views import View

from demo.utils import LockedAtomicTransaction
from .models import Account, Transaction
logger = logging.getLogger("django")


class WithdrawView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            holder = Account.objects.filter(user=request.user).first()
            current = holder.current
            return HttpResponse(current)
        return HttpResponse("")

    def post(self, request, *args, **kwargs):
        with LockedAtomicTransaction(Account):
            holder = Account.objects.filter(user=request.user).first()
            withdrawl = 1
            current = holder.make_withdrawl(withdrawl)
            Transaction.objects.create(
                holder=holder,
                balance=current,
                transaction=withdrawl
            )

        return HttpResponse(current)
