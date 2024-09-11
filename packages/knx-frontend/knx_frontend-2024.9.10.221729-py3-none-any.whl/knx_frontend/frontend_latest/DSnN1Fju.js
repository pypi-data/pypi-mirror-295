/*! For license information please see DSnN1Fju.js.LICENSE.txt */
export const id=5494;export const ids=[5494];export const modules={920:(e,t,i)=>{var n=i(5461),r=i(9534),a=(i(7350),i(8597)),o=i(196),d=i(10),s=i(2994);(0,n.A)([(0,o.EM)("ha-button-menu")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:s.Xr,value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"corner",value(){return"BOTTOM_START"}},{kind:"field",decorators:[(0,o.MZ)()],key:"menuCorner",value(){return"START"}},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"x",value(){return null}},{kind:"field",decorators:[(0,o.MZ)({type:Number})],key:"y",value(){return null}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"multi",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"activatable",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"fixed",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Boolean,attribute:"no-anchor"})],key:"noAnchor",value(){return!1}},{kind:"field",decorators:[(0,o.P)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){return this._menu?.items}},{kind:"get",key:"selected",value:function(){return this._menu?.selected}},{kind:"method",key:"focus",value:function(){this._menu?.open?this._menu.focusItemAtIndex(0):this._triggerButton?.focus()}},{kind:"method",key:"render",value:function(){return a.qy`
      <div @click=${this._handleClick}>
        <slot name="trigger" @slotchange=${this._setTriggerAria}></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .menuCorner=${this.menuCorner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
        .y=${this.y}
        .x=${this.x}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,r.A)(i,"firstUpdated",this,3)([e]),"rtl"===d.G.document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),a.WF)},3604:(e,t,i)=>{var n=i(5461),r=i(9534),a=i(8597),o=i(6513),d=i(196),s=i(1497),l=i(8678);let c=class extends s.L{};c.styles=[l.R],c=(0,o.Cg)([(0,d.EM)("mwc-checkbox")],c);var h=i(9760),u=i(6175);class m extends u.J{constructor(){super(...arguments),this.left=!1,this.graphic="control"}render(){const e={"mdc-deprecated-list-item__graphic":this.left,"mdc-deprecated-list-item__meta":!this.left},t=this.renderText(),i=this.graphic&&"control"!==this.graphic&&!this.left?this.renderGraphic():a.qy``,n=this.hasMeta&&this.left?this.renderMeta():a.qy``,r=this.renderRipple();return a.qy`
      ${r}
      ${i}
      ${this.left?"":t}
      <span class=${(0,h.H)(e)}>
        <mwc-checkbox
            reducedTouchTarget
            tabindex=${this.tabindex}
            .checked=${this.selected}
            ?disabled=${this.disabled}
            @change=${this.onChange}>
        </mwc-checkbox>
      </span>
      ${this.left?t:""}
      ${n}`}async onChange(e){const t=e.target;this.selected===t.checked||(this._skipPropRequest=!0,this.selected=t.checked,await this.updateComplete,this._skipPropRequest=!1)}}(0,o.Cg)([(0,d.P)("slot")],m.prototype,"slotElement",void 0),(0,o.Cg)([(0,d.P)("mwc-checkbox")],m.prototype,"checkboxElement",void 0),(0,o.Cg)([(0,d.MZ)({type:Boolean})],m.prototype,"left",void 0),(0,o.Cg)([(0,d.MZ)({type:String,reflect:!0})],m.prototype,"graphic",void 0);const p=a.AH`:host(:not([twoline])){height:56px}:host(:not([left])) .mdc-deprecated-list-item__meta{height:40px;width:40px}`;var g=i(5592),k=i(3167);(0,n.A)([(0,d.EM)("ha-check-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"onChange",value:async function(e){(0,r.A)(i,"onChange",this,3)([e]),(0,k.r)(this,e.type)}},{kind:"field",static:!0,key:"styles",value(){return[g.R,p,a.AH`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }

      :host([graphic="avatar"]) .mdc-deprecated-list-item__graphic,
      :host([graphic="medium"]) .mdc-deprecated-list-item__graphic,
      :host([graphic="large"]) .mdc-deprecated-list-item__graphic,
      :host([graphic="control"]) .mdc-deprecated-list-item__graphic {
        margin-inline-end: var(--mdc-list-item-graphic-margin, 16px);
        margin-inline-start: 0px;
        direction: var(--direction);
      }
      .mdc-deprecated-list-item__meta {
        flex-shrink: 0;
        direction: var(--direction);
        margin-inline-start: auto;
        margin-inline-end: 0;
      }
      .mdc-deprecated-list-item__graphic {
        margin-top: var(--check-list-item-graphic-margin-top);
      }
      :host([graphic="icon"]) .mdc-deprecated-list-item__graphic {
        margin-inline-start: 0;
        margin-inline-end: var(--mdc-list-item-graphic-margin, 32px);
      }
    `]}}]}}),m)},5494:(e,t,i)=>{i.r(t),i.d(t,{HaFormMultiSelect:()=>l});var n=i(5461),r=i(8597),a=i(196),o=i(3167);i(920),i(3604),i(9887),i(2694),i(9222),i(9373);function d(e){return Array.isArray(e)?e[0]:e}function s(e){return Array.isArray(e)?e[1]||e[0]:e}let l=(0,n.A)([(0,a.EM)("ha-form-multi_select")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,a.MZ)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,a.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,a.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,a.wk)()],key:"_opened",value(){return!1}},{kind:"field",decorators:[(0,a.P)("ha-button-menu")],key:"_input",value:void 0},{kind:"method",key:"focus",value:function(){this._input&&this._input.focus()}},{kind:"method",key:"render",value:function(){const e=Array.isArray(this.schema.options)?this.schema.options:Object.entries(this.schema.options),t=this.data||[];return e.length<6?r.qy`<div>
        ${this.label}${e.map((e=>{const i=d(e);return r.qy`
            <ha-formfield .label=${s(e)}>
              <ha-checkbox
                .checked=${t.includes(i)}
                .value=${i}
                .disabled=${this.disabled}
                @change=${this._valueChanged}
              ></ha-checkbox>
            </ha-formfield>
          `}))}
      </div> `:r.qy`
      <ha-button-menu
        .disabled=${this.disabled}
        fixed
        @opened=${this._handleOpen}
        @closed=${this._handleClose}
        multi
        activatable
      >
        <ha-textfield
          slot="trigger"
          .label=${this.label}
          .value=${t.map((t=>s(e.find((e=>d(e)===t)))||t)).join(", ")}
          .disabled=${this.disabled}
          tabindex="-1"
        ></ha-textfield>
        <ha-svg-icon
          slot="trigger"
          .path=${this._opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"}
        ></ha-svg-icon>
        ${e.map((e=>{const i=d(e),n=t.includes(i);return r.qy`<ha-check-list-item
            left
            .selected=${n}
            .activated=${n}
            @request-selected=${this._selectedChanged}
            .value=${i}
            .disabled=${this.disabled}
          >
            ${s(e)}
          </ha-check-list-item>`}))}
      </ha-button-menu>
    `}},{kind:"method",key:"firstUpdated",value:function(){this.updateComplete.then((()=>{const{formElement:e,mdcRoot:t}=this.shadowRoot?.querySelector("ha-textfield")||{};e&&(e.style.textOverflow="ellipsis"),t&&(t.style.cursor="pointer")}))}},{kind:"method",key:"updated",value:function(e){e.has("schema")&&this.toggleAttribute("own-margin",Object.keys(this.schema.options).length>=6&&!!this.schema.required)}},{kind:"method",key:"_selectedChanged",value:function(e){e.stopPropagation(),"property"!==e.detail.source&&this._handleValueChanged(e.target.value,e.detail.selected)}},{kind:"method",key:"_valueChanged",value:function(e){const{value:t,checked:i}=e.target;this._handleValueChanged(t,i)}},{kind:"method",key:"_handleValueChanged",value:function(e,t){let i;if(t)if(this.data){if(this.data.includes(e))return;i=[...this.data,e]}else i=[e];else{if(!this.data.includes(e))return;i=this.data.filter((t=>t!==e))}(0,o.r)(this,"value-changed",{value:i})}},{kind:"method",key:"_handleOpen",value:function(e){e.stopPropagation(),this._opened=!0,this.toggleAttribute("opened",!0)}},{kind:"method",key:"_handleClose",value:function(e){e.stopPropagation(),this._opened=!1,this.toggleAttribute("opened",!1)}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`
      :host([own-margin]) {
        margin-bottom: 5px;
      }
      ha-button-menu {
        display: block;
        cursor: pointer;
      }
      ha-formfield {
        display: block;
        padding-right: 16px;
        padding-inline-end: 16px;
        padding-inline-start: initial;
        direction: var(--direction);
      }
      ha-textfield {
        display: block;
        pointer-events: none;
      }
      ha-svg-icon {
        color: var(--input-dropdown-icon-color);
        position: absolute;
        right: 1em;
        top: 1em;
        cursor: pointer;
        inset-inline-end: 1em;
        inset-inline-start: initial;
        direction: var(--direction);
      }
      :host([opened]) ha-svg-icon {
        color: var(--primary-color);
      }
      :host([opened]) ha-button-menu {
        --mdc-text-field-idle-line-color: var(--input-hover-line-color);
        --mdc-text-field-label-ink-color: var(--primary-color);
      }
    `}}]}}),r.WF)}};
//# sourceMappingURL=DSnN1Fju.js.map