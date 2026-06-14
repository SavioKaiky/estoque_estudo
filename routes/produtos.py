from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db
from models.produto import Produto
from models.insumo import Insumo
from models.ficha_tecnica import FichaTecnica

produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")

@produtos_bp.route("/", methods=["GET", "POST"])
def listar_produtos():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        if not nome:
            flash("O nome do produto é obrigatório.", "danger")
        else:
            db.session.add(Produto(nome=nome))
            db.session.commit()
            flash(f"Produto '{nome}' cadastrado.", "success")
        return redirect(url_for("produtos.listar_produtos"))
    return render_template("produtos/listar.html", produtos=Produto.query.all())

@produtos_bp.route("/<int:produto_id>/ficha", methods=["GET", "POST"])
def ficha(produto_id):
    produto = db.session.get(Produto, produto_id)
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("produtos.listar_produtos"))
    insumos = Insumo.query.all()
    if request.method == "POST":
        # Usuário informa em gramas; banco armazena em kg
        quantidade_gramas = float(request.form.get("quantidade"))
        item = FichaTecnica(produto_id=produto_id,
                            insumo_id=int(request.form.get("insumo_id")),
                            quantidade=quantidade_gramas / 1000)
        db.session.add(item)
        db.session.commit()
        flash("Insumo adicionado à ficha técnica.", "success")
        return redirect(url_for("produtos.ficha", produto_id=produto_id))
    return render_template("produtos/ficha.html", produto=produto, insumos=insumos,
                           ficha=FichaTecnica.query.filter_by(produto_id=produto_id).all())