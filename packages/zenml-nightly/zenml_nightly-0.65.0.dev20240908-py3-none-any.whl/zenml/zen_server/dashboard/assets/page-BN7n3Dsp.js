import{j as e}from"./@radix-DnFH_oo1.js";import{B as r,P as o,E as i}from"./index-Davdjm1d.js";import{C as n}from"./CodeSnippet-i_WEOWw9.js";import{I as c}from"./Infobox-BB7dfbrO.js";import{c as l}from"./@react-router-APVeuk-U.js";import{C as m,a as f}from"./cloud-only-DrdxC8NV.js";import"./@tanstack-QbMbTrh5.js";import"./@reactflow-IuMOnBUC.js";import"./copy-CaGlDsUy.js";function x(){return e.jsx(c,{children:e.jsxs("div",{className:"flex w-full flex-wrap items-center gap-x-2 gap-y-0.5 text-text-md",children:[e.jsx("p",{className:"font-semibold",children:"This is a ZenML Pro feature. "}),e.jsx("p",{children:"Upgrade to ZenML Pro to access the Artifact Control Plane and interact with your artifacts in the Dashboard."})]})})}function d(){const[s]=l(),t=s.get("artifact");function a(){return t?`zenml artifact list --name='contains:${t}'`:"zenml artifact list"}return e.jsxs(r,{className:"flex flex-wrap justify-between p-5",children:[e.jsxs("div",{children:[e.jsx("p",{className:"text-text-xl font-semibold",children:"Staying Open Source? "}),e.jsx("p",{className:"text-theme-text-secondary",children:"No problem! Use this CLI command to list your artifacts"})]}),e.jsx(n,{code:a()})]})}const p="/assets/acp-DOsXjFc7.webp";function w(){return e.jsxs("div",{children:[e.jsxs(o,{className:"flex items-center gap-1",children:[e.jsx("h1",{className:"text-display-xs font-semibold",children:"Artifacts"}),e.jsx(i,{color:"purple",rounded:!0,size:"sm",children:e.jsx("span",{className:"font-semibold text-primary-500",children:"Pro"})})]}),e.jsxs("div",{className:"layout-container space-y-5 py-5",children:[e.jsx(x,{}),e.jsx(m,{feature:"artifact",image:{src:p,alt:"Screenshot of the ZenML Pro Artifact Control plane"},features:f}),e.jsx(d,{})]})]})}export{w as default};
