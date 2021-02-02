from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = {'text',}
        widgets = {
            'text': forms.fields.TextInput(attrs={
            'placeholder': 'Enter a to-do item',
            'class': 'border py-2 px-3 text-grey-darkest',
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }