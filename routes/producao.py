from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.produto import Produto
from services.producao_service import produzir, saida_produto
 
 
producao_bp = Blueprint("producao", __name__, url_prefix="/producao")
 
 
@producao_bp.route("/", methods=["GET", "POST"])
def produzir_view():
    produtos = Produto.query.all()
 
    if request.method == "POST":
        produto_id = int(request.form.get("produto_id"))
        quantidade = int(request.form.get("quantidade"))
 
        try:
            resultado = produzir(produto_id, quantidade)
            flash(
                f"Produção registrada! CMV: R$ {resultado['custo_total']:.2f} "
                f"(R$ {resultado['custo_unitario']:.2f}/un)",
                "success"
            )
        except ValueError as e:
            flash(str(e), "danger")
 
        return redirect(url_for("producao.produzir_view"))
 
    return render_template("producao/produzir.html", produtos=produtos)
 
 
@producao_bp.route("/venda", methods=["GET", "POST"])
def venda():
    produtos = Produto.query.all()
 
    if request.method == "POST":
        produto_id = int(request.form.get("produto_id"))
        quantidade = int(request.form.get("quantidade"))
 
        try:
            saida_produto(produto_id, quantidade)
            flash("Venda registrada com sucesso.", "success")
        except ValueError as e:
            flash(str(e), "danger")
 
        return redirect(url_for("producao.venda"))
 
    return render_template("producao/venda.html", produtos=produtos)
 