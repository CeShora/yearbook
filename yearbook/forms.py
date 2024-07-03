from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from .models import QUESTIONS, Student, Answer

User = get_user_model()

class StudentRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}))

    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'email',
            'github_link', 'linkedin_link', 'phone', 'description', 'one_liner'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub Link'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn Link'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'one_liner': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'One Liner'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        student = super().save(commit=False)
        student.set_password(self.cleaned_data["password1"])
        if commit:
            student.save()
        return student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'email',
            'github_link', 'linkedin_link', 'phone', 'description', 'one_liner'
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub Link'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn Link'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'one_liner': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'One Liner'}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question_number', 'answer_text']
        widgets = {
            'question_number': forms.HiddenInput(),
            'answer_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Answer text'})
        }

AnswerFormSet = inlineformset_factory(Student, Answer, form=AnswerForm, extra=3)

def get_dynamic_answer_forms():
    class DynamicAnswerForm(forms.Form):
        pass

    for i, question in enumerate(QUESTIONS):
        DynamicAnswerForm.base_fields[f'question_{i}'] = forms.CharField(
            label=question,
            required=False,
            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': question})
        )

    return DynamicAnswerForm