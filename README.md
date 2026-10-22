# Ordenação híbrida

Implementei uma quicksort com pivô aleatório e partição em menores, iguais e maiores para comparar seu desempenho com uma versão que usa inserção em trechos pequenos.

## Executar o experimento

Use Python 3.10 ou superior. Não há dependências externas.

```bash
git clone https://github.com/Euclidespilon-Neto/ordenacao_hibrida.git
cd ordenacao_hibrida
python experimento.py
```

O comando mede a quicksort pura e os cortes `1, 5, 10, 16, 20, 32, 50, 100 e 200` em 20.000 elementos. Ele confere a ordenação e grava os tempos em `resultados.csv` e o gráfico em `grafico.svg`.

## Usar a ordenação

```python
from ordenacao import quicksort_hibrida

valores = [8, 3, 8, 1, 5]
quicksort_hibrida(valores, corte=20)
print(valores)  # [1, 3, 5, 8, 8]
```

A função ordena a lista no próprio lugar. `corte` define o tamanho abaixo do qual um trecho passa para a inserção; `seed` é opcional e reproduz a sequência de pivôs. Para executar apenas a quicksort, use `quicksort_pura(valores)`. Com `corte=1`, a inserção não é chamada.

## Resultados registrados

Entre os cortes avaliados, **20** teve o menor tempo mediano: **19,6018 ms** em nove repetições. A quicksort pura levou **23,5732 ms**, uma redução de **16,8%** no tempo medido. A tabela completa, o gráfico e a análise dos cortes grandes estão em [RELATORIO.md](RELATORIO.md).
