from django import forms 
from . import models
from django.contrib.auth import models as djangoModels

class Login_Form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label='ID')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}),label='Password')
    



class userForm(forms.ModelForm):
    class Meta:
        model = djangoModels.User
        fields = '__all__'



class admissionForm(forms.Form):
    name = forms.CharField(max_length=50,label='Name')
    fatherName = forms.CharField(max_length=50,label='Father Name')
    dateOFBirth = forms.DateField(label = 'Date of Birth')
    contactNumber = forms.CharField(max_length=11, label= 'Contact Number')
    cnic = forms.CharField(max_length=14,label='CNIC/Form.B #')
    email = forms.EmailField(label='Email')
    secularEducation = forms.ChoiceField(widget=forms.RadioSelect({'class' : 'form-control field ',}),choices=((1,'school'),(2,'matric'),(3,'intermediate'),(4,'Bachlors'),(5,'Master'),('6','PhD')))
    religiousEducation = forms.CharField(max_length=14,label='Religious Education')
    bloodGroup = forms.ChoiceField(label = 'Blood Group')
    residentialAddress = forms.CharField(max_length=256,label='Residential Address')
    transferForm = forms.CharField(max_length=256,label='Tranfer Form')
    # Badge Details 
    
class Scout_Form(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput({'class' : 'form-control field ',}),required=False)
    cnic = forms.ImageField(widget=forms.FileInput({'class' : 'form-control field ',}),required=False)

    def __init__(self,userGroup, *args, **kwargs):
        super().__init__(*args,**kwargs)
        
        if userGroup != 'superuser':
            self.fields['group'].initial = userGroup.group.id
            self.fields['group'].disabled = True
            self.fields['section'].initial = userGroup.section.id
            self.fields['section'].disabled = True
    class Meta:
        model = models.Scout
        fields = ['group','section','name','dateOfBirth','dateOfJoining','highestScoutingQualification',]
        widgets ={
            'group':forms.Select({'class' : 'form-control field ',}),
            'section':forms.Select({'class' : 'form-control field ',}),
            'name' : forms.TextInput({'class' : 'form-control field ','placeholder':'Scout Name',}),
            'dateOfBirth' :  forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd','data-toggle':"datepicker"}),
            'dateOfJoining' :  forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd','data-toggle':"datepicker"}),
            'highestScoutingQualification' : forms.TextInput({'class' : 'form-control field ','placeholder':'Qualification'}),
            #'image' : forms.FileInput({'class' : 'form-control field ',}),
        }
     


class Scout_Rank_Badge_FormAdmin(forms.ModelForm):
    def __init__(self,scoutSection,badgeCategory, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.category = badgeCategory
        self.section = scoutSection
        
       
    def reset(self):
        self.fields['badge'].queryset = self.fields['badge'].queryset.filter(section=self.section,category=self.category) 


    class Meta:
        """Meta definition for Scout_Ranked_Badgeform."""

        model = models.Scout_Rank_Badge
        fields = ('dateOfPassing','badge','is_approved')
        widgets ={
            'dateOfPassing':forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd'}),
            'badge':forms.Select({'class' : 'form-control field ',}),
            'is_approved':forms.CheckboxInput({'label':'approved'})
        }


class Scout_Proficiency_Badge_FormAdmin(forms.ModelForm):
    def __init__(self,scoutSection,badgeCategory, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.category = badgeCategory
        self.section = scoutSection
        
       
    def reset(self):
        print("OLD Query",self.fields['badge'].queryset)
        self.fields['badge'].queryset = self.fields['badge'].queryset.filter(section=self.section,category=self.category) 
        print("New Query",self.fields['badge'].queryset)


    class Meta:
        """Meta definition for Scout_Ranked_Badgeform."""

        model = models.Scout_Proficiency_Badge
        fields = ('dateOfPassing','badge','certificateNo','is_approved')
        widgets ={
            'dateOfPassing':forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd'}),
            'badge':forms.Select({'class' : 'form-control field ',}),
            'certificateNo':forms.TextInput({'class' : 'form-control field ','placeholder':'Certificate #',}),
        }



class Scout_Rank_Badge_Form(forms.ModelForm):
    def __init__(self,scoutSection,badgeCategory, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.category = badgeCategory
        self.section = scoutSection
        
       
    def reset(self):
        self.fields['badge'].queryset = self.fields['badge'].queryset.filter(section=self.section,category=self.category) 


    class Meta:
        """Meta definition for Scout_Ranked_Badgeform."""

        model = models.Scout_Rank_Badge
        fields = ('dateOfPassing','badge')
        widgets ={
            'dateOfPassing':forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd'}),
            'badge':forms.Select({'class' : 'form-control field ',}),
            
        }


class Scout_Proficiency_Badge_Form(forms.ModelForm):
    def __init__(self,scoutSection,badgeCategory, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.category = badgeCategory
        self.section = scoutSection
        
       
    def reset(self):
        print("OLD Query",self.fields['badge'].queryset)
        self.fields['badge'].queryset = self.fields['badge'].queryset.filter(section=self.section,category=self.category) 
        print("New Query",self.fields['badge'].queryset)


    class Meta:
        """Meta definition for Scout_Ranked_Badgeform."""

        model = models.Scout_Proficiency_Badge
        fields = ('dateOfPassing','badge','certificateNo')
        widgets ={
            'dateOfPassing':forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd'}),
            'badge':forms.Select({'class' : 'form-control field ',}),
            'certificateNo':forms.TextInput({'class' : 'form-control field ','placeholder':'Certificate #',}),
        }



class BadgeForm(forms.ModelForm):
    
    class Meta:
        model =models.Badge
        fields = '__all__'
        widgets ={
            'name':forms.TextInput({'class' : 'form-control field ','placeholder':'Badge Name',}),
            'category':forms.Select({'class' : 'form-control field ',}),
            'section':forms.Select({'class' : 'form-control field ',}),
        }


class ScoutFilterForm(forms.Form):
    group = forms.ModelChoiceField(models.Group.objects.all(),required=False,label='Group',widget=forms.Select({'class' : 'form-control field ','placeholder':'group'}),empty_label="All")
    name = forms.CharField(required=False,widget=forms.TextInput({'class' : 'form-control field ','placeholder':'Name',}))
    id = forms.IntegerField(required=False,widget=forms.TextInput({'class' : 'form-control field ','placeholder':'ID',}))

    def getFilteredQuery(self,querySet):
        self.is_valid()
        group = self.cleaned_data['group']
        name = self.cleaned_data['name']
        id = self.cleaned_data['id']
        print(group,name,id)
        
        if id:
            return querySet.filter(id=id)
        if not name =='' :
            querySet= querySet.filter(name__icontains=name)
        if group:
            querySet= querySet.filter(group_id=group)
        return querySet


class approveBadgeFilterForm(forms.Form):
    group = forms.ModelChoiceField(models.Group.objects.all(),required=False,label='Group',widget=forms.Select({'class' : 'form-control field ','placeholder':'group'}),empty_label="All")
    section = forms.ModelChoiceField(models.Section.objects.all(),required=False,label='Section',widget=forms.Select({'class' : 'form-control field ','placeholder':'group'}),empty_label="All")
    badge_name = forms.CharField(required=False,label='Badge Name',widget=forms.TextInput({'class' : 'form-control field ','placeholder':'Badge Name',}))
    scout_name = forms.CharField(required=False,label='Scout Name',widget=forms.TextInput({'class' : 'form-control field ','placeholder':'Scout Name',}))
    
    badge_id = forms.IntegerField(required=False,label='Badge ID',widget=forms.TextInput({'class' : 'form-control field ','placeholder':'Badge ID',}))
    scout_id = forms.IntegerField(required=False,label='Scout ID',widget=forms.TextInput({'class' : 'form-control field ','placeholder':'Scout ID',}))
    

    def getFilteredQuery(self,querySet):
        self.is_valid()
        group = self.cleaned_data['group']
        section = self.cleaned_data['section']
        badge_name = self.cleaned_data['badge_name']
        scout_name = self.cleaned_data['scout_name']
        scout_id = self.cleaned_data['scout_id']
        badge_id = self.cleaned_data['badge_id']
        print(group,section,badge_name,scout_name)
        
        if group:
            querySet.filter(scout__group_id = group )
        if section:
            querySet= querySet.filter(badge__section_id=section)
        if not badge_name=='':
            querySet= querySet.filter(badge__name__icontains=badge_name)
        if not scout_name == '':
            querySet= querySet.filter(scout__name__icontains=scout_name)
        if badge_id:
            querySet= querySet.filter(badge__id=badge_id)
        if scout_id:
            querySet= querySet.filter(scout__id=scout_id)
        return querySet



class fileForm(forms.Form):
    file = forms.FileField()