from django.contrib import admin
from .models import (
     Technology, Skill, Tag, Testimonials, ContactUs
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency_level', 'created_at')


admin.site.register(Testimonials)
admin.site.register(ContactUs)