import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import Script, Character, Scene, SceneContent, Overlay
from .forms import (
    ScriptForm, RoleSelectionForm,
    CharacterForm, SceneForm, SceneContentForm, OverlayForm
)
from .utils import extract_dialogues
from PyPDF2 import PdfReader


# ---------------- REJESTRACJA / LOGOWANIE / WYLOGOWANIE ----------------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Konto zostało utworzone! Możesz się zalogować.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'scripts/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- DASHBOARD ----------------

@login_required
def dashboard(request):
    scripts = Script.objects.filter(owner=request.user)
    return render(request, 'scripts/dashboard.html', {'scripts': scripts})


# ---------------- SCRIPT CRUD ----------------

@login_required
def add_script(request):
    if request.method == 'POST':
        form = ScriptForm(request.POST, request.FILES)
        if form.is_valid():
            script = form.save(commit=False)
            script.owner = request.user
            script.save()
            messages.success(request, "Scenariusz dodany pomyślnie!")
            return redirect('dashboard')
    else:
        form = ScriptForm()
    return render(request, 'scripts/add_script.html', {'form': form})


@login_required
def edit_script(request, script_id):
    script = get_object_or_404(Script, id=script_id, owner=request.user)
    if request.method == 'POST':
        form = ScriptForm(request.POST, request.FILES, instance=script)
        if form.is_valid():
            form.save()
            messages.success(request, "Scenariusz zaktualizowany.")
            return redirect('dashboard')
    else:
        form = ScriptForm(instance=script)
    return render(request, 'scripts/edit_script.html', {'form': form, 'script': script})


@login_required
def delete_script(request, script_id):
    script = get_object_or_404(Script, id=script_id, owner=request.user)
    script.delete()
    messages.info(request, "Scenariusz został usunięty.")
    return redirect('dashboard')


@login_required
def view_script(request, script_id):
    script = get_object_or_404(Script, id=script_id, owner=request.user)
    text = ''
    try:
        reader = PdfReader(script.pdf.path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n\n'
    except Exception as e:
        text = f"Błąd podczas odczytu PDF-a: {str(e)}"

    return render(request, 'scripts/view_script.html', {'script': script, 'text': text})


# ---------------- WYBÓR RÓL / STRON ----------------


@login_required
def choose_roles(request, script_id):
    script = get_object_or_404(Script, id=script_id, owner=request.user)

    if request.method == 'POST':
        form = RoleSelectionForm(request.POST)
        if form.is_valid():
            start_page = form.cleaned_data['start_page']
            end_page = form.cleaned_data['end_page']
            spoken_roles = [r.strip().title() for r in form.cleaned_data['spoken_roles'].split(',')]
            silent_roles = [r.strip().title() for r in form.cleaned_data['silent_roles'].split(',')] if form.cleaned_data['silent_roles'] else []

            dialogues = extract_dialogues(script.pdf.path, start_page, end_page, spoken_roles, silent_roles)

            return render(request, 'scripts/preview_roles.html', {
                'script': script,
                'dialogues': json.dumps(dialogues, ensure_ascii=False),
                'spoken_roles': json.dumps(spoken_roles, ensure_ascii=False),
            })
    else:
        form = RoleSelectionForm()

    return render(request, 'scripts/choose_roles.html', {'form': form, 'script': script})


# ---------------- CHARACTER CRUD ----------------

@login_required
def add_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Postać została dodana.")
            return redirect('dashboard')
    else:
        form = CharacterForm()
    return render(request, 'scripts/add_character.html', {'form': form})


@login_required
def edit_character(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    if request.method == 'POST':
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            messages.success(request, "Postać zaktualizowana.")
            return redirect('dashboard')
    else:
        form = CharacterForm(instance=character)
    return render(request, 'scripts/edit_character.html', {'form': form})


@login_required
def delete_character(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    character.delete()
    messages.info(request, "Postać usunięta.")
    return redirect('dashboard')


# ---------------- SCENE CRUD ----------------

@login_required
def add_scene(request):
    if request.method == 'POST':
        form = SceneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Scena została dodana.")
            return redirect('dashboard')
    else:
        form = SceneForm()
    return render(request, 'scripts/add_scene.html', {'form': form})


@login_required
def edit_scene(request, scene_id):
    scene = get_object_or_404(Scene, id=scene_id)
    if request.method == 'POST':
        form = SceneForm(request.POST, instance=scene)
        if form.is_valid():
            form.save()
            messages.success(request, "Scena zaktualizowana.")
            return redirect('dashboard')
    else:
        form = SceneForm(instance=scene)
    return render(request, 'scripts/edit_scene.html', {'form': form})


@login_required
def delete_scene(request, scene_id):
    scene = get_object_or_404(Scene, id=scene_id)
    scene.delete()
    messages.info(request, "Scena została usunięta.")
    return redirect('dashboard')


# ---------------- SCENECONTENT CRUD ----------------

@login_required
def add_scene_content(request):
    if request.method == 'POST':
        form = SceneContentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kwestia została dodana.")
            return redirect('dashboard')
    else:
        form = SceneContentForm()
    return render(request, 'scripts/add_scene_content.html', {'form': form})


@login_required
def edit_scene_content(request, content_id):
    content = get_object_or_404(SceneContent, id=content_id)
    if request.method == 'POST':
        form = SceneContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, "Kwestia zaktualizowana.")
            return redirect('dashboard')
    else:
        form = SceneContentForm(instance=content)
    return render(request, 'scripts/edit_scene_content.html', {'form': form})


@login_required
def delete_scene_content(request, content_id):
    content = get_object_or_404(SceneContent, id=content_id)
    content.delete()
    messages.info(request, "Kwestia została usunięta.")
    return redirect('dashboard')


# ---------------- OVERLAY CRUD ----------------

@login_required
def add_overlay(request):
    if request.method == 'POST':
        form = OverlayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Nakładka została dodana.")
            return redirect('dashboard')
    else:
        form = OverlayForm()
    return render(request, 'scripts/add_overlay.html', {'form': form})


@login_required
def edit_overlay(request, overlay_id):
    overlay = get_object_or_404(Overlay, id=overlay_id)
    if request.method == 'POST':
        form = OverlayForm(request.POST, instance=overlay)
        if form.is_valid():
            form.save()
            messages.success(request, "Nakładka zaktualizowana.")
            return redirect('dashboard')
    else:
        form = OverlayForm(instance=overlay)
    return render(request, 'scripts/edit_overlay.html', {'form': form})


@login_required
def delete_overlay(request, overlay_id):
    overlay = get_object_or_404(Overlay, id=overlay_id)
    overlay.delete()
    messages.info(request, "Nakładka została usunięta.")
    return redirect('dashboard')

@login_required
def list_characters(request):
    characters = Character.objects.filter(script__owner=request.user)
    return render(request, 'scripts/characters_list.html', {'characters': characters})

@login_required
def list_scenes(request):
    scenes = Scene.objects.filter(script__owner=request.user)
    return render(request, 'scripts/scenes_list.html', {'scenes': scenes})

@login_required
def list_scenecontents(request):
    contents = SceneContent.objects.filter(scene__script__owner=request.user)
    return render(request, 'scripts/scenecontents_list.html', {'contents': contents})

@login_required
def list_overlays(request):
    overlays = Overlay.objects.filter(contents__scene__script__owner=request.user).distinct()
    return render(request, 'scripts/overlays_list.html', {'overlays': overlays})
