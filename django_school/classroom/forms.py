from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from classroom.models import (Answer, Question, Student, StudentAnswer, Subject, User, Temp2)

''' Student Module '''

class ProfileForm(forms.ModelForm):

    model = Temp2

    fname = forms.CharField(max_length = 20)
    lname = forms.CharField(max_length = 20)
    dob = forms.DateField()
    email = forms.CharField(max_length = 40)
    contactnum = forms.IntegerField()

    egap = forms.IntegerField()
    tenper = forms.FloatField()
    tenyop = forms.IntegerField()
    tweper = forms.FloatField()
    tweyop = forms.IntegerField()

    regid = forms.IntegerField()
    rollno = forms.CharField(max_length = 20)
    gper = forms.FloatField()
    back = forms.IntegerField()

    class Meta: 
        model = Temp2
        fields=('fname','lname','dob','email','contactnum','egap','tenper','tenyop','tweper','tweyop','regid','rollno','gper','back',)

    def form_valid(self, form):
        user=form.save()

''' Student Module '''

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
