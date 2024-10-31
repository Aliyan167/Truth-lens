from django.contrib import admin
from .models import TeamMember, Rank

# Register your models here.
class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [TeamMemberInline]

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'created_at', 'updated_at')
