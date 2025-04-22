from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect
from gadmin.models import Recycler

def recycler_index(request):
    # Ensure the user is logged in
    recycler_id = request.session.get("recycler_id")
    recycler_name = request.session.get("recycler_name")

    if not recycler_id:
        return redirect("recycler_signin")  # Redirect to login if not logged in

    # Fetch full recycler details (optional, if needed)
    try:
        recycler = Recycler.objects.get(recycler_id=recycler_id)
    except Recycler.DoesNotExist:
        recycler = None

    return render(request, "recycler_index.html", {
        "driver_id": recycler_id,
        "driver_name": recycler_name,
        "recycler": recycler,  # Full recycler object if needed
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from gadmin.models import Recycler

def recycler_signin(request):
    if request.method == "POST":
        recycler_id = request.POST.get("driver_id", "").strip()
        password = request.POST.get("password", "").strip()

        # Backend Validation
        if not recycler_id or not password:
            messages.error(request, "Recycler ID and Password are required.")
            return render(request, "recycler_signin.html")

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, "recycler_signin.html")

        try:
            recycler = Recycler.objects.get(recycler_id=recycler_id)

            # Direct password comparison (since it's stored as plain text)
            if recycler.password == password:  
                request.session["recycler_id"] = recycler.recycler_id
                request.session["recycler_name"] = recycler.name
                
                return redirect("recycler:recycler_index")  
            else:
                messages.error(request, "Invalid password. Please try again.")
        except Recycler.DoesNotExist:
            messages.error(request, "Recycler ID not found. Please check your credentials.")

    return render(request, "recycler_signin.html")

from django.shortcuts import render, redirect

def recycler_logout(request):
    request.session.flush()  # Clear session data
    return redirect("recycler:recycler_signin")  # Redirect to login

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from gadmin.models import Recycler

def recycler_profile(request):
    """ View and update recycler profile """

    # Assuming user is logged in and their recycler ID is stored in session
    recycler_id = request.session.get('recycler_id')

    # Fetch recycler details
    recycler = get_object_or_404(Recycler, recycler_id=recycler_id)

    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Update recycler details
        recycler.name = name
        recycler.phone_number = phone_number
        recycler.address = address

        # Handle password update (without hashing)
        if new_password and confirm_password:
            if new_password == confirm_password:
                recycler.password = new_password  # Storing as plaintext (not recommended)
            else:
                messages.error(request, "Passwords do not match.")
                return redirect("recycler:recycler_profile")

        recycler.save()
        messages.success(request, "Profile updated successfully!")

        return redirect("recycler:recycler_profile")

    return render(request, "recycler_profile.html", {"recycler": recycler})

from django.shortcuts import render, redirect
from django.contrib import messages
from gadmin.models import Recycler
from .models import RecyclerRequests
from datetime import datetime

def recycler_request_garbage(request):
    """ Recycler can request garbage for recycling """

    recycler_id = request.session.get('recycler_id')
    recycler = Recycler.objects.get(recycler_id=recycler_id)

    if request.method == "POST":
        # Process multiple garbage types and their weights
        garbage_details = {}
        garbage_types = ["plastic", "paper", "glass", "e-waste"]
        for gtype in garbage_types:
            weight = request.POST.get(f"{gtype}_weight")
            if weight:
                garbage_details[gtype] = int(weight)

        pickup_date = request.POST.get("pickup_date")
        notes = request.POST.get("notes")

        if not garbage_details:
            messages.error(request, "Please select at least one garbage type with a valid weight.")
            return redirect("recycler:recycler_request_garbage")

        try:
            pickup_date = datetime.strptime(pickup_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid pickup date format!")
            return redirect("recycler:recycler_request_garbage")

        if pickup_date < datetime.today().date():
            messages.error(request, "Pickup date cannot be in the past!")
            return redirect("recycler:recycler_request_garbage")

        # Save request with garbage details as JSON
        RecyclerRequests.objects.create(
            recycler=recycler,
            garbage_details=garbage_details,
            pickup_date=pickup_date,
            notes=notes,
            status="pending"
        )

        messages.success(request, "Garbage request submitted successfully!")
        return redirect("recycler:view_requests")

    # Fetch recycler’s past requests
    recycler_requests = RecyclerRequests.objects.filter(recycler=recycler).order_by("-request_date")

    return render(request, "request_garbage.html", {"recycler_requests": recycler_requests})

from django.shortcuts import render
from .models import RecyclerRequests

def view_requests(request):
    """ Display all garbage requests submitted by the recycler """
    recycler_id = request.session.get('recycler_id')
    requests = RecyclerRequests.objects.filter(recycler__recycler_id=recycler_id).order_by("-request_date")

    return render(request, "view_request.html", {"requests": requests})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import RecycledProducts
from django.contrib.auth.decorators import login_required

def add_recycled_product(request):
    """ Add a new recycled product with SuperCoin value """
    if request.method == "POST":
        category = request.POST["category"]
        name = request.POST["name"]
        description = request.POST["description"]
        price = request.POST["price"]
        supercoin_value = request.POST["supercoin_value"]  # New SuperCoin field
        stock = request.POST["stock"]
        image = request.FILES.get("image")

        if not category or not name or not description or not price or not supercoin_value or not stock or not image:
            messages.error(request, "All fields are required!")
            return redirect("recycler:add_recycled_product")

        product = RecycledProducts(
            category=category,
            name=name,
            description=description,
            price=price,
            supercoin_value=supercoin_value,  # Storing SuperCoin value
            stock=stock,
            image=image
        )
        product.save()
        messages.success(request, "Product added successfully!")
        return redirect("recycler:view_products")

    return render(request, "add_products.html")

def view_products(request):
    """ Display all recycled products with SuperCoin values """
    products = RecycledProducts.objects.all()  # Fetch all products
    return render(request, "view_products.html", {"products": products})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import RecycledProducts

def edit_product(request, product_id):
    product = get_object_or_404(RecycledProducts, id=product_id)

    if request.method == "POST":
        product.category = request.POST.get("category")
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.supercoin_value = request.POST.get("supercoin_value")
        product.stock = request.POST.get("stock")

        # Handle image upload
        if "image" in request.FILES:
            product.image = request.FILES["image"]

        product.save()
        messages.success(request, "Product updated successfully!")

        # Redirect to the view products page
        return redirect("recycler:view_products")  # Change to your actual URL name

    return render(request, "edit_product.html", {"product": product})
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import RecycledProducts

def delete_product(request, product_id):
    # Check if the user is logged in
    if not request.session.get('recycler_id'):
        return redirect("recycler:recycler_signin")

    # Get and delete the product by its ID
    product = get_object_or_404(RecycledProducts, id=product_id)
    product.delete()

    messages.success(request, "Product deleted successfully!")
    return redirect("recycler:view_products")




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Complaint, RecyclerRequests

def submit_complaint(request):
    recycler_id = request.session.get("recycler_id")  # Get Recycler ID from session
    
    if not recycler_id:
        messages.error(request, "You must be logged in as a recycler to submit complaints.")
        return redirect("recycler:recycler_signin")  # Redirect to recycler sign-in

    if request.method == "POST":
        recycler_request_id = request.POST.get("request_id")
        complaint_text = request.POST.get("complaint_text")

        if not recycler_request_id or not complaint_text:
            messages.error(request, "All fields are required.")
            return redirect("recycler:submit_complaint")

        recycler_request = get_object_or_404(RecyclerRequests, id=recycler_request_id, recycler_id=recycler_id)

        # Create complaint
        Complaint.objects.create(
            recycler_request=recycler_request,
            complaint_text=complaint_text,
        )

        messages.success(request, "Complaint submitted successfully!")
        return redirect("recycler:view_complaints")

    # ✅ Fetch **approved requests** based on Recycler ID
    recycler_requests = RecyclerRequests.objects.filter(
        recycler_id=recycler_id, status="approved"
    ).order_by("-id")  # Fetch by ID (latest first)

    return render(request, "recycler_complaint.html", {"recycler_requests": recycler_requests})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Complaint

def view_complaints(request):
    recycler_id = request.session.get("recycler_id")  # Get recycler ID from session
    if not recycler_id:
        messages.error(request, "You must be logged in as a recycler to view complaints.")
        return redirect("recycler:recycler_signin")  # Redirect to login page

    # Fetch complaints where the recycler matches the logged-in recycler
    complaints = Complaint.objects.filter(recycler_request__recycler_id=recycler_id).order_by("-filed_at")

    return render(request, "view_recycler_complaint.html", {"complaints": complaints})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from user.models import Order, OrderItem, UserDetails
from customer.models import UserProfile  # Import from customer app

def order_details(request):
    orders = Order.objects.select_related('user__userprofile', 'user__userdetails').prefetch_related('order_items__product').all()
    return render(request, 'view_orders.html', {'orders': orders})

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):  # Validate status
            order.status = new_status
            order.save()
            messages.success(request, "Order status updated successfully!")
        else:
            messages.error(request, "Invalid status selection!")

    return redirect('recycler:order_details')  # Redirect to order details page


def completed_orders(request):
    orders = Order.objects.filter(status="complete")  # Filter only completed orders
    return render(request, 'completed_order.html', {'orders': orders})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from user.models import Order
from django.contrib.auth.decorators import login_required

def pending_orders(request):
    orders = Order.objects.filter(status="pending")  # Filter only pending orders
    return render(request, 'pending_order.html', {'orders': orders})

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        messages.success(request, "Order status updated successfully.")
        return redirect('recycler:pending_orders')  # Redirect to pending orders page
    return redirect('recycler:pending_orders')

import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.conf import settings
from user.models import Order, OrderItem
from recycler.models import RecycledProducts


def daily_orders(request):
    today = now().date()
    orders = Order.objects.filter(created_at__date=today)

    # Compute totals safely
    total_orders = orders.count()

    total_supercoins = sum(
        item.total_supercoins() if callable(item.total_supercoins) else item.supercoin_value * item.quantity
        for order in orders
        for item in order.order_items.all()
        if item.supercoin_value is not None
    )

    total_cash = sum(
        item.total_price() if callable(item.total_price) else item.price * item.quantity
        for order in orders if order.payment_method != "Supercoins"
        for item in order.order_items.all()
        if item.price is not None
    )

    # If the user requests an Excel download
    if "download" in request.GET:
        return generate_excel_report(orders, total_orders, total_supercoins, total_cash)

    context = {
        "orders": orders,
        "total_orders": total_orders,
        "total_supercoins": total_supercoins,
        "total_cash": total_cash,
    }
    return render(request, "daily_reports.html", context)


def generate_excel_report(orders, total_orders, total_supercoins, total_cash):
    # Create a new workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Daily Orders Report"

    # Add column headers
    headers = ["Order Date", "Name", "Product Name", "Quantity", "Price/Supercoin", "Status", "Payment Method"]
    ws.append(headers)

    # Add order data
    for order in orders:
        for item in order.order_items.all():
            # Handle missing userdetails safely
            user_name = getattr(order.user.userdetails, "name", order.user.username) if hasattr(order.user, "userdetails") else order.user.username

            # ✅ FIXED: Ensuring correct fetching of values
            price = item.total_price() if callable(item.total_price) else item.price * item.quantity
            supercoins = item.total_supercoins() if callable(item.total_supercoins) else item.supercoin_value * item.quantity

            price_or_supercoins = f"{supercoins} Supercoins" if order.payment_method == "Supercoins" else f"₹{price}"

            ws.append([
                order.created_at.strftime("%d-%m-%Y"),
                user_name,
                item.product.name,
                item.quantity,
                price_or_supercoins,
                order.status,
                order.payment_method,
            ])

    # Add summary
    ws.append([])
    ws.append(["Total Orders", "Total Supercoins Used", "Total Cash Payments"])
    ws.append([total_orders, f"{total_supercoins} Supercoins", f"₹{total_cash}"])

    # Create HTTP response with Excel file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="Daily_Report_{now().strftime("%Y-%m-%d")}.xlsx"'
    
    # Save the workbook to the response
    wb.save(response)
    return response


from django.shortcuts import render
from user.models import Feedback, UserDetails  # Import UserDetails from user app
from customer.models import UserProfile  # Import UserProfile from customer app

def user_feedback(request):
    feedbacks = Feedback.objects.select_related("user").order_by("-created_at")

    feedback_data = []
    for feedback in feedbacks:
        # Try fetching name from UserDetails (user app)
        user_details = UserDetails.objects.filter(user=feedback.user).first()
        if user_details:
            name = user_details.name
        else:
            # If not found, fetch name from UserProfile (customer app)
            user_profile = UserProfile.objects.filter(user=feedback.user).first()
            name = user_profile.user.username if user_profile else feedback.user.username  # Default to username

        feedback_data.append({
            "name": name,
            "message": feedback.message,
            "created_at": feedback.created_at
        })

    return render(request, "user_feedback.html", {"feedback_data": feedback_data})
from django.shortcuts import render
from user.models import UserDetails, Order  # Import UserDetails and Order
from customer.models import UserProfile  # Import UserProfile

def ordered_users(request):
    # Fetch users from UserDetails who have placed at least one order
    ordered_users = UserDetails.objects.filter(user__order__isnull=False).distinct()

    # Extract emails from UserDetails to avoid duplicates
    ordered_user_emails = ordered_users.values_list('email', flat=True)

    # Fetch users from UserProfile who have placed an order but are NOT in UserDetails (by email)
    customer_ordered_users = UserProfile.objects.filter(
        user__order__isnull=False
    ).exclude(user__email__in=ordered_user_emails).distinct()

    return render(request, 'user_details.html', {
        'ordered_users': ordered_users,
        'customer_ordered_users': customer_ordered_users
    })
