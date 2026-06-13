from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db
from models.insumo import Insumo
from models.movimentacao_insumo import MovimentacaoInsumo
from services.estoque_service import movimentar_insumo
 
 
insumos_bp = Blueprint("insumos", __name__, url_prefix="/insumos")
 
 
@insumos_bp.route("/", methods=["GET", "POST"])
def listar_insumos():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        unidade = request.form.get("unidade", "")
        estoque_minimo = request.form.get("estoque_minimo", 0)
 
        if not nome:
            flash("O nome do insumo é obrigatório.", "danger")
        else:
            novo = Insumo(
                nome=nome,
                unidade=unidade,
                estoque_minimo=float(estoque_minimo or 0)
            )
            db.session.add(novo)
            try:
                db.session.commit()
                flash(f"Insumo '{nome}' cadastrado com sucesso.", "success")
            except Exception:
                db.session.rollback()
                flash("Erro ao salvar insumo.", "danger")
 
        return redirect(url_for("insumos.listar_insumos"))
 
    insumos = Insumo.query.all()
    return render_template("insumos/listar.html", insumos=insumos)
 
 
@insumos_bp.route("/movimentar", methods=["POST"])
def movimentar():
    insumo_id = int(request.form.get("insumo_id"))
    tipo = request.form.get("tipo")
    quantidade = float(request.form.get("quantidade"))
    motivo = request.form.get("motivo", "")
    valor_total_raw = request.form.get("valor_total")
    valor_total = float(valor_total_raw) if valor_total_raw else None
 
    try:
        movimentar_insumo(insumo_id, tipo, quantidade, motivo, valor_total)
        flash("Movimentação registrada com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "danger")
 
    return redirect(url_for("insumos.listar_insumos"))
 
 
@insumos_bp.route("/historico")
def historico():
    movs = MovimentacaoInsumo.query.order_by(
        MovimentacaoInsumo.created_at.desc()
    ).all()
    return render_template("insumos/historico.html", movs=movs)
 