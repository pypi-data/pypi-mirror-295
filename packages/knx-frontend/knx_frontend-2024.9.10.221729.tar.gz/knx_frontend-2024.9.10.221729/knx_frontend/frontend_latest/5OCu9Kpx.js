/*! For license information please see 5OCu9Kpx.js.LICENSE.txt */
export const id=2535;export const ids=[2535];export const modules={8873:(e,t,s)=>{s.d(t,{a:()=>n});var i=s(6601),r=s(9263);function n(e,t){const s=(0,r.m)(e.entity_id),n=void 0!==t?t:e?.state;if(["button","event","input_button","scene"].includes(s))return n!==i.Hh;if((0,i.g0)(n))return!1;if(n===i.KF&&"alert"!==s)return!1;switch(s){case"alarm_control_panel":return"disarmed"!==n;case"alert":return"idle"!==n;case"cover":case"valve":return"closed"!==n;case"device_tracker":case"person":return"not_home"!==n;case"lawn_mower":return["mowing","error"].includes(n);case"lock":return"locked"!==n;case"media_player":return"standby"!==n;case"vacuum":return!["idle","docked","paused"].includes(n);case"plant":return"problem"===n;case"group":return["on","home","open","locked","problem"].includes(n);case"timer":return"active"===n;case"camera":return"streaming"===n}return!0}},8498:(e,t,s)=>{var i=s(5461),r=s(8597),n=s(196),a=s(1330),l=(s(185),s(6601)),o=s(3496);s(8368);(0,i.A)([(0,n.EM)("entity-preview-row")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"stateObj",value:void 0},{kind:"method",key:"render",value:function(){if(!this.stateObj)return r.s6;const e=this.stateObj;return r.qy`<state-badge
        .hass=${this.hass}
        .stateObj=${e}
        stateColor
      ></state-badge>
      <div class="name" .title=${(0,a.u)(e)}>
        ${(0,a.u)(e)}
      </div>
      <div class="value">
        ${e.attributes.device_class!==o.Sn||(0,l.g0)(e.state)?this.hass.formatEntityState(e):r.qy`
              <hui-timestamp-display
                .hass=${this.hass}
                .ts=${new Date(e.state)}
                capitalize
              ></hui-timestamp-display>
            `}
      </div>`}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`
      :host {
        display: flex;
        align-items: center;
        flex-direction: row;
      }
      .name {
        margin-left: 16px;
        margin-right: 8px;
        margin-inline-start: 16px;
        margin-inline-end: 8px;
        flex: 1 1 30%;
      }
      .value {
        direction: ltr;
      }
    `}}]}}),r.WF)},9123:(e,t,s)=>{var i=s(5461),r=s(9534),n=s(8597),a=s(196),l=s(1355);s(8498);var o=s(3167);(0,i.A)([(0,a.EM)("flow-preview-template")],(function(e,t){class s extends t{constructor(...t){super(...t),e(this)}}return{F:s,d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"flowType",value:void 0},{kind:"field",key:"handler",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"stepId",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"flowId",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"stepData",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_preview",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_listeners",value:void 0},{kind:"field",decorators:[(0,a.wk)()],key:"_error",value:void 0},{kind:"field",key:"_unsub",value:void 0},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.A)(s,"disconnectedCallback",this,3)([]),this._unsub&&(this._unsub.then((e=>e())),this._unsub=void 0)}},{kind:"method",key:"willUpdate",value:function(e){e.has("stepData")&&this._debouncedSubscribePreview()}},{kind:"method",key:"render",value:function(){return this._error?n.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:n.qy`<entity-preview-row
        .hass=${this.hass}
        .stateObj=${this._preview}
      ></entity-preview-row>
      ${this._listeners?.time?n.qy`
            <p>
              ${this.hass.localize("ui.dialogs.helper_settings.template.time")}
            </p>
          `:n.s6}
      ${this._listeners?this._listeners.all?n.qy`
              <p class="all_listeners">
                ${this.hass.localize("ui.dialogs.helper_settings.template.all_listeners")}
              </p>
            `:this._listeners.domains.length||this._listeners.entities.length?n.qy`
                <p>
                  ${this.hass.localize("ui.dialogs.helper_settings.template.listeners")}
                </p>
                <ul>
                  ${this._listeners.domains.sort().map((e=>n.qy`
                        <li>
                          <b
                            >${this.hass.localize("ui.dialogs.helper_settings.template.domain")}</b
                          >: ${e}
                        </li>
                      `))}
                  ${this._listeners.entities.sort().map((e=>n.qy`
                        <li>
                          <b
                            >${this.hass.localize("ui.dialogs.helper_settings.template.entity")}</b
                          >: ${e}
                        </li>
                      `))}
                </ul>
              `:this._listeners.time?n.s6:n.qy`<p class="all_listeners">
                  ${this.hass.localize("ui.dialogs.helper_settings.template.no_listeners")}
                </p>`:n.s6} `}},{kind:"field",key:"_setPreview",value(){return e=>{if("error"in e)return this._error=e.error,void(this._preview=void 0);this._error=void 0,this._listeners=e.listeners;const t=(new Date).toISOString();this._preview={entity_id:`${this.stepId}.___flow_preview___`,last_changed:t,last_updated:t,context:{id:"",parent_id:null,user_id:null},attributes:e.attributes,state:e.state}}}},{kind:"field",key:"_debouncedSubscribePreview",value(){return(0,l.s)((()=>{this._subscribePreview()}),250)}},{kind:"method",key:"_subscribePreview",value:async function(){var e,t,s,i,r;if(this._unsub&&((await this._unsub)(),this._unsub=void 0),"repair_flow"!==this.flowType)try{this._unsub=(e=this.hass,t=this.flowId,s=this.flowType,i=this.stepData,r=this._setPreview,e.connection.subscribeMessage(r,{type:"template/start_preview",flow_id:t,flow_type:s,user_input:i})),await this._unsub,(0,o.r)(this,"set-flow-errors",{errors:{}})}catch(n){"string"==typeof n.message?this._error=n.message:(this._error=void 0,(0,o.r)(this,"set-flow-errors",n.message)),this._unsub=void 0,this._preview=void 0}}}]}}),n.WF)},6625:(e,t,s)=>{s.d(t,{T:()=>h});var i=s(4078),r=s(3982),n=s(3267);class a{constructor(e){this.G=e}disconnect(){this.G=void 0}reconnect(e){this.G=e}deref(){return this.G}}class l{constructor(){this.Y=void 0,this.Z=void 0}get(){return this.Y}pause(){var e;null!==(e=this.Y)&&void 0!==e||(this.Y=new Promise((e=>this.Z=e)))}resume(){var e;null===(e=this.Z)||void 0===e||e.call(this),this.Y=this.Z=void 0}}var o=s(2154);const d=e=>!(0,r.sO)(e)&&"function"==typeof e.then,u=1073741823;class c extends n.Kq{constructor(){super(...arguments),this._$C_t=u,this._$Cwt=[],this._$Cq=new a(this),this._$CK=new l}render(...e){var t;return null!==(t=e.find((e=>!d(e))))&&void 0!==t?t:i.c0}update(e,t){const s=this._$Cwt;let r=s.length;this._$Cwt=t;const n=this._$Cq,a=this._$CK;this.isConnected||this.disconnected();for(let i=0;i<t.length&&!(i>this._$C_t);i++){const e=t[i];if(!d(e))return this._$C_t=i,e;i<r&&e===s[i]||(this._$C_t=u,r=0,Promise.resolve(e).then((async t=>{for(;a.get();)await a.get();const s=n.deref();if(void 0!==s){const i=s._$Cwt.indexOf(e);i>-1&&i<s._$C_t&&(s._$C_t=i,s.setValue(t))}})))}return i.c0}disconnected(){this._$Cq.disconnect(),this._$CK.pause()}reconnected(){this._$Cq.reconnect(this),this._$CK.resume()}}const h=(0,o.u$)(c)}};
//# sourceMappingURL=5OCu9Kpx.js.map