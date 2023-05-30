from django.http import JsonResponse
from django.shortcuts import render, redirect


from django.contrib import messages
from .models import *
from django import views
# Create your views here.

def home(request):
    category = Category.objects.filter(status=0)
    trending_products = Product.objects.filter(trending=1)
    context = {'category': category , 'trending_products': trending_products }
    return render(request, 'store/index.html', context)


def nosotros(request):
    return render(request, 'store/nosotros.html')

def productos(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, 'store/productos.html', context)

def collectionsview(request, slug):
    if(Category.objects.filter(slug=slug, status=0)):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        context = {'products': products, 'category':category}
        return render(request, "store/products/index.html", context)
    else:
        messages.warning(request, "No se encuentra la categoria")
        return redirect('collections')
    
def productview(request, cate_slug, prod_slug):
        if(Category.objects.filter(slug=cate_slug, status=0)):
            if(Product.objects.filter(slug=prod_slug, status=0)):
                products = Product.objects.filter(slug=prod_slug, status=0).first
                context = {'products':products}
            
            else:
                messages.error(request, "No se encuentra producto")
                return redirect('collections')
            
        else:
            messages.error(request, "No se encuentra categoria")
            return redirect('collections')
        return render(request, 'store/products/view.html', context)


def productlistAjax(request):
    products= Product.objects.filter(status=0).values_list('name', flat=True)
    productsList = list(products)

    return JsonResponse(productsList, safe=False)

def searchproduct(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('productsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__contains=searchedterm).first()

            if product:
                return redirect('collections/' +product.category.slug+'/'+product.slug)
            else:
                messages.info(request, "El producto no se encuentra")
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

from django.shortcuts import render, redirect
from django.contrib import messages
from store.forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro Exitoso! Proceda al acceso ')
            return redirect('/login')
    context = {'form': form}
    return render (request, "store/auth/register.html", context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Ya has iniciado sesion')
        return redirect('/')
    
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')

            user = authenticate(request, username=name, password=passwd)

            if user is not None:
                login(request, user)
                messages.success(request, "Has iniciado sesion")
                return redirect('/')
            else:
                messages.error(request, 'Usuario y Contraseña incorrectos')
                return redirect('/login')
        return render(request, 'store/auth/login.html')
    
def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Has cerrado sesion")
        return redirect('/')