from django.contrib import admin
from classroom.models import User, Subject, Quiz, Question, Answer, Student, TakenQuiz, StudentAnswer, Selected_lists, Placement

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Student)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)
admin.site.register(Placement)
admin.site.register(Selected_lists)
