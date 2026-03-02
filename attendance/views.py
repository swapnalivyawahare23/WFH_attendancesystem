from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import Attendance
from django.contrib.auth.decorators import login_required
from datetime import datetime
def login_view(request):
    print("Request method:", request.method)

    if request.method == "POST":
        print("POST received")

        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username, password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("User authenticated")
            login(request, user)
            return redirect("dashboard")
        else:
            print("Authentication failed")
            return render(request, "attendance/login.html", {"error": "Invalid credentials"})

    return render(request, "attendance/login.html")


@login_required
def dashboard(request):
    today = timezone.now().date()

    # Today's attendance
    attendance = Attendance.objects.filter(
        user=request.user,
        date=today
    ).first()

    # All attendance records
    records = Attendance.objects.filter(user=request.user)

    # Present Days = records where check_in exists
    present_days = records.filter(check_in__isnull=False).count()

    # Calculate total working hours
    total_hours = 0

    for record in records:
        if record.check_in and record.check_out:
            check_in_datetime = datetime.combine(record.date, record.check_in)
            check_out_datetime = datetime.combine(record.date, record.check_out)

            duration = check_out_datetime - check_in_datetime
            total_hours += duration.total_seconds() / 3600

    total_hours = round(total_hours, 2)

    context = {
        "attendance": attendance,
        "present_days": present_days,
        "total_hours": total_hours,
    }

    return render(request, "attendance/dashboard.html", context)

@login_required
def check_in(request):
    today = timezone.now().date()

    attendance, created = Attendance.objects.get_or_create(
        user=request.user,
        date=today
    )

    if not attendance.check_in:
        attendance.check_in = timezone.now().time()
        attendance.save()

    return redirect("dashboard")


@login_required
def check_out(request):
    today = timezone.now().date()

    try:
        attendance = Attendance.objects.get(user=request.user, date=today)
        if not attendance.check_out:
            attendance.check_out = timezone.now().time()
            attendance.save()
    except Attendance.DoesNotExist:
        pass

    return redirect("dashboard")
@login_required
def attendance_history(request):
    records = Attendance.objects.filter(
        user=request.user
    ).order_by('-date')

    return render(request, "attendance/attendance_history.html", {
        "records": records
    })