from django.urls import path
from api.views import registration_view, login_view
from api.views import registration_view, login_view, create_note_view, update_note_view, delete_note_view,user_notes_view,all_users_notes_view

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('notes/create/', create_note_view, name='create-note'),
    path('notes/<int:note_id>/update/', update_note_view, name='update-note'),
    path('notes/<int:note_id>/delete/', delete_note_view, name='delete-note'),
     # User's own notes
    path('api/user-notes/', user_notes_view, name='user-notes'),

    # Admin access to all users' notes
    path('api/all-users-notes/', all_users_notes_view, name='all-users-notes'),
]
