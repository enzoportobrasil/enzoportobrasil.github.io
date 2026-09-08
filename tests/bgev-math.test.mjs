import assert from 'node:assert/strict';
import {pdf,cdf,quantile,gevPDF,gevCDF,support,spatialSites} from '../assets/js/bgev-math.mjs';
const near=(a,b,t=1e-8)=>assert.ok(Math.abs(a-b)<=t,`${a} ≠ ${b}, tolerance ${t}`);
function integral(f,a,b,tol=1e-9){
 const sim=(a,b,fa,fm,fb)=>(b-a)*(fa+4*fm+fb)/6;
 function rec(a,b,fa,fm,fb,v,t,n){const m=(a+b)/2,l=f((a+m)/2),r=f((m+b)/2),vl=sim(a,m,fa,l,fm),vr=sim(m,b,fm,r,fb);if(n===0||Math.abs(vl+vr-v)<15*t)return vl+vr+(vl+vr-v)/15;return rec(a,m,fa,l,fm,vl,t/2,n-1)+rec(m,b,fm,r,fb,vr,t/2,n-1);}
 const m=(a+b)/2,fa=f(a),fm=f(m),fb=f(b);return rec(a,b,fa,fm,fb,sim(a,b,fa,fm,fb),tol,28);
}
let maxIntegral=0,maxDerivative=0,maxQuantile=0;
const cases=[];for(const xi of [-1,0,1,-1e-9,1e-9,-1.5,-.5])for(const delta of [0,1,3])cases.push({xi,mu:0,rho:1,delta});cases.push(...spatialSites(),{xi:.2,mu:2,rho:1.4,delta:.01});
for(const p of cases){
 near(cdf(-Infinity,p),0);near(cdf(Infinity,p),1);
 let previous=0;for(let i=0;i<=1000;i++){const y=-10+i*.03,v=cdf(y,p);assert.ok(v>=previous);assert.ok(!Number.isNaN(pdf(y,p)));previous=v;}
 const probs=[1e-10,1e-8,1e-6,.0001,.001,.01,.1,.3,Math.exp(-1),.5,.7,.9,.99,.999,.9999,1-1e-6,1-1e-8,1-1e-10];
 const cuts=probs.map(v=>quantile(v,p));let sum=0;for(let i=1;i<cuts.length;i++)sum+=integral(y=>pdf(y,p),cuts[i-1],cuts[i]);maxIntegral=Math.max(maxIntegral,Math.abs(sum-1));near(sum,1,2e-6);
 for(const prob of probs){const q=quantile(prob,p),error=Math.abs(cdf(q,p)-prob);maxQuantile=Math.max(maxQuantile,error);near(cdf(q,p),prob,2e-8);}
 for(const y of [-1.3,-.4,.25,.7,1.4,2.5]){const [lo,hi]=support(p);if(y<=lo+1e-4||y>=hi-1e-4||Math.abs(y-p.mu)<1e-4)continue;const d=(cdf(y+1e-6,p)-cdf(y-1e-6,p))/2e-6,err=Math.abs(d-pdf(y,p));maxDerivative=Math.max(maxDerivative,err);near(d,pdf(y,p),2e-7);}
 if(p.delta===0)for(const y of [-10,-1,0,1,10]){near(pdf(y,p),gevPDF(y-p.mu,p.xi,p.rho));near(cdf(y,p),gevCDF(y-p.mu,p.xi,p.rho));}
 if(p.delta>0)near(pdf(p.mu,p),0);
}
for(const delta of [0,1,3]){const p={xi:-1,delta};near(pdf(1,p),delta+1);near(pdf(1+1e-10,p),0);near(cdf(1,p),1);near(pdf(1-1e-9,p),delta+1,1e-7);}
near(pdf(0,{delta:0}),Math.exp(-1));near(pdf(0,{delta:1e-12}),0);
for(const y of [-2,-.1,0,.1,2,10])for(const delta of [0,1,3])for(const xi of [-1e-10,1e-10]){near(cdf(y,{xi,delta}),cdf(y,{xi:0,delta}),1e-8);near(pdf(y,{xi,delta}),pdf(y,{xi:0,delta}),1e-8);}
assert.equal(pdf(.5,{xi:-2,rho:1,delta:0}),Infinity);assert.equal(pdf(2,{xi:-.5,delta:0}),0);
assert.deepEqual(spatialSites(),spatialSites());
console.log(JSON.stringify({cases:cases.length,maxIntegralError:maxIntegral,maxDerivativeError:maxDerivative,maxQuantileError:maxQuantile,tailMassOmitted:2e-10,sites:spatialSites()},null,2));
