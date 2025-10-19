from django.contrib import admin

from quiz.models import CustomUser, QuizDifficulty, QuizType, Quiz


@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    pass

@admin.register(QuizDifficulty)
class AdminQuizDifficulty(admin.ModelAdmin):
    pass
@admin.register(QuizType)
class AdminQuizType(admin.ModelAdmin):
    pass
@admin.register(Quiz)
class AdminQuiz(admin.ModelAdmin):
    pass
