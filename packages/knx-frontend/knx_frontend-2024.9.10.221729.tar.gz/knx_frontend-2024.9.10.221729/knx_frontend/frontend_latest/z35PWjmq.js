export const id=6928;export const ids=[6928];export const modules={6928:(e,t,i)=>{i.r(t),i.d(t,{HaSelectorUiStateContent:()=>V});var a=i(5461),s=i(8597),n=i(196),o=i(5845),r=i(6580),l=i(5081),d=i(6041),u=i(3167),c=i(9263),h=i(85),_=i(9534),v=i(3139),m=i(1695);(0,a.A)([(0,n.EM)("ha-relative-time")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"datetime",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"capitalize",value(){return!1}},{kind:"field",key:"_interval",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,_.A)(i,"disconnectedCallback",this,3)([]),this._clearInterval()}},{kind:"method",key:"connectedCallback",value:function(){(0,_.A)(i,"connectedCallback",this,3)([]),this.datetime&&this._startInterval()}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"firstUpdated",value:function(e){(0,_.A)(i,"firstUpdated",this,3)([e]),this._updateRelative()}},{kind:"method",key:"update",value:function(e){(0,_.A)(i,"update",this,3)([e]),this._updateRelative()}},{kind:"method",key:"_clearInterval",value:function(){this._interval&&(window.clearInterval(this._interval),this._interval=void 0)}},{kind:"method",key:"_startInterval",value:function(){this._clearInterval(),this._interval=window.setInterval((()=>this._updateRelative()),6e4)}},{kind:"method",key:"_updateRelative",value:function(){if(this.datetime){const e=(0,v.K)(new Date(this.datetime),this.hass.locale);this.innerHTML=this.capitalize?(0,m.Z)(e):e}else this.innerHTML=this.hass.localize("ui.components.relative_time.never")}}]}}),s.mN);var p=i(6601),k=i(3496),f=i(2503);i(8368);const b=["button","input_button","scene"],y=["remaining_time","install_status"],g={timer:["remaining_time"],update:["install_status"]},$={valve:["current_position"],cover:["current_position"],fan:["percentage"],light:["brightness"]},M={climate:["state","current_temperature"],cover:["state","current_position"],fan:"percentage",humidifier:["state","current_humidity"],light:"brightness",timer:"remaining_time",update:"install_status",valve:["state","current_position"]};(0,a.A)([(0,n.EM)("state-display")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"content",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"name",value:void 0},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"get",key:"_content",value:function(){const e=(0,h.t)(this.stateObj);return this.content??M[e]??"state"}},{kind:"method",key:"_computeContent",value:function(e){const t=this.stateObj,a=(0,h.t)(t);if("state"===e)return t.attributes.device_class!==k.Sn&&!b.includes(a)||(0,p.g0)(t.state)?this.hass.formatEntityState(t):s.qy`
          <hui-timestamp-display
            .hass=${this.hass}
            .ts=${new Date(t.state)}
            format="relative"
            capitalize
          ></hui-timestamp-display>
        `;if("name"===e)return s.qy`${this.name||t.attributes.friendly_name}`;if("last_changed"===e||"last-changed"===e)return s.qy`
        <ha-relative-time
          .hass=${this.hass}
          .datetime=${t.last_changed}
        ></ha-relative-time>
      `;if("last_updated"===e||"last-updated"===e)return s.qy`
        <ha-relative-time
          .hass=${this.hass}
          .datetime=${t.last_updated}
        ></ha-relative-time>
      `;if("last_triggered"===e)return s.qy`
        <ha-relative-time
          .hass=${this.hass}
          .datetime=${t.attributes.last_triggered}
        ></ha-relative-time>
      `;if((g[a]??[]).includes(e)){if("install_status"===e)return s.qy`
          ${(0,f.A_)(t,this.hass)}
        `;if("remaining_time"===e)return i.e(1126).then(i.bind(i,1126)),s.qy`
          <ha-timer-remaining-time
            .hass=${this.hass}
            .stateObj=${t}
          ></ha-timer-remaining-time>
        `}const n=t.attributes[e];return null==n||$[a]?.includes(e)&&!n?void 0:this.hass.formatEntityAttributeValue(t,e)}},{kind:"method",key:"render",value:function(){const e=this.stateObj,t=(0,d.e)(this._content).map((e=>this._computeContent(e))).filter(Boolean);return t.length?s.qy`
      ${t.map(((e,t,i)=>s.qy`${e}${t<i.length-1?" ⸱ ":s.s6}`))}
    `:s.qy`${this.hass.formatEntityState(e)}`}}]}}),s.WF);i(6442);const S=["access_token","available_modes","battery_icon","battery_level","code_arm_required","code_format","color_modes","device_class","editable","effect_list","entity_id","entity_picture","event_types","fan_modes","fan_speed_list","friendly_name","frontend_stream_type","has_date","has_time","hvac_modes","icon","id","max_color_temp_kelvin","max_mireds","max_temp","max","min_color_temp_kelvin","min_mireds","min_temp","min","mode","operation_list","options","percentage_step","precipitation_unit","preset_modes","pressure_unit","remaining","sound_mode_list","source_list","state_class","step","supported_color_modes","supported_features","swing_modes","target_temp_step","temperature_unit","token","unit_of_measurement","visibility_unit","wind_speed_unit"];(0,a.A)([(0,n.EM)("ha-entity-state-content-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"entityId",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"allow-name"})],key:"allowName",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,n.P)("ha-combo-box",!0)],key:"_comboBox",value:void 0},{kind:"method",key:"shouldUpdate",value:function(e){return!(!e.has("_opened")&&this._opened)}},{kind:"field",key:"options",value(){return(0,l.A)(((e,t,i)=>{const a=e?(0,c.m)(e):void 0;return[{label:this.hass.localize("ui.components.state-content-picker.state"),value:"state"},...i?[{label:this.hass.localize("ui.components.state-content-picker.name"),value:"name"}]:[],{label:this.hass.localize("ui.components.state-content-picker.last_changed"),value:"last_changed"},{label:this.hass.localize("ui.components.state-content-picker.last_updated"),value:"last_updated"},...a?y.filter((e=>g[a]?.includes(e))).map((e=>({label:this.hass.localize(`ui.components.state-content-picker.${e}`),value:e}))):[],...Object.keys(t?.attributes??{}).filter((e=>!S.includes(e))).map((e=>({value:e,label:this.hass.formatEntityAttributeName(t,e)})))]}))}},{kind:"field",key:"_filter",value(){return""}},{kind:"method",key:"render",value:function(){if(!this.hass)return s.s6;const e=this._value,t=this.entityId?this.hass.states[this.entityId]:void 0,i=this.options(this.entityId,t,this.allowName),a=i.filter((e=>!this._value.includes(e.value)));return s.qy`
      ${e?.length?s.qy`
            <ha-sortable
              no-style
              @item-moved=${this._moveItem}
              .disabled=${this.disabled}
            >
              <ha-chip-set>
                ${(0,r.u)(this._value,(e=>e),((e,t)=>{const a=i.find((t=>t.value===e))?.label||e;return s.qy`
                      <ha-input-chip
                        .idx=${t}
                        @remove=${this._removeItem}
                        .label=${a}
                        selected
                      >
                        <ha-svg-icon
                          slot="icon"
                          .path=${"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"}
                          data-handle
                        ></ha-svg-icon>

                        ${a}
                      </ha-input-chip>
                    `}))}
              </ha-chip-set>
            </ha-sortable>
          `:s.s6}

      <ha-combo-box
        item-value-path="value"
        item-label-path="label"
        .hass=${this.hass}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required&&!e.length}
        .value=${""}
        .items=${a}
        allow-custom-value
        @filter-changed=${this._filterChanged}
        @value-changed=${this._comboBoxValueChanged}
        @opened-changed=${this._openedChanged}
      ></ha-combo-box>
    `}},{kind:"get",key:"_value",value:function(){return this.value?(0,d.e)(this.value):[]}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value,this._comboBox.filteredItems=this._comboBox.items}},{kind:"method",key:"_filterChanged",value:function(e){this._filter=e?.detail.value||"";const t=this._comboBox.items?.filter((e=>(e.label||e.value).toLowerCase().includes(this._filter?.toLowerCase())));this._filter&&t?.unshift({label:this._filter,value:this._filter}),this._comboBox.filteredItems=t}},{kind:"method",key:"_moveItem",value:async function(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail,a=this._value.concat(),s=a.splice(t,1)[0];a.splice(i,0,s),this._setValue(a),await this.updateComplete,this._filterChanged()}},{kind:"method",key:"_removeItem",value:async function(e){e.stopPropagation();const t=[...this._value];t.splice(e.target.idx,1),this._setValue(t),await this.updateComplete,this._filterChanged()}},{kind:"method",key:"_comboBoxValueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(this.disabled||""===t)return;const i=this._value;i.includes(t)||(setTimeout((()=>{this._filterChanged(),this._comboBox.setInputValue("")}),0),this._setValue([...i,t]))}},{kind:"method",key:"_setValue",value:function(e){const t=0===e.length?void 0:1===e.length?e[0]:e;this.value=t,(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",static:!0,key:"styles",value(){return s.AH`
    :host {
      position: relative;
    }

    ha-chip-set {
      padding: 8px 0;
    }

    .sortable-fallback {
      display: none;
      opacity: 0;
    }

    .sortable-ghost {
      opacity: 0.4;
    }

    .sortable-drag {
      cursor: grabbing;
    }
  `}}]}}),s.WF);let V=(0,a.A)([(0,n.EM)("ha-selector-ui_state_content")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){return s.qy`
      <ha-entity-state-content-picker
        .hass=${this.hass}
        .entityId=${this.selector.ui_state_content?.entity_id||this.context?.filter_entity}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .allowName=${this.selector.ui_state_content?.allow_name}
      ></ha-entity-state-content-picker>
    `}}]}}),(0,o.E)(s.WF))},2503:(e,t,i)=>{i.d(t,{A_:()=>o,Jy:()=>n});i(3758);var a=i(222);i(6412);let s=function(e){return e[e.INSTALL=1]="INSTALL",e[e.SPECIFIC_VERSION=2]="SPECIFIC_VERSION",e[e.PROGRESS=4]="PROGRESS",e[e.BACKUP=8]="BACKUP",e[e.RELEASE_NOTES=16]="RELEASE_NOTES",e}({});const n=e=>(e=>(0,a.$)(e,s.PROGRESS)&&"number"==typeof e.attributes.in_progress)(e)||!!e.attributes.in_progress,o=(e,t)=>{const i=e.state,o=e.attributes;if("off"===i){return o.latest_version&&o.skipped_version===o.latest_version?o.latest_version:t.formatEntityState(e)}if("on"===i&&n(e)){return(0,a.$)(e,s.PROGRESS)&&"number"==typeof o.in_progress?t.localize("ui.card.update.installing_with_progress",{progress:o.in_progress}):t.localize("ui.card.update.installing")}return t.formatEntityState(e)}},5845:(e,t,i)=>{i.d(t,{E:()=>o});var a=i(5461),s=i(9534),n=i(196);const o=e=>(0,a.A)(null,(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,s.A)(i,"connectedCallback",this,3)([]),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,s.A)(i,"disconnectedCallback",this,3)([]),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){if((0,s.A)(i,"updated",this,3)([e]),e.has("hass"))this.__checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const t of e.keys())if(this.hassSubscribeRequiredHostProps.includes(t))return void this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&!this.hassSubscribeRequiredHostProps?.some((e=>void 0===this[e]))&&(this.__unsubs=this.hassSubscribe())}}]}}),e)}};
//# sourceMappingURL=z35PWjmq.js.map