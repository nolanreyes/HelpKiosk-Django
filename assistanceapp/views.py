from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd
from rest_framework.permissions import AllowAny
from .models import Location
from .forms import LocationEdit, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import LocationSerializer
import requests
import json
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'AssistanceApp/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('assistance_base')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('assistance_base')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context = {}
        return render(request, 'AssistanceApp/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('assistance_login')


@login_required(login_url='login')
def base(request):
    return render(request, 'AssistanceApp/base.html')


@login_required(login_url='login')
def map_view(request):
    # read csv file for sample locations which reload everytime map is opened
    df = pd.read_csv("assistanceapp/data/ResourceLocations.csv")
    for _, row in df.iterrows():
        existing_location = Location.objects.filter(latitude=row['latitude'], longitude=row['longitude']).first()
        # check if already exists
        if not existing_location:
            Location.objects.create(
                resource_name=row['resource_name'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                location_type=row.get('location_type', 'OTHER'),
                address=row.get('address', ''),
                description=row.get('description', ''),
                hours=row.get('hours', '')
            )
    locations = list(Location.objects.values('latitude', 'longitude')[:100])
    context = {'locations': locations}
    return render(request, 'AssistanceApp/map.html', context)


@login_required(login_url='login')
def manage_locations(request):
    # display existing Location entries with pagination
    locations_list = Location.objects.all()
    paginator = Paginator(locations_list, 15)
    page_number = request.GET.get('page')
    locations = paginator.get_page(page_number)

    if request.method == 'POST':
        form = LocationEdit(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manageLocations')
    else:
        form = LocationEdit()
    # render the template
    context = {'form': form, 'locations': locations}
    return render(request, 'AssistanceApp/manageLocations.html', context)


@login_required(login_url='login')
def edit_location(request, resource_name):
    location = get_object_or_404(Location, resource_name=resource_name)

    if request.method == 'POST':
        form = LocationEdit(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('manageLocations')
    else:
        form = LocationEdit(instance=location)

    context = {'form': form, 'location': location}
    return render(request, 'AssistanceApp/editLocation.html', context)


@login_required(login_url='login')
def delete_location(request, resource_name):
    location = get_object_or_404(Location, resource_name=resource_name)
    location.delete()
    return redirect('manageLocations')


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('id')
    serializer_class = LocationSerializer


class GetWeatherData(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        api_key = '77a4c49ffa3bb54972685765aea215f0'
        latitude = '53.3498'  # Example latitude for Dublin
        longitude = '-6.2603'  # Example longitude for Dublin

        url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric'

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            # Return the data as JSON
            return Response(data)
        else:
            return Response(data, status=response.status_code)


# Bookings
def send_booking_request(room_id, check_in_date, check_out_date):
    data = {
        'room': room_id,
        'check_in_date': check_in_date,
        'check_out_date': check_out_date,
        # fix these and add more info
    }
    response = requests.post('http://localhost:8000/sheltermanagement/api/bookings/', data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})
    return response.json()
