from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Farm, Device, Observation, Alert


@login_required
def dashboard(request):
    farms = Farm.objects.all()
    devices = Device.objects.all()
    alerts = Alert.objects.order_by("-created_at")[:5]
    observations = Observation.objects.order_by("-capture_time")[:8]

    context = {
        "now": datetime.now(),
        "farm_count": farms.count(),
        "device_count": devices.count(),
        "alert_count": alerts.count(),
        "recent_alerts": alerts,
        "recent_observations": observations,
    }
    return render(request, "dashboard.html", context)


@login_required
def logout_view(request):
    """退出当前登录账号并返回登录页面。"""
    logout(request)
    return redirect("/login/")
