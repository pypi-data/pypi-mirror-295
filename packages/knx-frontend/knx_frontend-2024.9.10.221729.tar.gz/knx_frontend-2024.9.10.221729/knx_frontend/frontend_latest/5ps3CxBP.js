/*! For license information please see 5ps3CxBP.js.LICENSE.txt */
export const id=7150;export const ids=[7150];export const modules={7150:(e,t,d)=>{d.r(t),d.d(t,{HaFormBoolean:()=>u});var a=d(5461),o=d(6513),i=d(196),l=d(487),n=d(4258);let r=class extends l.M{};r.styles=[n.R],r=(0,o.Cg)([(0,i.EM)("mwc-formfield")],r);var c=d(8597),s=d(3167);d(9887);let u=(0,a.A)([(0,i.EM)("ha-form-boolean")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,i.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,i.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,i.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,i.P)("ha-checkbox",!0)],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){return c.qy`
      <mwc-formfield .label=${this.label}>
        <ha-checkbox
          .checked=${this.data}
          .disabled=${this.disabled}
          @change=${this._valueChanged}
        ></ha-checkbox>
      </mwc-formfield>
    `}},{kind:"method",key:"_valueChanged",value:function(e){(0,s.r)(this,"value-changed",{value:e.target.checked})}}]}}),c.WF)}};
//# sourceMappingURL=5ps3CxBP.js.map