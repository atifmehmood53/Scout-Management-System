from django.shortcuts import render
from django.shortcuts import HttpResponse , reverse , redirect, get_object_or_404
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from . import models
from . import forms
def getUserGroup(user):
    if user.is_superuser:
        return 'superuser'

    try:
        return models.Group_User.objects.get(user=user)
    except models.Group_User.DoesNotExist:
        return None




def getSections(userGroup):
    if userGroup != 'superuser':
        return [userGroup.section]
    return models.Section.objects.all()


def filterBadgeToUser(userGroup, badgeFormset):
    for i in badgeFormset.forms:
        q = i.fields['badge'].queryset
        i.fields['badge'].queryset = q.filter(section = userGroup.section)



def adminScoutDetails(request,id):
    rankFormSet = formset_factory(forms.Scout_Ranked_Badge_Form,)
    proficiencyFormSet = formset_factory(forms.Scout_Proficiency_Badge_Form)
    instance=models.Scout.objects.get(id=id)





    proficiencyBadges = models.Scout_Proficiency_Badge.objects.filter(scout = instance)
    rankedBadges = models.Scout_Ranked_Badge.objects.filter(scout = instance)
    rankFormSet = rankFormSet(prefix="rank") 
    proficiencyFormSet = proficiencyFormSet(prefix="proficiency")
    
    return  render(request,'boyScouts/scoutDetails.html',context={'sections':getSections('superuser'),'instance':instance,'rankFormSet':rankFormSet,'proficiencyFormSet':proficiencyFormSet,'proficiencyBadges':proficiencyBadges,'rankedBadges':rankedBadges})
    