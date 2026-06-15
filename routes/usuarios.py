"""
routes/usuarios.py
===================
Camada HTTP de usuários.
Sem lógica de negócio — apenas recebe request, chama service, retorna response.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.usuario_service import (
    listar_usuarios,
    cadastrar_usuario,
    editar_usuario,
    alternar_ativo,
    EmailJaCadastradoError,
)
from models.user import User
from database import db

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.route("/", methods=["GET", "POST"])
def listar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        try:
            cadastrar_usuario(nome, email, senha)
            flash(f"Usuário '{nome}' cadastrado com sucesso.", "success")
        except EmailJaCadastradoError as e:
            flash(str(e), "danger")
        except ValueError as e:
            flash(str(e), "danger")

        return redirect(url_for("usuarios.listar"))

    usuarios = listar_usuarios()
    return render_template("usuarios/listar.html", usuarios=usuarios)


@usuarios_bp.route("/<int:user_id>/editar", methods=["GET", "POST"])
def editar(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for("usuarios.listar"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        nova_senha = request.form.get("nova_senha", "").strip() or None

        try:
            editar_usuario(user_id, nome, email, nova_senha)
            flash("Usuário atualizado com sucesso.", "success")
            return redirect(url_for("usuarios.listar"))
        except EmailJaCadastradoError as e:
            flash(str(e), "danger")
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("usuarios/editar.html", user=user)


@usuarios_bp.route("/<int:user_id>/alternar-ativo", methods=["POST"])
def alternar(user_id):
    try:
        user = alternar_ativo(user_id)
        status = "ativado" if user.ativo else "desativado"
        flash(f"Usuário '{user.nome}' {status}.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("usuarios.listar"))