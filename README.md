# Carrinho de compras com GitHub Actions

Projeto simples em Python para a atividade prática 6 de Engenharia de Software 2.
O objetivo é demonstrar testes unitários com `pytest` em diferentes sistemas
operacionais e versões do Python.

## Funcionamento

A classe `Carrinho`, em [carrinho.py](carrinho.py), permite:

- Adicionar produtos pelo nome, preço e quantidade (padrão: 1).
- Acumular quantidades ao adicionar novamente um produto com o mesmo nome e preço.
- Remover todas as unidades de um produto pelo nome.
- Calcular o subtotal e o total com desconto percentual.

Preços devem ser positivos e ter até duas casas decimais; quantidades devem ser
inteiros positivos. Nomes vazios, produtos inexistentes na remoção e descontos
fora de 0 a 100% geram `ValueError`. Um produto já adicionado não pode receber
outro preço. Cada novo desconto substitui o anterior e vale para todo o carrinho.

Valores monetários usam `Decimal` da biblioteca padrão. Prefira informar preços
como strings; o total é arredondado para centavos com `ROUND_HALF_UP`.
Não há banco de dados ou interface gráfica.

```python
from carrinho import Carrinho

carrinho = Carrinho()
carrinho.adicionar_produto("Caderno", "12.50", quantidade=2)
carrinho.adicionar_produto("Caneta", "3.00")
carrinho.aplicar_desconto(10)

print(carrinho.subtotal())  # 28.00
print(carrinho.total())     # 25.20

carrinho.remover_produto("Caneta")
print(carrinho.total())     # 22.50
```

## Executar os testes localmente

Com Python 3.11 ou 3.12 instalado, execute na raiz do projeto:

```sh
python -m venv .venv
```

Ative o ambiente virtual no Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Ou no Linux/macOS:

```sh
source .venv/bin/activate
```

Instale a dependência de testes e execute a suíte:

```sh
python -m pip install -r requirements.txt
python -m pytest -v
```

Os testes em [tests/test_carrinho.py](tests/test_carrinho.py) cobrem adição,
remoção, subtotal, desconto, arredondamento e entradas inválidas. Alguns usam
parametrização para verificar vários valores para o mesmo comportamento.

## GitHub Actions

O workflow [.github/workflows/tests.yml](.github/workflows/tests.yml) executa a
cada `push` em qualquer branch e também em pull requests. A matriz gera seis jobs:

| Sistema operacional | Versões do Python |
| --- | --- |
| Ubuntu (`ubuntu-latest`) | 3.11 e 3.12 |
| Windows (`windows-latest`) | 3.11 e 3.12 |
| macOS (`macos-latest`) | 3.11 e 3.12 |

Cada job obtém o código, configura o Python, instala o `pytest`, verifica a
compilação do módulo com `compileall` e executa todos os testes. Como o projeto
é um módulo Python simples, não é necessário gerar um pacote ou executável.
A opção `fail-fast: false` permite concluir as demais combinações se uma falhar.

Após publicar os arquivos no GitHub, abra a aba **Actions** e selecione a execução
mais recente em que os seis jobs passaram. Copie a URL dessa execução para a
submissão no Moodle, no formato:

```text
https://github.com/SEU_USUARIO/SEU_REPOSITORIO/actions/runs/ID_DA_EXECUCAO
```
