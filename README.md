# Lemon Billiard - Projeto de Mestrado

Este repositório contém os arquivos de modelagem, circuitos, código do robô e pipeline de processamento de dados para o experimento de bilhar caótico (Lemon Billiard).

## Estrutura do Repositório

```text
.
├── docs/
│   ├── manuais/               # Manuais e especificações do robô
│   ├── circuito/              # Esquemas e diagramas eletrônicos
│   └── fluxograma.md          # Fluxograma do experimento em sintaxe Mermaid
├── hardware/
│   └── 3d_printing/           # Arquivos de modelagem (.stl) e parâmetros de fatiamento
├── robot_software/            # Código-fonte embarcado de controle do robô
└── data_pipeline/
    ├── 01_frame_extractor/    # Conversão de frames de vídeo para dados de trajetória
    ├── 02_collision_detector/ # Processamento de trajetórias para detecção de colisões
    └── 03_analysis/           # Reconstrução do Espaço de Fase e cálculo do Expoente de Lyapunov
```

## Fluxo de Dados Técnico

1. **Captação**: O robô executa o experimento físico sob controle do firmware localizado em `robot_software/`.
2. **Extração**: O módulo `data_pipeline/01_frame_extractor/` realiza o rastreamento planar a partir de gravações de vídeo, convertendo coordenadas visuais em séries temporais de trajetória.
3. **Detecção**: O módulo `data_pipeline/02_collision_detector/` processa as descontinuidades vetoriais das séries temporais de trajetória para inferir os instantes e pontos exatos de colisão com as fronteiras do bilhar.
4. **Análise Não-Linear**: O módulo `data_pipeline/03_analysis/` processa as coordenadas de colisão para efetuar a reconstrução do espaço de fase e estimar os expoentes de Lyapunov, quantificando a divergência caótica do sistema dinâmico.
