from django import forms

from .models import *


class NewEmployeeForm(forms.ModelForm):
    class Meta:
        model = Salesman
        fields = ['f_name', 'l_name', 'position_id', 'base_pay', 'commission']

    def save(self, commit=True):
        form = super(NewEmployeeForm, self).save(commit=False)

        if commit:
            form.save()
        return form

    def __init__(self, *args, **kwargs):
        super(NewEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['f_name'].label = 'First Name'
        self.fields['l_name'].label = 'Last Name'
        self.fields['position_id'].label = 'Position'
        self.fields['position_id'].to_field_name = 'position_name'


class NewPositionsForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['position_name']

    def save(self, commit=True):
        form = super(NewPositionsForm, self).save(commit=False)

        if commit:
            form.save()
        return form

    def __init__(self, *args, **kwargs):
        super(NewPositionsForm, self).__init__(*args, **kwargs)


class NewCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model_id',
                  'year',
                  'color',
                  'mileage',
                  'dealership',
                  'description']

    def save(self, commit=True):
        form = super(NewCarForm, self).save(commit=False)

        if commit:
            form.save()
        return form

    def __init__(self, *args, **kwargs):
        super(NewCarForm, self).__init__(*args, **kwargs)


class NewMakeForm(forms.ModelForm):
    class Meta:
        model = CarMake
        fields = ['make_name']

    def save(self, commit=True):
        form = super(NewMakeForm, self).save(commit=False)

        if commit:
            form.save()
        return form


class NewModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['make_id', 'model_name']

    def save(self, commit=True):
        form = super(NewModelForm, self).save(commit=False)

        if commit:
            form.save()
        return form


class ZipCodeForm(forms.ModelForm):
    class Meta:
        model = ZipCode
        field = ['city', 'state']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        field = ['street_number', 'street_name']


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        field = ['']


class NewSiteForm(forms.Form):
    site_name = forms.CharField(label='Site Name', max_length=DEFAULT_MAX)
    city = forms.CharField(label='City', max_length=DEFAULT_MAX)
    state = forms.CharField(label='State', max_length=2)
    zip_code = forms.IntegerField(label='Zip Code')

    def __init__(self, *args, **kwargs):
        super(NewModelForm, self).__init__(*args, **kwargs)
