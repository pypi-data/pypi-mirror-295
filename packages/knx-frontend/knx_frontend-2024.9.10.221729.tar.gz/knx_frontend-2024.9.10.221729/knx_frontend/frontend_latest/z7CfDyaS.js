/*! For license information please see z7CfDyaS.js.LICENSE.txt */
export const id=4475;export const ids=[4475];export const modules={8762:(t,e,i)=>{i.d(e,{l:()=>h});var o=i(5461),a=i(9534),r=i(2387),c=i(2280),s=i(8597),d=i(196),n=i(2994);i(6396);const l=["button","ha-list-item"],h=(t,e)=>s.qy`
  <div class="header_title">
    <span>${e}</span>
    <ha-icon-button
      .label=${t?.localize("ui.dialogs.generic.close")??"Close"}
      .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
      dialogAction="close"
      class="header_button"
    ></ha-icon-button>
  </div>
`;(0,o.A)([(0,d.EM)("ha-dialog")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",key:n.Xr,value:void 0},{kind:"method",key:"scrollToPos",value:function(t,e){this.contentElement?.scrollTo(t,e)}},{kind:"method",key:"renderHeading",value:function(){return s.qy`<slot name="heading"> ${(0,a.A)(i,"renderHeading",this,3)([])} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){(0,a.A)(i,"firstUpdated",this,3)([]),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,l].join(", "),this._updateScrolledAttribute(),this.contentElement?.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.A)(i,"disconnectedCallback",this,3)([]),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value(){return[c.R,s.AH`
      :host([scrolled]) ::slotted(ha-dialog-header) {
        border-bottom: 1px solid
          var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
      }
      .mdc-dialog {
        --mdc-dialog-scroll-divider-color: var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );
        z-index: var(--dialog-z-index, 8);
        -webkit-backdrop-filter: var(
          --ha-dialog-scrim-backdrop-filter,
          var(--dialog-backdrop-filter, none)
        );
        backdrop-filter: var(
          --ha-dialog-scrim-backdrop-filter,
          var(--dialog-backdrop-filter, none)
        );
        --mdc-dialog-box-shadow: var(--dialog-box-shadow, none);
        --mdc-typography-headline6-font-weight: 400;
        --mdc-typography-headline6-font-size: 1.574rem;
      }
      .mdc-dialog__actions {
        justify-content: var(--justify-action-buttons, flex-end);
        padding-bottom: max(env(safe-area-inset-bottom), 24px);
      }
      .mdc-dialog__actions span:nth-child(1) {
        flex: var(--secondary-action-button-flex, unset);
      }
      .mdc-dialog__actions span:nth-child(2) {
        flex: var(--primary-action-button-flex, unset);
      }
      .mdc-dialog__container {
        align-items: var(--vertical-align-dialog, center);
      }
      .mdc-dialog__title {
        padding: 24px 24px 0 24px;
      }
      .mdc-dialog__actions {
        padding: 12px 24px 12px 24px;
      }
      .mdc-dialog__title::before {
        content: unset;
      }
      .mdc-dialog .mdc-dialog__content {
        position: var(--dialog-content-position, relative);
        padding: var(--dialog-content-padding, 24px);
      }
      :host([hideactions]) .mdc-dialog .mdc-dialog__content {
        padding-bottom: max(
          var(--dialog-content-padding, 24px),
          env(safe-area-inset-bottom)
        );
      }
      .mdc-dialog .mdc-dialog__surface {
        position: var(--dialog-surface-position, relative);
        top: var(--dialog-surface-top);
        margin-top: var(--dialog-surface-margin-top);
        min-height: var(--mdc-dialog-min-height, auto);
        border-radius: var(--ha-dialog-border-radius, 28px);
        -webkit-backdrop-filter: var(--ha-dialog-surface-backdrop-filter, none);
        backdrop-filter: var(--ha-dialog-surface-backdrop-filter, none);
        background: var(
          --ha-dialog-surface-background,
          var(--mdc-theme-surface, #fff)
        );
      }
      :host([flexContent]) .mdc-dialog .mdc-dialog__content {
        display: flex;
        flex-direction: column;
      }
      .header_title {
        position: relative;
        padding-right: 40px;
        padding-inline-end: 40px;
        padding-inline-start: initial;
        direction: var(--direction);
      }
      .header_title span {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        display: block;
      }
      .header_button {
        position: absolute;
        right: -12px;
        top: -12px;
        text-decoration: none;
        color: inherit;
        inset-inline-start: initial;
        inset-inline-end: -12px;
        direction: var(--direction);
      }
      .dialog-actions {
        inset-inline-start: initial !important;
        inset-inline-end: 0px !important;
        direction: var(--direction);
      }
    `]}}]}}),r.u)},3442:(t,e,i)=>{var o=i(5461),a=i(9534),r=i(6513),c=(i(6395),i(5789)),s=i(1086),d=i(6584),n=i(523),l=i(4943),h={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},p={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"};const m=function(t){function e(i){return t.call(this,(0,r.Cl)((0,r.Cl)({},e.defaultAdapter),i))||this}return(0,r.C6)(e,t),Object.defineProperty(e,"strings",{get:function(){return p},enumerable:!1,configurable:!0}),Object.defineProperty(e,"cssClasses",{get:function(){return h},enumerable:!1,configurable:!0}),Object.defineProperty(e,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),e.prototype.setChecked=function(t){this.adapter.setNativeControlChecked(t),this.updateAriaChecked(t),this.updateCheckedStyling(t)},e.prototype.setDisabled=function(t){this.adapter.setNativeControlDisabled(t),t?this.adapter.addClass(h.DISABLED):this.adapter.removeClass(h.DISABLED)},e.prototype.handleChange=function(t){var e=t.target;this.updateAriaChecked(e.checked),this.updateCheckedStyling(e.checked)},e.prototype.updateCheckedStyling=function(t){t?this.adapter.addClass(h.CHECKED):this.adapter.removeClass(h.CHECKED)},e.prototype.updateAriaChecked=function(t){this.adapter.setNativeControlAttr(p.ARIA_CHECKED_ATTR,""+!!t)},e}(l.I);var u=i(8597),b=i(196),v=i(9278);class g extends s.O{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=m,this.rippleHandlers=new n.I((()=>(this.shouldRenderRipple=!0,this.ripple)))}changeHandler(t){this.mdcFoundation.handleChange(t),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},(0,s.i)(this.mdcRoot)),{setNativeControlChecked:t=>{this.formElement.checked=t},setNativeControlDisabled:t=>{this.formElement.disabled=t},setNativeControlAttr:(t,e)=>{this.formElement.setAttribute(t,e)}})}renderRipple(){return this.shouldRenderRipple?u.qy`
        <mwc-ripple
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const t=this.formElement;t&&(this.rippleHandlers.startFocus(),t.focus())}blur(){const t=this.formElement;t&&(this.rippleHandlers.endFocus(),t.blur())}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}render(){return u.qy`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              aria-label="${(0,v.J)(this.ariaLabel)}"
              aria-labelledby="${(0,v.J)(this.ariaLabelledBy)}"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(t){const e=()=>{window.removeEventListener("mouseup",e),this.handleRippleDeactivate()};window.addEventListener("mouseup",e),this.rippleHandlers.startPress(t)}handleRippleTouchStart(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,r.Cg)([(0,b.MZ)({type:Boolean}),(0,d.P)((function(t){this.mdcFoundation.setChecked(t)}))],g.prototype,"checked",void 0),(0,r.Cg)([(0,b.MZ)({type:Boolean}),(0,d.P)((function(t){this.mdcFoundation.setDisabled(t)}))],g.prototype,"disabled",void 0),(0,r.Cg)([c.T,(0,b.MZ)({attribute:"aria-label"})],g.prototype,"ariaLabel",void 0),(0,r.Cg)([c.T,(0,b.MZ)({attribute:"aria-labelledby"})],g.prototype,"ariaLabelledBy",void 0),(0,r.Cg)([(0,b.P)(".mdc-switch")],g.prototype,"mdcRoot",void 0),(0,r.Cg)([(0,b.P)("input")],g.prototype,"formElement",void 0),(0,r.Cg)([(0,b.nJ)("mwc-ripple")],g.prototype,"ripple",void 0),(0,r.Cg)([(0,b.wk)()],g.prototype,"shouldRenderRipple",void 0),(0,r.Cg)([(0,b.Ls)({passive:!0})],g.prototype,"handleRippleMouseDown",null),(0,r.Cg)([(0,b.Ls)({passive:!0})],g.prototype,"handleRippleTouchStart",null);const _=u.AH`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`;var f=i(3167);(0,o.A)([(0,b.EM)("ha-switch")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,b.MZ)({type:Boolean})],key:"haptic",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){(0,a.A)(i,"firstUpdated",this,3)([]),this.addEventListener("change",(()=>{var t;this.haptic&&(t="light",(0,f.r)(window,"haptic",t))}))}},{kind:"field",static:!0,key:"styles",value(){return[_,u.AH`
      :host {
        --mdc-theme-secondary: var(--switch-checked-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
        background-color: var(--switch-checked-button-color);
        border-color: var(--switch-checked-button-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__track {
        background-color: var(--switch-checked-track-color);
        border-color: var(--switch-checked-track-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
        background-color: var(--switch-unchecked-button-color);
        border-color: var(--switch-unchecked-button-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
        background-color: var(--switch-unchecked-track-color);
        border-color: var(--switch-unchecked-track-color);
      }
    `]}}]}}),g)},4475:(t,e,i)=>{i.r(e);var o=i(5461),a=(i(8068),i(8597)),r=i(196),c=i(9760),s=i(9278),d=i(3167);i(8762),i(9222),i(3442);(0,o.A)([(0,r.EM)("dialog-box")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,r.P)("ha-textfield")],key:"_textField",value:void 0},{kind:"method",key:"showDialog",value:async function(t){this._params=t}},{kind:"method",key:"closeDialog",value:function(){return!this._params?.confirmation&&!this._params?.prompt&&(!this._params||(this._dismiss(),!0))}},{kind:"method",key:"render",value:function(){if(!this._params)return a.s6;const t=this._params.confirmation||this._params.prompt;return a.qy`
      <ha-dialog
        open
        ?scrimClickAction=${t}
        ?escapeKeyAction=${t}
        @closed=${this._dialogClosed}
        defaultAction="ignore"
        .heading=${a.qy`${this._params.warning?a.qy`<ha-svg-icon
              .path=${"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16"}
              style="color: var(--warning-color)"
            ></ha-svg-icon> `:""}${this._params.title?this._params.title:this._params.confirmation&&this.hass.localize("ui.dialogs.generic.default_confirmation_title")}`}
      >
        <div>
          ${this._params.text?a.qy`
                <p class=${this._params.prompt?"no-bottom-padding":""}>
                  ${this._params.text}
                </p>
              `:""}
          ${this._params.prompt?a.qy`
                <ha-textfield
                  dialogInitialFocus
                  value=${(0,s.J)(this._params.defaultValue)}
                  .placeholder=${this._params.placeholder}
                  .label=${this._params.inputLabel?this._params.inputLabel:""}
                  .type=${this._params.inputType?this._params.inputType:"text"}
                  .min=${this._params.inputMin}
                  .max=${this._params.inputMax}
                ></ha-textfield>
              `:""}
        </div>
        ${t&&a.qy`
          <mwc-button
            @click=${this._dismiss}
            slot="secondaryAction"
            ?dialogInitialFocus=${!this._params.prompt&&this._params.destructive}
          >
            ${this._params.dismissText?this._params.dismissText:this.hass.localize("ui.dialogs.generic.cancel")}
          </mwc-button>
        `}
        <mwc-button
          @click=${this._confirm}
          ?dialogInitialFocus=${!this._params.prompt&&!this._params.destructive}
          slot="primaryAction"
          class=${(0,c.H)({destructive:this._params.destructive||!1})}
        >
          ${this._params.confirmText?this._params.confirmText:this.hass.localize("ui.dialogs.generic.ok")}
        </mwc-button>
      </ha-dialog>
    `}},{kind:"method",key:"_dismiss",value:function(){this._params?.cancel&&this._params.cancel(),this._close()}},{kind:"method",key:"_confirm",value:function(){this._params.confirm&&this._params.confirm(this._textField?.value),this._close()}},{kind:"method",key:"_dialogClosed",value:function(t){"ignore"!==t.detail.action&&this._dismiss()}},{kind:"method",key:"_close",value:function(){this._params&&(this._params=void 0,(0,d.r)(this,"dialog-closed",{dialog:this.localName}))}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host([inert]) {
        pointer-events: initial !important;
        cursor: initial !important;
      }
      a {
        color: var(--primary-color);
      }
      p {
        margin: 0;
        color: var(--primary-text-color);
      }
      .no-bottom-padding {
        padding-bottom: 0;
      }
      .secondary {
        color: var(--secondary-text-color);
      }
      .destructive {
        --mdc-theme-primary: var(--error-color);
      }
      ha-dialog {
        /* Place above other dialogs */
        --dialog-z-index: 104;
      }
      @media all and (min-width: 600px) {
        ha-dialog {
          --mdc-dialog-min-width: 400px;
        }
      }
      ha-textfield {
        width: 100%;
      }
    `}}]}}),a.WF)}};
//# sourceMappingURL=z7CfDyaS.js.map