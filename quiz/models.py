from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    tg_id = models.CharField(max_length=150, blank=True)
    wrongs = models.IntegerField(default=0,verbose_name='Wrongs',)
    admin = models.BooleanField(default=False,verbose_name="Admin")
    corrects = models.IntegerField(default=0,verbose_name='Corrects')
    owner = models.BooleanField(default=False,verbose_name="Owner")
    def __str__(self):
        return f"{self.first_name} {self.tg_id}"

class QuizType(models.Model):
    title = models.CharField(verbose_name="Title", max_length=150, blank=True)
    description = models.TextField(
        verbose_name='Description',
        blank=True,
        max_length=300,
    )
    def __str__(self):
        return self.title

class QuizDifficulty(models.Model):
    title = models.CharField(verbose_name="Title", max_length=150, blank=True)
    description = models.TextField(
        verbose_name='Description',
        blank=True,
        max_length=300,
    )
    def __str__(self):
        return self.title

class Quiz(models.Model):
    question = models.TextField(
        verbose_name='Question',
        blank=True,
        max_length=300,
    )
    right_answer = models.CharField(
        verbose_name='Right Answer',
        blank=True,
        max_length=300,
    )
    wrong_answer_1 = models.CharField(
        verbose_name='Wrong Answer 1',
        blank=True,
        max_length=300,
    )
    wrong_answer_2 = models.CharField(
        verbose_name='Wrong Answer 2',
        blank=True,
        max_length=300,
    )
    wrong_answer_3 = models.CharField(
        verbose_name='Wrong Answer 3',
        blank=True,
        max_length=300,
    )
    type = models.ForeignKey(
        QuizType,
        on_delete=models.CASCADE,
        related_name="quiz_types",
        blank=True,
        null=True,
        verbose_name="Type"
    )
    difficulty = models.ForeignKey(
        QuizDifficulty,
        on_delete=models.CASCADE,
        related_name="quiz_types",
        blank=True,
        null=True,
        verbose_name="Difficulty"
    )
    def __str__(self):
        return self.question