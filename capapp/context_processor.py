from .models import ShopCart, Category, Carousel


def cartread(request):
    cart = ShopCart.objects.filter(user__username=request.user.username, paid_order=False)


    cartreader = 0
    for item in cart:
        cartreader += item.quantity

    context = {
        'cartreader':cartreader
    }

    return context

def dropdown(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }
    
    return context    

def carousel(request):
    carousel = Carousel.objects.get(pk=1)
    carousel2 = Carousel.objects.get(pk=2)
    carousel3 = Carousel.objects.get(pk=3)

    context = {
        'carousel':carousel,
        'carousel2':carousel2,
        'carousel3':carousel3
    }
    return context