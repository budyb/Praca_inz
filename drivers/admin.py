from django.contrib import admin
from drivers.models import *

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):

    pass


admin.site.register(Driver, AuthorAdmin)
admin.site.register(Team, AuthorAdmin)
admin.site.register(Schedule, AuthorAdmin)
