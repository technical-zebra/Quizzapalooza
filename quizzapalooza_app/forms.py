from django import forms
from .models import Quiz


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your password'}))


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your password'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter your password again'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class QuizForm(forms.Form):
    QUIZ_MODE_CHOICES = [
        ("TrueOrFalse", "True or False mode"),
        ("MutiChoices", "4 multiple choice mode"),
    ]

    question = forms.CharField(required=True,
                               label="Your Question",
                               widget=forms.TextInput(attrs={"class": "form-control"}),
                               )
    quiz_mode = forms.ChoiceField(
        required=True,
        label="Quiz Mode",
        choices=QUIZ_MODE_CHOICES,
        widget=forms.RadioSelect(attrs={"id": "quiz_mode", "onclick": "SelectRadioValue()"}),
        initial="MutiChoices",
    )
    choice1 = forms.CharField(
        label="Choice 1",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    choice2 = forms.CharField(
        label="Choice 2",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    choice3 = forms.CharField(
        label="Choice 3",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    choice4 = forms.CharField(
        label="Choice 4",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    answer = forms.ChoiceField(
        label="Answer",
        choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")],
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        question = cleaned_data.get("question")
        quiz_mode = cleaned_data.get("quiz_mode")
        answer = cleaned_data.get("answer")

        if len(question) < 3:
            raise forms.ValidationError("Question should be at least 3 characters")
        elif answer not in ["1", "2", "3", "4"]:
            raise forms.ValidationError('Answer should be "1" or "2" or "3" or "4"')
        elif quiz_mode not in ["MutiChoices", "TrueOrFalse"]:
            raise forms.ValidationError("Please give a valid quiz mode")

        return cleaned_data

    def save(self, user):
        question = self.cleaned_data["question"]
        quiz_mode = self.cleaned_data["quiz_mode"]
        answer = self.cleaned_data["answer"]

        if quiz_mode == "MutiChoices":
            choice1 = self.cleaned_data["choice1"]
            choice2 = self.cleaned_data["choice2"]
            choice3 = self.cleaned_data["choice3"]
            choice4 = self.cleaned_data["choice4"]
        elif quiz_mode == "TrueOrFalse":
            choice1 = self.cleaned_data["choice1"]
            choice2 = self.cleaned_data["choice2"]
            choice3 = ""
            choice4 = ""

        new_quiz = Quiz(
            user=user,
            content=question,
            type=quiz_mode,
            answer_id=answer,
            choice_1_content=choice1,
            choice_2_content=choice2,
            choice_3_content=choice3,
            choice_4_content=choice4,
        )
        new_quiz.save()


class JoinQuizForm(forms.Form):
    session_id = forms.IntegerField()
    nickname = forms.CharField()
