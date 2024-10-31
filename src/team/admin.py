from django.contrib import admin
from .models import TeamMember, Rank, CEO

# Register your models here.
class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'created_at', 'updated_at')


admin.site.register(CEO)
