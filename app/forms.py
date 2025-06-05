from django import forms
from app.models import Usuario
from .models import Produto

from django import forms
from app.models import Usuario, Produto, Venda
from django.core.exceptions import ValidationError

from django import forms
from app.models import Usuario, Produto, Venda
from django.core.exceptions import ValidationError

class formUsuario(forms.ModelForm):
    confirmacao_senha = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}), label="Confirmação de Senha")

    class Meta:
        model = Usuario
        fields = (
            'nome', 'email', 'senha', 'confirmacao_senha', 'cep', 'logradouro', 'bairro',
            'localidade', 'uf', 'numero_residencia'
        )
        widgets = { # <-- RE-ADICIONE ESTE BLOCO COMPLETO
            'nome': forms.TextInput(attrs={'type': 'text'}),
            'email': forms.TextInput(attrs={'type': 'email'}),
            'senha': forms.TextInput(attrs={'type': 'password'}),
            'cep': forms.TextInput(attrs={'onblur': 'buscarCEP(this.value)'}),
            'logradouro': forms.TextInput(attrs={'readonly': 'readonly'}),
            'bairro': forms.TextInput(attrs={'readonly': 'readonly'}),
            'localidade': forms.TextInput(attrs={'readonly': 'readonly'}),
            'uf': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmacao_senha = cleaned_data.get('confirmacao_senha')

        if senha and confirmacao_senha and senha != confirmacao_senha:
            raise ValidationError("A senha e a confirmação de senha não são compatíveis.")

        if self.instance is None and Usuario.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError("Este email já está cadastrado.")

        return cleaned_data

class formLogin(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'type':'email'}))
    senha = forms.CharField(widget=forms.TextInput(attrs={'type':'password'}))

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'foto', 'categoria']

    foto = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/*'}))

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['numero_cartao', 'validade', 'cvv']
        widgets = {
            'numero_cartao': forms.TextInput(attrs={'placeholder': 'Número do Cartão', 'maxlength': '16'}),
            'validade': forms.TextInput(attrs={'placeholder': 'MM/AA', 'maxlength': '5'}),
            'cvv': forms.TextInput(attrs={'placeholder': 'CVV', 'maxlength': '4'}),
        }