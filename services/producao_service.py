from database import db
from models.produto import Produto
from models.insumo import Insumo
from models.ficha_tecnica import FichaTecnica
from models.movimentacao_produto import MovimentacaoProduto
from models.movimentacao_insumo import MovimentacaoInsumo
from services.custo_service import baixar_estoque_fifo, validar_estoque_fifo


def produzir(produto_id: int, quantidade: int) -> dict:
    """
    Orquestra a produção de um produto acabado:
      1. Valida existência do produto e da ficha técnica
      2. Verifica saldo de todos os insumos ANTES de alterar qualquer coisa
      3. Consome insumos via FIFO acumulando o CMV
      4. Atualiza estoque do produto e registra movimentações
    
    Retorna dict com custo_total e custo_unitario da produção.
    """
    produto = Produto.query.get(produto_id)
    if not produto:
        raise ValueError("Produto não encontrado")

    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero")

    ficha = FichaTecnica.query.filter_by(produto_id=produto_id).all()
    if not ficha:
        raise ValueError("Produto sem ficha técnica cadastrada")

    # ETAPA 1 — Validar TODOS os insumos antes de alterar qualquer coisa
    for item in ficha:
        insumo = Insumo.query.get(item.insumo_id)
        consumo = item.quantidade * quantidade
        if not validar_estoque_fifo(insumo.id, consumo):
            raise ValueError(f"Estoque insuficiente: {insumo.nome} "
                             f"(necessário: {consumo}, disponível em lotes)")

    # ETAPA 2 — Consumir insumos via FIFO e acumular CMV
    cmv_total = 0.0   # CORREÇÃO: declarado ANTES de ser usado

    for item in ficha:
        insumo = Insumo.query.get(item.insumo_id)
        consumo = item.quantidade * quantidade

        custo = baixar_estoque_fifo(insumo.id, consumo)
        cmv_total += custo

        insumo.estoque_atual -= consumo

        mov_insumo = MovimentacaoInsumo(
            insumo_id=insumo.id,
            tipo="saida",
            quantidade=consumo,
            motivo="produção"
        )
        db.session.add(mov_insumo)

    # ETAPA 3 — Registrar entrada do produto acabado
    cmv_unitario = cmv_total / quantidade  # CORREÇÃO: calculado DEPOIS de cmv_total

    produto.estoque_atual += quantidade

    mov_produto = MovimentacaoProduto(
        produto_id=produto_id,
        tipo="entrada",
        quantidade=quantidade,
        motivo="produção",
        custo_total=cmv_total,
        custo_unitario=cmv_unitario
    )
    db.session.add(mov_produto)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {"custo_total": cmv_total, "custo_unitario": cmv_unitario}


def saida_produto(produto_id: int, quantidade: int) -> None:
    """
    Registra venda/saída de produto acabado.
    Extraído de utils/produto_saida.py — sem alteração de comportamento.
    """
    produto = Produto.query.get(produto_id)
    if not produto:
        raise ValueError("Produto não encontrado")

    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero")

    if produto.estoque_atual < quantidade:
        raise ValueError(f"Estoque insuficiente. Disponível: {produto.estoque_atual}")

    produto.estoque_atual -= quantidade

    mov = MovimentacaoProduto(
        produto_id=produto_id,
        tipo="saida",
        quantidade=quantidade,
        motivo="venda"
    )
    db.session.add(mov)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise