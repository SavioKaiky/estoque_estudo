from database import db
from sqlalchemy import func
 
 
class Insumo(db.Model):
    __tablename__ = "insumos"
 
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    unidade = db.Column(db.String(20))
    estoque_minimo = db.Column(db.Float, default=0)
 
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
 