from django.contrib import admin
from .models import Project, ProjectTechnology, ProjectCategory

# Register your models here.

class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1



@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date', 'end_date', 'is_active')
    inlines = [ProjectTechnologyInline]