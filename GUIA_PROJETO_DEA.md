# 📊 Projeto DEA — Eficiência de Empresas de Petróleo & Gás

> **Disciplina:** LE505 — Análise Envoltória de Dados  
> **Entrega:** 03/06 via Classroom (relatório + código Python)  
> **Tema:** Eficiência relativa de empresas de petróleo e gás (majors internacionais)

---

## 🗂️ Estrutura do Projeto

```
projeto_dea/
├── data/
│   ├── raw_data.csv           # dados brutos coletados
│   └── processed_data.csv     # dados limpos e normalizados
├── src/
│   ├── collect_data.py        # coleta via yfinance
│   ├── dea_models.py          # modelos CCR e BCC (PuLP)
│   └── visualization.py       # gráficos e tabelas
├── results/
│   ├── ccr_results.csv
│   ├── bcc_results.csv
│   └── figures/
├── main.py                    # pipeline completo
├── requirements.txt
├── CLAUDE.md                  # contexto para o Claude Code
└── relatorio/
    └── relatorio_final.md     # rascunho do relatório
```

---

## ✅ Etapas do Projeto

### ETAPA 0 — Setup inicial

**Prompt para o Claude Code:**
```
Crie a estrutura completa de pastas do projeto conforme o layout abaixo:
- data/, src/, results/figures/, relatorio/
Crie também o arquivo requirements.txt com as dependências:
pandas, numpy, matplotlib, seaborn, yfinance, pulp, scipy, openpyxl, jupyter
E crie um arquivo CLAUDE.md explicando que este é um projeto de DEA em Python
para avaliar eficiência de empresas de petróleo e gás usando modelos CCR e BCC.
```

---

### ETAPA 1 — Coleta de Dados (`src/collect_data.py`)

**DMUs utilizadas (~20 empresas):**

| Ticker | Empresa         | País         |
|--------|----------------|--------------|
| XOM    | ExxonMobil     | EUA          |
| CVX    | Chevron        | EUA          |
| SHEL   | Shell          | Reino Unido  |
| BP     | BP             | Reino Unido  |
| TTE    | TotalEnergies  | França       |
| COP    | ConocoPhillips | EUA          |
| PBR    | Petrobras      | Brasil       |
| EQNR   | Equinor        | Noruega      |
| E      | Eni            | Itália       |
| REP    | Repsol         | Espanha      |
| OXY    | Occidental     | EUA          |
| PXD    | Pioneer NR     | EUA          |
| DVN    | Devon Energy   | EUA          |
| HES    | Hess           | EUA          |
| MRO    | Marathon Oil   | EUA          |
| VLO    | Valero         | EUA          |
| PSX    | Phillips 66    | EUA          |
| MPC    | Marathon Petro | EUA          |
| SLB    | Schlumberger   | EUA          |
| HAL    | Halliburton    | EUA          |

**Variáveis a coletar (ano fiscal mais recente disponível):**

| Tipo    | Variável              | Campo yfinance            |
|---------|-----------------------|---------------------------|
| Input   | Ativos Totais         | `totalAssets`             |
| Input   | Custo Operacional     | `operatingExpenses`       |
| Input   | Nº de Funcionários    | `fullTimeEmployees`       |
| Output  | Receita Líquida       | `totalRevenue`            |
| Output  | EBITDA                | `ebitda`                  |

**Prompt para o Claude Code:**
```
Crie o arquivo src/collect_data.py que:
1. Use yfinance para coletar dados financeiros anuais das seguintes empresas
   (tickers: XOM, CVX, SHEL, BP, TTE, COP, PBR, EQNR, E, REP, OXY, DVN, HES,
   MRO, VLO, PSX, MPC, SLB, HAL)
2. Para cada empresa, colete do balanço e demonstrativo de resultados:
   - totalAssets (input)
   - operatingExpenses (input)
   - fullTimeEmployees (input)
   - totalRevenue (output)
   - ebitda (output)
3. Use o ano fiscal mais recente disponível
4. Salve os dados brutos em data/raw_data.csv
5. Trate valores ausentes (remover DMUs com dados incompletos)
6. Salve os dados limpos em data/processed_data.csv
7. Imprima um resumo com quantas DMUs ficaram válidas
```

---

### ETAPA 2 — Análise Exploratória (`notebooks/analysis.ipynb` ou `src/eda.py`)

**O que deve ser feito:**
- Estatísticas descritivas (média, mediana, desvio padrão, min, max)
- Matriz de correlação entre variáveis
- Boxplots para identificar outliers
- Discussão sobre homogeneidade das DMUs
- Verificar a regra DEA: nº DMUs ≥ 3 × (nº inputs + nº outputs)

**Prompt para o Claude Code:**
```
Crie o arquivo src/eda.py que realiza análise exploratória dos dados em
data/processed_data.csv. O script deve:
1. Calcular e exibir estatísticas descritivas completas (describe())
2. Plotar boxplots de cada variável (inputs e outputs separados)
3. Plotar uma matriz de correlação com heatmap
4. Identificar e listar outliers (usando IQR ou z-score)
5. Verificar a regra prática do DEA: número de DMUs >= 3*(num_inputs + num_outputs)
6. Salvar todos os gráficos em results/figures/ com nomes descritivos
7. Imprimir um relatório resumido com as principais observações
```

---

### ETAPA 3 — Modelos DEA (`src/dea_models.py`)

**Formulação teórica:**

**Modelo CCR (Charnes, Cooper, Rhodes, 1978) — Retornos Constantes de Escala:**

Orientação a output (maximizar produção mantendo inputs fixos):

```
max  θ
s.t. Σ λⱼ xᵢⱼ ≤ xᵢₒ    para cada input i
     Σ λⱼ yrⱼ ≥ θ yrₒ   para cada output r
     λⱼ ≥ 0
```

**Modelo BCC (Banker, Charnes, Cooper, 1984) — Retornos Variáveis de Escala:**

Mesma formulação do CCR com a restrição adicional:
```
Σ λⱼ = 1   (convexidade — garante retornos variáveis)
```

**Eficiência de Escala:** `SE = θ_CCR / θ_BCC`

**Prompt para o Claude Code:**
```
Crie o arquivo src/dea_models.py com as seguintes funções:

1. run_ccr(inputs_df, outputs_df, orientation='output') -> DataFrame
   - Implementa o modelo CCR com PuLP
   - orientation pode ser 'input' ou 'output'
   - Retorna DataFrame com colunas: DMU, efficiency_score, benchmarks, lambdas

2. run_bcc(inputs_df, outputs_df, orientation='output') -> DataFrame
   - Implementa o modelo BCC com PuLP (adiciona restrição sum(lambda)=1)
   - Retorna DataFrame com colunas: DMU, efficiency_score, benchmarks, lambdas

3. compute_scale_efficiency(ccr_results, bcc_results) -> DataFrame
   - Calcula eficiência de escala: SE = CCR / BCC
   - Classifica tipo de retorno de escala (CRS, IRS, DRS)

4. get_improvement_targets(dmu_name, model_results, inputs_df, outputs_df) -> dict
   - Para DMU ineficiente, calcula as metas de melhoria
   - Retorna inputs que devem diminuir e outputs que devem aumentar

Use PuLP para resolver todos os problemas de programação linear.
Para cada DMU ineficiente, identifique os benchmarks (DMUs com lambda > 0.001).
Salve resultados em results/ccr_results.csv e results/bcc_results.csv
```

---

### ETAPA 4 — Visualizações (`src/visualization.py`)

**Gráficos necessários para o relatório:**

1. Histograma de scores de eficiência (CCR e BCC)
2. Gráfico de barras: ranking de eficiência por DMU
3. Scatter plot: eficiência CCR vs BCC
4. Heatmap de benchmarks (quais DMUs são referência para quais)
5. Gráfico de metas de melhoria para as 3 DMUs mais ineficientes

**Prompt para o Claude Code:**
```
Crie o arquivo src/visualization.py com as seguintes funções:

1. plot_efficiency_histogram(ccr_df, bcc_df)
   - Histograma sobreposto dos scores CCR e BCC
   - Linha vertical em θ=1 (fronteira eficiente)

2. plot_efficiency_ranking(ccr_df, bcc_df)
   - Gráfico de barras horizontais com as empresas ordenadas por eficiência CCR
   - Mostrar CCR e BCC lado a lado

3. plot_ccr_vs_bcc(ccr_df, bcc_df)
   - Scatter plot: eixo x = CCR score, eixo y = BCC score
   - Linha diagonal y=x para referência
   - Anotar nome de cada DMU

4. plot_benchmark_heatmap(ccr_df)
   - Heatmap mostrando intensidade dos lambdas
   - Linhas = DMUs ineficientes, Colunas = DMUs eficientes (benchmarks)

5. plot_improvement_targets(dmu_name, targets_dict)
   - Gráfico de radar ou barras mostrando situação atual vs meta

Usar matplotlib e seaborn. Salvar tudo em results/figures/.
Usar paleta de cores profissional (ex: seaborn colorblind).
```

---

### ETAPA 5 — Pipeline Principal (`main.py`)

**Prompt para o Claude Code:**
```
Crie o arquivo main.py que executa o pipeline completo do projeto DEA:

1. Importar dados de data/processed_data.csv
2. Separar inputs (totalAssets, operatingExpenses, fullTimeEmployees)
   e outputs (totalRevenue, ebitda)
3. Rodar modelo CCR com orientação a output
4. Rodar modelo BCC com orientação a output
5. Calcular eficiência de escala
6. Gerar todas as visualizações
7. Para cada DMU ineficiente, calcular metas de melhoria
8. Imprimir relatório completo no terminal:
   - DMUs eficientes em CCR
   - DMUs eficientes em BCC
   - Top 3 mais ineficientes com seus benchmarks e metas
   - Estatísticas gerais dos scores

O script deve rodar do início ao fim com: python main.py
```

---

### ETAPA 6 — Análise dos Resultados (manual + com ajuda do Claude Code)

**O que analisar e reportar:**

- [ ] Quantas DMUs são eficientes no CCR? E no BCC?
- [ ] Qual a eficiência média nos dois modelos?
- [ ] Quais empresas são benchmarks recorrentes?
- [ ] Para as 3 DMUs mais ineficientes:
  - Quais são seus benchmarks?
  - Quanto precisariam aumentar outputs para ser eficientes?
- [ ] O que a eficiência de escala revela sobre cada empresa?
- [ ] Petrobras: como se sai em relação às majors?

**Prompt para análise qualitativa:**
```
Com base nos resultados em results/ccr_results.csv e results/bcc_results.csv,
me ajude a interpretar:
1. Por que [EMPRESA X] é ineficiente? Quais são seus benchmarks e o que eles
   têm em comum?
2. Qual é o significado econômico da diferença entre CCR e BCC para 
   [EMPRESA Y]?
3. Escreva um parágrafo de análise para a seção "Resultados" do relatório
   sobre as DMUs ineficientes, incluindo as metas de melhoria.
```

---

### ETAPA 7 — Relatório Final

**Estrutura (máx. 15 páginas):**

| Seção | Conteúdo | Páginas sugeridas |
|-------|----------|-------------------|
| Introdução | Contextualização do setor, motivação do DEA, objetivos | 1 |
| Apresentação do Problema | DMUs, inputs, outputs, fonte dos dados | 1–2 |
| Análise Envoltória de Dados | Formulação CCR e BCC, orientação escolhida | 2–3 |
| Resultados | EDA, scores, benchmarks, metas de melhoria | 5–6 |
| Conclusões | Achados, limitações, trabalhos futuros | 1 |
| Referências | Charnes et al. (1978), Banker et al. (1984), yfinance, etc. | 0.5 |

**Prompt para redigir o relatório:**
```
Com base nos resultados do projeto DEA sobre eficiência de empresas de
petróleo e gás, ajude-me a redigir a seção [NOME DA SEÇÃO] do relatório.
Os principais achados foram: [COLE AQUI OS RESULTADOS DO main.py].
O texto deve ser acadêmico, em português, com no máximo [N] parágrafos.
```

---

## 🔧 Como Executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Coletar os dados
python src/collect_data.py

# 3. Análise exploratória
python src/eda.py

# 4. Rodar pipeline completo (modelos + visualizações + resultados)
python main.py
```

---

## 📚 Referências Principais

- Charnes, A., Cooper, W. W., & Rhodes, E. (1978). *Measuring the efficiency of decision making units.* European Journal of Operational Research, 2(6), 429–444.
- Banker, R. D., Charnes, A., & Cooper, W. W. (1984). *Some models for estimating technical and scale inefficiencies in data envelopment analysis.* Management Science, 30(9), 1078–1092.
- Cooper, W. W., Seiford, L. M., & Tone, K. (2007). *Data Envelopment Analysis: A Comprehensive Text with Models, Applications, References and DEA-Solver Software.* Springer.
- Dados: Yahoo Finance via biblioteca `yfinance` (Python)

---

## 📋 Checklist de Entrega

- [ ] `requirements.txt` criado e testado
- [ ] `src/collect_data.py` — dados salvos em `data/processed_data.csv`
- [ ] `src/eda.py` — gráficos EDA em `results/figures/`
- [ ] `src/dea_models.py` — CCR e BCC implementados com PuLP
- [ ] `src/visualization.py` — todos os gráficos gerados
- [ ] `main.py` — pipeline completo rodando com `python main.py`
- [ ] Relatório final (máx. 15 páginas) em PDF
- [ ] Anexo respondido (perguntas sobre uso de IA)
- [ ] Upload no Classroom até 03/06

---

> 💡 **Dica para usar com Claude Code:** Abra o terminal na raiz do projeto e rode `claude`. 
> Cole os prompts de cada etapa acima diretamente no Claude Code. 
> Valide os resultados antes de avançar para a próxima etapa.
