from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    cep = models.CharField(max_length=9, blank=True)
    logradouro = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    localidade = models.CharField(max_length=100, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    numero_residencia = models.CharField(max_length=10, blank=True)

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.senha)

    def __str__(self):
        return f"{self.nome} ({self.email})"
    
class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nome}"

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    foto = models.ImageField(upload_to='imagens/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome

class Venda(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    preco_da_venda = models.DecimalField(max_digits=10, decimal_places=2)
    numero_cartao = models.CharField(max_length=16)
    validade = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    data_da_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda {self.id} - {self.produto.nome} para {self.cliente.nome}"
