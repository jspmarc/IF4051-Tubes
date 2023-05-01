import{c as ct,d as X,r as F,s as ft,o as Dt,a as bt,w as E,t as et,h as dt,i as ht,C as mt,L as Mt,v as xt,b as Q,e as pt,f as _t,u as wt,g as St,j as S,k as it,l as ot,m as Ot}from"./index-4f632e0a.js";var nt={},Ct={get exports(){return nt},set exports(a){nt=a}};(function(a,r){(function(m,v){a.exports=v()})(ct,function(){var m=1e3,v=6e4,d=36e5,$="millisecond",h="second",p="minute",s="hour",D="day",O="week",f="month",x="quarter",k="year",C="date",i="Invalid Date",_=/^(\d{4})[-/]?(\d{1,2})?[-/]?(\d{0,2})[Tt\s]*(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?[.:]?(\d+)?$/,A=/\[([^\]]+)]|Y{1,4}|M{1,4}|D{1,2}|d{1,4}|H{1,2}|h{1,2}|a|A|m{1,2}|s{1,2}|Z{1,2}|SSS/g,H={name:"en",weekdays:"Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),months:"January_February_March_April_May_June_July_August_September_October_November_December".split("_"),ordinal:function(o){var n=["th","st","nd","rd"],t=o%100;return"["+o+(n[(t-20)%10]||n[t]||n[0])+"]"}},Y=function(o,n,t){var u=String(o);return!u||u.length>=n?o:""+Array(n+1-u.length).join(t)+o},Z={s:Y,z:function(o){var n=-o.utcOffset(),t=Math.abs(n),u=Math.floor(t/60),e=t%60;return(n<=0?"+":"-")+Y(u,2,"0")+":"+Y(e,2,"0")},m:function o(n,t){if(n.date()<t.date())return-o(t,n);var u=12*(t.year()-n.year())+(t.month()-n.month()),e=n.clone().add(u,f),c=t-e<0,l=n.clone().add(u+(c?-1:1),f);return+(-(u+(t-e)/(c?e-l:l-e))||0)},a:function(o){return o<0?Math.ceil(o)||0:Math.floor(o)},p:function(o){return{M:f,y:k,w:O,d:D,D:C,h:s,m:p,s:h,ms:$,Q:x}[o]||String(o||"").toLowerCase().replace(/s$/,"")},u:function(o){return o===void 0}},W="en",L={};L[W]=H;var N=function(o){return o instanceof J},R=function o(n,t,u){var e;if(!n)return W;if(typeof n=="string"){var c=n.toLowerCase();L[c]&&(e=c),t&&(L[c]=t,e=c);var l=n.split("-");if(!e&&l.length>1)return o(l[0])}else{var g=n.name;L[g]=n,e=g}return!u&&e&&(W=e),e||!u&&W},b=function(o,n){if(N(o))return o.clone();var t=typeof n=="object"?n:{};return t.date=o,t.args=arguments,new J(t)},y=Z;y.l=R,y.i=N,y.w=function(o,n){return b(o,{locale:n.$L,utc:n.$u,x:n.$x,$offset:n.$offset})};var J=function(){function o(t){this.$L=R(t.locale,null,!0),this.parse(t)}var n=o.prototype;return n.parse=function(t){this.$d=function(u){var e=u.date,c=u.utc;if(e===null)return new Date(NaN);if(y.u(e))return new Date;if(e instanceof Date)return new Date(e);if(typeof e=="string"&&!/Z$/i.test(e)){var l=e.match(_);if(l){var g=l[2]-1||0,w=(l[7]||"0").substring(0,3);return c?new Date(Date.UTC(l[1],g,l[3]||1,l[4]||0,l[5]||0,l[6]||0,w)):new Date(l[1],g,l[3]||1,l[4]||0,l[5]||0,l[6]||0,w)}}return new Date(e)}(t),this.$x=t.x||{},this.init()},n.init=function(){var t=this.$d;this.$y=t.getFullYear(),this.$M=t.getMonth(),this.$D=t.getDate(),this.$W=t.getDay(),this.$H=t.getHours(),this.$m=t.getMinutes(),this.$s=t.getSeconds(),this.$ms=t.getMilliseconds()},n.$utils=function(){return y},n.isValid=function(){return this.$d.toString()!==i},n.isSame=function(t,u){var e=b(t);return this.startOf(u)<=e&&e<=this.endOf(u)},n.isAfter=function(t,u){return b(t)<this.startOf(u)},n.isBefore=function(t,u){return this.endOf(u)<b(t)},n.$g=function(t,u,e){return y.u(t)?this[u]:this.set(e,t)},n.unix=function(){return Math.floor(this.valueOf()/1e3)},n.valueOf=function(){return this.$d.getTime()},n.startOf=function(t,u){var e=this,c=!!y.u(u)||u,l=y.p(t),g=function(V,U){var P=y.w(e.$u?Date.UTC(e.$y,U,V):new Date(e.$y,U,V),e);return c?P:P.endOf(D)},w=function(V,U){return y.w(e.toDate()[V].apply(e.toDate("s"),(c?[0,0,0,0]:[23,59,59,999]).slice(U)),e)},M=this.$W,T=this.$M,I=this.$D,j="set"+(this.$u?"UTC":"");switch(l){case k:return c?g(1,0):g(31,11);case f:return c?g(1,T):g(0,T+1);case O:var z=this.$locale().weekStart||0,B=(M<z?M+7:M)-z;return g(c?I-B:I+(6-B),T);case D:case C:return w(j+"Hours",0);case s:return w(j+"Minutes",1);case p:return w(j+"Seconds",2);case h:return w(j+"Milliseconds",3);default:return this.clone()}},n.endOf=function(t){return this.startOf(t,!1)},n.$set=function(t,u){var e,c=y.p(t),l="set"+(this.$u?"UTC":""),g=(e={},e[D]=l+"Date",e[C]=l+"Date",e[f]=l+"Month",e[k]=l+"FullYear",e[s]=l+"Hours",e[p]=l+"Minutes",e[h]=l+"Seconds",e[$]=l+"Milliseconds",e)[c],w=c===D?this.$D+(u-this.$W):u;if(c===f||c===k){var M=this.clone().set(C,1);M.$d[g](w),M.init(),this.$d=M.set(C,Math.min(this.$D,M.daysInMonth())).$d}else g&&this.$d[g](w);return this.init(),this},n.set=function(t,u){return this.clone().$set(t,u)},n.get=function(t){return this[y.p(t)]()},n.add=function(t,u){var e,c=this;t=Number(t);var l=y.p(u),g=function(T){var I=b(c);return y.w(I.date(I.date()+Math.round(T*t)),c)};if(l===f)return this.set(f,this.$M+t);if(l===k)return this.set(k,this.$y+t);if(l===D)return g(1);if(l===O)return g(7);var w=(e={},e[p]=v,e[s]=d,e[h]=m,e)[l]||1,M=this.$d.getTime()+t*w;return y.w(M,this)},n.subtract=function(t,u){return this.add(-1*t,u)},n.format=function(t){var u=this,e=this.$locale();if(!this.isValid())return e.invalidDate||i;var c=t||"YYYY-MM-DDTHH:mm:ssZ",l=y.z(this),g=this.$H,w=this.$m,M=this.$M,T=e.weekdays,I=e.months,j=function(U,P,tt,K){return U&&(U[P]||U(u,c))||tt[P].slice(0,K)},z=function(U){return y.s(g%12||12,U,"0")},B=e.meridiem||function(U,P,tt){var K=U<12?"AM":"PM";return tt?K.toLowerCase():K},V={YY:String(this.$y).slice(-2),YYYY:this.$y,M:M+1,MM:y.s(M+1,2,"0"),MMM:j(e.monthsShort,M,I,3),MMMM:j(I,M),D:this.$D,DD:y.s(this.$D,2,"0"),d:String(this.$W),dd:j(e.weekdaysMin,this.$W,T,2),ddd:j(e.weekdaysShort,this.$W,T,3),dddd:T[this.$W],H:String(g),HH:y.s(g,2,"0"),h:z(1),hh:z(2),a:B(g,w,!0),A:B(g,w,!1),m:String(w),mm:y.s(w,2,"0"),s:String(this.$s),ss:y.s(this.$s,2,"0"),SSS:y.s(this.$ms,3,"0"),Z:l};return c.replace(A,function(U,P){return P||V[U]||l.replace(":","")})},n.utcOffset=function(){return 15*-Math.round(this.$d.getTimezoneOffset()/15)},n.diff=function(t,u,e){var c,l=y.p(u),g=b(t),w=(g.utcOffset()-this.utcOffset())*v,M=this-g,T=y.m(this,g);return T=(c={},c[k]=T/12,c[f]=T,c[x]=T/3,c[O]=(M-w)/6048e5,c[D]=(M-w)/864e5,c[s]=M/d,c[p]=M/v,c[h]=M/m,c)[l]||M,e?T:y.a(T)},n.daysInMonth=function(){return this.endOf(f).$D},n.$locale=function(){return L[this.$L]},n.locale=function(t,u){if(!t)return this.$L;var e=this.clone(),c=R(t,u,!0);return c&&(e.$L=c),e},n.clone=function(){return y.w(this.$d,this)},n.toDate=function(){return new Date(this.valueOf())},n.toJSON=function(){return this.isValid()?this.toISOString():null},n.toISOString=function(){return this.$d.toISOString()},n.toString=function(){return this.$d.toUTCString()},o}(),rt=J.prototype;return b.prototype=rt,[["$ms",$],["$s",h],["$m",p],["$H",s],["$W",D],["$M",f],["$y",k],["$D",C]].forEach(function(o){rt[o[1]]=function(n){return this.$g(n,o[0],o[1])}}),b.extend=function(o,n){return o.$i||(o(n,J,b),o.$i=!0),b},b.locale=R,b.isDayjs=N,b.unix=function(o){return b(1e3*o)},b.en=L[W],b.Ls=L,b.p={},b})})(Ct);const st=nt;var at={},Tt={get exports(){return at},set exports(a){at=a}};(function(a,r){(function(m,v){a.exports=v()})(ct,function(){var m="minute",v=/[+-]\d\d(?::?\d\d)?/g,d=/([+-]|\d\d)/g;return function($,h,p){var s=h.prototype;p.utc=function(i){var _={date:i,utc:!0,args:arguments};return new h(_)},s.utc=function(i){var _=p(this.toDate(),{locale:this.$L,utc:!0});return i?_.add(this.utcOffset(),m):_},s.local=function(){return p(this.toDate(),{locale:this.$L,utc:!1})};var D=s.parse;s.parse=function(i){i.utc&&(this.$u=!0),this.$utils().u(i.$offset)||(this.$offset=i.$offset),D.call(this,i)};var O=s.init;s.init=function(){if(this.$u){var i=this.$d;this.$y=i.getUTCFullYear(),this.$M=i.getUTCMonth(),this.$D=i.getUTCDate(),this.$W=i.getUTCDay(),this.$H=i.getUTCHours(),this.$m=i.getUTCMinutes(),this.$s=i.getUTCSeconds(),this.$ms=i.getUTCMilliseconds()}else O.call(this)};var f=s.utcOffset;s.utcOffset=function(i,_){var A=this.$utils().u;if(A(i))return this.$u?0:A(this.$offset)?f.call(this):this.$offset;if(typeof i=="string"&&(i=function(W){W===void 0&&(W="");var L=W.match(v);if(!L)return null;var N=(""+L[0]).match(d)||["-",0,0],R=N[0],b=60*+N[1]+ +N[2];return b===0?0:R==="+"?b:-b}(i),i===null))return this;var H=Math.abs(i)<=16?60*i:i,Y=this;if(_)return Y.$offset=H,Y.$u=i===0,Y;if(i!==0){var Z=this.$u?this.toDate().getTimezoneOffset():-1*this.utcOffset();(Y=this.local().add(H+Z,m)).$offset=H,Y.$x.$localOffset=Z}else Y=this.utc();return Y};var x=s.format;s.format=function(i){var _=i||(this.$u?"YYYY-MM-DDTHH:mm:ss[Z]":"");return x.call(this,_)},s.valueOf=function(){var i=this.$utils().u(this.$offset)?0:this.$offset+(this.$x.$localOffset||this.$d.getTimezoneOffset());return this.$d.valueOf()-6e4*i},s.isUTC=function(){return!!this.$u},s.toISOString=function(){return this.toDate().toISOString()},s.toString=function(){return this.toDate().toUTCString()};var k=s.toDate;s.toDate=function(i){return i==="s"&&this.$offset?p(this.format("YYYY-MM-DD HH:mm:ss:SSS")).toDate():k.call(this)};var C=s.diff;s.diff=function(i,_,A){if(i&&this.$u===i.$u)return C.call(this,i,_,A);var H=this.local(),Y=p(i).local();return C.call(H,Y,_,A)}}})})(Tt);const vt=at,$t={data:{type:Object,required:!0},options:{type:Object,default:()=>({})},plugins:{type:Array,default:()=>[]},datasetIdKey:{type:String,default:"label"},updateMode:{type:String,default:void 0}},kt={type:{type:String,required:!0},...$t},Yt=xt[0]==="2"?(a,r)=>Object.assign(a,{attrs:r}):(a,r)=>Object.assign(a,r);function q(a){return ht(a)?et(a):a}function Ut(a){let r=arguments.length>1&&arguments[1]!==void 0?arguments[1]:a;return ht(r)?new Proxy(a,{}):a}function At(a,r){const m=a.options;m&&r&&Object.assign(m,r)}function gt(a,r){a.labels=r}function yt(a,r,m){const v=[];a.datasets=r.map(d=>{const $=a.datasets.find(h=>h[m]===d[m]);return!$||!d.data||v.includes($)?{...d}:(v.push($),Object.assign($,d),$)})}function Ht(a,r){const m={labels:[],datasets:[]};return gt(m,a.labels),yt(m,a.datasets,r),m}const Lt=X({props:kt,setup(a,r){let{expose:m}=r;const v=F(null),d=ft(null);m({chart:d});const $=()=>{if(!v.value)return;const{type:s,data:D,options:O,plugins:f,datasetIdKey:x}=a,k=Ht(D,x),C=Ut(k,D);d.value=new mt(v.value,{type:s,data:C,options:{...O},plugins:f})},h=()=>{const s=et(d.value);s&&(s.destroy(),d.value=null)},p=s=>{s.update(a.updateMode)};return Dt($),bt(h),E([()=>a.options,()=>a.data],(s,D)=>{let[O,f]=s,[x,k]=D;const C=et(d.value);if(!C)return;let i=!1;if(O){const _=q(O),A=q(x);_&&_!==A&&(At(C,_),i=!0)}if(f){const _=q(f.labels),A=q(k.labels),H=q(f.datasets),Y=q(k.datasets);_!==A&&(gt(C.config.data,_),i=!0),H&&H!==Y&&(yt(C.config.data,H,a.datasetIdKey),i=!0)}i&&p(C)},{deep:!0}),()=>dt("canvas",{ref:v})}});function Wt(a,r){return mt.register(r),X({props:$t,setup(m,v){let{expose:d}=v;const $=ft(null),h=p=>{$.value=p==null?void 0:p.chart};return d({chart:$}),()=>dt(Lt,Yt({ref:h},{type:a,...m}))}})}const jt=Wt("line",Mt);function It(a){return a?{type:"line",borderColor:"black",borderDashOffset:0,borderWidth:10,drawTime:"beforeDatasetsDraw",label:{display:!0,backgroundColor:"black",borderColor:"black",borderRadius:10,borderWidth:2,content:r=>`Average for the last 15 seconds: ${r.chart.options.plugins.annotation.annotations.average.value}`,rotation:"auto"},scaleID:"y",value:a,z:10}:void 0}function Pt(a){return a?{type:"line",borderColor:"green",borderDashOffset:0,borderWidth:10,drawTime:"beforeDatasetsDraw",label:{display:!0,backgroundColor:"green",borderColor:"green",borderRadius:10,borderWidth:2,content:r=>`Minimum for the last 15 seconds: ${r.chart.options.plugins.annotation.annotations.minimum.value}`,rotation:"auto"},scaleID:"y",value:a}:void 0}function Nt(a){return a?{type:"line",borderColor:"red",borderDashOffset:0,borderWidth:10,drawTime:"beforeDatasetsDraw",label:{display:!0,backgroundColor:"red",borderColor:"red",borderRadius:10,borderWidth:2,content:r=>`Maximum for the last 15 seconds: ${r.chart.options.plugins.annotation.annotations.maximum.value}`,rotation:"auto"},scaleID:"y",value:a}:void 0}function ut(a,r){const m=[],v=[];return a.forEach($=>{const{time:h}=$;m.push(h.format("DD-MM-YYYY HH:mm:ss")),v.push($.value)}),{labels:m,datasets:[{label:r,data:v}]}}const Rt={class:"h-full w-full"},lt=X({__name:"Chart",props:{data:null,dataLabel:null,mean:null,min:null,max:null},setup(a){const r=a,m=F({...ut(r.data,r.dataLabel)});E(()=>r.data,p=>{const s=ut(p,r.dataLabel);m.value={...s}});const v=It(r.mean);E(()=>r.mean,p=>{const s=h.value.plugins.annotation.annotations.average;s&&p&&(s.value=p,h.value={...h.value})});const d=Pt(r.mean);E(()=>r.min,p=>{const s=h.value.plugins.annotation.annotations.minimum;s&&p&&(s.value=p,h.value={...h.value})});const $=Nt(r.mean);E(()=>r.max,p=>{const s=h.value.plugins.annotation.annotations.average;s&&p&&(s.value=p,h.value={...h.value})});const h=F({responsive:!0,maintainAspectRatio:!1,plugins:{annotation:{annotations:{average:v,minimum:d,maximum:$}}}});return(p,s)=>(Q(),pt("div",Rt,[_t(wt(jt),{data:m.value,options:h.value},null,8,["data","options"])]))}});st.extend(vt);async function G(a,r,m){let v=`${a}/realtime-data?time_range=-${m}`;r=="all"?v+="&data=co2&data=temperature":r=="temp"?v+="&data=temperature":r=="co2"&&(v+="&data=co2");const d=await(await fetch(v)).json(),$={};for(const h in d){if(h!=="humidity"&&h!=="temperature"&&h!=="co2")continue;const p=d[h];p&&($[h]=p.map(s=>({time:st.utc(s[0]).local(),value:s[1]})))}return $}const Vt={class:"flex flex-col gap-4 items-center justify-center"},qt={class:"flex flex-col lg:flex-row h-screen lg:h-[30rem] items-center justify-center px-4 lg:px-10 w-full"},zt={class:"flex flex-col items-center justify-center h-full w-full"},Bt=S("p",null,"Temperature",-1),Et={class:"flex flex-col items-center justify-center h-full w-full"},Ft=S("p",null,[Ot("CO"),S("sub",null,"2")],-1),Zt={class:"selection gray-1 flex flex-row gap-6 p-1 rounded-full"},Jt={class:"rounded-full"},Kt={class:"rounded-full"},Gt={class:"rounded-full"},Qt={class:"rounded-full"},Xt={class:"rounded-full"},ee=X({__name:"StatsView",props:{appState:null,beUrl:null},async setup(a){let r,m;const v=a;st.extend(vt);const d=F({}),$=F("30s"),h=([r,m]=St(()=>G(v.beUrl,"all",$.value)),r=await r,m(),r);d.value={...h};async function p(O){O.preventDefault();const f=await G(v.beUrl,"temp",$.value);d.value.co2&&(f.co2=[...d.value.co2]),d.value={...f}}async function s(O){O.preventDefault();const f=await G(v.beUrl,"co2",$.value);d.value.temperature&&(f.temperature=[...d.value.temperature]),d.value={...f}}async function D(O,f){O.preventDefault(),$.value=f;const x=await G(v.beUrl,"all",f);d.value={...x}}return(O,f)=>(Q(),pt("div",Vt,[S("div",qt,[S("div",zt,[Bt,d.value.temperature!=null?(Q(),it(lt,{key:0,data:d.value.temperature,mean:a.appState.dht22_statistics.temperature_avg,min:a.appState.dht22_statistics.temperature_min,max:a.appState.dht22_statistics.temperature_max,"data-label":"Temperature (in °C)"},null,8,["data","mean","min","max"])):ot("",!0),S("button",{onClick:p},"Update data")]),S("div",Et,[Ft,d.value.co2!=null?(Q(),it(lt,{key:0,data:d.value.co2,mean:a.appState.mq135_statistics.co2_avg,min:a.appState.mq135_statistics.co2_min,max:a.appState.mq135_statistics.co2_max,"data-label":"CO2 PPM"},null,8,["data","mean","min","max"])):ot("",!0),S("button",{onClick:s},"Update data")])]),S("ul",Zt,[S("li",Jt,[S("button",{class:"p-1",onClick:f[0]||(f[0]=x=>D(x,"30s"))}," 30 seconds ago ")]),S("li",Kt,[S("button",{class:"p-1",onClick:f[1]||(f[1]=x=>D(x,"1m"))}," 1 minute ago ")]),S("li",Gt,[S("button",{class:"p-1",onClick:f[2]||(f[2]=x=>D(x,"5m"))}," 5 minutes ago ")]),S("li",Qt,[S("button",{class:"p-1",onClick:f[3]||(f[3]=x=>D(x,"30m"))}," 30 minutes ago ")]),S("li",Xt,[S("button",{class:"p-1",onClick:f[4]||(f[4]=x=>D(x,"1h"))}," 1 hour ago ")])])]))}});export{ee as default};
