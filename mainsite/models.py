import hashlib
import random
from urllib import parse
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your models here.
class Settings(models.Model):
    """Runtime application settings"""

    # do we give free keys?
    free_keys = models.BooleanField(default=False)
    in_beta = models.BooleanField(default=True)


class Domain(models.Model):
    """Domain a user may have many domains, for each domain there must be a
    purhased plan in order to be usable
    """

    # Foreign key to User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    domain = models.CharField(max_length=512, default='')
    api_key = models.CharField(max_length=512, default='')
    # if true the user can use the service for free
    free_key = models.BooleanField(default=False)
    # Domain limits, based on purchased plan
    # days of active subscription, each day reduced by 1
    days_left = models.IntegerField(default=0)
    max_concurrent_connections = models.IntegerField(default=0)
    # Domain status - current usage
    # api calls per month, at the beginning of the month this goes to 0
    current_month_api_calls = models.IntegerField(default=0)
    # current connected sockets
    current_connections = models.IntegerField(default=0)
    # Domain status last update
    user_limits_last_update = models.DateTimeField(null=True)

    def generate_key(self):
        """Generates a new API key"""
        self.api_key = hashlib.sha256(str(
            random.getrandbits(128)).encode('utf-8')).hexdigest()

    def get_absolute_url(self):
        return reverse('domain-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # url = parse.urlparse(self.domain)
        self.domain = parse.urlparse(self.domain)[1]
        print(self.domain)
        super(Domain, self).save(*args, **kwargs)


class Billing(models.Model):
    """Billing history for each user

    The stored values will be also used to generate receipts
    the Order ID will be the User ID + the purchase_date as Unix timestamp
    """

    # keep billing history even if user deletes his account
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    purchase_date = models.DateTimeField(auto_now_add=True)
    domain_name = models.CharField(max_length=512, null=True)
    # product price without taxes - vat
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # the total of taxes (will be added to price)
    tax = models.DecimalField(max_digits=8, decimal_places=2)
    # product details
    days = models.IntegerField(default=0)
    max_concurrent_users = models.IntegerField(default=0)
