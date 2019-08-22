# 文件: comment/forms.py
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': "width:60%;"}
        )
    )
    email = forms.CharField(
        label='Email',
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control', 'style': "width: 60%;"}
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': "width: 60%;"}
        )
    )

    def clean_content(self):
        # 用于控制评论的长度
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('你说的东西太少了啦！')
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']