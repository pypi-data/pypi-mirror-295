const d=(o,a={})=>{const l=a.with_line_breaks||"no";let[f,p]=o.toString().split(".");const c=i=>{let e="",r=i.length;for(let t=r-1;t>=0;t--){let n=r-t;e=i[t]+e,l==="yes"?l==="yes"&&n%25===0&&t!==0?e=`
`+e:n%5===0&&t!==0&&(e=" "+e):n%5===0&&t!==0&&(e=","+e)}return e},g=i=>{if(!i)return"";let e="";i.length;for(let r=0;r<=i.length-1;r++){let t=r+1;e=e+i[r],t%5===0&&r!==0&&(e=e+",")}return e};let s=c(f),_=g(p);return _===""?s:`${s}.${_}`};export{d as p};
//# sourceMappingURL=parse_with_commas.BiYKGtV3.js.map
