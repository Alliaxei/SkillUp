from django import forms

from curriculum.models import Lecture, Module, Task


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["title", "description"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {
                        "class": "form-control rounded-4 px-3 py-3",
                        "rows": "4",
                        "id": "descriptionTextarea",
                        "maxlength": "1000",
                    }
                )
            else:
                field.widget.attrs.update(
                    {"class": "form-control btn-rounded px-3 py-2"}
                )
            field.widget.attrs.update({"placeholder": field.label})


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        label="Крайний срок сдачи",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "text",
                "class": "form-control btn-rounded px-3 py-2 datepicker",
                "placeholder": "Выберите дату...",
            },
        ),
    )

    class Meta:
        model = Task
        fields = ["module", "title", "description", "deadline", "max_score"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "deadline":
                continue

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update(
                    {
                        "class": "form-control rounded-4 px-3 py-3",
                        "rows": "4",
                        "id": "taskDescriptionTextarea",
                        "maxlength": "1500",
                    }
                )
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update(
                    {"class": "form-select btn-rounded px-3 py-2"}
                )
            else:
                field.widget.attrs.update(
                    {"class": "form-control btn-rounded px-3 py-2"}
                )

            if field_name == "max_score":
                field.widget.attrs.update({"id": "maxScoreInput"})

            field.widget.attrs.update({"placeholder": field.label})


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class LectureForm(forms.ModelForm):
    # images = forms.ImageField(
    #     widget=MultipleFileInput(
    #         attrs={"multiple": True, "class": "form-control btn-rounded"}
    #     ),
    #     required=False,
    #     label="Добавить изображения в галерею",
    # )

    class Meta:
        model = Lecture
        fields = ["module", "title", "content"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "content":
                continue
            if field_name != "images":
                field.widget.attrs.update(
                    {"class": "form-control btn-rounded px-3 py-2"}
                )
            field.widget.attrs.update({"placeholder": field.label})
