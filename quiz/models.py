# coding: utf-8

import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class QuestionSubject(models.Model):
    subject = models.CharField(max_length=50)

    def __unicode__(self):
        return self.subject

    class Meta:
        verbose_name = 'Question Subject'
        verbose_name_plural = 'Questions Subjects'

class QuestionDificulty(models.Model):
    dificulty = models.CharField(max_length=50)
    weight = models.IntegerField()

    def __unicode__(self):
        return self.dificulty

    class Meta:
        verbose_name = 'Question Dificulty'
        verbose_name_plural = 'Questions Dificulties'
        ordering = ['weight',]

class Question(models.Model):
    OPEN = u'O'
    CLOSED = u'C'
    QUESTION_TYPES = (
        (OPEN, u'Open'),
        (CLOSED, u'Closed'),
    )

    question = models.CharField(max_length=255)
    example = models.TextField(max_length=2000, blank=True, null=True)
    subject = models.ForeignKey(QuestionSubject)
    question_type = models.CharField(max_length=1, choices=QUESTION_TYPES)
    dificulty = models.ForeignKey(QuestionDificulty)
    image = models.ImageField(upload_to='/tmp/',max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    letter = models.CharField(max_length=1)

    def __unicode__(self):
        return self.answer

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

class QuizSubject(models.Model):
    subject = models.CharField(max_length=50)

    def __unicode__(self):
        return self.subject

    class Meta:
        verbose_name = 'Quiz Subject'
        verbose_name_plural = 'Quizzes Subjects'

class Quiz(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(QuizSubject)
    questions = models.ManyToManyField(Question)
    expire_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

class UserQuiz(models.Model):
    NEW = u'N'
    ONGOING = u'O'
    FINISHED = u'F'
    EXPIRED = u'E'

    STATUS = (
        (NEW, u'New'),
        (ONGOING, u'Ongoing'),
        (FINISHED, u'Finished'),
        (EXPIRED, u'Expired'),
    )

    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    expire_date = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=NEW)

    def __unicode__(self):
         return u'%s %s' % (self.user, self.quiz)

    def has_finished(self):
        if self.status == self.FINISHED:
            return True
        else:
            if self.start_time and self.end_time:
                self.status = self.FINISHED
                self.save()
                return True
            else:
                return False
    has_finished.boolean = True
    has_finished.short_description = 'Finished?'

    def has_expired(self):
        if self.status == self.EXPIRED:
            return True
        else:
            if self.expire_date and timezone.now() > self.expire_date:
                self.status = self.EXPIRED
                self.save()
                return True
            else:
                return False
    has_expired.boolean = True
    has_expired.short_description = 'Expired?'

    def get_progress(self):
        total_questions = self.quiz.questions.count()
        answered_questions = UserQuizAnswers.objects.filter(user_quiz__id=self.id).count()
        current_progress = float(answered_questions) / float(total_questions) * 100
        current_progress = int(round(current_progress))
        return u'{0}%'.format(current_progress)

    def get_status(self):
        if self.has_finished():
            return 'Finished'
        elif self.has_expired():
            return 'Expired'
        elif self.start_time and not self.end_time:
            return 'Ongoing'
        else:
            return 'New'
    get_status.short_description = 'Status'
    
    class Meta:
        verbose_name = 'Apply Quiz'
        verbose_name_plural = 'Apply Quizzes'

class UserQuizAnswers(models.Model):
    user_quiz = models.ForeignKey(UserQuiz)
    question = models.ForeignKey(Question)
    closed_answer = models.ForeignKey(Answer, null=True)
    open_answer = models.CharField(max_length=2000, blank=True, null=True)