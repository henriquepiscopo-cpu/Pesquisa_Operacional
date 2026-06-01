"""
Gerador do Relatório Final DEA em .docx
Formatação baseada em relatorio_metrologia_claudecomcapaprarevisar.docx
"""

import os
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ── Caminhos ────────────────────────────────────────────────────────────────
HERE  = os.path.dirname(os.path.abspath(__file__))
BASE  = os.path.dirname(HERE)
FIGS2 = os.path.join(BASE, "ETAPA 2", "figures")
FIGS4 = os.path.join(BASE, "ETAPA 4", "figures")
OUT   = os.path.join(HERE, "relatorio_final.docx")

# ── Helpers ──────────────────────────────────────────────────────────────────

def set_cell_border(cell, **kwargs):
    """Define bordas de célula via XML."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tag = OxmlElement(f'w:{edge}')
        tag.set(qn('w:val'), kwargs.get(edge, 'single'))
        tag.set(qn('w:sz'), '4')
        tag.set(qn('w:space'), '0')
        tag.set(qn('w:color'), '000000')
        tcBorders.append(tag)
    tcPr.append(tcBorders)

def add_run(para, text, bold=False, italic=False, size=12, color=None):
    run = para.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = 'Times New Roman'
    if color:
        run.font.color.rgb = RGBColor(*color)
    return run

def heading(doc, text, level='main'):
    """Adiciona cabeçalho de seção (maiúsculas, negrito, centralizado)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)
    add_run(p, text, bold=True, size=12)
    return p

def subheading(doc, title, rest=''):
    """Subseção em negrito inline com texto na sequência."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    fmt = p.paragraph_format
    fmt.space_before = Pt(6)
    fmt.space_after = Pt(0)
    fmt.first_line_indent = Cm(1.25)
    add_run(p, title, bold=True, size=12)
    if rest:
        add_run(p, rest, size=12)
    return p

def body(doc, text, indent=True):
    """Parágrafo de corpo de texto justificado."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    fmt = p.paragraph_format
    fmt.space_before = Pt(0)
    fmt.space_after = Pt(6)
    if indent:
        fmt.first_line_indent = Cm(1.25)
    add_run(p, text, size=12)
    return p

def caption(doc, text):
    """Legenda de figura/tabela: negrito + texto, centralizado."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fmt = p.paragraph_format
    fmt.space_before = Pt(2)
    fmt.space_after = Pt(10)
    # Divide em "Figura N." (bold) + resto
    if '. ' in text:
        label, rest = text.split('. ', 1)
        add_run(p, label + '. ', bold=True, size=10)
        add_run(p, rest, size=10)
    else:
        add_run(p, text, bold=True, size=10)
    return p

def add_figure(doc, path, caption_text, width=Cm(14)):
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        run = p.add_run()
        run.add_picture(path, width=width)
    else:
        p = doc.add_paragraph(f'[Figura não encontrada: {path}]')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption(doc, caption_text)

def add_table(doc, headers, rows, caption_text):
    """Cria tabela com cabeçalho em negrito e bordas simples."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Cabeçalho
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(10)
        run.font.name = 'Times New Roman'

    # Linhas de dados
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(val))
            run.font.size = Pt(10)
            run.font.name = 'Times New Roman'

    # Espaço + legenda
    doc.add_paragraph()
    caption(doc, caption_text)
    return table

def page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(docx_break_type())

def docx_break_type():
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    return br

def real_page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    run._r.append(br)


# ── Documento ────────────────────────────────────────────────────────────────

doc = Document()

# Margens (iguais ao modelo)
sec = doc.sections[0]
sec.top_margin    = Cm(2.54)
sec.bottom_margin = Cm(2.54)
sec.left_margin   = Cm(2.22)
sec.right_margin  = Cm(2.22)

# Estilo padrão
from docx.shared import Pt
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.paragraph_format.line_spacing = Pt(14)

# ════════════════════════════════════════════════════════════════════════════
# CAPA
# ════════════════════════════════════════════════════════════════════════════

# Cabeçalho direito
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
add_run(p, 'LE505 - Pesquisa Operacional', size=12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
add_run(p, 'Prof.ª Priscila Rampazzo', size=12)

# Espaço
for _ in range(6):
    doc.add_paragraph()

# Instituição
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_run(p, 'Universidade Estadual de Campinas', bold=True, size=14)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_run(p, 'FCA – Faculdade de Ciências Aplicadas', bold=True, size=13)

for _ in range(4):
    doc.add_paragraph()

# Título
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_run(p, 'Análise de Eficiência Relativa de Empresas de Petróleo e Gás\npor meio da Análise Envoltória de Dados (DEA)', size=12)

for _ in range(2):
    doc.add_paragraph()

# Data
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_run(p, 'Junho/2026', size=12)

for _ in range(4):
    doc.add_paragraph()

# Autoria
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
add_run(p, 'Henrique Arbex Rodrigues Piscopo', bold=True, size=12)
add_run(p, '          RA: 284675', bold=True, size=12)

for _ in range(6):
    doc.add_paragraph()

# Rodapé da capa
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_run(p, 'Limeira', size=12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
add_run(p, '2026', size=12)

real_page_break(doc)

# ════════════════════════════════════════════════════════════════════════════
# RESUMO
# ════════════════════════════════════════════════════════════════════════════

heading(doc, 'RESUMO')
body(doc, (
    'O presente trabalho aplica a Análise Envoltória de Dados (DEA) para mensurar a eficiência '
    'relativa de 22 empresas do setor de petróleo e gás listadas em bolsas internacionais. '
    'Foram empregados os modelos CCR (retornos constantes de escala) e BCC (retornos variáveis '
    'de escala), ambos com orientação a output, implementados em Python com uso da biblioteca '
    'PuLP para resolução dos problemas de programação linear. Os dados financeiros foram coletados '
    'via biblioteca yfinance, referentes ao exercício fiscal mais recente disponível, e compreendem '
    'três inputs — ativos totais, despesas operacionais e número de funcionários — e dois outputs '
    '— receita líquida e EBITDA. Os resultados indicam que 9 das 22 empresas (41%) são eficientes '
    'no modelo CCR e 10 (45%) no modelo BCC, com scores médios de 1,0811 e 1,0591, respectivamente. '
    'A Equinor (EQNR) e a Petrobras (PBR) emergem como benchmarks dominantes, sendo referenciadas '
    'por 12 e 10 DMUs ineficientes no modelo CCR, respectivamente. A Canadian Natural Resources (CNQ) '
    'é a empresa mais ineficiente da amostra (θ = 1,2597), seguida da Eni (θ = 1,1942) e da Chevron '
    '(θ = 1,1849). Conclui-se que a maioria das grandes empresas integradas do setor opera próximo '
    'à fronteira eficiente, com ineficiências moderadas atribuíveis a diferenças de modelo de negócio, '
    'escala de operação e contexto regulatório.'
))

# ════════════════════════════════════════════════════════════════════════════
# INTRODUÇÃO
# ════════════════════════════════════════════════════════════════════════════

heading(doc, 'INTRODUÇÃO')
body(doc, (
    'O setor de petróleo e gás é marcado por elevada intensidade de capital, volatilidade de preços '
    'e crescentes pressões regulatórias e ambientais. Nesse ambiente, a avaliação comparativa do '
    'desempenho das empresas torna-se instrumento estratégico para gestores, investidores e '
    'formuladores de políticas públicas. Métodos tradicionais de análise financeira, como indicadores '
    'de rentabilidade e retorno sobre ativos, avaliam empresas de forma isolada e são fortemente '
    'influenciados por variáveis de preço exógenas ao controle das firmas, o que limita a capacidade '
    'de identificar ineficiências genuinamente operacionais.'
))
body(doc, (
    'A Análise Envoltória de Dados (DEA), método não paramétrico desenvolvido por Charnes, Cooper e '
    'Rhodes (1978) e expandido por Banker, Charnes e Cooper (1984), oferece uma abordagem comparativa '
    'que constrói uma fronteira de melhores práticas a partir das próprias observações da amostra. '
    'Por meio da resolução de problemas de programação linear, o DEA identifica quais unidades de '
    'decisão (DMUs) operam na fronteira eficiente, quais estão aquém dela e em quanto cada unidade '
    'ineficiente precisaria expandir seus outputs para tornar-se eficiente.'
))
body(doc, (
    'Este trabalho tem por objetivo aplicar os modelos DEA-CCR e DEA-BCC, com orientação a output, '
    'para avaliar a eficiência relativa de 22 grandes empresas do setor de petróleo e gás, identificar '
    'os benchmarks setoriais e propor metas de melhoria para as unidades ineficientes.'
))

# ════════════════════════════════════════════════════════════════════════════
# APRESENTAÇÃO DO PROBLEMA
# ════════════════════════════════════════════════════════════════════════════

heading(doc, 'APRESENTAÇÃO DO PROBLEMA')

subheading(doc, 'Unidades de Decisão (DMUs). ',
    'A amostra é composta por 22 empresas do setor de petróleo e gás listadas em bolsas '
    'internacionais, abrangendo majors integradas, independentes de exploração, empresas de refino, '
    'serviços e midstream. As empresas selecionadas são megacorporações globais com operações em '
    'múltiplos países e dados reportados em dólares americanos, o que minimiza distorções de '
    'comparação internacional típicas de estudos com unidades puramente domésticas. '
    'A composição da amostra é apresentada na Tabela 1.')

add_table(doc,
    headers=['Ticker', 'Empresa', 'País', 'Segmento'],
    rows=[
        ('XOM','ExxonMobil','EUA','Integrada'),
        ('CVX','Chevron','EUA','Integrada'),
        ('SHEL','Shell','Reino Unido','Integrada'),
        ('BP','BP','Reino Unido','Integrada'),
        ('TTE','TotalEnergies','França','Integrada'),
        ('COP','ConocoPhillips','EUA','Exploração'),
        ('PBR','Petrobras','Brasil','Integrada'),
        ('EQNR','Equinor','Noruega','Integrada'),
        ('E','Eni','Itália','Integrada'),
        ('OXY','Occidental Petroleum','EUA','Exploração'),
        ('DVN','Devon Energy','EUA','Exploração'),
        ('VLO','Valero Energy','EUA','Refino'),
        ('PSX','Phillips 66','EUA','Refino'),
        ('MPC','Marathon Petroleum','EUA','Refino'),
        ('SLB','SLB (Schlumberger)','EUA','Serviços'),
        ('HAL','Halliburton','EUA','Serviços'),
        ('IMO','Imperial Oil','Canadá','Integrada'),
        ('CNQ','Canadian Natural Resources','Canadá','Exploração'),
        ('SU','Suncor Energy','Canadá','Integrada'),
        ('BKR','Baker Hughes','EUA','Serviços'),
        ('FTI','TechnipFMC','EUA/França','Serviços'),
        ('WMB','Williams Companies','EUA','Midstream'),
    ],
    caption_text='Tabela 1. Relação das DMUs analisadas, com ticker, empresa, país de origem e segmento de atuação.'
)

subheading(doc, 'Variáveis. ',
    'A escolha de variáveis seguiu os critérios de disponibilidade, representatividade econômica '
    'e ausência de multicolinearidade severa. Foram definidos três inputs e dois outputs, '
    'conforme apresentado na Tabela 2.')

add_table(doc,
    headers=['Tipo', 'Variável', 'Descrição'],
    rows=[
        ('Input','Total Assets','Ativos totais — proxy para capital empregado'),
        ('Input','Operating Expenses','Despesas operacionais — proxy para custos'),
        ('Input','Employees','Nº de funcionários — proxy para capital humano'),
        ('Output','Total Revenue','Receita líquida total'),
        ('Output','EBITDA','Lucro antes de juros, impostos, depreciação e amortização'),
    ],
    caption_text='Tabela 2. Variáveis utilizadas no modelo DEA, com tipo (input/output) e descrição.'
)

body(doc, (
    'A regra prática do DEA recomenda que o número de DMUs seja pelo menos três vezes a soma '
    'de inputs e outputs: 3 × (3 + 2) = 15. Com 22 DMUs, a regra é atendida com margem de '
    '7 unidades, conferindo adequada capacidade discriminatória ao modelo. Os dados foram coletados '
    'via API do Yahoo Finance (biblioteca yfinance, Python), com valores expressos em dólares '
    'americanos. Cinco empresas inicialmente selecionadas foram removidas da amostra por '
    'apresentarem dados incompletos (REP, MRO, HES, YPF, EC).'
))

subheading(doc, 'Limitações. ',
    'Algumas limitações metodológicas devem ser reconhecidas. A fonte de dados automática '
    '(Yahoo Finance) pode apresentar inconsistências para empresas listadas em bolsas não '
    'americanas. Os anos fiscais não são uniformes entre todas as empresas, podendo introduzir '
    'viés temporal. A Petrobras (PBR) foi identificada como outlier em três das cinco variáveis '
    'na análise exploratória, podendo distorcer a fronteira eficiente. Adicionalmente, a amostra '
    'inclui empresas de segmentos distintos, o que reduz parcialmente a homogeneidade das DMUs.'
)

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE ENVOLTÓRIA DE DADOS
# ════════════════════════════════════════════════════════════════════════════

heading(doc, 'ANÁLISE ENVOLTÓRIA DE DADOS')

subheading(doc, 'Introdução ao DEA. ',
    'A Análise Envoltória de Dados é uma técnica de programação matemática não paramétrica que '
    'avalia a eficiência relativa de unidades de decisão que compartilham o mesmo conjunto de '
    'inputs e outputs. Ao contrário de métodos paramétricos, o DEA não pressupõe uma forma '
    'funcional específica para a relação entre inputs e outputs, construindo a fronteira eficiente '
    'empiricamente a partir das melhores práticas observadas na amostra. Uma DMU é considerada '
    'eficiente quando nenhuma combinação linear das demais DMUs consegue produzir mais outputs '
    'com os mesmos ou menos inputs.'
)

subheading(doc, 'Modelo CCR. ',
    'O modelo CCR (Charnes, Cooper e Rhodes, 1978) assume retornos constantes de escala (CRS). '
    'Com orientação a output, busca o fator máximo θ pelo qual os outputs da DMU avaliada podem '
    'ser expandidos, mantendo os inputs fixos. Formalmente:'
)

# Equações CCR
for eq, num in [
    ('max  θ', '(1)'),
    ('s.a.   Σⱼ λⱼ xᵢⱼ ≤ xᵢₒ,   ∀ i', '(2)'),
    ('        Σⱼ λⱼ yᵣⱼ ≥ θ · yᵣₒ,  ∀ r', '(3)'),
    ('        λⱼ ≥ 0,   ∀ j', '(4)'),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Cm(3)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    add_run(p, f'{eq:<50}{num}', size=12)

body(doc, (
    'onde xᵢⱼ é o valor do input i da DMU j; yᵣⱼ é o valor do output r da DMU j; λⱼ são os '
    'pesos das DMUs de referência; e θ é o score de eficiência. Uma DMU é eficiente quando '
    'θ = 1,0; ineficiente quando θ > 1,0, indicando que os outputs poderiam ser expandidos '
    'pelo fator θ mantendo os inputs constantes.'
))

subheading(doc, 'Modelo BCC. ',
    'O modelo BCC (Banker, Charnes e Cooper, 1984) admite retornos variáveis de escala (VRS) '
    'por meio de uma restrição de convexidade adicional. A formulação é idêntica ao CCR com '
    'a inclusão de:'
)

for eq, num in [
    ('max  θ', '(5)'),
    ('s.a.   Σⱼ λⱼ xᵢⱼ ≤ xᵢₒ,   ∀ i', '(6)'),
    ('        Σⱼ λⱼ yᵣⱼ ≥ θ · yᵣₒ,  ∀ r', '(7)'),
    ('        λⱼ ≥ 0,   ∀ j', '(8)'),
    ('        Σⱼ λⱼ = 1', '(9)'),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Cm(3)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    add_run(p, f'{eq:<50}{num}', size=12)

body(doc, (
    'A restrição (9) garante que cada DMU seja comparada apenas com combinações convexas de '
    'outras DMUs de porte similar, eliminando o componente de ineficiência de escala.'
))

subheading(doc, 'Eficiência de Escala. ',
    'A eficiência de escala (SE) é obtida pela razão entre os scores dos dois modelos:'
)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.LEFT
p.paragraph_format.left_indent = Cm(3)
add_run(p, f'{"SE = θ_CCR / θ_BCC":<50}{"(10)"}', size=12)

body(doc, (
    'Quando SE = 1, a DMU opera na escala ótima (CRS). Quando SE > 1, há ineficiência de escala — '
    'a DMU operaria de forma mais eficiente em tamanho diferente do atual.'
))

subheading(doc, 'Orientação escolhida. ',
    'Adotou-se a orientação a output neste estudo, pois as empresas do setor operam com estrutura '
    'de ativos, força de trabalho e custos operacionais relativamente fixos no curto e médio prazo. '
    'A pergunta economicamente mais relevante é quanto mais receita e EBITDA cada empresa poderia '
    'gerar com os recursos que já possui, caso operasse sobre a fronteira eficiente.'
)

# ════════════════════════════════════════════════════════════════════════════
# RESULTADOS E DISCUSSÕES
# ════════════════════════════════════════════════════════════════════════════

real_page_break(doc)
heading(doc, 'RESULTADOS E DISCUSSÕES')

subheading(doc, 'Análise Exploratória dos Dados. ',
    'A análise exploratória revelou elevada dispersão nas variáveis, reflexo da heterogeneidade '
    'de porte entre as 22 DMUs. Os boxplots das variáveis normalizadas (Figura 5) evidenciam a '
    'presença de valores atípicos, especialmente nos outputs.'
)
add_figure(doc,
    os.path.join(FIGS2, 'boxplots.png'),
    'Figura 5. Boxplots das variáveis de input e output normalizadas pelo valor máximo da amostra.',
    width=Cm(14)
)

body(doc, (
    'A matriz de correlação (Figura 6) apresenta alta correlação positiva entre inputs e outputs, '
    'esperada pela relação entre porte e capacidade produtiva das empresas. A análise pelo método '
    'IQR identificou a Petrobras (PBR) como outlier em três variáveis: Total Assets, Receita '
    'Líquida e EBITDA. Seu porte desproporcionalmente elevado em relação à mediana da amostra '
    'pode favorecer artificialmente seu posicionamento como benchmark.'
))
add_figure(doc,
    os.path.join(FIGS2, 'correlation_heatmap.png'),
    'Figura 6. Matriz de correlação entre as variáveis de input e output.',
    width=Cm(11)
)

subheading(doc, 'Scores de Eficiência. ',
    'Os resultados dos modelos CCR e BCC são apresentados na Tabela 3. No modelo CCR, 9 das '
    '22 DMUs (41%) atingiram a fronteira eficiente (θ = 1,0000), enquanto no BCC esse número '
    'sobe para 10 DMUs (45%). O score médio CCR é 1,0811 e o BCC é 1,0591, indicando que as '
    'DMUs ineficientes precisariam expandir seus outputs em aproximadamente 8,1% e 5,9%, '
    'respectivamente, para atingir a fronteira.'
)

add_table(doc,
    headers=['DMU', 'Empresa', 'CCR', 'BCC', 'Ef. Escala', 'Efic. CCR', 'Efic. BCC'],
    rows=[
        ('XOM','ExxonMobil','1,1023','1,0000','1,1023','Não','Sim'),
        ('CVX','Chevron','1,1849','1,1281','1,0504','Não','Não'),
        ('SHEL','Shell','1,1356','1,0188','1,1146','Não','Não'),
        ('BP','BP','1,1522','1,0686','1,0782','Não','Não'),
        ('TTE','TotalEnergies','1,1495','1,0854','1,0591','Não','Não'),
        ('COP','ConocoPhillips','1,0587','1,0585','1,0002','Não','Não'),
        ('PBR','Petrobras','1,0000','1,0000','1,0000','Sim','Sim'),
        ('EQNR','Equinor','1,0000','1,0000','1,0000','Sim','Sim'),
        ('E','Eni','1,1942','1,1937','1,0004','Não','Não'),
        ('OXY','Occidental','1,1281','1,1253','1,0025','Não','Não'),
        ('DVN','Devon Energy','1,0000','1,0000','1,0000','Sim','Sim'),
        ('VLO','Valero','1,0000','1,0000','1,0000','Sim','Sim'),
        ('PSX','Phillips 66','1,0000','1,0000','1,0000','Sim','Sim'),
        ('MPC','Marathon Petro.','1,0000','1,0000','1,0000','Sim','Sim'),
        ('SLB','SLB','1,0976','1,0889','1,0080','Não','Não'),
        ('HAL','Halliburton','1,0504','1,0488','1,0015','Não','Não'),
        ('IMO','Imperial Oil','1,0000','1,0000','1,0000','Sim','Sim'),
        ('CNQ','Canadian Natural','1,2597','1,2438','1,0128','Não','Não'),
        ('SU','Suncor Energy','1,1513','1,1336','1,0156','Não','Não'),
        ('BKR','Baker Hughes','1,1199','1,1077','1,0110','Não','Não'),
        ('FTI','TechnipFMC','1,0000','1,0000','1,0000','Sim','Sim'),
        ('WMB','Williams Cos.','1,0000','1,0000','1,0000','Sim','Sim'),
    ],
    caption_text='Tabela 3. Scores de eficiência CCR, BCC e eficiência de escala para as 22 DMUs. Scores iguais a 1,0000 indicam DMU eficiente.'
)

body(doc, (
    'A distribuição dos scores é visualizada no histograma da Figura 1, que evidencia a '
    'concentração de DMUs na fronteira eficiente (θ = 1,0) e a cauda direita de ineficiências '
    'moderadas, com CNQ se destacando como caso extremo.'
))
add_figure(doc,
    os.path.join(FIGS4, 'histogram_efficiency.png'),
    'Figura 1. Distribuição dos scores de eficiência CCR e BCC. A linha vertical vermelha tracejada indica a fronteira eficiente (θ = 1,0).',
    width=Cm(14)
)

body(doc, 'O ranking de eficiência por empresa é apresentado na Figura 2.')
add_figure(doc,
    os.path.join(FIGS4, 'ranking_efficiency.png'),
    'Figura 2. Ranking de eficiência das 22 DMUs pelos scores CCR e BCC. Barras à direita da linha vermelha representam DMUs ineficientes.',
    width=Cm(14)
)

subheading(doc, 'DMUs Eficientes. ',
    'As empresas que atingiram a fronteira eficiente em cada modelo são sintetizadas na Tabela 4.'
)
add_table(doc,
    headers=['Modelo', 'DMUs Eficientes (θ = 1,0000)'],
    rows=[
        ('CCR', 'PBR, EQNR, DVN, VLO, PSX, MPC, IMO, FTI, WMB (9 empresas)'),
        ('BCC', 'XOM, PBR, EQNR, DVN, VLO, PSX, MPC, IMO, FTI, WMB (10 empresas)'),
    ],
    caption_text='Tabela 4. DMUs eficientes nos modelos CCR e BCC. XOM aparece eficiente exclusivamente no BCC, evidenciando ineficiência de escala.'
)

subheading(doc, 'Benchmarks e Lambdas. ',
    'O scatter plot CCR vs BCC (Figura 3) evidencia a relação entre os dois modelos e identifica '
    'visualmente os casos de ineficiência de escala — DMUs cujo score BCC é significativamente '
    'menor que o CCR.'
)
add_figure(doc,
    os.path.join(FIGS4, 'ccr_vs_bcc.png'),
    'Figura 3. Dispersão entre scores CCR e BCC por DMU. Pontos sobre a diagonal (y = x) indicam ausência de ineficiência de escala. XOM destaca-se pelo maior afastamento vertical.',
    width=Cm(12)
)

body(doc, (
    'As intensidades dos pesos λ das DMUs eficientes que compõem os benchmarks das ineficientes '
    'são visualizadas no heatmap da Figura 4 e detalhadas na Tabela 5.'
))
add_figure(doc,
    os.path.join(FIGS4, 'benchmark_heatmap.png'),
    'Figura 4. Heatmap de intensidade dos pesos λ (modelo CCR). Linhas: DMUs ineficientes; Colunas: DMUs eficientes utilizadas como benchmark.',
    width=Cm(14)
)

add_table(doc,
    headers=['DMU Ineficiente', 'Score CCR', 'Benchmarks (CCR)'],
    rows=[
        ('XOM','1,1023','PBR, EQNR, IMO'),
        ('CVX','1,1849','PBR, EQNR, IMO'),
        ('SHEL','1,1356','EQNR, MPC, FTI'),
        ('BP','1,1522','EQNR, FTI'),
        ('TTE','1,1495','PBR, EQNR'),
        ('COP','1,0587','PBR, EQNR, DVN'),
        ('E','1,1942','PBR, EQNR'),
        ('OXY','1,1281','PBR, WMB'),
        ('SLB','1,0976','PBR, EQNR'),
        ('HAL','1,0504','EQNR, FTI'),
        ('CNQ','1,2597','PBR, EQNR, DVN'),
        ('SU','1,1513','PBR, EQNR'),
        ('BKR','1,1199','PBR, EQNR'),
    ],
    caption_text='Tabela 5. Benchmarks das DMUs ineficientes no modelo CCR. EQNR é referência para 12 das 13 DMUs ineficientes; PBR, para 10.'
)

body(doc, (
    'A Equinor (EQNR) é o benchmark dominante, servindo de referência para 12 das 13 DMUs '
    'ineficientes no modelo CCR. Seu perfil — alta receita e EBITDA por ativo empregado, com '
    'base de funcionários enxuta (aproximadamente 22.000 colaboradores) — representa o padrão '
    'de excelência setorial. A Petrobras (PBR) aparece como segundo benchmark mais frequente '
    '(10 DMUs), combinando grande volume de outputs com integração vertical do pré-sal.'
))

subheading(doc, 'Metas de Melhoria para DMUs Ineficientes. ',
    'A orientação a output implica que as DMUs ineficientes deveriam, mantendo seus inputs atuais, '
    'expandir receita e EBITDA no percentual correspondente a (θ − 1) × 100%. '
    'As metas calculadas são apresentadas na Tabela 6 e visualizadas na Figura 7.'
)

add_table(doc,
    headers=['DMU', 'Score CCR', 'Receita Atual\n(USD bi)', 'Meta Receita\n(USD bi)', 'Aumento', 'EBITDA Atual\n(USD bi)', 'Meta EBITDA\n(USD bi)', 'Aumento'],
    rows=[
        ('CNQ','1,2597','38,6','48,7','+26,0%','14,8','18,6','+26,0%'),
        ('E (Eni)','1,1942','84,5','101,0','+19,4%','12,0','14,3','+19,4%'),
        ('CVX','1,1849','186,0','220,4','+18,5%','37,9','44,9','+18,5%'),
    ],
    caption_text='Tabela 6. Metas de melhoria para as três DMUs mais ineficientes no modelo CCR. Valores em bilhões de dólares americanos (USD bi).'
)

add_figure(doc,
    os.path.join(FIGS4, 'improvement_targets.png'),
    'Figura 7. Comparação entre outputs atuais e metas de melhoria para as três DMUs mais ineficientes (CNQ, Eni e Chevron), com orientação a output.',
    width=Cm(14)
)

body(doc, (
    'A Canadian Natural Resources (CNQ), com θ = 1,2597, é a empresa mais ineficiente da amostra. '
    'Sua principal fonte de ineficiência é estrutural: a empresa opera majoritariamente com extração '
    'de oil sands, cuja curva de custo por barril é significativamente superior à do petróleo '
    'convencional explorado por seus benchmarks (EQNR e DVN). A Eni (E), com θ = 1,1942, apresenta '
    'base de ativos e de funcionários elevada em relação ao nível de receita gerado. A Chevron (CVX), '
    'com θ = 1,1849, não extrai o máximo de receita e EBITDA de sua base de ativos, possivelmente '
    'em razão de estratégia conservadora de alocação de capital e maior diversificação geográfica.'
))

subheading(doc, 'Eficiência de Escala. ',
    'A eficiência de escala de cada DMU é apresentada na Tabela 7. Todas as DMUs apresentaram '
    'classificação CRS, com eficiências de escala muito próximas de 1,0 para a maioria das empresas.'
)

add_table(doc,
    headers=['DMU', 'Score CCR', 'Score BCC', 'Ef. Escala', 'Retorno de Escala'],
    rows=[
        ('XOM','1,1023','1,0000','1,1023','CRS'),('CVX','1,1849','1,1281','1,0504','CRS'),
        ('SHEL','1,1356','1,0188','1,1146','CRS'),('BP','1,1522','1,0686','1,0782','CRS'),
        ('TTE','1,1495','1,0854','1,0591','CRS'),('COP','1,0587','1,0585','1,0002','CRS'),
        ('PBR','1,0000','1,0000','1,0000','CRS'),('EQNR','1,0000','1,0000','1,0000','CRS'),
        ('E','1,1942','1,1937','1,0004','CRS'),('OXY','1,1281','1,1253','1,0025','CRS'),
        ('DVN','1,0000','1,0000','1,0000','CRS'),('VLO','1,0000','1,0000','1,0000','CRS'),
        ('PSX','1,0000','1,0000','1,0000','CRS'),('MPC','1,0000','1,0000','1,0000','CRS'),
        ('SLB','1,0976','1,0889','1,0080','CRS'),('HAL','1,0504','1,0488','1,0015','CRS'),
        ('IMO','1,0000','1,0000','1,0000','CRS'),('CNQ','1,2597','1,2438','1,0128','CRS'),
        ('SU','1,1513','1,1336','1,0156','CRS'),('BKR','1,1199','1,1077','1,0110','CRS'),
        ('FTI','1,0000','1,0000','1,0000','CRS'),('WMB','1,0000','1,0000','1,0000','CRS'),
    ],
    caption_text='Tabela 7. Eficiência de escala e tipo de retorno de escala para todas as DMUs.'
)

body(doc, (
    'O caso mais relevante é o da ExxonMobil (XOM), com SE = 1,1023 — a maior eficiência de '
    'escala da amostra. Seu score CCR de 1,1023 cai para 1,0000 no BCC, evidenciando que toda '
    'a ineficiência observada no modelo CCR é de natureza escalar, não operacional. A XOM opera '
    'de forma tecnicamente eficiente dado seu porte, mas sua escala de operação difere do ponto '
    'ótimo global identificado pelo modelo de retornos constantes.'
))

# ════════════════════════════════════════════════════════════════════════════
# CONCLUSÕES
# ════════════════════════════════════════════════════════════════════════════

real_page_break(doc)
heading(doc, 'CONCLUSÕES')
body(doc, (
    'O presente trabalho aplicou os modelos DEA-CCR e DEA-BCC, com orientação a output, para '
    'avaliar a eficiência relativa de 22 grandes empresas do setor de petróleo e gás. Os '
    'resultados permitiram identificar as melhores práticas setoriais, quantificar as ineficiências '
    'e propor metas concretas de melhoria de desempenho.'
))
body(doc, (
    '41% das DMUs (9/22) são eficientes no CCR e 45% (10/22) no BCC, com scores médios de 1,0811 '
    'e 1,0591 respectivamente, indicando ineficiências moderadas na maioria das empresas. '
    'A Equinor (EQNR) e a Petrobras (PBR) são os benchmarks dominantes — referências para 12 e '
    '10 DMUs ineficientes, respectivamente — representando os padrões de melhor prática setorial. '
    'A Canadian Natural Resources (CNQ) é a empresa mais ineficiente (θ = 1,2597), com '
    'ineficiência majoritariamente estrutural associada ao modelo de negócio de oil sands. '
    'A ExxonMobil (XOM) apresenta o caso mais didático de ineficiência de escala: '
    'operacionalmente eficiente no BCC, mas com SE = 1,1023 no CCR. As grandes majors europeias '
    '— Shell, BP, TotalEnergies e Eni — apresentam-se como ineficientes em ambos os modelos, '
    'com scores entre 1,02 e 1,19.'
))
body(doc, (
    'Para trabalhos futuros, recomenda-se a realização de análise de janela temporal (window '
    'analysis) para capturar a evolução da eficiência ao longo dos ciclos de preço do petróleo, '
    'a inclusão de variáveis ambientais e de governança (ESG) como outputs indesejáveis, e a '
    'aplicação de modelos DEA com outputs indesejáveis (emissões de CO₂) para refletir as '
    'externalidades do setor.'
))

# ════════════════════════════════════════════════════════════════════════════
# REFERÊNCIAS BIBLIOGRÁFICAS
# ════════════════════════════════════════════════════════════════════════════

heading(doc, 'REFERÊNCIAS BIBLIOGRÁFICAS')

refs = [
    ('BANKER, R. D.; CHARNES, A.; COOPER, W. W. ', 'Some models for estimating technical and scale inefficiencies in data envelopment analysis. ', 'Management Science', ', v. 30, n. 9, p. 1078–1092, 1984.'),
    ('CHARNES, A.; COOPER, W. W.; RHODES, E. ', 'Measuring the efficiency of decision making units. ', 'European Journal of Operational Research', ', v. 2, n. 6, p. 429–444, 1978.'),
    ('COOPER, W. W.; SEIFORD, L. M.; TONE, K. ', 'Data Envelopment Analysis: A Comprehensive Text with Models, Applications, References and DEA-Solver Software', '. 2. ed. New York: Springer, 2007.', ''),
    ('LINS, M. P. E.; MEZA, L. A. ', 'Análise Envoltória de Dados e Perspectivas de Integração no Ambiente de Apoio à Decisão', '. Rio de Janeiro: COPPE/UFRJ, 2000.', ''),
    ('MITCHELL, J. ', 'yfinance: Yahoo! Finance market data downloader', '. Disponível em: https://pypi.org/project/yfinance/. Acesso em: jun. 2025.', ''),
    ('MITCHELL, S. et al. ', 'PuLP: A Linear Programming toolkit for Python', '. Disponível em: https://pypi.org/project/PuLP/. Acesso em: jun. 2025.', ''),
]

for ref in refs:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Cm(1.25)
    p.paragraph_format.first_line_indent = Cm(-1.25)
    if len(ref) == 4:
        add_run(p, ref[0], bold=False, size=12)
        add_run(p, ref[1], italic=True, size=12)
        add_run(p, ref[2], bold=False, size=12)
        add_run(p, ref[3], size=12)
    else:
        add_run(p, ref[0], size=12)

# ── Salvar ───────────────────────────────────────────────────────────────────
doc.save(OUT)
print(f'Relatório salvo em: {OUT}')
