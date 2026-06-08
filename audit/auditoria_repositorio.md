# Relatório de Auditoria do Repositório (Legado e Source)

Este documento apresenta a análise dos arquivos legados encontrados no diretório `source/` e subdiretórios, definindo sua relevância e destinação lógica no novo esquema organizacional do repositório.

## 1. Núcleo Algorítmico (Arquivos Essenciais)

O arquivo principal que contém toda a lógica de processamento e análise é o `source/AIO6.2Tiago.py` (e sua cópia idêntica no diretório legado). Ele consolida:
- Tratamento e rotação de trajetórias físicas.
- Filtro passa-baixa de Butterworth.
- Algoritmo de identificação de colisões (`StraightWalk` & `Col`).
- Ajuste geométrico de contorno (Lemon Billiard) via regressão circular.
- Reconstrução de Espaço de Fase e cálculo do Expoente de Lyapunov.
- Geração de gráficos complexos (Recorrência, Poincaré, Lyapunov).

### Proposta para o Código-Fonte:
- O script monolítico `AIO6.2Tiago.py` deve ser modularizado e dividido nas pastas correspondentes do pipeline:
  - **`data_pipeline/01_frame_extractor/`**: Lógica de leitura de trajetórias brutas, rotação e normalização.
  - **`data_pipeline/02_collision_detector/`**: Filtro Butterworth e rotina de detecção de colisões.
  - **`data_pipeline/03_analysis/`**: Cálculo do expoente de Lyapunov, mapeamento de Poincaré e geração de plots.

---

## 2. Inventário de Arquivos do Legado e Destinação Proposta

| Arquivo/Pasta Original | Tipo de Conteúdo | Status de Relevância | Ação Recomendada |
| :--- | :--- | :--- | :--- |
| `AIO6.2Tiago.py` | Código principal ativo. | **Crítico** | Manter e usar como base para a partição do pipeline. |
| `AIO6.2Tiago.py~` | Backup temporário do editor. | **Irrelevante** | Descartar / Adicionar ao `.gitignore`. |
| `AIO5.9.1-I.py` a `AIO6.2.py` | Versões incrementais antigas (monolítico). | **Legado redundante** | Mover para pasta de histórico `docs/historico_codigo/` ou descartar. |
| `All_In_One*.py` | Protótipos anteriores de integração. | **Legado redundante** | Mover para pasta de histórico ou descartar. |
| `Lemon_Simulator*.py` | Simulador numérico do bilhar. | **Útil** | Mover para `/robot_software/` (caso sirva de gêmeo digital) ou `/data_pipeline/03_analysis/`. |
| `LyapLemon.py`, `SimetriaLyap.py` | Scripts auxiliares de Lyapunov. | **Útil** | Incorporar na pasta `/data_pipeline/03_analysis/`. |
| `G*.py`, `GCP*.py`, `GSP*.py` | Scripts de plotagem de gráficos antigos. | **Legado** | Avaliar se há rotinas de gráficos não inclusas no script principal, senão descartar. |
| `Passo.py`, `Metragem.py` | Scripts utilitários de medição física. | **Legado** | Mover para `/docs/` ou descartar se obsoletos. |
| `Gamma05-Fusion.3mf` (16.9 MB) | Modelo 3D completo do experimento. | **Crítico (Hardware)** | Mover para `hardware/3d_printing/`. |
| `Trava-Body.3mf`, `Trava.FCStd` | Arquivos CAD de peças do bilhar. | **Crítico (Hardware)** | Mover para `hardware/3d_printing/`. |
| `Trava-Body.gcode` | Arquivo fatiado de manufatura. | **Opcional** | Manter em `hardware/3d_printing/` apenas se for a versão final homologada. |
| `Apr1.odt` a `Apr4.pdf` | Rascunhos de relatórios/apresentações. | **Documentação** | Mover para `docs/relatorios/`. |
| `2024-02-01-03.pdf` / `.png` | Dados de referência visual. | **Documentação** | Mover para `docs/`. |
| `DadosCrus/`, `DadosExp/` | Arquivos de coordenadas brutas (`.txt`). | **Dados de Entrada** | Adicionar amostras pequenas em `data_pipeline/test_data/` para testes locais; o restante deve ser ignorado no Git. |
| `DadosTratados/` | Arquivos processados (`.dat`). | **Dados de Saída** | Não devem ser versionados no Git (adicionar ao `.gitignore`). |
| `Gráficos/` | Plots de saída gerados (`.png`, `.pdf`). | **Resultados** | Não devem ser versionados no Git (adicionar ao `.gitignore`). |
| `Lyapunov/` | Resultados numéricos calculados. | **Resultados** | Não devem ser versionados no Git (adicionar ao `.gitignore`). |
| `Old/`, `Outros/` | Pastas de descarte desorganizadas. | **Irrelevante** | Descartar ou arquivar fora do repositório de produção. |

---

## 3. Configuração de Controle de Versão (`.gitignore`)

Para evitar inflar o repositório com dados gerados temporários ou de grande escala, propõe-se a exclusão das seguintes extensões e pastas:

```text
# Arquivos temporários e backups
*~
*.bak
*.tmp
__pycache__/

# Dados gerados e gráficos de saída
data_pipeline/01_frame_extractor/DadosTratados/
data_pipeline/03_analysis/Lyapunov/
data_pipeline/03_analysis/Gráficos/
source/APR2.4 (Dissertação)/DadosTratados/
source/APR2.4 (Dissertação)/Gráficos/
source/APR2.4 (Dissertação)/Lyapunov/

# Arquivos CAD pesados de fatiamento que não sejam modelos fonte (.gcode)
*.gcode
```
