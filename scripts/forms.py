from django import forms
from .models import Script

class ScriptForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['title', 'pdf']

    def clean_pdf(self):
        pdf = self.cleaned_data.get('pdf')
        if not pdf:
            raise forms.ValidationError("Musisz wybrać plik PDF.")
        return pdf

class RoleSelectionForm(forms.Form):
    start_page = forms.IntegerField(label='Strona początkowa', min_value=1)
    end_page = forms.IntegerField(label='Strona końcowa', min_value=1)
    spoken_roles = forms.CharField(label='Postaci do czytania na głos (oddziel przecinkami)')
    silent_roles = forms.CharField(label='Postaci tylko do wyświetlania (oddziel przecinkami)', required=False)
