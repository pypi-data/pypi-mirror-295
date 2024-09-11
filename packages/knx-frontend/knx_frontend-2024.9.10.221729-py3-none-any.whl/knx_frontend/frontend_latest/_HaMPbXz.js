/*! For license information please see _HaMPbXz.js.LICENSE.txt */
export const id=8726;export const ids=[8726];export const modules={8017:(e,t,a)=>{const n=Intl&&Intl.DateTimeFormat,r=[38,33,36],i=[40,34,35],o=new Set([37,...r]),s=new Set([39,...i]),l=new Set([39,...r]),d=new Set([37,...i]),c=new Set([37,39,...r,...i]);var u=a(6513),h=a(8597),m=a(196),f=a(4078),p=a(2154),y=a(3982);const g=e=>(0,y.ps)(e)?e._$litType$.h:e.strings,w=(0,p.u$)(class extends p.WL{constructor(e){super(e),this.tt=new WeakMap}render(e){return[e]}update(e,[t]){const a=(0,y.qb)(this.et)?g(this.et):null,n=(0,y.qb)(t)?g(t):null;if(null!==a&&(null===n||a!==n)){const t=(0,y.cN)(e).pop();let n=this.tt.get(a);if(void 0===n){const e=document.createDocumentFragment();n=(0,f.XX)(f.s6,e),n.setConnected(!1),this.tt.set(a,n)}(0,y.mY)(n,[t]),(0,y.Dx)(n,void 0,t)}if(null!==n){if(null===a||a!==n){const t=this.tt.get(n);if(void 0!==t){const a=(0,y.cN)(t).pop();(0,y.Jz)(e),(0,y.Dx)(e,void 0,a),(0,y.mY)(e,[a])}}this.et=t}else this.et=void 0;return this.render(t)}});var b=a(9760),v=a(6580);function _(e,t,a){return new Date(Date.UTC(e,t,a))}const k=h.qy`<svg height="24" viewBox="0 0 24 24" width="24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"></path></svg>`,D=h.qy`<svg height="24" viewBox="0 0 24 24" width="24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"></path></svg>`,x=h.AH`
button {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;

  position: relative;
  display: block;
  margin: 0;
  padding: 0;
  background: none; /** NOTE: IE11 fix */
  color: inherit;
  border: none;
  font: inherit;
  text-align: left;
  text-transform: inherit;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}
`,M=(h.AH`
a {
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);

  position: relative;
  display: inline-block;
  background: initial;
  color: inherit;
  font: inherit;
  text-transform: inherit;
  text-decoration: none;
  outline: none;
}
a:focus,
a:focus.page-selected {
  text-decoration: underline;
}
`,h.AH`
svg {
  display: block;
  min-width: var(--svg-icon-min-width, 24px);
  min-height: var(--svg-icon-min-height, 24px);
  fill: var(--svg-icon-fill, currentColor);
  pointer-events: none;
}
`,h.AH`[hidden] { display: none !important; }`,h.AH`
:host {
  display: block;

  /* --app-datepicker-width: 300px; */
  /* --app-datepicker-primary-color: #4285f4; */
  /* --app-datepicker-header-height: 80px; */
}

* {
  box-sizing: border-box;
}
`);function T(e,t){return+t-+e}function C({hasAltKey:e,keyCode:t,focusedDate:a,selectedDate:n,disabledDaysSet:r,disabledDatesSet:i,minTime:c,maxTime:u}){const h=a.getUTCFullYear(),m=a.getUTCMonth(),f=a.getUTCDate(),p=+a,y=n.getUTCFullYear(),g=n.getUTCMonth();let w=h,b=m,v=f,k=!0;switch((g!==m||y!==h)&&(w=y,b=g,v=1,k=34===t||33===t||35===t),k){case p===c&&o.has(t):case p===u&&s.has(t):break;case 38===t:v-=7;break;case 40===t:v+=7;break;case 37===t:v-=1;break;case 39===t:v+=1;break;case 34===t:e?w+=1:b+=1;break;case 33===t:e?w-=1:b-=1;break;case 35===t:b+=1,v=0;break;default:v=1}if(34===t||33===t){const e=_(w,b+1,0).getUTCDate();v>e&&(v=e)}const D=function({keyCode:e,disabledDaysSet:t,disabledDatesSet:a,focusedDate:n,maxTime:r,minTime:i}){const o=+n;let s=o<i,c=o>r;if(T(i,r)<864e5)return n;let u=s||c||t.has(n.getUTCDay())||a.has(o);if(!u)return n;let h=0,m=s===c?n:new Date(s?i-864e5:864e5+r);const f=m.getUTCFullYear(),p=m.getUTCMonth();let y=m.getUTCDate();for(;u;)(s||!c&&l.has(e))&&(y+=1),(c||!s&&d.has(e))&&(y-=1),m=_(f,p,y),h=+m,s||(s=h<i,s&&(m=new Date(i),h=+m,y=m.getUTCDate())),c||(c=h>r,c&&(m=new Date(r),h=+m,y=m.getUTCDate())),u=t.has(m.getUTCDay())||a.has(h);return m}({keyCode:t,maxTime:u,minTime:c,disabledDaysSet:r,disabledDatesSet:i,focusedDate:_(w,b,v)});return D}function S(e,t,a){return e.dispatchEvent(new CustomEvent(t,{detail:a,bubbles:!0,composed:!0}))}function W(e,t){return e.composedPath().find((e=>e instanceof HTMLElement&&t(e)))}function F(e){return t=>e.format(t).replace(/\u200e/gi,"")}function N(e){const t=n(e,{timeZone:"UTC",weekday:"short",month:"short",day:"numeric"}),a=n(e,{timeZone:"UTC",day:"numeric"}),r=n(e,{timeZone:"UTC",year:"numeric",month:"short",day:"numeric"}),i=n(e,{timeZone:"UTC",year:"numeric",month:"long"}),o=n(e,{timeZone:"UTC",weekday:"long"}),s=n(e,{timeZone:"UTC",weekday:"narrow"}),l=n(e,{timeZone:"UTC",year:"numeric"});return{locale:e,dateFormat:F(t),dayFormat:F(a),fullDateFormat:F(r),longMonthYearFormat:F(i),longWeekdayFormat:F(o),narrowWeekdayFormat:F(s),yearFormat:F(l)}}function P(e,t){const a=function(e,t){const a=t.getUTCFullYear(),n=t.getUTCMonth(),r=t.getUTCDate(),i=t.getUTCDay();let o=i;return"first-4-day-week"===e&&(o=3),"first-day-of-year"===e&&(o=6),"first-full-week"===e&&(o=0),_(a,n,r-i+o)}(e,t),n=_(a.getUTCFullYear(),0,1),r=1+(+a-+n)/864e5;return Math.ceil(r/7)}function $(e){if(e>=0&&e<7)return Math.abs(e);return((e<0?7*Math.ceil(Math.abs(e)):0)+e)%7}function E(e,t,a){const n=$(e-t);return a?1+n:n}function Y(e){const{dayFormat:t,fullDateFormat:a,locale:n,longWeekdayFormat:r,narrowWeekdayFormat:i,selectedDate:o,disabledDates:s,disabledDays:l,firstDayOfWeek:d,max:c,min:u,showWeekNumber:h,weekLabel:m,weekNumberType:f}=e,p=null==u?Number.MIN_SAFE_INTEGER:+u,y=null==c?Number.MAX_SAFE_INTEGER:+c,g=function(e){const{firstDayOfWeek:t=0,showWeekNumber:a=!1,weekLabel:n,longWeekdayFormat:r,narrowWeekdayFormat:i}=e||{},o=1+(t+(t<0?7:0))%7,s=n||"Wk",l=a?[{label:"Wk"===s?"Week":s,value:s}]:[],d=Array.from(Array(7)).reduce(((e,t,a)=>{const n=_(2017,0,o+a);return e.push({label:r(n),value:i(n)}),e}),l);return d}({longWeekdayFormat:r,narrowWeekdayFormat:i,firstDayOfWeek:d,showWeekNumber:h,weekLabel:m}),w=e=>[n,e.toJSON(),null==s?void 0:s.join("_"),null==l?void 0:l.join("_"),d,null==c?void 0:c.toJSON(),null==u?void 0:u.toJSON(),h,m,f].filter(Boolean).join(":"),b=o.getUTCFullYear(),v=o.getUTCMonth(),k=[-1,0,1].map((e=>{const r=_(b,v+e,1),i=+_(b,v+e+1,0),o=w(r);if(i<p||+r>y)return{key:o,calendar:[],disabledDatesSet:new Set,disabledDaysSet:new Set};const g=function(e){const{date:t,dayFormat:a,disabledDates:n=[],disabledDays:r=[],firstDayOfWeek:i=0,fullDateFormat:o,locale:s="en-US",max:l,min:d,showWeekNumber:c=!1,weekLabel:u="Week",weekNumberType:h="first-4-day-week"}=e||{},m=$(i),f=t.getUTCFullYear(),p=t.getUTCMonth(),y=_(f,p,1),g=new Set(r.map((e=>E(e,m,c)))),w=new Set(n.map((e=>+e))),b=[y.toJSON(),m,s,null==l?"":l.toJSON(),null==d?"":d.toJSON(),Array.from(g).join(","),Array.from(w).join(","),h].filter(Boolean).join(":"),v=E(y.getUTCDay(),m,c),k=null==d?+new Date("2000-01-01"):+d,D=null==l?+new Date("2100-12-31"):+l,x=c?8:7,M=_(f,1+p,0).getUTCDate(),T=[];let C=[],S=!1,W=1;for(const F of[0,1,2,3,4,5]){for(const e of[0,1,2,3,4,5,6].concat(7===x?[]:[7])){const t=e+F*x;if(!S&&c&&0===e){const e=P(h,_(f,p,W-(F<1?m:0))),t=`${u} ${e}`;C.push({fullDate:null,label:t,value:`${e}`,key:`${b}:${t}`,disabled:!0});continue}if(S||t<v){C.push({fullDate:null,label:"",value:"",key:`${b}:${t}`,disabled:!0});continue}const n=_(f,p,W),r=+n,i=g.has(e)||w.has(r)||r<k||r>D;i&&w.add(r),C.push({fullDate:n,label:o(n),value:a(n),key:`${b}:${n.toJSON()}`,disabled:i}),W+=1,W>M&&(S=!0)}T.push(C),C=[]}return{disabledDatesSet:w,calendar:T,disabledDaysSet:new Set(r.map((e=>$(e)))),key:b}}({dayFormat:t,fullDateFormat:a,locale:n,disabledDates:s,disabledDays:l,firstDayOfWeek:d,max:c,min:u,showWeekNumber:h,weekLabel:m,weekNumberType:f,date:r});return{...g,key:o}})),D=[],x=new Set,M=new Set;for(const _ of k){const{disabledDatesSet:e,disabledDaysSet:t,...a}=_;if(a.calendar.length>0){if(t.size>0)for(const e of t)M.add(e);if(e.size>0)for(const t of e)x.add(t)}D.push(a)}return{calendars:D,weekdays:g,disabledDatesSet:x,disabledDaysSet:M,key:w(o)}}function L(e){const t=null==e?new Date:new Date(e),a="string"==typeof e&&(/^\d{4}-\d{2}-\d{2}$/i.test(e)||/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}(Z|\+00:00|-00:00)$/i.test(e)),n="number"==typeof e&&e>0&&isFinite(e);let r=t.getFullYear(),i=t.getMonth(),o=t.getDate();return(a||n)&&(r=t.getUTCFullYear(),i=t.getUTCMonth(),o=t.getUTCDate()),_(r,i,o)}function U(e,t){return e.classList.contains(t)}function q(e,t){return!(null==e||!(t instanceof Date)||isNaN(+t))}function O(e){return e-Math.floor(e)>0?+e.toFixed(3):e}function A(e){return{passive:!0,handleEvent:e}}function H(e,t){const a="string"==typeof e&&e.length>0?e.split(/,\s*/i):[];return a.length?"function"==typeof t?a.map(t):a:[]}function z(e){if(e instanceof Date&&!isNaN(+e)){const t=e.toJSON();return null==t?"":t.replace(/^(.+)T.+/i,"$1")}return""}function j(e,t){if(T(e,t)<864e5)return[];const a=e.getUTCFullYear();return Array.from(Array(t.getUTCFullYear()-a+1),((e,t)=>t+a))}function V(e,t,a){const n="number"==typeof e?e:+e,r=+t,i=+a;return n<r?r:n>i?i:e}var Z,B,X=a(6029);function G(e){const{clientX:t,clientY:a,pageX:n,pageY:r}=e,i=Math.max(n,t),o=Math.max(r,a),s=e.identifier||e.pointerId;return{x:i,y:o,id:null==s?0:s}}function I(e,t){const a=t.changedTouches;if(null==a)return{newPointer:G(t),oldPointer:e};const n=Array.from(a,(e=>G(e)));return{newPointer:null==e?n[0]:n.find((t=>t.id===e.id)),oldPointer:e}}function Q(e,t,a){e.addEventListener(t,a,!!X.QQ&&{passive:!0})}class J{constructor(e,t){this._element=e,this._startPointer=null;const{down:a,move:n,up:r}=t;this._down=this._onDown(a),this._move=this._onMove(n),this._up=this._onUp(r),e&&e.addEventListener&&(e.addEventListener("mousedown",this._down),Q(e,"touchstart",this._down),Q(e,"touchmove",this._move),Q(e,"touchend",this._up))}disconnect(){const e=this._element;e&&e.removeEventListener&&(e.removeEventListener("mousedown",this._down),e.removeEventListener("touchstart",this._down),e.removeEventListener("touchmove",this._move),e.removeEventListener("touchend",this._up))}_onDown(e){return t=>{t instanceof MouseEvent&&(this._element.addEventListener("mousemove",this._move),this._element.addEventListener("mouseup",this._up),this._element.addEventListener("mouseleave",this._up));const{newPointer:a}=I(this._startPointer,t);e(a,t),this._startPointer=a}}_onMove(e){return t=>{this._updatePointers(e,t)}}_onUp(e){return t=>{this._updatePointers(e,t,!0)}}_updatePointers(e,t,a){a&&t instanceof MouseEvent&&(this._element.removeEventListener("mousemove",this._move),this._element.removeEventListener("mouseup",this._up),this._element.removeEventListener("mouseleave",this._up));const{newPointer:n,oldPointer:r}=I(this._startPointer,t);e(n,r,t),this._startPointer=a?null:n}}class K extends h.WF{constructor(){super(),this.firstDayOfWeek=0,this.showWeekNumber=!1,this.weekNumberType="first-4-day-week",this.landscape=!1,this.locale=n&&n().resolvedOptions&&n().resolvedOptions().locale||"en-US",this.disabledDays="",this.disabledDates="",this.weekLabel="Wk",this.inline=!1,this.dragRatio=.15,this._hasMin=!1,this._hasMax=!1,this._disabledDaysSet=new Set,this._disabledDatesSet=new Set,this._dx=-1/0,this._hasNativeWebAnimation="animate"in HTMLElement.prototype,this._updatingDateWithKey=!1;const e=L(),t=N(this.locale),a=z(e),r=L("2100-12-31");this.value=a,this.startView="calendar",this._min=new Date(e),this._max=new Date(r),this._todayDate=e,this._maxDate=r,this._yearList=j(e,r),this._selectedDate=new Date(e),this._focusedDate=new Date(e),this._formatters=t}get startView(){return this._startView}set startView(e){const t=e||"calendar";if("calendar"!==t&&"yearList"!==t)return;const a=this._startView;this._startView=t,this.requestUpdate("startView",a)}get min(){return this._hasMin?z(this._min):""}set min(e){const t=L(e),a=q(e,t);this._min=a?t:this._todayDate,this._hasMin=a,this.requestUpdate("min")}get max(){return this._hasMax?z(this._max):""}set max(e){const t=L(e),a=q(e,t);this._max=a?t:this._maxDate,this._hasMax=a,this.requestUpdate("max")}get value(){return z(this._focusedDate)}set value(e){const t=L(e),a=q(e,t)?t:this._todayDate;this._focusedDate=new Date(a),this._selectedDate=this._lastSelectedDate=new Date(a)}disconnectedCallback(){super.disconnectedCallback(),this._tracker&&(this._tracker.disconnect(),this._tracker=void 0)}render(){this._formatters.locale!==this.locale&&(this._formatters=N(this.locale));const e="yearList"===this._startView?this._renderDatepickerYearList():this._renderDatepickerCalendar(),t=this.inline?null:h.qy`<div class="datepicker-header" part="header">${this._renderHeaderSelectorButton()}</div>`;return h.qy`
    ${t}
    <div class="datepicker-body" part="body">${w(e)}</div>
    `}firstUpdated(){let e;e="calendar"===this._startView?this.inline?this.shadowRoot.querySelector(".btn__month-selector"):this._buttonSelectorYear:this._yearViewListItem,S(this,"datepicker-first-updated",{firstFocusableElement:e,value:this.value})}async updated(e){const t=this._startView;if(e.has("min")||e.has("max")){this._yearList=j(this._min,this._max),"yearList"===t&&this.requestUpdate();const e=+this._min,a=+this._max;if(T(e,a)>864e5){const t=+this._focusedDate;let n=t;t<e&&(n=e),t>a&&(n=a),this.value=z(new Date(n))}}if(e.has("_startView")||e.has("startView")){if("yearList"===t){const e=48*(this._selectedDate.getUTCFullYear()-this._min.getUTCFullYear()-2);!function(e,t){if(null==e.scrollTo){const{top:a,left:n}=t||{};e.scrollTop=a||0,e.scrollLeft=n||0}else e.scrollTo(t)}(this._yearViewFullList,{top:e,left:0})}if("calendar"===t&&null==this._tracker){const e=this.calendarsContainer;let t=!1,a=!1,n=!1;if(e){const r={down:()=>{n||(t=!0,this._dx=0)},move:(r,i)=>{if(n||!t)return;const o=this._dx,s=o<0&&U(e,"has-max-date")||o>0&&U(e,"has-min-date");!s&&Math.abs(o)>0&&t&&(a=!0,e.style.transform=`translateX(${O(o)}px)`),this._dx=s?0:o+(r.x-i.x)},up:async(r,i,o)=>{if(t&&a){const r=this._dx,i=e.getBoundingClientRect().width/3,o=Math.abs(r)>Number(this.dragRatio)*i,s=350,l="cubic-bezier(0, 0, .4, 1)",d=o?O(i*(r<0?-1:1)):0;n=!0,await async function(e,t){const{hasNativeWebAnimation:a=!1,keyframes:n=[],options:r={duration:100}}=t||{};if(Array.isArray(n)&&n.length)return new Promise((t=>{if(a)e.animate(n,r).onfinish=()=>t();else{const[,a]=n||[],i=()=>{e.removeEventListener("transitionend",i),t()};e.addEventListener("transitionend",i),e.style.transitionDuration=`${r.duration}ms`,r.easing&&(e.style.transitionTimingFunction=r.easing),Object.keys(a).forEach((t=>{t&&(e.style[t]=a[t])}))}}))}(e,{hasNativeWebAnimation:this._hasNativeWebAnimation,keyframes:[{transform:`translateX(${r}px)`},{transform:`translateX(${d}px)`}],options:{duration:s,easing:l}}),o&&this._updateMonth(r<0?"next":"previous").handleEvent(),t=a=n=!1,this._dx=-1/0,e.removeAttribute("style"),S(this,"datepicker-animation-finished")}else t&&(this._updateFocusedDate(o),t=a=!1,this._dx=-1/0)}};this._tracker=new J(e,r)}}e.get("_startView")&&"calendar"===t&&this._focusElement('[part="year-selector"]')}this._updatingDateWithKey&&(this._focusElement('[part="calendars"]:nth-of-type(2) .day--focused'),this._updatingDateWithKey=!1)}_focusElement(e){const t=this.shadowRoot.querySelector(e);t&&t.focus()}_renderHeaderSelectorButton(){const{yearFormat:e,dateFormat:t}=this._formatters,a="calendar"===this.startView,n=this._focusedDate,r=t(n),i=e(n);return h.qy`
    <button
      class="${(0,b.H)({"btn__year-selector":!0,selected:!a})}"
      type="button"
      part="year-selector"
      data-view="${"yearList"}"
      @click="${this._updateView("yearList")}">${i}</button>

    <div class="datepicker-toolbar" part="toolbar">
      <button
        class="${(0,b.H)({"btn__calendar-selector":!0,selected:a})}"
        type="button"
        part="calendar-selector"
        data-view="${"calendar"}"
        @click="${this._updateView("calendar")}">${r}</button>
    </div>
    `}_renderDatepickerYearList(){const{yearFormat:e}=this._formatters,t=this._focusedDate.getUTCFullYear();return h.qy`
    <div class="datepicker-body__year-list-view" part="year-list-view">
      <div class="year-list-view__full-list" part="year-list" @click="${this._updateYear}">
      ${this._yearList.map((a=>h.qy`<button
        class="${(0,b.H)({"year-list-view__list-item":!0,"year--selected":t===a})}"
        type="button"
        part="year"
        .year="${a}">${e(_(a,0,1))}</button>`))}</div>
    </div>
    `}_renderDatepickerCalendar(){const{longMonthYearFormat:e,dayFormat:t,fullDateFormat:a,longWeekdayFormat:n,narrowWeekdayFormat:r}=this._formatters,i=H(this.disabledDays,Number),o=H(this.disabledDates,L),s=this.showWeekNumber,l=this._focusedDate,d=this.firstDayOfWeek,c=L(),u=this._selectedDate,m=this._max,f=this._min,{calendars:p,disabledDaysSet:y,disabledDatesSet:g,weekdays:w}=Y({dayFormat:t,fullDateFormat:a,longWeekdayFormat:n,narrowWeekdayFormat:r,firstDayOfWeek:d,disabledDays:i,disabledDates:o,locale:this.locale,selectedDate:u,showWeekNumber:this.showWeekNumber,weekNumberType:this.weekNumberType,max:m,min:f,weekLabel:this.weekLabel}),_=!p[0].calendar.length,x=!p[2].calendar.length,M=w.map((e=>h.qy`<th
        class="calendar-weekday"
        part="calendar-weekday"
        role="columnheader"
        aria-label="${e.label}"
      >
        <div class="weekday" part="weekday">${e.value}</div>
      </th>`)),T=(0,v.u)(p,(e=>e.key),(({calendar:t},a)=>{if(!t.length)return h.qy`<div class="calendar-container" part="calendar"></div>`;const n=`calendarcaption${a}`,r=t[1][1].fullDate,i=1===a,o=i&&!this._isInVisibleMonth(l,u)?C({disabledDaysSet:y,disabledDatesSet:g,hasAltKey:!1,keyCode:36,focusedDate:l,selectedDate:u,minTime:+f,maxTime:+m}):l;return h.qy`
      <div class="calendar-container" part="calendar">
        <table class="calendar-table" part="table" role="grid" aria-labelledby="${n}">
          <caption id="${n}">
            <div class="calendar-label" part="label">${r?e(r):""}</div>
          </caption>

          <thead role="rowgroup">
            <tr class="calendar-weekdays" part="weekdays" role="row">${M}</tr>
          </thead>

          <tbody role="rowgroup">${t.map((e=>h.qy`<tr role="row">${e.map(((e,t)=>{const{disabled:a,fullDate:n,label:r,value:d}=e;if(!n&&d&&s&&t<1)return h.qy`<th
                      class="full-calendar__day weekday-label"
                      part="calendar-day"
                      scope="row"
                      role="rowheader"
                      abbr="${r}"
                      aria-label="${r}"
                    >${d}</th>`;if(!d||!n)return h.qy`<td class="full-calendar__day day--empty" part="calendar-day"></td>`;const u=+new Date(n),m=+l===u,f=i&&o.getUTCDate()===Number(d);return h.qy`
                  <td
                    tabindex="${f?"0":"-1"}"
                    class="${(0,b.H)({"full-calendar__day":!0,"day--disabled":a,"day--today":+c===u,"day--focused":!a&&m})}"
                    part="calendar-day${+c===u?" calendar-today":""}"
                    role="gridcell"
                    aria-disabled="${a?"true":"false"}"
                    aria-label="${r}"
                    aria-selected="${m?"true":"false"}"
                    .fullDate="${n}"
                    .day="${d}"
                  >
                    <div
                      class="calendar-day"
                      part="day${+c===u?" today":""}"
                    >${d}</div>
                  </td>
                  `}))}</tr>`))}</tbody>
        </table>
      </div>
      `}));return this._disabledDatesSet=g,this._disabledDaysSet=y,h.qy`
    <div class="datepicker-body__calendar-view" part="calendar-view">
      <div class="calendar-view__month-selector" part="month-selectors">
        <div class="month-selector-container">${_?null:h.qy`
          <button
            class="btn__month-selector"
            type="button"
            part="month-selector"
            aria-label="Previous month"
            @click="${this._updateMonth("previous")}"
          >${k}</button>
        `}</div>

        <div class="month-selector-container">${x?null:h.qy`
          <button
            class="btn__month-selector"
            type="button"
            part="month-selector"
            aria-label="Next month"
            @click="${this._updateMonth("next")}"
          >${D}</button>
        `}</div>
      </div>

      <div
        class="${(0,b.H)({"calendars-container":!0,"has-min-date":_,"has-max-date":x})}"
        part="calendars"
        @keyup="${this._updateFocusedDateWithKeyboard}"
      >${T}</div>
    </div>
    `}_updateView(e){return A((()=>{"calendar"===e&&(this._selectedDate=this._lastSelectedDate=new Date(V(this._focusedDate,this._min,this._max))),this._startView=e}))}_updateMonth(e){return A((()=>{if(null==this.calendarsContainer)return this.updateComplete;const t=this._lastSelectedDate||this._selectedDate,a=this._min,n=this._max,r="previous"===e,i=_(t.getUTCFullYear(),t.getUTCMonth()+(r?-1:1),1),o=i.getUTCFullYear(),s=i.getUTCMonth(),l=a.getUTCFullYear(),d=a.getUTCMonth(),c=n.getUTCFullYear(),u=n.getUTCMonth();return o<l||o<=l&&s<d||(o>c||o>=c&&s>u)||(this._lastSelectedDate=i,this._selectedDate=this._lastSelectedDate),this.updateComplete}))}_updateYear(e){const t=W(e,(e=>U(e,"year-list-view__list-item")));if(null==t)return;const a=V(new Date(this._focusedDate).setUTCFullYear(+t.year),this._min,this._max);this._selectedDate=this._lastSelectedDate=new Date(a),this._focusedDate=new Date(a),this._startView="calendar"}_updateFocusedDate(e){const t=W(e,(e=>U(e,"full-calendar__day")));null==t||["day--empty","day--disabled","day--focused","weekday-label"].some((e=>U(t,e)))||(this._focusedDate=new Date(t.fullDate),S(this,"datepicker-value-updated",{isKeypress:!1,value:this.value}))}_updateFocusedDateWithKeyboard(e){const t=e.keyCode;if(13===t||32===t)return S(this,"datepicker-value-updated",{keyCode:t,isKeypress:!0,value:this.value}),void(this._focusedDate=new Date(this._selectedDate));if(9===t||!c.has(t))return;const a=this._selectedDate,n=C({keyCode:t,selectedDate:a,disabledDatesSet:this._disabledDatesSet,disabledDaysSet:this._disabledDaysSet,focusedDate:this._focusedDate,hasAltKey:e.altKey,maxTime:+this._max,minTime:+this._min});this._isInVisibleMonth(n,a)||(this._selectedDate=this._lastSelectedDate=n),this._focusedDate=n,this._updatingDateWithKey=!0,S(this,"datepicker-value-updated",{keyCode:t,isKeypress:!0,value:this.value})}_isInVisibleMonth(e,t){const a=e.getUTCFullYear(),n=e.getUTCMonth(),r=t.getUTCFullYear(),i=t.getUTCMonth();return a===r&&n===i}get calendarsContainer(){return this.shadowRoot.querySelector(".calendars-container")}}K.styles=[M,x,h.AH`
    :host {
      width: 312px;
      /** NOTE: Magic number as 16:9 aspect ratio does not look good */
      /* height: calc((var(--app-datepicker-width) / .66) - var(--app-datepicker-footer-height, 56px)); */
      background-color: var(--app-datepicker-bg-color, #fff);
      color: var(--app-datepicker-color, #000);
      border-radius:
        var(--app-datepicker-border-top-left-radius, 0)
        var(--app-datepicker-border-top-right-radius, 0)
        var(--app-datepicker-border-bottom-right-radius, 0)
        var(--app-datepicker-border-bottom-left-radius, 0);
      contain: content;
      overflow: hidden;
    }
    :host([landscape]) {
      display: flex;

      /** <iphone-5-landscape-width> - <standard-side-margin-width> */
      min-width: calc(568px - 16px * 2);
      width: calc(568px - 16px * 2);
    }

    .datepicker-header + .datepicker-body {
      border-top: 1px solid var(--app-datepicker-separator-color, #ddd);
    }
    :host([landscape]) > .datepicker-header + .datepicker-body {
      border-top: none;
      border-left: 1px solid var(--app-datepicker-separator-color, #ddd);
    }

    .datepicker-header {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      position: relative;
      padding: 16px 24px;
    }
    :host([landscape]) > .datepicker-header {
      /** :this.<one-liner-month-day-width> + :this.<side-padding-width> */
      min-width: calc(14ch + 24px * 2);
    }

    .btn__year-selector,
    .btn__calendar-selector {
      color: var(--app-datepicker-selector-color, rgba(0, 0, 0, .55));
      cursor: pointer;
      /* outline: none; */
    }
    .btn__year-selector.selected,
    .btn__calendar-selector.selected {
      color: currentColor;
    }

    /**
      * NOTE: IE11-only fix. This prevents formatted focused date from overflowing the container.
      */
    .datepicker-toolbar {
      width: 100%;
    }

    .btn__year-selector {
      font-size: 16px;
      font-weight: 700;
    }
    .btn__calendar-selector {
      font-size: 36px;
      font-weight: 700;
      line-height: 1;
    }

    .datepicker-body {
      position: relative;
      width: 100%;
      overflow: hidden;
    }

    .datepicker-body__calendar-view {
      min-height: 56px;
    }

    .calendar-view__month-selector {
      display: flex;
      align-items: center;

      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      padding: 0 8px;
      z-index: 1;
    }

    .month-selector-container {
      max-height: 56px;
      height: 100%;
    }
    .month-selector-container + .month-selector-container {
      margin: 0 0 0 auto;
    }

    .btn__month-selector {
      padding: calc((56px - 24px) / 2);
      /**
        * NOTE: button element contains no text, only SVG.
        * No extra height will incur with such setting.
        */
      line-height: 0;
    }
    .btn__month-selector > svg {
      fill: currentColor;
    }

    .calendars-container {
      display: flex;
      justify-content: center;

      position: relative;
      top: 0;
      left: calc(-100%);
      width: calc(100% * 3);
      transform: translateZ(0);
      will-change: transform;
      /**
        * NOTE: Required for Pointer Events API to work on touch devices.
        * Native \`pan-y\` action will be fired by the browsers since we only care about the
        * horizontal direction. This is great as vertical scrolling still works even when touch
        * event happens on a datepicker's calendar.
        */
      touch-action: pan-y;
      /* outline: none; */
    }

    .year-list-view__full-list {
      max-height: calc(48px * 7);
      overflow-y: auto;

      scrollbar-color: var(--app-datepicker-scrollbar-thumb-bg-color, rgba(0, 0, 0, .35)) rgba(0, 0, 0, 0);
      scrollbar-width: thin;
    }
    .year-list-view__full-list::-webkit-scrollbar {
      width: 8px;
      background-color: rgba(0, 0, 0, 0);
    }
    .year-list-view__full-list::-webkit-scrollbar-thumb {
      background-color: var(--app-datepicker-scrollbar-thumb-bg-color, rgba(0, 0, 0, .35));
      border-radius: 50px;
    }
    .year-list-view__full-list::-webkit-scrollbar-thumb:hover {
      background-color: var(--app-datepicker-scrollbar-thumb-hover-bg-color, rgba(0, 0, 0, .5));
    }

    .calendar-weekdays > th,
    .weekday-label {
      color: var(--app-datepicker-weekday-color, rgba(0, 0, 0, .55));
      font-weight: 400;
      transform: translateZ(0);
      will-change: transform;
    }

    .calendar-container,
    .calendar-label,
    .calendar-table {
      width: 100%;
    }

    .calendar-container {
      position: relative;
      padding: 0 16px 16px;
    }

    .calendar-table {
      -moz-user-select: none;
      -webkit-user-select: none;
      user-select: none;

      border-collapse: collapse;
      border-spacing: 0;
      text-align: center;
    }

    .calendar-label {
      display: flex;
      align-items: center;
      justify-content: center;

      height: 56px;
      font-weight: 500;
      text-align: center;
    }

    .calendar-weekday,
    .full-calendar__day {
      position: relative;
      width: calc(100% / 7);
      height: 0;
      padding: calc(100% / 7 / 2) 0;
      outline: none;
      text-align: center;
    }
    .full-calendar__day:not(.day--disabled):focus {
      outline: #000 dotted 1px;
      outline: -webkit-focus-ring-color auto 1px;
    }
    :host([showweeknumber]) .calendar-weekday,
    :host([showweeknumber]) .full-calendar__day {
      width: calc(100% / 8);
      padding-top: calc(100% / 8);
      padding-bottom: 0;
    }
    :host([showweeknumber]) th.weekday-label {
      padding: 0;
    }

    /**
      * NOTE: Interesting fact! That is ::after will trigger paint when dragging. This will trigger
      * layout and paint on **ONLY** affected nodes. This is much cheaper as compared to rendering
      * all :::after of all calendar day elements. When dragging the entire calendar container,
      * because of all layout and paint trigger on each and every ::after, this becomes a expensive
      * task for the browsers especially on low-end devices. Even though animating opacity is much
      * cheaper, the technique does not work here. Adding 'will-change' will further reduce overall
      * painting at the expense of memory consumption as many cells in a table has been promoted
      * a its own layer.
      */
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.weekday-label) {
      transform: translateZ(0);
      will-change: transform;
    }
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.weekday-label).day--focused::after,
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.day--focused):not(.weekday-label):hover::after {
      content: '';
      display: block;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: var(--app-datepicker-accent-color, #1a73e8);
      border-radius: 50%;
      opacity: 0;
      pointer-events: none;
    }
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.weekday-label) {
      cursor: pointer;
      pointer-events: auto;
      -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    }
    .full-calendar__day.day--focused:not(.day--empty):not(.day--disabled):not(.weekday-label)::after,
    .full-calendar__day.day--today.day--focused:not(.day--empty):not(.day--disabled):not(.weekday-label)::after {
      opacity: 1;
    }

    .calendar-weekday > .weekday,
    .full-calendar__day > .calendar-day {
      display: flex;
      align-items: center;
      justify-content: center;

      position: absolute;
      top: 5%;
      left: 5%;
      width: 90%;
      height: 90%;
      color: currentColor;
      font-size: 14px;
      pointer-events: none;
      z-index: 1;
    }
    .full-calendar__day.day--today {
      color: var(--app-datepicker-accent-color, #1a73e8);
    }
    .full-calendar__day.day--focused,
    .full-calendar__day.day--today.day--focused {
      color: var(--app-datepicker-focused-day-color, #fff);
    }
    .full-calendar__day.day--empty,
    .full-calendar__day.weekday-label,
    .full-calendar__day.day--disabled > .calendar-day {
      pointer-events: none;
    }
    .full-calendar__day.day--disabled:not(.day--today) {
      color: var(--app-datepicker-disabled-day-color, rgba(0, 0, 0, .55));
    }

    .year-list-view__list-item {
      position: relative;
      width: 100%;
      padding: 12px 16px;
      text-align: center;
      /** NOTE: Reduce paint when hovering and scrolling, but this increases memory usage */
      /* will-change: opacity; */
      /* outline: none; */
    }
    .year-list-view__list-item::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: var(--app-datepicker-focused-year-bg-color, #000);
      opacity: 0;
      pointer-events: none;
    }
    .year-list-view__list-item:focus::after {
      opacity: .05;
    }
    .year-list-view__list-item.year--selected {
      color: var(--app-datepicker-accent-color, #1a73e8);
      font-size: 24px;
      font-weight: 500;
    }

    @media (any-hover: hover) {
      .btn__month-selector:hover,
      .year-list-view__list-item:hover {
        cursor: pointer;
      }
      .full-calendar__day:not(.day--empty):not(.day--disabled):not(.day--focused):not(.weekday-label):hover::after {
        opacity: .15;
      }
      .year-list-view__list-item:hover::after {
        opacity: .05;
      }
    }

    @supports (background: -webkit-canvas(squares)) {
      .calendar-container {
        padding: 56px 16px 16px;
      }

      table > caption {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translate3d(-50%, 0, 0);
        will-change: transform;
      }
    }
    `],(0,u.Cg)([(0,m.MZ)({type:Number,reflect:!0})],K.prototype,"firstDayOfWeek",void 0),(0,u.Cg)([(0,m.MZ)({type:Boolean,reflect:!0})],K.prototype,"showWeekNumber",void 0),(0,u.Cg)([(0,m.MZ)({type:String,reflect:!0})],K.prototype,"weekNumberType",void 0),(0,u.Cg)([(0,m.MZ)({type:Boolean,reflect:!0})],K.prototype,"landscape",void 0),(0,u.Cg)([(0,m.MZ)({type:String,reflect:!0})],K.prototype,"startView",null),(0,u.Cg)([(0,m.MZ)({type:String,reflect:!0})],K.prototype,"min",null),(0,u.Cg)([(0,m.MZ)({type:String,reflect:!0})],K.prototype,"max",null),(0,u.Cg)([(0,m.MZ)({type:String})],K.prototype,"value",null),(0,u.Cg)([(0,m.MZ)({type:String})],K.prototype,"locale",void 0),(0,u.Cg)([(0,m.MZ)({type:String})],K.prototype,"disabledDays",void 0),(0,u.Cg)([(0,m.MZ)({type:String})],K.prototype,"disabledDates",void 0),(0,u.Cg)([(0,m.MZ)({type:String})],K.prototype,"weekLabel",void 0),(0,u.Cg)([(0,m.MZ)({type:Boolean})],K.prototype,"inline",void 0),(0,u.Cg)([(0,m.MZ)({type:Number})],K.prototype,"dragRatio",void 0),(0,u.Cg)([(0,m.MZ)({type:Date,attribute:!1})],K.prototype,"_selectedDate",void 0),(0,u.Cg)([(0,m.MZ)({type:Date,attribute:!1})],K.prototype,"_focusedDate",void 0),(0,u.Cg)([(0,m.MZ)({type:String,attribute:!1})],K.prototype,"_startView",void 0),(0,u.Cg)([(0,m.P)(".year-list-view__full-list")],K.prototype,"_yearViewFullList",void 0),(0,u.Cg)([(0,m.P)(".btn__year-selector")],K.prototype,"_buttonSelectorYear",void 0),(0,u.Cg)([(0,m.P)(".year-list-view__list-item")],K.prototype,"_yearViewListItem",void 0),(0,u.Cg)([(0,m.Ls)({passive:!0})],K.prototype,"_updateYear",null),(0,u.Cg)([(0,m.Ls)({passive:!0})],K.prototype,"_updateFocusedDateWithKeyboard",null),Z="app-datepicker",B=K,window.customElements&&!window.customElements.get(Z)&&window.customElements.define(Z,B)},6913:(e,t,a)=>{a.d(t,{q:()=>r});let n={};function r(){return n}},9518:(e,t,a)=>{a.d(t,{my:()=>n,w4:()=>r});Math.pow(10,8);const n=6048e5,r=864e5},6174:(e,t,a)=>{function n(e,t){return e instanceof Date?new e.constructor(t):new Date(t)}a.d(t,{w:()=>n})},4006:(e,t,a)=>{a.d(t,{m:()=>s});var n=a(9518),r=a(3352),i=a(4396);function o(e){const t=(0,i.a)(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return a.setUTCFullYear(t.getFullYear()),+e-+a}function s(e,t){const a=(0,r.o)(e),i=(0,r.o)(t),s=+a-o(a),l=+i-o(i);return Math.round((s-l)/n.w4)}},5286:(e,t,a)=>{a.d(t,{GP:()=>J});const n={lessThanXSeconds:{one:"less than a second",other:"less than {{count}} seconds"},xSeconds:{one:"1 second",other:"{{count}} seconds"},halfAMinute:"half a minute",lessThanXMinutes:{one:"less than a minute",other:"less than {{count}} minutes"},xMinutes:{one:"1 minute",other:"{{count}} minutes"},aboutXHours:{one:"about 1 hour",other:"about {{count}} hours"},xHours:{one:"1 hour",other:"{{count}} hours"},xDays:{one:"1 day",other:"{{count}} days"},aboutXWeeks:{one:"about 1 week",other:"about {{count}} weeks"},xWeeks:{one:"1 week",other:"{{count}} weeks"},aboutXMonths:{one:"about 1 month",other:"about {{count}} months"},xMonths:{one:"1 month",other:"{{count}} months"},aboutXYears:{one:"about 1 year",other:"about {{count}} years"},xYears:{one:"1 year",other:"{{count}} years"},overXYears:{one:"over 1 year",other:"over {{count}} years"},almostXYears:{one:"almost 1 year",other:"almost {{count}} years"}};function r(e){return(t={})=>{const a=t.width?String(t.width):e.defaultWidth;return e.formats[a]||e.formats[e.defaultWidth]}}const i={date:r({formats:{full:"EEEE, MMMM do, y",long:"MMMM do, y",medium:"MMM d, y",short:"MM/dd/yyyy"},defaultWidth:"full"}),time:r({formats:{full:"h:mm:ss a zzzz",long:"h:mm:ss a z",medium:"h:mm:ss a",short:"h:mm a"},defaultWidth:"full"}),dateTime:r({formats:{full:"{{date}} 'at' {{time}}",long:"{{date}} 'at' {{time}}",medium:"{{date}}, {{time}}",short:"{{date}}, {{time}}"},defaultWidth:"full"})},o={lastWeek:"'last' eeee 'at' p",yesterday:"'yesterday at' p",today:"'today at' p",tomorrow:"'tomorrow at' p",nextWeek:"eeee 'at' p",other:"P"};function s(e){return(t,a)=>{let n;if("formatting"===(a?.context?String(a.context):"standalone")&&e.formattingValues){const t=e.defaultFormattingWidth||e.defaultWidth,r=a?.width?String(a.width):t;n=e.formattingValues[r]||e.formattingValues[t]}else{const t=e.defaultWidth,r=a?.width?String(a.width):e.defaultWidth;n=e.values[r]||e.values[t]}return n[e.argumentCallback?e.argumentCallback(t):t]}}function l(e){return(t,a={})=>{const n=a.width,r=n&&e.matchPatterns[n]||e.matchPatterns[e.defaultMatchWidth],i=t.match(r);if(!i)return null;const o=i[0],s=n&&e.parsePatterns[n]||e.parsePatterns[e.defaultParseWidth],l=Array.isArray(s)?function(e,t){for(let a=0;a<e.length;a++)if(t(e[a]))return a;return}(s,(e=>e.test(o))):function(e,t){for(const a in e)if(Object.prototype.hasOwnProperty.call(e,a)&&t(e[a]))return a;return}(s,(e=>e.test(o)));let d;d=e.valueCallback?e.valueCallback(l):l,d=a.valueCallback?a.valueCallback(d):d;return{value:d,rest:t.slice(o.length)}}}var d;const c={code:"en-US",formatDistance:(e,t,a)=>{let r;const i=n[e];return r="string"==typeof i?i:1===t?i.one:i.other.replace("{{count}}",t.toString()),a?.addSuffix?a.comparison&&a.comparison>0?"in "+r:r+" ago":r},formatLong:i,formatRelative:(e,t,a,n)=>o[e],localize:{ordinalNumber:(e,t)=>{const a=Number(e),n=a%100;if(n>20||n<10)switch(n%10){case 1:return a+"st";case 2:return a+"nd";case 3:return a+"rd"}return a+"th"},era:s({values:{narrow:["B","A"],abbreviated:["BC","AD"],wide:["Before Christ","Anno Domini"]},defaultWidth:"wide"}),quarter:s({values:{narrow:["1","2","3","4"],abbreviated:["Q1","Q2","Q3","Q4"],wide:["1st quarter","2nd quarter","3rd quarter","4th quarter"]},defaultWidth:"wide",argumentCallback:e=>e-1}),month:s({values:{narrow:["J","F","M","A","M","J","J","A","S","O","N","D"],abbreviated:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],wide:["January","February","March","April","May","June","July","August","September","October","November","December"]},defaultWidth:"wide"}),day:s({values:{narrow:["S","M","T","W","T","F","S"],short:["Su","Mo","Tu","We","Th","Fr","Sa"],abbreviated:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"],wide:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]},defaultWidth:"wide"}),dayPeriod:s({values:{narrow:{am:"a",pm:"p",midnight:"mi",noon:"n",morning:"morning",afternoon:"afternoon",evening:"evening",night:"night"},abbreviated:{am:"AM",pm:"PM",midnight:"midnight",noon:"noon",morning:"morning",afternoon:"afternoon",evening:"evening",night:"night"},wide:{am:"a.m.",pm:"p.m.",midnight:"midnight",noon:"noon",morning:"morning",afternoon:"afternoon",evening:"evening",night:"night"}},defaultWidth:"wide",formattingValues:{narrow:{am:"a",pm:"p",midnight:"mi",noon:"n",morning:"in the morning",afternoon:"in the afternoon",evening:"in the evening",night:"at night"},abbreviated:{am:"AM",pm:"PM",midnight:"midnight",noon:"noon",morning:"in the morning",afternoon:"in the afternoon",evening:"in the evening",night:"at night"},wide:{am:"a.m.",pm:"p.m.",midnight:"midnight",noon:"noon",morning:"in the morning",afternoon:"in the afternoon",evening:"in the evening",night:"at night"}},defaultFormattingWidth:"wide"})},match:{ordinalNumber:(d={matchPattern:/^(\d+)(th|st|nd|rd)?/i,parsePattern:/\d+/i,valueCallback:e=>parseInt(e,10)},(e,t={})=>{const a=e.match(d.matchPattern);if(!a)return null;const n=a[0],r=e.match(d.parsePattern);if(!r)return null;let i=d.valueCallback?d.valueCallback(r[0]):r[0];return i=t.valueCallback?t.valueCallback(i):i,{value:i,rest:e.slice(n.length)}}),era:l({matchPatterns:{narrow:/^(b|a)/i,abbreviated:/^(b\.?\s?c\.?|b\.?\s?c\.?\s?e\.?|a\.?\s?d\.?|c\.?\s?e\.?)/i,wide:/^(before christ|before common era|anno domini|common era)/i},defaultMatchWidth:"wide",parsePatterns:{any:[/^b/i,/^(a|c)/i]},defaultParseWidth:"any"}),quarter:l({matchPatterns:{narrow:/^[1234]/i,abbreviated:/^q[1234]/i,wide:/^[1234](th|st|nd|rd)? quarter/i},defaultMatchWidth:"wide",parsePatterns:{any:[/1/i,/2/i,/3/i,/4/i]},defaultParseWidth:"any",valueCallback:e=>e+1}),month:l({matchPatterns:{narrow:/^[jfmasond]/i,abbreviated:/^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)/i,wide:/^(january|february|march|april|may|june|july|august|september|october|november|december)/i},defaultMatchWidth:"wide",parsePatterns:{narrow:[/^j/i,/^f/i,/^m/i,/^a/i,/^m/i,/^j/i,/^j/i,/^a/i,/^s/i,/^o/i,/^n/i,/^d/i],any:[/^ja/i,/^f/i,/^mar/i,/^ap/i,/^may/i,/^jun/i,/^jul/i,/^au/i,/^s/i,/^o/i,/^n/i,/^d/i]},defaultParseWidth:"any"}),day:l({matchPatterns:{narrow:/^[smtwf]/i,short:/^(su|mo|tu|we|th|fr|sa)/i,abbreviated:/^(sun|mon|tue|wed|thu|fri|sat)/i,wide:/^(sunday|monday|tuesday|wednesday|thursday|friday|saturday)/i},defaultMatchWidth:"wide",parsePatterns:{narrow:[/^s/i,/^m/i,/^t/i,/^w/i,/^t/i,/^f/i,/^s/i],any:[/^su/i,/^m/i,/^tu/i,/^w/i,/^th/i,/^f/i,/^sa/i]},defaultParseWidth:"any"}),dayPeriod:l({matchPatterns:{narrow:/^(a|p|mi|n|(in the|at) (morning|afternoon|evening|night))/i,any:/^([ap]\.?\s?m\.?|midnight|noon|(in the|at) (morning|afternoon|evening|night))/i},defaultMatchWidth:"any",parsePatterns:{any:{am:/^a/i,pm:/^p/i,midnight:/^mi/i,noon:/^no/i,morning:/morning/i,afternoon:/afternoon/i,evening:/evening/i,night:/night/i}},defaultParseWidth:"any"})},options:{weekStartsOn:0,firstWeekContainsDate:1}};var u=a(6913),h=a(4006),m=a(4396),f=a(6174);function p(e){const t=(0,m.a)(e),a=(0,f.w)(e,0);return a.setFullYear(t.getFullYear(),0,1),a.setHours(0,0,0,0),a}function y(e){const t=(0,m.a)(e);return(0,h.m)(t,p(t))+1}var g=a(9518),w=a(6994);function b(e){return(0,w.k)(e,{weekStartsOn:1})}function v(e){const t=(0,m.a)(e),a=t.getFullYear(),n=(0,f.w)(e,0);n.setFullYear(a+1,0,4),n.setHours(0,0,0,0);const r=b(n),i=(0,f.w)(e,0);i.setFullYear(a,0,4),i.setHours(0,0,0,0);const o=b(i);return t.getTime()>=r.getTime()?a+1:t.getTime()>=o.getTime()?a:a-1}function _(e){const t=v(e),a=(0,f.w)(e,0);return a.setFullYear(t,0,4),a.setHours(0,0,0,0),b(a)}function k(e){const t=(0,m.a)(e),a=+b(t)-+_(t);return Math.round(a/g.my)+1}function D(e,t){const a=(0,m.a)(e),n=a.getFullYear(),r=(0,u.q)(),i=t?.firstWeekContainsDate??t?.locale?.options?.firstWeekContainsDate??r.firstWeekContainsDate??r.locale?.options?.firstWeekContainsDate??1,o=(0,f.w)(e,0);o.setFullYear(n+1,0,i),o.setHours(0,0,0,0);const s=(0,w.k)(o,t),l=(0,f.w)(e,0);l.setFullYear(n,0,i),l.setHours(0,0,0,0);const d=(0,w.k)(l,t);return a.getTime()>=s.getTime()?n+1:a.getTime()>=d.getTime()?n:n-1}function x(e,t){const a=(0,u.q)(),n=t?.firstWeekContainsDate??t?.locale?.options?.firstWeekContainsDate??a.firstWeekContainsDate??a.locale?.options?.firstWeekContainsDate??1,r=D(e,t),i=(0,f.w)(e,0);i.setFullYear(r,0,n),i.setHours(0,0,0,0);return(0,w.k)(i,t)}function M(e,t){const a=(0,m.a)(e),n=+(0,w.k)(a,t)-+x(a,t);return Math.round(n/g.my)+1}function T(e,t){return(e<0?"-":"")+Math.abs(e).toString().padStart(t,"0")}const C={y(e,t){const a=e.getFullYear(),n=a>0?a:1-a;return T("yy"===t?n%100:n,t.length)},M(e,t){const a=e.getMonth();return"M"===t?String(a+1):T(a+1,2)},d(e,t){return T(e.getDate(),t.length)},a(e,t){const a=e.getHours()/12>=1?"pm":"am";switch(t){case"a":case"aa":return a.toUpperCase();case"aaa":return a;case"aaaaa":return a[0];default:return"am"===a?"a.m.":"p.m."}},h(e,t){return T(e.getHours()%12||12,t.length)},H(e,t){return T(e.getHours(),t.length)},m(e,t){return T(e.getMinutes(),t.length)},s(e,t){return T(e.getSeconds(),t.length)},S(e,t){const a=t.length,n=e.getMilliseconds();return T(Math.trunc(n*Math.pow(10,a-3)),t.length)}},S="midnight",W="noon",F="morning",N="afternoon",P="evening",$="night",E={G:function(e,t,a){const n=e.getFullYear()>0?1:0;switch(t){case"G":case"GG":case"GGG":return a.era(n,{width:"abbreviated"});case"GGGGG":return a.era(n,{width:"narrow"});default:return a.era(n,{width:"wide"})}},y:function(e,t,a){if("yo"===t){const t=e.getFullYear(),n=t>0?t:1-t;return a.ordinalNumber(n,{unit:"year"})}return C.y(e,t)},Y:function(e,t,a,n){const r=D(e,n),i=r>0?r:1-r;if("YY"===t){return T(i%100,2)}return"Yo"===t?a.ordinalNumber(i,{unit:"year"}):T(i,t.length)},R:function(e,t){return T(v(e),t.length)},u:function(e,t){return T(e.getFullYear(),t.length)},Q:function(e,t,a){const n=Math.ceil((e.getMonth()+1)/3);switch(t){case"Q":return String(n);case"QQ":return T(n,2);case"Qo":return a.ordinalNumber(n,{unit:"quarter"});case"QQQ":return a.quarter(n,{width:"abbreviated",context:"formatting"});case"QQQQQ":return a.quarter(n,{width:"narrow",context:"formatting"});default:return a.quarter(n,{width:"wide",context:"formatting"})}},q:function(e,t,a){const n=Math.ceil((e.getMonth()+1)/3);switch(t){case"q":return String(n);case"qq":return T(n,2);case"qo":return a.ordinalNumber(n,{unit:"quarter"});case"qqq":return a.quarter(n,{width:"abbreviated",context:"standalone"});case"qqqqq":return a.quarter(n,{width:"narrow",context:"standalone"});default:return a.quarter(n,{width:"wide",context:"standalone"})}},M:function(e,t,a){const n=e.getMonth();switch(t){case"M":case"MM":return C.M(e,t);case"Mo":return a.ordinalNumber(n+1,{unit:"month"});case"MMM":return a.month(n,{width:"abbreviated",context:"formatting"});case"MMMMM":return a.month(n,{width:"narrow",context:"formatting"});default:return a.month(n,{width:"wide",context:"formatting"})}},L:function(e,t,a){const n=e.getMonth();switch(t){case"L":return String(n+1);case"LL":return T(n+1,2);case"Lo":return a.ordinalNumber(n+1,{unit:"month"});case"LLL":return a.month(n,{width:"abbreviated",context:"standalone"});case"LLLLL":return a.month(n,{width:"narrow",context:"standalone"});default:return a.month(n,{width:"wide",context:"standalone"})}},w:function(e,t,a,n){const r=M(e,n);return"wo"===t?a.ordinalNumber(r,{unit:"week"}):T(r,t.length)},I:function(e,t,a){const n=k(e);return"Io"===t?a.ordinalNumber(n,{unit:"week"}):T(n,t.length)},d:function(e,t,a){return"do"===t?a.ordinalNumber(e.getDate(),{unit:"date"}):C.d(e,t)},D:function(e,t,a){const n=y(e);return"Do"===t?a.ordinalNumber(n,{unit:"dayOfYear"}):T(n,t.length)},E:function(e,t,a){const n=e.getDay();switch(t){case"E":case"EE":case"EEE":return a.day(n,{width:"abbreviated",context:"formatting"});case"EEEEE":return a.day(n,{width:"narrow",context:"formatting"});case"EEEEEE":return a.day(n,{width:"short",context:"formatting"});default:return a.day(n,{width:"wide",context:"formatting"})}},e:function(e,t,a,n){const r=e.getDay(),i=(r-n.weekStartsOn+8)%7||7;switch(t){case"e":return String(i);case"ee":return T(i,2);case"eo":return a.ordinalNumber(i,{unit:"day"});case"eee":return a.day(r,{width:"abbreviated",context:"formatting"});case"eeeee":return a.day(r,{width:"narrow",context:"formatting"});case"eeeeee":return a.day(r,{width:"short",context:"formatting"});default:return a.day(r,{width:"wide",context:"formatting"})}},c:function(e,t,a,n){const r=e.getDay(),i=(r-n.weekStartsOn+8)%7||7;switch(t){case"c":return String(i);case"cc":return T(i,t.length);case"co":return a.ordinalNumber(i,{unit:"day"});case"ccc":return a.day(r,{width:"abbreviated",context:"standalone"});case"ccccc":return a.day(r,{width:"narrow",context:"standalone"});case"cccccc":return a.day(r,{width:"short",context:"standalone"});default:return a.day(r,{width:"wide",context:"standalone"})}},i:function(e,t,a){const n=e.getDay(),r=0===n?7:n;switch(t){case"i":return String(r);case"ii":return T(r,t.length);case"io":return a.ordinalNumber(r,{unit:"day"});case"iii":return a.day(n,{width:"abbreviated",context:"formatting"});case"iiiii":return a.day(n,{width:"narrow",context:"formatting"});case"iiiiii":return a.day(n,{width:"short",context:"formatting"});default:return a.day(n,{width:"wide",context:"formatting"})}},a:function(e,t,a){const n=e.getHours()/12>=1?"pm":"am";switch(t){case"a":case"aa":return a.dayPeriod(n,{width:"abbreviated",context:"formatting"});case"aaa":return a.dayPeriod(n,{width:"abbreviated",context:"formatting"}).toLowerCase();case"aaaaa":return a.dayPeriod(n,{width:"narrow",context:"formatting"});default:return a.dayPeriod(n,{width:"wide",context:"formatting"})}},b:function(e,t,a){const n=e.getHours();let r;switch(r=12===n?W:0===n?S:n/12>=1?"pm":"am",t){case"b":case"bb":return a.dayPeriod(r,{width:"abbreviated",context:"formatting"});case"bbb":return a.dayPeriod(r,{width:"abbreviated",context:"formatting"}).toLowerCase();case"bbbbb":return a.dayPeriod(r,{width:"narrow",context:"formatting"});default:return a.dayPeriod(r,{width:"wide",context:"formatting"})}},B:function(e,t,a){const n=e.getHours();let r;switch(r=n>=17?P:n>=12?N:n>=4?F:$,t){case"B":case"BB":case"BBB":return a.dayPeriod(r,{width:"abbreviated",context:"formatting"});case"BBBBB":return a.dayPeriod(r,{width:"narrow",context:"formatting"});default:return a.dayPeriod(r,{width:"wide",context:"formatting"})}},h:function(e,t,a){if("ho"===t){let t=e.getHours()%12;return 0===t&&(t=12),a.ordinalNumber(t,{unit:"hour"})}return C.h(e,t)},H:function(e,t,a){return"Ho"===t?a.ordinalNumber(e.getHours(),{unit:"hour"}):C.H(e,t)},K:function(e,t,a){const n=e.getHours()%12;return"Ko"===t?a.ordinalNumber(n,{unit:"hour"}):T(n,t.length)},k:function(e,t,a){let n=e.getHours();return 0===n&&(n=24),"ko"===t?a.ordinalNumber(n,{unit:"hour"}):T(n,t.length)},m:function(e,t,a){return"mo"===t?a.ordinalNumber(e.getMinutes(),{unit:"minute"}):C.m(e,t)},s:function(e,t,a){return"so"===t?a.ordinalNumber(e.getSeconds(),{unit:"second"}):C.s(e,t)},S:function(e,t){return C.S(e,t)},X:function(e,t,a){const n=e.getTimezoneOffset();if(0===n)return"Z";switch(t){case"X":return L(n);case"XXXX":case"XX":return U(n);default:return U(n,":")}},x:function(e,t,a){const n=e.getTimezoneOffset();switch(t){case"x":return L(n);case"xxxx":case"xx":return U(n);default:return U(n,":")}},O:function(e,t,a){const n=e.getTimezoneOffset();switch(t){case"O":case"OO":case"OOO":return"GMT"+Y(n,":");default:return"GMT"+U(n,":")}},z:function(e,t,a){const n=e.getTimezoneOffset();switch(t){case"z":case"zz":case"zzz":return"GMT"+Y(n,":");default:return"GMT"+U(n,":")}},t:function(e,t,a){return T(Math.trunc(e.getTime()/1e3),t.length)},T:function(e,t,a){return T(e.getTime(),t.length)}};function Y(e,t=""){const a=e>0?"-":"+",n=Math.abs(e),r=Math.trunc(n/60),i=n%60;return 0===i?a+String(r):a+String(r)+t+T(i,2)}function L(e,t){if(e%60==0){return(e>0?"-":"+")+T(Math.abs(e)/60,2)}return U(e,t)}function U(e,t=""){const a=e>0?"-":"+",n=Math.abs(e);return a+T(Math.trunc(n/60),2)+t+T(n%60,2)}const q=(e,t)=>{switch(e){case"P":return t.date({width:"short"});case"PP":return t.date({width:"medium"});case"PPP":return t.date({width:"long"});default:return t.date({width:"full"})}},O=(e,t)=>{switch(e){case"p":return t.time({width:"short"});case"pp":return t.time({width:"medium"});case"ppp":return t.time({width:"long"});default:return t.time({width:"full"})}},A={p:O,P:(e,t)=>{const a=e.match(/(P+)(p+)?/)||[],n=a[1],r=a[2];if(!r)return q(e,t);let i;switch(n){case"P":i=t.dateTime({width:"short"});break;case"PP":i=t.dateTime({width:"medium"});break;case"PPP":i=t.dateTime({width:"long"});break;default:i=t.dateTime({width:"full"})}return i.replace("{{date}}",q(n,t)).replace("{{time}}",O(r,t))}},H=/^D+$/,z=/^Y+$/,j=["D","DD","YY","YYYY"];function V(e){return e instanceof Date||"object"==typeof e&&"[object Date]"===Object.prototype.toString.call(e)}function Z(e){if(!V(e)&&"number"!=typeof e)return!1;const t=(0,m.a)(e);return!isNaN(Number(t))}const B=/[yYQqMLwIdDecihHKkms]o|(\w)\1*|''|'(''|[^'])+('|$)|./g,X=/P+p+|P+|p+|''|'(''|[^'])+('|$)|./g,G=/^'([^]*?)'?$/,I=/''/g,Q=/[a-zA-Z]/;function J(e,t,a){const n=(0,u.q)(),r=a?.locale??n.locale??c,i=a?.firstWeekContainsDate??a?.locale?.options?.firstWeekContainsDate??n.firstWeekContainsDate??n.locale?.options?.firstWeekContainsDate??1,o=a?.weekStartsOn??a?.locale?.options?.weekStartsOn??n.weekStartsOn??n.locale?.options?.weekStartsOn??0,s=(0,m.a)(e);if(!Z(s))throw new RangeError("Invalid time value");let l=t.match(X).map((e=>{const t=e[0];if("p"===t||"P"===t){return(0,A[t])(e,r.formatLong)}return e})).join("").match(B).map((e=>{if("''"===e)return{isToken:!1,value:"'"};const t=e[0];if("'"===t)return{isToken:!1,value:K(e)};if(E[t])return{isToken:!0,value:e};if(t.match(Q))throw new RangeError("Format string contains an unescaped latin alphabet character `"+t+"`");return{isToken:!1,value:e}}));r.localize.preprocessor&&(l=r.localize.preprocessor(s,l));const d={firstWeekContainsDate:i,weekStartsOn:o,locale:r};return l.map((n=>{if(!n.isToken)return n.value;const i=n.value;(!a?.useAdditionalWeekYearTokens&&function(e){return z.test(e)}(i)||!a?.useAdditionalDayOfYearTokens&&function(e){return H.test(e)}(i))&&function(e,t,a){const n=function(e,t,a){const n="Y"===e[0]?"years":"days of the month";return`Use \`${e.toLowerCase()}\` instead of \`${e}\` (in \`${t}\`) for formatting ${n} to the input \`${a}\`; see: https://github.com/date-fns/date-fns/blob/master/docs/unicodeTokens.md`}(e,t,a);if(console.warn(n),j.includes(e))throw new RangeError(n)}(i,t,String(e));return(0,E[i[0]])(s,i,r.localize,d)})).join("")}function K(e){const t=e.match(G);return t?t[1].replace(I,"'"):e}},3352:(e,t,a)=>{a.d(t,{o:()=>r});var n=a(4396);function r(e){const t=(0,n.a)(e);return t.setHours(0,0,0,0),t}},6994:(e,t,a)=>{a.d(t,{k:()=>i});var n=a(4396),r=a(6913);function i(e,t){const a=(0,r.q)(),i=t?.weekStartsOn??t?.locale?.options?.weekStartsOn??a.weekStartsOn??a.locale?.options?.weekStartsOn??0,o=(0,n.a)(e),s=o.getDay(),l=(s<i?7:0)+s-i;return o.setDate(o.getDate()-l),o.setHours(0,0,0,0),o}},4396:(e,t,a)=>{function n(e){const t=Object.prototype.toString.call(e);return e instanceof Date||"object"==typeof e&&"[object Date]"===t?new e.constructor(+e):"number"==typeof e||"[object Number]"===t||"string"==typeof e||"[object String]"===t?new Date(e):new Date(NaN)}a.d(t,{a:()=>n})}};
//# sourceMappingURL=_HaMPbXz.js.map