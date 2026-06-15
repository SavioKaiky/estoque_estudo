"""
services/usuario_service.py
=============================
REGRAS DE NEGÓCIO de usuários.

Responsabilidades:
  - Validar unicidade de e-mail
  - Aplicar hash de senha via model
  - Ativar / desativar usuário
  - Nunca retornar senha_hash para fora desta camada
"""

from database import db
from models.user import User


class EmailJaCadastradoError(Exception):
    pass


def listar_usuarios() -> list[User]:
    return User.query.order_by(User.nome.asc()).all()


def cadastrar_usuario(nome: str, email: str, senha: str) -> User:
    if not nome or not email or not senha:
        raise ValueError("Nome, e-mail e senha são obrigatórios.")

    if User.query.filter_by(email=email).first():
        raise EmailJaCadastradoError(f"E-mail '{email}' já está cadastrado.")

    user = User(nome=nome, email=email)
    user.set_senha(senha)

    db.session.add(user)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return user


def editar_usuario(user_id: int, nome: str, email: str,
                   nova_senha: str = None) -> User:
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError("Usuário não encontrado.")

    # Verifica conflito de e-mail com outro usuário
    existente = User.query.filter_by(email=email).first()
    if existente and existente.id != user_id:
        raise EmailJaCadastradoError(f"E-mail '{email}' já está em uso.")

    user.nome = nome
    user.email = email

    if nova_senha:
        user.set_senha(nova_senha)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return user


def alternar_ativo(user_id: int) -> User:
    """Ativa o usuário se estiver inativo, e vice-versa."""
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError("Usuário não encontrado.")

    user.ativo = not user.ativo

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return user