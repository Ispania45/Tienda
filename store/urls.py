from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from store.controller import cart, wishlist, checkout, order
from django.contrib.auth import views as authviews

urlpatterns = [

    path('', views.home, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('productos/', views.productos, name='productos'),
    path('collections/<str:slug>', views.collectionsview, name='collectionsview'),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name='productview'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logoutpage, name='logout'),
    path('add-to-cart', cart.addtocart, name='addtocart' ),
    path('cart', cart.viewcart, name='cart'),
    path("update-cart", cart.updatecart, name="updatecart"),
    path('delete-cart-item', cart.deletecartitem, name='deletecartitem'),
    path('wishlist', wishlist.index, name='wishlist'),
    path('add-to-wishlist', wishlist.addtowishlist, name='addtowishlist'),
    path('delete-wishlist-item', wishlist.deletewishlistitem, name='deletewishlistitem'),
    path('checkout', checkout.index, name='checkout'),
    path('place-order', checkout.placeorder, name='placeorder'),
    path('searchproduct', views.searchproduct, name="searchproduct"),

    path('my-orders', order.index, name="myorders"),
    path('view-order/<str:t_no>', order.vieworder, name="orderview"),
    path('product-list', views.productlistAjax),
    path('proceed-to-pay', checkout.razorpaycheck),
    path('my-orders', checkout.orders),
    path('password_reset/',authviews.PasswordResetView.as_view(template_name="store/reset/password_reset.html"),name="password_reset"),
    path('password_reset/done',authviews.PasswordResetDoneView.as_view(template_name="store/reset/password_reset_done.html"),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',authviews.PasswordResetConfirmView.as_view(template_name="store/reset/password_reset_confirm.html"),name="password_reset_confirm"),
    path('password_reset_complete/',authviews.PasswordResetCompleteView.as_view(template_name="store/reset/password_reset_complete.html"),name="password_reset_complete"),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
