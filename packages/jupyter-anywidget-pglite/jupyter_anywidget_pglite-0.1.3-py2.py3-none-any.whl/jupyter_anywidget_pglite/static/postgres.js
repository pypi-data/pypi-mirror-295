var v=`<div class="pglite-app-container">

    <h1><tt>pglite</tt></h1>

    <div>Executed commands:</div>
    <div class="code-editor" title="code-editor"></div>
    <div id="pglite-timestamp"></div>
    <hr>
    <div>Result:</div>
    <div title="results"></div>
    <hr>
    <div>Raw Output:</div>
    <div title="output"></div>
</div>`;function b(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(e){let t=Math.random()*16|0;return(e==="x"?t:t&3|8).toString(16)})}import{PGlite as w}from"https://cdn.jsdelivr.net/npm/@electric-sql/pglite/dist/index.js";var U=`
-- Optionally select statements to execute.

CREATE TABLE IF NOT EXISTS test  (
        id serial primary key,
        title varchar not null
      );

INSERT INTO test (title) values ('dummy');

`.trim();function T(e){let t=document.createElement("table"),a=t.insertRow();return e.fields.forEach(r=>{let s=document.createElement("th");s.textContent=r.name,a.appendChild(s)}),t}function E(e,t){e.rows.forEach(a=>{let r=t.insertRow();e.fields.forEach(s=>{let p=r.insertCell();p.textContent=String(a[s.name])})})}function R(e){if(e&&e.file_content&&e.file_info){let{file_content:t,file_info:a}=e,r=atob(t),s=new Array(r.length);for(let n=0;n<r.length;n++)s[n]=r.charCodeAt(n);let p=new Uint8Array(s),u=new Blob([p],{type:a.type});return new File([u],a.name,{type:a.type,lastModified:a.lastModified})}return null}function D({model:e,el:t}){let a=e.get("idb"),r=e.get("file_package"),s=R(r),p={};s&&(p.loadDataDir=s);let u=a?new w(a,p):new w(p),x=e.get("headless");if(!x){let n=document.createElement("div");n.innerHTML=v;let o=b();n.id=o,t.appendChild(n)}e.on("change:datadump",async()=>{if(e.get("datadump")=="generate_dump"){let o=await u.dumpDataDir(),g=new FileReader;g.onload=d=>{let m={name:o.name,size:o.size,type:o.type,lastModified:o.lastModified},y=d.target.result.split(",")[1],l={file_info:m,file_content:y};e.set("file_package",l),e.save_changes()},g.readAsDataURL(o)}}),e.on("change:code_content",async()=>{function n(i){let c=t.querySelector('div[title="code-editor"]');c.innerHTML=c.innerHTML+"<br>"+i}function o(i){let c=t.querySelector('div[title="output"]'),f=t.querySelector('div[title="results"]');c.innerHTML=JSON.stringify(i);let h=T(i);E(i,h),f.innerHTML="",f.append(h)}function g(i,c){x||(n(i),o(c))}let d=e.get("code_content"),m=e.get("multiline"),y=e.get("multiexec"),l={rows:[],fields:[{name:"",dataTypeID:0}]};if(y){n(d);let i=await u.exec(d);o(i[i.length-1]),e.set("response",{response:i,response_type:"multi"})}else if(m!=""){let i=d.split(m);for(let c of i){let f=c.trim();f!==""&&(n(`${f};`),l=await u.query(f),o(l))}e.set("response",{response:l,response_type:"single"})}else n(d),l=await u.query(d),o(l),e.set("response",{response:l,response_type:"single"});e.save_changes()})}var O={render:D};export{O as default};
