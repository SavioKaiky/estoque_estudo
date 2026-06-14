from database import db
from datetime import datetime

class MovimentacaoInsumo(db.Model):
    __tablename__ = "movimentacao_insumo"

    id = db.Column(db.Integer, primary_key=True)
    insumo_id = db.Column(db.Integer,db.ForeignKey("insumo.id"),nullable=False)
    tipo = db.Column(db.String(20))
    quantidade = db.Column(db.Float)
    motivo = db.Column(db.String(100))
    # user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    insumo = db.relationship("Insumo")
    user = db.relationship("User")