from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#init do db
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # init extenção flask migrate
    db.init_app(app)
    migrate.init_app(app, db)
    
    #import dos blueprints
    from app.routes.usuarios import usuarios_bp
    from app.routes.produtos import produtos_bp
    from app.routes.movimentacao_estoque import movimentacao_estoque_bp
    from app.routes.pedidos import pedidos_bp
    from app.routes.itens_pedido import itens_pedido_bp
    from app.routes.logs_atividades import logs_atividades_bp
    from app.routes.relatorios_estoque import relatorios_estoque_bp
    from app.routes.relatorios_vendas import relatorios_vendas_bp
    from app.routes.alertas_reposicao import alertas_reposicao_bp
    
    #registro dos blueprints
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(produtos_bp, url_prefix='/produtos')
    app.register_blueprint(movimentacao_estoque_bp, url_prefix='/movimentacao_estoque')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(itens_pedido_bp, url_prefix='/itens_pedido')
    app.register_blueprint(logs_atividades_bp, url_prefix='/logs_atividades')
    app.register_blueprint(relatorios_estoque_bp, url_prefix='/relatorios_estoque')
    app.register_blueprint(relatorios_vendas_bp, url_prefix='/relatorios_vendas')
    app.register_blueprint(alertas_reposicao_bp, url_prefix='/alertas_reposicao')
    
    return app
