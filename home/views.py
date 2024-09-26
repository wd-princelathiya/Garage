from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from .models import Product, Category
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'home/index.html')


def register(request):
    """Register user"""
    # Forget any user_id
    logout(request)
    request.session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Assinging username and password
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Ensure username and password was submitted
        if not username or not password:
            return render(request, "home/register.html", {
                "error": "enter username and password"
            })

        # Ensure confirmation was submitted
        elif request.POST.get("confirmation") != password:
            return render(request, "home/register.html", {
                "error": "password and confirmation didn't match"
            })

        # Ensure username isn't already in the database
        if User.objects.filter(username=username).exists():
            return render(request, "home/register.html", {
                "error": "Username is already taken."
            })

        # Insert the username and password into database
        user = User.objects.create(
            username=username,
            password=make_password(password)
            )
        user.save()

        # Log the user in
        login(request, user)

        # Redirect user to home page render(request, 'home/index.html')
        return redirect('index')

    # User reached route via GET (as by clicking a link or via redirect)
    return render(request, 'home/register.html')


def log_in(request):
    """Log user in"""

    # Forget any user_id
    logout(request)
    request.session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Assinging username and password
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Ensure username and password was submitted
        if not username or not password:
            return render(request, 'home/login.html', {
                "error": "enter username and password"
            })

        # Check the authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:

            # Log the user in
            login(request, user)

            # Redirect user to home page
            return redirect('index')

        # Show an error and redirect user to home page
        return render(request, 'home/login.html', {
            "error": "username and/or password is incorrect"
        })

    # User reached route via GET (as by clicking a link or via redirect)
    return render(request, 'home/login.html')


def log_out(request):
    """Log user out"""

    # Forget any user_id
    logout(request)

    # Redirect user to login form
    return redirect('log_in')


def sell(request):
    """"Present a product for sale"""

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('log_in')

        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        # checking
        if not name or not price or not quantity:
            return render(request, 'home/sell.html', {
                "error": "enter name, price and quantity"
            })
        if category == "0":
            category = request.POST.get('catname')
            if not category:
                return render(request, 'home/sell.html', {
                    "error": "enter category"
                })
            if Category.objects.filter(name__iexact=category):
                return render(request, 'home/sell.html', {
                    "error": "Evidently we have that category"
                })
            Category.objects.create(name=category)
        Product.objects.create(
            user=request.user,
            name=name,
            category=Category.objects.get(name=category),
            price=price,
            quantity=quantity
            )

        return render(request, 'home/sell.html')

    return render(request, 'home/sell.html', {
        "category": Product.objects.values_list(
            'category',
            flat=True
            ).distinct()
    })


def buy(request):
    """"Present a product for purchase"""

    if request.method == "POST":
        name = request.POST.get('name')
        quantity = (request.POST.get('quantity'))
        product = get_object_or_404(Product, name=name)

        if product.quantity >= quantity:
            product.quantity -= quantity
            product.save()
            return HttpResponse("Product sold successfully!")
        else:
            return HttpResponse("Not enough stock available!")

    return render(request, 'home/buy.html', {'product': Product.objects.all()})


def profile(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'home/profile.html', {
        "product": product
    })
