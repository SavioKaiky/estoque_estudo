from database import db
from models.insumo import Insumo
from models.movimentacao_insumo import MovimentacaoInsumo
from models.lote_insumo import LoteInsumo


def movimentar_insumo(insumo_id, tipo, quantidade, motivo, valor_total=None):
    insumo = Insumo.query.get(insumo_id)

    if not insumo:
        raise Exception("Insumo não encontrado")

    if quantidade <= 0:
        raise Exception("Quantidade inválida")

    # SAÍDA (validação de estoque)
    if tipo == "saida":
        if insumo.estoque_atual < quantidade:
            raise Exception("Estoque insuficiente")

        insumo.estoque_atual -= quantidade

    elif tipo == "entrada":
        insumo.estoque_atual += quantidade
        custo_unitario = valor_total / quantidade
        lote = LoteInsumo(
            insumo_id=insumo_id,
            quantidade_inicial=quantidade,
            quantidade_restante=quantidade,
            custo_unitario=custo_unitario
        )

        db.session.add(lote)

        insumo.estoque_atual += quantidade

    else:
        raise Exception("Tipo inválido")

    mov = MovimentacaoInsumo(
        insumo_id=insumo_id,
        tipo=tipo,
        quantidade=quantidade,
        motivo=motivo
    )

    db.session.add(mov)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise