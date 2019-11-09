from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from shopping.forms import writereview
from .models import Category, Product, Review


@login_required
def list_categories(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'shopping/index.html', {'categories': categories, 'products': products})


def itemsview(request, pk):
    categories = Category.objects.all()
    cat = Category.objects.get(id=pk)
    current_order_products = []
    # if request.user.is_authenticated:
    #     filtered_orders = Order.objects.filter(owner=request.user.cus, is_ordered=False)
    #     if filtered_orders.exists():
    #         user_order = filtered_orders[0]
    #         user_order_items = user_order.items.all()
    #         current_order_products = [product.product for product in user_order_items]

    context = {
        'categories': categories,
        'cat': cat,
        'current_order_products': current_order_products
    }

    return render(request, "shopping/items.html", context)


def itemdetailview(request, pk, ck):
    categories = Category.objects.all()
    cat = Category.objects.get(id=pk)
    prod = Product.objects.get(id=ck)
    products = Product.objects.filter(category=cat)
    current_order_products = []

    if request.method == 'POST':
        form = writereview(request.POST)
        if form.is_valid():
            content = request.POST.get('content')
            rating = request.POST.get('rating')
            review1 = Review.objects.create(category=cat, product=prod, customer=request.user, content=content,
                                            rating=rating)
            review1.save()
            return redirect(reverse('shopping:specificitem', args=(pk, ck,)))
    else:
        form = writereview()
    return render(request, 'shopping/itemdetail.html', {'form': form,
                                                        'categories': categories,
                                                        'cat': cat,
                                                        'prod': prod,
                                                        'current_order_products': current_order_products, })

def reviewtext(request, categ, product):
    prod = get_object_or_404(Product, pk=product)
    cat = get_object_or_404(Category, pk=categ)
    if request.method == 'POST':
        form = writereview(request.POST)
        if form.is_valid():
            content = request.POST.get('content')
            rating = request.POST.get('rating')
            review1 = Review.objects.create(category=cat, product=prod, customer=request.user, content=content,
                                            rating=rating)
            review1.save()
            return redirect(reverse('shopping:specificitem', args=(product, categ,)))
    else:
        form = writereview()
    return render(request, 'shopping/writereview.html', {'form': form})
