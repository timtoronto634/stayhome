from django.contrib import admin

from .models import Room, Player, Topic

admin.site.register(Room)
admin.site.register(Player)
admin.site.register(Topic)
# empty line needed
