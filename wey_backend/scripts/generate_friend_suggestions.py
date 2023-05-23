import django
import os
import sys

from collections import Counter
from datetime import timedelta

from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wey_backend.settings')
django.setup()

from account.models import User


def check_friends(curr_user, friend):
    for friend_sugg in friend.friends.all():
        if (
            friend_sugg not in curr_user.friends.all()
            and friend_sugg not in curr_user.people_you_may_know.all()
            and friend_sugg != curr_user
        ):
            curr_user.people_you_may_know.add(friend_sugg)
            print('    %s may know %s' % (curr_user, friend_sugg))
    return friend


users = User.objects.all()

for user in users:
    # Clear the suggestion list
    user.people_you_may_know.clear()

    print('Find friends for:', user)
    for friend in user.friends.all():
        print('  Checking friends at', check_friends(user, friend))
