# views.py
from django.shortcuts import render, redirect
from .models import AdminUser
from django.contrib import messages

def admin_signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")  

        if AdminUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
        else:
            user = AdminUser(email=email, password=password)  # Plain text password
            user.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect("gadmin:admin_signin")

    return render(request, "admin_signup.html")

def admin_signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = AdminUser.objects.get(email=email)
            if user.password == password:  # Plain text comparison (⚠ Not secure)
                request.session["admin_id"] = user.id  # Store session
                messages.success(request, "Login successful!")
                return redirect("gadmin:gadminhome")
            else:
                messages.error(request, "Invalid credentials")
        except AdminUser.DoesNotExist:
            messages.error(request, "User does not exist")

    return render(request, "admin_signin.html")  


def gadminhome(request):
    return render(request, 'aindex.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from gadmin.models import Driver

def add_driver(request):
    if request.method == "POST":
        driver_id = request.POST.get("driver_id")
        name = request.POST.get("name")
        aadhar_number = request.POST.get("aadhar_number")
        address = request.POST.get("address")
        driving_license_number = request.POST.get("driving_license_number")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        print("Received driver_id:", driver_id)  # Debugging

        if not driver_id:
            messages.error(request, "Driver ID is required!")
            return redirect("gadmin:add_driver")

        try:
            driver = Driver.objects.create(
                driver_id=driver_id,
                name=name,
                aadhar_number=aadhar_number,
                address=address,
                driving_license_number=driving_license_number,
                phone_number=phone_number,
                password=password
            )
            messages.success(request, "Driver added successfully!")
            return redirect("gadmin:view_driver")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("gadmin:add_driver")

    return render(request, "add_driver.html")

def view_driver(request):
    drivers = Driver.objects.all()  # Fetch all drivers from the database
    return render(request, 'view_driver.html', {'drivers': drivers})
from django.shortcuts import get_object_or_404, redirect
from .models import Driver

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Driver

def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, driver_id=driver_id)

    if request.method == "POST":
        name = request.POST.get("name")
        aadhar_number = request.POST.get("aadhar_number")
        address = request.POST.get("address")
        driving_license_number = request.POST.get("driving_license_number")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")

        # Validate required fields
        if not name or not aadhar_number or not address or not driving_license_number or not phone_number:
            messages.error(request, "All fields are required.")
            return redirect("gadmin:edit_driver", driver_id=driver_id)

        # Validate Aadhar (12 digits)
        if not aadhar_number.isdigit() or len(aadhar_number) != 12:
            messages.error(request, "Aadhar Number must be a valid 12-digit number.")
            return redirect("gadmin:edit_driver", driver_id=driver_id)

        # Validate phone number (10 digits)
        if not phone_number.isdigit() or len(phone_number) != 10:
            messages.error(request, "Phone Number must be a valid 10-digit number.")
            return redirect("gadmin:edit_driver", driver_id=driver_id)

        # Update driver details
        driver.name = name
        driver.aadhar_number = aadhar_number
        driver.address = address
        driver.driving_license_number = driving_license_number
        driver.phone_number = phone_number

        # Update password only if entered
        if password:
            driver.set_password(password)  # Hashing the password before saving

        driver.save()
        messages.success(request, "Driver details updated successfully!")
        return redirect("gadmin:view_driver")

    return render(request, "edit_driver.html", {"driver": driver})
def delete_driver(request, driver_id):
    driver = get_object_or_404(Driver, driver_id=driver_id)

    if request.method == "POST":
        driver.delete()
        messages.success(request, "Driver deleted successfully!")
        return redirect("gadmin:view_driver")

    return render(request, "delete_driver.html", {"driver": driver})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Recycler

def add_recycler(request):
    if request.method == "POST":
        recycler_id = request.POST.get("recycler_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        company_name = request.POST.get("company_name")
        address = request.POST.get("address")
        password = request.POST.get("password")  # Consider hashing this before storing

        if recycler_id and name and email and phone_number and company_name and address and password:
            if Recycler.objects.filter(recycler_id=recycler_id).exists():
                messages.error(request, "Recycler ID already exists!")
            elif Recycler.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
            else:
                Recycler.objects.create(
                    recycler_id=recycler_id,
                    name=name,
                    email=email,
                    phone_number=phone_number,
                    company_name=company_name,
                    address=address,
                    password=password,  # Consider hashing before saving
                )
                messages.success(request, "Recycler added successfully!")
                return redirect("gadmin:view_recycler")
        else:
            messages.error(request, "All fields are required!")

    return render(request, "add_recycler.html")


def view_recycler(request):
    recyclers = Recycler.objects.all().order_by("recycler_id")
    return render(request, "view_recycler.html", {"recyclers": recyclers})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Recycler
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from gadmin.models import Recycler

def edit_recycler(request, recycler_id):
    recycler = get_object_or_404(Recycler, recycler_id=recycler_id)

    if request.method == "POST":
        recycler.name = request.POST.get("name")
        recycler.email = request.POST.get("email")
        recycler.phone_number = request.POST.get("phone_number")
        recycler.address = request.POST.get("address")
        recycler.company_name = request.POST.get("company_name")
        recycler.save()
        messages.success(request, "Recycler details updated successfully!")
        return redirect("gadmin:view_recycler")

    return render(request, "edit_recycler.html", {"recycler": recycler})


def delete_recycler(request, recycler_id):
    recycler = get_object_or_404(Recycler, recycler_id=recycler_id)

    if request.method == "POST":
        recycler.delete()
        messages.success(request, "Recycler deleted successfully!")
        return redirect("gadmin:view_recycler")

    return render(request, "delete_recycler.html", {"recycler": recycler})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from customer.models import GarbagePickup
from gadmin.models import Driver

def manage_garbage(request):

    schedules = GarbagePickup.objects.select_related('user').all()
    
    context = {
        'schedules': schedules,
    }
    return render(request, 'manage_garbage.html', context)
    


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from customer.models import GarbagePickup
from gadmin.models import Driver, DriverAssigned

def assign_driver(request, schedule_id):
    schedule = get_object_or_404(GarbagePickup, id=schedule_id)
    drivers = Driver.objects.all()

    # Fetch existing assignment if available
    assignment, created = DriverAssigned.objects.get_or_create(garbage_pickup=schedule)

    if request.method == "POST":
        driver_id = request.POST.get("driver_id")
        status = request.POST.get("status")
        driver = get_object_or_404(Driver, id=driver_id)

        # Update the assignment
        assignment.driver = driver
        assignment.status = status
        assignment.save()

        messages.success(request, f"🚛 Driver {driver.name} assigned successfully!")
        return redirect('gadmin:assigned_drivers_list')


    return render(request, 'assign_driver.html', {
        'schedule': schedule,
        'drivers': drivers,
        'assignment': assignment
    })

from django.urls import reverse

def assigned_drivers_list(request):
   schedules = GarbagePickup.objects.select_related("user").all()
   assigned_drivers = DriverAssigned.objects.select_related("garbage_pickup", "driver").all()
   return render(request, "assigned.html", {
        "schedules": schedules,
        "assigned_drivers": assigned_drivers
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from recycler.models import RecyclerRequests

def manage_recycler_requests(request):
    """Fetch all recycler requests and display them in the admin panel."""
    requests = RecyclerRequests.objects.all().order_by("-request_date")  # Fetch all requests
    
    return render(request, "view_garbage_requests.html", {"requests": requests})

def update_request_status(request, request_id):
    """Update the status of a recycler request."""
    recycler_request = get_object_or_404(RecyclerRequests, id=request_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(RecyclerRequests.STATUS_CHOICES):  # Validate status
            recycler_request.status = new_status
            recycler_request.save()
            messages.success(request, "Request status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect("gadmin:manage_recycler_requests")  # Redirect back to admin page


def delete_request(request, request_id):
    
    if request.method == "POST":
        request_obj = get_object_or_404(RecyclerRequests, id=request_id)
        request_obj.delete()
        messages.success(request, "Request deleted successfully.")
    return redirect('gadmin:manage_recycler_requests') 

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from customer.models import Complaint as CustomerComplaint  # Alias to avoid confusion
from collector.models import Complaint as CollectorComplaint  # Alias to avoid confusion

# --------------------- View for Resident Complaints ---------------------
from django.shortcuts import render, redirect, get_object_or_404


def view_residents_complaint(request):
    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.is_solved = not complaint.is_solved  # Toggle status
        complaint.save()
        messages.success(request, "Complaint status updated successfully.")
        return redirect("gadmin:view_residents_complaint")

    # Fetch complaints along with pickup schedule details
    complaints = CustomerComplaint.objects.select_related("user", "pickup_schedule").order_by("-created_at")

    return render(request, "view_residents_complaint.html", {"complaints": complaints})


# --------------------- View for Collector Complaints ---------------------


def view_collector_complaint(request):
    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        complaint = get_object_or_404(CollectorComplaint, id=complaint_id)
        complaint.is_solved = not complaint.is_solved  # Toggle status
        complaint.save()
        messages.success(request, "Complaint status updated successfully.")
        return redirect("gadmin:view_collector_complaint")

    # Fetch complaints with driver and pickup details
    complaints = CollectorComplaint.objects.select_related("pickup", "driver").order_by("-submitted_at")

    return render(request, "view_collector_complaint.html", {"complaints": complaints})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from recycler.models import Complaint

def view_recycler_complaints(request):
    """Fetch all complaints and allow status updates."""
    complaints = Complaint.objects.all().order_by("-filed_at")

    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        complaint = get_object_or_404(Complaint, id=complaint_id)

        # Toggle `is_solved` status
        complaint.is_solved = not complaint.is_solved
        complaint.save()

        status_message = "Complaint marked as solved." if complaint.is_solved else "Complaint status set to not solved."
        messages.success(request, status_message)

        return redirect("gadmin:view_recycler_complaints")

    return render(request, "view_recyclers_complaint.html", {"complaints": complaints})
from django.shortcuts import render
from django.utils.timezone import now
from user.models import Order

def daily_report(request):
    today = now().date()
    orders = Order.objects.filter(created_at__date=today)

    # Compute totals safely
    total_orders = orders.count()
    
    total_supercoins = sum(
        getattr(item, 'total_supercoins', lambda: item.supercoin_value * item.quantity)()
        for order in orders
        for item in order.order_items.all()
        if item.supercoin_value is not None
    )

    total_cash = sum(
        getattr(item, 'total_price', lambda: item.price * item.quantity)()
        for order in orders if order.payment_method != "Supercoins"
        for item in order.order_items.all()
        if item.price is not None
    )

    context = {
        "orders": orders,
        "total_orders": total_orders,
        "total_supercoins": total_supercoins,
        "total_cash": total_cash,
    }
    return render(request, "daily_report.html", context)

from django.contrib.auth import logout
from django.shortcuts import redirect

def admin_logout(request):
    logout(request)
    return redirect('gadmin:admin_signin')  # Redirect to admin sign-in page


from recycler.models import RecycledProducts

def view_recycledproducts(request):
    """ Display all recycled products with SuperCoin values """
    products = RecycledProducts.objects.all()  # Fetch all products
    return render(request, "view_recycledproducts.html", {"products": products})
