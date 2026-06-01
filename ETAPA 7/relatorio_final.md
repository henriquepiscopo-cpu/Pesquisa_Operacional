<!-- CAPA -->

<div align="right">

LE505 - Pesquisa Operacional
Prof.ª Priscila Rampazzo

</div>

<div align="center">

**Universidade Estadual de Campinas**
**FCA – Faculdade de Ciências Aplicadas**

Análise de Eficiência Relativa de Empresas de Petróleo e Gás por meio da Análise Envoltória de Dados (DEA)

Junho/2026

**Henrique Arbex Rodrigues Piscopo    RA: 284675**

</div>

<div align="center">

Limeira
2026

</div>

---

## RESUMO

O presente trabalho aplica a Análise Envoltória de Dados (DEA) para mensurar a eficiência relativa de 22 empresas do setor de petróleo e gás listadas em bolsas internacionais. Foram empregados os modelos CCR (retornos constantes de escala) e BCC (retornos variáveis de escala), ambos com orientação a output, implementados em Python com uso da biblioteca PuLP para resolução dos problemas de programação linear. Os dados financeiros foram coletados via biblioteca yfinance, referentes ao exercício fiscal mais recente disponível, e compreendem três inputs — ativos totais, despesas operacionais e número de funcionários — e dois outputs — receita líquida e EBITDA. Os resultados indicam que 9 das 22 empresas (41%) são eficientes no modelo CCR e 10 (45%) no modelo BCC, com scores médios de 1,0811 e 1,0591, respectivamente. A Equinor (EQNR) e a Petrobras (PBR) emergem como benchmarks dominantes, sendo referenciadas por 12 e 10 DMUs ineficientes no modelo CCR, respectivamente. A Canadian Natural Resources (CNQ) é a empresa mais ineficiente da amostra (θ = 1,2597), seguida da Eni (θ = 1,1942) e da Chevron (θ = 1,1849). A ExxonMobil apresenta o caso mais relevante de ineficiência de escala: tecnicamente eficiente no BCC, mas ineficiente no CCR. Conclui-se que a maioria das grandes empresas integradas do setor opera próximo à fronteira eficiente, com ineficiências moderadas que podem ser atribuídas a diferenças de modelo de negócio, escala de operação e contexto regulatório.

---

## INTRODUÇÃO

O setor de petróleo e gás é marcado por elevada intensidade de capital, volatilidade de preços e crescentes pressões regulatórias e ambientais. Nesse ambiente, a avaliação comparativa do desempenho das empresas torna-se instrumento estratégico para gestores, investidores e formuladores de políticas públicas. Métodos tradicionais de análise financeira, como indicadores de rentabilidade e retorno sobre ativos, avaliam empresas de forma isolada e são fortemente influenciados por variáveis de preço exógenas ao controle das firmas, o que limita a capacidade de identificar ineficiências genuinamente operacionais.

A Análise Envoltória de Dados (DEA), método não paramétrico desenvolvido por Charnes, Cooper e Rhodes (1978) e expandido por Banker, Charnes e Cooper (1984), oferece uma abordagem comparativa que constrói uma fronteira de melhores práticas a partir das próprias observações da amostra. Por meio da resolução de problemas de programação linear, o DEA identifica quais unidades de decisão operam na fronteira eficiente, quais estão aquém dela e em quanto cada unidade ineficiente precisaria expandir seus outputs — ou contrair seus inputs — para tornar-se eficiente.

Este trabalho tem por objetivo aplicar os modelos DEA-CCR e DEA-BCC, com orientação a output, para avaliar a eficiência relativa de 22 grandes empresas do setor de petróleo e gás, identificar os benchmarks setoriais e propor metas de melhoria para as unidades ineficientes.

---

## APRESENTAÇÃO DO PROBLEMA

**Unidades de Decisão (DMUs).** A amostra é composta por 22 empresas do setor de petróleo e gás listadas em bolsas internacionais, abrangendo majors integradas, independentes de exploração, empresas de refino, serviços e midstream. As empresas selecionadas são megacorporações globais com operações em múltiplos países e dados reportados em dólares americanos, o que minimiza distorções de comparação internacional típicas de estudos com unidades puramente domésticas. A composição da amostra é apresentada na Tabela 1 (ver Tabela 1).

| Ticker | Empresa                   | País         | Segmento      |
|--------|---------------------------|--------------|---------------|
| XOM    | ExxonMobil                | EUA          | Integrada     |
| CVX    | Chevron                   | EUA          | Integrada     |
| SHEL   | Shell                     | Reino Unido  | Integrada     |
| BP     | BP                        | Reino Unido  | Integrada     |
| TTE    | TotalEnergies             | França       | Integrada     |
| COP    | ConocoPhillips            | EUA          | Exploração    |
| PBR    | Petrobras                 | Brasil       | Integrada     |
| EQNR   | Equinor                   | Noruega      | Integrada     |
| E      | Eni                       | Itália       | Integrada     |
| OXY    | Occidental Petroleum      | EUA          | Exploração    |
| DVN    | Devon Energy              | EUA          | Exploração    |
| VLO    | Valero Energy             | EUA          | Refino        |
| PSX    | Phillips 66               | EUA          | Refino        |
| MPC    | Marathon Petroleum        | EUA          | Refino        |
| SLB    | SLB (Schlumberger)        | EUA          | Serviços      |
| HAL    | Halliburton               | EUA          | Serviços      |
| IMO    | Imperial Oil              | Canadá       | Integrada     |
| CNQ    | Canadian Natural Resources| Canadá       | Exploração    |
| SU     | Suncor Energy             | Canadá       | Integrada     |
| BKR    | Baker Hughes              | EUA          | Serviços      |
| FTI    | TechnipFMC                | EUA/França   | Serviços      |
| WMB    | Williams Companies        | EUA          | Midstream     |

**Tabela 1.** Relação das DMUs analisadas, com ticker, empresa, país de origem e segmento de atuação.

**Variáveis.** A escolha de variáveis seguiu os critérios de disponibilidade, representatividade econômica e ausência de multicolinearidade severa. Foram definidos três inputs e dois outputs, conforme apresentado na Tabela 2 (ver Tabela 2).

| Tipo   | Variável            | Descrição                                        |
|--------|---------------------|--------------------------------------------------|
| Input  | Total Assets        | Ativos totais — proxy para capital empregado     |
| Input  | Operating Expenses  | Despesas operacionais — proxy para custos        |
| Input  | Employees           | Nº de funcionários — proxy para capital humano   |
| Output | Total Revenue       | Receita líquida total                            |
| Output | EBITDA              | Lucro antes de juros, impostos, depreciação e amortização |

**Tabela 2.** Variáveis utilizadas no modelo DEA, com tipo (input/output) e descrição.

A regra prática do DEA recomenda que o número de DMUs seja pelo menos três vezes a soma de inputs e outputs: 3 × (3 + 2) = 15. Com 22 DMUs, a regra é atendida com margem de 7 unidades, conferindo adequada capacidade discriminatória ao modelo.

Os dados foram coletados via API do Yahoo Finance (biblioteca `yfinance`, Python), referentes ao exercício fiscal mais recente disponível, com valores expressos em dólares americanos. Cinco empresas inicialmente selecionadas foram removidas da amostra por apresentarem dados incompletos (REP, MRO, HES, YPF, EC).

**Limitações.** Algumas limitações metodológicas devem ser reconhecidas na interpretação dos resultados. A fonte de dados automática (Yahoo Finance) pode apresentar inconsistências para empresas listadas em bolsas não americanas. Os anos fiscais não são uniformes entre todas as empresas, podendo introduzir viés temporal. A Petrobras (PBR) foi identificada como outlier em três das cinco variáveis na análise exploratória, podendo distorcer a fronteira eficiente. Adicionalmente, a amostra inclui empresas de segmentos distintos — exploração, refino, serviços e midstream — o que reduz parcialmente a homogeneidade das DMUs.

---

## ANÁLISE ENVOLTÓRIA DE DADOS

**Introdução ao DEA.** A Análise Envoltória de Dados é uma técnica de programação matemática não paramétrica que avalia a eficiência relativa de unidades de decisão que compartilham o mesmo conjunto de inputs e outputs. Ao contrário de métodos paramétricos como a análise de regressão, o DEA não pressupõe uma forma funcional específica para a relação entre inputs e outputs, construindo a fronteira eficiente empiricamente a partir das melhores práticas observadas na amostra. Uma DMU é considerada eficiente quando nenhuma combinação linear das demais DMUs da amostra é capaz de produzir mais outputs com os mesmos ou menos inputs.

**Modelo CCR.** O modelo CCR, proposto por Charnes, Cooper e Rhodes (1978), assume retornos constantes de escala (CRS — *Constant Returns to Scale*), ou seja, pressupõe que um aumento proporcional nos inputs resulta em aumento proporcional nos outputs para qualquer DMU. Com orientação a output, o modelo busca o fator máximo *θ* pelo qual os outputs de cada DMU podem ser expandidos, mantendo os inputs fixos. Formalmente, para cada DMU *o*, resolve-se o seguinte problema de programação linear:

$$\max \; \theta \tag{1}$$

$$\text{sujeito a:} \quad \sum_{j=1}^{n} \lambda_j \, x_{ij} \leq x_{io}, \quad \forall \, i \tag{2}$$

$$\sum_{j=1}^{n} \lambda_j \, y_{rj} \geq \theta \cdot y_{ro}, \quad \forall \, r \tag{3}$$

$$\lambda_j \geq 0, \quad \forall \, j \tag{4}$$

onde *x*$_{ij}$ é o valor do input *i* da DMU *j*; *y*$_{rj}$ é o valor do output *r* da DMU *j*; *x*$_{io}$ e *y*$_{ro}$ são os valores de input e output da DMU avaliada *o*; *λ*$_j$ são os pesos (intensidades) das DMUs de referência; e *θ* é o score de eficiência. Uma DMU é eficiente quando *θ* = 1 (não é possível expandir outputs); ineficiente quando *θ* > 1, indicando que os outputs poderiam ser multiplicados por *θ* mantendo os inputs constantes.

**Modelo BCC.** O modelo BCC, proposto por Banker, Charnes e Cooper (1984), generaliza o CCR ao admitir retornos variáveis de escala (VRS — *Variable Returns to Scale*), incluindo retornos crescentes, constantes e decrescentes. Isso é obtido pela adição de uma restrição de convexidade ao conjunto de possibilidades de produção. A formulação é idêntica ao CCR com a adição da equação (9):

$$\max \; \theta \tag{5}$$

$$\text{sujeito a:} \quad \sum_{j=1}^{n} \lambda_j \, x_{ij} \leq x_{io}, \quad \forall \, i \tag{6}$$

$$\sum_{j=1}^{n} \lambda_j \, y_{rj} \geq \theta \cdot y_{ro}, \quad \forall \, r \tag{7}$$

$$\lambda_j \geq 0, \quad \forall \, j \tag{8}$$

$$\sum_{j=1}^{n} \lambda_j = 1 \tag{9}$$

A restrição (9) garante que cada DMU seja comparada apenas com combinações convexas de outras DMUs de porte similar, eliminando o componente de ineficiência de escala da medida de eficiência técnica.

**Eficiência de Escala.** A eficiência de escala (*SE*) é obtida pela razão entre os scores dos dois modelos:

$$SE = \frac{\theta_{CCR}}{\theta_{BCC}} \tag{10}$$

Quando *SE* = 1, a DMU opera na escala ótima (retornos constantes de escala — CRS). Quando *SE* > 1, a DMU apresenta ineficiência de escala — opera em tamanho diferente do ótimo global. Nesse caso, a comparação entre o score BCC individual e o benchmark CCR permite inferir se a DMU opera com retornos crescentes (IRS) ou decrescentes (DRS) de escala.

**Orientação escolhida.** Adotou-se a orientação a output neste estudo com base na natureza das operações do setor de petróleo e gás. As empresas operam com estrutura de ativos, força de trabalho e custos operacionais relativamente fixos no curto e médio prazo — variáveis que dependem de decisões estratégicas de longo prazo, como fusões, aquisições e desinvestimentos. A pergunta economicamente mais relevante é, portanto, quanto mais receita e EBITDA cada empresa poderia gerar com os recursos que já possui, caso operasse sobre a fronteira eficiente.

---

## RESULTADOS E DISCUSSÕES

**Análise Exploratória dos Dados.** A análise exploratória revelou elevada dispersão nas variáveis, reflexo da heterogeneidade de porte entre as 22 DMUs. Os boxplots das variáveis normalizadas (ver Figura 5) evidenciam a presença de valores atípicos, especialmente nos outputs.

![Boxplots das variáveis](../ETAPA%202/figures/boxplots.png)

**Figura 5.** Boxplots das variáveis de input e output normalizadas pelo valor máximo da amostra.

A matriz de correlação (ver Figura 6) apresenta alta correlação positiva entre inputs e outputs, esperada em razão da relação entre porte e capacidade produtiva das empresas.

![Matriz de correlação](../ETAPA%202/figures/correlation_heatmap.png)

**Figura 6.** Matriz de correlação entre as variáveis de input e output. Valores próximos de 1 (vermelho) indicam alta correlação positiva.

A análise pelo método IQR identificou a Petrobras (PBR) como outlier em três variáveis: Total Assets, Receita Líquida e EBITDA. Seu porte desproporcionalmente elevado em relação à mediana da amostra pode distorcer a fronteira eficiente, favorecendo artificialmente seu posicionamento como benchmark. Essa limitação é reconhecida e discutida nas conclusões.

**Scores de Eficiência.** Os resultados dos modelos CCR e BCC são apresentados na Tabela 3 (ver Tabela 3). No modelo CCR, 9 das 22 DMUs (41%) atingiram a fronteira eficiente (*θ* = 1,0), enquanto no modelo BCC esse número sobe para 10 DMUs (45%). O score médio CCR é de 1,0811 e o BCC de 1,0591, indicando que, em média, as DMUs ineficientes precisariam expandir seus outputs em aproximadamente 8,1% e 5,9%, respectivamente, para atingir a fronteira.

| DMU   | Empresa                    | Score CCR | Score BCC | Ef. Escala | Eficiente CCR | Eficiente BCC |
|-------|----------------------------|-----------|-----------|------------|:---:|:---:|
| XOM   | ExxonMobil                 | 1,1023    | 1,0000    | 1,1023     | Não | Sim |
| CVX   | Chevron                    | 1,1849    | 1,1281    | 1,0504     | Não | Não |
| SHEL  | Shell                      | 1,1356    | 1,0188    | 1,1146     | Não | Não |
| BP    | BP                         | 1,1522    | 1,0686    | 1,0782     | Não | Não |
| TTE   | TotalEnergies              | 1,1495    | 1,0854    | 1,0591     | Não | Não |
| COP   | ConocoPhillips             | 1,0587    | 1,0585    | 1,0002     | Não | Não |
| PBR   | Petrobras                  | 1,0000    | 1,0000    | 1,0000     | Sim | Sim |
| EQNR  | Equinor                    | 1,0000    | 1,0000    | 1,0000     | Sim | Sim |
| E     | Eni                        | 1,1942    | 1,1937    | 1,0004     | Não | Não |
| OXY   | Occidental Petroleum       | 1,1281    | 1,1253    | 1,0025     | Não | Não |
| DVN   | Devon Energy               | 1,0000    | 1,0000    | 1,0000     | Sim | Sim |
| VLO   | Valero Energy              | 1,0000    | 1,0000    | 1,0000     | Sim | Sim |
| PSX   | Phillips 66                | 1,0000    | 1,0000    | 1,0000     | Sim | Sim |
| MPC   | Marathon Petroleum         | 1,0000    | 1,0000    | 1,0000     | Sim | Sim |
| SLB   | SLB                        | 1,0976    | 1,0889    | 1,0080     | Não | Não |
| HAL   | Halliburton                | 1,0504    | 1,0488    | 1,0015     | Não | Não |
| IMO   | Imperial Oil               | 1,0000    | 1,0000    | 1,0000     | Sim | Sim |
| CNQ   | Canadian Natural Resources | 1,2597    | 1,2438    | 1,0128     | Não | Não |
| SU    | Suncor Energy              | 1,1513    | 1,1336    | 1,0156     | Não | Não |
| BKR   | Baker Hughes               | 1,1199    | 1,1077    | 1,0110     | Não | Não |
| FTI   | TechnipFMC                 | 1,0000    | 1,0000    | 1,0000     | Sim | Sim |
| WMB   | Williams Companies         | 1,0000    | 1,0000    | 1,0000     | Sim | Sim |

**Tabela 3.** Scores de eficiência CCR, BCC e eficiência de escala para as 22 DMUs analisadas. Scores iguais a 1,0000 indicam DMU eficiente.

A distribuição dos scores é visualizada no histograma da Figura 1 (ver Figura 1), que evidencia a concentração de DMUs na fronteira eficiente (*θ* = 1,0) e a cauda direita de ineficiências moderadas, com CNQ se destacando como caso extremo.

![Histograma de scores](../ETAPA%204/figures/histogram_efficiency.png)

**Figura 1.** Distribuição dos scores de eficiência CCR e BCC. A linha vertical vermelha tracejada indica a fronteira eficiente (*θ* = 1,0).

O ranking de eficiência por empresa é apresentado na Figura 2 (ver Figura 2), com as DMUs ordenadas pelo score CCR de forma crescente.

![Ranking de eficiência](../ETAPA%204/figures/ranking_efficiency.png)

**Figura 2.** Ranking de eficiência das 22 DMUs pelos scores CCR e BCC. Barras à direita da linha vermelha (*θ* = 1,0) representam DMUs ineficientes.

**DMUs Eficientes.** As empresas que atingiram a fronteira eficiente em cada modelo são sintetizadas na Tabela 4 (ver Tabela 4).

| Modelo | DMUs Eficientes (*θ* = 1,0000) |
|--------|-------------------------------|
| CCR    | PBR, EQNR, DVN, VLO, PSX, MPC, IMO, FTI, WMB (9 empresas) |
| BCC    | XOM, PBR, EQNR, DVN, VLO, PSX, MPC, IMO, FTI, WMB (10 empresas) |

**Tabela 4.** DMUs eficientes nos modelos CCR e BCC. XOM aparece como eficiente exclusivamente no BCC, evidenciando ineficiência de escala no CCR.

**Benchmarks e Lambdas.** O scatter plot CCR vs BCC (ver Figura 3) evidencia a relação entre os dois modelos e identifica visualmente os casos de ineficiência de escala — DMUs cujo score BCC é significativamente menor que o CCR.

![Scatter CCR vs BCC](../ETAPA%204/figures/ccr_vs_bcc.png)

**Figura 3.** Dispersão entre scores CCR e BCC por DMU. Pontos sobre a diagonal (*y* = *x*) indicam que CCR ≈ BCC (ausência de ineficiência de escala). XOM destaca-se pelo maior afastamento vertical.

As intensidades dos pesos *λ* das DMUs eficientes que compõem os benchmarks das ineficientes são apresentadas no heatmap da Figura 4 (ver Figura 4) e detalhadas na Tabela 5 (ver Tabela 5).

![Heatmap de benchmarks](../ETAPA%204/figures/benchmark_heatmap.png)

**Figura 4.** Heatmap de intensidade dos pesos *λ* (modelo CCR). Linhas representam DMUs ineficientes; colunas representam DMUs eficientes utilizadas como benchmark. Cores mais intensas indicam maior peso na combinação de referência.

| DMU Ineficiente | Score CCR | Benchmarks (CCR)    |
|-----------------|-----------|---------------------|
| XOM             | 1,1023    | PBR, EQNR, IMO      |
| CVX             | 1,1849    | PBR, EQNR, IMO      |
| SHEL            | 1,1356    | EQNR, MPC, FTI      |
| BP              | 1,1522    | EQNR, FTI           |
| TTE             | 1,1495    | PBR, EQNR           |
| COP             | 1,0587    | PBR, EQNR, DVN      |
| E               | 1,1942    | PBR, EQNR           |
| OXY             | 1,1281    | PBR, WMB            |
| SLB             | 1,0976    | PBR, EQNR           |
| HAL             | 1,0504    | EQNR, FTI           |
| CNQ             | 1,2597    | PBR, EQNR, DVN      |
| SU              | 1,1513    | PBR, EQNR           |
| BKR             | 1,1199    | PBR, EQNR           |

**Tabela 5.** Benchmarks das DMUs ineficientes no modelo CCR. EQNR é referência para 12 das 13 DMUs ineficientes; PBR, para 10.

A Equinor (EQNR) é o benchmark dominante da amostra, servindo de referência para 12 das 13 DMUs ineficientes no modelo CCR. Seu perfil — alta receita e EBITDA por ativo empregado, com base de funcionários enxuta (aproximadamente 22.000 colaboradores) e modelo de governança eficiente — representa o padrão de excelência setorial identificado pelo DEA. A Petrobras (PBR) aparece como segundo benchmark mais frequente (10 DMUs), combinando grande volume de outputs com integração vertical do pré-sal, embora seu status de outlier imponha cautela na interpretação.

**Metas de Melhoria para DMUs Ineficientes.** A orientação a output implica que as DMUs ineficientes deveriam, mantendo seus inputs atuais, expandir receita e EBITDA no percentual correspondente a (*θ* − 1) × 100%. As metas calculadas são apresentadas na Tabela 6 (ver Tabela 6) e visualizadas na Figura 7 (ver Figura 7).

| DMU | Score CCR | Receita Atual (USD bi) | Meta Receita (USD bi) | Aumento | EBITDA Atual (USD bi) | Meta EBITDA (USD bi) | Aumento |
|-----|-----------|------------------------|----------------------|---------|----------------------|---------------------|---------|
| CNQ | 1,2597    | 38,6                   | 48,7                 | +26,0%  | 14,8                 | 18,6                | +26,0%  |
| E   | 1,1942    | 84,5                   | 101,0                | +19,4%  | 12,0                 | 14,3                | +19,4%  |
| CVX | 1,1849    | 186,0                  | 220,4                | +18,5%  | 37,9                 | 44,9                | +18,5%  |

**Tabela 6.** Metas de melhoria para as três DMUs mais ineficientes no modelo CCR. Valores em bilhões de dólares americanos (USD bi).

![Metas de melhoria](../ETAPA%204/figures/improvement_targets.png)

**Figura 7.** Comparação entre outputs atuais e metas de melhoria para as três DMUs mais ineficientes (CNQ, Eni e Chevron), com orientação a output.

A Canadian Natural Resources (CNQ), com *θ* = 1,2597, é a empresa mais ineficiente da amostra. Sua principal fonte de ineficiência é estrutural: a empresa opera majoritariamente com extração de *oil sands*, cuja curva de custo por barril é significativamente superior à do petróleo convencional explorado por seus benchmarks (EQNR e DVN). O DEA, por ser agnóstico em relação ao tipo de recurso explorado, penaliza a CNQ pela menor produtividade relativa de seus ativos, o que não necessariamente reflete má gestão, mas diferença de modelo de negócio.

A Eni (E), com *θ* = 1,1942, apresenta base de ativos e de funcionários elevada em relação ao nível de receita gerado. Comparada com a Equinor — sua principal referência —, a Eni apresenta menor eficiência por funcionário, possivelmente em razão de maior exposição a países com alto risco operacional e estrutura organizacional mais extensa.

A Chevron (CVX), com *θ* = 1,1849, representa um resultado contraintuitivo: trata-se de uma das maiores majors do mundo, mas o DEA aponta que a combinação linear de PBR, EQNR e IMO replica seu perfil de inputs com maior geração de outputs. Isso sugere que a CVX não extrai o máximo de receita e EBITDA de sua base de ativos, possivelmente em razão de estratégia conservadora de alocação de capital e maior diversificação geográfica.

**Eficiência de Escala.** A eficiência de escala de cada DMU é apresentada na Tabela 7 (ver Tabela 7). Todas as DMUs apresentaram classificação CRS, com eficiências de escala muito próximas de 1,0 para a maioria das empresas.

| DMU  | Score CCR | Score BCC | Ef. Escala | Retorno de Escala |
|------|-----------|-----------|------------|-------------------|
| XOM  | 1,1023    | 1,0000    | 1,1023     | CRS               |
| CVX  | 1,1849    | 1,1281    | 1,0504     | CRS               |
| SHEL | 1,1356    | 1,0188    | 1,1146     | CRS               |
| BP   | 1,1522    | 1,0686    | 1,0782     | CRS               |
| TTE  | 1,1495    | 1,0854    | 1,0591     | CRS               |
| COP  | 1,0587    | 1,0585    | 1,0002     | CRS               |
| PBR  | 1,0000    | 1,0000    | 1,0000     | CRS               |
| EQNR | 1,0000    | 1,0000    | 1,0000     | CRS               |
| E    | 1,1942    | 1,1937    | 1,0004     | CRS               |
| OXY  | 1,1281    | 1,1253    | 1,0025     | CRS               |
| DVN  | 1,0000    | 1,0000    | 1,0000     | CRS               |
| VLO  | 1,0000    | 1,0000    | 1,0000     | CRS               |
| PSX  | 1,0000    | 1,0000    | 1,0000     | CRS               |
| MPC  | 1,0000    | 1,0000    | 1,0000     | CRS               |
| SLB  | 1,0976    | 1,0889    | 1,0080     | CRS               |
| HAL  | 1,0504    | 1,0488    | 1,0015     | CRS               |
| IMO  | 1,0000    | 1,0000    | 1,0000     | CRS               |
| CNQ  | 1,2597    | 1,2438    | 1,0128     | CRS               |
| SU   | 1,1513    | 1,1336    | 1,0156     | CRS               |
| BKR  | 1,1199    | 1,1077    | 1,0110     | CRS               |
| FTI  | 1,0000    | 1,0000    | 1,0000     | CRS               |
| WMB  | 1,0000    | 1,0000    | 1,0000     | CRS               |

**Tabela 7.** Eficiência de escala e tipo de retorno de escala para todas as DMUs.

O caso mais relevante é o da ExxonMobil (XOM), com *SE* = 1,1023 — a maior eficiência de escala da amostra. Seu score CCR de 1,1023 cai para 1,0000 no BCC, evidenciando que toda a ineficiência observada no modelo CCR é de natureza escalar, não operacional. A XOM opera de forma tecnicamente eficiente dado seu porte, mas sua escala de operação difere do ponto ótimo global identificado pelo modelo de retornos constantes.

---

## CONCLUSÕES

O presente trabalho aplicou os modelos DEA-CCR e DEA-BCC, com orientação a output, para avaliar a eficiência relativa de 22 grandes empresas do setor de petróleo e gás. Os resultados permitiram identificar as melhores práticas setoriais, quantificar as ineficiências e propor metas concretas de melhoria de desempenho.

Os principais achados são os seguintes. Primeiro, 41% das DMUs (9/22) são eficientes no CCR e 45% (10/22) no BCC, com scores médios de 1,0811 e 1,0591 respectivamente, indicando ineficiências moderadas na maioria das empresas. Segundo, a Equinor (EQNR) e a Petrobras (PBR) são os benchmarks dominantes — referências para 12 e 10 DMUs ineficientes, respectivamente —, representando os padrões de melhor prática setorial identificados pelo modelo. Terceiro, a Canadian Natural Resources (CNQ) é a empresa mais ineficiente (*θ* = 1,2597), com ineficiência de natureza majoritariamente estrutural, associada ao modelo de negócio de *oil sands*. Quarto, a ExxonMobil (XOM) apresenta o caso mais didático de ineficiência de escala: operacionalmente eficiente no BCC, mas com *SE* = 1,1023 no CCR, indicando que sua escala de operação não coincide com o ponto ótimo global. Quinto, as grandes majors europeias — Shell, BP, TotalEnergies e Eni — apresentam-se como ineficientes em ambos os modelos, com scores entre 1,02 e 1,19.

Entre as limitações, destacam-se a heterogeneidade parcial da amostra — que inclui empresas de segmentos distintos —, a possível distorção introduzida pela Petrobras como outlier, e a incapacidade do DEA de capturar diferenças estruturais de modelo de negócio, como o custo superior de extração de *oil sands* frente ao petróleo convencional.

Para trabalhos futuros, recomenda-se a realização de análise de janela temporal (*window analysis*) para capturar a evolução da eficiência ao longo dos ciclos de preço do petróleo, a inclusão de variáveis ambientais e de governança (ESG) como outputs indesejáveis, e a aplicação de modelos DEA com outputs indesejáveis (emissões de CO₂) para refletir as externalidades do setor.

---

## REFERÊNCIAS BIBLIOGRÁFICAS

BANKER, R. D.; CHARNES, A.; COOPER, W. W. Some models for estimating technical and scale inefficiencies in data envelopment analysis. **Management Science**, v. 30, n. 9, p. 1078–1092, 1984.

CHARNES, A.; COOPER, W. W.; RHODES, E. Measuring the efficiency of decision making units. **European Journal of Operational Research**, v. 2, n. 6, p. 429–444, 1978.

COOPER, W. W.; SEIFORD, L. M.; TONE, K. **Data Envelopment Analysis: A Comprehensive Text with Models, Applications, References and DEA-Solver Software**. 2. ed. New York: Springer, 2007.

LINS, M. P. E.; MEZA, L. A. **Análise Envoltória de Dados e Perspectivas de Integração no Ambiente de Apoio à Decisão**. Rio de Janeiro: COPPE/UFRJ, 2000.

MITCHELL, J. **yfinance: Yahoo! Finance market data downloader**. Disponível em: https://pypi.org/project/yfinance/. Acesso em: jun. 2025.

MITCHELL, S. et al. **PuLP: A Linear Programming toolkit for Python**. Disponível em: https://pypi.org/project/PuLP/. Acesso em: jun. 2025.
