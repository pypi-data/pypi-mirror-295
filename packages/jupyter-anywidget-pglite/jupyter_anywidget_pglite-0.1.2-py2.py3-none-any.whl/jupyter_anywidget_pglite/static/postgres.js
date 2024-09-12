var m=`<div class="pglite-app-container">

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
</div>`;function f(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(e){let n=Math.random()*16|0;return(e==="x"?n:n&3|8).toString(16)})}import{PGlite as g}from"https://cdn.jsdelivr.net/npm/@electric-sql/pglite/dist/index.js";var q=`
-- Optionally select statements to execute.

CREATE TABLE IF NOT EXISTS test  (
        id serial primary key,
        title varchar not null
      );

INSERT INTO test (title) values ('dummy');

`.trim();function h(e){let n=document.createElement("table"),o=n.insertRow();return e.fields.forEach(s=>{let a=document.createElement("th");a.textContent=s.name,o.appendChild(a)}),n}function T(e,n){e.rows.forEach(o=>{let s=n.insertRow();e.fields.forEach(a=>{let i=s.insertCell();i.textContent=String(o[a.name])})})}function w({model:e,el:n}){let o=e.get("idb"),s=o?new g(o):new g,a=e.get("headless");if(!a){let i=document.createElement("div");i.innerHTML=m;let l=f();i.id=l,n.appendChild(i)}e.on("change:code_content",async()=>{function i(t){let r=n.querySelector('div[title="code-editor"]');r.innerHTML=r.innerHTML+"<br>"+t}function l(t){let r=n.querySelector('div[title="output"]'),c=n.querySelector('div[title="results"]');r.innerHTML=JSON.stringify(t);let x=h(t);T(t,x),c.innerHTML="",c.append(x)}function E(t,r){a||(i(t),l(r))}let d=e.get("code_content"),u=e.get("multiline"),y=e.get("multiexec"),p={rows:[],fields:[{name:"",dataTypeID:0}]};if(y){i(d);let t=await s.exec(d);l(t[t.length-1]),e.set("response",{response:t,response_type:"multi"})}else if(u!=""){let t=d.split(u);for(let r of t){let c=r.trim();c!==""&&(i(`${c};`),p=await s.query(c),l(p))}e.set("response",{response:p,response_type:"single"})}else i(d),p=await s.query(d),l(p),e.set("response",{response:p,response_type:"single"});e.save_changes()})}var C={render:w};export{C as default};
