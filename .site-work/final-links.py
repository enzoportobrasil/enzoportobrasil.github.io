from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
bsc='https://bdm.unb.br/handle/10483/38509'
paper='https://www.gov.br/hubrasil/pt-br/ensino-e-pesquisa/revista-juridica-da-ebserh/numero-atual/artigos-de-autores-convidados-1/relacoes-de-trabalho-na-empresa-brasileira-de-servicos-hospitalares-democratizacao-e-promocao-da-diversidade-da-equidade-e-da-inclusao.pdf'
p=ROOT/'resources.html';s=p.read_text(encoding='utf-8');s=s.replace('<article><div class="output-year">2022 · PIBIC</div>',f'<article><div class="output-year">2023 · BSc</div><h3 lang="pt-BR">Técnicas de imputação de dados faltantes com uso de modelagem preditiva</h3><p>BSc thesis · Universidade de Brasília · Portuguese · 61 pages</p><div class="document-links"><a href="{bsc}">University repository ↗</a><a href="research/missing-data-extremes.html">Research context →</a></div></article>\n<article><div class="output-year">2022 · PIBIC</div>');p.write_text(s,encoding='utf-8')
p=ROOT/'research/missing-data-extremes.html';s=p.read_text(encoding='utf-8');s=s.replace('<h3>Related outputs</h3><div class="aside-list">',f'<h3>Related outputs</h3><div class="aside-list"><a href="{bsc}">BSc thesis · 2023 ↗</a>');p.write_text(s,encoding='utf-8')
p=ROOT/'cv.html';s=p.read_text(encoding='utf-8');s=s.replace('<em>Imputation Methods for Missing Data Using Predictive Modelling</em>',f'<em lang="pt-BR"><a href="{bsc}">Técnicas de imputação de dados faltantes com uso de modelagem preditiva</a></em>');p.write_text(s,encoding='utf-8')
p=ROOT/'publications.html';s=p.read_text(encoding='utf-8');s=s.replace('<div class="output-title">Labor Relations at the Brazilian Hospital Services Company: Democratization and the Promotion of Diversity, Equity, and Inclusion</div>','<h3 class="output-title" lang="pt-BR">Relações de trabalho na Empresa Brasileira de Serviços Hospitalares: democratização e promoção da diversidade, da equidade e da inclusão</h3>');s=s.replace('2(2) · Portuguese</div></div><span class="status">Published</span>','2(2) · Portuguese</div><span class="status">Published</span></div><a class="button small" href="'+paper+'">Read article (PDF) ↗</a>');p.write_text(s,encoding='utf-8')
p=ROOT/'index.html';s=p.read_text(encoding='utf-8');s=s.replace('"@type":"Person","name":"Enzo Porto Brasil"','"@type":"Person","name":"Enzo Porto Brasil","jobTitle":"Statistician","url":"https://enzoportobrasil.github.io/","sameAs":["https://github.com/enzoportobrasil","https://www.linkedin.com/in/enzo-porto-brasil-3231971b3/"]');p.write_text(s,encoding='utf-8')
# Canonical English descriptions and titles remain in the head for discoverability.
p=ROOT/'assets/i18n/translations.js';s=p.read_text(encoding='utf-8');s=s.replace('`.trim().split', '''2023 · BSc|2023 · Graduação|2023 · Grado
BSc thesis · Universidade de Brasília · Portuguese · 61 pages|Trabalho de conclusão de curso · Universidade de Brasília · Português · 61 páginas|Trabajo de grado · Universidade de Brasília · Portugués · 61 páginas
University repository ↗|Repositório da universidade ↗|Repositorio de la universidad ↗
BSc thesis · 2023 ↗|Trabalho de graduação · 2023 ↗|Trabajo de grado · 2023 ↗
Read article (PDF) ↗|Ler artigo (PDF) ↗|Leer artículo (PDF) ↗
`.trim().split''')
# Remove identical repeated rows.
before,catalog,after=s.split('`',2);seen=set();lines=[]
for line in catalog.splitlines():
 if line not in seen:lines.append(line);seen.add(line)
p.write_text(before+'`'+'\n'.join(lines)+'\n`'+after,encoding='utf-8')
print('Added verified BSc repository and published article links.')
