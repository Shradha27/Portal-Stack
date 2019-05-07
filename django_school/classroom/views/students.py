from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DetailView

from ..decorators import student_required
from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm, ProfileForm
from ..models import Quiz, Student, TakenQuiz, User, NewStudent, Temp2


''' Student module '''

'''class ProfileView(TemplateView):

    template_name = 'profile.html'
    form_class = ProfileForm

    def profile(self,request):
        
        MyForm = ProfileForm(request.POST)
      
        if MyForm.is_valid():

            profile = MyForm.save(commit = False)
            profile.user = request.user
            profile.save()

            fname = MyForm.cleaned_data['fname']
            lname = MyForm.cleaned_data['lname']
            dob = MyForm.cleaned_data['dob']
            email = MyForm.cleaned_data['email']
            contactnum = MyForm.cleaned_data['contactnum']
            egap = MyForm.cleaned_data['egap']
            tenper = MyForm.cleaned_data['tenper']
            tenyop = MyForm.cleaned_data['tenyop']
            tweper = MyForm.cleaned_data['tweper']
            tweyop = MyForm.cleaned_data['tweyop']
            regid = MyForm.cleaned_data['regid']
            rollno = MyForm.cleaned_data['rollno']
            gper = MyForm.cleaned_data['gper']
            back = MyForm.cleaned_data['back']
            MyForm = ProfileForm()

def studentProfile1(request):
        if request.method == 'POST':
            if request.POST.get('fname'):
            post=Temp2(request.POST)
            post.fname= request.POST('fname')
            post.lname= request.POST('lname')
            post.dob= request.POST('dob')
            post.email= request.POST('email')
            post.contactnumber= request.POST('cnum')
            post.egap= request.POST('egap')
            post.tenper= request.POST('tenper')
            post.tenyop= request.POST('tenyop')
            post.tweper= request.POST('tweper')
            post.tweyop= request.POST('tweyop')
            post.regid= request.POST('regid')
            post.rollno= request.POST('rollno')
            post.gper= request.POST('gper')
            post.back= request.POST('back')

            p=post.save()
            p.save()'''

@login_required
@student_required
def profile_data(request):
    pdata = get_object_or_404(NewStudent, user=request.user)

    return render(request, 'student/pages/forms/profile.html', {
        'pdata': pdata
    })

@method_decorator([login_required, student_required], name='dispatch')
class ProfileView(DetailView):
    model = NewStudent
    context_object_name = 'pr'
    template_name = 'student/pages/forms/profile.html'

    def get_queryset(self):
        student = self.request.user.student
        fname = student.fname
        return queryset

''' Student Module '''

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })
