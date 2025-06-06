from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Usuario, Produto, Venda
from app.forms import formUsuario, formLogin, ProdutoForm, VendaForm
import requests
import matplotlib.pyplot as plt
import io, urllib, base64
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db.models import Sum
from collections import defaultdict

def index(request):
    return render(request, "index.html")

def exibirUsuarios(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'ListUsuarios': usuarios})

def addUsuario(request):
    formUser = formUsuario(request.POST or None)

    if request.POST:
        if formUser.is_valid():
            print("Formulário de cadastro VÁLIDO!")
            usuario = formUser.save(commit=False)
            usuario.set_password(formUser.cleaned_data['senha'])
            usuario.save()
            print(f"Usuário {usuario.email} SALVO no banco de dados.")
            messages.success(request, "Usuário cadastrado com sucesso! Faça login para continuar.")
            return redirect("login")
        else:
            print("Formulário de cadastro INVÁLIDO!")
            print("Erros do formulário de Cadastro:", formUser.errors)
    return render(request, "add-usuario.html", {'form': formUser})

def excluirUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect("exibirUsuarios")

def editarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    
    formUser = formUsuario(request.POST or None, instance=usuario)
    
    if request.POST:
        if formUser.is_valid():
            formUser.save()
            return redirect("exibirUsuarios")
    return render(request, "editar-usuario.html", {'form':formUser})

def listar_produtos(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    produtos_db = Produto.objects.all()
    produtos_api = requests.get("https://fakestoreapi.com/products").json()

    return render(request, 'produtos/listar.html', {
        'produtos_db': produtos_db,
        'produtos_api': produtos_api
    })

def cadastrar_produto(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Cadastrar Produto'})

def editar_produto(request, pk):
    sessao = verificar_sessao(request)
    if sessao: return sessao #

    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Editar Produto'})

def excluir_produto(request, pk):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, "Produto excluído com sucesso!")
        return redirect('listar_produtos')
    return render(request, 'produtos/confirmar_exclusao.html', {'produto': produto})

def login(request):
    frmLogin = formLogin(request.POST or None)
    if request.POST:
        if frmLogin.is_valid():
            _email = frmLogin.cleaned_data.get('email')
            _senha = frmLogin.cleaned_data.get('senha')
            try:
                userLogin = Usuario.objects.get(email=_email)
                if userLogin.check_password(_senha):
                    request.session.set_expiry(timedelta(seconds=600))
                    request.session['email'] = _email
                    messages.success(request, f"Bem-vindo(a), {userLogin.nome}!")
                    return redirect("dashboard")
                else:
                    messages.error(request, "Senha incorreta.")
            except Usuario.DoesNotExist:
                messages.error(request, "Usuário não encontrado.")
        else:
            print("Erros do formulário de Login:", frmLogin.errors)
            messages.error(request, "Credenciais inválidas.")
    return render(request, "login.html", {'form': frmLogin})

def logout(request):
    request.session.clear()
    messages.info(request, "Você foi desconectado.")
    return redirect('index')

def dashboard(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    _email = request.session.get("email")
    return render(request, "dashboard.html", {"email": _email})

def verificar_sessao(request):
    if not request.session.get('email'):
        return redirect('index')
    return None

def comprar_produto(request, produto_id):
    if not request.session.get('email'):
        messages.info(request, "Você precisa estar logado para finalizar a compra.")
        return redirect('login')

    produto = get_object_or_404(Produto, pk=produto_id)
    request.session['produto_compra_id'] = produto.id
    return redirect('checkout')

def checkout(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    produto_id = request.session.get('produto_compra_id')
    if not produto_id:
        messages.error(request, "Nenhum produto selecionado para compra.")
        return redirect('listar_produtos')

    produto = get_object_or_404(Produto, pk=produto_id)
    usuario_email = request.session.get('email')
    cliente = get_object_or_404(Usuario, email=usuario_email)

    form_venda = VendaForm(request.POST or None)

    if request.method == 'POST':
        if form_venda.is_valid():
            venda = form_venda.save(commit=False)
            venda.cliente = cliente
            venda.produto = produto
            venda.preco_da_venda = produto.preco
            venda.save()

            produto.estoque -= 1
            produto.save()

            del request.session['produto_compra_id']

            messages.success(request, "Compra finalizada com sucesso!")
            return redirect('listar_produtos')
        else:
            messages.error(request, "Por favor, corrija os erros no formulário de pagamento.")

    context = {
        'cliente': cliente,
        'produto': produto,
        'form_venda': form_venda
    }
    return render(request, 'checkout.html', context)

def grafico(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    produtos = Produto.objects.all()
    nome = [produto.nome for produto in produtos]
    estoque = [produto.estoque for produto in produtos]

    # Configurações para o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(nome, estoque, color='#4a90e2') # Cor das barras
    ax.set_xlabel("Produto", color='#b0b0b0')
    ax.set_ylabel("Estoque", color='#b0b0b0')
    ax.set_title("Estoque de Produtos", color='#f0f0f0')
    
    # Linha corrigida: Removido 'ha='right''
    ax.tick_params(axis='x', colors='#b0b0b0', rotation=45) 
    ax.tick_params(axis='y', colors='#b0b0b0') 
    
    ax.set_facecolor('#2a2a2a') # Fundo do gráfico
    fig.set_facecolor('#2a2a2a') # Fundo da figura
    ax.spines['left'].set_color('#b0b0b0') # Cor dos eixos
    ax.spines['bottom'].set_color('#b0b0b0')
    ax.spines['right'].set_color('none') # Remover borda direita
    ax.spines['top'].set_color('none') # Remover borda superior
    ax.grid(axis='y', linestyle='--', alpha=0.7, color='#555') # Linhas de grade mais suaves

    plt.tight_layout() # Ajusta o layout para evitar sobreposição

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    plt.close(fig) # Fechar a figura para liberar memória

    return render(request, 'grafico.html', {'dados':uri})

def grafico_vendas(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    vendas = Venda.objects.order_by('data_da_compra').values('data_da_compra__date').annotate(total_vendas=Sum('preco_da_venda'))

    datas = [v['data_da_compra__date'].strftime('%Y-%m-%d') for v in vendas]
    totais = [float(v['total_vendas']) for v in vendas]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(datas, totais, marker='o')
    ax.set_xlabel("Data")
    ax.set_ylabel("Total de Vendas (R$)")
    ax.set_title("Vendas por Dia")
    ax.grid(True)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    plt.close(fig)

    return render(request, 'grafico_vendas.html', {'dados_vendas': uri})

