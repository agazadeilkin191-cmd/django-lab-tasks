from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Ana səhifə</h1><p>Xoş gəlmisiniz!</p>")


def about(request):
    return HttpResponse("<h1>Haqqımızda</h1><p>Django laboratoriya tapşırığı №2.</p>")


def contact(request):
    return HttpResponse("<h1>Əlaqə</h1><p>Əlaqə bölməsi.</p>")
