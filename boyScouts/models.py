from django.db import models
from django.contrib.auth import models as djangoModels

# Create your models here.



"""
class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    fatherName = models.CharField(max_length=50)
    dateOFBirth = models.DateField()
    contactNumber = models.CharField(max_length=11)
    cnic = models.CharField(max_length=14)
    email = models.EmailField()
    secularEducation = models.CharField(max_length =20) 
    religiousEducation =models.CharField(max_length=14)
    bloodGroup = models.CharField(max_length=30)
    residentialAddress = models.CharField(max_length=256)
    transferForm = models.CharField(max_length=256)
"""



class Group(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length = 3)
    address = models.CharField(max_length=256)
    email = models.EmailField()
    #gsl = models.CharField(max_length=30)
    contact = models.CharField(max_length=15)


    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Group_User(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    user = models.OneToOneField(djangoModels.User,on_delete=models.CASCADE)
    section = models.OneToOneField(Section,on_delete=models.CASCADE)




class Badge_Category(models.Model):
    name = models.CharField(max_length= 100)
    def __str__(self):
        return self.name



class Badge(models.Model):
    name = models.CharField(max_length= 100)
    category = models.ForeignKey(Badge_Category,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.section.name+" | "+self.name 

class Scout(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE) 
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,verbose_name="Name")
    dateOfBirth = models.DateField(verbose_name="Date Of Birth")
    dateOfJoining = models.DateField(verbose_name="Joining Date")
    highestScoutingQualification = models.CharField(max_length=50,verbose_name="Highest Scout Qualification")
    image = models.ImageField(blank=True, null=True)
    def __str__(self):
        return self.name




class Scout_Ranked_Badge(models.Model):
    scout = models.ForeignKey(Scout,on_delete = models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete = models.CASCADE)
    dateOfPassing = models.DateField()



    def __str__(self):
        return self.scout.name +" | "+self.badge.__str__()
    


class Scout_Proficiency_Badge(models.Model):
    scout = models.ForeignKey(Scout,on_delete = models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    dateOfPassing = models.DateField()
    certificateNo = models.CharField(max_length=4)
    
    def __str__(self):
        return self.scout.name +" | "+self.badge.__str__()
