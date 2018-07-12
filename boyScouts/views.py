from django.shortcuts import render
from django.shortcuts import HttpResponse , reverse , redirect, get_object_or_404
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import models

from . import forms

#helper functions

def getUserGroup(user):
    try:
        return models.Group_User.objects.get(user=user)
    except models.Group_User.DoesNotExist:
        return None




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
            return redirect(reverse('unitSelection'))
        else:
            error = "Invalid username or password"
            ContexDictionary ={'Login_Form':form,'error': error}
            return render(request,'boyScouts/login.html', ContexDictionary)
    ContexDictionary ={'Login_Form':form}
    return render(request,'boyScouts/login.html', ContexDictionary)



def unitSelection(request):
    userGroup = getUserGroup(request.user)# get user group 
    if userGroup == None:
        return HttpResponse("You Don't have any assigned group, please contact your admin.")

    return  render(request,'boyScouts/unitSelection.html', context={'groupObject':userGroup})


def scoutsList(request):
    userGroup = getUserGroup(request.user)# get user group 
    if userGroup == None:
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    

    scouts = models.Scout.objects.all().filter(group= userGroup.group )
    return  render(request,'boyScouts/scoutList.html', context={'scoutList':scouts})



def scoutDetails(request,id):
    userGroup = getUserGroup(request.user)# get user group 
    if userGroup == None:
        return HttpResponse("You Don't have any assigned group, please contact your admin.")

    rankFormSet = formset_factory(forms.Scout_Ranked_Badge_Form)
    proficiencyFormSet = formset_factory(forms.Scout_Proficiency_Badge_Form)

    admissionForm = forms.Scout_Form(instance=models.Scout.objects.get(id=id))
    for field in admissionForm.fields:
        admissionForm.fields[field].disabled = True
    rankFormSet = rankFormSet(prefix="rank") 
    proficiencyFormSet = proficiencyFormSet(prefix="proficiency")
    
    return  render(request,'boyScouts/scoutDetails.html',context={'admissionForm':admissionForm,'rankFormSet':rankFormSet,'proficiencyFormSet':proficiencyFormSet})
    



def admission(request):
    userGroup = getUserGroup(request.user)# get user group 
    if userGroup == None:
        return HttpResponse("You Don't have any assigned group, please contact your admin.")

    rankFormSet = formset_factory(forms.Scout_Ranked_Badge_Form)
    proficiencyFormSet = formset_factory(forms.Scout_Proficiency_Badge_Form)


    if request.method == 'POST':
        print('\n')
        for values in request.POST:
            print(values , request.POST[values])
        print('\n')
        # admissionForm
        postData = request.POST.copy()#making copy to add group details in it
        postData['group']= userGroup.id
        admissionForm = forms.Scout_Form(postData)

        print(admissionForm.data)
        # rankFormSet
        rankFormSet = rankFormSet(request.POST,prefix="rank")
        # proficiency Form
        proficiencyFormSet = proficiencyFormSet(request.POST,prefix="proficiency")

        if admissionForm.is_valid() and rankFormSet.is_valid() and proficiencyFormSet.is_valid():
            print("AdmissionForm is valid!")
            print("RankFormset is valid!")
            print("RankFormset is valid!\n")
            newScout = admissionForm.save()
            print("New Scout: ",newScout)
            for form in rankFormSet:
                cleanedData = form.cleaned_data
                if cleanedData != {}:
                    cleanedData['scout'] = newScout
                    modelObject = models.Scout_Ranked_Badge.objects.create(**cleanedData)
                    print(modelObject)
            for form in proficiencyFormSet:
                cleanedData = form.cleaned_data
                if cleanedData != {}:
                    cleanedData['scout'] = newScout
                    modelObject = models.Scout_Proficiency_Badge.objects.create(**cleanedData)
            return HttpResponse("Saved")

        else:
            admissionForm.fields['group'].disabled = True
            return render(request,'boyScouts/admissionForm.html',context={'admissionForm':admissionForm,'rankFormSet':rankFormSet,'proficiencyFormSet':proficiencyFormSet})
    admissionForm = forms.Scout_Form(initial={'group':userGroup})
    admissionForm.fields['group'].disabled = True
    rankFormSet = rankFormSet(prefix="rank") 
    proficiencyFormSet = proficiencyFormSet(prefix="proficiency")
    
    return  render(request,'boyScouts/admissionForm.html',context={'admissionForm':admissionForm,'rankFormSet':rankFormSet,'proficiencyFormSet':proficiencyFormSet})
    

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