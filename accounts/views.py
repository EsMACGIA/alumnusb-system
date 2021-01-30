from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login

from .models import UserInformation, UserStats, ProfilePicture
from .forms import SignUpForm, EditUserDataForm, getUserDataForm, pictureId
from django.contrib.auth.views import LoginView

@csrf_protect
def registerView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not UserInformation.objects.filter(email=user.email).exists():
                user1inf = UserInformation(first_name='',middle_name='',
                    last_name='',mailing_city='',usb_alumn=0,
                    codigo_alumn_usb='',mailing_country='',
                    email=user.email,mobile='',cohorte=0,birthdate='2020-1-1',
                    age=1,undergrad_degree='',graduate_degree='',carnet=0,
                    usb_undergrad_campus='',graduate_campus='',work_email='',
                    workplace='',donor=1,social_networks='',twitter_account='',
                    instagram_account='')
                user1inf.save()
            if not UserStats.objects.filter(email=user.email).exists():
                user1stats = UserStats(email=user.email,average_gift=0,
                    largest_gift=0,smallest_gift=0,total_gifts=0,
                    best_gift_year_total=0,best_gift_year=0, first_gift_date='2020-1-1', last_gift_date='2020-1-1', total_number_of_gifts=0)
                user1stats.save()
            return redirect('login_url')
    else:
        form = SignUpForm()
    return render(request,'registration/register.html',{'form':form})

@login_required
def edit_user_data(request, username):

    if request.user.username != username:
        return redirect('home')
    
    usr = get_object_or_404(User, username=username)
    user_info = get_object_or_404(UserInformation,  email=usr.email)

    if request.method == 'POST':
        form = EditUserDataForm(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return redirect('user_data', request.user.username)  
    else:
        form = EditUserDataForm(instance=user_info)

    return render(request, 'edit_user_data.html', {'UserInformation': user_info, 'form': form})

@login_required
def user_data(request, username):

    if request.user.username != username:
        return redirect('home')

    usr = get_object_or_404(User, username=username)
    user_info = get_object_or_404(UserInformation,  email=usr.email)

    ret_all_pics = []
    all_pictures = ProfilePicture.objects.all()
    for p in all_pictures:
        ret_all_pics.append(( p , "/"+ p.picture.url ))


    if ( user_info.picture != None ):
        pic = ProfilePicture.objects.get(id=user_info.picture.id)
        ret_pic = ( "/"+ pic.picture.url , True, pic.id )
    else:
        ret_pic = ( "" , False , -1)

    form = pictureId()

    args = {
            'User_information': user_info, 
            'pic': ret_pic,
            'prof_pics':ret_all_pics,
            'form': form
            }

    return render(request, 'user_data.html', args)

@login_required
def edit_user_picture(request, username):

    if request.user.username != username:
        return redirect('home')
    
    usr = get_object_or_404(User, username=username)
    user_info = get_object_or_404(UserInformation,  email=usr.email)

    if request.method == 'POST':
        form = pictureId(request.POST)
        pic_id = form.data['Pic_id']
        if ProfilePicture.objects.filter(id=pic_id).exists():
            pic = ProfilePicture.objects.get(id=pic_id)
            user_info.picture = pic
            user_info.save()
            return redirect('user_data', request.user.username)  
        else:
            form = pictureId()
    else:
        form = pictureId()

    return render(request, 'edit_user_picture.html', {'form': form})