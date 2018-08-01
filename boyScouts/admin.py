from django.contrib import admin
from . import models


#admin.site.register(models.Scout)
admin.site.register(models.Section)
admin.site.register(models.Scout_Rank_Badge)
admin.site.register(models.Scout_Proficiency_Badge)
admin.site.register(models.Badge)
admin.site.register(models.Group)
admin.site.register(models.Badge_Category)
admin.site.register(models.Group_User)

# Register your models here.
"""
class ScoutRankBadgesInline(admin.StackedInline):
    model = models.Scout_Ranked_Badge
    verbose_name = 'Ranked Badges Earned'
    extra = 1
    

class ScoutProficiencyBadgesInline(admin.StackedInline):
    model = models.Scout_Ranked_Badge
    verbose_name = 'Proficiency Badges Earned'
    extra = 1
    
"""

@admin.register(models.Scout)
class ScoutListView(admin.ModelAdmin):
    list_display = ['name','group','section','dateOfJoining']
    list_filter = ['group','section','dateOfJoining']
    fieldsets = ()
    list_per_page = 3
    admin.ModelAdmin.search_fields =['name','group__name','section__name']
    #inlines = [ScoutRankBadgesInline,ScoutProficiencyBadgesInline]