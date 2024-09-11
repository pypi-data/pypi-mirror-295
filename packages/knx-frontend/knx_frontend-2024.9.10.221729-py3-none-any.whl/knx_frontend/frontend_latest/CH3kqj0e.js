export const id=2011;export const ids=[2011];export const modules={6640:(e,a,i)=>{var s=i(5461),t=i(8597),l=i(196),o=i(3167);i(6589);(0,s.A)([(0,l.EM)("ha-aliases-editor")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Array})],key:"aliases",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){return this.aliases?t.qy`
      <ha-multi-textfield
        .hass=${this.hass}
        .value=${this.aliases}
        .disabled=${this.disabled}
        .label=${this.hass.localize("ui.dialogs.aliases.label")}
        .removeLabel=${this.hass.localize("ui.dialogs.aliases.remove")}
        .addLabel=${this.hass.localize("ui.dialogs.aliases.add")}
        item-index
        @value-changed=${this._aliasesChanged}
      >
      </ha-multi-textfield>
    `:t.s6}},{kind:"method",key:"_aliasesChanged",value:function(e){(0,o.r)(this,"value-changed",{value:e})}}]}}),t.WF)},2011:(e,a,i)=>{i.r(a);var s=i(5461),t=(i(8068),i(9805),i(8597)),l=i(196),o=i(3167),r=(i(1074),i(6640),i(8762)),n=(i(7385),i(3650),i(1848),i(9373),i(9549),i(3799));const d={round:!1,type:"image/jpeg",quality:.75,aspectRatio:1.78};let h=(0,s.A)(null,(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_aliases",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_labels",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_picture",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_floor",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,l.wk)()],key:"_submitting",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._error=void 0,this._name=this._params.entry?this._params.entry.name:this._params.suggestedName||"",this._aliases=this._params.entry?this._params.entry.aliases:[],this._labels=this._params.entry?this._params.entry.labels:[],this._picture=this._params.entry?.picture||null,this._icon=this._params.entry?.icon||null,this._floor=this._params.entry?.floor_id||null,await this.updateComplete}},{kind:"method",key:"closeDialog",value:function(){this._error="",this._params=void 0,(0,o.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params)return t.s6;const e=this._params.entry,a=!this._isNameValid();return t.qy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${(0,r.l)(this.hass,e?this.hass.localize("ui.panel.config.areas.editor.update_area"):this.hass.localize("ui.panel.config.areas.editor.create_area"))}
      >
        <div>
          ${this._error?t.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
          <div class="form">
            ${e?t.qy`
                  <ha-settings-row>
                    <span slot="heading">
                      ${this.hass.localize("ui.panel.config.areas.editor.area_id")}
                    </span>
                    <span slot="description"> ${e.area_id} </span>
                  </ha-settings-row>
                `:t.s6}

            <ha-textfield
              .value=${this._name}
              @input=${this._nameChanged}
              .label=${this.hass.localize("ui.panel.config.areas.editor.name")}
              .validationMessage=${this.hass.localize("ui.panel.config.areas.editor.name_required")}
              required
              dialogInitialFocus
            ></ha-textfield>

            <ha-icon-picker
              .hass=${this.hass}
              .value=${this._icon}
              @value-changed=${this._iconChanged}
              .label=${this.hass.localize("ui.panel.config.areas.editor.icon")}
            ></ha-icon-picker>

            <ha-floor-picker
              .hass=${this.hass}
              .value=${this._floor}
              @value-changed=${this._floorChanged}
              .label=${this.hass.localize("ui.panel.config.areas.editor.floor")}
            ></ha-floor-picker>

            <ha-labels-picker
              .hass=${this.hass}
              .value=${this._labels}
              @value-changed=${this._labelsChanged}
            ></ha-labels-picker>

            <ha-picture-upload
              .hass=${this.hass}
              .value=${this._picture}
              crop
              .cropOptions=${d}
              @change=${this._pictureChanged}
            ></ha-picture-upload>

            <h3 class="header">
              ${this.hass.localize("ui.panel.config.areas.editor.aliases_section")}
            </h3>

            <p class="description">
              ${this.hass.localize("ui.panel.config.areas.editor.aliases_description")}
            </p>
            <ha-aliases-editor
              .hass=${this.hass}
              .aliases=${this._aliases}
              @value-changed=${this._aliasesChanged}
            ></ha-aliases-editor>
          </div>
        </div>
        <mwc-button slot="secondaryAction" @click=${this.closeDialog}>
          ${this.hass.localize("ui.common.cancel")}
        </mwc-button>
        <mwc-button
          slot="primaryAction"
          @click=${this._updateEntry}
          .disabled=${a||this._submitting}
        >
          ${e?this.hass.localize("ui.common.save"):this.hass.localize("ui.common.add")}
        </mwc-button>
      </ha-dialog>
    `}},{kind:"method",key:"_isNameValid",value:function(){return""!==this._name.trim()}},{kind:"method",key:"_nameChanged",value:function(e){this._error=void 0,this._name=e.target.value}},{kind:"method",key:"_floorChanged",value:function(e){this._error=void 0,this._floor=e.detail.value}},{kind:"method",key:"_iconChanged",value:function(e){this._error=void 0,this._icon=e.detail.value}},{kind:"method",key:"_labelsChanged",value:function(e){this._error=void 0,this._labels=e.detail.value}},{kind:"method",key:"_pictureChanged",value:function(e){this._error=void 0,this._picture=e.target.value}},{kind:"method",key:"_updateEntry",value:async function(){const e=!this._params.entry;this._submitting=!0;try{const a={name:this._name.trim(),picture:this._picture||(e?void 0:null),icon:this._icon||(e?void 0:null),floor_id:this._floor||(e?void 0:null),labels:this._labels||null,aliases:this._aliases};e?await this._params.createEntry(a):await this._params.updateEntry(a),this.closeDialog()}catch(a){this._error=a.message||this.hass.localize("ui.panel.config.areas.editor.unknown_error")}finally{this._submitting=!1}}},{kind:"method",key:"_aliasesChanged",value:function(e){this._aliases=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return[n.nA,t.AH`
        ha-textfield,
        ha-icon-picker,
        ha-floor-picker,
        ha-labels-picker,
        ha-picture-upload {
          display: block;
          margin-bottom: 16px;
        }
      `]}}]}}),t.WF);customElements.define("dialog-area-registry-detail",h)}};
//# sourceMappingURL=CH3kqj0e.js.map