from django.contrib import admin
from drivers.models import Driver, Team

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):

    pass


admin.site.register(Driver, AuthorAdmin)
admin.site.register(Team, AuthorAdmin)
