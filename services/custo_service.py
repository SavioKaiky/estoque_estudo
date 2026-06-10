from models.lote_insumo import LoteInsumo
from database import db

def baixar_estoque_fifo(insumo_id, quantidade):
    lotes = LoteInsumo.query.filter_by(insumo_id=insumo_id)\
        .filter(LoteInsumo.quantidade_restante > 0)\
        .order_by(LoteInsumo.created_at.asc())\
        .all()

    restante = quantidade
    custo_total = 0

    for lote in lotes:
        if restante <= 0:
            break

        usar = min(lote.quantidade_restante, restante)

        custo_total += usar * lote.custo_unitario

        lote.quantidade_restante -= usar
        restante -= usar

    if restante > 0:
        raise Exception("Estoque insuficiente (FIFO)")

    db.session.commit()

    return custo_total

def baixar_estoque_lifo(insumo_id, quantidade):
    lotes = LoteInsumo.query.filter_by(insumo_id=insumo_id)\
        .filter(LoteInsumo.quantidade_restante > 0)\
        .order_by(LoteInsumo.created_at.desc())\
        .all()

    restante = quantidade
    custo_total = 0

    for lote in lotes:
        if restante <= 0:
            break

        usar = min(lote.quantidade_restante, restante)

        custo_total += usar * lote.custo_unitario

        lote.quantidade_restante -= usar
        restante -= usar

    if restante > 0:
        raise Exception("Estoque insuficiente (LIFO)")

    db.session.commit()

    return custo_total


def validar_estoque_fifo(insumo_id, quantidade):
    lotes = LoteInsumo.query.filter_by(insumo_id=insumo_id)\
        .filter(LoteInsumo.quantidade_restante > 0)\
        .all()

    total_disponivel = sum(l.quantidade_restante for l in lotes)

    if total_disponivel < quantidade:
        return False

    return True