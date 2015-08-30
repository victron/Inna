__author__ = 'vic'
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, modelformset_factory, modelform_factory
from django.core.exceptions import ValidationError
from models import Dreams, Dreams_D_Tags, D_Tags

# https://docs.djangoproject.com/en/1.8/ref/forms/fields/#modelchoicefield
# This method will receive a model object, and should return a string suitable for representing it
# instead __str__ in model
# later need to check, because Note that the default widget for ModelChoiceField becomes
# impractical when the number of entries increases. You should avoid using it for more
# than 100 items.

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id

class MyModelChoiceField_d_tag(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.d_tag

class Dreams_D_TagsForm(ModelForm):
    tag = MyModelChoiceField_d_tag(queryset=D_Tags.objects.all())
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Dreams_D_Tags
        fields = ['dream_tag_weight', 'tag']
        # exclude = ('dream_id', )


class tagFormSet(forms.formsets.BaseFormSet):
    def __init__(self, *args, **kwargs):
        #http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/2422221#2422221
        # for error generation for empty fields in form
        super(tagFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def clean(self):
        # something from http://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html

        if any(self.errors):
            return
        tags = [form.cleaned_data['tag'] for form in self.forms]
        duplicates = True if len(tags) != len(set(tags)) else False
        if duplicates:
            raise ValidationError('tags must be unique', code='duplicate_tags')
        # ------- equal to above code --------
        # tags = []
        # duplicates = False
        # for form in self.forms:
        #     if form.is_valid():
        #         # weight = form.cleaned_data['dream_tag_weight']
        #         tag = form.cleaned_data['tag']
        #         if tag in tags:
        #             duplicates = True
        #         tags.append(tag)
        #         if duplicates:
        #             raise ValidationError('tags must be unique', code='duplicate_tags')
        # ============================================================================





Dreams_D_TagsFormSet = forms.formset_factory(Dreams_D_TagsForm, extra=2, formset=tagFormSet)

DreamForm = modelform_factory(Dreams, exclude=('user', ))

# Dreams_D_TagsForm = modelform_factory(Dreams_D_Tags, exclude=('dream_id',))




