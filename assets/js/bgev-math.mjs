// Bimodal GEV, dissertation equations 2.6–2.12. No window normalization.
export function validate({xi=0,mu=0,rho=1,delta=0}={}) {
 if (![xi,mu,rho,delta].every(Number.isFinite)||rho<=0||delta<=-1) throw new RangeError('Invalid BGEV parameters');
 return {xi,mu,rho,delta};
}
export const transform=(y,mu,delta)=>delta===0?y-mu:Math.sign(y-mu)*Math.pow(Math.abs(y-mu),delta+1);
export const inverse=(x,mu,delta)=>mu+(delta===0?x:Math.sign(x)*Math.pow(Math.abs(x),1/(delta+1)));
export function support(p={}) {const {xi,mu,rho,delta}=validate(p);const b=xi===0?0:inverse(-rho/xi,mu,delta);return xi>0?[b,Infinity]:xi<0?[-Infinity,b]:[-Infinity,Infinity];}
export function gevCDF(x,xi=0,rho=1) {
 if(x===-Infinity)return 0;if(x===Infinity)return 1;
 const z=x/rho;if(xi!==0&&1+xi*z<=0)return xi>0?0:1;
 const a=xi===0?-z:-Math.log1p(xi*z)/xi;
 return Math.exp(-Math.exp(a));
}
export function gevLogPDF(x,xi=0,rho=1) {
 if(!Number.isFinite(x))return -Infinity;
 const z=x/rho,t=1+xi*z;
 if(xi!==0&&t<0)return -Infinity;
 if(xi!==0&&t===0)return xi>0||xi> -1?-Infinity:xi===-1?-Math.log(rho):Infinity;
 const a=xi===0?-z:-Math.log1p(xi*z)/xi;
 if(a>709)return -Infinity;
 return -Math.log(rho)+(1+xi)*a-Math.exp(a);
}
export const gevPDF=(x,xi=0,rho=1)=>Math.exp(gevLogPDF(x,xi,rho));
export function cdf(y,p={}) {const {xi,mu,rho,delta}=validate(p);const [lo,hi]=support(p);if(y<=lo)return 0;if(y>=hi)return 1;return gevCDF(transform(y,mu,delta),xi,rho);}
export function pdf(y,p={}) {
 const {xi,mu,rho,delta}=validate(p),[lo,hi]=support(p);
 if(y<lo||y>hi||!Number.isFinite(y))return 0;
 if(delta===0)return gevPDF(y-mu,xi,rho);
 if(y===mu)return delta>0?0:Infinity;
 const logJ=Math.log1p(delta)+delta*Math.log(Math.abs(y-mu));
 if(y===hi&&xi<0)return xi> -1?0:xi===-1?Math.exp(logJ)/rho:Infinity;
 if(y===lo&&xi>0)return 0;
 return Math.exp(gevLogPDF(transform(y,mu,delta),xi,rho)+logJ);
}
export function quantile(prob,p={}) {
 const {xi,mu,rho,delta}=validate(p);if(prob<0||prob>1||Number.isNaN(prob))throw new RangeError('Probability outside [0,1]');
 if(prob===0)return support(p)[0];if(prob===1)return support(p)[1];
 const l=Math.log(-Math.log(prob));
 return inverse(xi===0?-rho*l:rho*Math.expm1(-xi*l)/xi,mu,delta);
}
// Exact finite-dimensional GP draws at three sites, exponential covariance.
export function spatialSites(seed=2026) {
 const sites=[[.18,.68],[.5,.28],[.82,.62]],L=sites.map(()=>[0,0,0]);
 const random=()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return (seed+.5)/4294967296;};
 const normal=()=>Math.sqrt(-2*Math.log(random()))*Math.cos(2*Math.PI*random());
 for(let i=0;i<3;i++)for(let j=0;j<=i;j++){let a=Math.exp(-Math.hypot(sites[i][0]-sites[j][0],sites[i][1]-sites[j][1])/.55);for(let k=0;k<j;k++)a-=L[i][k]*L[j][k];L[i][j]=i===j?Math.sqrt(a):a/L[j][j];}
 const fields=[0,0,0,.2].map((m,j)=>{const z=sites.map(normal);return sites.map((_,i)=>m+[.35,.55,.18,.28][j]*L[i].reduce((a,v,k)=>a+v*z[k],0));});
 return sites.map((s,i)=>({s,xi:.7*Math.tanh(fields[0][i]),mu:fields[1][i],rho:Math.exp(fields[2][i]),delta:Math.exp(fields[3][i])}));
}
