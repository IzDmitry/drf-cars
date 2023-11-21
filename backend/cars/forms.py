from django import forms
from .models import Mark


class MarkForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Mark.objects.all(),
                                  widget=forms.Select())

    class Meta:
        model = Mark
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(MarkForm, self).__init__(*args, **kwargs)
        css = 'form-select form-select-lg mb-3'
        self.fields['name'].widget.attrs['class'] = css
