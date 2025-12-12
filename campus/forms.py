from django import forms
from .models import Material


class UploadMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['course_code', 'description', 'year_used', 'file']

    widgets = {
        'description' : forms.TextInput(attrs={
            'class' : 'form-input',
            'placeholder' : "Past questions, Mr A's note",
        }),
        'year-used' : forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': '2025',
        }),
        'file' : forms.FileInput(attrs={
            'class': 'form-input',
        })
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = True
        self.label_suffix = ''