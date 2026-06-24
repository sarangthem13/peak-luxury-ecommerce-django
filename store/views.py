from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import Product, Category, Review
from .forms import ReviewForm
# ==========================
# HOME
# ==========================
def home(request):
    products = Product.objects.filter(available=True)[:8]

    return render(
        request,
        'home.html',
        {
            'products': products
        }
    )


# ==========================
# PRODUCT LIST
# ==========================
def product_list(request):
    categories = Category.objects.all()

    products = Product.objects.filter(
        available=True
    )

    return render(
        request,
        'product_list.html',
        {
            'products': products,
            'categories': categories
        }
    )

# ==========================
# LOGIN
# ==========================
def login_view(request):

    if request.method == "POST":

        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(
                email=username_or_email
            )
            username = user_obj.username

        except User.DoesNotExist:
            username = username_or_email

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(
            request,
            'Invalid username/email or password'
        )

    return render(
        request,
        'login.html'
    )


# ==========================
# REGISTER
# ==========================
def register_view(request):

    if request.method == 'POST':

        full_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(
                request,
                'Passwords do not match'
            )
            return redirect('register')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists'
            )
            return redirect('register')

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                'Email already exists'
            )
            return redirect('register')

        first_name = full_name.split()[0]
        last_name = " ".join(
            full_name.split()[1:]
        )

        User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        messages.success(
            request,
            'Account created successfully'
        )

        return redirect('login')

    return render(
        request,
        'register.html'
    )


# ==========================
# LOGOUT
# ==========================
def logout_view(request):
    logout(request)
    return redirect('login')


# ==========================
# CART
# ==========================
def cart_view(request):
    return render(
        request,
        'cart.html'
    )


# ==========================
# WISHLIST
# ==========================
def wishlist(request):

    wishlist_ids = request.session.get(
        'wishlist',
        []
    )

    products = Product.objects.filter(
        id__in=wishlist_ids
    )

    return render(
        request,
        'wishlist.html',
        {
            'products': products
        }
    )


# ==========================
# CHECKOUT
# ==========================
def checkout(request):
    return render(
        request,
        'checkout.html'
    )


# ==========================
# PROFILE
# ==========================
def profile(request):
    return render(
        request,
        'profile.html'
    )


# ==========================
# ORDER HISTORY
# ==========================
def order_history(request):
    return render(
        request,
        'order_history.html'
    )


# ==========================
# CONTACT
# ==========================
def contact(request):
    return render(
        request,
        'contact.html'
    )


# ==========================
# ABOUT
# ==========================
def about(request):
    return render(
        request,
        'about.html'
    )


# ==========================
# FAQ
# ==========================
def faq(request):
    return render(
        request,
        'faq.html'
    )


def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    products = Product.objects.filter(
        category=category,
        available=True
    )

    return render(
        request,
        'product_list.html',
        {
            'products': products,
            'category': category
        }
    )


def search_products(request):

    query = request.GET.get('q', '')

    products = Product.objects.filter(
        name__icontains=query
    )

    return render(
        request,
        'product_list.html',
        {
            'products': products,
            'query': query
        }
    )

def add_to_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')

def cart_view(request):

    cart = request.session.get('cart', {})

    cart_products = []

    total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        cart_products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(
        request,
        'cart.html',
        {
            'cart_products': cart_products,
            'total': total
        }
    )

def add_to_wishlist(request, product_id):

    wishlist = request.session.get('wishlist', [])

    product_id = str(product_id)

    if product_id not in wishlist:
        wishlist.append(product_id)

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist')

def increase_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

def remove_from_wishlist(request, product_id):

    wishlist = request.session.get(
        'wishlist',
        []
    )

    product_id = str(product_id)

    if product_id in wishlist:
        wishlist.remove(product_id)

    request.session['wishlist'] = wishlist

    return redirect('wishlist')


def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    reviews = product.reviews.all()

    if request.method == "POST":

        if request.user.is_authenticated:

            form = ReviewForm(request.POST)

            if form.is_valid():

                review = form.save(commit=False)

                review.product = product
                review.user = request.user

                review.save()

                return redirect(
                    'product_detail',
                    id=product.id
                )

    else:

        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }

    return render(
    request,
    'product_detail.html',
    context
)

from .models import Address

def profile(request):

    wishlist_ids = request.session.get(
        'wishlist',
        []
    )

    cart = request.session.get(
        'cart',
        {}
    )

    wishlist_count = len(wishlist_ids)

    cart_count = sum(cart.values())

    context = {

        'wishlist_count': wishlist_count,

        'cart_count': cart_count,

        'total_orders': 0,

        'orders': [],

    }

    return render(
        request,
        'profile.html',
        context
    )

def addresses(request):

    return render(
        request,
        'addresses.html'
    )
    