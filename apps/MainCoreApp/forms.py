from django import forms
from . import models


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = models.ArticleComment
        fields = ['com_username', 'com_content', 'com_photo']
        error_messages = {
            'com_username': {
                'required': '名字不能为空',
                'max_length': '名字太长'
            },
            'com_content': {
                'required': '内容不能为空',
                'max_length': '内容太长'
            },
            'com_photo': {
                'required': '头像不能为空',
            },
        }
