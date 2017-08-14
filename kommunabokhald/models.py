from django.db import models
from django.contrib.auth.models import User

import datetime


# Create your models here.
def get_total_housemates():
    return Housemate.objects.count()


class Housemate(User):
    """
    a class extending the user model to be able to calculate debts
    will also use the same table as User model
    """
    class Meta:
        proxy = True

    def get_total_debt_due(self):
        """
        calculates the total a person has to pay (this is for all time since joining)
        :return: the total debt of a user rounded down to nearest int
        """
        rent = sum(r.get_payment_per_person() for r in Rent.objects.filter(created__gte=self.date_joined))
        self_payments = sum(p.amount for p in Payment.objects.filter(user=self))
        # all non rent payment
        other_payments = sum((p.amount / p.housemates_this_month) for p in
                             Payment.objects.filter(is_rent=False, payment_date__gte=self.date_joined))

        return int((rent + other_payments) - self_payments)


class Payment(models.Model):
    """
    Representation of a single payment made for any reason
    """
    amount = models.IntegerField()
    payment_date = models.DateField(default=datetime.date.today)
    reason = models.CharField(max_length=200, default='')
    user = models.ForeignKey(Housemate)
    is_rent = models.BooleanField(default=False)
    # auto filled used for calculations and book keeping
    housemates_this_month = models.IntegerField(default=get_total_housemates)


class Rent(models.Model):
    """
    representation of monthly expenses that will divide evenly between all housemates
    """
    house_rent = models.IntegerField()
    house_fund = models.IntegerField()
    electricity = models.IntegerField()
    internet = models.IntegerField()
    gagnaveitan = models.IntegerField()
    house_reparations = models.IntegerField()
    comments = models.CharField(max_length=200, default='')

    # auto filled used for calculations and book keeping
    housemates_this_month = models.IntegerField(default=get_total_housemates)
    created = models.DateField(default=datetime.date.today)

    def get_total_payment_due(self):
        """
        get the total calculated amount that is to be split between all housemates
        :return: the total amount to pay for a current month
        """
        return (self.house_rent + self.house_fund + self.electricity + self.internet + self.gagnaveitan  # expenses
                - self.house_reparations)  # deductibles

    def get_payment_per_person(self):
        """
        get the total amount each housemate has to pay
        :return:
        """
        return self.get_total_payment_due() // self.housemates_this_month
