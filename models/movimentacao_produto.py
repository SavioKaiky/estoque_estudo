from database import db
from datetime import datetime

class MovimentacaoProduto(db.Model):
    __tablename__ = "movimentacoes_produtos"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"))
    tipo = db.Column(db.String(10))  # entrada ou saida
    quantidade = db.Column(db.Integer)
    motivo = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    custo_total = db.Column(db.Float)
    custo_unitario = db.Column(db.Float)

    produto = db.relationship("Produto")

    