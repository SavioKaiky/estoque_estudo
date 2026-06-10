from flask import Blueprint, render_template, request, redirect, url_for
from models.produto import Produto
from services.producao_service import produzir, saida_produto
 
 
producao_bp = Blueprint("producao", __name__, url_prefix="/producao")
 
 
@producao_bp.route("/", methods=["GET", "POST"])
def produzir_view():
    """Exibe formulário de produção e processa o POST."""
    produtos = Produto.query.all()
 
    if request.method == "POST":
        produto_id = int(request.form.get("produto_id"))
        quantidade = int(request.form.get("quantidade"))
 
        try:
            produzir(produto_id, quantidade)
        except ValueError as e:
            return str(e), 400
 
        return redirect(url_for("producao.produzir_view"))
 
    return render_template("producao/produzir.html", produtos=produtos)
 
 
@producao_bp.route("/venda", methods=["GET", "POST"])
def venda():
    """Exibe formulário de venda e processa o POST."""
    produtos = Produto.query.all()
 
    if request.method == "POST":
        produto_id = int(request.form.get("produto_id"))
        quantidade = int(request.form.get("quantidade"))
 
        try:
            saida_produto(produto_id, quantidade)
        except ValueError as e:
            return str(e), 400
 
        return redirect(url_for("producao.venda"))
 
    return render_template("producao/venda.html", produtos=produtos)
 