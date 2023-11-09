from django.contrib import admin
from apps.users.models import User, AuthGroup, UsersUserGroups

# Register your models here.
admin.site.register(User)
admin.site.register(AuthGroup)
admin.site.register(UsersUserGroups)
