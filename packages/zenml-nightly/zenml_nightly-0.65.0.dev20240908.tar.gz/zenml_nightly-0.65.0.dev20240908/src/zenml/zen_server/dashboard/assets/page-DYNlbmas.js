import{r as f,j as e}from"./@radix-DnFH_oo1.js";import{S as X,u as y,C as v,P as N,a as $,W as ee,L as te}from"./ProviderRadio-DkPE6alG.js";import{u,R as se,a as re,E as ae,D as A,G as ne,A as oe,C as O,b as ie,N as ce}from"./Partials-RDhJ8Ci7.js";import{S as V,B as Y,aF as de,h as le,r as T}from"./index-Davdjm1d.js";import{c as me,b as ue}from"./@react-router-APVeuk-U.js";import{I as G}from"./Infobox-BB7dfbrO.js";import{t as H}from"./zod-uFd1wBcd.js";import{u as Q,F as pe}from"./index.esm-BE1uqCX5.js";import{a as xe,c as q,b as fe,p as he}from"./persist-g4uRK-v-.js";import{C as h}from"./ProviderIcon-wA4qBOv1.js";import{s as J}from"./sharedSchema-Dbpe2oAO.js";import{a as K}from"./@tanstack-QbMbTrh5.js";import"./Tick-DEACFydX.js";import"./package-DYKZ5jKW.js";import"./logs-GiDJXbLS.js";import"./CodeSnippet-i_WEOWw9.js";import"./copy-CaGlDsUy.js";import"./NumberBox-CrN0_kqI.js";import"./@reactflow-IuMOnBUC.js";import"./gcp-Dj6ntk0L.js";import"./url-DNHuFfYx.js";import"./stack-detail-query-fuuoot1D.js";import"./layout-Dru15_XR.js";import"./rocket-SESCGQXm.js";function je(){const{formRef:t,setIsNextButtonDisabled:s,setData:a,data:n}=u(),o=Q({resolver:H(xe),mode:"onChange",defaultValues:{region:n.location,stackName:n.stackName||""}});f.useEffect(()=>{s(!o.formState.isValid)},[o.formState.isValid,s]);function l(r){a(m=>({...m,location:r.region,stackName:r.stackName}))}return e.jsx(j,{title:"Review Stack Configuration",children:e.jsx(pe,{...o,children:e.jsxs("div",{className:"space-y-5",children:[e.jsxs(G,{className:"text-text-sm",children:[e.jsx("p",{className:"font-semibold",children:"Important"}),e.jsx("p",{children:"This will create new resources in your account. Ensure you have the necessary permissions and are aware of any potential costs."})]}),e.jsxs("form",{onSubmit:o.handleSubmit(l),ref:t,className:"space-y-5",children:[e.jsx(se,{provider:n.provider||"aws"}),e.jsx(X,{})]}),e.jsx(re,{provider:n.provider||"aws"}),e.jsx(ae,{provider:n.provider||"aws"})]})})})}function ve(){const{data:t,timestamp:s,setIsNextButtonDisabled:a}=u(),{setCurrentStep:n}=y(),{isPending:o,isError:l,data:r}=K({...J.stackDeploymentStack({provider:t.provider,stack_name:t.stackName,date_start:s}),refetchInterval:5e3,throwOnError:!0});return f.useEffect(()=>{r&&(q(),n(m=>m+1),a(!1))},[r]),o?e.jsx(V,{className:"h-[200px] w-full"}):l?null:e.jsxs("div",{className:"space-y-5",children:[e.jsx(Ne,{}),e.jsx(ye,{stack:r})]})}function Ne(){const{data:t}=u();return e.jsxs("section",{className:"space-y-5 border-b border-theme-border-moderate pb-5",children:[e.jsxs(Y,{className:"flex items-center justify-between gap-4 px-6 py-5",children:[e.jsxs("div",{className:"flex items-start gap-3",children:[e.jsx(h,{provider:t.provider,className:"h-6 w-6 shrink-0"}),e.jsxs("div",{children:[e.jsx("p",{className:"text-text-lg font-semibold",children:"Deploying the Stack..."}),e.jsx("p",{className:"text-theme-text-secondary",children:"Follow the steps in your Cloud console to finish the setup. You can come back to check once your components are deployed."})]})]}),t.provider==="azure"?e.jsx(A,{children:e.jsx("span",{children:"Deploy in Azure"})}):e.jsx(A,{})]}),t.provider==="gcp"&&e.jsx(ne,{}),t.provider==="azure"&&e.jsx(oe,{})]})}function ye({stack:t}){const s=!!t;return e.jsxs("div",{className:"space-y-5",children:[!s&&e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"flex items-center gap-1 text-text-lg font-semibold",children:[e.jsx(de,{className:"h-5 w-5 fill-primary-400"}),"Creating your stack and components..."]}),e.jsx("p",{className:"text-theme-text-secondary",children:"We are creating your stack and stack components based on your configuration. Once you finish the setup, come back to check your brand new stack and components ready."})]}),e.jsx(Se,{isReady:s}),e.jsx(ge,{stack:t})]})}function ge({stack:t}){const s=!!t,{data:a}=u();return e.jsxs("div",{className:"relative overflow-hidden rounded-md",children:[!s&&e.jsx("div",{className:"absolute z-50 h-full w-full bg-neutral-50/50"}),e.jsx(O,{type:a.provider,componentProps:{isLoading:!s,isSuccess:s,stackName:a.stackName}})]})}function Se({isReady:t}){const[s,a]=f.useState(!1);return f.useEffect(()=>{const n=setTimeout(()=>{a(!0)},3e5);return()=>clearTimeout(n)},[]),!s||t?null:e.jsx(G,{children:"Your stack is taking longer than usual to deploy. Please check your Cloud console, or the stacks list in ZenML."})}function ke(){return e.jsx(j,{title:"Deploy ZenML Stack",children:e.jsx(be,{})})}function be(){const{setIsNextButtonDisabled:t,isLoading:s}=u();return f.useEffect(()=>{t(!0)},[]),s?e.jsx(ve,{}):e.jsx(ie,{})}function we(){const{formRef:t,setIsNextButtonDisabled:s,setData:a,data:n}=u(),{register:o,handleSubmit:l,formState:{isValid:r}}=Q({resolver:H(fe),defaultValues:{provider:n.provider}});f.useEffect(()=>{s(!r)},[r,s]);function m(d){a(c=>({...c,provider:d.provider}))}return e.jsx(j,{title:"New Cloud Infrastructure",children:e.jsxs("div",{className:"space-y-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsx("p",{className:"text-text-lg font-semibold",children:"Select a Cloud Provider"}),e.jsx("p",{className:"text-theme-text-secondary",children:"Select the cloud provider where your want to create your infrastructure and deploy your ZenML models. You will be able to remove the ZenML stack at any time."})]}),e.jsxs("form",{id:"provider-form",onSubmit:l(m),className:"grid grid-cols-1 gap-3 xl:grid-cols-3",ref:t,children:[e.jsx(v,{id:"aws-provider",...o("provider"),value:"aws",children:e.jsx(N,{icon:e.jsx(h,{provider:"aws",className:"h-6 w-6 shrink-0"}),title:"AWS",subtitle:"ZenML stack with S3, ECR, and SageMaker integration"})}),e.jsx(v,{id:"gcp-provider",...o("provider"),value:"gcp",children:e.jsx(N,{icon:e.jsx(h,{provider:"gcp",className:"h-6 w-6 shrink-0"}),title:"GCP",subtitle:"Create ZenML infrastructure using GCS, Artifact Registry, and Vertex AI"})}),e.jsx(v,{id:"azure-provider",...o("provider"),value:"azure",children:e.jsx(N,{icon:e.jsx(h,{provider:"azure",className:"h-6 w-6 shrink-0"}),title:"Azure",subtitle:"Set up ZenML with Azure Storage, Container Registry, and ML services"})})]})]})})}function Ce({provider:t,stackName:s,timestamp:a,isTerraform:n}){var g,S,k,b,w,C,P,D,I,z,L,R,B,E,W,F,M,_;const{isPending:o,isError:l,data:r}=K({...J.stackDeploymentStack({provider:t,stack_name:s,date_start:a,terraform:n}),throwOnError:!0});if(o)return e.jsx(V,{className:"h-[200px] w-full"});if(l)return null;const m=r.stack.name,d=(g=r.stack.metadata)==null?void 0:g.components.orchestrator,c=(S=r.stack.metadata)==null?void 0:S.components.artifact_store,i=(k=r.stack.metadata)==null?void 0:k.components.container_registry,p=(b=r.stack.metadata)==null?void 0:b.components.image_builder,x=(w=r.stack.metadata)==null?void 0:w.components.step_operator,U={orchestrator:{name:((C=d==null?void 0:d[0])==null?void 0:C.name)??"Orchestrator",id:((P=d==null?void 0:d[0])==null?void 0:P.id.split("-")[0])??""},artifactStore:{name:((D=c==null?void 0:c[0])==null?void 0:D.name)??"Artifact Store",id:((I=c==null?void 0:c[0])==null?void 0:I.id.split("-")[0])??""},registry:{name:((z=i==null?void 0:i[0])==null?void 0:z.name)??"Container Registry",id:((L=i==null?void 0:i[0])==null?void 0:L.id.split("-")[0])??""},connector:{name:(R=r.service_connector)==null?void 0:R.name,id:((E=(B=r.service_connector)==null?void 0:B.id)==null?void 0:E.split("-")[0])??""},imageBuilder:{name:((W=p==null?void 0:p[0])==null?void 0:W.name)??"Image Builder",id:((F=p==null?void 0:p[0])==null?void 0:F.id.split("-")[0])??""},operator:{name:((M=x==null?void 0:x[0])==null?void 0:M.name)??"Step Operator",id:((_=x==null?void 0:x[0])==null?void 0:_.id.split("-")[0])??""}};return e.jsx(O,{type:t,componentProps:{components:U,isSuccess:!0,stackName:m}})}function Pe(){const{setIsNextButtonDisabled:t,data:s,timestamp:a}=u();return t(!1),e.jsx(j,{title:"Your Stack",children:e.jsxs("div",{className:"space-y-5",children:[e.jsx("p",{className:"text-theme-text-secondary",children:"Here you can review the created stack and stack components. Now you can start running pipelines using this new configuration."}),e.jsx(Ce,{provider:s.provider||"aws",stackName:s.stackName||"",timestamp:a})]})})}function De(){const{currentStep:t}=y();if(t===1)return e.jsx(we,{});if(t===2)return e.jsx(je,{});if(t===3)return e.jsx(ke,{});if(t===4)return e.jsx(Pe,{})}function Ie(){var c;const[s]=me(),{setCurrentStep:a,currentStep:n}=y(),{formRef:o,isNextButtonDisabled:l}=u(),r=ue(),m=s.get("origin")==="onboarding";async function d(){o.current&&(o.current.requestSubmit(),await new Promise(i=>setTimeout(i,20))),a(i=>i<4?i+1:i),n===4&&(q(),r(m?T.onboarding:T.stacks.overview))}return e.jsx(le,{form:(c=o.current)==null?void 0:c.id,disabled:l,onClick:()=>d(),size:"md",children:n===4?"Finish":"Next"})}function j({children:t,title:s}){return e.jsxs(Y,{className:"w-full",children:[e.jsx("div",{className:"border-b border-theme-border-moderate px-5 py-3 text-display-xs font-semibold",children:s}),e.jsx("div",{className:"p-5",children:t}),e.jsxs("div",{className:"flex items-center justify-end gap-2 border-t border-theme-border-moderate p-5",children:[e.jsx($,{}),e.jsx(Ie,{})]})]})}const Z=["Infrastructure Type","Cloud Provider","Review Configuration","Deploy Stack"];function et(){const{success:t}=he();return e.jsx(ee,{maxSteps:Z.length,initialStep:t?3:1,children:e.jsx(ce,{children:e.jsxs("section",{className:"layout-container flex flex-col gap-5 p-5 xl:flex-row",children:[e.jsx(te,{entries:Z}),e.jsx("div",{className:"w-full overflow-y-hidden",children:e.jsx(De,{})})]})})})}export{et as default};
