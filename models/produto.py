from database import db
from sqlalchemy import func
 
 
class Produto(db.Model):
    __tablename__ = "produtos"
 
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
 
    # REMOVIDO: estoque_atual como coluna — era fonte de inconsistência.
    # O saldo agora é calculado a partir das movimentações via property.
 
    movimentacoes = db.relationship("MovimentacaoProduto", backref="produto_ref", lazy="dynamic")
 
    @property
    def estoque_atual(self) -> int:
        """
        Saldo calculado em tempo real somando entradas e subtraindo saídas.
        Nunca fica divergente do histórico real.
        """
        from models.movimentacao_produto import MovimentacaoProduto
        entradas = db.session.query(
            func.coalesce(func.sum(MovimentacaoProduto.quantidade), 0)
        ).filter_by(produto_id=self.id, tipo="entrada").scalar()
 
        saidas = db.session.query(
            func.coalesce(func.sum(MovimentacaoProduto.quantidade), 0)
        ).filter_by(produto_id=self.id, tipo="saida").scalar()
 
        return int(entradas) - int(saidas)
 
    def __repr__(self):
        return f"<Produto {self.nome}>"
 