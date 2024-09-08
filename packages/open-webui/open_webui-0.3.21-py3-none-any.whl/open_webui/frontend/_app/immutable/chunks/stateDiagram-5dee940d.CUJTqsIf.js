import{p as P,d as N,s as W}from"./styles-0784dbeb.D1SpV_dD.js";import{c as t,h as H,l as b,i as R,j as T,x as v,u as U}from"./Messages.C1lVODGw.js";import{G as C}from"./graph.BJgDJdeF.js";import{l as F}from"./layout.HCFqc6Ni.js";import"./dayjs.min.CnqrW7zs.js";import{l as $}from"./line.CCxlCCKr.js";const O=e=>e.append("circle").attr("class","start-state").attr("r",t().state.sizeUnit).attr("cx",t().state.padding+t().state.sizeUnit).attr("cy",t().state.padding+t().state.sizeUnit),X=e=>e.append("line").style("stroke","grey").style("stroke-dasharray","3").attr("x1",t().state.textHeight).attr("class","divider").attr("x2",t().state.textHeight*2).attr("y1",0).attr("y2",0),J=(e,i)=>{const o=e.append("text").attr("x",2*t().state.padding).attr("y",t().state.textHeight+2*t().state.padding).attr("font-size",t().state.fontSize).attr("class","state-title").text(i.id),c=o.node().getBBox();return e.insert("rect",":first-child").attr("x",t().state.padding).attr("y",t().state.padding).attr("width",c.width+2*t().state.padding).attr("height",c.height+2*t().state.padding).attr("rx",t().state.radius),o},Y=(e,i)=>{const o=function(l,m,w){const E=l.append("tspan").attr("x",2*t().state.padding).text(m);w||E.attr("dy",t().state.textHeight)},s=e.append("text").attr("x",2*t().state.padding).attr("y",t().state.textHeight+1.3*t().state.padding).attr("font-size",t().state.fontSize).attr("class","state-title").text(i.descriptions[0]).node().getBBox(),g=s.height,p=e.append("text").attr("x",t().state.padding).attr("y",g+t().state.padding*.4+t().state.dividerMargin+t().state.textHeight).attr("class","state-description");let a=!0,r=!0;i.descriptions.forEach(function(l){a||(o(p,l,r),r=!1),a=!1});const y=e.append("line").attr("x1",t().state.padding).attr("y1",t().state.padding+g+t().state.dividerMargin/2).attr("y2",t().state.padding+g+t().state.dividerMargin/2).attr("class","descr-divider"),x=p.node().getBBox(),d=Math.max(x.width,s.width);return y.attr("x2",d+3*t().state.padding),e.insert("rect",":first-child").attr("x",t().state.padding).attr("y",t().state.padding).attr("width",d+2*t().state.padding).attr("height",x.height+g+2*t().state.padding).attr("rx",t().state.radius),e},I=(e,i,o)=>{const c=t().state.padding,s=2*t().state.padding,g=e.node().getBBox(),p=g.width,a=g.x,r=e.append("text").attr("x",0).attr("y",t().state.titleShift).attr("font-size",t().state.fontSize).attr("class","state-title").text(i.id),x=r.node().getBBox().width+s;let d=Math.max(x,p);d===p&&(d=d+s);let l;const m=e.node().getBBox();i.doc,l=a-c,x>p&&(l=(p-d)/2+c),Math.abs(a-m.x)<c&&x>p&&(l=a-(x-p)/2);const w=1-t().state.textHeight;return e.insert("rect",":first-child").attr("x",l).attr("y",w).attr("class",o?"alt-composit":"composit").attr("width",d).attr("height",m.height+t().state.textHeight+t().state.titleShift+1).attr("rx","0"),r.attr("x",l+c),x<=p&&r.attr("x",a+(d-s)/2-x/2+c),e.insert("rect",":first-child").attr("x",l).attr("y",t().state.titleShift-t().state.textHeight-t().state.padding).attr("width",d).attr("height",t().state.textHeight*3).attr("rx",t().state.radius),e.insert("rect",":first-child").attr("x",l).attr("y",t().state.titleShift-t().state.textHeight-t().state.padding).attr("width",d).attr("height",m.height+3+2*t().state.textHeight).attr("rx",t().state.radius),e},_=e=>(e.append("circle").attr("class","end-state-outer").attr("r",t().state.sizeUnit+t().state.miniPadding).attr("cx",t().state.padding+t().state.sizeUnit+t().state.miniPadding).attr("cy",t().state.padding+t().state.sizeUnit+t().state.miniPadding),e.append("circle").attr("class","end-state-inner").attr("r",t().state.sizeUnit).attr("cx",t().state.padding+t().state.sizeUnit+2).attr("cy",t().state.padding+t().state.sizeUnit+2)),q=(e,i)=>{let o=t().state.forkWidth,c=t().state.forkHeight;if(i.parentId){let s=o;o=c,c=s}return e.append("rect").style("stroke","black").style("fill","black").attr("width",o).attr("height",c).attr("x",t().state.padding).attr("y",t().state.padding)},Z=(e,i,o,c)=>{let s=0;const g=c.append("text");g.style("text-anchor","start"),g.attr("class","noteText");let p=e.replace(/\r\n/g,"<br/>");p=p.replace(/\n/g,"<br/>");const a=p.split(T.lineBreakRegex);let r=1.25*t().state.noteMargin;for(const y of a){const x=y.trim();if(x.length>0){const d=g.append("tspan");if(d.text(x),r===0){const l=d.node().getBBox();r+=l.height}s+=r,d.attr("x",i+t().state.noteMargin),d.attr("y",o+s+1.25*t().state.noteMargin)}}return{textWidth:g.node().getBBox().width,textHeight:s}},j=(e,i)=>{i.attr("class","state-note");const o=i.append("rect").attr("x",0).attr("y",t().state.padding),c=i.append("g"),{textWidth:s,textHeight:g}=Z(e,0,0,c);return o.attr("height",g+2*t().state.noteMargin),o.attr("width",s+t().state.noteMargin*2),o},L=function(e,i){const o=i.id,c={id:o,label:i.id,width:0,height:0},s=e.append("g").attr("id",o).attr("class","stateGroup");i.type==="start"&&O(s),i.type==="end"&&_(s),(i.type==="fork"||i.type==="join")&&q(s,i),i.type==="note"&&j(i.note.text,s),i.type==="divider"&&X(s),i.type==="default"&&i.descriptions.length===0&&J(s,i),i.type==="default"&&i.descriptions.length>0&&Y(s,i);const g=s.node().getBBox();return c.width=g.width+2*t().state.padding,c.height=g.height+2*t().state.padding,c};let G=0;const K=function(e,i,o){const c=function(r){switch(r){case N.relationType.AGGREGATION:return"aggregation";case N.relationType.EXTENSION:return"extension";case N.relationType.COMPOSITION:return"composition";case N.relationType.DEPENDENCY:return"dependency"}};i.points=i.points.filter(r=>!Number.isNaN(r.y));const s=i.points,g=$().x(function(r){return r.x}).y(function(r){return r.y}).curve(v),p=e.append("path").attr("d",g(s)).attr("id","edge"+G).attr("class","transition");let a="";if(t().state.arrowMarkerAbsolute&&(a=window.location.protocol+"//"+window.location.host+window.location.pathname+window.location.search,a=a.replace(/\(/g,"\\("),a=a.replace(/\)/g,"\\)")),p.attr("marker-end","url("+a+"#"+c(N.relationType.DEPENDENCY)+"End)"),o.title!==void 0){const r=e.append("g").attr("class","stateLabel"),{x:y,y:x}=U.calcLabelPosition(i.points),d=T.getRows(o.title);let l=0;const m=[];let w=0,E=0;for(let u=0;u<=d.length;u++){const h=r.append("text").attr("text-anchor","middle").text(d[u]).attr("x",y).attr("y",x+l),f=h.node().getBBox();w=Math.max(w,f.width),E=Math.min(E,f.x),b.info(f.x,y,x+l),l===0&&(l=h.node().getBBox().height,b.info("Title height",l,x)),m.push(h)}let k=l*d.length;if(d.length>1){const u=(d.length-1)*l*.5;m.forEach((h,f)=>h.attr("y",x+f*l-u)),k=l*d.length}const n=r.node().getBBox();r.insert("rect",":first-child").attr("class","box").attr("x",y-w/2-t().state.padding/2).attr("y",x-k/2-t().state.padding/2-3.5).attr("width",w+t().state.padding).attr("height",k+t().state.padding),b.info(n)}G++};let B;const z={},Q=function(){},V=function(e){e.append("defs").append("marker").attr("id","dependencyEnd").attr("refX",19).attr("refY",7).attr("markerWidth",20).attr("markerHeight",28).attr("orient","auto").append("path").attr("d","M 19,7 L9,13 L14,7 L9,1 Z")},D=function(e,i,o,c){B=t().state;const s=t().securityLevel;let g;s==="sandbox"&&(g=H("#i"+i));const p=s==="sandbox"?H(g.nodes()[0].contentDocument.body):H("body"),a=s==="sandbox"?g.nodes()[0].contentDocument:document;b.debug("Rendering diagram "+e);const r=p.select(`[id='${i}']`);V(r);const y=c.db.getRootDoc();A(y,r,void 0,!1,p,a,c);const x=B.padding,d=r.node().getBBox(),l=d.width+x*2,m=d.height+x*2,w=l*1.75;R(r,m,w,B.useMaxWidth),r.attr("viewBox",`${d.x-B.padding}  ${d.y-B.padding} `+l+" "+m)},tt=e=>e?e.length*B.fontSizeFactor:1,A=(e,i,o,c,s,g,p)=>{const a=new C({compound:!0,multigraph:!0});let r,y=!0;for(r=0;r<e.length;r++)if(e[r].stmt==="relation"){y=!1;break}o?a.setGraph({rankdir:"LR",multigraph:!0,compound:!0,ranker:"tight-tree",ranksep:y?1:B.edgeLengthFactor,nodeSep:y?1:50,isMultiGraph:!0}):a.setGraph({rankdir:"TB",multigraph:!0,compound:!0,ranksep:y?1:B.edgeLengthFactor,nodeSep:y?1:50,ranker:"tight-tree",isMultiGraph:!0}),a.setDefaultEdgeLabel(function(){return{}}),p.db.extract(e);const x=p.db.getStates(),d=p.db.getRelations(),l=Object.keys(x);for(const n of l){const u=x[n];o&&(u.parentId=o);let h;if(u.doc){let f=i.append("g").attr("id",u.id).attr("class","stateGroup");h=A(u.doc,f,u.id,!c,s,g,p);{f=I(f,u,c);let S=f.node().getBBox();h.width=S.width,h.height=S.height+B.padding/2,z[u.id]={y:B.compositTitleSize}}}else h=L(i,u);if(u.note){const f={descriptions:[],id:u.id+"-note",note:u.note,type:"note"},S=L(i,f);u.note.position==="left of"?(a.setNode(h.id+"-note",S),a.setNode(h.id,h)):(a.setNode(h.id,h),a.setNode(h.id+"-note",S)),a.setParent(h.id,h.id+"-group"),a.setParent(h.id+"-note",h.id+"-group")}else a.setNode(h.id,h)}b.debug("Count=",a.nodeCount(),a);let m=0;d.forEach(function(n){m++,b.debug("Setting edge",n),a.setEdge(n.id1,n.id2,{relation:n,width:tt(n.title),height:B.labelHeight*T.getRows(n.title).length,labelpos:"c"},"id"+m)}),F(a),b.debug("Graph after layout",a.nodes());const w=i.node();a.nodes().forEach(function(n){n!==void 0&&a.node(n)!==void 0?(b.warn("Node "+n+": "+JSON.stringify(a.node(n))),s.select("#"+w.id+" #"+n).attr("transform","translate("+(a.node(n).x-a.node(n).width/2)+","+(a.node(n).y+(z[n]?z[n].y:0)-a.node(n).height/2)+" )"),s.select("#"+w.id+" #"+n).attr("data-x-shift",a.node(n).x-a.node(n).width/2),g.querySelectorAll("#"+w.id+" #"+n+" .divider").forEach(h=>{const f=h.parentElement;let S=0,M=0;f&&(f.parentElement&&(S=f.parentElement.getBBox().width),M=parseInt(f.getAttribute("data-x-shift"),10),Number.isNaN(M)&&(M=0)),h.setAttribute("x1",0-M+8),h.setAttribute("x2",S-M-8)})):b.debug("No Node "+n+": "+JSON.stringify(a.node(n)))});let E=w.getBBox();a.edges().forEach(function(n){n!==void 0&&a.edge(n)!==void 0&&(b.debug("Edge "+n.v+" -> "+n.w+": "+JSON.stringify(a.edge(n))),K(i,a.edge(n),a.edge(n).relation))}),E=w.getBBox();const k={id:o||"root",label:o||"root",width:0,height:0};return k.width=E.width+2*B.padding,k.height=E.height+2*B.padding,b.debug("Doc rendered",k,a),k},et={setConf:Q,draw:D},dt={parser:P,db:N,renderer:et,styles:W,init:e=>{e.state||(e.state={}),e.state.arrowMarkerAbsolute=e.arrowMarkerAbsolute,N.clear()}};export{dt as diagram};
//# sourceMappingURL=stateDiagram-5dee940d.CUJTqsIf.js.map
