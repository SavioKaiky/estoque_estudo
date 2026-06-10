from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models.produto import Produto
from models.insumo import Insumo
from models.ficha_tecnica import FichaTecnica

produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")

@produtos_bp.route("/", methods=["GET", "POST"])
def listar_produtos():
    """Lista produtos e processa cadastro de novo produto."""
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        if nome:
            novo = Produto(nome=nome)
            db.session.add(novo)
            db.session.commit()
        return redirect(url_for("produtos.listar_produtos"))
 
    produtos = Produto.query.all()
    return render_template("produtos/listar.html", produtos=produtos)

@produtos_bp.route("/<int:produto_id>/ficha", methods=["GET", "POST"])
def ficha(produto_id):
    """Exibe e edita a ficha técnica (lista de insumos) de um produto."""
    produto = Produto.query.get_or_404(produto_id)
    insumos = Insumo.query.all()

    if request.method == "POST":
        insumo_id = int(request.form.get("insumo_id"))
        quantidade = float(request.form.get("quantidade"))
 
        item = FichaTecnica(
            produto_id=produto_id,
            insumo_id=insumo_id,
            quantidade=quantidade
        )
        
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("produtos.ficha", produto_id=produto_id))

    ficha_itens = FichaTecnica.query.filter_by(produto_id=produto_id).all()
    return render_template(
        "produtos/ficha.html",
        produto=produto,
        insumos=insumos,
        ficha=ficha_itens
    )
