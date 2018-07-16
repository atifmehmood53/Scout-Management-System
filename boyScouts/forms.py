from django import forms 
from . import models


class Login_Form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label='ID')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}),label='Password')
    

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
    class Meta:
        model = models.Scout
        fields = '__all__'
        widgets ={
            'group':forms.Select({'class' : 'form-control field ',}),
            'section':forms.Select({'class' : 'form-control field ',}),
            'name' : forms.TextInput({'class' : 'form-control field ','placeholder':'Scout Name',}),
            'dateOfBirth' :  forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd','data-toggle':"datepicker"}),
            'dateOfJoining' :  forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd','data-toggle':"datepicker"}),
            'highestScoutingQualification' : forms.TextInput({'class' : 'form-control field ','placeholder':'Qualification'}),
            'image' : forms.FileInput({'class' : 'form-control field ',}),
        }

class Scout_Ranked_Badge_Form(forms.Form):
    #have to work on section
    badge = forms.ModelChoiceField(models.Badge.objects.filter(category__name ='Rank Badge',),to_field_name="name",widget=forms.Select({'class' : 'form-control field ',}))
    dateOfPassing= forms.DateField(widget= forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd'}),required=True)


class Scout_Proficiency_Badge_Form(forms.Form):
    badge = forms.ModelChoiceField(models.Badge.objects.filter(category__name ='Proficiency Badge'),widget=forms.Select({'class' : 'form-control field ',}))
    dateOfPassing = forms.DateField(widget= forms.DateInput({'class' : 'form-control field date','placeholder':'yyyy-mm-dd'}),)
    certificateNo =  forms.CharField(max_length=4,widget= forms.TextInput({'class' : 'form-control field ','placeholder':'Certificate #'}),required=True)


"""
class admissionForm(forms.ModelForm):
    class Meta:
        #model = models.Student
        fields ='__all__'
        widgets = {
            'name' : forms.TextInput({'class' : 'form-control field ',}),
            'fatherName': forms.TextInput({'class' : 'form-control field ',}),
            'dateOFBirth': forms.DateInput({'class' : 'form-control field ',}),
            'contactNumber' :  forms.TextInput({'class' : 'form-control field ',}),
            'cnic' : forms.TextInput({'class' : 'form-control field ',}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control '}),
            'secularEducation' : forms.Select({'class' : 'form-control field ',},choices=((1,'school'),(2,'matric'),(3,'intermediate'),(4,'Bachlors'),(5,'Master'),('6','PhD'))),
            'religiousEducation' : forms.TextInput({'class' : 'form-control field ',}),
            'bloodGroup' : forms.SelectMultiple({'class' : 'form-control field ',}),
            'residentialAddress' : forms.TextInput({'class' : 'form-control field ',}),
            'transferForm' : forms.TextInput({'class' : 'form-control field ',}),

        }
    
    # Badge Details 
    

   
    """