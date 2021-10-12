from django.contrib import admin

from .models import Comments, Review, Title

admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comments)
