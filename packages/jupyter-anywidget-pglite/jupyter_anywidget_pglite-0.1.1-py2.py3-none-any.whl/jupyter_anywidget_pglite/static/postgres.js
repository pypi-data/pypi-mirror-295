var x=`<div class="pglite-app-container">

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
</div>`;function f(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(t){let e=Math.random()*16|0;return(t==="x"?e:e&3|8).toString(16)})}import{PGlite as g}from"https://cdn.jsdelivr.net/npm/@electric-sql/pglite/dist/index.js";var q=`
-- Optionally select statements to execute.

CREATE TABLE IF NOT EXISTS test  (
        id serial primary key,
        title varchar not null
      );

INSERT INTO test (title) values ('dummy');

`.trim();function y(t){let e=document.createElement("table"),o=e.insertRow();return t.fields.forEach(s=>{let a=document.createElement("th");a.textContent=s.name,o.appendChild(a)}),e}function h(t,e){t.rows.forEach(o=>{let s=e.insertRow();t.fields.forEach(a=>{let n=s.insertCell();n.textContent=String(o[a.name])})})}function T({model:t,el:e}){let o=t.get("idb"),s=o?new g(o):new g,a=t.get("headless");if(!a){let n=document.createElement("div");n.innerHTML=x;let d=f();n.id=d,e.appendChild(n)}t.on("change:code_content",async()=>{function n(i){let r=e.querySelector('div[title="code-editor"]');r.innerHTML=r.innerHTML+"<br>"+i}function d(i){let r=e.querySelector('div[title="output"]'),c=e.querySelector('div[title="results"]');r.innerHTML=JSON.stringify(i);let u=y(i);h(i,u),c.innerHTML="",c.append(u)}function w(i,r){a||(n(i),d(r))}let p=t.get("code_content"),m=t.get("multiline"),l={rows:[],fields:[{name:"",dataTypeID:0}]};if(m!=""){let i=p.split(m);for(let r of i){let c=r.trim();c!==""&&(n(`${c};`),l=await s.query(c),d(l))}t.set("response",l)}else n(p),l=await s.query(p),d(l),t.set("response",l);t.save_changes()})}var C={render:T};export{C as default};
