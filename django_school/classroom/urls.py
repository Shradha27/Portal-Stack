from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('', students.QuizListView.as_view(), name='quiz_list'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.dashboard, name='dashboard'),
        path('charts/', teachers.charts, name='charts'),
        path('placement/', teachers.PlacementListView.as_view(), name='placement_change_list'),
        path('list/', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('placement/add/', teachers.PlacementCreateView.as_view(), name='placement_add'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('placement/<int:pk>/', teachers.PlacementUpdateView.as_view(), name='placement_change'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('placement/<int:pk>/delete/', teachers.PlacementDeleteView.as_view(), name='placement_delete'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('placement/<int:pk>/list/add/', teachers.upload_csv, name='list_add'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('placement/<int:placement_pk>/selected_lists/<int:selected_lists_pk>/delete/', teachers.StudentDeleteView.as_view(), name='student_delete'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
