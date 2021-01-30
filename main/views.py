from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login

from accounts.models import UserInformation, UserStats, Achievements, UserAchievements, Message, ProfilePicture
from accounts.forms import SignUpForm, EditUserDataForm, getUserDataForm
from django.contrib.auth.views import LoginView

from datetime import datetime, timedelta, date

def index(request):
    return render(request,'home.html',{'variable':''})

@login_required
def dashboard(request, username):
    #Check the username and the logged user
    if request.user.username != username:
        return redirect('home')
    
    #try to get the user data if exists
    usr = get_object_or_404(User, username=username)
    user_info = get_object_or_404(UserInformation,  email=usr.email)

    #Try to get the user stats:
    usr_stats = get_object_or_404(UserStats, email=usr.email)

    ach = Achievements.objects.all()

    ach_by_date = []
    ach_by_lvl = []

    for x in ach:
        if UserAchievements.objects.filter(owner=usr.id,achievement=x.name).exists():
            y = UserAchievements.objects.get(owner=usr.id,achievement=x.name)
            ach_by_date.append( (x,y.date, "../../" + x.picture.url) )
            ach_by_lvl.append( (x, "../../" + x.picture.url) )
        
    ach_by_date.sort(key=lambda x:x[1], reverse=True)
    ach_by_lvl.sort(key=lambda x:x[0].level, reverse=True)

    ach_by_date = ach_by_date[:5]
    ach_by_lvl = ach_by_lvl[:5]

    if Message.objects.filter(page='Resumen').exists():
        msg = Message.objects.get(page='Resumen')
    else:
        msg = None

    if ( user_info.picture != None ):
        pic = ProfilePicture.objects.get(id=user_info.picture.id)
        ret_pic = ( "/"+ pic.picture.url , True, pic.id )
    else:
        ret_pic = ( "" , False , -1)

    args = {
                'User_information': user_info,
                'stat': usr_stats,
                'ach_by_date':ach_by_date,
                'ach_by_lvl':ach_by_lvl,
                'msg':msg,
                'pic': ret_pic
            }

    return render(request, 'dashboard/index.html', args)

########################################################################
# View para el chart de la pagina de resumen del dashboard
def resume_chart(request):
    
    usr = get_object_or_404(User, username=request.user)

    #Try to get the user stats:
    usr_stats = get_object_or_404(UserStats, email=usr.email)

    labels = ['Mejor donación', 'Donación promedio', 'Mejor donación en un año', 'Última donación']
    data = [usr_stats.largest_gift, usr_stats.average_gift, usr_stats.best_gift_year_total, usr_stats.last_gift_date]


    return JsonResponse(data = { 'labels': labels, 'data': data})


########################################################################

@login_required
def user_stats(request, username):
    #Check the username and the loged user
    if request.user.username != username:
        return redirect('home')
    
    #try to get the user data if exists
    usr = get_object_or_404(User, username=username)
    user_info = get_object_or_404(UserInformation,  email=usr.email)

    #Try to get the user stats:
    usr_stats = get_object_or_404(UserStats, email=usr.email)
    if ( user_info.picture != None ):
        pic = ProfilePicture.objects.get(id=user_info.picture.id)
        ret_pic = ( "/"+ pic.picture.url , True, pic.id )
    else:
        ret_pic = ( "" , False , -1)


    args = {
                'User_information': user_info,
                'stat': usr_stats,
                'pic': ret_pic
            }

    return render(request, 'dashboard/user_stats.html', args)


def achievements(request, username):

    #Check the username and the loged user
    if request.user.username != username:
        return redirect('home')
    
    #try to get the user data if exists
    usr = get_object_or_404(User, username=username)

    #Try to get the user stats:
    usr_stats = get_object_or_404(UserStats, email=usr.email)

    usr_info = get_object_or_404(UserInformation,  email=usr.email)


    A = Achievements.objects.all()

    ret = []

    for achiev in A:

        if (achiev.name == 'Numero donaciones bronce'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_number_of_gifts
                if ( n is not None and n>=5 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Numero donaciones plata'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_number_of_gifts
                if ( n is not None and n>=10 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Numero donaciones oro'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_number_of_gifts
                if ( n is not None and n>=20 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Numero donaciones platino'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_number_of_gifts
                if ( n is not None and n>=50 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Numero donaciones diamante'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_number_of_gifts
                if ( n is not None and n>=100 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )


        elif (achiev.name == 'Total donaciones bronce'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_gifts
                if ( n is not None and n>=100 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Total donaciones plata'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_gifts
                if ( n is not None and n>=500 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Total donaciones oro'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_gifts
                if ( n is not None and n>=1500 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Total donaciones platino'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_gifts
                if ( n is not None and n>=3000 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Total donaciones diamante'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_gifts
                if ( n is not None and n>=5000 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )


        elif (achiev.name == 'Donacion estrella bronce'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.largest_gift
                if ( n is not None and n>=5 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Donacion estrella plata'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.largest_gift
                if ( n is not None and n>=20 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Donacion estrella oro'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.largest_gift
                if ( n is not None and n>=50 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Donacion estrella platino'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.largest_gift
                if ( n is not None and n>=100 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

        elif (achiev.name == 'Donacion estrella diamante'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.largest_gift
                if ( n is not None and n>=500 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )


        elif (achiev.name == 'Donante'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                n = usr_stats.total_number_of_gifts
                if ( n is not None and n>=1 ):
                    new = UserAchievements(owner=usr,achievement=achiev)
                    new.save()
                    user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                    ret.append( (achiev, user_ach.date, True) )
                else:
                    ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )


        elif (achiev.name == 'Donante recurrente'):
            if not UserAchievements.objects.filter(owner=usr.id,achievement=achiev.name).exists():
                    f = 1
                    n_gifts = usr_stats.total_number_of_gifts
                    if(n_gifts==None):
                        f = 0
                    start = usr_stats.first_gift_date
                    if(start==None):
                        f = 0
                    last = date.today()
                    if(last==None):
                        f = 0
                    months = ((last - start).days)//30
                    if months == 0 :
                        f = 0
                    if(f==1 and n_gifts/months >= 1):
                        new = UserAchievements(owner=usr,achievement=achiev)
                        new.save()
                        user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                        ret.append( (achiev, user_ach.date, True) )
                    else:
                        ret.append( (achiev, None, False) )
            else:
                user_ach = UserAchievements.objects.get(owner=usr.id,achievement=achiev.name)
                ret.append( (achiev, user_ach.date, True) )

    ret2 = []

    for i in range(len(ret)):
        ret2.append( (ret[i][0], ret[i][1], ret[i][2], "../../" + ret[i][0].picture.url) )

    ret2.sort(key=lambda x:x[0].level, reverse=True)

    if ( usr_info.picture != None ):
        pic = ProfilePicture.objects.get(id=usr_info.picture.id)
        ret_pic = ( "/"+ pic.picture.url , True, pic.id )
    else:
        ret_pic = ( "" , False , -1)


    args = {
                'achievs':ret2,
                'user_stats':usr_stats, 
                'User_information':usr_info,
                'pic': ret_pic
            }

    return render(request, 'dashboard/user_achievements.html', args)

@login_required
def user_achievs(request, username):

    if request.user.username != username:
        return redirect('home')

    usr = get_object_or_404(User, username=username)
    user_info = get_object_or_404(UserInformation,  email=usr.email)

    return render(request, 'dashboard/user_achievements.html', {'User_information': user_info})

