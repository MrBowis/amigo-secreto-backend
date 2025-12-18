from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import SecretSantaEvent, Participant, Assignment
from .serializers import SecretSantaEventSerializer, DrawSerializer
from .email_service import send_secret_santa_assignment_email, send_draw_completed_email


class SecretSantaEventViewSet(viewsets.ModelViewSet):
    queryset = SecretSantaEvent.objects.all()
    serializer_class = SecretSantaEventSerializer

    def get_queryset(self):
        """Filter events by created_by if user parameter is provided"""
        queryset = SecretSantaEvent.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(created_by=user_id)
        return queryset

    @action(detail=True, methods=['post'])
    def draw(self, request, pk=None):
        """Perform the secret santa draw for an event"""
        event = self.get_object()
        
        if event.is_drawn:
            return Response(
                {'error': 'El sorteo ya ha sido realizado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        draw_serializer = DrawSerializer()
        try:
            assignments = draw_serializer.perform_draw(event)
            event.refresh_from_db()
            
            # Send emails to all participants
            send_emails = request.data.get('send_emails', True)
            if send_emails:
                emails_sent = 0
                for assignment in assignments:
                    success = send_secret_santa_assignment_email(
                        participant_name=assignment.giver.name,
                        participant_email=assignment.giver.email,
                        receiver_name=assignment.receiver.name,
                        event_name=event.name,
                        event_id=event.id
                    )
                    if success:
                        emails_sent += 1
                
                # Optionally notify creator (would need to store creator email)
                # send_draw_completed_email(creator_email, event.name, len(assignments))
            
            serializer = self.get_serializer(event)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def by_participant(self, request):
        """Get events where the email is a participant"""
        email = request.query_params.get('email')
        
        if not email:
            return Response(
                {'error': 'Email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find participants with this email
        participants = Participant.objects.filter(email=email)
        event_ids = participants.values_list('event_id', flat=True).distinct()
        
        # Get the events
        events = SecretSantaEvent.objects.filter(id__in=event_ids, is_drawn=True)
        
        # For each event, only return the assignment for this participant
        result = []
        for event in events:
            participant = participants.filter(event=event).first()
            if participant:
                assignment = Assignment.objects.filter(
                    event=event, 
                    giver=participant
                ).select_related('receiver').first()
                
                event_data = {
                    'id': event.id,
                    'name': event.name,
                    'created_at': event.created_at,
                    'participant': {
                        'id': participant.id,
                        'name': participant.name,
                        'email': participant.email
                    },
                    'assignment': {
                        'receiver_id': assignment.receiver.id,
                        'receiver_name': assignment.receiver.name,
                        'receiver_email': assignment.receiver.email
                    } if assignment else None
                }
                result.append(event_data)
        
        return Response(result)

    @action(detail=True, methods=['get'])
    def participants_wishlists(self, request, pk=None):
        """Get all participants of an event with their wishlists"""
        event = self.get_object()
        email = request.query_params.get('email')
        
        # Verify the requester is a participant
        if email:
            is_participant = event.participants.filter(email=email).exists()
            if not is_participant:
                return Response(
                    {'error': 'No eres participante de este sorteo'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # Get all participants
        participants = event.participants.all()
        
        # Import here to avoid circular imports
        from wishlist.models import Wishlist
        
        result = []
        for participant in participants:
            participant_data = {
                'id': participant.id,
                'name': participant.name,
                'email': participant.email,
                'wishlist': None
            }
            
            # Try to find wishlist by email field first, then by user field
            try:
                wishlist = Wishlist.objects.filter(email=participant.email).first()
                if not wishlist:
                    # Fallback: search in user field (Firebase UID might contain email)
                    wishlist = Wishlist.objects.filter(user__icontains=participant.email).first()
                
                if wishlist:
                    participant_data['wishlist'] = {
                        'id': wishlist.id,
                        'items': [
                            {
                                'id': item.id,
                                'title': item.title,
                                'reference': item.reference
                            }
                            for item in wishlist.items.all()
                        ]
                    }
            except Exception as e:
                print(f"Error finding wishlist for {participant.email}: {str(e)}")
                pass
            
            result.append(participant_data)
        
        return Response(result)
