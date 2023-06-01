from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import viewsets
from .Serializers import *


# Create your views here.
def index(request):
    if request.method == "POST":
        product_id = request.POST.get("cartid")
        remove = request.POST.get("minus")
        cart_id = request.session.get("cart")
        if cart_id:
            quantity = cart_id.get(product_id)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity - 1
                else:
                    cart_id[product_id] = quantity + 1
            else:
                cart_id[product_id] = 1
        else:
            cart_id = {}
            cart_id[product_id] = 1
        request.session["cart"] = cart_id
    fetch_cat = Category.objects.all()
    cat_id = request.GET.get("category_id")
    if cat_id:
        fetch_product = Product.objects.filter(product_category=cat_id)
    else:
        fetch_product = Product.objects.all()
    context = {"cats": fetch_cat, "products": fetch_product}
    return render(request, "index.html", context=context)


def signup(request):
    if request.method == "POST":
        f_name = request.POST.get("firstname")
        l_name = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        save_info = Registration(
            first_name=f_name,
            last_name=l_name,
            email=email,
            password=make_password(password),
            mobile=mobile,
            gender=gender,
        )
        save_info.save()
        return HttpResponse("Your registration saved successfully")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
    try:
        user = Registration.objects.get(email=email)
        if user:
            if check_password(password, user.password):
                request.session["name"] = user.first_name
                request.session["customer_id"] = user.id
                return redirect("home")
            else:
                return HttpResponse("Invalid Password")
    except:
        return HttpResponse("Email does not exist")


def logout(request):
    request.session.clear()
    return redirect("home")


def cart_details(request):
    ids = list(request.session.get("cart").keys())
    product = Product.objects.filter(id__in=ids)
    return render(request, "cart.html", {"cart_details": product})


def checkout(request):
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        customer_id = request.session.get("customer_id")
        if not customer_id:
            return HttpResponse("Please Login")
        cart = request.session.get("cart")
        product = Product.objects.filter(id__in=list(cart.keys()))
        for item in product:
            save_ord_dtls = Order(
                address=address,
                mobile=mobile,
                customer=Registration(id=customer_id),
                product=item,
                quantity=cart.get(str(item.id)),
                price=item.product_price,
            )
            save_ord_dtls.save()

        return redirect("order")


def order(request):
    customer_id = request.session.get("customer_id")

    order_details = Order.objects.filter(customer=customer_id)

    order_details = Order.objects.all()
    tp = 0
    for item in order_details:
        tp += item.price * item.quantity

    return render(request, "orders.html", {"order_details": order_details, "tp": tp})


class UserViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
