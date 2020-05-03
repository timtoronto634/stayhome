import random
import string

from .models import Room, Player


def generate_room_name():
    room_name = "abc"
    while Room.objects.filter(room_name=room_name).exists():
        room_name = ''.join([random.choice(string.ascii_lowercase
                                           + string.digits) for n in range(3)])
    return room_name
# empty line needed
