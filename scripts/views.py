from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Script
from .forms import ScriptForm
from .forms import RoleSelectionForm
from .utils import extract_dialogues
from PyPDF2 import PdfReader
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # django.contrib.auth.urls
    else:
        form = UserCreationForm()
    return render(request, 'scripts/register.html', {'form': form})

@login_required
def add_script(request):
    if request.method == 'POST':
        form = ScriptForm(request.POST, request.FILES)
        if form.is_valid():
            script = form.save(commit=False)
            script.owner = request.user
            script.save()
            return redirect('dashboard')
    else:
        form = ScriptForm()
    return render(request, 'scripts/add_script.html', {'form': form})

@login_required
def delete_script(request, script_id):
    script = get_object_or_404(Script, id=script_id, owner=request.user)
    script.delete()
    return redirect('dashboard')

@login_required
def view_script(request, script_id):
    # Pobierz konkretny scenariusz tego użytkownika
    script = get_object_or_404(Script, id=script_id, owner=request.user)

    # Ścieżka do pliku PDF
    pdf_path = script.pdf.path

    # Wyciąganie tekstu z PDF-a
    text = ''
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n\n'
    except Exception as e:
        text = f"Błąd podczas odczytu PDF-a: {str(e)}"

    # Przekaż dane do szablonu
    context = {
        'script': script,
        'text': text,
    }

    return render(request, 'scripts/view_script.html', context)

@login_required
def dashboard(request):
    scripts = Script.objects.filter(owner=request.user)
    return render(request, 'scripts/dashboard.html', {'scripts': scripts})

@login_required
def choose_roles(request, script_id):
    script = get_object_or_404(Script, id=script_id, owner=request.user)

    if request.method == 'POST':
        form = RoleSelectionForm(request.POST)
        if form.is_valid():
            start_page = form.cleaned_data['start_page']
            end_page = form.cleaned_data['end_page']
            spoken_roles = [r.strip() for r in form.cleaned_data['spoken_roles'].split(',')]
            silent_roles = [r.strip() for r in form.cleaned_data['silent_roles'].split(',')] if form.cleaned_data['silent_roles'] else []

            pdf_path = script.pdf.path
            dialogues = extract_dialogues(pdf_path, start_page, end_page, spoken_roles, silent_roles)

            context = {
                'script': script,
                'dialogues': dialogues,
                'spoken_roles': spoken_roles,
            }
            return render(request, 'scripts/preview_roles.html', context)
    else:
        form = RoleSelectionForm()

    # Jeśli GET lub niepoprawny POST – zawsze wracamy do formularza
    return render(request, 'scripts/choose_roles.html', {'form': form, 'script': script})

def logout_view(request):
    logout(request)
    return redirect('register')


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
