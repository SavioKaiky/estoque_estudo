from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_senha(self, senha: str) -> None:
        """Gera e armazena o hash da senha."""
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha: str) -> bool:
        """Verifica se a senha confere com o hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<User {self.email}>"