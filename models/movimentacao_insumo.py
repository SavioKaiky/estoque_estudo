from database import db
from datetime import datetime

class MovimentacaoInsumo(db.Model):
    __tablename__ = "movimentacoes_insumos"

    id = db.Column(db.Integer, primary_key=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey("insumos.id"))
    tipo = db.Column(db.String(10))  # entrada ou saida
    quantidade = db.Column(db.Float)
    motivo = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    insumo = db.relationship("Insumo")