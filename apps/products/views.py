from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, View, DeleteView
from faker import Faker

from apps.products.forms import ProductForm
from apps.products.models import Category, Product, ProductImage, ShoppingCard, \
    WishList
from apps.products.permissions import permissions_required, \
    PermissionsRequiredMixin


def homepage(request):
    return render(request, 'products/homepage.html')


class BlogView(ListView):
    template_name = 'products/product-list.html'
    context_object_name = 'products'

    def paginate_queryset(self, queryset, page_size):
        return super().paginate_queryset(queryset, page_size)

    def get_queryset(self):
        self.queryset = Product.objects.all()
        name = self.request.GET.get('category', '*')
        self.queryset = self.queryset.filter_or_all(category__name=name)
        self.queryset = self.queryset.filter_or_all(
            name__icontains=self.request.GET.get('search', '*')
        )

        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        return context


def products_list(request):
    page = int(request.GET.get('page', 1))
    if request.user.is_authenticated and request.user.type == 'vip_client':
        products = Product.objects
    else:
        products = Product.objects.filter(
            is_premium=False
        )
    paginator = Paginator(products.select_related('category').order_by('id'), per_page=7)

    redirect_url = reverse_lazy(
        'products:products_list'
    ) + '?page='

    if paginator.num_pages < page:
        return redirect(redirect_url + str(paginator.num_pages))
    if page <= 0:
        return redirect(redirect_url + '1')
    pages = paginator.get_page(page)
    context = {
        'products': pages,
    }
    return render(request, 'products/product-list.html', context)


@permissions_required(('admin',))
def add_product(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    if request.method == 'POST':
        data = request.POST.copy()
        filtered_data = sorted(
            filter(
                lambda x: x.startswith('key') or x.startswith('value'),
                data
            ), key=lambda x: int(x[-1])
        )
        specification = {
            request.POST[filtered_data[i]]: request.POST[filtered_data[i + 1]]
            for i in range(0, len(filtered_data) - 1, 2)
        }
        form = ProductForm(request.POST)
        if form.is_valid():
            Product.objects.filter()
            product = Product(
                name=request.POST.get('name'),
                price=request.POST.get('price'),
                short_description=request.POST.get('short_description'),
                description=request.POST.get('description'),
                discount=request.POST.get('discount'),
                quantity=request.POST.get('quantity'),
                shipping_cost=request.POST.get('shipping_cost'),
                specification=specification,
                category=get_object_or_404(
                    Category,
                    id=int(request.POST.get('category', 0)),
                    owner=request.user.pk
                )
            )
            product.save()
            lst_of_images = []
            for image in request.FILES.getlist('images'):
                lst_of_images.append(ProductImage(
                    product=product,
                    image=image
                ))

            ProductImage.objects.bulk_create(
                lst_of_images
            )

    return render(request, 'products/add_product.html', context)


def generate_fake_data(request):
    fake = Faker()
    lst_of_products = []
    for _ in range(200):
        discount = fake.random.randint(1, 9) * 10
        lst_of_products.append(Product(
            name=fake.name(),
            price=fake.random.randint(2000, 180000),
            short_description=fake.sentence(10),
            description=fake.sentence(100),
            discount=discount,
            quantity=fake.random.randint(1, 10),
            shipping_cost=fake.random.randint(10, 80),
            category_id=fake.random.randint(1, 2),
            owner_id=1
        ))
    Product.objects.bulk_create(lst_of_products)
    return redirect(reverse('products:homepage'))


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'product': product
    }
    return render(request, 'products/product-details.html', context)


@permissions_required(('client', 'vip_client'))
def shopping_cart(request):
    products = ShoppingCard.objects.filter(user_id=request.user.id).all()
    context = {
        'products': products,
        'total_price': request.user.get_total_price
    }
    return render(request, 'products/shopping-cart.html', context)


@permissions_required(('client', 'vip_client'))
def add_to_shopping_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    ShoppingCard(user=request.user, product=product).save()
    return redirect(
        reverse('products:products_list')
    )


@permissions_required(('client', 'vip_client'))
def delete_shopping_cart_item(request, pk):
    product = ShoppingCard.objects.filter(product_id=pk).first()
    product.delete()
    return redirect(reverse('products:shopping_cart'))


@permissions_required(('client', 'vip_client'))
def buy_shopping_cart_items(request):
    ShoppingCard.objects.filter(user=request.user).delete()
    return redirect(reverse('products:products_list'))


# class based views

class MyProductsView(PermissionsRequiredMixin, ListView):
    permission_required = ('admin',)
    paginate_by = 7
    template_name = 'products/product-list.html'

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['products'] = context.pop('page_obj')
        return context


class EditMyProductView(PermissionsRequiredMixin, UpdateView):
    permission_required = ('admin',)
    form_class = ProductForm
    template_name = 'products/edit_product.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['specification'] = zip(
            range(len(context['product'].specification)),
            context['product'].specification.items()
        )
        return context

    def get_success_url(self):
        return reverse('products:my_products')

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        filtered_data = sorted(
            filter(
                lambda x: x.startswith('key') or x.startswith('value'),
                data
            ), key=lambda x: int(x[-1])
        )
        specification = {
            request.POST[filtered_data[i]]: request.POST[filtered_data[i + 1]]
            for i in range(0, len(filtered_data) - 1, 2)
        }
        form = ProductForm(request.POST | {'owner': request.user})
        if form.is_valid():
            product = Product.objects.filter(
                pk=self.kwargs['pk']
            ).update(
                **form.data, **specification
            )
            lst_of_images = []
            for image in request.FILES.getlist('images'):
                lst_of_images.append(ProductImage(
                    product=product,
                    image=image
                ))

            ProductImage.objects.bulk_create(
                lst_of_images
            )
        return redirect(self.get_success_url())


class DeleteMyProductView(PermissionsRequiredMixin, DeleteView):
    permission_required = ('admin',)
    model = Product
    success_url = reverse_lazy('products:my_products')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not obj.owner == self.request.user:
            raise Http404('You are not allowed to delete this product')

        return obj

    def get(self, request, *args, **kwargs):
        return self.delete(self, *args, **kwargs)


class AddFavorite(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        wish, created = WishList.objects.get_or_create(
            product=product, user=self.request.user
        )
        if not created:
            wish.delete()

        return redirect(reverse('products:products_list'))
