from django.shortcuts import render


def base(request):
    # base
    return render(request, 'helpfinance/base.html')


def dashboard(request):
    # dashboard
    return render(request, 'helpfinance/dashboard.html')
