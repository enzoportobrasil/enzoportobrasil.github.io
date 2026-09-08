import {pdf,cdf,quantile,support,spatialSites} from './bgev-math.mjs';
const root=document.querySelector('[data-bgev]');
if(root){
const t=(value,parameters)=>window.SITE_I18N?.text(value,parameters)||value;
const sites=spatialSites(), reduced=matchMedia('(prefers-reduced-motion: reduce)');
root.querySelector('.bgev-fallback').hidden=true;
root.insertAdjacentHTML('beforeend',`
<div class="bgev-head"><div><div class="bgev-kicker">A distribution, constructed · 18 seconds</div><h2>Start with a GEV</h2></div><span class="bgev-step">01 / 04</span></div>
<div class="bgev-equations"></div>
<div class="bgev-spatial" hidden><div class="bgev-sites" role="group" aria-label="Select an illustrative location">${sites.map((p,i)=>`<button data-site="${i}" style="left:${p.s[0]*100}%;top:${p.s[1]*100}%" aria-label="Select location ${'ABC'[i]}">${'ABC'[i]}</button>`).join('')}</div><div class="bgev-site-copy"></div></div>
<div class="bgev-plots"><div><div class="bgev-plot-title"><span>Probability density</span><span class="bgev-params"></span></div><svg class="bgev-density" viewBox="0 0 560 290" role="img" aria-label="GEV reference and BGEV probability densities"></svg></div><div class="bgev-cdf"><div class="bgev-plot-title"><span>Cumulative probability</span><span>F(y)</span></div><svg viewBox="0 0 350 220" role="img" aria-label="Cumulative distribution, from zero to one"></svg></div></div>
<div class="bgev-legend"><span>Transformed BGEV</span><span>Initial GEV · ξ = 0, μ = 0, ϱ = 1</span></div>
<p class="bgev-note"></p>
<div class="bgev-controls"><label class="bgev-delta">δ <input type="range" min="0" max="3" step="0.01" value="0" aria-label="BGEV delta"><output aria-live="off">0.00</output></label><div class="bgev-presets" role="group" aria-label="Shape parameter presets"><button data-xi="-1">ξ = −1</button><button data-xi="0" aria-pressed="true">ξ = 0</button><button data-xi="1">ξ = +1</button></div><div class="bgev-presets" role="group" aria-label="Reference delta values"><button data-delta="0">δ = 0</button><button data-delta="1">δ = 1</button><button data-delta="3">δ = 3</button></div></div>
<div class="bgev-transport"><button class="bgev-play">Pause</button><button class="bgev-reset" aria-label="Restart animation">↺ Restart</button><input class="bgev-progress" type="range" min="0" max="18" step="0.01" value="0" aria-label="Animation progress in seconds"><span class="bgev-time">0.0 / 18 s</span></div>
<p class="bgev-footer">Bimodal Generalized Extreme Value · μ ∈ ℝ, ϱ &gt; 0, δ &gt; −1. Interactive range: 0 ≤ δ ≤ 3.</p>
<details><summary>Mathematics &amp; spatial model (English)</summary><div lang="en"><p>T(y) = (y − μ)|y − μ|<sup>δ</sup><br>F<sub>BGEV</sub>(y) = F<sub>GEV</sub>(T(y); ξ, 0, ϱ)<br>f<sub>BGEV</sub>(y) = f<sub>GEV</sub>(T(y); ξ, 0, ϱ) · (δ + 1)|y − μ|<sup>δ</sup></p><p>For ξ ≠ 0, the interior support satisfies 1 + ξT(y)/ϱ &gt; 0. For ξ = 0, F(y) = exp{−exp[−T(y)/ϱ]}. At δ = 0 the density is exactly GEV, including y = μ; at δ &gt; 0, f(μ) = 0. The pointwise change at μ is intentional.</p><p>Spatial links (Eq. 3.18): μ = g<sub>μ</sub>, ϱ = exp(g<sub>ϱ</sub>), δ = exp(g<sub>δ</sub>), ξ = ξ<sub>max</sub> tanh(g<sub>ξ</sub>). Here ξ<sub>max</sub> = 0.7. The spatial model uses δ &gt; 0, a subclass of δ &gt; −1.</p><p>Illustrative simulation, seed 2026: independent latent Gaussian fields evaluated jointly at three locations, m<sub>j</sub> = c<sub>j</sub><sup>⊤</sup>β<sub>j</sub>, k<sub>j</sub>(s,s′) = σ<sub>j</sub>² exp(−‖s−s′‖/α<sub>j</sub>). Dependence comes from the shared latent fields and conditional model; local marginals alone do not specify joint dependence. The grid is an abstract domain, not an estimated map.</p><p>Source: dissertation §2.1.2, Eqs. 2.6–2.12; §3.2 and Eq. 3.18. Curves are evaluated directly, without normalization to the plotted window.</p></div></details>`);
const $=s=>root.querySelector(s), $$=s=>root.querySelectorAll(s);
let time=0,playing=!reduced.matches,visible=false,manual=false,xi=0,delta=0,site=0,last=0,lastDraw=0,stage=-1;
const titles=['Start with a GEV','Transform the variable','Account for the Jacobian','Let parameters vary in space'];
const equations=[
'<p>X ∼ GEV(ξ, 0, ϱ)</p><p class="bgev-sub">Begin with ξ = 0, μ = 0 and ϱ = 1.</p>',
'<p>Y = T<sup>−1</sup>(X) = μ + sgn(X)|X|<sup>1/(δ+1)</sup></p><p class="bgev-sub">Fixed probabilities move to new positions. Marker height is not density.</p>',
'<p>F<sub>BGEV</sub>(y) = F<sub>GEV</sub>(T(y); ξ, 0, ϱ)</p><p>f<sub>BGEV</sub>(y) = f<sub>GEV</sub>(T(y); ξ, 0, ϱ) · <span class="bgev-jac">(δ+1)|y−μ|<sup>δ</sup></span></p>',
'<p>θ<sub>j</sub>(s) = h<sub>j</sub>(g<sub>j</sub>(s)), &nbsp; g<sub>j</sub> ∼ GP(m<sub>j</sub>, k<sub>j</sub>)</p><p>Y(s) | θ(s) ∼ BGEV(ξ(s), μ(s), ϱ(s), δ(s))</p>'
];
function curve(fn,p,w,h,maxY,isCDF=false){
 const l=42,r=w-16,top=16,b=h-52,xmin=-4,xmax=8, X=x=>l+(x-xmin)/(xmax-xmin)*(r-l),Y=y=>b-y/maxY*(b-top);
 const [lo,hi]=support(p), pts=[];for(let i=0;i<=1000;i++)pts.push(xmin+i/1000*(xmax-xmin));
 pts.push(p.mu??0);if(lo>=xmin&&lo<=xmax)pts.push(lo);if(hi>=xmin&&hi<=xmax)pts.push(hi);pts.sort((a,b)=>a-b);
 let d='',started=false;for(const x of pts){if(!isCDF&&(x<lo||x>hi)){started=false;continue;}const y=fn(x,p);if(!Number.isFinite(y)){started=false;continue;}d+=(started?'L':'M')+X(x).toFixed(2)+','+Y(y).toFixed(2);started=true;}
 return {d,X,Y,l,r,top,b,lo,hi};
}
function plot(el,p,isCDF=false,markers=false){
 const mobile=matchMedia('(max-width:620px)').matches,w=isCDF||mobile?350:560,h=isCDF?(mobile?165:220):(mobile?240:290),max=isCDF?1:p.xi===-1?4.3:1.8;
 const f=isCDF?cdf:pdf,a=curve(f,p,w,h,max,isCDF),ref=curve(f,{xi:0,mu:0,rho:1,delta:0},w,h,max,isCDF);
 let svg='';for(const y of isCDF?[0,.5,1]:p.xi===-1?[0,1,2,3,4]:[0,.5,1,1.5])svg+=`<path class="grid" d="M${a.l},${a.Y(y)}H${a.r}"/><text x="${a.l-9}" y="${a.Y(y)+4}" text-anchor="end">${y}</text>`;
 for(const x of (mobile?[-4,0,4,8]:[-4,-2,0,2,4,6,8]))svg+=`<text x="${a.X(x)}" y="${a.b+19}" text-anchor="middle">${x}</text>`;
 svg+=`<path class="axis" d="M${a.l},${a.top}V${a.b}H${a.r}"/><text x="${a.r}" y="${a.b+37}" text-anchor="end">y</text><path class="reference" d="${ref.d}"/><path class="curve" d="${a.d}"/>`;
 if(!isCDF&&Number.isFinite(a.hi)&&a.hi<=8&&a.hi>=-4){const y=pdf(a.hi,p);if(Number.isFinite(y)&&y<=max)svg+=`<circle cx="${a.X(a.hi)}" cy="${a.Y(y)}" r="3.5" fill="#b94d11"/><path class="axis" stroke-dasharray="2 4" d="M${a.X(a.hi)},${a.Y(y)}V${a.b}"/>`;}
 if(markers&&!isCDF){const probs=[.1,.3,.5,.7,.9];svg+=`<path class="axis" d="M${a.l},${h-12}H${a.r}"/>`;for(const prob of probs)svg+=`<circle class="quantile" cx="${a.X(quantile(prob,p))}" cy="${h-12}" r="4"><title>Fixed p = ${prob}; Q(p) = ${quantile(prob,p).toFixed(3)}</title></circle>`;}
 el.setAttribute('viewBox',`0 0 ${w} ${h}`);el.innerHTML=svg;
}
function render(){
 let s=manual?2:time<3?0:time<7?1:time<12?2:3;
 if(!manual){xi=0;delta=time<3?0:time<7?(time-3)/4:time<12?1+2*(time-7)/5:3;if(s===3)site=Math.min(2,Math.floor((time-12)/2));}
 const spatial=s===3,p=spatial?sites[site]:{xi,mu:0,rho:1,delta};
 if(stage!==s){$('h2').textContent=t(titles[s]);$('.bgev-step').textContent=`0${s+1} / 04`;$('.bgev-equations').innerHTML=equations[s];stage=s;window.SITE_I18N?.translate(root);}
 root.classList.toggle('bgev-highlight',s===2&&time<9&&!manual);root.classList.toggle('bgev-restart',time>17.65&&!manual&&playing&&!reduced.matches);
 $('.bgev-spatial').hidden=!spatial;
 if(spatial){$('.bgev-site-copy').innerHTML=`<strong>${t('Location {site} → orange density',{site:'ABC'[site]})}</strong><br>μ = ${p.mu.toFixed(2)} · ϱ = ${p.rho.toFixed(2)}<br>ξ = ${p.xi.toFixed(2)} · δ = ${p.delta.toFixed(2)}<br><span class="bgev-sub">${t('Illustrative simulation · seed 2026')}</span>`;$$('[data-site]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.site)===site));}
 $('.bgev-params').textContent=`ξ ${p.xi.toFixed(2)} · δ ${p.delta.toFixed(2)}`;
 plot($('.bgev-density'),p,false,s===1||s===2);plot($('.bgev-cdf svg'),p,true);
 const mass=(cdf(-4,p)+1-cdf(8,p))*100;
 $('.bgev-note').textContent=(s===1||s===2?t('Quantile rail: p = 0.1, 0.3, 0.5, 0.7, 0.9.')+' ':'')+t('Fixed window −4 ≤ y ≤ 8; {mass}% probability outside.',{mass:mass.toFixed(2)})+' '+(p.xi===-1?t('Left density limit at y = 1: {limit}; density is zero beyond support.',{limit:(p.delta+1).toFixed(2)}):t('Curves are not renormalized.'));
 $('.bgev-delta input').value=p.delta;$('.bgev-delta output').textContent=p.delta.toFixed(2);
 $$('[data-xi]').forEach(b=>b.setAttribute('aria-pressed',!spatial&&Number(b.dataset.xi)===xi));$$('[data-delta]').forEach(b=>b.setAttribute('aria-pressed',!spatial&&Number(b.dataset.delta)===delta));
 $('.bgev-progress').value=time;$('.bgev-time').textContent=`${time.toFixed(1)} / 18 s`;$('.bgev-play').textContent=t(playing?'Pause':'Play');
}
function pause(){playing=false;last=0;}
function explore(){pause();manual=true;}
$('.bgev-delta input').addEventListener('input',e=>{explore();delta=Number(e.target.value);render();});
$$('[data-xi]').forEach(b=>b.addEventListener('click',()=>{explore();xi=Number(b.dataset.xi);render();}));
$$('[data-delta]').forEach(b=>b.addEventListener('click',()=>{explore();delta=Number(b.dataset.delta);render();}));
$$('[data-site]').forEach(b=>b.addEventListener('click',()=>{pause();manual=false;time=12+Number(b.dataset.site)*2;render();}));
$('.bgev-progress').addEventListener('input',e=>{pause();manual=false;time=Number(e.target.value);render();});
$('.bgev-play').addEventListener('click',()=>{if(manual){manual=false;time=0;}if(time>=18)time=0;playing=!playing;last=0;render();});
$('.bgev-reset').addEventListener('click',()=>{time=0;manual=false;last=0;playing=!reduced.matches;render();});
reduced.addEventListener('change',()=>{if(reduced.matches){pause();render();}});
new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;last=0;},{threshold:.12}).observe(root);
document.addEventListener('visibilitychange',()=>{last=0;});
function tick(now){if(playing&&visible&&!document.hidden){if(last)time+=(now-last)/1000;last=now;if(time>=18){time=0;stage=-1;}if(now-lastDraw>32){render();lastDraw=now;}}else last=0;requestAnimationFrame(tick);}
window.addEventListener('resize',()=>requestAnimationFrame(render));
document.addEventListener('site:language',()=>{stage=-1;render();});
render();requestAnimationFrame(tick);
}
