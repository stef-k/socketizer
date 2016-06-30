"""Create a custom storage class for S3 Boto in order to split
STATIC and MEDIA files in different directories
"""
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key, self.secret_key,
                calling_format=self.calling_format,
                host='s3.eu-central-1.amazonaws.com')
        return self._connection


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                self.access_key, self.secret_key,
                calling_format=self.calling_format,
                host='s3.eu-central-1.amazonaws.com')
        return self._connection
