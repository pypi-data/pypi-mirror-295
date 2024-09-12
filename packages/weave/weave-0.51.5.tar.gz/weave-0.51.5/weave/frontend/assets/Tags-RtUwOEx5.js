import{l as h,b as d,R as a,C as m,s as $,W as A,r as E,L as p,_ as S}from"./index-DrgbEU4T.js";function y(e){return h.pick(e,["className","id"])}const L="text__single-line",N=e=>{const n=y(e),s=d(e.className,L),l={maxWidth:e.maxWidth?e.maxWidth:"",alignSelf:e.alignSelf?e.alignSelf:""},t=Array.isArray(e.children)?e.children.join(""):e.children,i={className:s,style:l,title:t},r=e.as||"span";return a.createElement(r,{...n,...i},e.children)},I={small:m`
    font-size: 12px;
  `,medium:m`
    font-size: 14px;
  `,large:m`
    font-size: 16px;
  `},x=$(A)`
  ${e=>I[e.size]};
  margin: 4px 4px 4px 4px;
  ${e=>e.$pos==="left"?"margin-left: -4px;":"margin-right: -4px;"}
  display: flex;
  align-items: center;
  opacity: ${e=>e.$opacity};
  ${e=>e.$cursor?`cursor: ${e.$cursor};`:""}
`;var k=(e=>(e[e.TAG=0]="TAG",e[e.ALIAS=1]="ALIAS",e[e.PROTECTED_ALIAS=2]="PROTECTED_ALIAS",e))(k||{});function z(e){switch(e){case"tag":return 0;case"alias":return 1;case"protected-alias":return 2;default:return 0}}function P(e,n){if(!e)return"tag-lightGray";switch(n){case 0:return"tag-teal-light";case 1:return"tag-sienna-light";case 2:return"tag-purple";default:return"tag-lightGray"}}const W=a.memo(({size:e,tag:n,noun:s,canDelete:l,showColor:t,onDelete:i,onClick:r})=>{const[o,u]=E.useState(!1),c=e||"large";s=s??"tag",l=l??!0,t=t??!0;const f=P(t,z(s));return a.createElement(p,{style:{marginLeft:"2px",maxWidth:"220px"},className:o?`run-tag ${c} tag-red-alert`:`run-tag ${c} ${f}`,key:n.name,onClick:r},a.createElement(x,{name:s==="tag"?"tag-latest":"email-at",size:c,$pos:"left"}),a.createElement(N,{alignSelf:"center"},n.name),l&&i&&a.createElement(x,{className:"delete-tag",name:"close-latest",size:c,onClick:g=>{g.stopPropagation(),i(g)},onMouseOver:()=>u(!0),onMouseOut:()=>u(!1),$pos:"right",$opacity:.6,$cursor:"pointer"}))});a.memo(({size:e,tags:n,enableDelete:s,noun:l,deleteTag:t,onClick:i})=>a.createElement("span",{className:"run-tags"},S.sortBy(n,"name").map(r=>a.createElement(W,{key:r.name,tag:r,size:e,onDelete:s&&t?o=>{t&&(o.stopPropagation(),t(r))}:void 0,onClick:()=>i?.(r.name),noun:l}))));export{W as T,k as a};
//# sourceMappingURL=Tags-RtUwOEx5.js.map
