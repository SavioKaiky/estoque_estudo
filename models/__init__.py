# Importa todos os models para garantir que o SQLAlchemy
# os registre antes de configurar os relacionamentos.
# Sem isso, db.relationship("User") falha com InvalidRequestError.

from models.user import User
from models.insumo import Insumo, MovimentacaoInsumo
from models.produto import Produto
from models.lote_insumo import LoteInsumo
from models.ficha_tecnica import FichaTecnica
from models.movimentacao_produto import MovimentacaoProduto