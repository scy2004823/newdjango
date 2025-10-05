from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import GameSession, GameStatistics
import random
import json


def index(request):
    """Main game page"""
    # Get or create game statistics
    stats, created = GameStatistics.objects.get_or_create(pk=1)
    
    # Get recent games for display
    recent_games = GameSession.objects.all()[:5]
    
    context = {
        'stats': stats,
        'recent_games': recent_games,
    }
    return render(request, 'game/index.html', context)


def determine_winner(player_choice, computer_choice):
    """Determine the winner of the game"""
    if player_choice == computer_choice:
        return 'draw'
    
    winning_combinations = {
        'rock': 'scissors',
        'paper': 'rock', 
        'scissors': 'paper'
    }
    
    if winning_combinations[player_choice] == computer_choice:
        return 'win'
    else:
        return 'lose'


@csrf_exempt
def play_game(request):
    """Handle game play via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            player_choice = data.get('choice')
            
            if player_choice not in ['rock', 'paper', 'scissors']:
                return JsonResponse({'error': 'Invalid choice'}, status=400)
            
            # Generate computer choice
            computer_choice = random.choice(['rock', 'paper', 'scissors'])
            
            # Determine winner
            result = determine_winner(player_choice, computer_choice)
            
            # Save game session
            game_session = GameSession.objects.create(
                player_choice=player_choice,
                computer_choice=computer_choice,
                result=result
            )
            
            # Update statistics
            stats, created = GameStatistics.objects.get_or_create(pk=1)
            stats.total_games += 1
            
            if result == 'win':
                stats.wins += 1
            elif result == 'lose':
                stats.losses += 1
            else:
                stats.draws += 1
            
            stats.save()
            
            return JsonResponse({
                'player_choice': player_choice,
                'computer_choice': computer_choice,
                'result': result,
                'stats': {
                    'total_games': stats.total_games,
                    'wins': stats.wins,
                    'losses': stats.losses,
                    'draws': stats.draws,
                    'win_percentage': stats.win_percentage
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def autoplay_game(request):
    """Handle autoplay mode requests (computer vs computer)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rounds = data.get('rounds', 1)
            speed = data.get('speed', 1000)  # milliseconds between rounds
            
            # Limit rounds for performance
            if rounds > 100:
                rounds = 100
            
            valid_choices = ['rock', 'paper', 'scissors']
            results = []
            
            for _ in range(rounds):
                # Generate choices for both computers
                computer1_choice = random.choice(valid_choices)
                computer2_choice = random.choice(valid_choices)
                
                # Determine result from computer1's perspective
                result = determine_winner(computer1_choice, computer2_choice)
                
                # Save game session (treating computer1 as player)
                game_session = GameSession.objects.create(
                    player_choice=computer1_choice,
                    computer_choice=computer2_choice,
                    result=result
                )
                
                # Update statistics
                stats, created = GameStatistics.objects.get_or_create(pk=1)
                stats.total_games += 1
                
                if result == 'win':
                    stats.wins += 1
                elif result == 'lose':
                    stats.losses += 1
                else:
                    stats.draws += 1
                
                stats.save()
                
                results.append({
                    'computer1_choice': computer1_choice,
                    'computer2_choice': computer2_choice,
                    'result': result
                })
            
            # Get updated stats
            stats = GameStatistics.objects.get(pk=1)
            
            return JsonResponse({
                'rounds_played': rounds,
                'results': results,
                'stats': {
                    'total_games': stats.total_games,
                    'wins': stats.wins,
                    'losses': stats.losses,
                    'draws': stats.draws,
                    'win_percentage': stats.win_percentage
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def reset_stats(request):
    """Reset game statistics"""
    if request.method == 'POST':
        GameSession.objects.all().delete()
        stats, created = GameStatistics.objects.get_or_create(pk=1)
        stats.total_games = 0
        stats.wins = 0
        stats.losses = 0
        stats.draws = 0
        stats.save()
        
        return redirect('game:index')
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
