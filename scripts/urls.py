from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & logowanie
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Script
    path('add/', views.add_script, name='add_script'),
    path('edit/<int:script_id>/', views.edit_script, name='edit_script'),
    path('delete/<int:script_id>/', views.delete_script, name='delete_script'),
    path('view/<int:script_id>/', views.view_script, name='view_script'),
    path('choose/<int:script_id>/', views.choose_roles, name='choose_roles'),

    # Character
    path('character/add/', views.add_character, name='add_character'),
    path('character/edit/<int:character_id>/', views.edit_character, name='edit_character'),
    path('character/delete/<int:character_id>/', views.delete_character, name='delete_character'),

    # Scene
    path('scene/add/', views.add_scene, name='add_scene'),
    path('scene/edit/<int:scene_id>/', views.edit_scene, name='edit_scene'),
    path('scene/delete/<int:scene_id>/', views.delete_scene, name='delete_scene'),

    # SceneContent (kwestia)
    path('scenecontent/add/', views.add_scene_content, name='add_scene_content'),
    path('scenecontent/edit/<int:content_id>/', views.edit_scene_content, name='edit_scene_content'),
    path('scenecontent/delete/<int:content_id>/', views.delete_scene_content, name='delete_scene_content'),

    # Overlay
    path('overlay/add/', views.add_overlay, name='add_overlay'),
    path('overlay/edit/<int:overlay_id>/', views.edit_overlay, name='edit_overlay'),
    path('overlay/delete/<int:overlay_id>/', views.delete_overlay, name='delete_overlay'),
    path('characters/', views.list_characters, name='list_characters'),
    path('scenes/', views.list_scenes, name='list_scenes'),
    path('contents/', views.list_scenecontents, name='list_scenecontents'),
    path('overlays/', views.list_overlays, name='list_overlays'),

]
