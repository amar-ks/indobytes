from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import User
from django.http import JsonResponse
import geocoder
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    name = ''
    email = ''
    username = ''
    password = ''
    captcha = ''
    message = 0
    
    if request.POST:
        if 'name' in request.POST:
            name = request.POST['name']
        if 'email' in request.POST:
            email = request.POST['email']
        if 'username' in request.POST:
            username = request.POST['username']
        if 'password' in request.POST:
            password = request.POST['password']
        if 'password_confirm' in request.POST:
            password_confirm = request.POST['password_confirm']
        if password != password_confirm:
            context = {
                'message': 5,
            }
            return render(request, 'indobytes/index.html', context)

        
        if name != '' and email != '' and username != '' and password != '':
            user_email = User.objects.filter(email__iexact=email)
            if user_email:
                context = {
                    'message': 2,
                }
                return render(request, 'indobytes/index.html', context)

            user_email = User.objects.filter(username__iexact=username)
            if user_email:
                context = {
                    'message': 4,
                }
                return render(request, 'indobytes/index.html', context)
            else:
                message = 1
                ip_address, ip_location = get_Host_location()
                captcha = NoReCaptchaField()
                password = make_password(request.POST['password'], 'n7!(gzweq86gr3+!2k-r2=p!tl413nar5^jx)*y3k4(zl2qv')
                query = User(
                    name=name,
                    email=email,
                    username=username,
                    password=password,
                    ip_address=ip_address,
                    location=ip_location,
                )
                query.save()
        else:
            message = 3


    context = {
        'message': message,
        'captcha': captcha
    }
    return render(request, "indobytes/index.html", context)


def validate_email(request):
    message = 0
    if request.method == "POST" and request.is_ajax():
        user_exist = User.objects.filter(email__iexact=request.POST['email'])
        if user_exist:
            message = 1
        else:
            message = 2

    return JsonResponse({'message': message}, safe=False)

def validate_username(request):
    message = 0
    if request.method == "POST" and request.is_ajax():
        user_exist = User.objects.filter(username__iexact=request.POST['username'])
        if user_exist:
            message = 1
        else:
            message = 2

    return JsonResponse({'message': message}, safe=False)


def get_Host_location():
    g = geocoder.ip('me')
    ip_address = g.ip
    ip_location_city = g.city
    ip_location_country = g.country
    ip_location_state = g.state
    ip_location_postal = g.postal
    # # ip_location_lat = g.lat
    # # ip_location_lng = g.lng

    ip_location = ip_location_city + ',' + ip_location_state + ',' + ip_location_country + ',' + ip_location_postal
    return ip_address, ip_location

def login(request):
    if 'id' in request.session:
        user_exist  = User.objects.filter(id__exact=request.session['id'], approved=1)
        if user_exist:
            return HttpResponseRedirect('../dashboard/')
        else:
            del request.session['id']
            return HttpResponseRedirect('/')
        
    else:
        username = ''
        password = ''
        if 'username' in request.POST:
            username = request.POST['username']
        if 'password' in request.POST:
            password = make_password(request.POST['password'], 'n7!(gzweq86gr3+!2k-r2=p!tl413nar5^jx)*y3k4(zl2qv')
        if username != '' and password !='':
            user_exist = User.objects.filter(username__iexact=username, password__exact=password)
            if user_exist:
                print("1")
                user_details = User.objects.filter(username__iexact=username, password__exact=password, approved=1)
                if user_details:
                    print(3)
                    request.session['id'] = user_details[0].id
                    request.session['username'] = user_details[0].username       
                    return render(request, 'indobytes/dashboard.html')
                else:
                    context = {
                        'message': 2,
                    }
                    return render(request, 'indobytes/login.html', context)
            else:
                context = {
                    'message': 1,
                }
                return render(request, 'indobytes/login.html', context)

    message = 0
    context = {
        'page_header': 'Log In',
        'message': message
    }
    return render(request, "indobytes/login.html", context)


def dashboard(request):
    if 'id' in request.session:
        user_exist  = User.objects.filter(id__exact=request.session['id'], approved=1)
        if user_exist:
            return HttpResponseRedirect('../dashboard/')
        else:
            del request.session['id']
            return HttpResponseRedirect('/')
        
    else:
        return HttpResponseRedirect('../login/')

    context = {
        'page_header': 'User Dashboard'
    }
    return render(request, 'indobytes/dashboard.html', context)


def logout(request):
	
    # request.session.flush()
    # request.session.modified = True
    del request.session['id']
    del request.session['username']
    return HttpResponseRedirect('../login/')