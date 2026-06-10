from flask import Blueprint, render_template, request, redirect, url_for
from database import db
from models.insumo import Insumo
from models.movimentacao_insumo import MovimentacaoInsumo
from services.estoque_service import movimentar_insumo


insumos_bp = Blueprint("insumos", __name__, url_prefix="/insumos")


@insumos_bp.route("/", methods=["GET", "POST"])
def listar_insumos():
    """Lista insumos e processa cadastro de novo insumo."""
    erro = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        unidade = request.form.get("unidade", "")
        estoque_minimo = request.form.get("estoque_minimo", 0)

        if not nome:
            erro = "O nome do insumo é obrigatório."
        else:
            novo = Insumo(
                nome=nome,
                unidade=unidade,
                estoque_minimo=float(estoque_minimo or 0)
            )
            db.session.add(novo)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            return redirect(url_for("insumos.listar_insumos"))

    insumos = Insumo.query.all()
    return render_template("insumos/listar.html", insumos=insumos, erro=erro)


@insumos_bp.route("/movimentar", methods=["POST"])
def movimentar():
    """Recebe o formulário de movimentação e delega ao service."""
    insumo_id = int(request.form.get("insumo_id"))
    tipo = request.form.get("tipo")
    quantidade = float(request.form.get("quantidade"))
    motivo = request.form.get("motivo", "")
    valor_total_raw = request.form.get("valor_total")
    valor_total = float(valor_total_raw) if valor_total_raw else None

    try:
        # Toda a lógica de negócio está no service
        movimentar_insumo(insumo_id, tipo, quantidade, motivo, valor_total)
    except ValueError as e:
        return str(e), 400

    return redirect(url_for("insumos.listar_insumos"))


@insumos_bp.route("/historico")
def historico():
    """Exibe histórico de movimentações de insumos."""
    movs = MovimentacaoInsumo.query.order_by(
        MovimentacaoInsumo.created_at.desc()
    ).all()
    return render_template("insumos/historico.html", movs=movs)
