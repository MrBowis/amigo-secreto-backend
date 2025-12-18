from rest_framework import serializers
from .models import SecretSantaEvent, Participant, Assignment
import random


class ParticipantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Participant
        fields = ['id', 'name', 'email']


class AssignmentSerializer(serializers.ModelSerializer):
    giver_id = serializers.IntegerField(source='giver.id', read_only=True)
    receiver_id = serializers.IntegerField(source='receiver.id', read_only=True)
    
    class Meta:
        model = Assignment
        fields = ['giver_id', 'receiver_id']


class SecretSantaEventSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)
    is_drawn = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = SecretSantaEvent
        fields = ['id', 'name', 'created_by', 'participants', 'assignments', 'is_drawn', 'created_at']
        read_only_fields = ['created_at', 'is_drawn']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        event = SecretSantaEvent.objects.create(**validated_data)
        
        for participant_data in participants_data:
            Participant.objects.create(event=event, **participant_data)
        
        return event


class DrawSerializer(serializers.Serializer):
    """Serializer for performing the secret santa draw"""
    
    def perform_draw(self, event):
        """Generate random assignments for the secret santa event"""
        participants = list(event.participants.all())
        
        if len(participants) < 2:
            raise serializers.ValidationError("Se necesitan al menos 2 participantes para realizar el sorteo")
        
        # Delete existing assignments
        Assignment.objects.filter(event=event).delete()
        
        # Create a valid assignment (no one gets themselves)
        receivers = participants.copy()
        random.shuffle(receivers)
        
        # Ensure no one gets themselves
        max_attempts = 100
        for attempt in range(max_attempts):
            valid = True
            for i, giver in enumerate(participants):
                if giver.id == receivers[i].id:
                    valid = False
                    break
            
            if valid:
                break
            
            random.shuffle(receivers)
        else:
            # If we couldn't find a valid arrangement, use a derangement algorithm
            receivers = self._derangement(participants)
        
        # Create assignments
        assignments = []
        for giver, receiver in zip(participants, receivers):
            assignment = Assignment.objects.create(
                event=event,
                giver=giver,
                receiver=receiver
            )
            assignments.append(assignment)
        
        # Mark event as drawn
        event.is_drawn = True
        event.save()
        
        return assignments
    
    def _derangement(self, participants):
        """Generate a derangement (permutation where no element appears in its original position)"""
        n = len(participants)
        result = participants.copy()
        
        for i in range(n):
            # Find a valid swap partner
            for j in range(i + 1, n):
                if result[i].id != participants[j].id and result[j].id != participants[i].id:
                    result[i], result[j] = result[j], result[i]
                    break
        
        return result
