from operator import mod
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class UserType(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return '{} - {}'.format(self.id, self.name)


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, related_name="new_user", on_delete=models.CASCADE)
#     user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
#     mobile = models.PositiveIntegerField()
#     address = models.TextField()
#     time_created = models.DateTimeField(auto_now_add=True)
#     time_modified = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return '{} - {}'.format(self.user.id, self.user.first_name)


class SkillCv(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class UserSkills(models.Model):
    user = models.ForeignKey(User, related_name="registred_user", on_delete=models.CASCADE)
    skill = models.OneToOneField(SkillCv, related_name="skill_cv", on_delete=models.CASCADE)
    percentage = models.PositiveIntegerField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    change_list_template = 'change_list_graph.html'

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.id, self.user.first_name, self.skill.name,self.percentage)