

from django.shortcuts import render
from django.shortcuts import HttpResponse , reverse , redirect, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms import formset_factory, inlineformset_factory
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

from django.db.models import Count
from boyScouts import models


from boyScouts import forms

from boyScouts.helpers import  *
#from  .test import * 
        


@login_required(login_url='/login')
def profile(request):
    ScoutFilterForm = forms.ScoutFilterForm()
    if request.user.is_superuser:
        return  render(request,'AdminApp/profile.html', context={'sections':getSections('superuser'),'ScoutFilterForm':ScoutFilterForm})
    return HttpResponse("you are not authorized to this view.")




@login_required(login_url='/login')
def scoutsList(request,id):
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    #filter = forms.ScoutFilterForm()
    scouts = models.Scout.objects.all().filter(section_id = id)
    #if request.method == 'POST':
    #    filter = forms.ScoutFilterForm(request.POST)
    #    scouts = filter.getFilteredQuery(scouts)

    #deletion logic --------x
    if 'deleteSelected' in request.GET:
        dict = []
        for key in request.GET:
            if key.__contains__('delete_'):
                dict.append(int(key.split('_')[1]))
        print(dict)
        models.Scout.objects.filter(pk__in=dict).delete()
    #end deletion logic -----x 

    filter = forms.ScoutFilterForm(request.GET)
    scouts = filter.getFilteredQuery(scouts)
    
    scouts = scouts.annotate(number_of_rank=Count('scout_rank_badge',distinct=True)).annotate(number_of_proficiency=Count('scout_proficiency_badge',distinct=True))
    #pagination 
    paginator = Paginator(scouts, 25)
    page = request.GET.get('page')
    scouts = paginator.get_page(page)
    return  render(request,'AdminApp/scoutList.html', context={'scoutList':scouts,'sections':getSections('superuser'),'category':models.Section.objects.get(id = id),'filter':filter})




@login_required(login_url='/login')
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
            Scout = scoutForm.save()
            try:
                scoutFiles(request,Scout)
                print('called')
                message = "Updated successfully."
                scoutForm.save()
            except:
                message = 'an error occured while uploading files.'
    return  render(request,'AdminApp/scoutDetails.html',context={'sections':getSections('superuser'),'instance':instance,'scoutForm':scoutForm,'rankBadges':rankBadges,'proficiencyBadges':proficiencyBadges,'message':message})
    



@login_required(login_url='/login')
def admission(request):
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
 
    print(request.POST)
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    admissionForm = forms.Scout_Form('superuser')
    if request.method == 'POST':
        # admissionForm
        admissionForm = forms.Scout_Form('superuser',request.POST)
        if admissionForm.is_valid() :
            newScout = admissionForm.save(commit=False)#not save to database
            admissionForm = forms.Scout_Form('superuser')
            #return redirect(reverse('AdminApp:editScoutBadges',args=[newScout.id]))
            try:
                scoutFiles(request,newScout)
            except:
                return render(request,'AdminApp/admissionForm.html',context={'sections':getSections('superuser'),'admissionForm':admissionForm,'error':'an error occured while uploading files'})
            newScout.save()
            return render(request,'AdminApp/admissionForm.html',context={'sections':getSections('superuser'),'admissionForm':admissionForm,'message':reverse('AdminApp:editScoutBadges',args=[newScout.id])})

    return  render(request,'AdminApp/admissionForm.html',context={'sections':getSections('superuser'),'admissionForm':admissionForm})


@login_required(login_url='/login')
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
    

@login_required(login_url='/login')
def addBadges(request):
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    context={'sections':getSections('superuser')}
    if request.method == 'POST':
        badgeForm = forms.BadgeForm(request.POST)
        print(request.POST,badgeForm.is_valid())
        if not badgeForm.is_valid():
            context['badgeForm'] = badgeForm
            
            return render(request,'AdminApp/badgeForm.html',context=context)
        else:
            badgeForm.save()
            context['message'] = 'Badge was added successfully.'
    badgeForm = forms.BadgeForm
    context['badgeForm'] = badgeForm
    return render(request,'AdminApp/badgeForm.html',context=context)


@login_required(login_url='/login')
def displayBadges(request,category,section_id):
    if not request.user.is_superuser :
        return HttpResponse("You Don't have any assigned group, please contact your admin.")
    print(category,category == 'RB',section_id)
    context={'sections':getSections('superuser')}

    errorslist = []
    



    #deletion logic --------x
    if 'deleteSelected' in request.GET:
        dict = []
        for key in request.GET:
            if key.__contains__('delete_'):
                dict.append(int(key.split('_')[1]))
        print(dict)
        for badge in dict:
            instance = models.Badge.objects.get(id=int(badge))
            print(instance)
            try:
                instance.delete()
            except:
                errorslist.append(instance.name)
        #models.Badge.objects.filter(pk__in=dict).delete()
    #end deletion logic -----x 


    """
    if request.method == 'POST':
        print(request.method)
        dict = request.POST.copy()
        del dict['csrfmiddlewaretoken']        
        for badge in dict:
            
            instance = models.Badge.objects.get(id=int(badge))
            print(instance)
            try:
                instance.delete()
            except:
                errorslist.append(instance.name)
    """

    context['errorslist'] = errorslist
    badges = None
    queryset = models.Badge.objects.filter(section = section_id)
    if category == 'PB':
        queryset = queryset.filter(category='PB')
        
    elif category == 'RB':
        queryset = queryset.filter(category='RB')
    #pagintor
    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    context['badges']= queryset
    return render(request,'AdminApp/displayBadges.html',context=context)


    
@login_required(login_url='/login')
def approveBadges(request, badge_category):
    context={'sections':getSections('superuser')}
    #filter = forms.approveBadgeFilterForm()
    if badge_category == 'RB':
        querySet = models.Scout_Rank_Badge.objects.filter(badge__approval_required=True,is_approved= False)
    elif badge_category == 'PB':
        querySet = models.Scout_Proficiency_Badge.objects.filter(badge__approval_required=True,is_approved= False)
    #appling filters
    filter = forms.approveBadgeFilterForm(request.GET)
    querySet = filter.getFilteredQuery(querySet)

    if 'update' in request.GET:
        #print(request.GET)
        delete = []
        approve = []
        for key in request.GET:
            if key.__contains__('delete_'):
                delete.append(int(key.split('_')[1]))
            elif key.__contains__('approve_'):
                approve.append(int(key.split('_')[1]))
        if badge_category == 'RB':
            models.Scout_Rank_Badge.objects.filter(pk__in=delete).delete()
            models.Scout_Rank_Badge.objects.filter(pk__in=approve).update(is_approved= True)
        elif badge_category == 'PB':
             models.Scout_Proficiency_Badge.objects.filter(pk__in=delete).delete()
             models.Scout_Proficiency_Badge.objects.filter(pk__in=approve).update(is_approved= True)
        print(
            "Approve:", approve,
            "Delete" , delete,
            )
        

    """
        if request.method == 'POST':
            filter = forms.approveBadgeFilterForm(request.POST)
            querySet = filter.getFilteredQuery( querySet)
            print(request.POST)
            dict = request.POST.copy()
            del dict['csrfmiddlewaretoken']
            print(dict)
            for i in dict:
                instance = i.split('_')
                if badge_category == 'RB':
                    if instance[0]=='delete':
                        models.Scout_Rank_Badge.objects.filter(id=str(instance[1])).delete()
                    elif instance[0]=='approve':
                        models.Scout_Rank_Badge.objects.filter(id=str(instance[1])).update(is_approved= True)
                elif badge_category == 'PB':
                    if instance[0]=='delete':
                        models.Scout_Proficiency_Badge.objects.filter(id=str(instance[1])).delete()
                    if instance[0]=='approve':
                        models.Scout_Proficiency_Badge.objects.filter(id=str(instance[1])).update(is_approved= True)
         print('ok') 
     """     


    paginator = Paginator(querySet, 25)
    page = request.GET.get('page')
    querySet = paginator.get_page(page)
    context['filter'] = filter
    context['badges'] = querySet

    return render(request,'AdminApp/approveBadges.html',context=context)




#drive test

def driveTest(request):
    form = forms.fileForm()
    #print(service.files().list().execute())
    print(service.files().list(pageSize=10, fields="nextPageToken, files(id, name, webContentLink)").execute())
    if request.method == 'POST':
        media = MediaInMemoryUpload(request.FILES['file'].read())
        object = service.files().create(body={'name': 'photo.jpg'},
                                    media_body=media,
                                    fields='id, webContentLink',).execute()
        print("Object url",object['webContentLink'])
        
    return render(request,'driveTest.html',context={'form':form})