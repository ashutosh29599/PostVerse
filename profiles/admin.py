from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
        If the admin interface doesn't need to be changed, then the following is enough.
        admin.site.register(Profile)
    """
    list_display = ['user', 'first_name', 'last_name', 'bio']
