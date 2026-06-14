from database import db

class FichaTecnica(db.Model):
    __tablename__ = "ficha_tecnica"

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"))
    insumo_id = db.Column(db.Integer, db.ForeignKey("insumos.id"))
    quantidade = db.Column(db.Float)  # quanto usa por unidade

    produto = db.relationship("Produto")
    insumo = db.relationship("Insumo")

    @property
    def quantidade_em_gramas(self) -> float:
        """
        Converte a quantidade (salva em kg) para gramas na exibição.
        Ex: 0.5 kg → 500.0 g
        """
        return self.quantidade * 1000
