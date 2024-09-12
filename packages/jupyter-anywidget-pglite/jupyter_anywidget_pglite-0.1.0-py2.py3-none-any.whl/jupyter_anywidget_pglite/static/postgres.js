var c=`<div class="pglite-app-container">

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
</div>`;function p(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(t){let e=Math.random()*16|0;return(t==="x"?e:e&3|8).toString(16)})}import{PGlite as x}from"https://cdn.jsdelivr.net/npm/@electric-sql/pglite/dist/index.js";var R=`
-- Optionally select statements to execute.

CREATE TABLE IF NOT EXISTS test  (
        id serial primary key,
        title varchar not null
      );

INSERT INTO test (title) values ('dummy');

`.trim();function g(t){let e=document.createElement("table"),n=e.insertRow();return t.fields.forEach(a=>{let i=document.createElement("th");i.textContent=a.name,n.appendChild(i)}),e}function f(t,e){t.rows.forEach(n=>{let a=e.insertRow();t.fields.forEach(i=>{let r=a.insertCell();r.textContent=String(n[i.name])})})}function v({model:t,el:e}){let n=t.get("idb"),a=n?new x(n):new x,i=t.get("headless");if(!i){let r=document.createElement("div");r.innerHTML=c;let o=p();r.id=o,e.appendChild(r)}t.on("change:code_content",async()=>{let r=t.get("code_content"),o=await a.query(r);if(t.set("response",o),!i){let s=e.querySelector('div[title="code-editor"]'),m=e.querySelector('div[title="output"]'),d=e.querySelector('div[title="results"]');s.innerHTML=s.innerHTML+"<br>"+t.get("code_content"),m.innerHTML=JSON.stringify(o);let l=g(o);f(o,l),d.innerHTML="",d.append(l)}t.save_changes()})}var S={render:v};export{S as default};
