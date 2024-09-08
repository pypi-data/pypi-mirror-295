import{j as e,r}from"./@radix-DnFH_oo1.js";import{B as a,ax as n,P as l,E as i}from"./index-Davdjm1d.js";import{C as m}from"./CodeSnippet-i_WEOWw9.js";import{I as c}from"./Infobox-BB7dfbrO.js";import{c as d}from"./@react-router-APVeuk-U.js";import{C as x,m as p}from"./cloud-only-DrdxC8NV.js";import"./@tanstack-QbMbTrh5.js";import"./@reactflow-IuMOnBUC.js";import"./copy-CaGlDsUy.js";function u(){return e.jsx(c,{children:e.jsxs("div",{className:"flex w-full flex-wrap items-center gap-x-2 gap-y-0.5 text-text-md",children:[e.jsx("p",{className:"font-semibold",children:"This is a ZenML Pro feature. "}),e.jsx("p",{children:"Upgrade to ZenML Pro to access the Model Control Plane and interact with your models in the Dashboard."})]})})}function f(){const[o]=d(),s=o.get("model");function t(){return s?`zenml model list --name='contains:${s}'`:"zenml model list"}return e.jsxs(a,{className:"flex flex-wrap justify-between p-5",children:[e.jsxs("div",{children:[e.jsx("p",{className:"text-text-xl font-semibold",children:"Staying Open Source? "}),e.jsx("p",{className:"text-theme-text-secondary",children:"No problem! Use this CLI command to list your models"})]}),e.jsx(m,{code:t()})]})}const h="/assets/mcp-Cb1aMeoq.webp";function w(){const{setTourState:o,tourState:{tourActive:s}}=n();return r.useEffect(()=>{s&&o(t=>({...t,run:!0,stepIndex:t.stepIndex}))},[s]),e.jsxs("div",{children:[e.jsxs(l,{className:"flex items-center gap-1",children:[e.jsx("h1",{className:"text-display-xs font-semibold",children:"Models"}),e.jsx(i,{color:"purple",rounded:!0,size:"sm",children:e.jsx("span",{className:"font-semibold text-primary-500",children:"Pro"})})]}),e.jsxs("div",{className:"layout-container space-y-5 py-5",children:[e.jsx(u,{}),e.jsx(x,{feature:"model",image:{src:h,alt:"Screenshot of the ZenML Pro Model Control plane"},features:p}),e.jsx(f,{})]})]})}export{w as default};
