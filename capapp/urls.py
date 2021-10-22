from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name= 'index'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:id>/' , views.single_category, name='category'), 
    path('products/', views.products, name='products'),
    path('details/<str:id>/', views.single_product, name='details'),
    path('logout/', views.logoutt, name='logoutt'),
    path('login/', views.loginform, name='loginform'),
    path('signup/', views.signupform, name='signupform'),
    path('password/', views.password, name='password'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('completed/', views.completed, name='completed'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('deleteitem/', views.deleteitem, name='deleteitem'),
    path('increase/', views.increase, name='increase'),
]

