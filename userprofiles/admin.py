from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from userprofiles.models import UserProfile
from mainsite.models import Domain, Billing

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

class UserDomainInline(admin.TabularInline):
    model = Domain
    # can_delete = False
    max_num = 1
    verbose_name_plural = 'user domains'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, UserDomainInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
