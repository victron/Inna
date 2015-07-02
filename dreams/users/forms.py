__author__ = 'vic'

from django.forms import ModelForm
from django.forms.models import inlineformset_factory, modelformset_factory, modelform_factory
from django.core.exceptions import ValidationError
from models import Dreams, Dreams_D_Tags


# class DreamForm(ModelForm):
#     class Meta:
#         model = Dreams
#         exclude = ('dream_date', 'user', )

DreamForm = modelform_factory(Dreams, exclude=('user', ))

Dreams_D_TagsForm = modelform_factory(Dreams_D_Tags, exclude=('dream_id',))



