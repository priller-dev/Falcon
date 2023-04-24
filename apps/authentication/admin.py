from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

Users = get_user_model()


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    exclude = ('',)


admin.site.unregister(Group)
