from django.shortcuts import render


def custom_404(request, exception):
    return render(request, 'errors/404.html')


def custom_500(request):
    return render(request, 'errors/500.html')
