from decimal import Decimal

import pytest

from carrinho import Carrinho


def test_carrinho_vazio():
    carrinho = Carrinho()
    assert carrinho.subtotal() == Decimal("0.00")
    assert carrinho.total() == Decimal("0.00")


def test_adicionar_produtos_com_quantidades():
    carrinho = Carrinho()
    carrinho.adicionar_produto("Caderno", "12.50", 2)
    carrinho.adicionar_produto("Caneta", "3.00")
    assert carrinho.subtotal() == Decimal("28.00")


def test_adicionar_mesmo_produto_acumula_quantidade():
    carrinho = Carrinho()
    carrinho.adicionar_produto("Caderno", "12.50")
    carrinho.adicionar_produto("Caderno", "12.50", 2)
    assert carrinho.subtotal() == Decimal("37.50")


def test_rejeitar_preco_diferente_para_mesmo_produto():
    carrinho = Carrinho()
    carrinho.adicionar_produto("Caneta", "3.00")
    with pytest.raises(ValueError):
        carrinho.adicionar_produto("Caneta", "4.00")
    assert carrinho.subtotal() == Decimal("3.00")


def test_remover_produto_remove_todas_as_unidades():
    carrinho = Carrinho()
    carrinho.adicionar_produto("Caderno", "12.50", 2)
    carrinho.adicionar_produto("Caneta", "3.00")
    carrinho.remover_produto("Caderno")
    assert carrinho.subtotal() == Decimal("3.00")


def test_remover_produto_inexistente():
    carrinho = Carrinho()
    with pytest.raises(ValueError):
        carrinho.remover_produto("Inexistente")


@pytest.mark.parametrize("percentual, esperado", [(0, "100.00"), (10, "90.00"), (100, "0.00")])
def test_aplicar_desconto(percentual, esperado):
    carrinho = Carrinho()
    carrinho.adicionar_produto("Mochila", "100.00")
    carrinho.aplicar_desconto(percentual)
    assert carrinho.total() == Decimal(esperado)
    assert carrinho.subtotal() == Decimal("100.00")


def test_novo_desconto_substitui_anterior():
    carrinho = Carrinho()
    carrinho.adicionar_produto("Mochila", "100.00")
    carrinho.aplicar_desconto(10)
    carrinho.aplicar_desconto(20)
    assert carrinho.total() == Decimal("80.00")


def test_valores_decimais_e_arredondamento():
    carrinho = Carrinho()
    carrinho.adicionar_produto("Produto A", "0.10")
    carrinho.adicionar_produto("Produto B", "0.20")
    assert carrinho.subtotal() == Decimal("0.30")
    carrinho.aplicar_desconto(15)
    assert carrinho.total() == Decimal("0.26")


@pytest.mark.parametrize("nome", ["", "   ", None])
def test_rejeitar_nome_invalido(nome):
    carrinho = Carrinho()
    with pytest.raises(ValueError):
        carrinho.adicionar_produto(nome, "10.00")
    assert carrinho.total() == Decimal("0.00")


@pytest.mark.parametrize("preco", [0, -1, "abc", "NaN", "Infinity", "1.001"])
def test_rejeitar_preco_invalido(preco):
    carrinho = Carrinho()
    with pytest.raises(ValueError):
        carrinho.adicionar_produto("Caderno", preco)
    assert carrinho.total() == Decimal("0.00")


@pytest.mark.parametrize("quantidade", [0, -1, 1.5, True, "2"])
def test_rejeitar_quantidade_invalida(quantidade):
    carrinho = Carrinho()
    with pytest.raises(ValueError):
        carrinho.adicionar_produto("Caderno", "10.00", quantidade)
    assert carrinho.total() == Decimal("0.00")


@pytest.mark.parametrize("percentual", [-1, 101, "abc", "NaN", "Infinity"])
def test_rejeitar_desconto_invalido_sem_alterar_desconto_atual(percentual):
    carrinho = Carrinho()
    carrinho.adicionar_produto("Mochila", "100.00")
    carrinho.aplicar_desconto(10)
    with pytest.raises(ValueError):
        carrinho.aplicar_desconto(percentual)
    assert carrinho.total() == Decimal("90.00")
