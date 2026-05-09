from django import forms

from .models import Review, Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["file"]
        widgets = {
            "file": forms.ClearableFileInput(
                attrs={"class": "form-control btn-rounded"}
            )
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["score", "comment"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control btn-rounded px-3 py-2",
                    "placeholder": field.label,
                }
            )
