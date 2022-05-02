from django import forms


class SearchForm(forms.Form):
    item_name = forms.CharField(label='商品名', max_length=32, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    title = forms.CharField(label='商品名', max_length=32,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='商品名', min_value=0,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
