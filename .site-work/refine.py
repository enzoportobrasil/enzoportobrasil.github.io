from pathlib import Path
import re, json, hashlib, unicodedata
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
pages=list(ROOT.glob('*.html'))+list((ROOT/'research').glob('*.html'))
baseline={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file() and '.site-work' not in p.parts and not p.name.startswith('qa-')}
(ROOT/'.site-work/baseline.json').write_text(json.dumps(baseline),encoding='utf-8')
def edit(name, fn):
 p=ROOT/name; s=p.read_text(encoding='utf-8'); p.write_text(fn(s),encoding='utf-8')
def replaces(s, pairs):
 for a,b in pairs:
  if a not in s: raise ValueError('Missing text: '+a[:100])
  s=s.replace(a,b)
 return s

def home(s):
 s=replaces(s,[
 ('Statistics · Astrostatistics · Cosmology · Space Science · Scientific Computing','Statistician · Inference · Extreme events · Astrostatistics'),
 ('I develop statistical models for extreme and complex phenomena, combining spatio-temporal inference, Extreme Value Theory, simulation studies, and uncertainty quantification across environmental, astrophysics and general physical data, with an increasing focus on astrostatistics and space science.','I study extreme events, spatial structure and uncertainty through statistical inference and simulation. My work connects environmental and atmospheric questions with a growing research direction in astrostatistics.'),
 ('Como podemos traduzir a incerteza e o medo do desconhecido, em ciência acessível e clara?','How can we turn uncertainty about the unknown into clear, accessible science?'),
 ('Bayesian &amp; Classical inference','Bayesian &amp; frequentist inference'),('Uncertainty understanding ','Uncertainty quantification'),
 ('A Bayesian hierarchical spatial model with Bimodal Generelized Extrem Value (BGEV) marginals, spatially varying parameters, simulation assessment, and an application to relative-humidity-deficit extremes in the Amazon due to El Nino 2026 context.','How can a spatial model represent extremes when one marginal shape is too restrictive? My MSc dissertation develops a Bayesian hierarchical model with Bimodal Generalized Extreme Value (BGEV) marginals, applied to relative humidity deficit in the Amazon.'),
 ('BGEV · latent Gaussian fields · Complex systems · HIERARCHICAL MODELS · MCMC/HMC/NUTS · STAN &amp; R','BGEV · Gaussian spatial fields · HMC/NUTS in Stan'),
 ('Prbabolity foundation and Extreme Value Theory interpretation to NASA SORCE observations, marking a deliberate move toward statistical inference for physical and astronomical data.','What can a finite satellite record tell us about unusually large changes in solar irradiance? Extreme Value Theory meets the observational limits of NASA’s SORCE/XPS record.'),
 ('SORCE/XPS · EVT · observational physics','SORCE/XPS · Extreme Value Theory · Preprint'),
 ('Compound Extreme Phenomenon and Dependence','Compound Extremes &amp; Dependence'),
 ('Joint return levels and multivariate behaviour through copula and extreme value theory.','How does dependence change the frequency of joint extremes? Copulas connect temperature, humidity and multivariate risk.'),
 ('A incerteza pode ter mais informação do que imagina [...]','Uncertainty may tell us more than we expect.'),
 ('This is an intellectual progression rather than a claim of a perfectly linear chronology.','Questions that recur across my work, from missing observations to environmental and astronomical systems.'),
 ('Astronomy & Cosmology','Physical &amp; environmental systems'),
 ('Increasingly astronomical applications, from enviromental and earth problems, to fundamentals questions behind the Universe.','Environmental extremes and solar observations, with growing interests in astronomy and cosmology.'),
 ('How I approach scientific challenges ','How I tend to think about a scientific problem'),
 ('Inference before decoration','What observations can support'),
 ('Ask what a model says about a scientific question, which assumptions make that statement possible, and how uncertainty propagates.','I often begin by asking what the observations can support, which assumptions the answer depends on, and what remains uncertain.'),
 ('Use controlled settings to study recovery, calibration, sensitivity and failure modes before trusting observational conclusions.','Simulation and diagnostics help me examine recovery, calibration and failure modes, especially when the observations offer few ways to check an assumption.'),
 ('Move toward the physical system','The system behind the data'),
 ('Let the domain problem and measurement process shape the statistical modelling, rather than treating every dataset as interchangeable.','The scientific question and the measurement process help shape my modelling choices. Different problems call for different tools and collaborations.'),
 ('Lightweight, accessible, and built for the open web.','Statistics, uncertainty and scientific questions.'),
 ('Joint return levels of maximum temperature and minimum relative humidity...','Joint return levels of maximum temperature and minimum relative humidity by combining copulas with an extreme value framework for bimodal data')])
 bio='''<div class="profile-biography">
          <p>I trained in Statistics at the University of Brasília, drawn to a way of reasoning about uncertainty that could travel across scientific questions. Probability and inference remain my foundation, even as the systems I study change.</p>
          <p>My first research asked what could be recovered when observations were missing. Predictive modelling and simulation led me to a harder version of that question: what can we infer when the observations that matter most are scarce or extreme?</p>
          <p>That question now connects my work on spatial extremes, dependence and environmental data with solar irradiance and astrostatistics. Astronomy has long been a personal interest; it is increasingly a place where I can contribute quantitatively, alongside the environmental questions that continue to shape my research.</p>
        </div>'''
 s=re.sub(r'<div class="profile-biography">.*?</div>',lambda m:bio,s,flags=re.S)
 return s
edit('index.html',home)

def research(s):
 s=s.replace('The application areas change; the statistical problem often does not.','Each scientific setting brings different observational constraints to those questions.')
 s=s.replace('Problem, method and scientific setting—shown together.','Each direction brings together its research question, methods, papers and presentations.')
 s=s.replace('Statistical modelling of solar and astronomical observations, with particular interest in extreme signals, systematic uncertainty, dependence and model-based physical interpretation.','Extreme Value Theory applied to solar spectral irradiance, alongside related studies of solar and atmospheric dependence. The observational record and measurement uncertainty shape the interpretation.')
 s=s.replace('<section class="section methods-band">','''<section class="section tint" id="interdisciplinary"><div class="container"><div class="section-heading"><div><div class="kicker">Applied &amp; interdisciplinary work</div><h2>Quantitative work in public life.</h2></div></div><div class="archive-list">
<article><h3>Education &amp; public policy</h3><p>At Ipea, my work with national microdata and territorial information supported research on full-time education in Brazil. Technical notes, a book-chapter contribution and education presentations extend this work into public policy.</p><a class="text-link" href="talks.html#upcoming">Education presentations →</a></article>
<article><h3>Health services &amp; organisational data</h3><p>My public-sector work involves data quality, administrative records, reproducible analyses and statistical reporting. A coauthored article addresses labour relations, diversity, equity and inclusion at the Brazilian Hospital Services Company.</p><a class="text-link" href="publications.html#interdisciplinary">Related outputs →</a></article>
</div></div></section>
  <section class="section methods-band">''')
 return s
edit('research.html',research)

def figure(src,href,alt,caption,width,height):
 return f'<figure class="research-evidence"><a href="{href}"><img src="{src}" alt="{alt}" width="{width}" height="{height}" loading="lazy" decoding="async"></a><figcaption>{caption} <a href="{href}">View original PDF ↗</a></figcaption></figure>'
prefix='../assets/img/apresentacoes/'
project_figures={
 'missing-data-extremes':figure(prefix+'cobipe-2024/web/imputation-mse-1600.webp',prefix+'cobipe-2024/figures/imputation-mse-20-percent.pdf','Boxplots and density curves comparing mean squared error in four imputation scenarios.','Earlier work: simulation comparison presented at coBIPE 2024. This figure belongs to the undergraduate research direction, not the 2026 preprint.',1600,690),
 'solar-irradiance':figure(prefix+'sys2025/web/maxima-workflow-1600.webp',prefix+'sys2025/figures/ssi-air-density-maxima-workflow.pdf','Workflow connecting solar irradiance and air density observations to marginal models, copulas and risk curves.','Related solar–atmospheric work presented at sys2025, slide 29. This is a separate analysis from the SORCE/XPS preprint.',1600,1011),
 'climate-dependence':figure(prefix+'rbras-seagro-2025/web/temperature-humidity-poster-1200.webp',prefix+'rbras-seagro-2025/documents/temperature-humidity-poster.pdf','Complete poster on bivariate maximum temperature and minimum relative humidity in Brasília.','Earlier temperature–humidity work, presented at RBras/SEAGRO 2025. The complete poster preserves the methods and figures in their original context.',1200,1697)
}
links={
 'missing-data-extremes': [('PIBIC report · 2022',prefix+'pibic-2022/documents/dichotomous-imputation-full-text.pdf'),('coBIPE talk · 2024','../talks.html#cobipe-2024'),('WASA poster · 2024','../talks.html#wasa-2024'),('MICE and extremes poster · 2025',prefix+'emr-epbest-2025/documents/extremes-mice-poster.pdf')],
 'solar-irradiance':[('Solar irradiance poster · 2025',prefix+'emr-epbest-2025/documents/solar-irradiance-poster.pdf'),('Solar–atmospheric poster · 2025',prefix+'rbras-seagro-2025/documents/solar-irradiance-poster.pdf'),('Alabama talk · 2025','../talks.html#sys2025'),('UnB invited talk · 2026','../talks.html#extremos-na-natureza')],
 'climate-dependence':[('Temperature–humidity poster · 2025',prefix+'rbras-seagro-2025/documents/temperature-humidity-poster.pdf'),('Climate–financial risk poster · 2025',prefix+'rbras-seagro-2025/documents/climate-financial-risk-poster.pdf'),('RBras/SEAGRO presentations','../talks.html#rbras-seagro-2025')]
}
for slug in project_figures:
 def project(s):
  s=re.sub(r'<div class="figure-placeholder">.*?</div></div>',lambda m:project_figures[slug],s,flags=re.S)
  s=re.sub(r'<span>[^<]*add later</span>','',s)
  related='<h3>Related outputs</h3><div class="aside-list">'+''.join(f'<a href="{url}">{label} →</a>' for label,url in links[slug])+'</div>'
  s=s.replace('</aside>',related+'</aside>')
  if slug=='solar-irradiance':
   s=s.replace('developed as part of my transition from statistical methodology toward physical and astronomical observations.','bringing statistical methodology into dialogue with physical observations.')
   s=s.replace('The work examines the tail behaviour of solar spectral irradiance using <strong>Extreme Value Theory</strong>. Related research extended the question toward dependence between solar irradiance and atmospheric quantities through copula modelling and uncertainty in joint extremes.','The preprint models extremes of daily logarithmic irradiance changes in the 2005–2019 SORCE/XPS record using GEV distributions. Maximum likelihood fits are checked against probability weighted moments. Long return periods require extrapolation beyond this finite record; reported measurement uncertainty informs interpretation but is not propagated through the likelihood.')
   s=s.replace('This research produced posters and oral presentations, including an international talk','Related solar and atmospheric research produced posters and oral presentations, including an international talk')
  if slug=='missing-data-extremes':
   s=s.replace('The project uses simulation to separate the effects of missingness from the effects of tail behaviour. This makes it possible to examine how imputation choices affect downstream inference under conditions that are difficult to diagnose from a single real dataset.','I use Monte Carlo simulation and MICE in R to compare multiple imputation methods in regression settings, with and without extreme values. The comparisons examine how sample size, missingness and the fitted model affect predictive performance. Linear regression imputation performed best overall by cross-validated mean squared error in the studied scenarios; that result is not a universal ranking of methods.')
  return s
 edit('research/'+slug+'.html',project)

thesis=next((ROOT/'assets/img/research/02-spatial-extremes').glob('disserta*.pdf')).relative_to(ROOT).as_posix()
thesis_url=quote(thesis,safe='/')
def spatial(s):
 s=re.sub(r'\.\./assets/img/research/02-spatial-extremes/dissertac[^" ]+\.pdf','../'+thesis_url,s)
 s=s.replace('PDF · 37 MB','PDF · 39.2 MB')
 s=s.replace('</main>','''<section class="section compact"><div class="container content"><h2>From dissertation to research programme</h2><p>The dissertation brings together model construction, simulation assessment and an Amazon application. A methodological manuscript is in preparation; the dissertation remains the complete public account of this work.</p><div class="document-links"><a href="../talks.html#extremos-na-natureza">UnB talk on extremes · 2026 →</a><a href="../publications.html#in-preparation">Manuscripts in preparation →</a></div></div></section></main>''')
 return s
edit('research/spatial-extremes.html',spatial)

def publications(s):
 s=s.replace('This page prioritizes stable links such as arXiv and published sources. As papers move through review, journal links can replace status labels without changing the structure.','Papers, preprints and applied research outputs, with submission status distinguished from publication.')
 s=s.replace('Preprints / submitted','Preprints &amp; submitted manuscripts')
 s=s.replace('Work growing from the MSc','Manuscripts in preparation')
 s=s.replace('These entries should be updated conservatively. Keep “in preparation” until there is a public preprint or submission.','Ongoing work on spatial extremes and solar–atmospheric dependence.')
 s=s.replace('<section class="section tint">','<section class="section tint" id="in-preparation">')
 s=s.replace('<section class="section"><div class="container"><div class="section-heading"><div><div class="kicker">Interdisciplinary work','<section class="section" id="interdisciplinary"><div class="container"><div class="section-heading"><div><div class="kicker">Interdisciplinary work')
 ids=['solar-irradiance','missing-data-extremes','climate-dependence','climate-dependence']
 for slug,title in zip(ids,re.findall(r'<div class="output-title">(.*?)</div>',s)[:4]):
  s=s.replace(f'<div class="output-title">{title}</div>',f'<h3 class="output-title" lang="en">{title}</h3><a class="output-context" href="research/{slug}.html">Research context →</a>',1)
 return s
edit('publications.html',publications)
edit('cv.html',lambda s:s.replace('This web CV is intentionally more readable than a PDF and less exhaustive than an application dossier. The website should explain the trajectory; the downloadable CV should remain the formal record.','Statistician with a BSc and MSc from the University of Brasília. My work spans inference, extremes, spatial modelling and scientific computing, across environmental, astronomical and public-sector questions.').replace('Researcher working at the interface of statistical inference, astrostatistics and the physical sciences','Statistician working on inference, environmental extremes and astrostatistics').replace('<a class="button" href="publications.html">Research outputs</a>','<a class="button" href="research.html">Selected research</a><a class="button" href="publications.html">Research outputs</a>'))

resources=f'''<section class="page-hero"><div class="container"><div class="eyebrow">Resources</div><h1>A living archive of research materials.</h1><p class="lead">Dissertations, research reports, presentation materials and records of academic training.</p></div></section>
<section class="section compact" id="research-documents"><div class="container"><div class="section-heading"><h2>Theses &amp; research documents</h2></div><div class="archive-list">
<article><div class="output-year">2026 · MSc</div><h3>Statistical Modelling of Spatial Extremes in Complex Systems</h3><p>Complete dissertation · Universidade de Brasília · Portuguese · 168 pages · PDF · 39.2 MB</p><div class="document-links"><a href="{thesis_url}">Read the dissertation ↗</a><a href="research/spatial-extremes.html">Research context →</a></div></article>
<article><div class="output-year">2022 · PIBIC</div><h3 lang="pt-BR">Técnicas de Imputação para Variáveis Dicotômicas</h3><p>Undergraduate research report · Portuguese · 12 pages · PDF</p><div class="document-links"><a href="assets/img/apresentacoes/pibic-2022/documents/dichotomous-imputation-full-text.pdf">Open full text ↗</a><a href="research/missing-data-extremes.html">Research context →</a></div></article>
<article><h3>Slides &amp; posters</h3><p>Complete presentations and posters, organised by event and linked to their research directions.</p><a class="text-link" href="talks.html">Browse presentation materials →</a></article>
<article><h3>Code &amp; scientific computing</h3><p>Public repositories and computational work.</p><a class="text-link" href="https://github.com/enzoportobrasil" target="_blank" rel="noreferrer">GitHub ↗</a></article>
</div></div></section>
<section class="section tint" id="training"><div class="container"><div class="section-heading"><div><div class="kicker">Academic training archive</div><h2>Courses &amp; certificates</h2></div><p>Documented participation, research training and presentations. Each record identifies what its certificate establishes.</p></div>
<div class="archive-controls" hidden data-certificate-controls><label for="certificate-search">Search records</label><input id="certificate-search" type="search" placeholder="Title, institution or year" aria-controls="certificate-list"><label for="certificate-category">Category</label><select id="certificate-category" aria-controls="certificate-list"><option value="all">All categories</option><option value="statistics">Statistics &amp; Data Science</option><option value="astronomy">Astronomy &amp; Space Science</option><option value="research">Research Practice</option></select></div><p data-certificate-count role="status"></p>
<!-- certificates:start --><div id="certificate-list" class="archive-list"></div><!-- certificates:end -->
</div></section>'''
edit('resources.html',lambda s:re.sub(r'(?<=<main id="main">).*?(?=</main>)',lambda m:'\n'+resources+'\n',s,flags=re.S))

def talks(s):
 s=s.replace('Selected talks, the ideas behind them, and a few moments from the places and people around the research.','Talks and posters, with complete slides, research figures and records of the scientific events.')
 # Keep the personal album accessible but subordinate to the scientific figure.
 album=re.search(r'<section class="photo-album".*?</section>',s,re.S).group()
 s=s.replace(album,'')
 anchor='</article>\n<article class="talk-event" id="cobipe-2024"'
 s=s.replace(anchor,'<details class="event-archive"><summary>Photographs from Huntsville</summary>'+album+'</details>\n'+anchor)
 s=s.replace('<article class="talk-event" id="pibic-2022"','<article class="talk-event" id="pibic-2022"')
 s=s.replace('<div class="project-meta"><span>Undergraduate research · recorded presentation</span>','<p class="kicker">Earlier presentations</p><div class="project-meta"><span>Undergraduate research · recorded presentation</span>')
 # Related programmes, without claiming all posters are the same paper.
 related={'extremos-na-natureza':'spatial-extremes','sys2025':'solar-irradiance','cobipe-2024':'missing-data-extremes','wasa-2024':'missing-data-extremes','pibic-2022':'missing-data-extremes','emr-epbest-2025':'missing-data-extremes','rbras-seagro-2025':'climate-dependence'}
 for ident,slug in related.items():
  pat=r'(<article class="talk-event" id="'+ident+r'".*?<p class="talk-description">.*?</p>)'
  s=re.sub(pat,lambda m:m.group(1)+f'<p><a class="text-link" href="research/{slug}.html">Related research →</a></p>',s,count=1,flags=re.S)
 return s
edit('talks.html',talks)

for p in pages:
 s=p.read_text(encoding='utf-8'); rel='../' if p.parent.name=='research' else ''
 s=s.replace('<html lang="en">','<html lang="en" data-theme="dark">')
 s=s.replace('<meta name="viewport" content="width=device-width, initial-scale=1">','<meta name="viewport" content="width=device-width, initial-scale=1">\n<script src="'+rel+'assets/js/preferences.js"></script>')
 s=s.replace('<div class="nav-actions">','<div class="nav-actions"><label class="sr-only" for="site-language">Language</label><select id="site-language" data-language-select aria-label="Language"><option value="en" lang="en">EN</option><option value="pt" lang="pt-BR">PT</option><option value="es" lang="es">ES</option></select>')
 s=s.replace('data-nav-toggle aria-expanded="false" aria-label=', 'data-nav-toggle aria-expanded="false" aria-controls="primary-nav" aria-label=')
 s=s.replace('class="nav-links" data-nav', 'class="nav-links" id="primary-nav" data-nav')
 s=s.replace('id="primary-nav" data-nav>', 'id="primary-nav" data-nav aria-label="Primary navigation">')
 s=s.replace('>arXiv ↗</a>','>Read preprint on arXiv ↗</a>')
 s=s.replace('Research materials are curated to complement, not duplicate, the academic CV.','Statistics, uncertainty and scientific questions.')
 # Working static contact links when JS is unavailable.
 s=s.replace('data-link="email" href="#"','data-link="email" href="mailto:enzoportobrasil@gmail.com"')
 s=s.replace('data-link="github" href="#"','data-link="github" href="https://github.com/enzoportobrasil"')
 s=s.replace('data-link="linkedin" href="#"','data-link="linkedin" href="https://www.linkedin.com/in/enzo-porto-brasil-3231971b3/"')
 s=s.replace('<a data-link="orcid"', '<a class="is-hidden" data-link="orcid"')
 # Scientific preview dimensions and role: this is a plotted map, not a satellite photograph.
 s=s.replace('alt="Satellite view representing spatial extremes research"','alt="Map illustrating the spatial research direction; the dissertation contains the labelled results."')
 s=s.replace('alt="Solar observatory and extreme solar activity"','alt="Editorial illustration of a spacecraft beside the Sun; not a research result."')
 s=s.replace('alt="Solar observatory beside extreme solar activity"','alt="Editorial illustration of a spacecraft beside the Sun; not a research result."')
 # Metadata uses existing canonical domain.
 url='https://enzoportobrasil.github.io/'+('' if p.name=='index.html' else p.relative_to(ROOT).as_posix())
 if p.name!='404.html':
  title=re.search(r'<title>(.*?)</title>',s).group(1)
  desc=re.search(r'<meta name="description" content="(.*?)">',s).group(1)
  s=s.replace('</head>',f'<link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"></head>')
 s=s.replace('</body>','<script src="'+rel+'assets/i18n/translations.js"></script><script src="'+rel+'assets/js/i18n.js"></script></body>')
 if p.name=='404.html':
  s=s.replace('href="assets/','href="/assets/').replace('src="assets/','src="/assets/').replace('href="index.html"','href="/index.html"').replace('href="research.html"','href="/research.html"')
 p.write_text(s,encoding='utf-8')

# Keep development artifacts and reserves out of Pages output.
edit('_config.yml',lambda s:s+'\n  - .site-work\n  - docs\n  - tests\n  - tools\n  - assets/reserve\n  - assets/ASSETS_MANIFEST.md\n  - assets/ASSET_MIGRATION_REPORT.md\n')
edit('sitemap.xml',lambda s:s.replace('</urlset>',''.join(f'  <url><loc>https://enzoportobrasil.github.io/research/{slug}.html</loc></url>\n' for slug in ['spatial-extremes','missing-data-extremes','solar-irradiance','climate-dependence'])+'</urlset>'))
print('English editorial and architecture pass complete.')
