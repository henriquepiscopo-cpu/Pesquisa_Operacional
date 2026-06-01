# ETAPA 6 — Análise dos Resultados DEA

> Base: resultados gerados pela ETAPA 3 e ETAPA 5 com 22 DMUs, modelos CCR e BCC orientação output.

---

## 1. Quantas DMUs são eficientes?

| Modelo | Eficientes | Ineficientes | Total |
|--------|-----------|--------------|-------|
| CCR    | 9 (41%)   | 13 (59%)     | 22    |
| BCC    | 10 (45%)  | 12 (55%)     | 22    |

**Eficientes no CCR:** PBR, EQNR, DVN, VLO, PSX, MPC, IMO, FTI, WMB

**Eficientes no BCC (inclui XOM além das 9 do CCR):** XOM, PBR, EQNR, DVN, VLO, PSX, MPC, IMO, FTI, WMB

O número relativamente alto de DMUs eficientes (41–45%) é esperado dada a margem estreita da amostra (22 DMUs, mínimo recomendado 15). Em amostras maiores, a fronteira tende a ser mais discriminante.

---

## 2. Eficiência média

| Modelo | Score médio | Interpretação |
|--------|-------------|---------------|
| CCR    | 1.0811      | Em média, as DMUs precisariam aumentar outputs em ~8,1% para atingir a fronteira |
| BCC    | 1.0591      | Com retornos variáveis, a ineficiência média cai para ~5,9% |

A diferença entre os dois modelos (2,2 p.p.) indica que parte da ineficiência observada no CCR é atribuível a **ineficiência de escala**, não apenas operacional.

---

## 3. Benchmarks mais recorrentes

| Benchmark | Referência para (CCR) | Referência para (BCC) | Perfil |
|-----------|----------------------|----------------------|--------|
| **EQNR**  | 12 DMUs              | 8 DMUs               | Alta receita por ativo; menor base de funcionários; eficiência operacional norueguesa |
| **PBR**   | 10 DMUs              | 7 DMUs               | Grande volume de ativos com altíssimo EBITDA relativo; integração vertical |
| **FTI**   | 3 DMUs               | 5 DMUs               | Empresa de serviços/tecnologia com poucos funcionários e boa receita por input |
| **DVN**   | 2 DMUs               | 4 DMUs               | Exploração independente enxuta, alta eficiência por ativo |
| **MPC**   | 1 DMU                | 4 DMUs               | Refino de alta rotatividade, receita elevada com ativos moderados |

**Interpretação:** EQNR e PBR dominam como benchmarks porque combinam alta receita e EBITDA com base de ativos e funcionários relativamente menor que as demais empresas de porte similar. São os padrões de eficiência da fronteira.

---

## 4. Análise das 3 DMUs mais ineficientes (CCR)

### 4.1 CNQ — Canadian Natural Resources (score CCR: 1.2597)
- **Benchmarks:** PBR, EQNR, DVN
- **Meta:** aumentar receita e EBITDA em **+26%** mantendo os mesmos inputs
- **Interpretação:** A CNQ possui grande base de ativos (exploração de oil sands canadense — capital intensivo) mas gera receita e EBITDA proporcionalmente baixos. O modelo aponta EQNR e DVN como referências — ambas operam exploração convencional com menor custo por barril. A ineficiência da CNQ é em grande parte estrutural: oil sands têm custo de extração muito superior ao petróleo convencional, o que o DEA não captura contextualmente.

### 4.2 Eni — ENI S.p.A. (score CCR: 1.1942)
- **Benchmarks:** PBR, EQNR
- **Meta:** aumentar receita e EBITDA em **+19%**
- **Interpretação:** A Eni tem ativos elevados e muitos funcionários para o nível de receita que gera. Comparada com EQNR (mesma categoria de major europeia integrada), a Eni apresenta menor eficiência por funcionário. Parte da ineficiência pode ser explicada por maior exposição a países de alto risco operacional (África, Médio Oriente) e maior estrutura burocrática.

### 4.3 CVX — Chevron (score CCR: 1.1849)
- **Benchmarks:** PBR, EQNR, IMO
- **Meta:** aumentar receita e EBITDA em **+18,5%**
- **Interpretação:** Surpreendente que CVX, uma das maiores majors do mundo, apareça como ineficiente. O DEA compara CVX com uma combinação linear de PBR, EQNR e IMO — que juntos replicam o perfil de inputs da CVX com mais outputs. Isso sugere que a CVX usa seus ativos e funcionários de forma menos intensa que seus benchmarks. Parte pode ser explicada por estratégia conservadora de capital e maior diversificação geográfica.

---

## 5. O que a eficiência de escala revela?

Todas as 22 DMUs apresentaram `returns_to_scale = CRS` (retornos constantes de escala), com eficiências de escala muito próximas de 1.0 para a maioria.

O caso mais relevante é **XOM**:
- CCR: 1.1023 (ineficiente) → BCC: 1.0000 (eficiente)
- Eficiência de escala: 1.1023

Isso significa que **toda a ineficiência da ExxonMobil é de escala**, não operacional. A XOM opera de forma tecnicamente eficiente dado seu tamanho, mas opera em escala diferente do ótimo de escala global da amostra. No BCC — que respeita a escala de cada DMU — ela é perfeita. No CCR — que assume escala ótima única — ela parece ineficiente porque está sendo comparada com DMUs de outros tamanhos.

---

## 6. Petrobras (PBR) — Posição na amostra

| Modelo | Score | Status | Benchmarks que usa |
|--------|-------|--------|--------------------|
| CCR    | 1.000 | ✅ Eficiente | — (ela própria é benchmark) |
| BCC    | 1.000 | ✅ Eficiente | — (ela própria é benchmark) |

A Petrobras é **eficiente em ambos os modelos** e é o **segundo benchmark mais referenciado da amostra** (10 DMUs no CCR, 7 no BCC).

**Por que PBR é eficiente?**
- Alto EBITDA relativo ao total de ativos — integração vertical do pré-sal
- Base de funcionários (~40.000) menor que majors como XOM (~61.000) ou Shell (~103.000)
- Alta receita dado o volume de ativos empregados

**Caveat importante (deve constar no relatório):** PBR foi identificada como outlier na ETAPA 2 em 3 das 5 variáveis. Sua eficiência no DEA pode ser em parte um artefato de sua escala desproporcionalmente grande — ela distorce a fronteira ao estabelecer um patamar de inputs/outputs que poucas outras DMUs conseguem replicar.

---

## 7. Checklist do Guia — Respondido

- [x] Quantas DMUs são eficientes no CCR? **9/22**
- [x] Quantas DMUs são eficientes no BCC? **10/22**
- [x] Eficiência média CCR: **1.0811** / BCC: **1.0591**
- [x] Benchmarks recorrentes: **EQNR (12×), PBR (10×)**
- [x] 3 DMUs mais ineficientes: **CNQ, Eni, CVX** com metas de +26%, +19%, +18,5%
- [x] Eficiência de escala: **XOM é o único caso com ineficiência puramente de escala**
- [x] Petrobras: **eficiente em ambos os modelos, 2º benchmark mais usado**
