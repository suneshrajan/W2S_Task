import imp
from django.contrib import admin
from . models import *
# Register your models here.

# admin.site.register(UserProfile)
# admin.site.register(UserType)
admin.site.register(SkillCv)
# admin.site.register(UserSkills)

class EmployeeTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'percentage')
    list_filter = ('user', )
    save_as = True
    save_on_top = True
    change_list_template = 'task/change_list_graph.html'


admin.site.register(UserSkills, EmployeeTaskAdmin)