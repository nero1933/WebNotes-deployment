from django.urls import path, include, re_path

from .views import *


urlpatterns = [
    path('', index, name='home'),

    path('private_notes/', PrivateNotes.as_view(), name='private_notes'),
    path('private_notes/<slug:username>/<slug:slug>/', ShowNote.as_view(), name='show_note'),
    path('private_notes/<slug:username>/<slug:slug>/update/', UpdatePrivateNote.as_view(), name='update_note'),
    path('private_notes/<slug:username>/<slug:slug>/delete/', DeletePrivateNote.as_view(), name='delete_note'),
    path('private_notes/delete_all_notes/', DeleteAllPrivateNotes.as_view(), name='delete_all_notes'),
    path('private_notes/add_note/', AddPrivateNote.as_view(), name='add_private_note'),

    path('private_folders/', AllFolders.as_view(), name='all_folders'),
    path('private_folders/<slug:username>/<slug:slug>/', ShowFolder.as_view(), name='show_folder'),
    path('private_folders/<slug:username>/<slug:slug>/delete/', DeleteFolder.as_view(), name='delete_folder'),
    path('private_folders/delete_all_folders/', DeleteAllFolders.as_view(), name='delete_all_folders'),
    path('add_private_folder/', AddFolder.as_view(), name='add_folder'),

    path('accounts/sign_in/', SignInUser.as_view(), name='sign_in'),
    path('accounts/login/', LoginUser.as_view(), name='login'),
    path('accounts/logout/', logout_user, name='logout'),
    path('accounts/<username>/', UserPage.as_view(), name='user'),
    path('accounts/<slug:username>/delete_user/', DeleteUser.as_view(), name='delete_user'),

    path('about_us/', about_us, name='about_us'),
    path('contact_us/', contact_us, name='contact_us'),
]

