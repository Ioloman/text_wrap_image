from django import forms


class RoomForm(forms.Form):
    name = forms.CharField(label='name')
    text = forms.CharField(label='text')