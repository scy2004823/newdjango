from django.contrib import admin
from .models import GameSession, GameStatistics


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['player_choice', 'computer_choice', 'result', 'played_at']
    list_filter = ['result', 'player_choice', 'computer_choice', 'played_at']
    search_fields = ['player_choice', 'computer_choice']
    readonly_fields = ['played_at']
    ordering = ['-played_at']


@admin.register(GameStatistics)
class GameStatisticsAdmin(admin.ModelAdmin):
    list_display = ['total_games', 'wins', 'losses', 'draws', 'win_percentage']
    readonly_fields = ['win_percentage']
    
    def has_add_permission(self, request):
        # Only allow one statistics record
        return not GameStatistics.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of statistics
        return False
