from database import db
from sqlalchemy import func
from datetime import datetime


class Insumo(db.Model):
    __tablename__ = "insumo"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    unidade = db.Column(db.String(20), nullable=False)
    estoque_minimo = db.Column(db.Float, default=0)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # REMOVIDO: estoque_atual como coluna — era fonte de inconsistência.
    # O saldo agora é calculado a partir das movimentações via property.

    movimentacoes = db.relationship("MovimentacaoInsumo", backref="insumo_ref", lazy="dynamic")

    @property
    def estoque_atual(self) -> float:
        """
        Saldo calculado em tempo real somando entradas e subtraindo saídas.
        Nunca fica divergente do histórico real.
        """
        from models.movimentacao_insumo import MovimentacaoInsumo
        entradas = db.session.query(
            func.coalesce(func.sum(MovimentacaoInsumo.quantidade), 0.0)
        ).filter_by(insumo_id=self.id, tipo="entrada").scalar()

        saidas = db.session.query(
            func.coalesce(func.sum(MovimentacaoInsumo.quantidade), 0.0)
        ).filter_by(insumo_id=self.id, tipo="saida").scalar()

        return float(entradas) - float(saidas)

    @property
    def abaixo_minimo(self) -> bool:
        return self.estoque_atual < self.estoque_minimo

    def __repr__(self):
        return f"<Insumo {self.nome}>"


class MovimentacaoInsumo(db.Model):
    __tablename__ = "movimentacao_insumo"

    id = db.Column(db.Integer, primary_key=True)

    insumo_id = db.Column(
        db.Integer,
        db.ForeignKey("insumo.id"),
        nullable=False
    )

    tipo = db.Column(db.String(20))
    quantidade = db.Column(db.Float)
    motivo = db.Column(db.String(100))

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    insumo = db.relationship("Insumo")
    user = db.relationship("User")