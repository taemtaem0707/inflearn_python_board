# from django import forms


# #  https://docs.djangoproject.com/ko/2.1/ref/forms/fields/
# class PostForm(forms.Form):
#     title = forms.CharField(label='제목', max_length=200)
#     content = forms.CharField(label='내용',widget=forms.Textarea)


# 위 방법은 model.py와 form.py를 계속 같은 코드를 사용해서 작업해줘야하는 번거로움이 존재
# 아래 방법은 model과 form을 연결하는 방법


from django.forms import ModelForm
from second.models import Post
from django.utils.translation import gettext_lazy as _

class PostForm(ModelForm):
    class Meta:
        model = Post # 연결할 모델
        fields = ['title', 'content'] # 사용할 필드
        labels = { # 필드 label 이름 변경
            'title': _('제목'),
            'content': _('내용'),
        }
        help_texts = { # 필드에 대한 설명
            'title': _('제목을 입력해주세요.'),
            'content': _('내용을 입력해주세요.'),
        }
        error_messages = { # err메시지 출력
            'name' : {
                'max_length': _('제목이 너무 깁니다. 30자 이하로 해주세요.')
            }
        }
