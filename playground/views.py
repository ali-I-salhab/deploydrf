from django.shortcuts import render


def say_hello(request):
    return render(request, 'hello.html', {'name': 'Mosh'})
def say_hellowword(request):
    return render(request,'hello.html',{'username':'ali salhab'})