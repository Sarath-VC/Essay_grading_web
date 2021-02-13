from django import forms
from .models import Essays, Topics, Bow
from django.utils.translation import gettext_lazy as _


class EssayupForm(forms.ModelForm):
    class Meta:
        model = Essays
        fields = ('topic', 'title', 'author', 'pdf')

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topics
        fields = ('topic_name',)
        labels = {
            'topic_name': _('Topic Name'),
        }
class BowForm(forms.ModelForm):

    class Meta:
        model = Bow
        fields = ('topic','word', 'priority',)
