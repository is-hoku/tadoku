from django import forms
from .models import Schedule


class SimpleScheduleForm(forms.ModelForm):
    """シンプルなスケジュール登録用フォーム"""

    class Meta:
        model = Schedule
        fields = ('date', 'title', 'series', 'level', 'word_cnt', 'evaluation', 'coment')
        widgets = {
            'date': forms.DateTimeField,
            'title': forms.TextInput,
            'series': forms.TextInput,
            'level': forms.TextInput,
            'word_cnt': forms.TextInput,
            'evaluation': forms.RadioSelect,
            'coment': forms.TextInput,
        }
