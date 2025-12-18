from django.db import models

# Create your models here.

class SecretSantaEvent(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.CharField(max_length=255)  # Firebase UID
    is_drawn = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'secret_santa_events'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Participant(models.Model):
    event = models.ForeignKey(SecretSantaEvent, related_name='participants', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'participants'

    def __str__(self):
        return f"{self.name} ({self.event.name})"


class Assignment(models.Model):
    event = models.ForeignKey(SecretSantaEvent, related_name='assignments', on_delete=models.CASCADE)
    giver = models.ForeignKey(Participant, related_name='giving_to', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Participant, related_name='receiving_from', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'assignments'
        unique_together = ['event', 'giver']

    def __str__(self):
        return f"{self.giver.name} -> {self.receiver.name}"
