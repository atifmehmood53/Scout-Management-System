from django.contrib import admin
from . import models


admin.site.register(models.Scout)
admin.site.register(models.Section)
admin.site.register(models.Scout_Ranked_Badge)
admin.site.register(models.Scout_Proficiency_Badge)
admin.site.register(models.Badge)
admin.site.register(models.Group)
admin.site.register(models.Badge_Category)
admin.site.register(models.Group_User)

# Register your models here.
