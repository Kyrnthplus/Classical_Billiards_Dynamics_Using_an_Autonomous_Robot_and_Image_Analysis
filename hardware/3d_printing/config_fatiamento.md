# Parâmetros de Fatiamento para Impressão 3D (PLA)

Este documento especifica a configuração básica de fatiamento recomendada para a fabricação das peças estruturais do robô (ex: [LemonRobot.stl](file:///media/Externos/HDEX/Dropbox/Obsidian/Quirino/10 - Anexos/10.03 - Projetos/10.03.12 - Lemon_Billiard/hardware/3d_printing/LemonRobot.stl)).

## Parâmetros Térmicos
* **Material**: PLA (Ácido Polilático)
* **Temperatura do Bico (Extrusora)**: 200 °C (padrão de referência: 190 °C - 210 °C)
* **Temperatura da Mesa (Base)**: 60 °C (padrão de referência: 50 °C - 60 °C)

## Estrutura e Preenchimento
* **Densidade de Preenchimento (Infill)**: 50% (alta resistência mecânica para o chassi)
* **Padrão de Preenchimento**: Giroide (Gyroid)
  * *Nota*: O padrão giroide distribui a resistência mecânica de forma isotrópica (em três dimensões) e reduz tensões de cisalhamento em velocidades de impressão elevadas.
* **Altura da Camada (Layer Height)**: 0.2 mm (padrão para equilíbrio entre acabamento superficial e tempo de impressão)
* **Perímetros (Paredes)**: 3 voltas externas (mínimo de 1.2 mm de espessura de parede)
* **Camadas de Topo/Base**: 4 camadas sólidas

## Resfriamento e Velocidade
* **Velocidade de Impressão**: 50 mm/s (perímetros externos: 35 mm/s; preenchimento: 60 mm/s)
* **Ventoinha de Resfriamento**: 100% ativa (desligada apenas na primeira camada para melhorar a adesão à mesa)
* **Suportes**: Ativar suporte automático para ângulos de balanço (overhangs) superiores a 45°.
