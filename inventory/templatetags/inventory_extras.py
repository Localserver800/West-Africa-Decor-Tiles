from django import template
from django.db.models import Avg

register = template.Library()

@register.filter(name='avg_rating')
def avg_rating(reviews):
    if reviews:
        return round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0)
    return 0
