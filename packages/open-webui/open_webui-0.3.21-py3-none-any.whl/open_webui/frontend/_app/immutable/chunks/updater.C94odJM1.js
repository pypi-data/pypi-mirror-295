import{w as d}from"./create.BkENi-Q3.js";import{w as l}from"./index.CPPrZiJ5.js";import{G as f}from"./scheduler.zIJcXxfw.js";const m=(r,n)=>{const e=d(r),t=(o,s)=>{e.update(c=>{const u=o(c);let i=u;return n&&(i=n({curr:c,next:u})),s==null||s(i),i})};return{...e,update:t,set:o=>{t(()=>o)}}};function v(r){const n={};return Object.keys(r).forEach(e=>{const t=e,a=r[t];n[t]=d(l(a))}),n}function y(r,n){const e={};return n.forEach(t=>{e[t]={[`data-${r}-${t}`]:""}}),t=>e[t]}function g(r){return r?{"aria-disabled":"true","data-disabled":""}:{"aria-disabled":void 0,"data-disabled":void 0}}function w(){const r=f();return n=>{const{originalEvent:e}=n.detail,{cancelable:t}=n,a=e.type;r(a,{originalEvent:e,currentTarget:e.currentTarget},{cancelable:t})||n.preventDefault()}}function D(r){const n={};for(const e in r){const t=r[e];t!==void 0&&(n[e]=t)}return n}function k(r){return function(n,e){if(e===void 0)return;const t=r[n];t&&t.set(e)}}export{y as a,w as c,g as d,k as g,m as o,D as r,v as t};
//# sourceMappingURL=updater.C94odJM1.js.map
