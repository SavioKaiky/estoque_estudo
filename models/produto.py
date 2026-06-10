from database import db

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    estoque_atual = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Produto {self.nome}>"