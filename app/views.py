from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Profile, Resturant, FoodItem, Order, Cart, CartItem, OrderItem, Review,Address
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import razorpay
from razorpay.errors import SignatureVerificationError
from django.conf import settings




# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')
    

def home(request):
    foods = FoodItem.objects.all()

    query = request.GET.get('q')
    if query:
        foods = foods.filter(name__icontains=query)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        foods = foods.filter(price__gte=min_price)
    if max_price:
        foods = foods.filter(price__lte=max_price)

    veg_only = request.GET.get('veg')
    if veg_only == 'true':
        foods = foods.filter(is_veg=True)

    restaurants_list = Resturant.objects.all()

    default_address = None
    if request.user.is_authenticated:
        default_address = Address.objects.filter(user=request.user, is_default=True).first()

    return render(request, "home.html", {
        'foods': foods,
        'query': query or '',
        'min_price': min_price or '',
        'max_price': max_price or '',
        'restaurants_list': restaurants_list,
        'default_address': default_address,
        'veg_only': veg_only,
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already taken. Please choose another."
            })

        user = User.objects.create_user(
            username=username,
            password=request.POST["password"]
        )
        Profile.objects.create(
            user=user,
            role=request.POST["role"]
        )
        return redirect('login')

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password",
                "username": username
            })

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def place_order(request, food_id):
    food = FoodItem.objects.get(id=food_id)
    return render(request, "choose_payment_buynow.html", {"food": food})


@login_required
def buy_now_online(request, food_id):
    food = FoodItem.objects.get(id=food_id)
    order = Order.objects.create(customer=request.user)
    OrderItem.objects.create(order=order, food=food, quantity=1, price=food.price)
    return render(request, "demo_payment.html", {"order": order})


@login_required
def buy_now_cod(request, food_id):
    food = FoodItem.objects.get(id=food_id)
    order = Order.objects.create(customer=request.user, payment_method='COD')
    OrderItem.objects.create(order=order, food=food, quantity=1, price=food.price)
    return redirect('my_orders')

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).exclude(
        payment_method='ONLINE', is_paid=False
    )
    return render(request, "my_orders.html", {'orders': orders})

@login_required
def delivery_orders(request):
    orders=Order.objects.filter(delivery=request.user)
    return render(request,"delivery_orders.html",{'orders':orders})

@login_required
def advance_status(request, order_id):
    order = Order.objects.get(id=order_id)

    if order.status == 'PACKING':
        order.status = 'OUT'
    elif order.status == 'OUT':
        order.status = 'DELIVERED'

    order.save()
    return redirect('delivery_orders')

@login_required
def add_to_cart(request, food_id):
    food = FoodItem.objects.get(id=food_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        food=food
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')



@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = CartItem.objects.filter(cart=cart)

    total = 0

    for item in items:
        total += item.food.price * item.quantity

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart')

    total = sum(item.subtotal for item in cart_items)

    return render(request, "choose_payment.html", {"total": total})


@login_required
def place_order_online(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart')

    order = Order.objects.create(customer=request.user)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            food=item.food,
            quantity=item.quantity,
            price=item.food.price
        )

    cart_items.delete()

    return render(request, "demo_payment.html", {"order": order})


@login_required
def confirm_demo_payment(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user)
    order.is_paid = True
    order.razorpay_payment_id = "demo_payment_" + str(order.id)
    order.save()
    return redirect('my_orders')

@login_required
def place_order_cod(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart')

    order = Order.objects.create(customer=request.user)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            food=item.food,
            quantity=item.quantity,
            price=item.food.price
        )

    cart_items.delete()

    order.is_paid = False
    order.payment_method = 'COD'
    order.save()

    return redirect('my_orders')


@login_required
def payment_success(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        order = Order.objects.get(id=order_id)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        params_dict = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            order.is_paid = True
            order.razorpay_payment_id = razorpay_payment_id
            order.save()
            return redirect('my_orders')
        except SignatureVerificationError:
            return render(request, "payment_failed.html")

    return redirect('cart')


@login_required
def available_orders(request):
    orders = Order.objects.filter(
        delivery__isnull=True,
        status='PLACED'
    ).filter(
        Q(is_paid=True) | Q(payment_method='COD')
    )
    return render(request, "available_orders.html", {'orders': orders})


@login_required
def accept_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delivery = request.user
    order.status = 'PACKING'
    order.save()
    return redirect('delivery_orders')

@login_required
def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id, cart__user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id, cart__user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

def restaurant_list(request):
    restaurants = Resturant.objects.all()
    return render(request, "restaurant_list.html", {'restaurants': restaurants})


def restaurant_menu(request, restaurant_id):
    restaurant = Resturant.objects.get(id=restaurant_id)
    foods = FoodItem.objects.filter(resturant=restaurant)
    return render(request, "restaurant_menu.html", {
        'restaurant': restaurant,
        'foods': foods
    })

@login_required
def retry_payment(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user)

    if order.is_paid:
        return redirect('my_orders')

    return render(request, "demo_payment.html", {"order": order})

@login_required
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user)

    if request.method == "POST":
        reason = request.POST.get("reason", "")

        if order.status in ['PLACED', 'PACKING']:

            if order.is_paid and not order.is_refunded:
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

                try:
                    client.payment.refund(order.razorpay_payment_id, {
                        "amount": int(order.total * 100)
                    })
                    order.is_refunded = True
                except Exception as e:
                    print("Refund failed:", e)

            order.status = 'CANCELLED'
            order.cancel_reason = reason
            order.save()

        return redirect('my_orders')

    return render(request, "cancel_order.html", {"order": order})


@login_required
def add_review(request, food_id):
    food = FoodItem.objects.get(id=food_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")

        Review.objects.update_or_create(
            user=request.user,
            food=food,
            defaults={"rating": rating, "comment": comment}
        )

    return redirect('food_detail', food_id=food.id)


def food_detail(request, food_id):
    food = FoodItem.objects.get(id=food_id)
    reviews = food.reviews.all().order_by('-created_at')

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    return render(request, "food_detail.html", {
        "food": food,
        "reviews": reviews,
        "user_review": user_review,
    })

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    next_url = request.GET.get('next', 'home')
    return render(request, "address_list.html", {
        "addresses": addresses,
        "next_url": next_url,
    })


@login_required
def add_address(request):
    next_url = request.GET.get('next', 'home')

    if request.method == "POST":
        label = request.POST.get("label", "Home")
        full_address = request.POST.get("full_address")

        is_first = not Address.objects.filter(user=request.user).exists()

        Address.objects.create(
            user=request.user,
            label=label,
            full_address=full_address,
            is_default=is_first
        )
        return redirect(request.POST.get('next', 'home'))

    return render(request, "add_address.html", {"next_url": next_url})


@login_required
def select_address(request, address_id):
    Address.objects.filter(user=request.user).update(is_default=False)
    address = Address.objects.get(id=address_id, user=request.user)
    address.is_default = True
    address.save()

    next_url = request.GET.get('next', 'home')
    return redirect(next_url)











