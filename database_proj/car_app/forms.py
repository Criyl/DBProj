from django import forms

from .models import *


class NewEmployeeForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ['f_name', 'l_name', 'position_id', 'base_pay', 'commission']

    def save(self, commit=True):
        position = super(NewEmployeeForm, self).save(commit=False)

        if commit:
            position.save()
        return position

    def __init__(self, *args, **kwargs):
        super(NewEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['f_name'].label = 'First Name'
        self.fields['l_name'].label = 'Last Name'
        self.fields['position_id'].label = 'Position'
        self.fields['position_id'].to_field_name = 'position_name'


class NewPositionsForm(forms.ModelForm):
    position_name = forms.CharField(label="Position Name", max_length=DEFAULT_MAX)

    class Meta:
        model = Position
        fields = ['position_name']

    def save(self, commit=True):
        position = super(NewPositionsForm, self).save(commit=False)

        if commit:
            position.save()
        return position

    def __init__(self, *args, **kwargs):
        super(NewPositionsForm, self).__init__(*args, **kwargs)


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
