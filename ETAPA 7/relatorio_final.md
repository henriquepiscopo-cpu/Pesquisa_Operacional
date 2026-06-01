# Análise de Eficiência Relativa de Empresas de Petróleo e Gás por meio da Análise Envoltória de Dados (DEA)

**Disciplina:** LE505 — Análise Envoltória de Dados
**Entrega:** 03/06/2025

---

## 1. Introdução

O setor de petróleo e gás é caracterizado por elevada intensidade de capital, alta volatilidade de preços e crescentes pressões ambientais e regulatórias. Nesse contexto, a mensuração da eficiência relativa entre empresas torna-se um instrumento estratégico tanto para gestores quanto para investidores e formuladores de políticas públicas. Métodos tradicionais de análise financeira, como indicadores de rentabilidade e retorno sobre ativos, avaliam empresas de forma isolada e dependem fortemente de variáveis de preço — sujeitas a fatores exógenos fora do controle das firmas.

A Análise Envoltória de Dados (DEA, do inglês *Data Envelopment Analysis*) oferece uma alternativa não paramétrica para avaliar a eficiência produtiva de unidades de decisão (*Decision Making Units* — DMUs) de forma comparativa, construindo uma fronteira de eficiência a partir das próprias observações da amostra. Desenvolvida originalmente por Charnes, Cooper e Rhodes (1978) e expandida por Banker, Charnes e Cooper (1984), a metodologia permite identificar quais empresas operam na fronteira eficiente, quais estão aquém dela e em quanto precisariam melhorar seus outputs para atingir tal fronteira.

O presente trabalho aplica os modelos DEA — CCR (retornos constantes de escala) e BCC (retornos variáveis de escala) — com orientação a output, para avaliar a eficiência relativa de 22 grandes empresas do setor de petróleo e gás listadas em bolsas internacionais, utilizando dados financeiros do exercício fiscal mais recente disponível.

---

## 2. Apresentação do Problema

### 2.1 Unidades de Decisão (DMUs)

A amostra é composta por 22 empresas (*majors* integradas, independentes de exploração e empresas de serviços) listadas em bolsas internacionais. Os dados foram coletados via API do Yahoo Finance (biblioteca `yfinance`, Python), referentes ao exercício fiscal mais recente disponível.

| Ticker | Empresa               | País         | Tipo          |
|--------|-----------------------|--------------|---------------|
| XOM    | ExxonMobil            | EUA          | Integrada     |
| CVX    | Chevron               | EUA          | Integrada     |
| SHEL   | Shell                 | Reino Unido  | Integrada     |
| BP     | BP                    | Reino Unido  | Integrada     |
| TTE    | TotalEnergies         | França       | Integrada     |
| COP    | ConocoPhillips        | EUA          | Exploração    |
| PBR    | Petrobras             | Brasil       | Integrada     |
| EQNR   | Equinor               | Noruega      | Integrada     |
| E      | Eni                   | Itália       | Integrada     |
| OXY    | Occidental Petroleum  | EUA          | Exploração    |
| DVN    | Devon Energy          | EUA          | Exploração    |
| VLO    | Valero Energy         | EUA          | Refino        |
| PSX    | Phillips 66           | EUA          | Refino        |
| MPC    | Marathon Petroleum    | EUA          | Refino        |
| SLB    | SLB (Schlumberger)    | EUA          | Serviços      |
| HAL    | Halliburton           | EUA          | Serviços      |
| IMO    | Imperial Oil          | Canadá       | Integrada     |
| CNQ    | Canadian Natural Res. | Canadá       | Exploração    |
| SU     | Suncor Energy         | Canadá       | Integrada     |
| BKR    | Baker Hughes          | EUA          | Serviços      |
| FTI    | TechnipFMC            | EUA/França   | Serviços      |
| WMB    | Williams Companies    | EUA          | Midstream     |

As empresas selecionadas são megacorporações globais listadas em bolsas internacionais, com operações em múltiplos países e dados reportados em dólares americanos, o que minimiza as distorções de comparação internacional típicas de estudos com unidades puramente domésticas.

### 2.2 Variáveis

A escolha de variáveis seguiu o critério de disponibilidade, representatividade econômica e ausência de multicolinearidade severa:

| Tipo   | Variável              | Descrição                                      |
|--------|-----------------------|------------------------------------------------|
| Input  | Total Assets          | Ativos totais — proxy para capital empregado   |
| Input  | Operating Expenses    | Custos operacionais — proxy para eficiência de custos |
| Input  | Full Time Employees   | Nº de funcionários — proxy para capital humano |
| Output | Total Revenue         | Receita líquida total                          |
| Output | EBITDA                | Lucro antes de juros, impostos, depreciação e amortização |

A regra prática do DEA recomenda que o número de DMUs seja pelo menos três vezes a soma de inputs e outputs: 3 × (3 + 2) = **15**. Com 22 DMUs, a regra é atendida com margem de 7 unidades.

### 2.3 Limitações

As seguintes limitações devem ser reconhecidas na interpretação dos resultados:

1. **Fonte dos dados:** os dados foram coletados automaticamente via Yahoo Finance, que pode apresentar inconsistências para empresas listadas em bolsas não americanas.
2. **Ano fiscal não uniforme:** nem todas as empresas encerram o exercício fiscal em dezembro, o que pode introduzir viés temporal.
3. **Outlier PBR:** a Petrobras apresenta-se como outlier em Total Assets, Receita Líquida e EBITDA, podendo distorcer a fronteira eficiente.
4. **Heterogeneidade parcial:** a amostra inclui empresas de exploração, refino, serviços e *midstream*, que possuem modelos de negócio distintos das *majors* integradas.
5. **Variáveis proxy:** `operatingExpenses` e `fullTimeEmployees` não capturam qualidade de gestão, tecnologia ou contexto regulatório de cada país.

---

## 3. Análise Envoltória de Dados

### 3.1 Formulação do Modelo CCR

O modelo CCR (Charnes, Cooper e Rhodes, 1978) assume retornos constantes de escala (CRS) e, na orientação a output, busca maximizar o fator pelo qual os outputs de cada DMU podem ser expandidos, mantendo os inputs fixos:

$$\max \theta$$

sujeito a:

$$\sum_{j=1}^{n} \lambda_j x_{ij} \leq x_{io} \quad \forall i$$

$$\sum_{j=1}^{n} \lambda_j y_{rj} \geq \theta \cdot y_{ro} \quad \forall r$$

$$\lambda_j \geq 0 \quad \forall j$$

onde $x_{ij}$ é o valor do input $i$ da DMU $j$, $y_{rj}$ é o valor do output $r$ da DMU $j$, $\lambda_j$ são os pesos (intensidades) das DMUs de referência, e $\theta$ é o score de eficiência. Uma DMU é eficiente quando $\theta = 1$; ineficiente quando $\theta > 1$ (orientação output).

### 3.2 Formulação do Modelo BCC

O modelo BCC (Banker, Charnes e Cooper, 1984) adiciona a restrição de convexidade ao CCR, permitindo retornos variáveis de escala (VRS):

$$\sum_{j=1}^{n} \lambda_j = 1$$

Essa restrição faz com que cada DMU seja comparada apenas com outras de porte similar, eliminando o efeito de escala da medida de eficiência.

### 3.3 Eficiência de Escala

A eficiência de escala (SE) é calculada como:

$$SE = \frac{\theta_{CCR}}{\theta_{BCC}}$$

Quando SE = 1, a DMU opera na escala ótima. Quando SE > 1, há ineficiência de escala — a DMU seria mais eficiente se operasse em tamanho diferente.

### 3.4 Orientação e Implementação

Adotou-se **orientação a output**, pois as empresas do setor operam com estrutura de ativos e força de trabalho relativamente fixos no curto prazo, sendo mais natural questionar quanto mais poderiam produzir (receita e EBITDA) com os recursos que já possuem.

Os modelos foram implementados em Python utilizando a biblioteca `PuLP` para resolução dos problemas de programação linear, com solver CBC.

---

## 4. Resultados

### 4.1 Análise Exploratória

As estatísticas descritivas revelam elevada dispersão em todas as variáveis, reflexo da heterogeneidade de tamanho entre as DMUs. O desvio padrão de Total Assets supera a média ($\bar{x} = 184,9$ bi; $\sigma = 261,9$ bi), indicando distribuição assimétrica.

A análise de outliers pelo método IQR identificou a **Petrobras (PBR)** como outlier em três variáveis: Total Assets, Receita Líquida e EBITDA. Seu porte desproporcionalmente grande em relação à mediana da amostra deve ser considerado na interpretação dos benchmarks.

A matriz de correlação evidenciou alta correlação positiva entre inputs e outputs — esperada, pois empresas maiores tendem a gerar mais receita — sem multicolinearidade extrema que justificasse eliminação de variáveis.

### 4.2 Scores de Eficiência

Os resultados dos modelos CCR e BCC são apresentados na tabela a seguir:

| DMU   | Empresa               | CCR    | BCC    | Ef. Escala | Eficiente CCR | Eficiente BCC |
|-------|-----------------------|--------|--------|------------|:---:|:---:|
| XOM   | ExxonMobil            | 1.1023 | 1.0000 | 1.1023     | ✗   | ✓   |
| CVX   | Chevron               | 1.1849 | 1.1281 | 1.0504     | ✗   | ✗   |
| SHEL  | Shell                 | 1.1356 | 1.0188 | 1.1146     | ✗   | ✗   |
| BP    | BP                    | 1.1522 | 1.0686 | 1.0782     | ✗   | ✗   |
| TTE   | TotalEnergies         | 1.1495 | 1.0854 | 1.0591     | ✗   | ✗   |
| COP   | ConocoPhillips        | 1.0587 | 1.0585 | 1.0002     | ✗   | ✗   |
| **PBR**   | **Petrobras**     | **1.0000** | **1.0000** | **1.0000** | **✓** | **✓** |
| **EQNR**  | **Equinor**       | **1.0000** | **1.0000** | **1.0000** | **✓** | **✓** |
| E     | Eni                   | 1.1942 | 1.1937 | 1.0004     | ✗   | ✗   |
| OXY   | Occidental            | 1.1281 | 1.1253 | 1.0025     | ✗   | ✗   |
| **DVN**   | **Devon Energy**  | **1.0000** | **1.0000** | **1.0000** | **✓** | **✓** |
| **VLO**   | **Valero**        | **1.0000** | **1.0000** | **1.0000** | **✓** | **✓** |
| **PSX**   | **Phillips 66**   | **1.0000** | **1.0000** | **1.0000** | **✓** | **✓** |
| **MPC**   | **Marathon Petro.**| **1.0000** | **1.0000** | **1.0000** | **✓** | **✓** |
| SLB   | SLB                   | 1.0976 | 1.0889 | 1.0080     | ✗   | ✗   |
| HAL   | Halliburton           | 1.0504 | 1.0488 | 1.0015     | ✗   | ✗   |
| **IMO**   | **Imperial Oil**  | **1.0000** | **1.0000** | **1.0000** | **✓** | **✓** |
| CNQ   | Canadian Natural      | 1.2597 | 1.2438 | 1.0128     | ✗   | ✗   |
| SU    | Suncor Energy         | 1.1513 | 1.1336 | 1.0156     | ✗   | ✗   |
| BKR   | Baker Hughes          | 1.1199 | 1.1077 | 1.0110     | ✗   | ✗   |
| **FTI**   | **TechnipFMC**    | **1.0000** | **1.0000** | **1.0000** | **✓** | **✓** |
| **WMB**   | **Williams Cos.** | **1.0000** | **1.0000** | **1.0000** | **✓** | **✓** |

**Score médio CCR:** 1.0811 | **Score médio BCC:** 1.0591

Em média, as DMUs ineficientes precisariam expandir seus outputs em **8,1% (CCR)** ou **5,9% (BCC)** para atingir a fronteira eficiente, mantendo os inputs constantes.

### 4.3 Benchmarks Dominantes

| Benchmark | CCR (nº DMUs referenciadas) | BCC (nº DMUs referenciadas) |
|-----------|-----------------------------|------------------------------|
| EQNR      | 12                          | 8                            |
| PBR       | 10                          | 7                            |
| FTI       | 3                           | 5                            |
| DVN       | 2                           | 4                            |
| MPC       | 1                           | 4                            |

**Equinor (EQNR)** é o benchmark dominante, servindo de referência para 12 das 13 DMUs ineficientes no CCR. Seu perfil — alta receita e EBITDA por ativo empregado, com base de funcionários relativamente enxuta (~22.000) — representa o padrão de eficiência da fronteira para empresas de exploração e produção integrada.

### 4.4 DMUs Mais Ineficientes e Metas de Melhoria

#### Canadian Natural Resources (CNQ) — Score CCR: 1.2597
A CNQ é a DMU mais ineficiente da amostra. Seus benchmarks — PBR, EQNR e DVN — operam com exploração convencional de menor custo por barril, enquanto a CNQ atua predominantemente em *oil sands*, cuja extração é altamente capital-intensiva. Mantendo seus inputs atuais, o modelo aponta que a CNQ deveria gerar:
- Receita: USD 38,6 bi → **USD 48,7 bi** (+25,97%)
- EBITDA: USD 14,8 bi → **USD 18,6 bi** (+25,97%)

#### Eni S.p.A. (E) — Score CCR: 1.1942
A Eni apresenta base de funcionários e ativos elevados para o nível de receita gerado. Em comparação com EQNR (benchmark principal), a Eni apresenta menor produtividade por funcionário. O modelo aponta:
- Receita: USD 84,5 bi → **USD 101,0 bi** (+19,42%)
- EBITDA: USD 12,0 bi → **USD 14,3 bi** (+19,42%)

#### Chevron (CVX) — Score CCR: 1.1849
A ineficiência da CVX frente aos benchmarks PBR, EQNR e IMO sugere que a empresa não extrai o máximo de receita e EBITDA de sua base de ativos e funcionários. O modelo aponta:
- Receita: USD 186,0 bi → **USD 220,4 bi** (+18,49%)
- EBITDA: USD 37,9 bi → **USD 44,9 bi** (+18,49%)

### 4.5 Eficiência de Escala — Caso ExxonMobil (XOM)

O caso da ExxonMobil é o mais revelador no que diz respeito à eficiência de escala. Com score CCR de 1.1023 (ineficiente) e score BCC de 1.0000 (eficiente), sua eficiência de escala é de 1.1023 — a maior da amostra.

Isso demonstra que a **ineficiência da XOM é integralmente de escala**, não operacional. A empresa opera de forma tecnicamente eficiente dado seu tamanho, mas sua escala de operação difere do ponto ótimo de escala identificado pelo modelo CCR. No BCC, que respeita a escala individual de cada DMU, a XOM é reconhecida como plenamente eficiente.

### 4.6 Posição da Petrobras (PBR)

A Petrobras é eficiente em ambos os modelos (θ = 1.0) e figura como o segundo benchmark mais referenciado da amostra. Seu desempenho reflete a combinação de alta integração vertical (exploração, refino e distribuição do pré-sal), elevado EBITDA relativo e base de funcionários moderada (~40.000) para a escala de operações.

Contudo, conforme documentado na análise exploratória (ETAPA 2), a PBR é outlier em três variáveis. Sua eficiência deve ser interpretada com cautela: por ser desproporcionalmente grande em receita e EBITDA, a PBR puxa a fronteira para um patamar elevado, contribuindo para que outras empresas pareçam ineficientes em comparação.

---

## 5. Conclusões

Este trabalho aplicou os modelos DEA-CCR e DEA-BCC, com orientação a output, para avaliar a eficiência relativa de 22 empresas do setor de petróleo e gás. Os principais achados são:

1. **41% das DMUs (9/22) são eficientes no CCR** e **45% (10/22) no BCC**, indicando que a fronteira é relativamente acessível dentro desta amostra.

2. **Equinor (EQNR) e Petrobras (PBR)** são os benchmarks dominantes, servindo de referência para a grande maioria das empresas ineficientes. Ambas combinam alta produtividade por ativo com estrutura operacional eficiente.

3. **Canadian Natural Resources (CNQ)** é a empresa mais ineficiente, com ineficiência estrutural ligada ao modelo de negócio de *oil sands* — custo de extração superior ao do petróleo convencional — o que o DEA não captura contextualmente, sendo uma limitação metodológica relevante.

4. **ExxonMobil (XOM)** representa o caso mais didático de separação entre ineficiência técnica e de escala: tecnicamente eficiente (BCC = 1.0), mas operando em escala divergente do ótimo global (CCR = 1.10).

5. As **majors europeias** (Shell, BP, TotalEnergies, Eni) apresentam-se como ineficientes em ambos os modelos, com scores entre 1.01 e 1.19, possivelmente reflexo de maior burocracia, exposição a mercados de maior risco e estratégias de transição energética que afetam a rentabilidade de curto prazo.

**Limitações e trabalhos futuros:** a análise poderia ser aprimorada com (i) inclusão de variáveis ambientais e de governança (ESG) como outputs indesejáveis; (ii) análise de janela temporal (*window analysis*) para capturar evolução da eficiência ao longo dos anos; (iii) aplicação de modelos DEA com outputs indesejáveis (emissões de CO₂) para refletir as externalidades do setor.

---

## 6. Referências

- CHARNES, A.; COOPER, W. W.; RHODES, E. Measuring the efficiency of decision making units. *European Journal of Operational Research*, v. 2, n. 6, p. 429–444, 1978.

- BANKER, R. D.; CHARNES, A.; COOPER, W. W. Some models for estimating technical and scale inefficiencies in data envelopment analysis. *Management Science*, v. 30, n. 9, p. 1078–1092, 1984.

- COOPER, W. W.; SEIFORD, L. M.; TONE, K. *Data Envelopment Analysis: A Comprehensive Text with Models, Applications, References and DEA-Solver Software*. 2. ed. New York: Springer, 2007.

- LINS, M. P. E.; MEZA, L. A. *Análise Envoltória de Dados e Perspectivas de Integração no Ambiente de Apoio à Decisão*. Rio de Janeiro: COPPE/UFRJ, 2000.

- Yahoo Finance. Dados financeiros coletados via biblioteca `yfinance` (Python). Disponível em: https://finance.yahoo.com. Acesso em: jun. 2025.

---

*Relatório gerado com suporte do Claude Code (Anthropic). Dados coletados via yfinance. Modelos implementados em Python com PuLP.*
