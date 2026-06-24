import time

from django.shortcuts import render, redirect, get_object_or_404

from .models import Order
from .forms import OrderCreateForm, OrderUpdateForm


def is_librarian(user):
    return user.is_authenticated and getattr(user, "role", 0) == 1


def order_list(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if is_librarian(request.user):
        orders = Order.get_all()
        return render(request, "order/order_list.html", {"orders": orders})

    return redirect("my_orders")


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect("login")

    orders = Order.objects.filter(user=request.user)
    return render(request, "order/my_orders.html", {"orders": orders})


def order_create(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect("my_orders")
    else:
        form = OrderCreateForm()

    return render(request, "order/order_form.html", {
        "form": form,
        "title": "Create order"
    })


def order_update(request, order_id):
    if not is_librarian(request.user):
        return redirect("home")

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = OrderUpdateForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect("order_list")
    else:
        form = OrderUpdateForm(instance=order)

    return render(request, "order/order_form.html", {
        "form": form,
        "title": "Edit order"
    })


def order_close(request, order_id):
    if not is_librarian(request.user):
        return redirect("home")

    order = get_object_or_404(Order, id=order_id)
    order.update(end_at=int(time.time()))

    return redirect("order_list")