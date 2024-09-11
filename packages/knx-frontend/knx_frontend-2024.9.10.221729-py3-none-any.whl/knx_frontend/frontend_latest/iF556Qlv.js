export const id=1382;export const ids=[1382];export const modules={1382:(e,t,r)=>{r.r(t),r.d(t,{HaTriggerSelector:()=>l});var a=r(5461),i=r(8597),o=r(196);r(6052);let l=(0,a.A)([(0,o.EM)("ha-selector-trigger")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){return i.qy`
      ${this.label?i.qy`<label>${this.label}</label>`:i.s6}
      <ha-automation-trigger
        .disabled=${this.disabled}
        .triggers=${this.value||[]}
        .hass=${this.hass}
        .path=${this.selector.trigger?.path}
      ></ha-automation-trigger>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return i.AH`
      ha-automation-trigger {
        display: block;
        margin-bottom: 16px;
      }
      label {
        display: block;
        margin-bottom: 4px;
        font-weight: 500;
      }
    `}}]}}),i.WF)}};
//# sourceMappingURL=iF556Qlv.js.map