export const id=8136;export const ids=[8136];export const modules={8136:(e,t,i)=>{i.r(t),i.d(t,{HaSelectorAttribute:()=>u});var a=i(5461),s=i(9534),d=i(8597),o=i(196),l=i(3167),r=i(4540);i(6442);(0,a.A)([(0,o.EM)("ha-entity-attribute-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"entityId",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Array,attribute:"hide-attributes"})],key:"hideAttributes",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,attribute:"allow-custom-value"})],key:"allowCustomValue",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,o.P)("ha-combo-box",!0)],key:"_comboBox",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return!(!e.has("_opened")&&this._opened)}},{kind:"method",key:"updated",value:function(e){if(e.has("_opened")&&this._opened){const e=this.entityId?this.hass.states[this.entityId]:void 0;this._comboBox.items=e?Object.keys(e.attributes).filter((e=>!this.hideAttributes?.includes(e))).map((t=>({value:t,label:(0,r.R)(this.hass.localize,e,this.hass.entities,t)}))):[]}}},{kind:"method",key:"render",value:function(){return this.hass?d.qy`
      <ha-combo-box
        .hass=${this.hass}
        .value=${this.value?(0,r.R)(this.hass.localize,this.hass.states[this.entityId],this.hass.entities,this.value):""}
        .autofocus=${this.autofocus}
        .label=${this.label??this.hass.localize("ui.components.entity.entity-attribute-picker.attribute")}
        .disabled=${this.disabled||!this.entityId}
        .required=${this.required}
        .helper=${this.helper}
        .allowCustomValue=${this.allowCustomValue}
        item-value-path="value"
        item-label-path="label"
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
      </ha-combo-box>
    `:d.s6}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_valueChanged",value:function(e){this.value=e.detail.value}}]}}),d.WF);let u=(0,a.A)([(0,o.EM)("ha-selector-attribute")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){return d.qy`
      <ha-entity-attribute-picker
        .hass=${this.hass}
        .entityId=${this.selector.attribute?.entity_id||this.context?.filter_entity}
        .hideAttributes=${this.selector.attribute?.hide_attributes}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-value
      ></ha-entity-attribute-picker>
    `}},{kind:"method",key:"updated",value:function(e){if((0,s.A)(i,"updated",this,3)([e]),!this.value||this.selector.attribute?.entity_id||!e.has("context"))return;const t=e.get("context");if(!this.context||!t||t.filter_entity===this.context.filter_entity)return;let a=!1;if(this.context.filter_entity){const e=this.hass.states[this.context.filter_entity];e&&this.value in e.attributes||(a=!0)}else a=void 0!==this.value;a&&(0,l.r)(this,"value-changed",{value:void 0})}}]}}),d.WF)}};
//# sourceMappingURL=KWYxbNbs.js.map