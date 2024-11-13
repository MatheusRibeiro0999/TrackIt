from . import db
from datetime import datetime

class Perfil(db.Model):
    __tablename__ = 'perfis'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

    # relaciona com a tabela usuarios
    usuarios = db.relationship('Usuario', backref='perfil', lazy=True)

    def __repr__(self):
        return f"<Perfil {self.nome}>"


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    perfil_id = db.Column(db.Integer, db.ForeignKey('perfis.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Usuario {self.nome}>"


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_estoque = db.Column(db.Integer, default=0)
    alerta_reposicao = db.Column(db.Integer, default=10)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Produto {self.nome}>"


class MovimentacaoEstoque(db.Model):
    __tablename__ = 'movimentacao_estoque'

    id = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    tipo = db.Column(db.Enum('entrada', 'saida'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)

    produto = db.relationship('Produto', backref=db.backref('movimentacoes', lazy=True))

    def __repr__(self):
        return f"<MovimentacaoEstoque {self.tipo} de {self.quantidade} unidades do produto {self.produto.nome}>"


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('pendente', 'processando', 'concluido', 'cancelado'), default='pendente')
    total = db.Column(db.Numeric(10, 2), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('pedidos', lazy=True))

    def __repr__(self):
        return f"<Pedido {self.id} - Status: {self.status}>"


class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'

    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    pedido = db.relationship('Pedido', backref=db.backref('itens', lazy=True))
    produto = db.relationship('Produto', backref=db.backref('itens', lazy=True))

    def __repr__(self):
        return f"<ItemPedido {self.produto.nome} - Quantidade: {self.quantidade}>"


class LogAtividade(db.Model):
    __tablename__ = 'logs_atividades'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    atividade = db.Column(db.String(255), nullable=False)
    data_atividade = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref=db.backref('logs', lazy=True))

    def __repr__(self):
        return f"<LogAtividade {self.atividade}>"


class RelatorioEstoque(db.Model):
    __tablename__ = 'relatorios_estoque'

    id = db.Column(db.Integer, primary_key=True)
    data_relatorio = db.Column(db.DateTime, default=datetime.utcnow)
    quantidade_produtos = db.Column(db.Integer, nullable=False)
    valor_total_estoque = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<RelatorioEstoque {self.data_relatorio}>"


class RelatorioVendas(db.Model):
    __tablename__ = 'relatorios_vendas'

    id = db.Column(db.Integer, primary_key=True)
    data_relatorio = db.Column(db.DateTime, default=datetime.utcnow)
    total_vendas = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_vendas = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<RelatorioVendas {self.data_relatorio}>"


class AlertaReposicao(db.Model):
    __tablename__ = 'alertas_reposicao'

    id = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False)
    quantidade_necessaria = db.Column(db.Integer, nullable=False)
    data_alerta = db.Column(db.DateTime, default=datetime.utcnow)

    produto = db.relationship('Produto', backref=db.backref('alertas', lazy=True))

    def __repr__(self):
        return f"<AlertaReposicao para {self.produto.nome}>"
