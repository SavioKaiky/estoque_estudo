from database import db
from datetime import datetime

class LoteInsumo(db.Model):
    __tablename__ = "lotes_insumos"

    id = db.Column(db.Integer, primary_key=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey("insumo.id"))
    
    quantidade_inicial = db.Column(db.Float)
    quantidade_restante = db.Column(db.Float)

    custo_unitario = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    insumo = db.relationship("Insumo")