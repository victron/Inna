__author__ = 'vic'
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, modelformset_factory, modelform_factory
from django.core.exceptions import ValidationError
from models import Dreams, Dreams_D_Tags, D_Tags

# https://docs.djangoproject.com/en/1.8/ref/forms/fields/#modelchoicefield
# This method will receive a model object, and should return a string suitable for representing it
# instead __str__ in model
class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id

class MyModelChoiceField_d_tag(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.d_tag

class Dreams_D_TagsForm(ModelForm):
    tag = MyModelChoiceField_d_tag(queryset=D_Tags.objects.all())
    class Meta:
        model = Dreams_D_Tags
        # fields = ['dream_tag_weight', 'tag']
        exclude = ('dream_id', )

# class Dreams_D_TagsForm(forms.Form):
#
#     id = forms.IntegerField(required=False, widget=forms.HiddenInput())
#     # dream_tag_weight = forms.ModelChoiceField(queryset=Color.objects.all())
#     tag = MyModelChoiceField_d_tag(queryset=D_Tags.objects.all())

DreamForm = modelform_factory(Dreams, exclude=('user', ))

# Dreams_D_TagsForm = modelform_factory(Dreams_D_Tags, exclude=('dream_id',))




