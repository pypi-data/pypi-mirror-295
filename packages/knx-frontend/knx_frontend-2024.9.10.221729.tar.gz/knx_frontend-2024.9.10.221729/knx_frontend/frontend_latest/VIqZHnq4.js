export const id=2293;export const ids=[2293];export const modules={678:(e,t,i)=>{i.d(t,{T:()=>s});var a=i(5081);const s=(e,t)=>{try{return o(t)?.of(e)??e}catch{return e}},o=(0,a.A)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})))},2714:(e,t,i)=>{var a=i(5461),s=i(8597),o=i(196);(0,a.A)([(0,o.EM)("ha-dialog-header")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return s.qy`
      <header class="header">
        <div class="header-bar">
          <section class="header-navigation-icon">
            <slot name="navigationIcon"></slot>
          </section>
          <section class="header-title">
            <slot name="title"></slot>
          </section>
          <section class="header-action-items">
            <slot name="actionItems"></slot>
          </section>
        </div>
        <slot></slot>
      </header>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[s.AH`
        :host {
          display: block;
        }
        :host([show-border]) {
          border-bottom: 1px solid
            var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
        }
        .header-bar {
          display: flex;
          flex-direction: row;
          align-items: flex-start;
          padding: 4px;
          box-sizing: border-box;
        }
        .header-title {
          flex: 1;
          font-size: 22px;
          line-height: 28px;
          font-weight: 400;
          padding: 10px 4px;
          min-width: 0;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        @media all and (min-width: 450px) and (min-height: 500px) {
          .header-bar {
            padding: 12px;
          }
        }
        .header-navigation-icon {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
        .header-action-items {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
      `]}}]}}),s.WF)},1729:(e,t,i)=>{var a={};i.r(a);var s=i(5461),o=i(9534),n=i(8597),r=i(196),d=i(5081),l=i(3167),c=i(4517),h=i(678),u=i(6412);i(9484),i(6334);(0,s.A)([(0,r.EM)("ha-language-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array})],key:"languages",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"nativeName",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"noSort",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_defaultLanguages",value(){return[]}},{kind:"field",decorators:[(0,r.P)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,o.A)(i,"firstUpdated",this,3)([e]),this._computeDefaultLanguageOptions()}},{kind:"method",key:"updated",value:function(e){(0,o.A)(i,"updated",this,3)([e]);const t=e.has("hass")&&this.hass&&e.get("hass")&&e.get("hass").locale.language!==this.hass.locale.language;if(e.has("languages")||e.has("value")||t){if(this._select.layoutOptions(),this._select.value!==this.value&&(0,l.r)(this,"value-changed",{value:this._select.value}),!this.value)return;const e=this._getLanguagesOptions(this.languages??this._defaultLanguages,this.nativeName,this.hass?.locale).findIndex((e=>e.value===this.value));-1===e&&(this.value=void 0),t&&this._select.select(e)}}},{kind:"field",key:"_getLanguagesOptions",value(){return(0,d.A)(((e,t,i)=>{let s=[];if(t){const t=a.translationMetadata.translations;s=e.map((e=>{let i=t[e]?.nativeName;if(!i)try{i=new Intl.DisplayNames(e,{type:"language",fallback:"code"}).of(e)}catch(a){i=e}return{value:e,label:i}}))}else i&&(s=e.map((e=>({value:e,label:(0,h.T)(e,i)}))));return!this.noSort&&i&&s.sort(((e,t)=>(0,u.S)(e.label,t.label,i.language))),s}))}},{kind:"method",key:"_computeDefaultLanguageOptions",value:function(){this._defaultLanguages=Object.keys(a.translationMetadata.translations)}},{kind:"method",key:"render",value:function(){const e=this._getLanguagesOptions(this.languages??this._defaultLanguages,this.nativeName,this.hass?.locale),t=this.value??(this.required?e[0]?.value:this.value);return n.qy`
      <ha-select
        .label=${this.label??(this.hass?.localize("ui.components.language-picker.language")||"Language")}
        .value=${t||""}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${c.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${0===e.length?n.qy`<ha-list-item value=""
              >${this.hass?.localize("ui.components.language-picker.no_languages")||"No languages"}</ha-list-item
            >`:e.map((e=>n.qy`
                <ha-list-item .value=${e.value}
                  >${e.label}</ha-list-item
                >
              `))}
      </ha-select>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;""!==t.value&&t.value!==this.value&&(this.value=t.value,(0,l.r)(this,"value-changed",{value:this.value}))}}]}}),n.WF)},5973:(e,t,i)=>{var a=i(5461),s=i(9534),o=i(8597),n=i(196),r=i(3167),d=i(4517),l=i(1355),c=i(6933);i(9484),i(6334);const h="__NONE_OPTION__";(0,a.A)([(0,n.EM)("ha-tts-voice-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"engineId",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_voices",value:void 0},{kind:"field",decorators:[(0,n.P)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"render",value:function(){if(!this._voices)return o.s6;const e=this.value??(this.required?this._voices[0]?.voice_id:h);return o.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.tts-voice-picker.voice")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${d.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?o.s6:o.qy`<ha-list-item .value=${h}>
              ${this.hass.localize("ui.components.tts-voice-picker.none")}
            </ha-list-item>`}
        ${this._voices.map((e=>o.qy`<ha-list-item .value=${e.voice_id}>
              ${e.name}
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,s.A)(i,"willUpdate",this,3)([e]),this.hasUpdated?(e.has("language")||e.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}},{kind:"field",key:"_debouncedUpdateVoices",value(){return(0,l.s)((()=>this._updateVoices()),500)}},{kind:"method",key:"_updateVoices",value:async function(){this.engineId&&this.language?(this._voices=(await(0,c.z3)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((e=>e.voice_id===this.value))||(this.value=void 0,(0,r.r)(this,"value-changed",{value:this.value})))):this._voices=void 0}},{kind:"method",key:"updated",value:function(e){(0,s.A)(i,"updated",this,3)([e]),e.has("_voices")&&this._select?.value!==this.value&&(this._select?.layoutOptions(),(0,r.r)(this,"value-changed",{value:this._select?.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===h||(this.value=t.value===h?void 0:t.value,(0,r.r)(this,"value-changed",{value:this.value}))}}]}}),o.WF)},2293:(e,t,i)=>{var a=i(5461),s=i(8597),o=i(196),n=i(3167),r=i(3799),d=(i(8762),i(2714),i(8068),i(2462));i(9222);(0,a.A)([(0,o.EM)("ha-media-manage-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"currentItem",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_uploading",value(){return 0}},{kind:"method",key:"render",value:function(){return this.currentItem&&(0,d.Jz)(this.currentItem.media_content_id||"")?s.qy`
      <mwc-button
        .label=${this.hass.localize("ui.components.media-browser.file_management.manage")}
        @click=${this._manage}
      >
        <ha-svg-icon .path=${"M19.39 10.74L11 19.13V20H4C2.9 20 2 19.11 2 18V6C2 4.89 2.89 4 4 4H10L12 6H20C21.1 6 22 6.89 22 8V10.15C21.74 10.06 21.46 10 21.17 10C20.5 10 19.87 10.26 19.39 10.74M13 19.96V22H15.04L21.17 15.88L19.13 13.83L13 19.96M22.85 13.47L21.53 12.15C21.33 11.95 21 11.95 20.81 12.15L19.83 13.13L21.87 15.17L22.85 14.19C23.05 14 23.05 13.67 22.85 13.47Z"} slot="icon"></ha-svg-icon>
      </mwc-button>
    `:s.s6}},{kind:"method",key:"_manage",value:function(){var e,t;e=this,t={currentItem:this.currentItem,onClose:()=>(0,n.r)(this,"media-refresh")},(0,n.r)(e,"show-dialog",{dialogTag:"dialog-media-manage",dialogImport:()=>i.e(6414).then(i.bind(i,6414)),dialogParams:t})}},{kind:"field",static:!0,key:"styles",value(){return s.AH`
    mwc-button {
      /* We use icon + text to show disabled state */
      --mdc-button-disabled-ink-color: --mdc-theme-primary;
    }

    ha-svg-icon[slot="icon"],
    ha-circular-progress[slot="icon"] {
      vertical-align: middle;
    }

    ha-svg-icon[slot="icon"] {
      margin-inline-start: 0px;
      margin-inline-end: 8px;
      direction: var(--direction);
    }
  `}}]}}),s.WF);i(5193);var l=i(4517);(0,a.A)([(0,o.EM)("dialog-media-player-browse")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_currentItem",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_navigateIds",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_preferredLayout",value(){return"auto"}},{kind:"field",decorators:[(0,o.P)("ha-media-player-browse")],key:"_browser",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._navigateIds=e.navigateIds||[{media_content_id:void 0,media_content_type:void 0}]}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._navigateIds=void 0,this._currentItem=void 0,this._preferredLayout="auto",this.classList.remove("opened"),(0,n.r)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params&&this._navigateIds?s.qy`
      <ha-dialog
        open
        scrimClickAction
        escapeKeyAction
        hideActions
        flexContent
        .heading=${this._currentItem?this._currentItem.title:this.hass.localize("ui.components.media-browser.media-player-browser")}
        @closed=${this.closeDialog}
        @opened=${this._dialogOpened}
      >
        <ha-dialog-header show-border slot="heading">
          ${this._navigateIds.length>1?s.qy`
                <ha-icon-button
                  slot="navigationIcon"
                  .path=${"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}
                  @click=${this._goBack}
                ></ha-icon-button>
              `:s.s6}
          <span slot="title">
            ${this._currentItem?this._currentItem.title:this.hass.localize("ui.components.media-browser.media-player-browser")}
          </span>
          <ha-media-manage-button
            slot="actionItems"
            .hass=${this.hass}
            .currentItem=${this._currentItem}
            @media-refresh=${this._refreshMedia}
          ></ha-media-manage-button>
          <ha-button-menu
            slot="actionItems"
            @action=${this._handleMenuAction}
            @closed=${l.d}
            fixed
          >
            <ha-icon-button
              slot="trigger"
              .label=${this.hass.localize("ui.common.menu")}
              .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
            ></ha-icon-button>
            <mwc-list-item graphic="icon">
              ${this.hass.localize("ui.components.media-browser.auto")}
              <ha-svg-icon
                class=${"auto"===this._preferredLayout?"selected_menu_item":""}
                slot="graphic"
                .path=${"M3,5A2,2 0 0,1 5,3H19A2,2 0 0,1 21,5V19A2,2 0 0,1 19,21H5C3.89,21 3,20.1 3,19V5M5,5V19H19V5H5M11,7H13A2,2 0 0,1 15,9V17H13V13H11V17H9V9A2,2 0 0,1 11,7M11,9V11H13V9H11Z"}
              ></ha-svg-icon>
            </mwc-list-item>
            <mwc-list-item graphic="icon">
              ${this.hass.localize("ui.components.media-browser.grid")}
              <ha-svg-icon
                class=${"grid"===this._preferredLayout?"selected_menu_item":""}
                slot="graphic"
                .path=${"M10,4V8H14V4H10M16,4V8H20V4H16M16,10V14H20V10H16M16,16V20H20V16H16M14,20V16H10V20H14M8,20V16H4V20H8M8,14V10H4V14H8M8,8V4H4V8H8M10,14H14V10H10V14M4,2H20A2,2 0 0,1 22,4V20A2,2 0 0,1 20,22H4C2.92,22 2,21.1 2,20V4A2,2 0 0,1 4,2Z"}
              ></ha-svg-icon>
            </mwc-list-item>
            <mwc-list-item graphic="icon">
              ${this.hass.localize("ui.components.media-browser.list")}
              <ha-svg-icon
                slot="graphic"
                class=${"list"===this._preferredLayout?"selected_menu_item":""}
                .path=${"M11 15H17V17H11V15M9 7H7V9H9V7M11 13H17V11H11V13M11 9H17V7H11V9M9 11H7V13H9V11M21 5V19C21 20.1 20.1 21 19 21H5C3.9 21 3 20.1 3 19V5C3 3.9 3.9 3 5 3H19C20.1 3 21 3.9 21 5M19 5H5V19H19V5M9 15H7V17H9V15Z"}
              ></ha-svg-icon>
            </mwc-list-item>
          </ha-button-menu>
          <ha-icon-button
            .label=${this.hass.localize("ui.dialogs.generic.close")}
            .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
            dialogAction="close"
            slot="actionItems"
          ></ha-icon-button>
        </ha-dialog-header>
        <ha-media-player-browse
          dialog
          .hass=${this.hass}
          .entityId=${this._params.entityId}
          .navigateIds=${this._navigateIds}
          .action=${this._action}
          .preferredLayout=${this._preferredLayout}
          @close-dialog=${this.closeDialog}
          @media-picked=${this._mediaPicked}
          @media-browsed=${this._mediaBrowsed}
        ></ha-media-player-browse>
      </ha-dialog>
    `:s.s6}},{kind:"method",key:"_dialogOpened",value:function(){this.classList.add("opened")}},{kind:"method",key:"_handleMenuAction",value:async function(e){switch(e.detail.index){case 0:this._preferredLayout="auto";break;case 1:this._preferredLayout="grid";break;case 2:this._preferredLayout="list"}}},{kind:"method",key:"_goBack",value:function(){this._navigateIds=this._navigateIds?.slice(0,-1),this._currentItem=void 0}},{kind:"method",key:"_mediaBrowsed",value:function(e){this._navigateIds=e.detail.ids,this._currentItem=e.detail.current}},{kind:"method",key:"_mediaPicked",value:function(e){this._params.mediaPickedCallback(e.detail),"play"!==this._action&&this.closeDialog()}},{kind:"get",key:"_action",value:function(){return this._params.action||"play"}},{kind:"method",key:"_refreshMedia",value:function(){this._browser.refresh()}},{kind:"get",static:!0,key:"styles",value:function(){return[r.nA,s.AH`
        ha-dialog {
          --dialog-z-index: 9;
          --dialog-content-padding: 0;
        }

        ha-media-player-browse {
          --media-browser-max-height: calc(100vh - 65px);
        }

        :host(.opened) ha-media-player-browse {
          height: calc(100vh - 65px);
        }

        @media (min-width: 800px) {
          ha-dialog {
            --mdc-dialog-max-width: 800px;
            --dialog-surface-position: fixed;
            --dialog-surface-top: 40px;
            --mdc-dialog-max-height: calc(100vh - 72px);
          }
          ha-media-player-browse {
            position: initial;
            --media-browser-max-height: 100vh - 137px;
            width: 700px;
          }
        }

        ha-dialog-header ha-media-manage-button {
          --mdc-theme-primary: var(--primary-text-color);
          margin: 6px;
          display: block;
        }
      `]}}]}}),s.WF)},5193:(e,t,i)=>{var a=i(5461),s=i(9534),o=i(4288),n=(i(8068),i(9805),i(3981),i(7777),i(8597)),r=i(196),d=i(9760),l=i(2506),c=i(6625),h=i(3167),u=i(1355),m=i(6601),p=i(3728),g=i(2462),v=i(6933),_=i(1447),y=i(3799),f=i(7424),k=i(1750),b=(i(5067),i(1074),i(920),i(4392),i(3279),i(7661),i(6396),i(9222),i(7905));i(7984),i(1729),i(5973);(0,a.A)([(0,r.EM)("ha-browse-media-tts")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"item",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"action",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_language",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_voice",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_provider",value:void 0},{kind:"field",decorators:[(0,b.I)({key:"TtsMessage",state:!0,subscribe:!1})],key:"_message",value:void 0},{kind:"method",key:"render",value:function(){return n.qy`<ha-card>
      <div class="card-content">
        <ha-textarea
          autogrow
          .label=${this.hass.localize("ui.components.media-browser.tts.message")}
          .value=${this._message||this.hass.localize("ui.components.media-browser.tts.example_message",{name:this.hass.user?.name||"Alice"})}
        >
        </ha-textarea>
        ${this._provider?.supported_languages?.length?n.qy` <div class="options">
              <ha-language-picker
                .hass=${this.hass}
                .languages=${this._provider.supported_languages}
                .value=${this._language}
                required
                @value-changed=${this._languageChanged}
              ></ha-language-picker>
              <ha-tts-voice-picker
                .hass=${this.hass}
                .value=${this._voice}
                .engineId=${this._provider.engine_id}
                .language=${this._language}
                required
                @value-changed=${this._voiceChanged}
              ></ha-tts-voice-picker>
            </div>`:n.s6}
      </div>
      <div class="card-actions">
        <mwc-button @click=${this._ttsClicked}>
          ${this.hass.localize(`ui.components.media-browser.tts.action_${this.action}`)}
        </mwc-button>
      </div>
    </ha-card> `}},{kind:"method",key:"willUpdate",value:function(e){if((0,s.A)(i,"willUpdate",this,3)([e]),e.has("item")&&this.item.media_content_id){const e=new URLSearchParams(this.item.media_content_id.split("?")[1]),i=e.get("message"),a=e.get("language"),s=e.get("voice");i&&(this._message=i),a&&(this._language=a),s&&(this._voice=s);const o=(0,v.EF)(this.item.media_content_id);o!==this._provider?.engine_id&&(this._provider=void 0,(0,v.u1)(this.hass,o).then((e=>{if(this._provider=e.provider,!this._language&&e.provider.supported_languages?.length){const t=`${this.hass.config.language}-${this.hass.config.country}`.toLowerCase(),i=e.provider.supported_languages.find((e=>e.toLowerCase()===t));if(i)return void(this._language=i);this._language=e.provider.supported_languages?.find((e=>e.substring(0,2)===this.hass.config.language.substring(0,2)))}})),"cloud"===o&&(t=this.hass,t.callWS({type:"cloud/status"})).then((e=>{e.logged_in&&(this._language=e.prefs.tts_default_voice[0])})))}var t;if(e.has("_message"))return;const a=this.shadowRoot.querySelector("ha-textarea")?.value;void 0!==a&&a!==this._message&&(this._message=a)}},{kind:"method",key:"_languageChanged",value:function(e){this._language=e.detail.value}},{kind:"method",key:"_voiceChanged",value:function(e){this._voice=e.detail.value}},{kind:"method",key:"_ttsClicked",value:async function(){const e=this.shadowRoot.querySelector("ha-textarea").value;this._message=e;const t={...this.item},i=new URLSearchParams;i.append("message",e),this._language&&i.append("language",this._language),this._voice&&i.append("voice",this._voice),t.media_content_id=`${t.media_content_id.split("?")[0]}?${i.toString()}`,t.can_play=!0,t.title=e,(0,h.r)(this,"tts-picked",{item:t})}},{kind:"field",static:!0,key:"styles",value(){return[y.og,n.AH`
      :host {
        margin: 16px auto;
        padding: 0 8px;
        display: flex;
        flex-direction: column;
        max-width: 448px;
      }
      .options {
        margin-top: 16px;
        display: flex;
        justify-content: space-between;
      }
      ha-textarea {
        width: 100%;
      }
      button.link {
        color: var(--primary-color);
      }
    `]}}]}}),n.WF);var w=i(1646);const x="M8,5.14V19.14L19,12.14L8,5.14Z",$="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z";(0,a.A)([(0,r.EM)("ha-media-player-browse")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"entityId",value:void 0},{kind:"field",decorators:[(0,r.MZ)()],key:"action",value(){return"play"}},{kind:"field",decorators:[(0,r.MZ)()],key:"preferredLayout",value(){return"auto"}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"dialog",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"navigateIds",value(){return[]}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"scrolled",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_parentItem",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_currentItem",value:void 0},{kind:"field",decorators:[(0,r.P)(".header")],key:"_header",value:void 0},{kind:"field",decorators:[(0,r.P)(".content")],key:"_content",value:void 0},{kind:"field",decorators:[(0,r.P)("lit-virtualizer")],key:"_virtualizer",value:void 0},{kind:"field",key:"_observed",value(){return!1}},{kind:"field",key:"_headerOffsetHeight",value(){return 0}},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,s.A)(i,"connectedCallback",this,3)([]),this.updateComplete.then((()=>this._attachResizeObserver()))}},{kind:"method",key:"disconnectedCallback",value:function(){(0,s.A)(i,"disconnectedCallback",this,3)([]),this._resizeObserver&&this._resizeObserver.disconnect()}},{kind:"method",key:"refresh",value:async function(){const e=this.navigateIds[this.navigateIds.length-1];try{this._currentItem=await this._fetchData(this.entityId,e.media_content_id,e.media_content_type),(0,h.r)(this,"media-browsed",{ids:this.navigateIds,current:this._currentItem})}catch(t){this._setError(t)}}},{kind:"method",key:"play",value:function(){this._currentItem?.can_play&&this._runAction(this._currentItem)}},{kind:"method",key:"willUpdate",value:function(e){if((0,s.A)(i,"willUpdate",this,3)([e]),this.hasUpdated||(0,w.i)(),e.has("entityId"))this._setError(void 0);else if(!e.has("navigateIds"))return;this._setError(void 0);const t=e.get("navigateIds"),a=this.navigateIds;this._content?.scrollTo(0,0),this.scrolled=!1;const o=this._currentItem,n=this._parentItem;this._currentItem=void 0,this._parentItem=void 0;const r=a[a.length-1],d=a.length>1?a[a.length-2]:void 0;let l,c;e.has("entityId")||(t&&a.length===t.length+1&&t.every(((e,t)=>{const i=a[t];return i.media_content_id===e.media_content_id&&i.media_content_type===e.media_content_type}))?c=Promise.resolve(o):t&&a.length===t.length-1&&a.every(((e,i)=>{const a=t[i];return e.media_content_id===a.media_content_id&&e.media_content_type===a.media_content_type}))&&(l=Promise.resolve(n))),l||(l=this._fetchData(this.entityId,r.media_content_id,r.media_content_type)),l.then((e=>{this._currentItem=e,(0,h.r)(this,"media-browsed",{ids:a,current:e})}),(i=>{t&&e.has("entityId")&&a.length===t.length&&t.every(((e,t)=>a[t].media_content_id===e.media_content_id&&a[t].media_content_type===e.media_content_type))?(0,h.r)(this,"media-browsed",{ids:[{media_content_id:void 0,media_content_type:void 0}],replace:!0}):"entity_not_found"===i.code&&(0,m.g0)(this.hass.states[this.entityId]?.state)?this._setError({message:this.hass.localize("ui.components.media-browser.media_player_unavailable"),code:"entity_not_found"}):this._setError(i)})),c||void 0===d||(c=this._fetchData(this.entityId,d.media_content_id,d.media_content_type)),c&&c.then((e=>{this._parentItem=e}))}},{kind:"method",key:"shouldUpdate",value:function(e){if(e.size>1||!e.has("hass"))return!0;const t=e.get("hass");return void 0===t||t.localize!==this.hass.localize}},{kind:"method",key:"firstUpdated",value:function(){this._measureCard(),this._attachResizeObserver()}},{kind:"method",key:"updated",value:function(e){if((0,s.A)(i,"updated",this,3)([e]),e.has("_scrolled"))this._animateHeaderHeight();else if(e.has("_currentItem")){if(this._setHeaderHeight(),this._observed)return;const e=this._virtualizer?._virtualizer;e&&(this._observed=!0,setTimeout((()=>e._observeMutations()),0))}}},{kind:"method",key:"render",value:function(){if(this._error)return n.qy`
        <div class="container">
          <ha-alert alert-type="error">
            ${this._renderError(this._error)}
          </ha-alert>
        </div>
      `;if(!this._currentItem)return n.qy`<ha-circular-progress indeterminate></ha-circular-progress>`;const e=this._currentItem,t=this.hass.localize(`ui.components.media-browser.class.${e.media_class}`),i=e.children||[],a=p.EC[e.media_class],s=e.children_media_class?p.EC[e.children_media_class]:p.EC.directory,r=e.thumbnail?this._getThumbnailURLorBase64(e.thumbnail).then((e=>`url(${e})`)):"none";return n.qy`
              ${e.can_play?n.qy`
                      <div
                        class="header ${(0,d.H)({"no-img":!e.thumbnail,"no-dialog":!this.dialog})}"
                        @transitionend=${this._setHeaderHeight}
                      >
                        <div class="header-content">
                          ${e.thumbnail?n.qy`
                                <div
                                  class="img"
                                  style="background-image: ${(0,c.T)(r,"")}"
                                >
                                  ${this.narrow&&e?.can_play?n.qy`
                                        <ha-fab
                                          mini
                                          .item=${e}
                                          @click=${this._actionClicked}
                                        >
                                          <ha-svg-icon
                                            slot="icon"
                                            .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                                            .path=${"play"===this.action?x:$}
                                          ></ha-svg-icon>
                                          ${this.hass.localize(`ui.components.media-browser.${this.action}`)}
                                        </ha-fab>
                                      `:""}
                                </div>
                              `:n.s6}
                          <div class="header-info">
                            <div class="breadcrumb">
                              <h1 class="title">${e.title}</h1>
                              ${t?n.qy` <h2 class="subtitle">${t}</h2> `:""}
                            </div>
                            ${!e.can_play||e.thumbnail&&this.narrow?"":n.qy`
                                  <mwc-button
                                    raised
                                    .item=${e}
                                    @click=${this._actionClicked}
                                  >
                                    <ha-svg-icon
                                      .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                                      .path=${"play"===this.action?x:$}
                                    ></ha-svg-icon>
                                    ${this.hass.localize(`ui.components.media-browser.${this.action}`)}
                                  </mwc-button>
                                `}
                          </div>
                        </div>
                      </div>
                    `:""}
          <div
            class="content"
            @scroll=${this._scroll}
            @touchmove=${this._scroll}
          >
            ${this._error?n.qy`
                    <div class="container">
                      <ha-alert alert-type="error">
                        ${this._renderError(this._error)}
                      </ha-alert>
                    </div>
                  `:(0,v.ni)(e.media_content_id)?n.qy`
                      <ha-browse-media-tts
                        .item=${e}
                        .hass=${this.hass}
                        .action=${this.action}
                        @tts-picked=${this._ttsPicked}
                      ></ha-browse-media-tts>
                    `:i.length||e.not_shown?"grid"===this.preferredLayout||"auto"===this.preferredLayout&&"grid"===s.layout?n.qy`
                          <lit-virtualizer
                            scroller
                            .layout=${(0,o.V)({itemSize:{width:"175px",height:"portrait"===s.thumbnail_ratio?"312px":"225px"},gap:"16px",flex:{preserve:"aspect-ratio"},justify:"space-evenly",direction:"vertical"})}
                            .items=${i}
                            .renderItem=${this._renderGridItem}
                            class="children ${(0,d.H)({portrait:"portrait"===s.thumbnail_ratio,not_shown:!!e.not_shown})}"
                          ></lit-virtualizer>
                          ${e.not_shown?n.qy`
                                <div class="grid not-shown">
                                  <div class="title">
                                    ${this.hass.localize("ui.components.media-browser.not_shown",{count:e.not_shown})}
                                  </div>
                                </div>
                              `:""}
                        `:n.qy`
                          <mwc-list>
                            <lit-virtualizer
                              scroller
                              .items=${i}
                              style=${(0,l.W)({height:72*i.length+26+"px"})}
                              .renderItem=${this._renderListItem}
                            ></lit-virtualizer>
                            ${e.not_shown?n.qy`
                                  <mwc-list-item
                                    noninteractive
                                    class="not-shown"
                                    .graphic=${a.show_list_images?"medium":"avatar"}
                                  >
                                    <span class="title">
                                      ${this.hass.localize("ui.components.media-browser.not_shown",{count:e.not_shown})}
                                    </span>
                                  </mwc-list-item>
                                `:""}
                          </mwc-list>
                        `:n.qy`
                        <div class="container no-items">
                          ${"media-source://media_source/local/."===e.media_content_id?n.qy`
                                <div class="highlight-add-button">
                                  <span>
                                    <ha-svg-icon
                                      .path=${"M21.5 9.5L20.09 10.92L17 7.83V13.5C17 17.09 14.09 20 10.5 20H4V18H10.5C13 18 15 16 15 13.5V7.83L11.91 10.91L10.5 9.5L16 4L21.5 9.5Z"}
                                    ></ha-svg-icon>
                                  </span>
                                  <span>
                                    ${this.hass.localize("ui.components.media-browser.file_management.highlight_button")}
                                  </span>
                                </div>
                              `:this.hass.localize("ui.components.media-browser.no_items")}
                        </div>
                      `}
          </div>
        </div>
      </div>
    `}},{kind:"field",key:"_renderGridItem",value(){return e=>{const t=e.thumbnail?this._getThumbnailURLorBase64(e.thumbnail).then((e=>`url(${e})`)):"none";return n.qy`
      <div class="child" .item=${e} @click=${this._childClicked}>
        <ha-card outlined>
          <div class="thumbnail">
            ${e.thumbnail?n.qy`
                  <div
                    class="${(0,d.H)({"centered-image":["app","directory"].includes(e.media_class),"brand-image":(0,f.bg)(e.thumbnail)})} image"
                    style="background-image: ${(0,c.T)(t,"")}"
                  ></div>
                `:n.qy`
                  <div class="icon-holder image">
                    <ha-svg-icon
                      class="folder"
                      .path=${p.EC["directory"===e.media_class&&e.children_media_class||e.media_class].icon}
                    ></ha-svg-icon>
                  </div>
                `}
            ${e.can_play?n.qy`
                  <ha-icon-button
                    class="play ${(0,d.H)({can_expand:e.can_expand})}"
                    .item=${e}
                    .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                    .path=${"play"===this.action?x:$}
                    @click=${this._actionClicked}
                  ></ha-icon-button>
                `:""}
          </div>
          <div class="title">
            ${e.title}
            <simple-tooltip fitToVisibleBounds position="top" offset="4"
              >${e.title}</simple-tooltip
            >
          </div>
        </ha-card>
      </div>
    `}}},{kind:"field",key:"_renderListItem",value(){return e=>{const t=this._currentItem,i=p.EC[t.media_class],a=i.show_list_images&&e.thumbnail?this._getThumbnailURLorBase64(e.thumbnail).then((e=>`url(${e})`)):"none";return n.qy`
      <mwc-list-item
        @click=${this._childClicked}
        .item=${e}
        .graphic=${i.show_list_images?"medium":"avatar"}
      >
        ${"none"!==a||e.can_play?n.qy`<div
              class=${(0,d.H)({graphic:!0,thumbnail:!0===i.show_list_images})}
              style="background-image: ${(0,c.T)(a,"")}"
              slot="graphic"
            >
              ${e.can_play?n.qy`<ha-icon-button
                    class="play ${(0,d.H)({show:!i.show_list_images||!e.thumbnail})}"
                    .item=${e}
                    .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                    .path=${"play"===this.action?x:$}
                    @click=${this._actionClicked}
                  ></ha-icon-button>`:n.s6}
            </div>`:n.qy`<ha-svg-icon
              .path=${p.EC["directory"===e.media_class&&e.children_media_class||e.media_class].icon}
              slot="graphic"
            ></ha-svg-icon>`}
        <span class="title">${e.title}</span>
      </mwc-list-item>
    `}}},{kind:"method",key:"_getThumbnailURLorBase64",value:async function(e){return e?e.startsWith("/")?new Promise(((t,i)=>{this.hass.fetchWithAuth(e).then((e=>e.blob())).then((e=>{const a=new FileReader;a.onload=()=>{const e=a.result;t("string"==typeof e?e:"")},a.onerror=e=>i(e),a.readAsDataURL(e)}))})):((0,f.bg)(e)&&(e=(0,f.MR)({domain:(0,f.a_)(e),type:"icon",useFallback:!0,darkOptimized:this.hass.themes?.darkMode})),e):""}},{kind:"field",key:"_actionClicked",value(){return e=>{e.stopPropagation();const t=e.currentTarget.item;this._runAction(t)}}},{kind:"method",key:"_runAction",value:function(e){(0,h.r)(this,"media-picked",{item:e,navigateIds:this.navigateIds})}},{kind:"method",key:"_ttsPicked",value:function(e){e.stopPropagation();const t=this.navigateIds.slice(0,-1);t.push(e.detail.item),(0,h.r)(this,"media-picked",{...e.detail,navigateIds:t})}},{kind:"field",key:"_childClicked",value(){return async e=>{const t=e.currentTarget.item;t&&(t.can_expand?(0,h.r)(this,"media-browsed",{ids:[...this.navigateIds,t]}):this._runAction(t))}}},{kind:"method",key:"_fetchData",value:async function(e,t,i){return e!==p.H1?(0,p.ET)(this.hass,e,t,i):(0,g.Fn)(this.hass,t)}},{kind:"method",key:"_measureCard",value:function(){this.narrow=(this.dialog?window.innerWidth:this.offsetWidth)<450}},{kind:"method",key:"_attachResizeObserver",value:async function(){this._resizeObserver||(this._resizeObserver=new ResizeObserver((0,u.s)((()=>this._measureCard()),250,!1))),this._resizeObserver.observe(this)}},{kind:"method",key:"_closeDialogAction",value:function(){(0,h.r)(this,"close-dialog")}},{kind:"method",key:"_setError",value:function(e){this.dialog?e&&(this._closeDialogAction(),(0,_.K$)(this,{title:this.hass.localize("ui.components.media-browser.media_browsing_error"),text:this._renderError(e)})):this._error=e}},{kind:"method",key:"_renderError",value:function(e){return"Media directory does not exist."===e.message?n.qy`
        <h2>
          ${this.hass.localize("ui.components.media-browser.no_local_media_found")}
        </h2>
        <p>
          ${this.hass.localize("ui.components.media-browser.no_media_folder")}
          <br />
          ${this.hass.localize("ui.components.media-browser.setup_local_help",{documentation:n.qy`<a
              href=${(0,k.o)(this.hass,"/more-info/local-media/setup-media")}
              target="_blank"
              rel="noreferrer"
              >${this.hass.localize("ui.components.media-browser.documentation")}</a
            >`})}
          <br />
          ${this.hass.localize("ui.components.media-browser.local_media_files")}
        </p>
      `:n.qy`<span class="error">${e.message}</span>`}},{kind:"method",key:"_setHeaderHeight",value:async function(){await this.updateComplete;const e=this._header,t=this._content;e&&t&&(this._headerOffsetHeight=e.offsetHeight,t.style.marginTop=`${this._headerOffsetHeight}px`,t.style.maxHeight=`calc(var(--media-browser-max-height, 100%) - ${this._headerOffsetHeight}px)`)}},{kind:"method",key:"_animateHeaderHeight",value:function(){let e;const t=i=>{void 0===e&&(e=i);const a=i-e;this._setHeaderHeight(),a<400&&requestAnimationFrame(t)};requestAnimationFrame(t)}},{kind:"method",decorators:[(0,r.Ls)({passive:!0})],key:"_scroll",value:function(e){const t=e.currentTarget;!this.scrolled&&t.scrollTop>this._headerOffsetHeight?this.scrolled=!0:this.scrolled&&t.scrollTop<this._headerOffsetHeight&&(this.scrolled=!1)}},{kind:"get",static:!0,key:"styles",value:function(){return[y.RF,n.AH`
        :host {
          display: flex;
          flex-direction: column;
          position: relative;
          direction: ltr;
        }

        ha-circular-progress {
          --mdc-theme-primary: var(--primary-color);
          display: flex;
          justify-content: center;
          margin: 40px;
        }

        .container {
          padding: 16px;
        }

        .no-items {
          padding-left: 32px;
        }

        .highlight-add-button {
          display: flex;
          flex-direction: row-reverse;
          margin-right: 48px;
        }

        .highlight-add-button ha-svg-icon {
          position: relative;
          top: -0.5em;
          margin-left: 8px;
        }

        .content {
          overflow-y: auto;
          box-sizing: border-box;
          height: 100%;
        }

        /* HEADER */

        .header {
          display: flex;
          justify-content: space-between;
          border-bottom: 1px solid var(--divider-color);
          background-color: var(--card-background-color);
          position: absolute;
          top: 0;
          right: 0;
          left: 0;
          z-index: 3;
          padding: 16px;
        }
        .header_button {
          position: relative;
          right: -8px;
        }
        .header-content {
          display: flex;
          flex-wrap: wrap;
          flex-grow: 1;
          align-items: flex-start;
        }
        .header-content .img {
          height: 175px;
          width: 175px;
          margin-right: 16px;
          background-size: cover;
          border-radius: 2px;
          transition:
            width 0.4s,
            height 0.4s;
        }
        .header-info {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          align-self: stretch;
          min-width: 0;
          flex: 1;
        }
        .header-info mwc-button {
          display: block;
          --mdc-theme-primary: var(--primary-color);
          padding-bottom: 16px;
        }
        .breadcrumb {
          display: flex;
          flex-direction: column;
          overflow: hidden;
          flex-grow: 1;
          padding-top: 16px;
        }
        .breadcrumb .title {
          font-size: 32px;
          line-height: 1.2;
          font-weight: bold;
          margin: 0;
          overflow: hidden;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          padding-right: 8px;
        }
        .breadcrumb .previous-title {
          font-size: 14px;
          padding-bottom: 8px;
          color: var(--secondary-text-color);
          overflow: hidden;
          text-overflow: ellipsis;
          cursor: pointer;
          --mdc-icon-size: 14px;
        }
        .breadcrumb .subtitle {
          font-size: 16px;
          overflow: hidden;
          text-overflow: ellipsis;
          margin-bottom: 0;
          transition:
            height 0.5s,
            margin 0.5s;
        }

        .not-shown {
          font-style: italic;
          color: var(--secondary-text-color);
          padding: 8px 16px 8px;
        }

        .grid.not-shown {
          display: flex;
          align-items: center;
          text-align: center;
        }

        /* ============= CHILDREN ============= */

        mwc-list {
          --mdc-list-vertical-padding: 0;
          --mdc-list-item-graphic-margin: 0;
          --mdc-theme-text-icon-on-background: var(--secondary-text-color);
          margin-top: 10px;
        }

        mwc-list li:last-child {
          display: none;
        }

        mwc-list li[divider] {
          border-bottom-color: var(--divider-color);
        }

        mwc-list-item {
          width: 100%;
        }

        div.children {
          display: grid;
          grid-template-columns: repeat(
            auto-fit,
            minmax(var(--media-browse-item-size, 175px), 0.1fr)
          );
          grid-gap: 16px;
          padding: 16px;
        }

        :host([dialog]) .children {
          grid-template-columns: repeat(
            auto-fit,
            minmax(var(--media-browse-item-size, 175px), 0.33fr)
          );
        }

        .child {
          display: flex;
          flex-direction: column;
          cursor: pointer;
        }

        ha-card {
          position: relative;
          width: 100%;
          box-sizing: border-box;
        }

        .children ha-card .thumbnail {
          width: 100%;
          position: relative;
          box-sizing: border-box;
          transition: padding-bottom 0.1s ease-out;
          padding-bottom: 100%;
        }

        .portrait ha-card .thumbnail {
          padding-bottom: 150%;
        }

        ha-card .image {
          border-radius: 3px 3px 0 0;
        }

        .image {
          position: absolute;
          top: 0;
          right: 0;
          left: 0;
          bottom: 0;
          background-size: cover;
          background-repeat: no-repeat;
          background-position: center;
        }

        .centered-image {
          margin: 0 8px;
          background-size: contain;
        }

        .brand-image {
          background-size: 40%;
        }

        .children ha-card .icon-holder {
          display: flex;
          justify-content: center;
          align-items: center;
        }

        .child .folder {
          color: var(--secondary-text-color);
          --mdc-icon-size: calc(var(--media-browse-item-size, 175px) * 0.4);
        }

        .child .play {
          position: absolute;
          transition: color 0.5s;
          border-radius: 50%;
          top: calc(50% - 50px);
          right: calc(50% - 35px);
          opacity: 0;
          transition: opacity 0.1s ease-out;
        }

        .child .play:not(.can_expand) {
          --mdc-icon-button-size: 70px;
          --mdc-icon-size: 48px;
        }

        ha-card:hover .play {
          opacity: 1;
        }

        ha-card:hover .play:not(.can_expand) {
          color: var(--primary-color);
        }

        ha-card:hover .play.can_expand {
          bottom: 8px;
        }

        .child .play.can_expand {
          background-color: rgba(var(--rgb-card-background-color), 0.5);
          top: auto;
          bottom: 0px;
          right: 8px;
          transition:
            bottom 0.1s ease-out,
            opacity 0.1s ease-out;
        }

        .child .play:hover {
          color: var(--primary-color);
        }

        .child .title {
          font-size: 16px;
          padding-top: 16px;
          padding-left: 2px;
          overflow: hidden;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 1;
          text-overflow: ellipsis;
        }

        .child ha-card .title {
          margin-bottom: 16px;
          padding-left: 16px;
        }

        mwc-list-item .graphic {
          background-size: contain;
          background-repeat: no-repeat;
          background-position: center;
          border-radius: 2px;
          display: flex;
          align-content: center;
          align-items: center;
          line-height: initial;
        }

        mwc-list-item .graphic .play {
          opacity: 0;
          transition: all 0.5s;
          background-color: rgba(var(--rgb-card-background-color), 0.5);
          border-radius: 50%;
          --mdc-icon-button-size: 40px;
        }

        mwc-list-item:hover .graphic .play {
          opacity: 1;
          color: var(--primary-text-color);
        }

        mwc-list-item .graphic .play.show {
          opacity: 1;
          background-color: transparent;
        }

        mwc-list-item .title {
          margin-left: 16px;
          margin-inline-start: 16px;
          margin-inline-end: initial;
        }

        /* ============= Narrow ============= */

        :host([narrow]) {
          padding: 0;
        }

        :host([narrow]) .media-source {
          padding: 0 24px;
        }

        :host([narrow]) div.children {
          grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
        }

        :host([narrow]) .breadcrumb .title {
          font-size: 24px;
        }
        :host([narrow]) .header {
          padding: 0;
        }
        :host([narrow]) .header.no-dialog {
          display: block;
        }
        :host([narrow]) .header_button {
          position: absolute;
          top: 14px;
          right: 8px;
        }
        :host([narrow]) .header-content {
          flex-direction: column;
          flex-wrap: nowrap;
        }
        :host([narrow]) .header-content .img {
          height: auto;
          width: 100%;
          margin-right: 0;
          padding-bottom: 50%;
          margin-bottom: 8px;
          position: relative;
          background-position: center;
          border-radius: 0;
          transition:
            width 0.4s,
            height 0.4s,
            padding-bottom 0.4s;
        }
        ha-fab {
          position: absolute;
          --mdc-theme-secondary: var(--primary-color);
          bottom: -20px;
          right: 20px;
        }
        :host([narrow]) .header-info mwc-button {
          margin-top: 16px;
          margin-bottom: 8px;
        }
        :host([narrow]) .header-info {
          padding: 0 16px 8px;
        }

        /* ============= Scroll ============= */
        :host([scrolled]) .breadcrumb .subtitle {
          height: 0;
          margin: 0;
        }
        :host([scrolled]) .breadcrumb .title {
          -webkit-line-clamp: 1;
        }
        :host(:not([narrow])[scrolled]) .header:not(.no-img) ha-icon-button {
          align-self: center;
        }
        :host([scrolled]) .header-info mwc-button,
        .no-img .header-info mwc-button {
          padding-right: 4px;
        }
        :host([scrolled][narrow]) .no-img .header-info mwc-button {
          padding-right: 16px;
        }
        :host([scrolled]) .header-info {
          flex-direction: row;
        }
        :host([scrolled]) .header-info mwc-button {
          align-self: center;
          margin-top: 0;
          margin-bottom: 0;
          padding-bottom: 0;
        }
        :host([scrolled][narrow]) .no-img .header-info {
          flex-direction: row-reverse;
        }
        :host([scrolled][narrow]) .header-info {
          padding: 20px 24px 10px 24px;
          align-items: center;
        }
        :host([scrolled]) .header-content {
          align-items: flex-end;
          flex-direction: row;
        }
        :host([scrolled]) .header-content .img {
          height: 75px;
          width: 75px;
        }
        :host([scrolled]) .breadcrumb {
          padding-top: 0;
          align-self: center;
        }
        :host([scrolled][narrow]) .header-content .img {
          height: 100px;
          width: 100px;
          padding-bottom: initial;
          margin-bottom: 0;
        }
        :host([scrolled]) ha-fab {
          bottom: 0px;
          right: -24px;
          --mdc-fab-box-shadow: none;
          --mdc-theme-secondary: rgba(var(--rgb-primary-color), 0.5);
        }

        lit-virtualizer {
          height: 100%;
          overflow: overlay !important;
          contain: size layout !important;
        }

        lit-virtualizer.not_shown {
          height: calc(100% - 36px);
        }

        ha-browse-media-tts {
          direction: var(--direction);
        }
      `]}}]}}),n.WF)},2462:(e,t,i)=>{i.d(t,{Fn:()=>a,Jz:()=>s,VA:()=>o,WI:()=>n});const a=(e,t)=>e.callWS({type:"media_source/browse_media",media_content_id:t}),s=e=>e.startsWith("media-source://media_source"),o=async(e,t,i)=>{const a=new FormData;a.append("media_content_id",t),a.append("file",i);const s=await e.fetchWithAuth("/api/media_source/local_source/upload",{method:"POST",body:a});if(413===s.status)throw new Error(`Uploaded file is too large (${i.name})`);if(200!==s.status)throw new Error("Unknown error");return s.json()},n=async(e,t)=>e.callWS({type:"media_source/local_source/remove",media_content_id:t})},6933:(e,t,i)=>{i.d(t,{EF:()=>o,Xv:()=>n,ni:()=>s,u1:()=>r,z3:()=>d});const a="media-source://tts/",s=e=>e.startsWith(a),o=e=>e.substring(19),n=(e,t,i)=>e.callWS({type:"tts/engine/list",language:t,country:i}),r=(e,t)=>e.callWS({type:"tts/engine/get",engine_id:t}),d=(e,t,i)=>e.callWS({type:"tts/engine/voices",engine_id:t,language:i})},1646:(e,t,i)=>{i.d(t,{i:()=>a});const a=async()=>{await i.e(3331).then(i.bind(i,3331))}},1750:(e,t,i)=>{i.d(t,{o:()=>a});const a=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}};
//# sourceMappingURL=VIqZHnq4.js.map