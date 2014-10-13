
from django import forms
from models import Lord

class TaxRecruitmentForm(forms.ModelForm):
    class Meta:
        model = Lord
        fields = ['tax', 'recruitment']