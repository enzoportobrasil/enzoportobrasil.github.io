import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {pdf,cdf} from '../assets/js/bgev-math.mjs';
const refs=JSON.parse(readFileSync(new URL('./bgev-reference-vectors.json',import.meta.url)));
let max=0;
for(const r of refs){let e=0;for(const [x,y]of r.points){if(r.xi===-1&&Math.abs(x-1)<.001)continue;const expected=(r.panel?cdf:pdf)(x,r)*r.scale+r.zero;e=Math.max(e,Math.abs(y-expected)); const dx=.0007;const f=r.panel?cdf:pdf;const rounding=Math.max(Math.abs(f(x+dx,r)*r.scale+r.zero-expected),Math.abs(f(x-dx,r)*r.scale+r.zero-expected))+.035;assert.ok(Math.abs(y-expected)<rounding,'Residual exceeds propagated PDF coordinate rounding');}max=Math.max(max,e);console.log(r.xi,r.delta,r.panel,e.toFixed(4));}
console.log('Maximum PDF-coordinate residual:',max,'points');
