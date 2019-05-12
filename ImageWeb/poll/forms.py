from django import forms


class ShowImageForm(forms.Form):
    sizeKafelek = forms.CharField(label='Width', required=True, help_text='Provide width')
    #width = forms.CharField(label='Width', required=True, help_text='Provide width')
    #height = forms.CharField(label='Height', required=True, help_text='Provide height')