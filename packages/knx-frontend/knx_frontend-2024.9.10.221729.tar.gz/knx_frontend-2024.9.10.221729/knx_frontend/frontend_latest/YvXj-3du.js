export const id=5576;export const ids=[5576];export const modules={5576:(e,a,l)=>{l.r(a),l.d(a,{HaLabelSelector:()=>o});var d=l(5461),i=l(8597),t=l(196),r=l(6041),s=l(3167);l(9549);let o=(0,d.A)([(0,t.EM)("ha-selector-label")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,t.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"name",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,t.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return this.selector.label.multiple?i.qy`
        <ha-labels-picker
          no-add
          .hass=${this.hass}
          .value=${(0,r.e)(this.value??[])}
          .disabled=${this.disabled}
          .label=${this.label}
          @value-changed=${this._handleChange}
        >
        </ha-labels-picker>
      `:i.qy`
      <ha-label-picker
        no-add
        .hass=${this.hass}
        .value=${this.value}
        .disabled=${this.disabled}
        .label=${this.label}
        @value-changed=${this._handleChange}
      >
      </ha-label-picker>
    `}},{kind:"method",key:"_handleChange",value:function(e){let a=e.detail.value;this.value!==a&&((""===a||Array.isArray(a)&&0===a.length)&&!this.required&&(a=void 0),(0,s.r)(this,"value-changed",{value:a}))}},{kind:"get",static:!0,key:"styles",value:function(){return i.AH`
      ha-labels-picker {
        display: block;
        width: 100%;
      }
    `}}]}}),i.WF)}};
//# sourceMappingURL=YvXj-3du.js.map