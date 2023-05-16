from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

@api_view(['POST'])
def registration_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password.'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({'success': 'User registered successfully.'}, status=201)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials.'}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }, status=200)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from api.models import Note
from api.serializers import NoteSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note_view(request):
    # Extract the title and content from the request data
    title = request.data.get('title')
    content = request.data.get('content')

    if not title or not content:
        return Response({'error': 'Please provide both title and content.'}, status=400)

    # Create the note and associate it with the authenticated user
    note = Note.objects.create(user=request.user, title=title, content=content)
    serializer = NoteSerializer(note)

    return Response({'success': 'Note created successfully.', 'note': serializer.data}, status=201)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found.'}, status=404)

    title = request.data.get('title')
    content = request.data.get('content')

    if not title or not content:
        return Response({'error': 'Please provide both title and content.'}, status=400)

    note.title = title
    note.content = content
    note.save()

    return Response({'success': 'Note updated successfully.'}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_note_view(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found.'}, status=404)

    note.delete()
    return Response({'success': 'Note deleted successfully.'}, status=200)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from api.models import Note
from api.serializers import NoteSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_notes_view(request):
    user = request.user
    notes = Note.objects.filter(user=user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from api.models import Note
from api.serializers import NoteSerializer
from rest_framework.permissions import IsAdminUser

@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_users_notes_view(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)



