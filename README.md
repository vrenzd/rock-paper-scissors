# freeCodeCamp - Rock Paper Scissors

Solução para o projeto **Rock Paper Scissors** da certificação Machine Learning with Python do freeCodeCamp.

## Objetivo

Criar uma função `player(prev_play)` que jogue contra quatro bots:

- Quincy
- Abbey
- Kris
- Mrugesh

Para passar no projeto, o jogador precisa vencer pelo menos 60% das partidas contra cada bot em partidas de 1000 rodadas.

## Estratégia usada

A solução usa previsores adaptativos:

1. Um previsor específico para o padrão do Quincy.
2. Um previsor específico para o comportamento do Kris.
3. Um previsor específico para o comportamento do Mrugesh.
4. Um previsor específico para o comportamento da Abbey.
5. Previsores genéricos baseados em cadeias de Markov simples.

A cada rodada, o código mede qual previsor está acertando mais e usa a melhor previsão para escolher a jogada que vence o próximo movimento provável do adversário.

## Como executar

```bash
python main.py
```

Para executar os testes, descomente a última linha do `main.py`:

```python
main(module="test_module", exit=False)
```

Ou execute diretamente:

```bash
python -m unittest test_module.py
```
