from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from store.models import Wishlist, Product

@login_required(login_url='loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': wishlist}
    return render(request, 'store/wishlist.html', context)

def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status': "El producto ya esta en la lista"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "El producto fue a agregado a la lista"})
            else:
                return JsonResponse({'status': "No se encuentra el producto "})
        else:
            return JsonResponse({'status': "Iniciar sesion para continuar"})
    return redirect('/')


def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))

            if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Wishlist.objects.get(product_id=prod_id)
                wishlistitem.delete()
                return JsonResponse({'status': "El producto fue borrado de la lista"})
            else:
                return JsonResponse({'status': "El producto no fue encontrado en la lista"})
        else:
            return JsonResponse({'status': "Iniciar sesion para continuar"})
    
    return redirect('/')



