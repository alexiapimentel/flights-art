# Flights Art

Projeto criado para a disciplina de Tópicos Especiais em Computação Gráfica IV, do mestrado em Engenharia da Computação, Coppe UFRJ.

Nesse projeto, transformo dados em arte, utilizando dados reais de voos realizados no Brasil em dezembro de 2021. Os dados podem ser obtidos [no portal de dados da ANAC](https://www.anac.gov.br/acesso-a-informacao/dados-abertos).

## Processo de criação:
___

* Os voos são agrupados em intervalos de 1h.
* Para cada intervalo a distância geodésica total é computada.
* Os voos tem sua cor atribuida de acordo com a distância total percorrida no intervalo de 1h a qual pertence. Essa cor é gerada dentro de uma escala de cores das distâncias totais percorridas.
* Para tornar criar padrões de cores diferentes, são escolhidos cinco escalas de cores que serão aleatóriamente distríbuidas entre os voos agrupados.
* Assim, os voos vão gerando padrões em tela. Quando um novo dia se inícia, a tela também é reiniciada.


## Referências
___

Esse projeto é inspirado na obra [Flight Patterns, de Aaron Klobin](http://www.aaronkoblin.com/project/flight-patterns/)


## Código Fonte
___
[Código disponível no Git Hub](https://github.com/alexiapimentel/flights-art)