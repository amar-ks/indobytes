from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import User
from django.http import JsonResponse
import geocoder
from django.contrib.auth.hashers import make_password

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

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
                current_site = get_current_site(request)
                import random
                token_no = random.randint(100000000000,999999999999)
                query = User(
                    name=name,
                    email=email,
                    username=username,
                    password=password,
                    ip_address=ip_address,
                    location=ip_location,
                    token_no=token_no,
                )
                query.save()
                
                send_email(receipient_email=email, domain=current_site.domain, token_no=token_no)
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
            context = {
                'page_header': 'User Dashboard'
            }
            return render(request, 'indobytes/dashboard.html', context)
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
                    context = {
                        'page_header': 'User Dashboard'
                    }      
                    # return render(request, 'indobytes/dashboard.html', context)
                    return HttpResponseRedirect('../dashboard/')
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
            user_details = User.objects.all().order_by('-created_date')
            context = {
                'page_header': 'User Dashboard',
                'total_users': len(user_details),
            }
            return render(request, 'indobytes/dashboard.html', context)
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

def admin_login(request):
    if 'id' in request.session:
        user_exist  = User.objects.filter(id__exact=request.session['id'], is_superuser=1, is_staff=1, is_active=1, approved=1)
        if user_exist:
            context = {
                'page_header': 'Admin Dashboard'
            }
            return render(request, 'indobytes/admin_dashboard.html', context)
        else:
            del request.session['id']
            return HttpResponseRedirect('../admin_login/')
        
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
                user_details = User.objects.filter(username__iexact=username, password__exact=password, is_superuser=1, is_staff=1, is_active=1, approved=1)
                if user_details:
                    print(3)
                    request.session['id'] = user_details[0].id
                    request.session['username'] = user_details[0].username
                    request.session['access_key']  = '321@123!#$'
                    context = {
                        'page_header': 'Admin Dashboard'
                    }      
                    # return render(request, 'indobytes/admin_dashboard.html', context)
                    return HttpResponseRedirect('../admin_dashboard/')
                else:
                    context = {
                        'message': 2,
                    }
                    return render(request, 'indobytes/admin_login.html', context)
            else:
                context = {
                    'message': 1,
                }
                return render(request, 'indobytes/admin_login.html', context)

    message = 0
    context = {
        'page_header': 'Admin Log In',
        'message': message
    }
    return render(request, 'indobytes/admin_login.html', context)

def admin_dashboard(request):
    if 'id' in request.session:

        user_exist  = User.objects.filter(id__exact=request.session['id'], is_superuser=1, is_staff=1, is_active=1, approved=1)
        if user_exist:
            user_details = User.objects.all().order_by('-created_date')
            context = {
                'page_header': 'Admin Dashboard',
                'user_details': user_details,
                'total_users': len(user_details),
            }
            return render(request, 'indobytes/admin_dashboard.html', context)
        else:
            del request.session['id']
            return HttpResponseRedirect('../admin_login/')
        
    else:
        return HttpResponseRedirect('../admin_login/')

    context = {
        'page_header': 'Admin Dashboard'
    }
    return render(request, 'indobytes/dashboard.html', context)

def admin_logout(request):
	
    # request.session.flush()
    # request.session.modified = True
    del request.session['id']
    del request.session['username']
    del request.session['access_key']
    return HttpResponseRedirect('../admin_login/')

def send_email(receipient_email, domain, token_no):
    message = 0 
    
    subject = 'Thank you for registering to our site'
    message = ' Click on below link to activate your account \n'+ 'http://' + domain + '/activate/uid=' + str(token_no)
    email_from = settings.EMAIL_HOST_USER
    # recipient_list = ['receiver@gmail.com',]
    recipient_list = [receipient_email]
    send_mail( subject, message, email_from, recipient_list )
    if send_mail:
        message = 1
        print(1)
    return message

def activate(request, uid):
    uid = request.POST.get('uid', uid)
    if uid:
        query = User.objects.filter(token_no__exact=uid)
        if query:
            query = User.objects.filter(token_no__exact=uid)
            query.update(
                approved=1
            )
            return HttpResponse("Account Activated")
    return HttpResponse("Activation failed")

def delete_user(request, user_id):
    if 'id' in request.session:
        user_exist  = User.objects.filter(id__exact=request.session['id'], is_superuser=1, is_staff=1, is_active=1, approved=1)
        if user_exist:
            get_user = User.objects.get(pk=user_id)
            if get_user:
                get_user = User.objects.get(pk=user_id)
                get_user.delete()
            return HttpResponseRedirect('../../admin_dashboard/')
        else:
            del request.session['id']
            return HttpResponseRedirect('../admin_login/')
        
    
    return HttpResponseRedirect('../admin_login/')

def is_active(request, user_id):
    if 'id' in request.session:
        user_exist  = User.objects.filter(id__exact=request.session['id'], is_superuser=1, is_staff=1, is_active=1, approved=1)
        if user_exist:
            get_user = User.objects.get(pk=user_id)
            if get_user:
                getuser = User.objects.filter(pk=user_id)
                if get_user.approved == 1:
                    getuser.update(
                        approved=0
                    )
                else:
                    getuser.update(
                        approved=1
                    )
            return HttpResponseRedirect('../../admin_dashboard/')
        else:
            del request.session['id']
            return HttpResponseRedirect('../admin_login/')
        
    
    return HttpResponseRedirect('../admin_login/')