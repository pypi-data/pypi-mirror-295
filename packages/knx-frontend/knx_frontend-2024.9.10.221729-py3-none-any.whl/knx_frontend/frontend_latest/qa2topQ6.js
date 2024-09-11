export const id=9184;export const ids=[9184];export const modules={2872:(e,t,i)=>{i.d(t,{x:()=>o});const o=(e,t)=>e&&e.config.components.includes(t)},106:(e,t,i)=>{i.d(t,{d:()=>o});const o=e=>{switch(e.language){case"cz":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},6287:(e,t,i)=>{var o=i(5461),a=i(9534),n=(i(8774),i(8597)),r=i(196),s=i(9760),l=i(3167),d=(i(6494),i(6396),i(106)),c=i(6041);const h="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",p="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z";(0,o.A)([(0,r.EM)("ha-file-upload")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"accept",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"icon",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"secondary",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"supports",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Object})],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"multiple",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"uploading",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Number})],key:"progress",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"auto-open-file-dialog"})],key:"autoOpenFileDialog",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_drag",value(){return!1}},{kind:"field",decorators:[(0,r.P)("#input")],key:"_input",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,a.A)(i,"firstUpdated",this,3)([e]),this.autoOpenFileDialog&&this._openFilePicker()}},{kind:"method",key:"render",value:function(){return n.qy`
      ${this.uploading?n.qy`<div class="container">
            <div class="row">
              <span class="header"
                >${this.value?this.hass?.localize("ui.components.file-upload.uploading_name",{name:this.value.toString()}):this.hass?.localize("ui.components.file-upload.uploading")}</span
              >
              ${this.progress?n.qy`<span class="progress"
                    >${this.progress}${(0,d.d)(this.hass.locale)}%</span
                  >`:""}
            </div>
            <mwc-linear-progress
              .indeterminate=${!this.progress}
              .progress=${this.progress?this.progress/100:void 0}
            ></mwc-linear-progress>
          </div>`:n.qy`<label
            for=${this.value?"":"input"}
            class="container ${(0,s.H)({dragged:this._drag,multiple:this.multiple,value:Boolean(this.value)})}"
            @drop=${this._handleDrop}
            @dragenter=${this._handleDragStart}
            @dragover=${this._handleDragStart}
            @dragleave=${this._handleDragEnd}
            @dragend=${this._handleDragEnd}
            >${this.value?"string"==typeof this.value?n.qy`<div class="row">
                    <div class="value" @click=${this._openFilePicker}>
                      <ha-svg-icon
                        .path=${this.icon||p}
                      ></ha-svg-icon>
                      ${this.value}
                    </div>
                    <ha-icon-button
                      @click=${this._clearValue}
                      .label=${this.hass?.localize("ui.common.delete")||"Delete"}
                      .path=${h}
                    ></ha-icon-button>
                  </div>`:(this.value instanceof FileList?Array.from(this.value):(0,c.e)(this.value)).map((e=>n.qy`<div class="row">
                        <div class="value" @click=${this._openFilePicker}>
                          <ha-svg-icon
                            .path=${this.icon||p}
                          ></ha-svg-icon>
                          ${e.name} - ${((e=0,t=2)=>{if(0===e)return"0 Bytes";t=t<0?0:t;const i=Math.floor(Math.log(e)/Math.log(1024));return`${parseFloat((e/1024**i).toFixed(t))} ${["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][i]}`})(e.size)}
                        </div>
                        <ha-icon-button
                          @click=${this._clearValue}
                          .label=${this.hass?.localize("ui.common.delete")||"Delete"}
                          .path=${h}
                        ></ha-icon-button>
                      </div>`)):n.qy`<ha-svg-icon
                    class="big-icon"
                    .path=${this.icon||p}
                  ></ha-svg-icon>
                  <ha-button unelevated @click=${this._openFilePicker}>
                    ${this.label||this.hass?.localize("ui.components.file-upload.label")}
                  </ha-button>
                  <span class="secondary"
                    >${this.secondary||this.hass?.localize("ui.components.file-upload.secondary")}</span
                  >
                  <span class="supports">${this.supports}</span>`}
            <input
              id="input"
              type="file"
              class="file"
              .accept=${this.accept}
              .multiple=${this.multiple}
              @change=${this._handleFilePicked}
          /></label>`}
    `}},{kind:"method",key:"_openFilePicker",value:function(){this._input?.click()}},{kind:"method",key:"_handleDrop",value:function(e){e.preventDefault(),e.stopPropagation(),e.dataTransfer?.files&&(0,l.r)(this,"file-picked",{files:this.multiple||1===e.dataTransfer.files.length?Array.from(e.dataTransfer.files):[e.dataTransfer.files[0]]}),this._drag=!1}},{kind:"method",key:"_handleDragStart",value:function(e){e.preventDefault(),e.stopPropagation(),this._drag=!0}},{kind:"method",key:"_handleDragEnd",value:function(e){e.preventDefault(),e.stopPropagation(),this._drag=!1}},{kind:"method",key:"_handleFilePicked",value:function(e){0!==e.target.files.length&&(this.value=e.target.files,(0,l.r)(this,"file-picked",{files:e.target.files}))}},{kind:"method",key:"_clearValue",value:function(e){e.preventDefault(),this._input.value="",this.value=void 0,(0,l.r)(this,"change")}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      :host {
        display: block;
        height: 240px;
      }
      :host([disabled]) {
        pointer-events: none;
        color: var(--disabled-text-color);
      }
      .container {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: solid 1px
          var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
        border-radius: var(--mdc-shape-small, 4px);
        height: 100%;
      }
      label.container {
        border: dashed 1px
          var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
        cursor: pointer;
      }
      :host([disabled]) .container {
        border-color: var(--disabled-color);
      }
      label.dragged {
        border-color: var(--primary-color);
      }
      .dragged:before {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: var(--primary-color);
        content: "";
        opacity: var(--dark-divider-opacity);
        pointer-events: none;
        border-radius: var(--mdc-shape-small, 4px);
      }
      label.value {
        cursor: default;
      }
      label.value.multiple {
        justify-content: unset;
        overflow: auto;
      }
      .highlight {
        color: var(--primary-color);
      }
      .row {
        display: flex;
        width: 100%;
        align-items: center;
        justify-content: space-between;
        padding: 0 16px;
        box-sizing: border-box;
      }
      ha-button {
        margin-bottom: 4px;
      }
      .supports {
        color: var(--secondary-text-color);
        font-size: 12px;
      }
      :host([disabled]) .secondary {
        color: var(--disabled-text-color);
      }
      input.file {
        display: none;
      }
      .value {
        cursor: pointer;
      }
      .value ha-svg-icon {
        margin-right: 8px;
        margin-inline-end: 8px;
        margin-inline-start: initial;
      }
      .big-icon {
        --mdc-icon-size: 48px;
        margin-bottom: 8px;
      }
      ha-button {
        --mdc-button-outline-color: var(--primary-color);
        --mdc-icon-button-size: 24px;
      }
      mwc-linear-progress {
        width: 100%;
        padding: 16px;
        box-sizing: border-box;
      }
      .header {
        font-weight: 500;
      }
      .progress {
        color: var(--secondary-text-color);
      }
    `}}]}}),n.WF)},8966:(e,t,i)=>{i.d(t,{Q:()=>o,n:()=>a});const o=async(e,t)=>{const i=new FormData;i.append("file",t);const o=await e.fetchWithAuth("/api/file_upload",{method:"POST",body:i});if(413===o.status)throw new Error(`Uploaded file is too large (${t.name})`);if(200!==o.status)throw new Error("Unknown error");return(await o.json()).file_id},a=async(e,t)=>e.callApi("DELETE","file_upload",{file_id:t})},2263:(e,t,i)=>{i.d(t,{PS:()=>o,VR:()=>a});const o=e=>e.data,a=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])},1447:(e,t,i)=>{i.d(t,{K$:()=>r,an:()=>l,dk:()=>s});var o=i(3167);const a=()=>Promise.all([i.e(2658),i.e(4475)]).then(i.bind(i,4475)),n=(e,t,i)=>new Promise((n=>{const r=t.cancel,s=t.confirm;(0,o.r)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:a,dialogParams:{...t,...i,cancel:()=>{n(!!i?.prompt&&null),r&&r()},confirm:e=>{n(!i?.prompt||e),s&&s(e)}}})})),r=(e,t)=>n(e,t),s=(e,t)=>n(e,t,{confirmation:!0}),l=(e,t)=>n(e,t,{prompt:!0})},7341:(e,t,i)=>{var o=i(5461),a=i(9534),n=i(8597),r=i(196),s=i(9760),l=i(5081),d=i(7626),c=(i(2312),i(2010),i(9222),i(9278)),h=i(2431),p=i(7515);(0,o.A)([(0,r.EM)("ha-ripple")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:"attachableTouchController",value(){return new h.i(this,this.onTouchControlChange.bind(this))}},{kind:"method",key:"attach",value:function(e){(0,a.A)(i,"attach",this,3)([e]),this.attachableTouchController.attach(e)}},{kind:"method",key:"detach",value:function(){(0,a.A)(i,"detach",this,3)([]),this.attachableTouchController.detach()}},{kind:"field",key:"_handleTouchEnd",value(){return()=>{this.disabled||(0,a.A)(i,"endPressAnimation",this,3)([])}}},{kind:"method",key:"onTouchControlChange",value:function(e,t){e?.removeEventListener("touchend",this._handleTouchEnd),t?.addEventListener("touchend",this._handleTouchEnd)}},{kind:"field",static:!0,key:"styles",value(){return[...(0,a.A)(i,"styles",this),n.AH`
      :host {
        --md-ripple-hover-opacity: var(--ha-ripple-hover-opacity, 0.08);
        --md-ripple-pressed-opacity: var(--ha-ripple-pressed-opacity, 0.12);
        --md-ripple-hover-color: var(
          --ha-ripple-hover-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );
        --md-ripple-pressed-color: var(
          --ha-ripple-pressed-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );
      }
    `]}}]}}),p.o),(0,o.A)([(0,r.EM)("ha-tab")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"active",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)()],key:"name",value:void 0},{kind:"method",key:"render",value:function(){return n.qy`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${(0,c.J)(this.name)}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?n.qy`<slot name="icon"></slot>`:""}
        <span class="name">${this.name}</span>
        <ha-ripple></ha-ripple>
      </div>
    `}},{kind:"method",key:"_handleKeyDown",value:function(e){"Enter"===e.key&&e.target.click()}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      div {
        padding: 0 32px;
        display: flex;
        flex-direction: column;
        text-align: center;
        box-sizing: border-box;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: var(--header-height);
        cursor: pointer;
        position: relative;
        outline: none;
      }

      .name {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
      }

      :host([active]) {
        color: var(--primary-color);
      }

      :host(:not([narrow])[active]) div {
        border-bottom: 2px solid var(--primary-color);
      }

      :host([narrow]) {
        min-width: 0;
        display: flex;
        justify-content: center;
        overflow: hidden;
      }

      :host([narrow]) div {
        padding: 0 4px;
      }

      div:focus-visible:before {
        position: absolute;
        display: block;
        content: "";
        inset: 0;
        background-color: var(--secondary-text-color);
        opacity: 0.08;
      }
    `}}]}}),n.WF);var u=i(3799),v=i(6041),f=i(2872);const k=(e,t)=>!t.component||(0,v.e)(t.component).some((t=>(0,f.x)(e,t))),b=(e,t)=>!t.not_component||!(0,v.e)(t.not_component).some((t=>(0,f.x)(e,t))),g=e=>e.core,x=(e,t)=>(e=>e.advancedOnly)(t)&&!(e=>e.userData?.showAdvanced)(e);(0,o.A)([(0,r.EM)("hass-tabs-subpage")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"supervisor",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"main-page"})],key:"mainPage",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"pane",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_activeTab",value:void 0},{kind:"field",decorators:[(0,d.a)(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return(0,l.A)(((e,t,i,o,a,r)=>{const s=e.filter((e=>((e,t)=>(g(t)||k(e,t))&&!x(e,t)&&b(e,t))(this.hass,e)));if(s.length<2){if(1===s.length){const e=s[0];return[e.translationKey?r(e.translationKey):e.name]}return[""]}return s.map((e=>n.qy`
          <a href=${e.path}>
            <ha-tab
              .hass=${this.hass}
              .active=${e.path===t?.path}
              .narrow=${this.narrow}
              .name=${e.translationKey?r(e.translationKey):e.name}
            >
              ${e.iconPath?n.qy`<ha-svg-icon
                    slot="icon"
                    .path=${e.iconPath}
                  ></ha-svg-icon>`:""}
            </ha-tab>
          </a>
        `))}))}},{kind:"method",key:"willUpdate",value:function(e){e.has("route")&&(this._activeTab=this.tabs.find((e=>`${this.route.prefix}${this.route.path}`.includes(e.path)))),(0,a.A)(i,"willUpdate",this,3)([e])}},{kind:"method",key:"render",value:function(){const e=this._getTabs(this.tabs,this._activeTab,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),t=e.length>1;return n.qy`
      <div class="toolbar">
        <slot name="toolbar">
          <div class="toolbar-content">
            ${this.mainPage||!this.backPath&&history.state?.root?n.qy`
                  <ha-menu-button
                    .hassio=${this.supervisor}
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                `:this.backPath?n.qy`
                    <a href=${this.backPath}>
                      <ha-icon-button-arrow-prev
                        .hass=${this.hass}
                      ></ha-icon-button-arrow-prev>
                    </a>
                  `:n.qy`
                    <ha-icon-button-arrow-prev
                      .hass=${this.hass}
                      @click=${this._backTapped}
                    ></ha-icon-button-arrow-prev>
                  `}
            ${this.narrow||!t?n.qy`<div class="main-title">
                  <slot name="header">${t?"":e[0]}</slot>
                </div>`:""}
            ${t&&!this.narrow?n.qy`<div id="tabbar">${e}</div>`:""}
            <div id="toolbar-icon">
              <slot name="toolbar-icon"></slot>
            </div>
          </div>
        </slot>
        ${t&&this.narrow?n.qy`<div id="tabbar" class="bottom-bar">${e}</div>`:""}
      </div>
      <div class="container">
        ${this.pane?n.qy`<div class="pane">
              <div class="shadow-container"></div>
              <div class="ha-scrollbar">
                <slot name="pane"></slot>
              </div>
            </div>`:n.s6}
        <div
          class="content ha-scrollbar ${(0,s.H)({tabs:t})}"
          @scroll=${this._saveScrollPos}
        >
          <slot></slot>
        </div>
      </div>
      <div id="fab" class=${(0,s.H)({tabs:t})}>
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[(0,r.Ls)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[u.dp,n.AH`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }

        :host([narrow]) {
          width: 100%;
          position: fixed;
        }

        .container {
          display: flex;
          height: calc(100% - var(--header-height));
        }

        :host([narrow]) .container {
          height: 100%;
        }

        ha-menu-button {
          margin-right: 24px;
          margin-inline-end: 24px;
          margin-inline-start: initial;
        }

        .toolbar {
          font-size: 20px;
          height: var(--header-height);
          background-color: var(--sidebar-background-color);
          font-weight: 400;
          border-bottom: 1px solid var(--divider-color);
          box-sizing: border-box;
        }
        .toolbar-content {
          padding: 8px 12px;
          display: flex;
          align-items: center;
          height: 100%;
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar-content {
            padding: 4px;
          }
        }
        .toolbar a {
          color: var(--sidebar-text-color);
          text-decoration: none;
        }
        .bottom-bar a {
          width: 25%;
        }

        #tabbar {
          display: flex;
          font-size: 14px;
          overflow: hidden;
        }

        #tabbar > a {
          overflow: hidden;
          max-width: 45%;
        }

        #tabbar.bottom-bar {
          position: absolute;
          bottom: 0;
          left: 0;
          padding: 0 16px;
          box-sizing: border-box;
          background-color: var(--sidebar-background-color);
          border-top: 1px solid var(--divider-color);
          justify-content: space-around;
          z-index: 2;
          font-size: 12px;
          width: 100%;
          padding-bottom: env(safe-area-inset-bottom);
        }

        #tabbar:not(.bottom-bar) {
          flex: 1;
          justify-content: center;
        }

        :host(:not([narrow])) #toolbar-icon {
          min-width: 40px;
        }

        ha-menu-button,
        ha-icon-button-arrow-prev,
        ::slotted([slot="toolbar-icon"]) {
          display: flex;
          flex-shrink: 0;
          pointer-events: auto;
          color: var(--sidebar-icon-color);
        }

        .main-title {
          flex: 1;
          max-height: var(--header-height);
          line-height: 20px;
          color: var(--sidebar-text-color);
          margin: var(--main-title-margin, var(--margin-title));
        }

        .content {
          position: relative;
          width: calc(
            100% - env(safe-area-inset-left) - env(safe-area-inset-right)
          );
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
          margin-inline-start: env(safe-area-inset-left);
          margin-inline-end: env(safe-area-inset-right);
          overflow: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([narrow]) .content.tabs {
          height: calc(100% - 2 * var(--header-height));
          height: calc(
            100% - 2 * var(--header-height) - env(safe-area-inset-bottom)
          );
        }

        #fab {
          position: fixed;
          right: calc(16px + env(safe-area-inset-right));
          inset-inline-end: calc(16px + env(safe-area-inset-right));
          inset-inline-start: initial;
          bottom: calc(16px + env(safe-area-inset-bottom));
          z-index: 1;
          display: flex;
          flex-wrap: wrap;
          justify-content: flex-end;
          gap: 8px;
        }
        :host([narrow]) #fab.tabs {
          bottom: calc(84px + env(safe-area-inset-bottom));
        }
        #fab[is-wide] {
          bottom: 24px;
          right: 24px;
          inset-inline-end: 24px;
          inset-inline-start: initial;
        }

        .pane {
          border-right: 1px solid var(--divider-color);
          border-inline-end: 1px solid var(--divider-color);
          border-inline-start: initial;
          box-sizing: border-box;
          display: flex;
          flex: 0 0 var(--sidepane-width, 250px);
          width: var(--sidepane-width, 250px);
          flex-direction: column;
          position: relative;
        }
        .pane .ha-scrollbar {
          flex: 1;
        }
      `]}}]}}),n.WF)},9184:(e,t,i)=>{i.r(t),i.d(t,{KNXInfo:()=>u});var o=i(5461),a=i(8597),n=i(196),r=i(3167),s=(i(4392),i(7341),i(6494),i(6287),i(4259),i(8966)),l=i(2263),d=i(1447),c=i(9987),h=i(1328);const p=new h.Q("info");let u=(0,o.A)([(0,n.EM)("knx-info")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_projectPassword",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_uploading",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_projectFile",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${this.tabs}
        .localizeFunc=${this.knx.localize}
      >
        <div class="columns">
          ${this._renderInfoCard()}
          ${this.knx.info.project?this._renderProjectDataCard(this.knx.info.project):a.s6}
          ${this._renderProjectUploadCard()}
        </div>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_renderInfoCard",value:function(){return a.qy` <ha-card class="knx-info">
      <div class="card-content knx-info-section">
        <div class="knx-content-row header">${this.knx.localize("info_information_header")}</div>

        <div class="knx-content-row">
          <div>XKNX Version</div>
          <div>${this.knx.info.version}</div>
        </div>

        <div class="knx-content-row">
          <div>KNX-Frontend Version</div>
          <div>${"2024.9.10.221729"}</div>
        </div>

        <div class="knx-content-row">
          <div>${this.knx.localize("info_connected_to_bus")}</div>
          <div>
            ${this.hass.localize(this.knx.info.connected?"ui.common.yes":"ui.common.no")}
          </div>
        </div>

        <div class="knx-content-row">
          <div>${this.knx.localize("info_individual_address")}</div>
          <div>${this.knx.info.current_address}</div>
        </div>

        <div class="knx-bug-report">
          ${this.knx.localize("info_issue_tracker")}
          <a href="https://github.com/XKNX/knx-integration" target="_blank">xknx/knx-integration</a>
        </div>

        <div class="knx-bug-report">
          ${this.knx.localize("info_my_knx")}
          <a href="https://my.knx.org" target="_blank">my.knx.org</a>
      </div>
    </ha-card>`}},{kind:"method",key:"_renderProjectDataCard",value:function(e){return a.qy`
      <ha-card class="knx-info">
          <div class="card-content knx-content">
            <div class="header knx-content-row">
              ${this.knx.localize("info_project_data_header")}
            </div>
            <div class="knx-content-row">
              <div>${this.knx.localize("info_project_data_name")}</div>
              <div>${e.name}</div>
            </div>
            <div class="knx-content-row">
              <div>${this.knx.localize("info_project_data_last_modified")}</div>
              <div>${new Date(e.last_modified).toUTCString()}</div>
            </div>
            <div class="knx-content-row">
              <div>${this.knx.localize("info_project_data_tool_version")}</div>
              <div>${e.tool_version}</div>
            </div>
            <div class="knx-content-row">
              <div>${this.knx.localize("info_project_data_xknxproject_version")}</div>
              <div>${e.xknxproject_version}</div>
            </div>
            <div class="knx-button-row">
              <ha-button
                class="knx-warning push-right"
                @click=${this._removeProject}
                .disabled=${this._uploading||!this.knx.info.project}
                >
                ${this.knx.localize("info_project_delete")}
              </ha-button>
            </div>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_renderProjectUploadCard",value:function(){return a.qy` <ha-card class="knx-info">
      <div class="card-content knx-content">
        <div class="knx-content-row header">${this.knx.localize("info_project_file_header")}</div>
        <div class="knx-content-row">${this.knx.localize("info_project_upload_description")}</div>
        <div class="knx-content-row">
          <ha-file-upload
            .hass=${this.hass}
            accept=".knxproj, .knxprojarchive"
            .icon=${"M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z"}
            .label=${this.knx.localize("info_project_file")}
            .value=${this._projectFile?.name}
            .uploading=${this._uploading}
            @file-picked=${this._filePicked}
          ></ha-file-upload>
        </div>
        <div class="knx-content-row">
          <ha-selector-text
            .hass=${this.hass}
            .value=${this._projectPassword||""}
            .label=${this.hass.localize("ui.login-form.password")}
            .selector=${{text:{multiline:!1,type:"password"}}}
            .required=${!1}
            @value-changed=${this._passwordChanged}
          >
          </ha-selector-text>
        </div>
        <div class="knx-button-row">
          <ha-button
            class="push-right"
            @click=${this._uploadFile}
            .disabled=${this._uploading||!this._projectFile}
            >${this.hass.localize("ui.common.submit")}</ha-button
          >
        </div>
      </div>
    </ha-card>`}},{kind:"method",key:"_filePicked",value:function(e){this._projectFile=e.detail.files[0]}},{kind:"method",key:"_passwordChanged",value:function(e){this._projectPassword=e.detail.value}},{kind:"method",key:"_uploadFile",value:async function(e){const t=this._projectFile;if(void 0===t)return;let i;this._uploading=!0;try{const e=await(0,s.Q)(this.hass,t);await(0,c.dc)(this.hass,e,this._projectPassword||"")}catch(o){i=o,(0,d.K$)(this,{title:"Upload failed",text:(0,l.VR)(o)})}finally{i||(this._projectFile=void 0,this._projectPassword=void 0),this._uploading=!1,(0,r.r)(this,"knx-reload")}}},{kind:"method",key:"_removeProject",value:async function(e){if(await(0,d.dk)(this,{text:this.knx.localize("info_project_delete")}))try{await(0,c.gV)(this.hass)}catch(t){(0,d.K$)(this,{title:"Deletion failed",text:(0,l.VR)(t)})}finally{(0,r.r)(this,"knx-reload")}else p.debug("User cancelled deletion")}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      .columns {
        display: flex;
        justify-content: center;
      }

      @media screen and (max-width: 1232px) {
        .columns {
          flex-direction: column;
        }

        .knx-button-row {
          margin-top: 20px;
        }

        .knx-info {
          margin-right: 8px;
        }
      }

      @media screen and (min-width: 1233px) {
        .knx-button-row {
          margin-top: auto;
        }

        .knx-info {
          width: 400px;
        }
      }

      .knx-info {
        margin-left: 8px;
        margin-top: 8px;
      }

      .knx-content {
        display: flex;
        flex-direction: column;
        height: 100%;
        box-sizing: border-box;
      }

      .knx-content-row {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
      }

      .knx-content-row > div:nth-child(2) {
        margin-left: 1rem;
      }

      .knx-button-row {
        display: flex;
        flex-direction: row;
        vertical-align: bottom;
        padding-top: 16px;
      }

      .push-left {
        margin-right: auto;
      }

      .push-right {
        margin-left: auto;
      }

      .knx-warning {
        --mdc-theme-primary: var(--error-color);
      }

      .knx-project-description {
        margin-top: -8px;
        padding: 0px 16px 16px;
      }

      .knx-delete-project-button {
        position: absolute;
        bottom: 0;
        right: 0;
      }

      .knx-bug-report {
        margin-top: 20px;

        a {
          text-decoration: none;
        }
      }

      .header {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 48px;
        padding: -4px 16px 16px;
        display: inline-block;
        margin-block-start: 0px;
        margin-block-end: 4px;
        font-weight: normal;
      }

      ha-file-upload,
      ha-selector-text {
        width: 100%;
        margin-top: 8px;
      }
    `}}]}}),a.WF)}};
//# sourceMappingURL=qa2topQ6.js.map