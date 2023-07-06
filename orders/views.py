from django.shortcuts import render, reverse, redirect

from .models import Product, Order


def home(request):
    return redirect(reverse("idle"))


def idle(request):
    return render(request, "idle.html")


def select(request):
    # payment validation #

    context = {
        "products": Product.objects.all()
    }
    return render(request, "select.html", context=context)


def order(request, product_id):
    product = Product.objects.get(id=product_id)
    Order.objects.create(product=product)

    # deliver product #

    return redirect(reverse("home"))


def about(request):
    return render(request, "about.html")
