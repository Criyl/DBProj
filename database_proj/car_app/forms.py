from django import forms

from .models import *


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['f_name', 'l_name']

    def save(self, commit=True):
        position = super(EditCustomerForm, self).save(commit=False)

        if commit:
            position.save()
        return position

    def __init__(self, *args, **kwargs):
        super(EditCustomerForm, self).__init__(*args, **kwargs)
        self.fields['f_name'].label = 'First Name'
        self.fields['l_name'].label = 'Last Name'
