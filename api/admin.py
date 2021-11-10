
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Titles, Reviews, Categories, Genres

admin.site.register(User, UserAdmin)
admin.site.register(Titles)
admin.site.register(Reviews)
admin.site.register(Categories)
admin.site.register(Genres)
