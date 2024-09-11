export const id=6401;export const ids=[6401];export const modules={6401:(e,t,i)=>{i.r(t),i.d(t,{HaTimeSelector:()=>o});var r=i(5461),d=i(8597),l=i(196);i(4110);let o=(0,r.A)([(0,l.EM)("ha-selector-time")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"method",key:"render",value:function(){return d.qy`
      <ha-time-input
        .value=${"string"==typeof this.value?this.value:void 0}
        .locale=${this.hass.locale}
        .disabled=${this.disabled}
        .required=${this.required}
        clearable
        .helper=${this.helper}
        .label=${this.label}
        .enableSecond=${!this.selector.time?.no_second}
      ></ha-time-input>
    `}}]}}),d.WF)}};
//# sourceMappingURL=uwVCnaPA.js.map