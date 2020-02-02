from django.db import models
from django.utils.translation import gettext_lazy as _
from django import forms


class Report(models.Model):

    title = models.CharField(max_length=200, unique=True)
    datetime = models.DateTimeField()
    content = models.TextField()
    source = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'report'
        managed = True
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'


class LoginForm(forms.Form):

    username = forms.CharField(
        label=_("用户名"),
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': '',
        })   
    )

    password = forms.CharField(
        label=_("密码"),
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': '',
            'type': "password",
        })   
    )