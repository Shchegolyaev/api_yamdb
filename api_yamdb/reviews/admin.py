from django.contrib import admin

from .models import Title, Review, Comments

admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comments)
