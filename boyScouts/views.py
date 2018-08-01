from django.shortcuts import render
from django.shortcuts import HttpResponse , reverse , redirect, get_object_or_404
from django.forms import formset_factory, inlineformset_factory
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from . import models
from . import forms
from .helpers import *

# Create your views here.
def loginView(request):
    form = forms.Login_Form()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username= username, password= password)
        if (user!=None):
            login(request,user)
            if 'next' in request.POST:
                #some way to send invalid details back
                return redirect(request.POST.get('next'))
            if user.is_superuser:
                return redirect(reverse('AdminApp:profile'))
            return redirect(reverse('boyScouts:profile'))
        else:
            error = "Invalid username or password"
            ContexDictionary ={'Login_Form':form,'error': error}
            return render(request,'boyScouts/login.html', ContexDictionary)
    ContexDictionary ={'Login_Form':form}
    return render(request,'boyScouts/login.html', ContexDictionary)

def logoutView(request):
    logout(request)
    return redirect(reverse('boyScouts:loginView'))




def profile(request):
    #profile
    userGroup = getUserGroup(request.user)# get user group 
    if userGroup == None:
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    return  render(request,'boyScouts/profile.html', context={'groupObject':userGroup,'sections':getSections(userGroup)})


def scoutsList(request,id):
    userGroup = getUserGroup(request.user)# get user group 
    if  userGroup==None :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    else:
        scouts = models.Scout.objects.all().filter(section_id = id, group= userGroup.group )
    scouts = scouts.annotate(number_of_rank=Count('scout_rank_badge',distinct=True)).annotate(number_of_proficiency=Count('scout_proficiency_badge',distinct=True))
    return  render(request,'boyScouts/scoutList.html', context={'scoutList':scouts,'sections':getSections(userGroup),'category':models.Section.objects.get(id = id)})




def scoutDetails(request,id):
    userGroup = getUserGroup(request.user)
    instance = models.Scout.objects.get(id=id)
    message = ""
    if userGroup == None :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    elif userGroup.group.id != instance.group.id or userGroup.section!= instance.section:
        return HttpResponse("You Don't have any assigned group, please contact your admin.")

    rankBadges = getScoutBadgePlaneList(instance,'RB')
    proficiencyBadges = getScoutBadgePlaneList(instance,'PB')

    return  render(request,'boyScouts/scoutDetails.html',context={'sections':getSections(userGroup),'instance':instance,'rankBadges':rankBadges,'proficiencyBadges':proficiencyBadges,'message':message})
    



def admission(request):
    userGroup = getUserGroup(request.user)# get user group 
    admissionForm = forms.Scout_Form(userGroup)
    if userGroup == None :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    
    if request.method == 'POST':
        # admissionForm
        admissionForm = forms.Scout_Form(userGroup,request.POST)
        print(admissionForm.data)
        if admissionForm.is_valid() :
            newScout = admissionForm.save()
            admissionForm = forms.Scout_Form(userGroup)
            return  redirect(reverse('boyScouts:editScoutBadges',args=[newScout.id]))
            return render(request,'boyScouts/admissionForm.html',context={'sections':getSections(userGroup),'admissionForm':admissionForm})

    
    
    return  render(request,'boyScouts/admissionForm.html',context={'sections':getSections(userGroup),'admissionForm':admissionForm})
    
def editScoutBadges(request,id):
    userGroup = getUserGroup(request.user)
    instance = models.Scout.objects.get(id=id)
    context={'sections':getSections(userGroup),'instance':instance}
    if userGroup == None :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    elif userGroup !='superuser' and (userGroup.group.id != instance.group.id or userGroup.section!= instance.section):
        return HttpResponse("You Don't have any assigned group, please contact your admin.")

    
    if request.method == 'POST':
        good = True
        rankFormsets = getScoutBadgeFormset(instance,userGroup,'RB',request=request)
        proficiencyFormsets = getScoutBadgeFormset(instance,userGroup,'PB',request=request)
        '''
        for formset in rankFormsets:
            if formset.is_valid():
                formset.save()
            else:   
                good = False
        for formset in proficiencyFormsets:
            if formset.is_valid():
                formset.save()
            else:   
                good = False
        '''
        context['rankFormsets']= rankFormsets
        context['proficiencyFormsets']= proficiencyFormsets
    else:
        context['rankFormsets']= getScoutBadgeFormset(instance,userGroup,'RB')
        context['proficiencyFormsets']= getScoutBadgeFormset(instance,userGroup,'PB')
    rankBadges = getScoutBadgePlaneList(instance,'RB')
    proficiencyBadges = getScoutBadgePlaneList(instance,'PB')
    context['rankBadges']= rankBadges
    context['proficiencyBadges'] =proficiencyBadges
    return render(request,'boyScouts/editBadges.html',context=context,)








def formset(request):
    if request.method == 'POST':
        print(request.POST)
        formset = formset_factory(forms.Scout_Ranked_Badge_Form)
        formset = formset(request.POST)
        if formset.is_valid():
           return HttpResponse("ok")
        
        return  render(request,'boyScouts/formset.html',context={'formset':formset})

    formset = formset_factory(forms.Scout_Ranked_Badge_Form,extra=3)
    return render(request,'boyScouts/formset.html',context={'formset':formset})






