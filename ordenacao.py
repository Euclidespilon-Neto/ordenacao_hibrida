"""Quicksort com pivô aleatório, partição de três vias e corte por inserção."""

import random


def ordenacao_por_insercao(valores: list[int], inicio: int, fim: int) -> None:
    """Ordena, no próprio vetor, o intervalo inclusivo [inicio, fim]."""
    for i in range(inicio + 1, fim + 1):
        atual = valores[i]
        j = i - 1
        while j >= inicio and valores[j] > atual:
            valores[j + 1] = valores[j]
            j -= 1
        valores[j + 1] = atual


def quicksort_hibrida(valores: list[int], corte: int, seed: int | None = None) -> None:
    """Ordena in-place; trechos com menos de `corte` itens usam inserção."""
    if not isinstance(corte, int) or corte < 1:
        raise ValueError("corte deve ser um inteiro positivo")

    gerador = random.Random(seed)

    def ordenar(inicio: int, fim: int) -> None:
        while inicio < fim:
            if fim - inicio + 1 < corte:
                ordenacao_por_insercao(valores, inicio, fim)
                return

            pivo = valores[gerador.randrange(inicio, fim + 1)]
            menores, atual, maiores = inicio, inicio, fim
            while atual <= maiores:
                if valores[atual] < pivo:
                    valores[menores], valores[atual] = valores[atual], valores[menores]
                    menores += 1
                    atual += 1
                elif valores[atual] > pivo:
                    valores[atual], valores[maiores] = valores[maiores], valores[atual]
                    maiores -= 1
                else:
                    atual += 1

            # Processar o lado menor por recursão limita o uso da pilha.
            if menores - inicio < fim - maiores:
                ordenar(inicio, menores - 1)
                inicio = maiores + 1
            else:
                ordenar(maiores + 1, fim)
                fim = menores - 1

    ordenar(0, len(valores) - 1)


def quicksort_pura(valores: list[int], seed: int | None = None) -> None:
    """Executa somente quicksort: corte 1 nunca aciona a inserção."""
    quicksort_hibrida(valores, corte=1, seed=seed)
