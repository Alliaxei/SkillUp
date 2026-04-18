from django import forms

from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["file"]
        widgets = {
            "file": forms.ClearableFileInput(
                attrs={"class": "form-control btn-rounded"}
            )
        }
