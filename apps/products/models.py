from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'category'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey('Product', models.CASCADE, 'images')
    image = models.ImageField()

    class Meta:
        verbose_name = 'ProductImage'
        verbose_name_plural = 'ProductImages'
        db_table = 'product_image'

    def __str__(self):
        return self.product_id


class Review(models.Model):
    user = models.ForeignKey('users.Users', models.CASCADE)
    body = models.TextField()
    product = models.ForeignKey('Product', models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    # rate = models.DecimalField()

    class Meta:
        verbose_name = 'Review'
        db_table = 'review'

    def __str__(self):
        return self.user_id


class ProductManager(models.Manager):
    def filter_or_all(self):
        return ProductQuerySet(self.model, using=self._db)


class ProductQuerySet(models.QuerySet):
    def filter_or_all(self, **params):
        if '*' in params:
            return self.all()
        return self.filter(**params)


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    short_description = models.TextField()
    owner = models.ForeignKey('users.Users', models.CASCADE)
    description = models.TextField(blank=True, null=True)
    discount = models.IntegerField(blank=True, default=0)
    quantity = models.IntegerField()
    shipping_cost = models.IntegerField()
    is_premium = models.BooleanField(default=False)
    specification = models.JSONField(default=dict, blank=True)
    category = models.ForeignKey('products.Category', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProductQuerySet.as_manager()

    @property
    def discount_price(self):
        return self.price - round(self.price / 100 * self.discount)

    @property
    def image_count(self):
        return self.productimage_set.count()

    class Meta:
        indexes = [models.Index(fields=['id'])]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'product'

    def __str__(self):
        return self.name


class ShoppingCard(models.Model):
    user = models.ForeignKey('users.Users', models.CASCADE)
    product = models.ForeignKey('Product', models.CASCADE)

    def __str__(self):
        return f"{self.user} -> {self.product}"


class WishList(models.Model):
    user = models.ForeignKey('users.Users', models.CASCADE)
    product = models.ForeignKey('Product', models.CASCADE)

    def __str__(self):
        return f"{self.user} -> {self.product}"


class ProductProxy(Product):
    class Meta:
        proxy = True
