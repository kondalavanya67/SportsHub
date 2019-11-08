from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from cart.models import OrderItem, Order, Transaction
from shopping.models import Product
from user_auth.models import Profile
from cart.extra import generate_order_id
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def get_user_pending_order(request):
    u = User.objects.get(pk=request.user.pk)
    user_profile = Profile.objects.get(user_name=u)
    ord = Order.objects.filter(owner=user_profile, is_ordered=False)

    # print(ord.is_ordered)

    if ord.exists():
        return ord[0]
    return 0


@login_required
def add_to_cart(request, prod_id):
    product = Product.objects.get(id=prod_id)
    # print(product.stock)

    # return HttpResponse('hello')

    # if request.GET:
    #     vendorid = request.GET['vendorid']
    #     print(vendorid)
    #     ven_qty = VendorQty.objects.get(id=vendorid)
    #     ven = ven_qty.Vendor
    #     print(ven)
    #     print(ven_qty)

    u = User.objects.get(pk=request.user.pk)
    user_profile = Profile.objects.get(user_name=u)
    print(user_profile)

    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)

    print(user_order, status)

    if status:
        ref_code = generate_order_id()
        print(ref_code)
        order_item, status = OrderItem.objects.get_or_create(product=product, ref_code=ref_code)
        user_order.items.add(order_item)
        user_order.ref_code = ref_code
        user_order.save()
    else:
        order_item, status = OrderItem.objects.get_or_create(product=product, ref_code=user_order.ref_code)
        user_order.items.add(order_item)
        user_order.save()

    if request.GET:
        nextto = request.GET["nextto"]
        return redirect(nextto)
    else:
        return redirect('cart:order_summary')


@login_required
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
    return redirect(reverse('cart:order_summary'))


@login_required
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)

    context = {
        'order': existing_order
    }
    return render(request, 'cart/order_summary.html', context)


@login_required
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'ordre': existing_order
    }

    return render(request, 'cart/checkout.html', context)


@login_required
def update_transaction_records(request):
    order_to_purchase = get_user_pending_order(request)

    # print(order_to_purchase)

    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()

    order_items = order_to_purchase.items.all()

    for item in order_items:
        product = Product.objects.get(prod_name=item.product)
        product.stock -= item.qty
        product.save()

    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    u = User.objects.get(pk=request.user.pk)
    profile = Profile.objects.get(user_name=u)
    transaction = Transaction(profile=profile,
                              order_id=order_to_purchase.ref_code,
                              amount=order_to_purchase.get_cart_total(),
                              success=True)

    transaction.save()
    subject = 'Your order has been successfully placed'
    context = {
        'ordre': order_to_purchase,
        'user': request.user,
        'total': order_to_purchase.get_cart_total(),
    }
    html = render_to_string('cart/message.html', context)
    message = render_to_string('cart/message.html', context)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email]

    send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=html)
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('user_auth:user_profile'))


def qtyupdate(request):
    a = request.POST.get('item_id')
    if request.method == "POST":
        order_id = request.POST["order_id"]
        item_id = request.POST["item_id"]
        qty = request.POST["z"]
        order = get_user_pending_order(request)
        item = order.items.get(pk=item_id)
        item.qty = qty
        print("data: " + item_id + "        " + order_id + "           " + qty)
        item.save()
        order.save()
    return HttpResponse(" ")
