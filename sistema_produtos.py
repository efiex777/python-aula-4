from collections import Counter
from typing import TypedDict


class Produto(TypedDict):
    nome: str
    preco: float
    categoria: str


def pedir_quantidade() -> int:
    while True:
        try:
            quantidade = int(input("Quantos produtos deseja cadastrar? ").strip())
            if quantidade > 0:
                return quantidade
            print("Informe uma quantidade maior que zero.")
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_preco(nome_produto: str) -> float:
    while True:
        entrada = input(f"Preço de {nome_produto}: ").strip().replace(",", ".")
        try:
            preco = float(entrada)
            if preco >= 0:
                return preco
            print("O preço não pode ser negativo.")
        except ValueError:
            print("Digite um preço válido, por exemplo 12,50.")


def cadastrar_produtos() -> list[Produto]:

    produtos: list[Produto] = []
    quantidade = pedir_quantidade()

    for numero in range(1, quantidade + 1):
        print(f"\nCadastro do produto {numero}:")

        nome = input("Nome: ").strip()
        while not nome:
            print("O nome não pode ficar vazio.")
            nome = input("Nome: ").strip()

        preco = ler_preco(nome)

        categoria = input("Categoria: ").strip()
        while not categoria:
            print("A categoria não pode ficar vazia.")
            categoria = input("Categoria: ").strip()

        produtos.append({
            "nome": nome,
            "preco": preco,
            "categoria": categoria,
        })

    return produtos


def escolher_criterio() -> str:

    while True:
        criterio = input(
            "\nFiltrar produtos (A) acima ou (B) abaixo do preço? "
        ).strip().lower()
        if criterio in {"a", "b"}:
            return criterio
        print("Escolha A para acima ou B para abaixo.")


def filtrar_por_preco(produtos: list[Produto]) -> list[Produto]:

    criterio = escolher_criterio()
    limite = ler_preco("limite para filtragem")

    if criterio == "a":
        return [produto for produto in produtos if produto["preco"] > limite]
    return [produto for produto in produtos if produto["preco"] < limite]


def exibir_produtos(titulo: str, produtos: list[Produto]) -> None:
    print(f"\n{titulo}")
    if not produtos:
        print("  Nenhum produto encontrado.")
        return

    for produto in produtos:
        print(
            f"  {produto['nome']} | "
            f"€{produto['preco']:.2f} | {produto['categoria']}"
        )


def exibir_resumo_estoque(produtos: list[Produto]) -> None:
    if not produtos:
        print("\nResumo do estoque: nenhum produto cadastrado.")
        return

    valor_total = sum(produto["preco"] for produto in produtos)
    categorias = [produto["categoria"] for produto in produtos]
    categoria_mais_comum = Counter(categorias).most_common(1)[0][0]

    print("\nResumo do estoque:")
    print(f"  Total de produtos: {len(produtos)}")
    print(f"  Valor total: €{valor_total:.2f}")
    print(f"  Categoria mais comum: {categoria_mais_comum}")


def gerar_relatorio(produtos: list[Produto]) -> None:

    filtrados = filtrar_por_preco(produtos)
    em_ordem_crescente = sorted(produtos, key=lambda produto: produto["preco"])
    em_ordem_decrescente = sorted(
        produtos, key=lambda produto: produto["preco"], reverse=True
    )

    categorias_unicas = sorted({produto["categoria"] for produto in produtos})
    precos = [produto["preco"] for produto in produtos]
    menor_preco = min(precos)
    maior_preco = max(precos)
    preco_medio = sum(precos) / len(precos)

    print("\n========== RELATÓRIO DE PRODUTOS ==========")
    exibir_produtos("Produtos cadastrados:", produtos)
    exibir_resumo_estoque(produtos)
    exibir_produtos("Produtos após a filtragem:", filtrados)
    exibir_produtos("Produtos por preço crescente:", em_ordem_crescente)
    exibir_produtos("Produtos por preço decrescente:", em_ordem_decrescente)

    print("\nCategorias únicas:")
    for categoria in categorias_unicas:
        print(f"  {categoria}")

    print("\nEstatísticas (tupla: menor, maior, média):")
    print(
        f"  Menor preço: €{menor_preco:.2f}\n"
        f"  Maior preço: €{maior_preco:.2f}\n"
        f"  Preço médio: €{preco_medio:.2f}"
    )
    print("===========================================")


def main() -> None:
    produtos = cadastrar_produtos()
    gerar_relatorio(produtos)


if __name__ == "__main__":
    main()