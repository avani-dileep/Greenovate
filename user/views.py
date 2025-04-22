from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required



from django.shortcuts import render
from recycler.models import RecycledProducts # Import your models

def home(request):
    products = RecycledProducts.objects.all()[:6]  # Fetch only 6 products
    return render(request, "index.html", {"products": products})

def guest(request):
    products = RecycledProducts.objects.all()[:6]  # Fetch only 6 products
    return render(request, "guestindex.html", {"products": products})


from django.contrib.auth import logout

def ulogout(request):
    logout(request)
    return redirect('user:signin')  # Redirect to home page or wherever you want after logout

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import UserDetails
from customer.models import UserProfile, CustomUser
@login_required
def profile(request):
    user = request.user
    user_details = None
    user_profile = None

    try:
        # Check if the user is from the UserDetails model
        user_details = UserDetails.objects.get(user=user)
    except UserDetails.DoesNotExist:
        pass

    try:
        # Check if the user is from the UserProfile model
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        pass

    context = {
        'user_details': user_details,
        'user_profile': user_profile,
        'user': user
    }

    return render(request, 'profile.html', context)

def about(request):
    return render(request, 'about.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import UserDetails
from customer.models import UserProfile, CustomUser
from .models import Feedback  # Assuming you have a Feedback model

@login_required
def contact(request):
    user = request.user
    user_details = None
    user_profile = None

    try:
        user_details = UserDetails.objects.get(user=user)
    except UserDetails.DoesNotExist:
        pass

    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        pass

    if request.method == "POST":
        feedback_text = request.POST.get("feedback")

        if feedback_text:
            # Save feedback to database
            Feedback.objects.create(user=user, message=feedback_text)
            messages.success(request, "Thank you for your feedback!")

            return redirect("user:contact")  # Redirect to avoid resubmission

    context = {
        "user_details": user_details,
        "user_profile": user_profile,
        "user": user
    }
    return render(request, "contact.html", context)



# views.py

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import UserDetails
import re
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
User = get_user_model()  # This ensures that you are using the correct user model

def usignup(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        password = request.POST.get('password')

        errors = {}

        # Validation logic (same as before)
        if not name:
            errors['name'] = 'Full Name is required.'
        elif not re.match(r'^[A-Za-z\s]{3,}$', name):
            errors['name'] = 'Name must contain only letters and spaces, minimum 3 characters.'

        if not email:
            errors['email'] = 'Email is required.'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors['email'] = 'Invalid email format.'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'This email is already registered.'

        if not phone:
            errors['phone'] = 'Phone number is required.'
        elif not re.match(r'^\+?[1-9]\d{9,14}$', phone):
            errors['phone'] = 'Invalid phone number format. Please use international format.'

        if not address:
            errors['address'] = 'Address is required.'
        elif len(address.split()) < 3:
            errors['address'] = 'Please provide a complete address.'

        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'
        elif not re.search(r'[A-Z]', password):
            errors['password'] = 'Password must contain at least one uppercase letter.'
        elif not re.search(r'[a-z]', password):
            errors['password'] = 'Password must contain at least one lowercase letter.'
        elif not re.search(r'\d', password):
            errors['password'] = 'Password must contain at least one number.'

        if errors:
            for error in errors.values():
                messages.error(request, error)
            return render(request, 'signup.html')

        try:
            # Create a new Django User
            user = User.objects.create_user(
                username=email,  # Use email as the username
                email=email,
                password=password
            )
            user.save()

            # Create a new UserDetails entry linked to the User
            user_details = UserDetails(
                user=user,
                name=name,
                email=email,
                phone=phone,
                address=address,
                password=make_password(password)  # Hash the password
            )
            user_details.save()

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('user:signin')
        
        except Exception as e:
            messages.error(request, f'An error occurred during registration: {str(e)}')
            return render(request, 'signup.html')

    return render(request, 'signup.html')

from django.contrib.auth import authenticate, login

def usignin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Both email and password are required.')
            return render(request, 'signin.html')

        try:
            # Authenticate using Django's authentication system
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('user:home')
            else:
                messages.error(request, 'Invalid email or password.')
        
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'signin.html')



from recycler.models import RecycledProducts

def product(request):
    products = RecycledProducts.objects.all()
    categories = RecycledProducts.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'product.html', {'products': products, 'categories': categories})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart, RecycledProducts

def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(RecycledProducts, id=product_id)
        quantity = int(request.POST.get('quantity', 1))

        # Check if stock is available
        if product.stock < quantity:
            return JsonResponse({"error": "❌ Stock is over. Cannot add to cart."}, status=400)

        # Check if user is authenticated
        if request.user.is_authenticated:
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock:
                    return JsonResponse({"error": "❌ Not enough stock available."}, status=400)
            cart_item.save()
            return JsonResponse({"message": "✅ Product added to cart!"})
        else:
            return JsonResponse({"error": "❌ User not authenticated."}, status=403)

    return JsonResponse({"error": "❌ Invalid request."}, status=400)


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)

    # Ensure only the cart owner can remove items
    if request.user != cart_item.user:
        return JsonResponse({"error": "❌ Unauthorized action."}, status=403)

    cart_item.delete()
    return redirect('user:cart_view')


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = []

    total_price = sum(item.total_price() for item in cart_items)
    total_supercoins = sum(item.total_supercoins() for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_supercoins': total_supercoins
    })

    
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Cart

def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if request.method == "POST":
        try:
            new_quantity = int(request.POST.get("quantity", cart_item.quantity))
        except ValueError:
            new_quantity = cart_item.quantity  # Keep the previous value if invalid

        # Ensure quantity is within the allowed limits
        if new_quantity < 1:
            new_quantity = 1
        elif new_quantity > cart_item.product.stock:
            new_quantity = cart_item.product.stock

        cart_item.quantity = new_quantity
        cart_item.save()

        # Recalculate total price and supercoins
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        total_supercoins = sum(item.total_supercoins() for item in cart_items)

        return JsonResponse({
            "success": True,
            "new_quantity": cart_item.quantity,
            "total_price": total_price,
            "total_supercoins": total_supercoins
        })

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Order, OrderItem, Cart, UserDetails
import re
from datetime import datetime

@login_required
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items:
        return JsonResponse({"status": "error", "message": "❌ Your cart is empty!"})

    total_price = sum(item.total_price() for item in cart_items)
    total_supercoins = sum(item.total_supercoins() for item in cart_items)

    user_profile = UserProfile.objects.filter(user=user).first()
    user_details = UserDetails.objects.filter(user=user).first()

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        use_supercoins = request.POST.get("buy_supercoins")  # Checkbox value (if checked, returns "on")

        errors = {}

        # ✅ Validate Card Details if Payment is Online
        if payment_method == "Online":
            card_number = request.POST.get("card_number", "").strip()
            cvv = request.POST.get("cvv", "").strip()
            expiry_date = request.POST.get("expiry_date", "").strip()

            if not re.fullmatch(r"\d{16}", card_number):
                errors["card_number"] = "❌ Card number must be exactly 16 digits."

            if not re.fullmatch(r"\d{3,4}", cvv):
                errors["cvv"] = "❌ CVV must be 3 or 4 digits."

            if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", expiry_date):
                errors["expiry_date"] = "❌ Expiry date must be in MM/YY format."
            else:
                exp_month, exp_year = map(int, expiry_date.split("/"))
                current_year = datetime.now().year % 100
                current_month = datetime.now().month
                if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
                    errors["expiry_date"] = "❌ Card expiry date must be in the future."

        # ✅ Validate SuperCoins Balance
        if payment_method == "Supercoins" and (not user_profile or user_profile.supercoins < total_supercoins):
            errors["supercoins"] = "❌ Not enough supercoins for this purchase."

        # ✅ Return Errors if Any
        if errors:
            return JsonResponse({"status": "error", "errors": errors})

        # ✅ Proceed with Order Placement
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    total_price=total_price,
                    payment_method=payment_method,
                    status="pending",
                )

                for cart_item in cart_items:
                    product = cart_item.product

                    # ✅ Ensure Stock Reduction Happens Only Once
                    if product.stock >= cart_item.quantity:
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=cart_item.quantity,
                            price=product.price,
                            supercoin_value=product.supercoin_value,
                        )

                        product.stock -= cart_item.quantity  # ✅ Deduct only the ordered quantity
                        product.save()
                    else:
                        raise Exception(f"Not enough stock for {product.name}.")

                # ✅ Deduct SuperCoins If Used
                if payment_method == "Supercoins" and user_profile:
                    user_profile.supercoins -= total_supercoins
                    user_profile.save()

                # ✅ Clear Cart After Order Placement
                cart_items.delete()

                return JsonResponse({"status": "success", "message": "🎉 Order placed successfully!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Something went wrong: {str(e)}"})

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "user_details": user_details,
        "user_profile": user_profile,
        "total_supercoins": total_supercoins,
    }
    return render(request, "checkout.html", context)

@login_required
def order_success(request):
    user = request.user

    # ✅ Fetch Orders with Items in One Query (Optimized)
    orders = Order.objects.filter(user=user, status__in=['complete', 'reject', 'pending']).prefetch_related('order_items')

    order_data = []

    for order in orders:
        order_items = []
        total_supercoins_used = sum(item.total_supercoins() for item in order.order_items.all())

        for order_item in order.order_items.all():
            order_items.append({
                "product_name": order_item.product.name,
                "quantity": order_item.quantity,
                "total_price": order_item.total_price(),
                "total_supercoins": order_item.total_supercoins(),
            })

        order_data.append({
            "id": order.id,
            "items": order_items,
            "total_price": order.total_price,
            "total_supercoins_used": total_supercoins_used,
            "payment_method": order.payment_method,
            "status": order.status,
            "created_at": order.created_at,
        })

    context = {
        "orders": order_data,
    }
    return render(request, "order_success.html", context)
