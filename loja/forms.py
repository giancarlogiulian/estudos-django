from django import forms


class CheckoutForm(forms.Form):
    nome_cliente = forms.CharField(label="Nome completo", max_length=200)
    email = forms.EmailField(label="E-mail")
    endereco = forms.CharField(label="Endereço", max_length=255, widget=forms.TextInput)
