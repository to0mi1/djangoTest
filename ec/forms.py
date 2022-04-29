from django import forms

class SearchForm(forms.Form):
    item_name = forms.CharField(label='商品名', max_length=32)