export const id=5608;export const ids=[5608];export const modules={6534:(e,l,r)=>{r.d(l,{M:()=>a,l:()=>o});const o=new Set(["primary","accent","disabled","red","pink","purple","deep-purple","indigo","blue","light-blue","cyan","teal","green","light-green","lime","yellow","amber","orange","deep-orange","brown","light-grey","grey","dark-grey","blue-grey","black","white"]);function a(e){return o.has(e)?`var(--${e}-color)`:e}},4090:(e,l,r)=>{var o=r(5461),a=(r(3981),r(8597)),t=r(196),i=r(2506),d=r(6534),s=r(3167),c=r(4517);r(6334),r(9484);(0,o.A)([(0,t.EM)("ha-color-picker")],(function(e,l){return{F:class extends l{constructor(...l){super(...l),e(this)}},d:[{kind:"field",decorators:[(0,t.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,t.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"defaultColor",value(){return!1}},{kind:"field",decorators:[(0,t.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"method",key:"_valueSelected",value:function(e){const l=e.target.value;l&&(0,s.r)(this,"value-changed",{value:"default"!==l?l:void 0})}},{kind:"method",key:"render",value:function(){return a.qy`
      <ha-select
        .icon=${Boolean(this.value)}
        .label=${this.label}
        .value=${this.value||"default"}
        .helper=${this.helper}
        .disabled=${this.disabled}
        @closed=${c.d}
        @selected=${this._valueSelected}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.value?a.qy`
              <span slot="icon">
                ${this.renderColorCircle(this.value||"grey")}
              </span>
            `:a.s6}
        ${this.defaultColor?a.qy` <ha-list-item value="default">
              ${this.hass.localize("ui.components.color-picker.default_color")}
            </ha-list-item>`:a.s6}
        ${Array.from(d.l).map((e=>a.qy`
            <ha-list-item .value=${e} graphic="icon">
              ${this.hass.localize(`ui.components.color-picker.colors.${e}`)||e}
              <span slot="graphic">${this.renderColorCircle(e)}</span>
            </ha-list-item>
          `))}
      </ha-select>
    `}},{kind:"method",key:"renderColorCircle",value:function(e){return a.qy`
      <span
        class="circle-color"
        style=${(0,i.W)({"--circle-color":(0,d.M)(e)})}
      ></span>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      .circle-color {
        display: block;
        background-color: var(--circle-color);
        border-radius: 10px;
        width: 20px;
        height: 20px;
      }
      ha-select {
        width: 100%;
      }
    `}}]}}),a.WF)},5608:(e,l,r)=>{r.r(l),r.d(l,{HaSelectorUiColor:()=>d});var o=r(5461),a=r(8597),t=r(196),i=r(3167);r(4090);let d=(0,o.A)([(0,t.EM)("ha-selector-ui_color")],(function(e,l){return{F:class extends l{constructor(...l){super(...l),e(this)}},d:[{kind:"field",decorators:[(0,t.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,t.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,t.MZ)()],key:"helper",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`
      <ha-color-picker
        .label=${this.label}
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .defaultColor=${this.selector.ui_color?.default_color}
        @value-changed=${this._valueChanged}
      ></ha-color-picker>
    `}},{kind:"method",key:"_valueChanged",value:function(e){(0,i.r)(this,"value-changed",{value:e.detail.value})}}]}}),a.WF)}};
//# sourceMappingURL=Qfbx8nGt.js.map