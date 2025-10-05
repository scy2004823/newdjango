from django.db import models
from users.models import User 

class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_spent = models.DurationField()  # store time spent in a day
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=2)  # store sleep hours
    steps_taken = models.IntegerField()  # store steps taken
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user