from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from app.forms import ProductForm, ProductModelForm
from app.models import Product
# from authentication.forms import LoginForm, RegisterForm, EmailForm

# Create your views here.


# def index(request):
#     page = request.GET.get('page', '')
#     products = Product.objects.all().order_by('-id')
#     paginator = Paginator(products, 2)
#     try:
#         page_obj = paginator.page(page)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#
#     context = {
#         'page_obj': page_obj
#     }
#     return render(request, 'app/index.html', context)

class ProductListView(View):
    def get(self, request):
        page = request.GET.get('page', '')
        products = Product.objects.all().order_by('-id')
        paginator = Paginator(products, 2)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context={
            'page_obj': page_obj
        }
        return render(request,'app/index.html', context)

# def product_detail(request, product_id):
#     product = Product.objects.get(id=product_id)
#     attributes = product.get_attributes()
#
#     context = {
#         'product': product,
#         'attributes': attributes
#     }
#     return render(request, 'app/product-detail.html', context)


# def add_product(request):
#     form = ProductForm()
#     # form = None
#     if request.method == 'POST':
#
#         name = request.POST['name']
#         description = request.POST['description']
#         price = request.POST['price']
#         rating = request.POST['rating']
#         discount = request.POST['discount']
#         quantity = request.POST['quantity']
#         form = ProductForm(request.POST)
#         product = Product(name=name, description=description, price=price, discount=discount, quantity=quantity,
#                           rating=rating)
#
#         if form.is_valid():
#             product.save()
#             return redirect('index')
#
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'app/add-product.html', context)


# def add_product(request):
#     form = ProductModelForm()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     context = {
#         'form': form,
#     }
#     return render(request, 'app/add-product.html', context)

class AddProductView(View):
    def get(self, request):
        form = ProductModelForm()
        return render(request, 'app/add-product.html', {'form': form})

    def post(self, request):
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


class EditProductView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        form = ProductModelForm(instance=product)
        return render(request, 'app/update-product.html', {'form': form})

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        form = ProductModelForm(instance=product, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk)


class ProductDeleteView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if product:
            product.delete()
            return redirect('index')


class ProductDetailTemplateView(TemplateView):
    template_name = 'app/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=kwargs['product_id'])
        context['product'] = product
        context['attributes'] = product.get_attributes()
        return context

class EditProductTemplateView(TemplateView):
    template_name = 'app/update-product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=kwargs['pk'])
        context['form'] = ProductModelForm(instance=product)
        return context

    def post(self, request,  *args, **kwargs):
        context = self.get_context_data(**kwargs)

        product = get_object_or_404(Product, id=kwargs['pk'])
        form = ProductModelForm(instance=product, data=request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('index')


