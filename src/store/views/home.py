from django.shortcuts import render , redirect , HttpResponseRedirect
from django.urls import reverse
from store.models.product import Products
from store.models.category import Category
from django.views import View


# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        p = Products.objects.filter(id=product)

        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            if quantity := cart.get(product):
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                    p.update(in_stock=p.first().in_stock+1)
                else:
                    cart[product]  = quantity+1
                    p.update(in_stock=p.first().in_stock-1)

            else:
                p.update(in_stock=p.first().in_stock-1)
                cart[product] = 1
        else:
            p.update(in_stock=p.first().in_stock-1)
            cart = {product: 1}
        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        url = reverse('product_page', kwargs={'id': int(product)})
        return redirect(url)

    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    if categoryID := request.GET.get('category'):
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products();

    data = {'products': products, 'categories': categories}
    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)


def product_page(request, id):
    context = {'product': Products.objects.get(id=id)}
    return render(request, 'product.html', context)