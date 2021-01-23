from django.contrib import admin
from drivers.models import *

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):

    pass


admin.site.register(Driver, AuthorAdmin)
admin.site.register(Team, AuthorAdmin)
admin.site.register(Schedule, AuthorAdmin)
admin.site.register(Ranking, AuthorAdmin)
admin.site.register(Prediction, AuthorAdmin)
admin.site.register(Season, AuthorAdmin)
admin.site.register(Result, AuthorAdmin)
admin.site.register(HistoricResult, AuthorAdmin)
