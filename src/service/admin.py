from django.contrib import admin
from .models import Service, ServiceCategory
# Register your models here.

class SkillInline(admin.TabularInline):
    model = Service.skills.through
    extra = 1

class TechnologyInline(admin.TabularInline):
    model = Service.technologies.through
    extra = 1

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    inlines = [SkillInline, TechnologyInline]