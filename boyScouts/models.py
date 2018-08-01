from django.db import models
from django.contrib.auth import models as djangoModels

# Create your models here.

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
    prerequisite = models.OneToOneField('self',on_delete=models.SET_NULL,null=True)
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

badge_categories = (
    ('PB', 'Proficiency Badge'),
    ('RB', 'Rank Badge'),
    )

class Badge(models.Model):
    name = models.CharField(max_length= 100,unique=True)
    category = models.CharField(max_length=30,choices=badge_categories)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name +' | '+ self.category+ ' | ' +  self.section.name





class Scout(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE) 
    section = models.ForeignKey(Section,on_delete=models.CASCADE,)
    name = models.CharField(max_length=50,verbose_name="Name")
    dateOfBirth = models.DateField(verbose_name="Date Of Birth")
    dateOfJoining = models.DateField(verbose_name="Joining Date")
    
    highestScoutingQualification = models.CharField(max_length=50,verbose_name="Highest Scout Qualification")
    image = models.ImageField(blank=True, null=True)
    def __str__(self):
        return self.name


class Scout_Rank_Badge(models.Model):
    badge = models.ForeignKey(Badge,on_delete=models.CASCADE)
    scout = models.ForeignKey(Scout,on_delete=models.CASCADE)
    dateOfPassing = models.DateField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.scout.name + ' | '+self.badge.section.name + ' | '+ self.badge.name 


class Scout_Proficiency_Badge(models.Model):
    badge = models.ForeignKey(Badge,on_delete=models.CASCADE)
    scout = models.ForeignKey(Scout,on_delete=models.CASCADE)
    dateOfPassing = models.DateField()
    certificateNo = models.CharField(max_length=4,blank=True)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
<<<<<<< HEAD
        return self.scout.name + ' | '+self.badge.section.name + ' | '+ self.badge.name 
=======
        return self.scout.name +" | "+self.badge.__str__()
>>>>>>> 92bc98177115a4856b65fefb17d26c25b1b7385e
