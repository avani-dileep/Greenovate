# views.py
from django.shortcuts import render

def collectorhome(request):
    drivers = Driver.objects.all()  # Fetch all drivers from the database
    return render(request, 'collectorindex.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from customer.models import GarbagePickup
from gadmin.models import Driver, DriverAssigned

def view_driver_pickups(request):
    # Retrieve driver_id from session
    driver_id = request.session.get("driver_id")

    if not driver_id:
        return redirect("collector:driver_signin")  # Redirect if not logged in as a driver

    try:
        # Fetch the driver based on driver_id
        driver = Driver.objects.get(driver_id=driver_id)
    except Driver.DoesNotExist:
        return redirect("collector:driver_signin")  # Redirect if driver not found

    # Fetch assigned pickups for the logged-in driver
    assigned_pickups = GarbagePickup.objects.filter(driverassigned__driver=driver)

    message = "No pickups assigned to you at the moment." if not assigned_pickups.exists() else None

    return render(request, "viewpickup.html", {
        "schedules": assigned_pickups,
        "driver_name": driver.name,
        "message": message
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customer.models import GarbagePickup  # Import GarbagePickup from customer app
from gadmin.models import DriverAssigned  # Import DriverAssigned from gadmin app

from django.shortcuts import render, redirect
from django.contrib import messages


def update_status(request):
    if request.method == "POST":
        # Handle payment status toggle
        if 'toggle_payment' in request.POST:
            schedule_id = request.POST.get('toggle_payment')
            try:
                schedule = GarbagePickup.objects.get(id=schedule_id)
                # Toggle payment status (0 → 1 or 1 → 0)
                schedule.payment_status = 1 if schedule.payment_status == 0 else 0
                schedule.save()
                messages.success(request, "Payment status updated successfully.")
            except GarbagePickup.DoesNotExist:
                messages.error(request, "Schedule not found.")

        # Handle status update
        for key, value in request.POST.items():
            if key.startswith("status_"):
                schedule_id = key.split("_")[1]
                try:
                    schedule = GarbagePickup.objects.get(id=schedule_id)
                    schedule.driverassigned.status = value
                    schedule.driverassigned.save()
                    messages.success(request, "Status updated successfully.")
                except GarbagePickup.DoesNotExist:
                    messages.error(request, "Schedule not found.")
        
        return redirect('collector:view_driver_pickups')  # Redirect back to the page

    return redirect('collector:view_driver_pickups')

from django.shortcuts import render, get_object_or_404, redirect

def editpickup(request, schedule_id):
    schedule = get_object_or_404(GarbagePickup, id=schedule_id, user=request.user)

    if request.method == 'POST':
        # Update the schedule with form data
        schedule.pickup_date = request.POST['pickup_date']
        schedule.frequency = request.POST['frequency']
        schedule.duration = request.POST['duration']
        schedule.total_payment = request.POST['total_payment']
        schedule.weight = request.POST['weight']
        schedule.subscription_end_date = request.POST.get('subscription_end_date')  # Update the new field
        schedule.save()
        
        return redirect('collector:viewpickup')  # Redirect to view after saving
    
    return render(request, 'editpickup.html', {'schedule': schedule})


def deletepickup(request, schedule_id):
    # Get the GarbagePickup object for the logged-in user
    schedule = get_object_or_404(GarbagePickup, id=schedule_id, user=request.user)
    
    if request.method == 'POST':
        # Delete the schedule
        schedule.delete()
        return redirect('collector:viewpickup')  # Redirect to the view schedule page after deletion
    
    return render(request, 'deletegarbage.html', {'schedule': schedule})

from django.shortcuts import render, redirect
from django.contrib import messages
from gadmin.models import Driver

def driver_signin(request):
    if request.method == "POST":
        driver_id = request.POST.get("driver_id")
        password = request.POST.get("password")

        try:
            # Authenticate using driver_id and password
            driver = Driver.objects.get(driver_id=driver_id, password=password)

            # Store driver details in session
            request.session["driver_id"] = driver.driver_id
            request.session["driver_name"] = driver.name
            
            return redirect("collector:collectorhome")  # Redirect to the driver dashboard
        except Driver.DoesNotExist:
            messages.error(request, "Invalid Driver ID or Password.")

    return render(request, "driver_signin.html")

from django.shortcuts import redirect

def driver_logout(request):
    # Clear the session
    request.session.flush()
    
    # Redirect to the driver sign-in page
    return redirect("collector:driver_signin")

from django.shortcuts import render, redirect
from django.contrib import messages
from gadmin.models import Driver  
from django.core.files.storage import default_storage

def collector_profile(request):
    driver_id = request.session.get("driver_id")

    if not driver_id:
        return redirect("collector:driver_signin")  

    try:
        driver = Driver.objects.get(driver_id=driver_id)
    except Driver.DoesNotExist:
        messages.error(request, "Driver not found.")
        return redirect("collector:driver_signin")

    if request.method == "POST":
        driver.name = request.POST.get("name")
        driver.phone_number = request.POST.get("phone_number")
        driver.address = request.POST.get("address")

        if "profile_picture" in request.FILES:
            if driver.profile_picture:
                default_storage.delete(driver.profile_picture.path)  # Delete old image
            driver.profile_picture = request.FILES["profile_picture"]

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password and confirm_password:
            if new_password == confirm_password:
                driver.password = new_password  # (⚠️ Ideally, use hashing)
            else:
                messages.error(request, "Passwords do not match!")
                return redirect("collector:collector_profile")

        driver.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("collector:collector_profile")

    return render(request, "collector_profile.html", {"driver": driver})
from django.shortcuts import render, redirect
from django.contrib import messages
from gadmin.models import Driver  # ✅ Import Driver model
from .models import Complaint
from customer.models import GarbagePickup
from gadmin.models import DriverAssigned

def submit_complaint(request):
    # Ensure the logged-in user is a driver
    driver_id = request.session.get("driver_id")

    if not driver_id:
        messages.error(request, "You must be logged in as a driver to access this page.")
        return redirect("collector:driver_signin")  # Redirect to login

    try:
        # Fetch the driver based on session-stored driver_id
        driver = Driver.objects.get(driver_id=driver_id)
    except Driver.DoesNotExist:
        messages.error(request, "Invalid session. Please log in again.")
        return redirect("collector:driver_signin")

    if request.method == "POST":
        pickup_id = request.POST.get("pickup_schedule")
        complaint_text = request.POST.get("complaint_text")

        if not pickup_id or not complaint_text:
            messages.error(request, "All fields are required.")
            return redirect("collector:collectorhome")

        try:
            # Ensure the driver can only complain about pickups assigned to them
            pickup = GarbagePickup.objects.get(id=pickup_id, driverassigned__driver=driver)
            Complaint.objects.create(driver=driver, pickup=pickup, complaint_text=complaint_text)
            messages.success(request, "Complaint submitted successfully.")
            return redirect("collector:view_complaint")
        except GarbagePickup.DoesNotExist:
            messages.error(request, "Invalid pickup selection. Please select an assigned pickup.")
            return redirect("collector:collectorhome")

    # Fetch only pickups assigned to the logged-in driver
    driver_schedules = GarbagePickup.objects.filter(driverassigned__driver=driver)
    return render(request, "driver_complaint.html", {"driver_schedules": driver_schedules})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Complaint
from gadmin.models import Driver


def view_complaint(request):
    # Ensure the user is a driver
    driver_id = request.session.get("driver_id")
    if not driver_id:
        return redirect("collector:driver_signin")

    try:
        driver = Driver.objects.get(driver_id=driver_id)
    except Driver.DoesNotExist:
        return redirect("collector:driver_signin")

    # Fetch complaints submitted by the logged-in driver
    complaints = Complaint.objects.filter(driver=driver).order_by("-submitted_at")

    return render(request, "view_driver_complaint.html", {"complaints": complaints})

