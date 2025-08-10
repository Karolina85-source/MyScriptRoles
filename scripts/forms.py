from django import forms
from .models import Script, Character, Scene, SceneContent, Overlay


# Formularz do dodawania scenariusza PDF
class ScriptForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['title', 'pdf']

    def clean_pdf(self):
        pdf = self.cleaned_data.get('pdf')
        if not pdf:
            raise forms.ValidationError("Musisz wybrać plik PDF.")
        if not pdf.name.lower().endswith('.pdf'):
            raise forms.ValidationError("Dozwolone są tylko pliki PDF.")
        return pdf


# Formularz wyboru zakresu stron i ról
class RoleSelectionForm(forms.Form):
    start_page = forms.IntegerField(label='Strona początkowa', min_value=1)
    end_page = forms.IntegerField(label='Strona końcowa', min_value=1)
    spoken_roles = forms.CharField(
        label='Postaci do czytania na głos (oddziel przecinkami)',
        help_text='Np.: Jan, Anna, Marek'
    )
    silent_roles = forms.CharField(
        label='Postaci tylko do wyświetlania (oddziel przecinkami)',
        required=False,
        help_text='Np.: Narrator, Statysta'
    )


# Formularz do dodawania postaci
class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'script']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Imię postaci'}),
            'script': forms.Select()
        }


# Formularz do dodawania scen
class SceneForm(forms.ModelForm):
    class Meta:
        model = Scene
        fields = ['title', 'script', 'characters']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Tytuł sceny'}),
            'characters': forms.CheckboxSelectMultiple()
        }


# Formularz do dodawania kwestii
class SceneContentForm(forms.ModelForm):
    class Meta:
        model = SceneContent
        fields = ['scene', 'character', 'text', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Treść kwestii'}),
            'order': forms.NumberInput(attrs={'min': 1}),
        }


# Formularz do dodawania nakładek (Overlay)
class OverlayForm(forms.ModelForm):
    class Meta:
        model = Overlay
        fields = ['name', 'contents', 'description']
        widgets = {
            'contents': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Opis lub uwagi'}),
        }

