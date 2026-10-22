"""Mede a quicksort em 20 mil elementos e cria CSV e gráfico SVG."""

import csv
import platform
import random
import statistics
import time
from pathlib import Path

from ordenacao import quicksort_hibrida, quicksort_pura


TAMANHO = 20_000
REPETICOES = 9
CORTES = (1, 5, 10, 16, 20, 32, 50, 100, 200)
SEMENTE_DADOS = 20261022
SAIDA_CSV = Path("resultados.csv")
SAIDA_SVG = Path("grafico.svg")


def medir() -> list[tuple[str, float]]:
    gerador = random.Random(SEMENTE_DADOS)
    dados = [gerador.randrange(1_000_000) for _ in range(TAMANHO)]
    esperado = sorted(dados)
    tempos: dict[str, list[float]] = {str(corte): [] for corte in CORTES}
    tempos["pura"] = []

    for repeticao in range(REPETICOES):
        ordem = list(tempos)
        random.Random(SEMENTE_DADOS + repeticao).shuffle(ordem)
        for nome in ordem:
            copia = dados.copy()
            semente_pivo = 10_000 + repeticao
            inicio = time.perf_counter_ns()
            if nome == "pura":
                quicksort_pura(copia, seed=semente_pivo)
            else:
                quicksort_hibrida(copia, int(nome), seed=semente_pivo)
            duracao_ms = (time.perf_counter_ns() - inicio) / 1_000_000
            if copia != esperado:
                raise AssertionError(f"resultado incorreto: {nome}")
            tempos[nome].append(duracao_ms)

    return [(nome, statistics.median(tempos[nome])) for nome in tempos]


def gravar_csv(resultados: list[tuple[str, float]]) -> None:
    with SAIDA_CSV.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(("corte", "tempo_mediano_ms"))
        for nome, tempo in resultados:
            escritor.writerow((nome, f"{tempo:.4f}"))


def gravar_grafico(resultados: list[tuple[str, float]]) -> None:
    valores = [tempo for nome, tempo in resultados if nome != "pura"]
    pura = dict(resultados)["pura"]
    minimo = min(valores + [pura])
    maximo = max(valores + [pura])
    limite_inferior = max(0.0, minimo - 3)
    limite_superior = maximo + 3
    esquerda, direita, topo, base = 95, 765, 65, 380
    x = lambda i: esquerda + i * (direita - esquerda) / (len(CORTES) - 1)
    y = lambda tempo: base - (tempo - limite_inferior) * (base - topo) / (limite_superior - limite_inferior)
    pontos = " ".join(f"{x(i):.1f},{y(tempo):.1f}" for i, tempo in enumerate(valores))
    circulos = "\n".join(
        f'<circle cx="{x(i):.1f}" cy="{y(tempo):.1f}" r="5" fill="#2563eb"/>'
        for i, tempo in enumerate(valores)
    )
    marcas_x = "\n".join(
        f'<text x="{x(i):.1f}" y="402" text-anchor="middle">{corte}</text>'
        for i, corte in enumerate(CORTES)
    )
    marcas_y = "\n".join(
        f'<text x="82" y="{y(limite_inferior + i * (limite_superior - limite_inferior) / 5) + 4:.1f}" text-anchor="end">{limite_inferior + i * (limite_superior - limite_inferior) / 5:.1f}</text>'
        for i in range(6)
    )
    linhas_y = "\n".join(
        f'<line x1="{esquerda}" y1="{y(limite_inferior + i * (limite_superior - limite_inferior) / 5):.1f}" x2="{direita}" y2="{y(limite_inferior + i * (limite_superior - limite_inferior) / 5):.1f}" stroke="#e2e8f0"/>'
        for i in range(6)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="850" height="470" viewBox="0 0 850 470">
<rect width="850" height="470" fill="white"/>
<g font-family="Arial, sans-serif" fill="#334155" font-size="13">
<text x="425" y="30" text-anchor="middle" font-size="20" font-weight="bold">Tempo por corte — 20.000 elementos</text>
{linhas_y}
<line x1="{esquerda}" y1="{base}" x2="{direita}" y2="{base}" stroke="#334155" stroke-width="2"/>
<line x1="{esquerda}" y1="{topo}" x2="{esquerda}" y2="{base}" stroke="#334155" stroke-width="2"/>
{marcas_x}
{marcas_y}
<line x1="{esquerda}" y1="{y(pura):.1f}" x2="{direita}" y2="{y(pura):.1f}" stroke="#64748b" stroke-width="2" stroke-dasharray="6 5"/>
<text x="{direita}" y="{y(pura) - 9:.1f}" text-anchor="end">quicksort pura: {pura:.4f} ms</text>
<polyline points="{pontos}" fill="none" stroke="#2563eb" stroke-width="3"/>
{circulos}
<text x="425" y="445" text-anchor="middle" font-size="15">Corte (elementos)</text>
<text x="23" y="225" text-anchor="middle" transform="rotate(-90 23 225)" font-size="15">Tempo mediano (ms)</text>
</g></svg>'''
    SAIDA_SVG.write_text(svg, encoding="utf-8")


def main() -> None:
    resultados = medir()
    gravar_csv(resultados)
    gravar_grafico(resultados)
    for nome, tempo in resultados:
        print(f"{nome:>4}: {tempo:.4f} ms")
    print(f"Python {platform.python_version()} | {platform.system()} {platform.release()}")


if __name__ == "__main__":
    main()
