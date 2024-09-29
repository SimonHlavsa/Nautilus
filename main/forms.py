from django import forms
from django.utils.translation import gettext_lazy as _

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs.update({'multiple': True})
        self.attrs = attrs

    def value_from_datadict(self, data, files, name):
        # Return a list of uploaded files
        upload = files.getlist(name)
        return upload

CERTIFICATION_CHOICES = [
    ('in_training', _('In Training')),
    ('owd', _('OWD')),
    ('aowd', _('AOWD')),
    ('divemaster', _('Dive Master')),
    ('instructor', _('Dive Instructor')),
    ('other', _('Other'))
]

class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        # Override the clean method to handle multiple files
        files = data
        if not files:
            if self.required:
                raise forms.ValidationError("No files were uploaded.")
            else:
                return []
        if not isinstance(files, list):
            files = [files]
        # Perform any additional validation here (e.g., file size/type)
        return files

class RegistrationForm(forms.Form):
    first_name = forms.CharField(label=_("First Name"), max_length=100)
    last_name = forms.CharField(label=_("Last Name"), max_length=100)
    email = forms.EmailField(label=_("School email"), max_length=100)
    phone = forms.CharField(label=_("Phone number"), max_length=100)

    certification_level = forms.ChoiceField(
        label=_("Highest Diver Certification"),
        choices=CERTIFICATION_CHOICES,
    )

    certification_proof_files = MultipleFileField(
        label="Proof of Certification",
        required=False,
        help_text=(
            "Please upload a photo of your diving license/a screenshot from a diving app or other online source. "
            "If you don't have the certificate yet, a screenshot from insis showing you have completed a school diving course with Pavel Dvořák will suffice, "
            "but ideally, proof that you have an open OWD course with NAUI. "
            "Upload up to 5 supported files: PDF or image. Maximum 10 MB per file."
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@vse.cz'):
            raise forms.ValidationError(_("The email address must end with '@vse.cz'."))
        return email

    def clean_certification_proof_files(self):
        files = self.cleaned_data.get('certification_proof_files')

        if not files:
            if self.fields['certification_proof_files'].required:
                raise forms.ValidationError("No files were uploaded.")
            else:
                return []

        if len(files) > 5:
            raise forms.ValidationError("You can upload up to 5 files.")

        for file in files:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError(f"File {file.name} is too large ( > 10MB ).")
            if file.content_type not in ['image/jpeg', 'image/png', 'application/pdf']:
                raise forms.ValidationError(f"File {file.name} is not a supported format (JPEG, PNG, PDF).")

        return files