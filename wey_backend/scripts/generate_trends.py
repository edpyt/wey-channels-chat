import django
import os
import sys
from django.core.exceptions import ObjectDoesNotExist

from collections import Counter
from datetime import timedelta
from django.utils import timezone


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wey_backend.settings')
django.setup()

from post.models import Post, Trend


for trend in Trend.objects.all():
    trend.delete()


def extract_hashtags(text, trends):
    trends.extend([x for word in text.split()
                   if word[0] == '#'
                   and '#' not in (x := word[1:])])
    return trends


trends = []

this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
twenty_four_hours = this_hour - timedelta(hours=24)


for post in Post.objects.filter(created_at__gte=twenty_four_hours):
    extract_hashtags(post.body, trends)

trends_count = Counter(trends).most_common(10)

for trend, count in trends_count:
    print(trend, ' ' * (15 - len(trend)), count)
    Trend.objects.create(hashtag=trend,
                         occurrences=count)

print(Trend.objects.all())
