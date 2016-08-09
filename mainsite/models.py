import hashlib
import random
from urllib import parse
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your models here.
class Settings(models.Model):
    """Runtime application settings"""

    service_is_active = \
        models.BooleanField(default=True,
                            help_text='Enables - disables the websocket '
                                      'service')

    service_key = \
        models.CharField(max_length=512,
                         default='',
                         help_text='A secret key to talk to websockets '
                                   'service')
    # max connections
    max_connection = models.IntegerField(default=5000,
                                         help_text='Server limits')
    # do we give free keys?
    free_keys = models.BooleanField(default=False)
    in_beta = models.BooleanField(default=True)
    # if yes we set some limits
    max_concurrent_connections = \
        models.IntegerField(default=100, help_text='Domain limits')

    class Meta:
        verbose_name_plural = 'settings'

    def generate_key(self):
        """Generates a new service key for communication between services"""
        self.service_key = hashlib.sha256(str(
            random.getrandbits(256)).encode('utf-8')).hexdigest()

    def save(self, *args, **kwargs):
        self.generate_key()
        super(Settings, self).save(*args, **kwargs)


class Stats(models.Model):
    """Holds simple stats about the application, such as, total clients served
    maximum concurrent clients ever served.
    """

    total_clients = models.BigIntegerField(default=0)
    max_concurrent_clients = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'stats'


class Domain(models.Model):
    """Domain a user may have many domains, for each domain there must be a
    purhased plan in order to be usable
    """

    # Foreign key to User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    domain = models.CharField(max_length=512, default='', unique=True)
    api_key = models.CharField(max_length=512, default='')
    # Domain limits, based on purchased plan
    # days of active subscription, each day reduced by 1
    days_left = models.IntegerField(default=0)
    max_concurrent_connections = models.IntegerField(default=0)
    # Domain status - current usage
    # api calls per month, at the beginning of the month this goes to 0
    current_month_api_calls = models.IntegerField(default=0)

    def generate_key(self):
        """Generates a new API key"""
        self.api_key = hashlib.sha256(str(
            random.getrandbits(128)).encode('utf-8')).hexdigest()

    def get_absolute_url(self):
        return reverse('domain-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        self.domain = parse.urlparse(self.domain)
        if self.domain[1] != '':
            self.domain = self.domain[1]
        else:
            self.domain = self.domain[2]
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
