from database import db

class Insumo(db.Model):
    __tablename__ = "insumos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    unidade = db.Column(db.String(20))
    estoque_atual = db.Column(db.Float, default=0)
    estoque_minimo = db.Column(db.Float, default=0)

    def __repr__(self):
        return f"<Insumo {self.nome}>"