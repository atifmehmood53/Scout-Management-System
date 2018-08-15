from . import models
from . import forms
from django.forms import formset_factory, inlineformset_factory
from AdminApp.test import * 

#saves files
def scoutFiles(request,newScout):
    image = request.FILES.get('image')
    cnic = request.FILES.get('cnic')
    print(image,cnic)
    try:
        if image:
            image = image.read()
            oldImage = newScout.imageId
            Imagemedia = MediaInMemoryUpload(image)
            
            image = service.files().create(body={'name': newScout.name+' '+newScout.group.name,'parents': ['1VlH9g74D_Mw0tot53hDjOsXOsbwOhR_r']},
                                    media_body=Imagemedia,
                                    fields='id, webContentLink',).execute()
            
            try:
                if oldImage != None and oldImage != '':
                   service.files().delete(fileId=oldImage).execute()
            except:
                raise FileNotFoundError


            newScout.imageId = image['id']
            newScout.image = image['webContentLink']
                
                    
        if cnic: 
            oldCnic = newScout.cnicId
            print(oldCnic,"$$"*50)
            cnic = cnic.read()
            
            Cnicmedia = MediaInMemoryUpload(cnic)
            
            cnic = service.files().create(body={'name': newScout.name+' '+newScout.group.name,'parents': ['1VlH9g74D_Mw0tot53hDjOsXOsbwOhR_r']},
                                    media_body=Cnicmedia,
                                    fields='id, webContentLink',).execute()

            print(oldCnic,"$$"*50)
            try:
                if oldCnic != None and oldCnic != '':
                   service.files().delete(fileId=oldCnic).execute()
            except:
                raise FileNotFoundError
            newScout.cnicId = cnic['id']
            newScout.cnic = cnic['webContentLink']
    except:
        raise OSError



    
    

def getScoutBadgePlaneList(instance,category):
    lst = []
    section = instance.section
    count = 0
    while section:
        if category == 'RB':
            badgeList = models.Scout_Rank_Badge.objects.filter(scout=instance,badge__section=section)
        else:
            badgeList = models.Scout_Proficiency_Badge.objects.filter(scout=instance,badge__section=section)
        lst.append((section.name, badgeList))
        section = section.prerequisite
    return lst

def getScoutBadgeFormsetAdmin(instance,category,request=None):
    formsets =[]
    section = instance.section
    count = 0
    extra = 1
    while section:
        print(section,models.Scout_Rank_Badge.objects.filter(badge__section=section,badge__category='RB'))
        if category == 'RB':
            inlineFormSet = inlineformset_factory(models.Scout,models.Scout_Rank_Badge,forms.Scout_Rank_Badge_FormAdmin, extra=extra)
            prefix = 'RB_'+section.name
            if request == None:
                inlineFormSet = inlineFormSet(form_kwargs={'scoutSection':section,'badgeCategory':'RB'},prefix=prefix,instance=instance,queryset=models.Scout_Rank_Badge.objects.filter(badge__section=section,badge__category='RB'))
            else:
                inlineFormSet = inlineFormSet(request.POST,form_kwargs={'scoutSection':section,'badgeCategory':'RB'},prefix=prefix,instance=instance,queryset=models.Scout_Rank_Badge.objects.filter(badge__section=section,badge__category='RB'))
                if inlineFormSet.is_valid():
                    inlineFormSet.save()
                    inlineFormSet = inlineformset_factory(models.Scout,models.Scout_Rank_Badge,forms.Scout_Rank_Badge_FormAdmin, extra=extra)
                    inlineFormSet = inlineFormSet(form_kwargs={'scoutSection':section,'badgeCategory':'RB'},prefix=prefix,instance=instance,queryset=models.Scout_Rank_Badge.objects.filter(badge__section=section,badge__category='RB'))
 


        else:
            inlineFormSet = inlineformset_factory(models.Scout,models.Scout_Proficiency_Badge,forms.Scout_Proficiency_Badge_FormAdmin, extra=extra)
            prefix = 'PB_'+section.name
            if request == None:
                inlineFormSet = inlineFormSet(form_kwargs={'scoutSection':section,'badgeCategory':'PB'},prefix=prefix,instance=instance,queryset=models.Scout_Proficiency_Badge.objects.filter(badge__section=section,badge__category='PB'))
            else:
                inlineFormSet = inlineFormSet(request.POST,form_kwargs={'scoutSection':section,'badgeCategory':'PB'},prefix=prefix,instance=instance,queryset=models.Scout_Proficiency_Badge.objects.filter(badge__section=section,badge__category='PB'))
                if inlineFormSet.is_valid():
                    inlineFormSet.save()
                    print('valid')
                    inlineFormSet = inlineformset_factory(models.Scout,models.Scout_Proficiency_Badge,forms.Scout_Proficiency_Badge_FormAdmin, extra=extra)
                    inlineFormSet = inlineFormSet(form_kwargs={'scoutSection':section,'badgeCategory':'PB'},prefix=prefix,instance=instance,queryset=models.Scout_Proficiency_Badge.objects.filter(badge__section=section,badge__category='PB'))


        for form in inlineFormSet:
            form.reset()# not sure
            print('ok')
        formsets.append (inlineFormSet)
        section = section.prerequisite
        count+=1
    print(formsets)
    return formsets

def getScoutBadgeFormset(instance,userGroup,category,request=None):
    formsets =[]
    section = instance.section
    count = 0
    extra = 1
    while section:
        if userGroup.section.id == section.id:
         
            if category == 'RB':
                inlineFormSet = inlineformset_factory(models.Scout,models.Scout_Rank_Badge,forms.Scout_Rank_Badge_Form, extra=extra)
                prefix = 'RB_'+section.name
                if request == None:
                    inlineFormSet = inlineFormSet(form_kwargs={'scoutSection':section,'badgeCategory':'RB'},prefix=prefix,instance=instance,queryset=models.Scout_Rank_Badge.objects.filter(badge__section=section,badge__category='RB'))
                else:# save
                    inlineFormSet = inlineFormSet(request.POST,form_kwargs={'scoutSection':section,'badgeCategory':'RB'},prefix=prefix,instance=instance,queryset=models.Scout_Rank_Badge.objects.filter(badge__section=section,badge__category='RB'))
                    if inlineFormSet.is_valid():
                        inlineFormSet.save()
                        inlineFormSet = inlineformset_factory(models.Scout,models.Scout_Rank_Badge,forms.Scout_Rank_Badge_Form, extra=extra)
                        inlineFormSet = inlineFormSet(form_kwargs={'scoutSection':section,'badgeCategory':'RB'},prefix=prefix,instance=instance,queryset=models.Scout_Rank_Badge.objects.filter(badge__section=section,badge__category='RB'))
                    

            else:
                inlineFormSet = inlineformset_factory(models.Scout,models.Scout_Proficiency_Badge,forms.Scout_Proficiency_Badge_Form, extra=extra)
                prefix = 'PB_'+section.name
                if request == None:
                    inlineFormSet = inlineFormSet(form_kwargs={'scoutSection':section,'badgeCategory':'PB'},prefix=prefix,instance=instance,queryset=models.Scout_Proficiency_Badge.objects.filter(badge__section=section,badge__category='PB'))
                else:
                    inlineFormSet = inlineFormSet(request.POST,form_kwargs={'scoutSection':section,'badgeCategory':'PB'},prefix=prefix,instance=instance,queryset=models.Scout_Proficiency_Badge.objects.filter(badge__section=section,badge__category='PB'))
                    if inlineFormSet.is_valid():
                        inlineFormSet.save()
                        inlineFormSet = inlineformset_factory(models.Scout,models.Scout_Proficiency_Badge,forms.Scout_Proficiency_Badge_Form, extra=extra)
                        inlineFormSet = inlineFormSet(form_kwargs={'scoutSection':section,'badgeCategory':'PB'},prefix=prefix,instance=instance,queryset=models.Scout_Proficiency_Badge.objects.filter(badge__section=section,badge__category='PB'))

            for form in inlineFormSet:
                form.reset()
            formsets.append (inlineFormSet)
        section = section.prerequisite
        count+=1
    return formsets




def getUserGroup(user):
    
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
        print(q)
        i.fields['badge'].queryset = q.filter(section = userGroup.section)
    
def scoutBageFiter(instance,formset):
    for i in formset.forms:
        q = i.fields['badge'].queryset
        i.fields['badge'].queryset = q.filter(section = instance.section)

#user group