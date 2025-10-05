from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']


class EditOptionsForm(forms.Form):
    width = forms.IntegerField(label='Resize Width', required=False)
    height = forms.IntegerField(label='Resize Height', required=False)
    scale = forms.FloatField(label='Scale Factor', min_value=0.1, max_value=10.0, required=False, help_text="Use scale for proportional resizing (e.g., 1.5 for 150%)")
    
    INTERPOLATION_CHOICES = [
        ('INTER_LINEAR', 'Linear'),
        ('INTER_CUBIC', 'Cubic'),
        ('INTER_NEAREST', 'Nearest'),
        ('INTER_LANCZOS4', 'Lanczos4'),
    ]
    interpolation = forms.ChoiceField(choices=INTERPOLATION_CHOICES, label='Interpolation Method', required=True)

    comment = forms.CharField(label='Comment', required=False, max_length=200)

    def clean(self):
        cleaned_data = super().clean()
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')
        scale = cleaned_data.get('scale')

        if not width and not height and not scale:
            raise forms.ValidationError("Please provide either width, height, or scale to resize the image.")
        return cleaned_data
