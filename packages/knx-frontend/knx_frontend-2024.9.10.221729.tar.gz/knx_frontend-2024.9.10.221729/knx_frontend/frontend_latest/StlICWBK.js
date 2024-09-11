export const id=8662;export const ids=[8662];export const modules={6640:(e,a,i)=>{var s=i(5461),t=i(8597),o=i(196),l=i(3167);i(6589);(0,s.A)([(0,o.EM)("ha-aliases-editor")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Array})],key:"aliases",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){return this.aliases?t.qy`
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
    `:t.s6}},{kind:"method",key:"_aliasesChanged",value:function(e){(0,l.r)(this,"value-changed",{value:e})}}]}}),t.WF)},8662:(e,a,i)=>{i.r(a);var s=i(5461),t=(i(8068),i(9805),i(8597)),o=i(196),l=i(6580),r=i(5081),d=i(3167),n=(i(3409),i(8331),i(1074),i(6640),i(8762)),h=(i(7385),i(3650),i(9222),i(9373),i(3799)),c=i(3895),u=i(3473);let _=(0,s.A)(null,(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_aliases",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_level",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_submitting",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_addedAreas",value(){return new Set}},{kind:"field",decorators:[(0,o.wk)()],key:"_removedAreas",value(){return new Set}},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._error=void 0,this._name=this._params.entry?this._params.entry.name:this._params.suggestedName||"",this._aliases=this._params.entry?.aliases||[],this._icon=this._params.entry?.icon||null,this._level=this._params.entry?.level??null,this._addedAreas.clear(),this._removedAreas.clear()}},{kind:"method",key:"closeDialog",value:function(){this._error="",this._params=void 0,this._addedAreas.clear(),this._removedAreas.clear(),(0,d.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"field",key:"_floorAreas",value(){return(0,r.A)(((e,a,i,s)=>Object.values(a).filter((a=>(a.floor_id===e?.floor_id||i.has(a.area_id))&&!s.has(a.area_id)))))}},{kind:"method",key:"render",value:function(){const e=this._floorAreas(this._params?.entry,this.hass.areas,this._addedAreas,this._removedAreas);if(!this._params)return t.s6;const a=this._params.entry,i=!this._isNameValid();return t.qy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${(0,n.l)(this.hass,a?this.hass.localize("ui.panel.config.floors.editor.update_floor"):this.hass.localize("ui.panel.config.floors.editor.create_floor"))}
      >
        <div>
          ${this._error?t.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
          <div class="form">
            ${a?t.qy`
                  <ha-settings-row>
                    <span slot="heading">
                      ${this.hass.localize("ui.panel.config.floors.editor.floor_id")}
                    </span>
                    <span slot="description">${a.floor_id}</span>
                  </ha-settings-row>
                `:t.s6}

            <ha-textfield
              .value=${this._name}
              @input=${this._nameChanged}
              .label=${this.hass.localize("ui.panel.config.floors.editor.name")}
              .validationMessage=${this.hass.localize("ui.panel.config.floors.editor.name_required")}
              required
              dialogInitialFocus
            ></ha-textfield>

            <ha-textfield
              .value=${this._level}
              @input=${this._levelChanged}
              .label=${this.hass.localize("ui.panel.config.floors.editor.level")}
              type="number"
            ></ha-textfield>

            <ha-icon-picker
              .hass=${this.hass}
              .value=${this._icon}
              @value-changed=${this._iconChanged}
              .label=${this.hass.localize("ui.panel.config.areas.editor.icon")}
            >
              ${this._icon?t.s6:t.qy`
                    <ha-floor-icon
                      slot="fallback"
                      .floor=${{level:this._level}}
                    ></ha-floor-icon>
                  `}
            </ha-icon-picker>

            <h3 class="header">
              ${this.hass.localize("ui.panel.config.floors.editor.areas_section")}
            </h3>

            <p class="description">
              ${this.hass.localize("ui.panel.config.floors.editor.areas_description")}
            </p>
            ${e.length?t.qy`<ha-chip-set>
                  ${(0,l.u)(e,(e=>e.area_id),(e=>t.qy`<ha-input-chip
                        .area=${e}
                        @click=${this._openArea}
                        @remove=${this._removeArea}
                        .label=${e?.name}
                      >
                        ${e.icon?t.qy`<ha-icon
                              slot="icon"
                              .icon=${e.icon}
                            ></ha-icon>`:t.qy`<ha-svg-icon
                              slot="icon"
                              .path=${"M20 2H4C2.9 2 2 2.9 2 4V20C2 21.11 2.9 22 4 22H20C21.11 22 22 21.11 22 20V4C22 2.9 21.11 2 20 2M4 6L6 4H10.9L4 10.9V6M4 13.7L13.7 4H18.6L4 18.6V13.7M20 18L18 20H13.1L20 13.1V18M20 10.3L10.3 20H5.4L20 5.4V10.3Z"}
                            ></ha-svg-icon>`}
                      </ha-input-chip>`))}
                </ha-chip-set>`:t.s6}
            <ha-area-picker
              no-add
              .hass=${this.hass}
              @value-changed=${this._addArea}
              .excludeAreas=${e.map((e=>e.area_id))}
              .label=${this.hass.localize("ui.panel.config.floors.editor.add_area")}
            ></ha-area-picker>

            <h3 class="header">
              ${this.hass.localize("ui.panel.config.floors.editor.aliases_section")}
            </h3>

            <p class="description">
              ${this.hass.localize("ui.panel.config.floors.editor.aliases_description")}
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
          .disabled=${i||this._submitting}
        >
          ${a?this.hass.localize("ui.common.save"):this.hass.localize("ui.common.add")}
        </mwc-button>
      </ha-dialog>
    `}},{kind:"method",key:"_openArea",value:function(e){const a=e.target.area;(0,c.J)(this,{entry:a,updateEntry:e=>(0,u.gs)(this.hass,a.area_id,e)})}},{kind:"method",key:"_removeArea",value:function(e){const a=e.target.area.area_id;if(this._addedAreas.has(a))return this._addedAreas.delete(a),void(this._addedAreas=new Set(this._addedAreas));this._removedAreas.add(a),this._removedAreas=new Set(this._removedAreas)}},{kind:"method",key:"_addArea",value:function(e){const a=e.detail.value;if(a){if(e.target.value="",this._removedAreas.has(a))return this._removedAreas.delete(a),void(this._removedAreas=new Set(this._removedAreas));this._addedAreas.add(a),this._addedAreas=new Set(this._addedAreas)}}},{kind:"method",key:"_isNameValid",value:function(){return""!==this._name.trim()}},{kind:"method",key:"_nameChanged",value:function(e){this._error=void 0,this._name=e.target.value}},{kind:"method",key:"_levelChanged",value:function(e){this._error=void 0,this._level=""===e.target.value?null:Number(e.target.value)}},{kind:"method",key:"_iconChanged",value:function(e){this._error=void 0,this._icon=e.detail.value}},{kind:"method",key:"_updateEntry",value:async function(){this._submitting=!0;const e=!this._params.entry;try{const a={name:this._name.trim(),icon:this._icon||(e?void 0:null),level:this._level,aliases:this._aliases};e?await this._params.createEntry(a,this._addedAreas):await this._params.updateEntry(a,this._addedAreas,this._removedAreas),this.closeDialog()}catch(a){this._error=a.message||this.hass.localize("ui.panel.config.floors.editor.unknown_error")}finally{this._submitting=!1}}},{kind:"method",key:"_aliasesChanged",value:function(e){this._aliases=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return[h.RF,h.nA,t.AH`
        ha-textfield {
          display: block;
          margin-bottom: 16px;
        }
        ha-floor-icon {
          color: var(--secondary-text-color);
        }
        ha-chip-set {
          margin-bottom: 8px;
        }
      `]}}]}}),t.WF);customElements.define("dialog-floor-registry-detail",_)}};
//# sourceMappingURL=StlICWBK.js.map