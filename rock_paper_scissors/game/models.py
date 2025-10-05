from django.db import models
from django.utils import timezone


class GameSession(models.Model):
    """Model to track individual game sessions and scores"""
    CHOICE_OPTIONS = [
        ('rock', 'Rock'),
        ('paper', 'Paper'),
        ('scissors', 'Scissors'),
    ]
    
    RESULT_OPTIONS = [
        ('win', 'Win'),
        ('lose', 'Lose'),
        ('draw', 'Draw'),
    ]
    
    player_choice = models.CharField(max_length=10, choices=CHOICE_OPTIONS)
    computer_choice = models.CharField(max_length=10, choices=CHOICE_OPTIONS)
    result = models.CharField(max_length=10, choices=RESULT_OPTIONS)
    played_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-played_at']
    
    def __str__(self):
        return f"Player: {self.player_choice} vs Computer: {self.computer_choice} = {self.result}"


class GameStatistics(models.Model):
    """Model to track overall game statistics"""
    total_games = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Game Statistics"
    
    def __str__(self):
        return f"Total: {self.total_games} | Wins: {self.wins} | Losses: {self.losses} | Draws: {self.draws}"
    
    @property
    def win_percentage(self):
        if self.total_games == 0:
            return 0
        return round((self.wins / self.total_games) * 100, 1)
