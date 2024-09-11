export const id=1546;export const ids=[1546];export const modules={1546:(e,t,i)=>{i.r(t),i.d(t,{HaSTTSelector:()=>v});var s=i(5461),a=i(8597),n=i(196),d=i(9534),l=i(3167),r=i(4517),u=i(1330),o=i(1355);i(9484),i(6334);var h=i(9263);const c="__NONE_OPTION__";(0,s.A)([(0,n.EM)("ha-stt-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_engines",value:void 0},{kind:"method",key:"render",value:function(){if(!this._engines)return a.s6;let e=this.value;if(!e&&this.required){for(const t of Object.values(this.hass.entities))if("cloud"===t.platform&&"stt"===(0,h.m)(t.entity_id)){e=t.entity_id;break}if(!e)for(const t of this._engines)if(0!==t?.supported_languages?.length){e=t.engine_id;break}}return e||(e=c),a.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.stt-picker.stt")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${r.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?a.s6:a.qy`<ha-list-item .value=${c}>
              ${this.hass.localize("ui.components.stt-picker.none")}
            </ha-list-item>`}
        ${this._engines.map((t=>{if(t.deprecated&&t.engine_id!==e)return a.s6;let i;if(t.engine_id.includes(".")){const e=this.hass.states[t.engine_id];i=e?(0,u.u)(e):t.engine_id}else i=t.name||t.engine_id;return a.qy`<ha-list-item
            .value=${t.engine_id}
            .disabled=${0===t.supported_languages?.length}
          >
            ${i}
          </ha-list-item>`}))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,d.A)(i,"willUpdate",this,3)([e]),this.hasUpdated?e.has("language")&&this._debouncedUpdateEngines():this._updateEngines()}},{kind:"field",key:"_debouncedUpdateEngines",value(){return(0,o.s)((()=>this._updateEngines()),500)}},{kind:"method",key:"_updateEngines",value:async function(){var e,t,i;if(this._engines=(await(e=this.hass,t=this.language,i=this.hass.config.country||void 0,e.callWS({type:"stt/engine/list",language:t,country:i}))).providers,!this.value)return;const s=this._engines.find((e=>e.engine_id===this.value));(0,l.r)(this,"supported-languages-changed",{value:s?.supported_languages}),s&&0!==s.supported_languages?.length||(this.value=void 0,(0,l.r)(this,"value-changed",{value:this.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===c||(this.value=t.value===c?void 0:t.value,(0,l.r)(this,"value-changed",{value:this.value}),(0,l.r)(this,"supported-languages-changed",{value:this._engines.find((e=>e.engine_id===this.value))?.supported_languages}))}}]}}),a.WF);let v=(0,s.A)([(0,n.EM)("ha-selector-stt")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`<ha-stt-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .language=${this.selector.stt?.language||this.context?.language}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-stt-picker>`}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    ha-stt-picker {
      width: 100%;
    }
  `}}]}}),a.WF)}};
//# sourceMappingURL=FSp_L9sO.js.map