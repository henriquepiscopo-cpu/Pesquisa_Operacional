# PROMPT PARA O CLAUDE CODE

> Cole este prompt diretamente no terminal do Claude Code (dentro da pasta do projeto).
> Suba também o arquivo `relatorio_metrologia_claudecomcapaprarevisar.docx` na raiz do repositório
> para que o Claude Code use como referência visual de estilo.

---

## PROMPT:

```
Leia o arquivo `relatorio_metrologia_claudecomcapaprarevisar.docx` que está na raiz
do repositório. Ele será o modelo de estilo para o relatório final deste projeto.

Em seguida, atualize o arquivo CLAUDE.md adicionando uma seção completa chamada
"## RELATÓRIO FINAL — INSTRUÇÕES DE ESTILO E FORMATAÇÃO" com todas as regras abaixo.

Depois, gere o arquivo `relatorio/relatorio_final.md` seguindo rigorosamente essas
instruções e preenchendo com os resultados reais do projeto DEA.

---

### DADOS DO TRABALHO

- Aluno: Henrique Arbex Rodrigues Piscopo
- RA: 284675
- Professora: Priscila Rampazzo
- Disciplina: Pesquisa Operacional — LE505
- Instituição: Universidade Estadual de Campinas — FCA (Faculdade de Ciências Aplicadas)
- Cidade: Limeira
- Ano: 2026

---

### REGRAS DE FORMATAÇÃO (baseadas no documento de referência)

**CAPA (primeira página):**
- Linha 1: "LE505 - Pesquisa Operacional" (alinhado à direita)
- Linha 2: "Prof.ª Priscila Rampazzo" (alinhado à direita)
- Linha 3 (centro, negrito): "Universidade Estadual de Campinas"
- Linha 4 (centro, negrito): "FCA – Faculdade de Ciências Aplicadas"
- Linha 5 (centro): Título completo do trabalho
- Linha 6: "Junho/2026"
- Bloco de autoria (negrito, alinhado): "Henrique Arbex Rodrigues Piscopo    RA: 284675"
- Rodapé: "Limeira" e "2026"

**ESTRUTURA DE SEÇÕES (nomes exatos, em maiúsculas):**
1. RESUMO
2. INTRODUÇÃO
3. APRESENTAÇÃO DO PROBLEMA
4. ANÁLISE ENVOLTÓRIA DE DADOS
5. RESULTADOS E DISCUSSÕES
6. CONCLUSÕES
7. REFERÊNCIAS BIBLIOGRÁFICAS

**SUBSECTIONS:**
- Títulos de subseções em negrito, primeira letra maiúscula, sem numeração
- Exemplo: **Modelo CCR.** Texto do parágrafo segue na mesma linha.

**FIGURAS:**
- Numeradas sequencialmente: Figura 1, Figura 2, etc.
- Legenda ABAIXO da figura, em negrito: **Figura N.** Descrição completa da figura.
- Toda figura deve ser referenciada no texto antes de aparecer: "(ver Figura 1)"
- Figuras geradas em Python devem ser inseridas a partir de `results/figures/`
- Lista de figuras obrigatórias:
  * Figura 1 — Histograma dos scores de eficiência CCR e BCC
  * Figura 2 — Ranking de eficiência por empresa (barras horizontais)
  * Figura 3 — Scatter plot CCR vs BCC com linha de referência y=x
  * Figura 4 — Heatmap de benchmarks (lambdas)
  * Figura 5 — Boxplots das variáveis (análise exploratória)
  * Figura 6 — Matriz de correlação (heatmap)
  * Figura 7 — Metas de melhoria para as 3 DMUs mais ineficientes

**TABELAS:**
- Numeradas sequencialmente: Tabela 1, Tabela 2, etc.
- Legenda ABAIXO da tabela, em negrito: **Tabela N.** Descrição completa.
- Toda tabela deve ser referenciada no texto: "(ver Tabela 1)"
- Tabelas obrigatórias:
  * Tabela 1 — DMUs analisadas (empresa, ticker, país)
  * Tabela 2 — Estatísticas descritivas dos inputs e outputs
  * Tabela 3 — Scores de eficiência CCR e BCC por DMU
  * Tabela 4 — DMUs eficientes por modelo
  * Tabela 5 — Benchmarks e lambdas das DMUs ineficientes
  * Tabela 6 — Metas de melhoria para DMUs ineficientes
  * Tabela 7 — Eficiência de escala e tipo de retorno (CRS/IRS/DRS)

**TEXTO:**
- Português formal e acadêmico
- Sem marcadores (bullets) no corpo do texto — apenas prosa corrida
- Listas quando necessárias devem ser integradas ao parágrafo
- Variáveis e símbolos matemáticos em itálico: *θ*, *λ*, *x*, *y*
- Siglas por extenso na primeira menção: Análise Envoltória de Dados (DEA)

**EQUAÇÕES:**
- Apresentar a formulação matemática dos modelos CCR e BCC
- Numeradas à direita: (1), (2), (3)...
- Explicar cada variável após apresentar a equação

**REFERÊNCIAS (ABNT):**
Formato obrigatório — seguir exatamente o padrão ABNT NBR 6023:
- Artigos: SOBRENOME, Nome. Título do artigo. Nome do Periódico, v. X, n. Y, p. ZZ–ZZ, Ano.
- Livros: SOBRENOME, Nome. Título. Edição. Local: Editora, Ano.
- Referências obrigatórias:
  * CHARNES, A.; COOPER, W. W.; RHODES, E. Measuring the efficiency of decision making units. European Journal of Operational Research, v. 2, n. 6, p. 429–444, 1978.
  * BANKER, R. D.; CHARNES, A.; COOPER, W. W. Some models for estimating technical and scale inefficiencies in data envelopment analysis. Management Science, v. 30, n. 9, p. 1078–1092, 1984.
  * COOPER, W. W.; SEIFORD, L. M.; TONE, K. Data Envelopment Analysis: A Comprehensive Text with Models, Applications, References and DEA-Solver Software. 2. ed. New York: Springer, 2007.
  * Citar a biblioteca yfinance com data de acesso
  * Citar a biblioteca PuLP com data de acesso

**LIMITE DE PÁGINAS:**
- Máximo de 15 páginas incluindo capa e referências
- Distribuição sugerida:
  * Capa: 1 página
  * Resumo + Introdução: 1 página
  * Apresentação do Problema: 1–2 páginas
  * Análise Envoltória de Dados (teoria): 2 páginas
  * Resultados e Discussões: 6–7 páginas (incluindo figuras e tabelas)
  * Conclusões: 1 página
  * Referências: 0,5 página

---

### CONTEÚDO DO RESUMO

O resumo deve conter em um único parágrafo (150–250 palavras):
- Objetivo do trabalho
- Metodologia (DEA, modelos CCR e BCC, orientação a output)
- Dados utilizados (fonte, número de DMUs, inputs e outputs)
- Principais resultados (quantas DMUs eficientes, qual o score médio, principais benchmarks)
- Conclusão principal

---

### CONTEÚDO DA SEÇÃO "ANÁLISE ENVOLTÓRIA DE DADOS"

Esta seção deve apresentar:

1. **Introdução ao DEA.** Explicar o método em linguagem acessível.

2. **Modelo CCR.** Apresentar a formulação do problema de programação linear
   com orientação a output. Explicar o significado de retornos constantes de escala.
   Equação numerada como (1) a (4).

3. **Modelo BCC.** Apresentar a formulação, destacando a restrição adicional
   sum(lambda) = 1 que garante retornos variáveis de escala.
   Equação numerada como (5) a (9).

4. **Eficiência de Escala.** Definir SE = theta_CCR / theta_BCC e explicar
   os três tipos de retorno: CRS, IRS, DRS.

5. **Orientação escolhida.** Justificar a orientação a output para este estudo.

---

### INSTRUÇÃO FINAL

Após criar o relatorio_final.md, verifique:
- [ ] Capa com todos os dados do aluno
- [ ] Todas as 7 seções presentes e em maiúsculas
- [ ] Todas as 7 figuras referenciadas no texto e com legenda abaixo
- [ ] Todas as 7 tabelas referenciadas no texto e com legenda abaixo
- [ ] Formulação matemática CCR e BCC com equações numeradas
- [ ] Referências em ABNT
- [ ] Máximo de 15 páginas
- [ ] Linguagem acadêmica em português
```
