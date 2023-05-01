from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CLIENT = 'client', 'Client'
        VIP_CLIENT = 'vip_client', 'VIP Client'

    used_token = models.BooleanField(default=False, null=True)
    type = models.CharField(
        max_length=11,
        choices=UserType.choices,
        default=UserType.CLIENT
    )

    @property
    def cart_count(self):
        return self.shoppingcard_set.count()

    @property
    def get_total_price(self):
        return sum(
            cart.product.discount_price
            for cart in self.shoppingcard_set.all()
        )

    class Meta:
        verbose_name = 'User'
        db_table = 'users'