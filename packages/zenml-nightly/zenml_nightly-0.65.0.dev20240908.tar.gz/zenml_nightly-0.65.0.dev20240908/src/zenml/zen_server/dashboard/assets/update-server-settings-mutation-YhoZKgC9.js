import{j as n,F as i,k as o,l as u}from"./index-Davdjm1d.js";import{b as c}from"./@tanstack-QbMbTrh5.js";async function p(e){const r=o(u.settings),t=await n(r,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)});if(!t.ok){const a=await t.json().then(s=>Array.isArray(s.detail)?s.detail[1]:s.detail).catch(()=>"Failed to update Server Settings");throw new i({status:t.status,statusText:t.statusText,message:a})}return t.json()}function f(e){return c({mutationFn:async r=>p(r),...e})}export{f as u};
