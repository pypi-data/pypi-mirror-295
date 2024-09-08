import{r as c,j as e}from"./@radix-DnFH_oo1.js";import{a2 as A,a3 as E,a4 as R,F as M,k as U,l as W,f as q,r as N,i as Q,aa as Y,ab as G,ac as K,ad as J,h as x,af as S,ag as V,ah as X,C as Z,a0 as ee,a1 as se,R as P,av as b,aw as C,M as te,N as ae,O as re,S as u,A as I,b as z,B as ne,z as g,D as ie,o as ce,ax as le,P as oe}from"./index-Davdjm1d.js";import{S as de}from"./plus-Bc8eLSDM.js";import{R as me}from"./refresh-CtPKdk2G.js";import{S as xe,P as ue}from"./SearchField-BPNazO4G.js";import{s as h}from"./sharedSchema-Dbpe2oAO.js";import{b as he,c as pe,a as f}from"./@tanstack-QbMbTrh5.js";import{b as fe,L as k,c as je}from"./@react-router-APVeuk-U.js";import{C as v}from"./CopyButton-BAYaQlWF.js";import{D as ge}from"./DisplayDate-DkCy54Bp.js";import{I as Ne}from"./InlineAvatar-C2ZECnGP.js";import{S as ye}from"./dots-horizontal-C6K59vUm.js";import{D as we,S as be}from"./DialogItem-B576Svvy.js";import{S as ke}from"./trash-DUWZWzse.js";import{I as y}from"./Infobox-BB7dfbrO.js";import{C as p}from"./CodeSnippet-i_WEOWw9.js";import{A as ve}from"./AlertDialogDropdownItem-CO2rOw5M.js";import{C as Se}from"./CollapsibleCard-C9BzoY6q.js";import{F as Ce}from"./chevron-right-double-c9H46Kl8.js";import{e as D}from"./components-Br2ezRib.js";import{s as De}from"./url-DNHuFfYx.js";import{N as T}from"./NumberBox-CrN0_kqI.js";import{C as Te,p as F,c as Ae}from"./persist-g4uRK-v-.js";import{p as O,c as Ee}from"./persist-CnMMI8ls.js";import"./@reactflow-IuMOnBUC.js";import"./index-5GJ5ysEZ.js";import"./stack-detail-query-fuuoot1D.js";import"./layout-Dru15_XR.js";import"./rocket-SESCGQXm.js";import"./copy-CaGlDsUy.js";import"./chevron-down-Cwb-W_B_.js";const $=c.forwardRef(({closeModal:s,name:t,...a},r)=>e.jsxs(A,{...a,ref:r,children:[e.jsx(E,{children:e.jsx(R,{children:"Update Stack"})}),e.jsxs("div",{className:"space-y-5 p-7",children:[e.jsx(Re,{action:"update"}),e.jsxs("div",{className:"space-y-1",children:[e.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:"Update a stack"}),e.jsx(p,{codeClasses:"whitespace-pre-wrap",wrap:!0,code:`zenml stack update ${t} -o NEW_ORCHESTRATOR_NAME`})]})]})]}));$.displayName="UpdateStackDialog";function Re({action:s}){function t(){switch(s){case"delete":return"delete";case"update":return"update";case"describe":return"get details of"}}return e.jsx(y,{children:e.jsx("div",{className:"flex w-full flex-wrap justify-between gap-2",children:e.jsxs("div",{className:"min-w-0",children:[e.jsx("p",{className:"truncate text-text-sm font-semibold",children:"We are working on the new Stacks experience."}),e.jsxs("p",{className:"truncate text-text-sm",children:["Meanwhile you can use the CLI to ",t()," your stack."]})]})})})}async function Pe({stackId:s},t){const a=U(W.stacks.detail(s)),r=await fetch(a,{method:"DELETE",credentials:"include",headers:{"Content-Type":"application/json",...t?{Authorization:`Bearer ${t}`}:{}}});if(!r.ok){const n=await r.json().then(i=>Array.isArray(i.detail)?i.detail[1]:i.detail).catch(()=>`Error while deleting stack ${s}`);throw new M({status:r.status,statusText:r.statusText,message:n})}return r.json()}function Ie(s){return he({...s,mutationFn:async({stackId:t})=>Pe({stackId:t})})}function ze(s){const{toast:t}=q(),a=pe(),r=fe(),n=Ie({onSuccess:async()=>{a.invalidateQueries({queryKey:h.all}),r(N.stacks.overview)},onError:l=>{t({status:"error",emphasis:"subtle",icon:e.jsx(Q,{className:"h-5 w-5 shrink-0 fill-error-700"}),description:l.message,rounded:!0})}});function i(){n.mutate({stackId:s})}return{handleDelete:i,deleteStack:n}}const B=c.forwardRef(({closeModal:s,name:t,stackId:a,...r},n)=>{const{handleDelete:i,deleteStack:l}=ze(a);return e.jsxs(Y,{...r,className:"p-0",ref:n,children:[e.jsxs(G,{className:"m-0 py-2 pl-5 pr-3 text-text-lg font-semibold",children:["Delete ",t]}),e.jsx("div",{className:"border-y border-theme-border-moderate px-5 py-5",children:e.jsxs(K,{children:["Are you sure you want to delete this stack? ",e.jsx("br",{}),"This action cannot be undone."]})}),e.jsxs("div",{className:"flex justify-end gap-3 px-5 py-3",children:[e.jsx(J,{onClick:()=>s==null?void 0:s(),asChild:!0,children:e.jsx(x,{intent:"secondary",children:"Cancel"})}),e.jsxs(x,{disabled:l.isPending,type:"button",onClick:()=>i(),intent:"danger",children:[l.isPending&&e.jsx("div",{role:"alert","aria-busy":"true",className:"full h-[20px] w-[20px] animate-spin rounded-rounded border-2 border-theme-text-negative border-b-theme-text-error"}),"Delete"]})]})]})});B.displayName="DeleteStackDialog";function Fe({name:s,id:t}){const[a,r]=c.useState(!1),[n,i]=c.useState(!1),l=c.useRef(null),d=c.useRef(null);function o(){d.current=l.current}function m(j){r(j),j===!1&&i(!1)}return e.jsx(S,{open:n,onOpenChange:i,children:e.jsxs(S,{children:[e.jsx(V,{className:"z-10",ref:l,children:e.jsx(ye,{className:"h-5 w-5 fill-theme-text-secondary"})}),e.jsxs(X,{hidden:a,onCloseAutoFocus:j=>{d.current&&(d.current.focus(),d.current=null,j.preventDefault())},className:"z-10",align:"end",sideOffset:1,children:[e.jsx(we,{onSelect:o,onOpenChange:m,icon:e.jsx(be,{className:"h-3 w-3 !fill-neutral-400"}),triggerChildren:"Update",children:e.jsx($,{name:s,className:"lg:min-w-[600px]",closeModal:()=>m(!1)})}),e.jsx(ve,{onSelect:o,onOpenChange:m,icon:e.jsx(ke,{className:"h-3  w-3 !fill-neutral-400"}),triggerChildren:"Delete",children:e.jsx(B,{stackId:t,name:s,className:"lg:min-w-[600px]",closeModal:()=>m(!1)})})]})]})})}function Oe(){return e.jsx("div",{className:"flex h-9 items-center border-b border-theme-border-moderate bg-theme-surface-primary px-4 py-3",children:e.jsxs(Z,{className:"focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none",children:[e.jsx(Ce,{className:"h-5 w-5 fill-neutral-500"}),e.jsx("span",{className:"sr-only",children:"Close"})]})})}const L=c.forwardRef(({name:s,children:t,type:a,...r},n)=>e.jsxs(ee,{children:[e.jsx(se,{asChild:!0,children:t}),e.jsxs(A,{className:"w-fit max-w-fit",...r,ref:n,children:[e.jsx(E,{children:e.jsx(R,{children:P(a||"")})}),e.jsxs("div",{className:"space-y-5 p-7",children:[e.jsx($e,{type:a}),e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"text-text-sm text-theme-text-secondary",children:["Describe your ",b(a)]}),e.jsx(p,{codeClasses:"whitespace-pre-wrap",wrap:!0,code:`zenml ${C(a)} describe ${s}`})]}),e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"text-text-sm text-theme-text-secondary",children:["Update your ",b(a)]}),e.jsx(p,{codeClasses:"whitespace-pre-wrap",wrap:!0,code:`zenml ${C(a)} update ${s}`})]})]})]})]}));L.displayName="ComponentFallbackDialog";function $e({type:s}){return e.jsx(y,{children:e.jsx("div",{className:"flex w-full flex-wrap justify-between gap-2",children:e.jsxs("div",{className:"min-w-0",children:[e.jsx("p",{className:"truncate text-text-sm font-semibold",children:"We are working on the new Stacks experience."}),e.jsxs("p",{className:"truncate text-text-sm",children:["Meanwhile you can use the CLI to manage your ",b(s),"."]})]})})})}const _=c.createContext(null);function Be({children:s}){const[t,a]=c.useState([]);return e.jsx(_.Provider,{value:{integrations:t,setIntegrations:a},children:s})}function H(){const s=c.useContext(_);if(s===null)throw new Error("useIntegrationsContext must be used within an AuthProvider");return s}function Le({children:s,stackId:t,stackName:a}){return e.jsxs(te,{children:[e.jsx(ae,{children:s}),e.jsx(re,{className:"w-[1000px] overflow-y-auto",children:e.jsxs(Be,{children:[e.jsx(Oe,{}),e.jsx(_e,{stackId:t}),e.jsx(Ue,{name:a}),e.jsx(He,{stackId:t})]})})]})}function _e({stackId:s}){const t=f({...h.stackDetail(s)});return t.isError?null:t.isPending?e.jsx("div",{className:"p-5",children:e.jsx(u,{className:"h-6 w-full"})}):e.jsxs("div",{className:"flex items-center space-x-2 border-b border-theme-border-moderate bg-theme-surface-primary p-5",children:[e.jsx(I,{type:"square",size:"lg",children:e.jsx(z,{size:"lg",children:t.data.name[0]})}),e.jsxs("div",{children:[e.jsxs("div",{className:"group/copybutton flex items-center gap-0.5",children:[e.jsx("p",{className:"mb-0.5 text-text-sm text-theme-text-secondary",children:t.data.id}),e.jsx(v,{copyText:t.data.id})]}),e.jsx("div",{className:"flex items-center gap-1",children:e.jsx("h2",{className:"text-display-xs font-semibold",children:t.data.name})})]})]})}function He({stackId:s}){var n;const{setIntegrations:t}=H(),a=f({...h.stackDetail(s)});if(c.useEffect(()=>{var d;if(!a.data)return;const l=D((d=a.data.metadata)==null?void 0:d.components).map(o=>{var m;return(m=o.body)==null?void 0:m.integration}).filter(o=>!!o&&o!=="built-in"&&o!=="custom");l.length>=1&&t(o=>Array.from(new Set([...o,...l])))},[a.data]),a.isError)return null;if(a.isPending)return e.jsx("div",{className:"p-5",children:e.jsx(u,{className:"h-[300px] w-full"})});const r=D((n=a.data.metadata)==null?void 0:n.components);return e.jsx("ul",{className:"space-y-5 p-5",children:r.map(i=>e.jsx("li",{children:e.jsx(Me,{component:i})},i.id))})}function Me({component:s}){var t,a,r,n,i;return e.jsxs(ne,{className:"flex items-center justify-between p-5",children:[e.jsxs("div",{className:"flex items-center space-x-3",children:[e.jsx("img",{width:32,height:32,alt:`${(t=s.body)==null?void 0:t.flavor} logo`,src:De(((a=s.body)==null?void 0:a.logo_url)||"")}),e.jsxs("div",{children:[e.jsx(L,{type:((r=s.body)==null?void 0:r.type)||"orchestrator",name:s.name,children:e.jsx("button",{className:"text-text-xl",children:s.name})}),e.jsxs("div",{className:"group/copybutton flex items-center gap-0.5",children:[e.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:s.id.split("-")[0]}),e.jsx(v,{copyText:s.id})]})]})]}),e.jsx(Te,{type:((n=s.body)==null?void 0:n.type)||"orchestrator",children:P(((i=s.body)==null?void 0:i.type)||"")})]})}function Ue({name:s}){const{integrations:t}=H();return e.jsx("section",{className:"px-5 pt-5",children:e.jsx(Se,{title:e.jsx("span",{className:"text-text-lg",children:"Set this stack"}),children:e.jsxs("ul",{className:"space-y-5",children:[e.jsxs("li",{className:"space-y-2",children:[e.jsxs("div",{className:"flex items-center gap-2",children:[e.jsx(T,{children:"1"}),e.jsx("p",{className:"font-semibold",children:"Set your stack"})]}),e.jsxs("div",{className:"space-y-1",children:[e.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:"Set the stack as active on your client"}),e.jsx(p,{codeClasses:"whitespace-pre-wrap",wrap:!0,code:`zenml stack set ${s}`})]})]}),t.length>=1&&e.jsxs("li",{className:"space-y-2",children:[e.jsxs("div",{className:"flex items-center gap-2",children:[e.jsx(T,{children:"2"}),e.jsx("p",{className:"font-semibold",children:"Install the integrations"})]}),e.jsxs("div",{className:"space-y-1",children:[e.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:"Install the required integrations to run pipelines in your stack"}),e.jsx(p,{codeClasses:"whitespace-pre-wrap",wrap:!0,code:`zenml integration install ${t.join(" ")}`})]})]})]})})})}function We(){return[{id:"name",header:"Stack",accessorFn:s=>({name:s.name,id:s.id}),cell:({getValue:s})=>{const{name:t,id:a}=s();return e.jsxs("div",{className:"group/copybutton flex items-center gap-2",children:[e.jsx(I,{type:"square",size:"md",children:e.jsx(z,{size:"md",children:t[0]})}),e.jsxs("div",{children:[e.jsx("div",{className:"flex items-center gap-1",children:e.jsx(Le,{stackName:t,stackId:a,children:e.jsx("h2",{className:"text-text-md font-semibold",children:t})})}),e.jsxs("div",{className:"flex items-center gap-1",children:[e.jsx("p",{className:"text-text-xs text-theme-text-secondary",children:a.split("-")[0]}),e.jsx(v,{copyText:a})]})]})]})}},{id:"created",header:"Created at",accessorFn:s=>{var t;return(t=s.body)==null?void 0:t.created},cell:({getValue:s})=>e.jsx("p",{className:"text-text-sm text-theme-text-secondary",children:e.jsx(ge,{dateString:s()})})},{id:"author",header:"Author",accessorFn:s=>{var t;return{author:(t=s.body)==null?void 0:t.user}},cell:({getValue:s})=>{const{author:t}=s();return t?e.jsx(Ne,{username:t.name}):null}},{id:"actions",header:"",accessorFn:s=>({name:s.name,id:s.id}),cell:({getValue:s})=>{const{id:t,name:a}=s();return e.jsx(Fe,{name:a,id:t})}}]}function qe({setHasResumeableStack:s}){const{success:t,data:a}=F(),r=f({...h.stackDeploymentStack({provider:(a==null?void 0:a.provider)||"aws",stack_name:(a==null?void 0:a.stackName)||"",date_start:a==null?void 0:a.timestamp}),enabled:t,throwOnError:!0});return c.useEffect(()=>{r.data&&(Ae(),s(!1))},[r.data]),!t||r.isError?null:r.isPending?e.jsx(u,{className:"h-[70px] w-full"}):e.jsx(y,{className:"w-full",children:e.jsxs("section",{className:"flex flex-wrap items-center justify-between gap-y-2",children:[e.jsxs("div",{className:"flex flex-wrap items-center gap-2",children:[e.jsx("p",{className:"font-semibold",children:"You have a Stack provision incomplete"}),e.jsx("p",{className:"text-text-sm",children:"Return to the setup and finish the configuration on your cloud provider"})]}),e.jsx("div",{children:e.jsx(x,{className:"w-fit bg-theme-surface-primary",intent:"primary",emphasis:"subtle",asChild:!0,children:e.jsx(k,{to:N.stacks.create.newInfra,children:e.jsx("span",{children:"Review Stack"})})})})]})})}const w=1,Qe=g.object({page:g.coerce.number().min(w).optional().default(w).catch(w),name:g.string().optional(),operator:g.enum(["and","or"]).optional()});function Ye(){const[s]=je(),{page:t,name:a,operator:r}=Qe.parse({page:s.get("page")||void 0,name:s.get("name")||void 0});return{page:t,name:a,logical_operator:r}}function Ge({setHasResumeableTerraform:s}){const{success:t,data:a}=O(),r=f({...h.stackDeploymentStack({provider:(a==null?void 0:a.provider)||"aws",stack_name:(a==null?void 0:a.stackName)||"",date_start:a==null?void 0:a.timestamp}),enabled:t,throwOnError:!0});return c.useEffect(()=>{r.data&&(Ee(),s(!1))},[r.data]),!t||r.isError?null:r.isPending?e.jsx(u,{className:"h-[70px] w-full"}):e.jsx(y,{className:"w-full",children:e.jsxs("section",{className:"flex flex-wrap items-center justify-between gap-y-2",children:[e.jsxs("div",{className:"flex flex-wrap items-center gap-2",children:[e.jsx("p",{className:"font-semibold",children:"You have a Terraform Stack provision incomplete"}),e.jsx("p",{className:"text-text-sm",children:"Return to the setup and finish the configuration on your cloud provider"})]}),e.jsx("div",{children:e.jsx(x,{className:"w-fit bg-theme-surface-primary",intent:"primary",emphasis:"subtle",asChild:!0,children:e.jsx(k,{to:N.stacks.create.terraform,children:e.jsx("span",{children:"Review Stack"})})})})]})})}function Ke(){const[s,t]=c.useState(F().success),[a,r]=c.useState(O().success),n=Ye(),{refetch:i,data:l}=f({...h.stackList({...n,sort_by:"desc:updated"}),throwOnError:!0});return e.jsx("section",{className:"p-5",children:e.jsxs("div",{className:"flex flex-col gap-5",children:[e.jsxs("div",{className:"flex flex-wrap items-center justify-between gap-y-4",children:[e.jsx(xe,{searchParams:n}),e.jsxs("div",{className:"flex items-center justify-between gap-2",children:[e.jsxs(x,{intent:"primary",emphasis:"subtle",size:"md",onClick:()=>i(),children:[e.jsx(me,{className:"h-5 w-5 fill-theme-text-brand"}),"Refresh"]}),e.jsx(x,{size:"md",asChild:!0,children:e.jsxs(k,{to:N.stacks.create.index,children:[e.jsx(de,{className:"h-5 w-5 shrink-0 fill-white"}),e.jsx("span",{children:"New Stack"})]})})]})]}),e.jsxs("div",{className:"flex flex-col items-center gap-5",children:[s&&e.jsx(qe,{setHasResumeableStack:t}),a&&e.jsx(Ge,{setHasResumeableTerraform:r}),e.jsx("div",{className:"w-full",children:l?e.jsx(ie,{columns:We(),data:l.items}):e.jsx(u,{className:"h-[500px] w-full"})}),l?l.total_pages>1&&e.jsx(ue,{searchParams:n,paginate:l}):e.jsx(u,{className:"h-[36px] w-[300px]"})]})]})})}function Ts(){const{setCurrentBreadcrumbData:s}=ce(),{setTourState:t,tourState:{tourActive:a}}=le();return c.useEffect(()=>{a&&t(r=>({...r,run:!0,stepIndex:r.stepIndex}))},[a]),c.useEffect(()=>{s({segment:"stacks",data:null})},[]),e.jsxs("div",{children:[e.jsx(Je,{}),e.jsx(Ke,{})]})}function Je(){return e.jsx(oe,{children:e.jsx("h1",{className:"text-display-xs font-semibold",children:"Stacks"})})}export{Ts as default};
