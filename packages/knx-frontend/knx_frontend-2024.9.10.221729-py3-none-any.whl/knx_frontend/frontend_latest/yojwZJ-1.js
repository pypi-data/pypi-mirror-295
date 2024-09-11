export const id=7674;export const ids=[7674];export const modules={678:(e,i,t)=>{t.d(i,{T:()=>l});var s=t(5081);const l=(e,i)=>{try{return a(i)?.of(e)??e}catch{return e}},a=(0,s.A)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})))},4625:(e,i,t)=>{var s=t(5461),l=t(9534),a=t(8597),d=t(196),r=t(3167),n=t(4517),u=t(678);t(9484),t(6334);const o="preferred",c="last_used";(0,s.A)([(0,d.EM)("ha-assist-pipeline-picker")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,d.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"includeLastUsed",value(){return!1}},{kind:"field",decorators:[(0,d.wk)()],key:"_pipelines",value:void 0},{kind:"field",decorators:[(0,d.wk)()],key:"_preferredPipeline",value(){return null}},{kind:"get",key:"_default",value:function(){return this.includeLastUsed?c:o}},{kind:"method",key:"render",value:function(){if(!this._pipelines)return a.s6;const e=this.value??this._default;return a.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.pipeline-picker.pipeline")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${n.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.includeLastUsed?a.qy`
              <ha-list-item .value=${c}>
                ${this.hass.localize("ui.components.pipeline-picker.last_used")}
              </ha-list-item>
            `:null}
        <ha-list-item .value=${o}>
          ${this.hass.localize("ui.components.pipeline-picker.preferred",{preferred:this._pipelines.find((e=>e.id===this._preferredPipeline))?.name})}
        </ha-list-item>
        ${this._pipelines.map((e=>a.qy`<ha-list-item .value=${e.id}>
              ${e.name}
              (${(0,u.T)(e.language,this.hass.locale)})
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"firstUpdated",value:function(e){var i;(0,l.A)(t,"firstUpdated",this,3)([e]),(i=this.hass,i.callWS({type:"assist_pipeline/pipeline/list"})).then((e=>{this._pipelines=e.pipelines,this._preferredPipeline=e.preferred_pipeline}))}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const i=e.target;!this.hass||""===i.value||i.value===this.value||void 0===this.value&&i.value===this._default||(this.value=i.value===this._default?void 0:i.value,(0,r.r)(this,"value-changed",{value:this.value}))}}]}}),a.WF)},7674:(e,i,t)=>{t.r(i),t.d(i,{HaAssistPipelineSelector:()=>d});var s=t(5461),l=t(8597),a=t(196);t(4625);let d=(0,s.A)([(0,a.EM)("ha-selector-assist_pipeline")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"method",key:"render",value:function(){return l.qy`
      <ha-assist-pipeline-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .includeLastUsed=${Boolean(this.selector.assist_pipeline?.include_last_used)}
      ></ha-assist-pipeline-picker>
    `}},{kind:"field",static:!0,key:"styles",value(){return l.AH`
    ha-conversation-agent-picker {
      width: 100%;
    }
  `}}]}}),l.WF)}};
//# sourceMappingURL=yojwZJ-1.js.map