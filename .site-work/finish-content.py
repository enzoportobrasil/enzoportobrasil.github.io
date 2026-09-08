from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
for p in list(ROOT.glob('*.html'))+list((ROOT/'research').glob('*.html')):
 s=p.read_text(encoding='utf-8')
 # Keep official paper/manuscript titles in their publication language.
 for title in ['Extremes of Solar Spectral Irradiance in the SORCE/XPS Record','Multiple Imputation Methods under Extreme Values','Joint return levels of maximum temperature and minimum relative humidity by combining copulas with an extreme value framework for bimodal data','Conditional copula representations and extremal bounds for multivariate statistical functionals','Characterising complex dependence between extreme solar irradiance and air density','Bayesian hierarchical modelling of spatial extremes with BGEV marginals']:
  s=re.sub(r'(<(?:h[123]|div|a)[^>]*)(>'+re.escape(title)+r'<)',lambda m:m[1]+('' if 'lang=' in m[1] else ' lang="en"')+m[2],s)
 s=s.replace('value="en" lang="en"','value="en" lang="en" aria-label="English"').replace('value="pt" lang="pt-BR"','value="pt" lang="pt-BR" aria-label="Português"').replace('value="es" lang="es"','value="es" lang="es" aria-label="Español"')
 s=s.replace('hero-nebula-1600.webp 1600w','hero-nebula-1600.webp 1599w')
 # Mark original event names with their language, independent of UI selection.
 for tag in ['p','h3']:
  s=re.sub(r'(<'+tag+r' class="(?:talk-event-name|output-meta)"[^>]*>)([^<]*(?:Encontro|Reunião|Workshop em|Colóquio)[^<]*)(</'+tag+'>)',lambda m:m[1].replace('>',' lang="pt-BR">')+m[2]+m[3],s)
 p.write_text(s,encoding='utf-8')
# The original Portuguese presentation title remains directly below its adapted title.
p=ROOT/'talks.html';s=p.read_text(encoding='utf-8')
s=s.replace('<h2 id="natureza-title" lang="pt-BR">Extremos na Natureza<span>estatística, incerteza e previsão diante de fenômenos extremos</span>\n</h2>','<h2 id="natureza-title">Extremes in nature<span>statistics, uncertainty and prediction in the face of extreme phenomena</span></h2><p class="original-title" lang="pt-BR">Extremos na Natureza: estatística, incerteza e previsão diante de fenômenos extremos</p>')
s=s.replace('<h2 id="pibic-title" lang="pt-BR">Técnicas de Imputação para Variáveis Dicotômicas</h2>','<h2 id="pibic-title">Imputation techniques for dichotomous variables</h2><p class="original-title" lang="pt-BR">Técnicas de Imputação para Variáveis Dicotômicas</p>')
p.write_text(s,encoding='utf-8')
# Detailed mathematical derivation is retained as an explicitly labelled English reference.
p=ROOT/'assets/js/bgev-animation.mjs';s=p.read_text(encoding='utf-8');s=s.replace('<summary>Mathematics &amp; spatial model</summary>','<summary>Mathematics &amp; spatial model (English)</summary><div lang="en">').replace('</p></details>`);','</p></div></details>`);');p.write_text(s,encoding='utf-8')
