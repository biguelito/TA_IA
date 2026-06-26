# NSGA-II para mTSP com Balanceamento por Centroide

Este projeto implementa uma abordagem multiobjetivo para o problema dos múltiplos caixeiros viajantes, ou mTSP, baseada no NSGA-II. A implementação busca otimizar simultaneamente duas funções objetivo:

- `total_distance`: custo total das rotas geradas para todos os caixeiros.
- `difference_longest_shortest`: diferença entre a maior e a menor rota, usada como medida de balanceamento.

A versão original do algoritmo foi estendida com um operador de mutação por centroide. Esse operador tenta melhorar a segunda função objetivo movendo cidades de uma rota para outra com base na proximidade geométrica entre os centroides das rotas. A intenção é reduzir o desbalanceamento entre caixeiros sem degradar excessivamente o custo total.

## Estrutura Geral

O fluxo principal fica em `codigos/main.py`, que instancia `Solver` e executa o protocolo experimental completo. As principais classes são:

- `Solver`: coordena execuções, experimentos, comparação entre baseline e centroide, salvamento e análise dos resultados.
- `MOmTSP`: executa o algoritmo evolutivo multiobjetivo.
- `Result`: armazena a frente de Pareto final e calcula as métricas da execução.
- `BasicOperations`: calcula métricas auxiliares, como espaçamento e espalhamento da frente.
- `Plotter`: gera visualizações das soluções e da frente de Pareto.
- `Operators`: contém operadores genéticos, incluindo o balanceamento por centroide.

## Como Executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o experimento principal:

```bash
python codigos/main.py
```

Por padrão, o experimento completo executa as seguintes variações:

| Variação | Problema TSPLIB | Caixeiros | Iterações |
|---|---|---:|---:|
| `eil51` | `eil51` | 7 | 1400 |
| `berlin52_1` | `berlin52` | 5 | 1400 |
| `berlin52_2` | `berlin52` | 7 | 1400 |
| `eil76_1` | `eil76` | 3 | 1800 |
| `eil76_2` | `eil76` | 7 | 1800 |
| `rat99` | `rat99` | 7 | 2200 |

Os resultados são salvos em `codigos/solucoes`, incluindo arquivos de experimentos, análises, soluções e gráficos.

## Métricas Avaliadas

As execuções calculam métricas de qualidade da frente de Pareto e de comparação entre a versão baseline e a versão com centroide:

- `best_total_distance`: menor custo total encontrado na frente.
- `median_total_distance`: mediana do custo total da frente.
- `best_difference`: menor diferença entre maior e menor rota.
- `median_difference`: mediana da diferença entre maior e menor rota, principal métrica para avaliar balanceamento.
- `hypervolume`: área dominada pela frente em relação ao ponto nadir; quanto maior, melhor.
- `spacing`: regularidade da distribuição dos pontos na frente; quanto menor, melhor.
- `spreading`: cobertura da frente em relação aos extremos teóricos; quanto menor, melhor.
- `front_size`: quantidade de soluções na frente de Pareto.
- `total_exec_time`: tempo total de execução.

No protocolo experimental, a melhoria por centroide é considerada clara apenas quando satisfaz simultaneamente os critérios definidos na análise: vencer pelo menos 60% das execuções em `median_difference`, melhorar `median_difference`, melhorar `best_difference`, não piorar o hypervolume mediano e manter a degradação do melhor custo total abaixo de 5%.

## Resultados Salvos em `analysis/10-20`

A tabela abaixo resume os arquivos presentes em `codigos/solucoes/analysis/10-20`. A coluna "Melhora no balanceamento" considera principalmente a mediana de `difference_longest_shortest`. A coluna "Melhora clara pelo protocolo" usa a decisão completa registrada em cada JSON de análise.

| Instância | Prob. centroide | Median diff. baseline | Median diff. centroide | Win rate median diff. | Best diff. baseline | Best diff. centroide | Hypervolume baseline | Hypervolume centroide | Best total baseline | Best total centroide | Degradação best total | Melhora no balanceamento | Melhora clara pelo protocolo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| berlin52_1 | 0.10 | 1678.75 | 2098.00 | 25% | 136.00 | 189.50 | 62,963,553.50 | 69,076,501.25 | 8874.50 | 8828.00 | -0.52% | Não | Não |
| berlin52_2 | 0.20 | 2163.00 | 2018.50 | 60% | 443.50 | 466.00 | 71,221,901.00 | 64,295,884.75 | 9324.00 | 9310.50 | -0.14% | Parcial | Não |
| eil51 | 0.20 | 90.25 | 80.50 | 60% | 21.00 | 18.00 | 167,686.50 | 143,346.25 | 545.00 | 548.50 | 0.64% | Parcial | Não |
| eil76_1 | 0.30 | 56.00 | 49.00 | 55% | 1.00 | 0.00 | 267,911.25 | 265,971.50 | 611.00 | 611.00 | 0.00% | Parcial | Não |
| eil76_2 | 0.80 | 122.00 | 124.50 | 50% | 24.00 | 15.00 | 303,510.50 | 303,583.50 | 676.50 | 671.00 | -0.81% | Mista | Não |
| rat99 | 0.50 | 452.50 | 391.50 | 60% | 44.00 | 46.00 | 2,751,019.50 | 2,765,464.25 | 1636.00 | 1645.50 | 0.58% | Parcial | Não |

## Leitura dos Resultados

Os resultados indicam que o operador por centroide trouxe ganhos parciais em algumas instâncias, principalmente quando se observa a mediana da diferença entre rotas. Esse comportamento aparece em `berlin52_2`, `eil51`, `eil76_1` e `rat99`.

Apesar disso, nenhuma instância foi classificada como melhoria clara pelo protocolo completo. Em geral, os ganhos de balanceamento vieram acompanhados de alguma perda em outra dimensão, como piora no hypervolume, piora no melhor balanceamento isolado ou taxa de vitórias insuficiente.

Assim, a conclusão experimental atual é que o balanceamento por centroide é promissor como operador de busca, mas ainda não demonstrou superioridade consistente sobre o baseline em todos os critérios avaliados.
