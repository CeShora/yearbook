from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Student, Answer

User = get_user_model()


class StudentRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'email',
            'github_link', 'linkedin_link', 'phone', 'description', 'one_liner'
        ]

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

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question_number', 'answer_text']

AnswerFormSet = inlineformset_factory(Student, Answer, form=AnswerForm, extra=1)
