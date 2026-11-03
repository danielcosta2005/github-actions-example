"""Carrinho de compras em memória, sem dependências externas."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def _decimal(valor):
    try:
        numero = Decimal(str(valor))
    except InvalidOperation:
        raise ValueError("Informe um número válido.") from None
    if not numero.is_finite():
        raise ValueError("Informe um número finito.")
    return numero


class Carrinho:
    def __init__(self):
        self._produtos = {}
        self._desconto = Decimal("0")

    def adicionar_produto(self, nome, preco, quantidade=1):
        """Adiciona unidades de um produto com preço positivo em reais."""
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("O nome do produto não pode ser vazio.")
        if type(quantidade) is not int or quantidade <= 0:
            raise ValueError("A quantidade deve ser um inteiro positivo.")
        preco = _decimal(preco)
        if preco <= 0 or preco != preco.quantize(Decimal("0.01")):
            raise ValueError("O preço deve ser positivo e ter até duas casas decimais.")

        if nome in self._produtos:
            preco_atual, quantidade_atual = self._produtos[nome]
            if preco != preco_atual:
                raise ValueError("O produto já possui outro preço no carrinho.")
            quantidade += quantidade_atual
        self._produtos[nome] = (preco, quantidade)

    def remover_produto(self, nome):
        """Remove todas as unidades do produto informado."""
        if nome not in self._produtos:
            raise ValueError("Produto não encontrado no carrinho.")
        del self._produtos[nome]

    def subtotal(self):
        """Retorna a soma dos preços multiplicados pelas quantidades."""
        return sum(
            (preco * quantidade for preco, quantidade in self._produtos.values()),
            Decimal("0.00"),
        )

    def aplicar_desconto(self, percentual):
        """Define um desconto de 0 a 100%, substituindo o desconto anterior."""
        percentual = _decimal(percentual)
        if not 0 <= percentual <= 100:
            raise ValueError("O desconto deve estar entre 0 e 100%.")
        self._desconto = percentual

    def total(self):
        """Retorna o subtotal com desconto, arredondado para centavos."""
        valor = self.subtotal() * (1 - self._desconto / 100)
        return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
