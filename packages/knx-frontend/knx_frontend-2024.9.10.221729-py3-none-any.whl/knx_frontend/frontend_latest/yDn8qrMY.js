export const id=3399;export const ids=[3399];export const modules={3399:(e,a,i)=>{i.r(a),i.d(a,{HaImageSelector:()=>h});var l=i(5461),t=i(9534),o=i(8597),d=i(196),s=i(3167),r=(i(6396),i(7984),i(9373),i(7385),i(2283),i(377));let h=(0,l.A)([(0,d.EM)("ha-selector-image")],(function(e,a){class i extends a{constructor(...a){super(...a),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"name",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,d.wk)()],key:"showUpload",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(e){(0,t.A)(i,"firstUpdated",this,3)([e]),this.value&&!this.value.startsWith(r.fO)||(this.showUpload=!0)}},{kind:"method",key:"render",value:function(){return o.qy`
      <div>
        <label>
          ${this.hass.localize("ui.components.selectors.image.select_image_with_label",{label:this.label||this.hass.localize("ui.components.selectors.image.image")})}
          <ha-formfield
            .label=${this.hass.localize("ui.components.selectors.image.upload")}
          >
            <ha-radio
              name="mode"
              value="upload"
              .checked=${this.showUpload}
              @change=${this._radioGroupPicked}
            ></ha-radio>
          </ha-formfield>
          <ha-formfield
            .label=${this.hass.localize("ui.components.selectors.image.url")}
          >
            <ha-radio
              name="mode"
              value="url"
              .checked=${!this.showUpload}
              @change=${this._radioGroupPicked}
            ></ha-radio>
          </ha-formfield>
        </label>
        ${this.showUpload?o.qy`
              <ha-picture-upload
                .hass=${this.hass}
                .value=${this.value?.startsWith(r.fO)?this.value:null}
                .original=${this.selector.image?.original}
                .cropOptions=${this.selector.image?.crop}
                @change=${this._pictureChanged}
              ></ha-picture-upload>
            `:o.qy`
              <ha-textfield
                .name=${this.name}
                .value=${this.value||""}
                .placeholder=${this.placeholder||""}
                .helper=${this.helper}
                helperPersistent
                .disabled=${this.disabled}
                @input=${this._handleChange}
                .label=${this.label||""}
                .required=${this.required}
              ></ha-textfield>
            `}
      </div>
    `}},{kind:"method",key:"_radioGroupPicked",value:function(e){this.showUpload="upload"===e.target.value}},{kind:"method",key:"_pictureChanged",value:function(e){const a=e.target.value;(0,s.r)(this,"value-changed",{value:a??void 0})}},{kind:"method",key:"_handleChange",value:function(e){let a=e.target.value;this.value!==a&&(""!==a||this.required||(a=void 0),(0,s.r)(this,"value-changed",{value:a}))}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        display: block;
        position: relative;
      }
      div {
        display: flex;
        flex-direction: column;
      }
      label {
        display: flex;
        flex-direction: column;
      }
      ha-textarea,
      ha-textfield {
        width: 100%;
      }
    `}}]}}),o.WF)}};
//# sourceMappingURL=yDn8qrMY.js.map