from django import template
from apps.products.models import WishList

register = template.Library()


@register.filter
def has_wishlist(user, product) -> bool:
    if user.is_anonymous:
        return False
    return WishList.objects.filter(user=user, product=product).exists()