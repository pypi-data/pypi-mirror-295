import{r as h,j as e}from"./@radix-DnFH_oo1.js";import{S as D}from"./package-DYKZ5jKW.js";import{I as j}from"./Infobox-BB7dfbrO.js";import{b as E,C as H}from"./index.esm-BE1uqCX5.js";import{T as N}from"./Tick-DEACFydX.js";import{aH as V,aI as T,aJ as O,aG as L,S as v,y as k,A as z,b as A,h as G,B as W,am as Y,an as q,ao as F,ap as Q,aq as J}from"./index-Davdjm1d.js";import{p as $,C as o,s as K}from"./persist-g4uRK-v-.js";import{s as b}from"./sharedSchema-Dbpe2oAO.js";import{g as U}from"./ProviderRadio-DkPE6alG.js";import{a as y}from"./@tanstack-QbMbTrh5.js";import{S as I}from"./logs-GiDJXbLS.js";import{C as w}from"./CodeSnippet-i_WEOWw9.js";import{N as M}from"./NumberBox-CrN0_kqI.js";import{C as X}from"./ProviderIcon-wA4qBOv1.js";const Z=h.createContext(null);function Be({children:a}){const{success:t,data:s}=$(),[r,n]=h.useState(!1),[l,i]=h.useState(!!t),[c,u]=h.useState(t?{location:s.location,provider:s.provider,stackName:s.stackName}:{}),[x,p]=h.useState(t?s.timestamp:""),m=h.useRef(null);return e.jsx(Z.Provider,{value:{isNextButtonDisabled:r,setIsNextButtonDisabled:n,data:c,setData:u,isLoading:l,setIsLoading:i,formRef:m,timestamp:x,setTimestamp:p},children:a})}function S(){const a=h.useContext(Z);if(a===null)throw new Error("useNewInfraFormContext must be used within an AuthProvider");return a}const ee=a=>h.createElement("svg",{viewBox:"0 0 24 24",fill:"black",xmlns:"http://www.w3.org/2000/svg",...a},h.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3ZM1 12C1 5.92487 5.92487 1 12 1C18.0751 1 23 5.92487 23 12C23 18.0751 18.0751 23 12 23C5.92487 23 1 18.0751 1 12ZM12 4.5C12.5523 4.5 13 4.94772 13 5.5V6H13.1667C15.0076 6 16.5 7.49238 16.5 9.33333C16.5 9.88562 16.0523 10.3333 15.5 10.3333C14.9477 10.3333 14.5 9.88562 14.5 9.33333C14.5 8.59695 13.903 8 13.1667 8H11C10.1716 8 9.5 8.67157 9.5 9.5C9.5 10.3284 10.1716 11 11 11H13C14.933 11 16.5 12.567 16.5 14.5C16.5 16.433 14.933 18 13 18V18.5C13 19.0523 12.5523 19.5 12 19.5C11.4477 19.5 11 19.0523 11 18.5V18H10.8333C8.99238 18 7.5 16.5076 7.5 14.6667C7.5 14.1144 7.94772 13.6667 8.5 13.6667C9.05228 13.6667 9.5 14.1144 9.5 14.6667C9.5 15.403 10.097 16 10.8333 16H13C13.8284 16 14.5 15.3284 14.5 14.5C14.5 13.6716 13.8284 13 13 13H11C9.067 13 7.5 11.433 7.5 9.5C7.5 7.567 9.067 6 11 6V5.5C11 4.94772 11.4477 4.5 12 4.5Z"})),re=a=>h.createElement("svg",{viewBox:"0 0 24 24",fill:"black",xmlns:"http://www.w3.org/2000/svg",...a},h.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M5.16145 4L18.8385 4C19.3657 3.99998 19.8205 3.99997 20.195 4.03057C20.5904 4.06287 20.9836 4.13419 21.362 4.32698C21.9265 4.6146 22.3854 5.07354 22.673 5.63803C22.8658 6.01641 22.9371 6.40963 22.9694 6.80498C23 7.17954 23 7.6343 23 8.16144V15.8386C23 16.3657 23 16.8205 22.9694 17.195C22.9371 17.5904 22.8658 17.9836 22.673 18.362C22.3854 18.9265 21.9265 19.3854 21.362 19.673C20.9836 19.8658 20.5904 19.9371 20.195 19.9694C19.8205 20 19.3657 20 18.8386 20L5.16148 20C4.63432 20 4.17955 20 3.80497 19.9694C3.40963 19.9371 3.01641 19.8658 2.63803 19.673C2.07354 19.3854 1.6146 18.9265 1.32698 18.362C1.13419 17.9836 1.06287 17.5904 1.03057 17.195C0.999967 16.8205 0.999983 16.3657 1 15.8385L1 10.0006C1 10.0004 1 10.0008 1 10.0006C1 10.0004 1 9.99958 1 9.99937L1 8.16146C0.999983 7.63431 0.999968 7.17955 1.03057 6.80497C1.06287 6.40963 1.13419 6.01641 1.32698 5.63803C1.6146 5.07354 2.07354 4.6146 2.63803 4.32698C3.01641 4.13419 3.40963 4.06287 3.80497 4.03057C4.17955 3.99997 4.63431 3.99998 5.16145 4ZM3 11V15.8C3 16.3766 3.00078 16.7488 3.02393 17.0322C3.04612 17.3038 3.0838 17.4045 3.109 17.454C3.20487 17.6422 3.35785 17.7951 3.54601 17.891C3.59546 17.9162 3.69617 17.9539 3.96784 17.9761C4.25117 17.9992 4.62345 18 5.2 18L18.8 18C19.3766 18 19.7488 17.9992 20.0322 17.9761C20.3038 17.9539 20.4045 17.9162 20.454 17.891C20.6422 17.7951 20.7951 17.6422 20.891 17.454C20.9162 17.4045 20.9539 17.3038 20.9761 17.0322C20.9992 16.7488 21 16.3766 21 15.8V11H3ZM21 9H3V8.2C3 7.62345 3.00078 7.25117 3.02393 6.96784C3.04612 6.69617 3.0838 6.59546 3.109 6.54601C3.20487 6.35785 3.35785 6.20487 3.54601 6.109C3.59546 6.0838 3.69617 6.04612 3.96784 6.02393C4.25118 6.00078 4.62345 6 5.2 6L18.8 6C19.3766 6 19.7488 6.00078 20.0322 6.02393C20.3038 6.04613 20.4045 6.0838 20.454 6.109C20.6422 6.20487 20.7951 6.35785 20.891 6.54601C20.9162 6.59546 20.9539 6.69617 20.9761 6.96784C20.9992 7.25118 21 7.62345 21 8.2V9ZM5 14C5 13.4477 5.44772 13 6 13H11C11.5523 13 12 13.4477 12 14C12 14.5523 11.5523 15 11 15H6C5.44772 15 5 14.5523 5 14Z"}));function _({provider:a}){return e.jsxs(V,{children:[e.jsx(T,{className:"block",children:e.jsxs(j,{intent:"warning",children:["This will give ZenML permissions and create secret keys for secure ZenML -",">"," ",U(a)," communication. You can revoke these permissions at any time."]})}),e.jsx(O,{sideOffset:0,className:"w-auto p-5",children:e.jsx(L,{viewportClassName:"max-h-[300px]",children:e.jsx(ae,{provider:a})})})]})}function ae({provider:a}){const{isPending:t,isError:s,error:r,data:n}=y(b.stackDeploymentInfo({provider:a}));if(t)return e.jsx(v,{className:"h-[100px] w-full"});if(s)return e.jsx("p",{children:r.message});const l=Object.entries(n.permissions);return e.jsx("ul",{className:"space-y-2 pr-3 text-text-sm",children:l.map(([i,c])=>e.jsxs("li",{className:"flex flex-col gap-1",children:[e.jsx("p",{children:i}),e.jsx("ul",{className:"list-inside list-[square] pl-4 text-neutral-400 marker:text-primary-200",children:c.map((u,x)=>e.jsx("li",{children:u},x))})]},i))})}function te({stackName:a,isLoading:t,isSuccess:s,components:r,displayPermissions:n=!1}){var l,i,c,u,x,p,m,g,C,f;return e.jsxs("div",{className:"divide-y divide-theme-border-moderate overflow-hidden rounded-md border border-theme-border-moderate",children:[e.jsxs("div",{className:"flex items-center gap-3 bg-theme-surface-secondary p-5 text-text-lg font-semibold",children:[t&&e.jsx(k,{className:"h-5 w-5 shrink-0 border-[3px]"}),s&&e.jsx(N,{className:"h-5 w-5",tickClasses:"w-3 h-3"}),e.jsx(z,{type:"square",size:"lg",children:e.jsx(A,{size:"lg",children:a[0]})}),a]}),e.jsxs("div",{className:"space-y-1 py-3 pl-9 pr-5",children:[e.jsx(d,{title:((l=r==null?void 0:r.connector)==null?void 0:l.name)||"IAM Role",isLoading:t,isSuccess:s,subtitle:((i=r==null?void 0:r.connector)==null?void 0:i.id)||"Manage access to AWS resources",badge:e.jsx(o,{type:"annotator",children:"Service Connector"}),img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/service_connector/iam.webp",alt:"IAM logo"}}),n&&e.jsx(_,{provider:"aws"})]}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((c=r==null?void 0:r.artifactStore)==null?void 0:c.name)||"S3 Bucket",subtitle:((u=r==null?void 0:r.artifactStore)==null?void 0:u.id)||"Artifact storage for ML pipelines",badge:e.jsx(o,{type:"artifact_store",children:"Artifact Store"}),isLoading:t,isSuccess:s,img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/artifact_store/aws.png",alt:"S3 logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((x=r==null?void 0:r.registry)==null?void 0:x.name)||"ECR Repository",subtitle:((p=r==null?void 0:r.registry)==null?void 0:p.id)||"Container image storage",badge:e.jsx(o,{type:"container_registry",children:"Container Registry"}),isLoading:t,isSuccess:s,img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/container_registry/aws.png",alt:"ECR logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((m=r==null?void 0:r.orchestrator)==null?void 0:m.name)||"SageMaker",isLoading:t,isSuccess:s,subtitle:((g=r==null?void 0:r.orchestrator)==null?void 0:g.id)||"ML Workflow orchestration",badge:e.jsx(o,{type:"orchestrator",children:"Orchestrator"}),img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/orchestrator/sagemaker.png",alt:"Sagemaker logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((C=r==null?void 0:r.operator)==null?void 0:C.name)||"Sagemaker Step Operator",subtitle:((f=r==null?void 0:r.operator)==null?void 0:f.id)||"Execute individual steps",badge:e.jsx(o,{type:"step_operator",children:"Step Operator"}),isLoading:t,isSuccess:s,img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/step_operator/sagemaker.png",alt:"Sagemaker step operator logo"}})})]})}const se=a=>h.createElement("svg",{viewBox:"0 0 24 24",fill:"black",xmlns:"http://www.w3.org/2000/svg",...a},h.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M7.7587 2L10 2C10.5523 2 11 2.44772 11 3C11 3.55229 10.5523 4 10 4H7.8C6.94342 4 6.36113 4.00078 5.91104 4.03755C5.47262 4.07337 5.24842 4.1383 5.09202 4.21799C4.7157 4.40973 4.40973 4.7157 4.21799 5.09202C4.1383 5.24842 4.07337 5.47262 4.03755 5.91104C4.00078 6.36113 4 6.94342 4 7.8V16.2C4 17.0566 4.00078 17.6389 4.03755 18.089C4.07337 18.5274 4.1383 18.7516 4.21799 18.908C4.40973 19.2843 4.7157 19.5903 5.09202 19.782C5.24842 19.8617 5.47262 19.9266 5.91104 19.9624C6.36113 19.9992 6.94342 20 7.8 20H16.2C17.0566 20 17.6389 19.9992 18.089 19.9624C18.5274 19.9266 18.7516 19.8617 18.908 19.782C19.2843 19.5903 19.5903 19.2843 19.782 18.908C19.8617 18.7516 19.9266 18.5274 19.9624 18.089C19.9992 17.6389 20 17.0566 20 16.2V14C20 13.4477 20.4477 13 21 13C21.5523 13 22 13.4477 22 14V16.2413C22 17.0463 22 17.7106 21.9558 18.2518C21.9099 18.8139 21.8113 19.3306 21.564 19.816C21.1805 20.5686 20.5686 21.1805 19.816 21.564C19.3306 21.8113 18.8139 21.9099 18.2518 21.9558C17.7106 22 17.0463 22 16.2413 22H7.75868C6.95372 22 6.28936 22 5.74817 21.9558C5.18608 21.9099 4.66937 21.8113 4.18404 21.564C3.43139 21.1805 2.81947 20.5686 2.43598 19.816C2.18868 19.3306 2.09012 18.8139 2.04419 18.2518C1.99998 17.7106 1.99999 17.0463 2 16.2413V7.7587C1.99999 6.95373 1.99998 6.28937 2.04419 5.74817C2.09012 5.18608 2.18868 4.66937 2.43597 4.18404C2.81947 3.43139 3.43139 2.81947 4.18404 2.43597C4.66937 2.18868 5.18608 2.09012 5.74817 2.04419C6.28937 1.99998 6.95373 1.99999 7.7587 2ZM14 3.00001C14 2.44773 14.4477 2.00001 15 2.00001H21C21.5523 2.00001 22 2.44773 22 3.00001L22 9.00001C22 9.55229 21.5523 10 21 10C20.4477 10 20 9.5523 20 9.00001L20 5.41422L12.7071 12.7071C12.3166 13.0976 11.6834 13.0976 11.2929 12.7071C10.9024 12.3166 10.9024 11.6834 11.2929 11.2929L18.5858 4.00001H15C14.4477 4.00001 14 3.5523 14 3.00001Z"}));function le({stackName:a,isLoading:t,isSuccess:s,components:r,displayPermissions:n=!1}){var l,i,c,u,x,p,m,g,C,f,R,B;return e.jsxs("div",{className:"divide-y divide-theme-border-moderate overflow-hidden rounded-md border border-theme-border-moderate",children:[e.jsxs("div",{className:"flex items-center gap-3 bg-theme-surface-secondary p-5 text-text-lg font-semibold",children:[t&&e.jsx(k,{className:"h-5 w-5 shrink-0 border-[3px]"}),s&&e.jsx(N,{className:"h-5 w-5",tickClasses:"w-3 h-3"}),e.jsx(z,{type:"square",size:"lg",children:e.jsx(A,{size:"lg",children:a[0]})}),a]}),e.jsxs("div",{className:"space-y-1 py-3 pl-9 pr-5",children:[e.jsx(d,{title:((l=r==null?void 0:r.connector)==null?void 0:l.name)||"Service Account",isLoading:t,isSuccess:s,subtitle:((i=r==null?void 0:r.connector)==null?void 0:i.id)||"Manage access to GCP resources",badge:e.jsx(o,{type:"annotator",children:"Service Connector"}),img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/service_connector/gcp-iam.webp",alt:"Service Account logo"}}),n&&e.jsx(_,{provider:"gcp"})]}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((c=r==null?void 0:r.artifactStore)==null?void 0:c.name)||"GCS Bucket",subtitle:((u=r==null?void 0:r.artifactStore)==null?void 0:u.id)||"Artifact storage for ML pipelines",badge:e.jsx(o,{type:"artifact_store",children:"Artifact Store"}),isLoading:t,isSuccess:s,img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/artifact_store/gcp.png",alt:"GCS logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((x=r==null?void 0:r.registry)==null?void 0:x.name)||"Google Artifact Registry",subtitle:((p=r==null?void 0:r.registry)==null?void 0:p.id)||"Container image storage",badge:e.jsx(o,{type:"container_registry",children:"Container Registry"}),isLoading:t,isSuccess:s,img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/container_registry/gcp.png",alt:"Google Artifact Registry logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((m=r==null?void 0:r.orchestrator)==null?void 0:m.name)||"Vertex AI",isLoading:t,isSuccess:s,subtitle:((g=r==null?void 0:r.orchestrator)==null?void 0:g.id)||"ML Workflow orchestration",badge:e.jsx(o,{type:"orchestrator",children:"Orchestrator"}),img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/orchestrator/vertexai.png",alt:"VertexAI logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((C=r==null?void 0:r.imageBuilder)==null?void 0:C.name)||"Cloud Build",isLoading:t,isSuccess:s,subtitle:((f=r==null?void 0:r.imageBuilder)==null?void 0:f.id)||"Build, test, and deploy images",badge:e.jsx(o,{type:"image_builder",children:"Image Builder"}),img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/image_builder/gcp.png",alt:"Cloud Build logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((R=r==null?void 0:r.operator)==null?void 0:R.name)||"Vertex Step Operator",subtitle:((B=r==null?void 0:r.operator)==null?void 0:B.id)||"Execute individual steps",badge:e.jsx(o,{type:"step_operator",children:"Step Operator"}),isLoading:t,isSuccess:s,img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/step_operator/vertexai.png",alt:"Vertex step operator logo"}})})]})}function ie(){return e.jsx(j,{className:"border-warning-300 bg-warning-50",intent:"warning",children:'The Cloud Shell session will warn you that the ZenML GitHub repository is untrusted. We recommend that you review the contents of the repository and then check the "Trust repo" checkbox to proceed with the deployment, otherwise the Cloud Shell session will not be authenticated to access your GCP projects.'})}function ce(){const{data:a}=S(),t=y({...b.stackDeploymentConfig({provider:"gcp",stack_name:a.stackName,location:a.location})});return t.isError?null:t.isPending?e.jsx(v,{className:"h-[200px] w-full"}):e.jsxs("section",{className:"space-y-5 border-t border-theme-border-moderate pt-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"flex items-center gap-1 text-text-lg font-semibold",children:[e.jsx(I,{className:"h-5 w-5 fill-primary-400"}),"Configuration"]}),e.jsx("p",{className:"text-theme-text-secondary",children:"You will be asked to provide the following configuration values during the deployment process."})]}),e.jsx(w,{fullWidth:!0,highlightCode:!0,codeClasses:"whitespace-pre-wrap word-break-all",wrap:!0,code:t.data.configuration||""})]})}function Ee(){const{data:a}=S();return e.jsxs("div",{className:"space-y-5",children:[e.jsx(j,{children:"This will provision and register a basic ZenML stack with all the necessary resources and credentials required to run pipelines."}),a.provider!=="azure"&&e.jsxs("div",{children:[e.jsxs("div",{className:"flex flex-wrap items-center gap-1",children:[e.jsx(X,{provider:a.provider,className:"h-5 w-5"}),e.jsx("p",{className:"text-text-lg font-semibold",children:"Deploy the Stack"})]}),e.jsx("p",{className:"text-theme-text-secondary",children:"Deploy the stack from your browser by clicking the button below:"})]}),a.provider==="gcp"&&e.jsx(ie,{}),a.provider!=="azure"&&e.jsx(P,{setTimestampBool:!0}),a.provider==="gcp"&&e.jsx(ce,{}),a.provider==="azure"&&e.jsx(de,{displayInfobox:!0})]})}function P({setTimestampBool:a,children:t}){const{data:s,setTimestamp:r,setIsLoading:n}=S(),l=y({...b.stackDeploymentConfig({provider:s.provider,location:s.location,stack_name:s.stackName})});if(l.isError)return null;if(l.isPending)return e.jsx(v,{className:"h-[48px] w-[100px]"});function i(){const c=new Date().toISOString().slice(0,-1);a&&r(c),K({location:s.location||"",provider:s.provider||"aws",stackName:s.stackName,timestamp:c}),n(!0)}return e.jsx(G,{asChild:!0,className:"w-fit gap-3 whitespace-nowrap",size:"lg",onClick:()=>i(),children:e.jsxs("a",{href:l.data.deployment_url,target:"_blank",rel:"noopener noreferrer",children:[t||e.jsxs("div",{children:["Deploy in ",e.jsx("span",{className:"uppercase",children:s.provider})]}),e.jsx(se,{className:"h-5 w-5 shrink-0 fill-white"})]})})}function oe({stackName:a,isLoading:t,isSuccess:s,components:r,displayPermissions:n=!1}){var l,i,c,u,x,p,m,g,C,f;return e.jsxs("div",{className:"divide-y divide-theme-border-moderate overflow-hidden rounded-md border border-theme-border-moderate",children:[e.jsxs("div",{className:"flex items-center gap-3 bg-theme-surface-secondary p-5 text-text-lg font-semibold",children:[t&&e.jsx(k,{className:"h-5 w-5 shrink-0 border-[3px]"}),s&&e.jsx(N,{className:"h-5 w-5",tickClasses:"w-3 h-3"}),e.jsx(z,{type:"square",size:"lg",children:e.jsx(A,{size:"lg",children:a[0]})}),a]}),e.jsxs("div",{className:"space-y-1 py-3 pl-9 pr-5",children:[e.jsx(d,{title:((l=r==null?void 0:r.connector)==null?void 0:l.name)||"Azure Service Principal",isLoading:t,isSuccess:s,subtitle:((i=r==null?void 0:r.connector)==null?void 0:i.id)||"Manage access to Azure resources",badge:e.jsx(o,{type:"annotator",children:"Service Connector"}),img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/service_connector/azure-service-principal.webp",alt:"Service Principal logo"}}),n&&e.jsx(_,{provider:"azure"})]}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((c=r==null?void 0:r.artifactStore)==null?void 0:c.name)||"Azure Blob Storage",subtitle:((u=r==null?void 0:r.artifactStore)==null?void 0:u.id)||"Artifact storage for ML pipelines",badge:e.jsx(o,{type:"artifact_store",children:"Artifact Store"}),isLoading:t,isSuccess:s,img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/artifact_store/azure.png",alt:"Blob Storage logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((x=r==null?void 0:r.registry)==null?void 0:x.name)||"Azure Container Registry",subtitle:((p=r==null?void 0:r.registry)==null?void 0:p.id)||"Container image storage",badge:e.jsx(o,{type:"container_registry",children:"Container Registry"}),isLoading:t,isSuccess:s,img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/container_registry/azure.png",alt:"Azure Container Registry logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((m=r==null?void 0:r.orchestrator)==null?void 0:m.name)||"Azure ML",isLoading:t,isSuccess:s,subtitle:((g=r==null?void 0:r.orchestrator)==null?void 0:g.id)||"ML Workflow orchestration",badge:e.jsx(o,{type:"orchestrator",children:"Orchestrator"}),img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/orchestrator/azureml.png",alt:"Azure ML logo"}})}),e.jsx("div",{className:"py-3 pl-9 pr-5",children:e.jsx(d,{title:((C=r==null?void 0:r.operator)==null?void 0:C.name)||"Azure Step Operator",subtitle:((f=r==null?void 0:r.operator)==null?void 0:f.id)||"Execute individual steps",badge:e.jsx(o,{type:"step_operator",children:"Step Operator"}),isLoading:t,isSuccess:s,img:{src:"https://public-flavor-logos.s3.eu-central-1.amazonaws.com/step_operator/azureml.png",alt:"Azure Step Operator logo"}})})]})}function de({displayInfobox:a=!1}){return e.jsxs("section",{className:"space-y-5",children:[e.jsx(pe,{}),e.jsx(ne,{displayInfobox:a}),e.jsx(xe,{}),e.jsx(he,{})]})}function ne({displayInfobox:a=!1}){return e.jsxs("div",{className:"space-y-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsxs("div",{className:"flex items-center gap-1",children:[e.jsx(M,{children:"1"}),e.jsx("span",{className:"text-text-lg font-semibold",children:"Open the Azure Cloud Shell Console"})]}),e.jsx("p",{className:"text-theme-text-secondary",children:"Deploy the stack using the Azure Cloud Shell console."})]}),e.jsx(P,{setTimestampBool:!0,children:e.jsx("span",{className:"text-text-lg font-semibold",children:"Open the Azure Cloud Shell"})}),a&&e.jsx(j,{className:"border-warning-300 bg-warning-50",intent:"warning",children:"After the Terraform deployment is complete, you can close the Cloud Shell session and return to the dashboard to view details about the associated ZenML stack automatically registered with ZenML."})]})}function xe(){return e.jsxs("div",{className:"space-y-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsxs("div",{className:"flex items-center gap-1",children:[e.jsx(M,{children:"2"}),e.jsx("span",{className:"text-text-lg font-semibold",children:"Create a file with the following configuration"})]}),e.jsxs("p",{className:"text-theme-text-secondary",children:["Create a file named ",e.jsx("code",{className:"font-mono text-primary-400",children:"main.tf"})," in the Cloud Shell and copy and paste the Terraform configuration below into it."]})]}),e.jsx(ue,{})]})}function he(){return e.jsxs("div",{className:"space-y-5",children:[e.jsx("div",{className:"space-y-1",children:e.jsxs("div",{className:"flex items-center gap-1",children:[e.jsx(M,{children:"3"}),e.jsx("span",{className:"text-text-lg font-semibold",children:"Run the following commands"})]})}),e.jsxs("div",{children:[e.jsx("p",{className:"mb-1 text-text-sm text-theme-text-secondary",children:"Initialize the Terraform configuration."}),e.jsx(w,{code:"terraform init --upgrade"})]}),e.jsxs("div",{children:[e.jsx("p",{className:"mb-1 text-text-sm text-theme-text-secondary",children:"Run terraform apply to deploy the ZenML stack to Azure."}),e.jsx(w,{code:"terraform apply"})]})]})}function ue(){const{data:a}=S(),t=y({...b.stackDeploymentConfig({provider:"azure",stack_name:a.stackName,location:a.location}),enabled:!!a.stackName});return t.isError?null:t.isPending?e.jsx(v,{className:"h-[200px] w-full"}):e.jsx(w,{fullWidth:!0,highlightCode:!0,codeClasses:"whitespace-pre-wrap word-break-all",wrap:!0,code:t.data.configuration||""})}function pe(){return e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"flex items-center gap-1 text-text-lg font-semibold",children:[e.jsx(I,{className:"h-5 w-5 fill-primary-400"}),"Configuration"]}),e.jsx("p",{className:"text-theme-text-secondary",children:"You will be asked to provide the following configuration values during the deployment process."})]})}function me({componentProps:a,type:t}){switch(t){case"aws":return e.jsx(te,{...a});case"gcp":return e.jsx(le,{...a});case"azure":return e.jsx(oe,{...a})}}function d({img:a,title:t,subtitle:s,badge:r,isSuccess:n,isLoading:l}){return e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsxs("div",{className:"flex items-center gap-3",children:[l&&e.jsx(k,{className:"h-5 w-5 shrink-0 border-[3px]"}),n&&e.jsx(N,{className:"h-5 w-5",tickClasses:"w-3 h-3"}),e.jsx("img",{width:"40",height:"40",alt:a.alt,src:a.src}),e.jsxs("div",{children:[e.jsx("p",{className:"text-text-lg font-semibold",children:t}),e.jsx("p",{className:"text-theme-text-secondary",children:s})]})]}),r]})}function Le({provider:a}){function t(){let s="#";switch(a){case"aws":s="https://calculator.aws/#/";break;case"gcp":s="https://cloud.google.com/products/calculator";break;case"azure":s="https://azure.microsoft.com/en-us/pricing/calculator/";break}return e.jsx("a",{href:s,target:"_blank",rel:"noopener noreferrer",className:"link",children:"official pricing calculator"})}return e.jsxs("div",{className:"space-y-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"flex items-center gap-1 text-text-lg font-semibold",children:[e.jsx(ee,{className:"h-5 w-5 fill-primary-400"}),"Estimated Cost"]}),e.jsx("p",{className:"text-theme-text-secondary",children:"These are rough estimates and actual costs may vary based on your usage."})]}),e.jsxs(W,{className:"flex items-start gap-[10px] p-3",children:[e.jsx("div",{className:"content-center rounded-sm bg-blue-25 p-1",children:e.jsx(re,{className:"h-5 w-5 fill-blue-400"})}),e.jsxs("div",{children:[e.jsxs("p",{children:["A small training job would cost around:"," ",e.jsx("span",{className:"font-semibold text-theme-text-success",children:"$0.60"})]}),e.jsxs("p",{className:"text-text-xs text-theme-text-secondary",children:["Please use the ",e.jsx(t,{})," for a detailed estimate"]})]})]})]})}const ge=a=>h.createElement("svg",{viewBox:"0 0 24 24",fill:"black",xmlns:"http://www.w3.org/2000/svg",...a},h.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12 3C8.13401 3 5 6.13401 5 10C5 11.8921 5.85317 13.678 7.29228 15.5467C8.50741 17.1245 10.0627 18.6673 11.7323 20.3233C11.8212 20.4115 11.9105 20.5 12 20.5889C12.0895 20.5 12.1788 20.4115 12.2677 20.3233C13.9373 18.6673 15.4926 17.1245 16.7077 15.5467C18.1468 13.678 19 11.8921 19 10C19 6.13401 15.866 3 12 3ZM3 10C3 5.02944 7.02944 1 12 1C16.9706 1 21 5.02944 21 10C21 12.5262 19.8532 14.7402 18.2923 16.767C16.988 18.4607 15.3185 20.1156 13.6508 21.7689C13.3354 22.0816 13.02 22.3943 12.7071 22.7071C12.3166 23.0976 11.6834 23.0976 11.2929 22.7071C10.98 22.3943 10.6646 22.0816 10.3492 21.7689C8.68147 20.1156 7.01205 18.4607 5.70772 16.767C4.14683 14.7402 3 12.5262 3 10ZM12 8C10.8954 8 10 8.89543 10 10C10 11.1046 10.8954 12 12 12C13.1046 12 14 11.1046 14 10C14 8.89543 13.1046 8 12 8ZM8 10C8 7.79086 9.79086 6 12 6C14.2091 6 16 7.79086 16 10C16 12.2091 14.2091 14 12 14C9.79086 14 8 12.2091 8 10Z"}));function Ce({provider:a}){const{control:t}=E(),{isPending:s,isError:r,data:n}=y({...b.stackDeploymentInfo({provider:a})});if(r)return null;if(s)return e.jsx(v,{className:"h-[40px] w-[100px]"});const l=Object.entries(n.locations);return e.jsx(H,{control:t,name:"region",render:({field:{onChange:i,ref:c,...u}})=>e.jsxs(Y,{...u,onValueChange:i,children:[e.jsx(q,{className:"border border-neutral-300 text-left text-text-md",children:e.jsx(F,{className:"flex items-center gap-2",placeholder:"Select your Location"})}),e.jsx(Q,{children:e.jsx(L,{viewportClassName:"max-h-[300px]",children:l.map(([x,p])=>e.jsxs(J,{value:p,children:[x," - ",e.jsx("span",{className:"text-theme-text-secondary",children:p})]},x))})})]})})}function Ie({provider:a}){return e.jsxs("div",{className:"space-y-5 border-b border-theme-border-moderate pb-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"flex items-center gap-1 text-text-lg font-semibold",children:[e.jsx(ge,{className:"h-5 w-5 fill-primary-400"}),"Choose Your Location"]}),e.jsx("p",{className:"text-theme-text-secondary",children:"Select where you want to deploy your cloud infrastructure for optimal performance and compliance."})]}),e.jsx(Ce,{provider:a})]})}function Ze({provider:a}){const{watch:t}=E();return e.jsxs("div",{className:"space-y-5 border-b border-theme-border-moderate pb-5",children:[e.jsxs("div",{className:"space-y-1",children:[e.jsxs("p",{className:"flex items-center gap-1 text-text-lg font-semibold",children:[e.jsx(D,{className:"h-5 w-5 fill-primary-400"}),"Review Your Stack Components"]}),e.jsx("p",{className:"text-theme-text-secondary",children:"The following components will be created for your ZenML stack."})]}),e.jsx(me,{type:a,componentProps:{displayPermissions:!0,stackName:t("stackName")}}),e.jsx(j,{children:"These resources create a basic ZenML stack for ML workflow management. ZenML supports highly flexible stacks. You can build advanced stacks at any time, combining your preferred tools and components for more complex MLOps."})]})}export{de as A,me as C,P as D,Le as E,ce as G,Be as N,Ie as R,se as S,Ze as a,Ee as b,S as u};
