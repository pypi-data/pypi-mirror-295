export const id=5187;export const ids=[5187];export const modules={5187:(t,e,o)=>{o.r(e),o.d(e,{HaConditionSelector:()=>n});var i=o(5461),a=o(8597),d=o(196);o(3115);let n=(0,i.A)([(0,d.EM)("ha-selector-condition")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){return a.qy`
      ${this.label?a.qy`<label>${this.label}</label>`:a.s6}
      <ha-automation-condition
        .disabled=${this.disabled}
        .conditions=${this.value||[]}
        .hass=${this.hass}
        .path=${this.selector.condition?.path}
      ></ha-automation-condition>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      ha-automation-condition {
        display: block;
        margin-bottom: 16px;
      }
      label {
        display: block;
        margin-bottom: 4px;
        font-weight: 500;
      }
    `}}]}}),a.WF)}};
//# sourceMappingURL=reMhYJmf.js.map