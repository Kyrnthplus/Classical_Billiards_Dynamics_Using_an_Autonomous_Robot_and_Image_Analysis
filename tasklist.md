# Cronograma de Atividades Pendentes - Lemon Billiard

Este documento lista todas as tarefas necessárias para a conclusão dos objetivos do projeto de mestrado, divididas por áreas de atuação.

## 1. Documentação e Planejamento
- [X] **Compilar manuais do robô**: Reunir e listar as especificações técnicas, manuais de motores, sensores e atuadores na pasta `docs/manuais/`.
- [X] **Esquema de circuito eletrônico**: Desenhar e incluir o diagrama esquemático das conexões eletrônicas do robô (ex: conexões Arduino, shields e drivers) na pasta `docs/circuito/`.

## 2. Hardware e Impressão 3D
- [X] **Organização de arquivos CAD**: Catalogar e adicionar os arquivos finais de modelagem 3D (`.stl`) na pasta `hardware/3d_printing/`.
- [X] **Configurações de fatiamento**: Criar um arquivo descritivo contendo os parâmetros ideais de impressão (temperatura, densidade de preenchimento, velocidade, suporte) para cada peça `.stl`.

## 3. Software do Robô (Firmware Embarcado)
- [X] **Estrutura de arquivos**: Transferir o código-fonte de controle embarcado do robô (firmware do Arduino) para a pasta `robot_software/`.
- [ ] **Refatoração e documentação**: Limpar o código embarcado, organizar funções de movimentação e controle, e documentar os principais parâmetros de controle do robô.

## 4. Pipeline de Processamento e Análise de Dados
- [ ] **Rastreamento de trajetórias reais**: Executar o script MATLAB `data_pipeline/01_frame_extractor/robo_stadium_mac.m` para processar sequências de vídeo de experimentos físicos reais e gerar as coordenadas em `data/raw/`.
- [ ] **Processamento em lote**: Executar o pipeline (`main.py` opção 2 e 3) para processar as trajetórias reais obtidas, gerando os respectivos coeficientes geométricos ($\gamma$), expoentes de Lyapunov ($\lambda$) e mapas de Poincaré em `data/results/`.
- [ ] **Análise comparativa**: Contrastar os resultados experimentais reais obtidos com as trajetórias teóricas geradas pelo simulador (`simulator.py`) para validar o modelo de bilhar caótico.
