from django.shortcuts import render
from django.shortcuts import HttpResponse , reverse , redirect, get_object_or_404
from django.forms import formset_factory, inlineformset_factory
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from boyScouts import models


from boyScouts import forms

from boyScouts.helpers import  *

        



def profile(request):
    if request.user.is_superuser:
        return  render(request,'AdminApp/profile.html', context={'sections':getSections('superuser')})
    return HttpResponse("you are not authorized to this view.")




def scoutsList(request,id):
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    else:
        scouts = models.Scout.objects.all().filter(section_id = id)
    scouts = scouts.annotate(number_of_rank=Count('scout_rank_badge',distinct=True)).annotate(number_of_proficiency=Count('scout_proficiency_badge',distinct=True))
    return  render(request,'AdminApp/scoutList.html', context={'scoutList':scouts,'sections':getSections('superuser'),'category':models.Section.objects.get(id = id)})




def scoutDetails(request,id):
    
    instance = models.Scout.objects.get(id=id)
    message = ""
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")

    rankBadges = getScoutBadgePlaneList(instance,'RB')
    proficiencyBadges = getScoutBadgePlaneList(instance,'PB')
    scoutForm = forms.Scout_Form('superuser',instance=instance)

    if request.method == 'POST':
        scoutForm = forms.Scout_Form('superuser',request.POST,instance=instance) 
        if scoutForm.is_valid():
            scoutForm.save()
            message = "Updated successfully."
    
    
    print(getScoutBadgePlaneList(instance,'RB'),getScoutBadgePlaneList(instance,'PB'))
    return  render(request,'AdminApp/scoutDetails.html',context={'sections':getSections('superuser'),'instance':instance,'scoutForm':scoutForm,'rankBadges':rankBadges,'proficiencyBadges':proficiencyBadges,'message':message})
    



def admission(request):
    
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    admissionForm = forms.Scout_Form('superuser')
    if request.method == 'POST':
        # admissionForm
        print(request.POST)
        admissionForm = forms.Scout_Form('superuser',request.POST)
        print(admissionForm.data)

        if admissionForm.is_valid() :
            newScout = admissionForm.save()
            admissionForm = forms.Scout_Form('superuser')
            return redirect(reverse('AdminApp:editScoutBadges',args=[newScout.id]))
            #return render(request,'AdminApp/admissionForm.html',context={'sections':getSections('superuser'),'admissionForm':admissionForm})

    return  render(request,'AdminApp/admissionForm.html',context={'sections':getSections('superuser'),'admissionForm':admissionForm})
    
def editScoutBadges(request,id):
    
    instance = models.Scout.objects.get(id=id)
    context={'sections':getSections('superuser'),'instance':instance}
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
 
    if request.method == 'POST':
        good = True
        rankFormsets = getScoutBadgeFormsetAdmin(instance,'RB',request=request)
        proficiencyFormsets = getScoutBadgeFormsetAdmin(instance,'PB',request=request)
        
        context['rankFormsets']= rankFormsets
        context['proficiencyFormsets']= proficiencyFormsets
    else:
        context['rankFormsets']= getScoutBadgeFormsetAdmin(instance,'RB')
        context['proficiencyFormsets']= getScoutBadgeFormsetAdmin(instance,'PB')

    rankBadges = getScoutBadgePlaneList(instance,'RB')
    proficiencyBadges = getScoutBadgePlaneList(instance,'PB')
    context['rankBadges']= rankBadges
    context['proficiencyBadges'] =proficiencyBadges
    return render(request,'AdminApp/editBadges.html',context=context)
    

def addBadges(request):
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    context={'sections':getSections('superuser')}
    if request.method == 'POST':
        badgeForm = forms.BadgeForm(request.POST)
        if not badgeForm.is_valid:
            context['badgeForm'] = badgeForm
            
            return render(request,'AdminApp/badgeForm.html',context=context)
        else:
            badgeForm.save()
            context['message'] = 'Badge was added successfully.'
    badgeForm = forms.BadgeForm
    context['badgeForm'] = badgeForm
    return render(request,'AdminApp/badgeForm.html',context=context)


def displayBadges(request,category,section_id):
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    print(category,category == 'RB',section_id)
    context={'sections':getSections('superuser')}
    badges = None
    queryset = models.Badge.objects.filter(section = section_id)
    if category == 'PB':
        queryset = queryset.filter(category='PB')
        
    elif category == 'RB':
        queryset = queryset.filter(category='RB')

    context['badges']= queryset
    return render(request,'AdminApp/displayBadges.html',context=context)

