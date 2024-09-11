/*! For license information please see UN0mk8zv.js.LICENSE.txt */
export const id=6052;export const ids=[6052];export const modules={6678:(e,t,i)=>{i.d(t,{F:()=>r,r:()=>s});const a=/{%|{{/,r=e=>a.test(e),s=e=>{if(!e)return!1;if("string"==typeof e)return r(e);if("object"==typeof e){return(Array.isArray(e)?e:Object.values(e)).some((e=>e&&s(e)))}return!1}},9411:(e,t,i)=>{i.d(t,{b:()=>a});const a=(e,t)=>{if(e===t)return!0;if(e&&t&&"object"==typeof e&&"object"==typeof t){if(e.constructor!==t.constructor)return!1;let i,r;if(Array.isArray(e)){if(r=e.length,r!==t.length)return!1;for(i=r;0!=i--;)if(!a(e[i],t[i]))return!1;return!0}if(e instanceof Map&&t instanceof Map){if(e.size!==t.size)return!1;for(i of e.entries())if(!t.has(i[0]))return!1;for(i of e.entries())if(!a(i[1],t.get(i[0])))return!1;return!0}if(e instanceof Set&&t instanceof Set){if(e.size!==t.size)return!1;for(i of e.entries())if(!t.has(i[0]))return!1;return!0}if(ArrayBuffer.isView(e)&&ArrayBuffer.isView(t)){if(r=e.length,r!==t.length)return!1;for(i=r;0!=i--;)if(e[i]!==t[i])return!1;return!0}if(e.constructor===RegExp)return e.source===t.source&&e.flags===t.flags;if(e.valueOf!==Object.prototype.valueOf)return e.valueOf()===t.valueOf();if(e.toString!==Object.prototype.toString)return e.toString()===t.toString();const s=Object.keys(e);if(r=s.length,r!==Object.keys(t).length)return!1;for(i=r;0!=i--;)if(!Object.prototype.hasOwnProperty.call(t,s[i]))return!1;for(i=r;0!=i--;){const r=s[i];if(!a(e[r],t[r]))return!1}return!0}return e!=e&&t!=t}},3604:(e,t,i)=>{var a=i(5461),r=i(9534),s=i(8597),n=i(6513),o=i(196),l=i(1497),d=i(8678);let u=class extends l.L{};u.styles=[d.R],u=(0,n.Cg)([(0,o.EM)("mwc-checkbox")],u);var c=i(9760),h=i(6175);class g extends h.J{constructor(){super(...arguments),this.left=!1,this.graphic="control"}render(){const e={"mdc-deprecated-list-item__graphic":this.left,"mdc-deprecated-list-item__meta":!this.left},t=this.renderText(),i=this.graphic&&"control"!==this.graphic&&!this.left?this.renderGraphic():s.qy``,a=this.hasMeta&&this.left?this.renderMeta():s.qy``,r=this.renderRipple();return s.qy`
      ${r}
      ${i}
      ${this.left?"":t}
      <span class=${(0,c.H)(e)}>
        <mwc-checkbox
            reducedTouchTarget
            tabindex=${this.tabindex}
            .checked=${this.selected}
            ?disabled=${this.disabled}
            @change=${this.onChange}>
        </mwc-checkbox>
      </span>
      ${this.left?t:""}
      ${a}`}async onChange(e){const t=e.target;this.selected===t.checked||(this._skipPropRequest=!0,this.selected=t.checked,await this.updateComplete,this._skipPropRequest=!1)}}(0,n.Cg)([(0,o.P)("slot")],g.prototype,"slotElement",void 0),(0,n.Cg)([(0,o.P)("mwc-checkbox")],g.prototype,"checkboxElement",void 0),(0,n.Cg)([(0,o.MZ)({type:Boolean})],g.prototype,"left",void 0),(0,n.Cg)([(0,o.MZ)({type:String,reflect:!0})],g.prototype,"graphic",void 0);const p=s.AH`:host(:not([twoline])){height:56px}:host(:not([left])) .mdc-deprecated-list-item__meta{height:40px;width:40px}`;var m=i(5592),v=i(3167);(0,a.A)([(0,o.EM)("ha-check-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"onChange",value:async function(e){(0,r.A)(i,"onChange",this,3)([e]),(0,v.r)(this,e.type)}},{kind:"field",static:!0,key:"styles",value(){return[m.R,p,s.AH`
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
    `]}}]}}),g)},9451:(e,t,i)=>{i.d(t,{$:()=>a});const a=e=>{const t={};return e.forEach((e=>{if(void 0!==e.description?.suggested_value&&null!==e.description?.suggested_value)t[e.name]=e.description.suggested_value;else if("default"in e)t[e.name]=e.default;else if(e.required){if("boolean"===e.type)t[e.name]=!1;else if("string"===e.type)t[e.name]="";else if("integer"===e.type)t[e.name]="valueMin"in e?e.valueMin:0;else if("constant"===e.type)t[e.name]=e.value;else if("float"===e.type)t[e.name]=0;else if("select"===e.type){if(e.options.length){const i=e.options[0];t[e.name]=Array.isArray(i)?i[0]:i}}else if("positive_time_period_dict"===e.type)t[e.name]={hours:0,minutes:0,seconds:0};else if("expandable"===e.type)t[e.name]=a(e.schema);else if("selector"in e){const i=e.selector;if("device"in i)t[e.name]=i.device?.multiple?[]:"";else if("entity"in i)t[e.name]=i.entity?.multiple?[]:"";else if("area"in i)t[e.name]=i.area?.multiple?[]:"";else if("boolean"in i)t[e.name]=!1;else if("addon"in i||"attribute"in i||"file"in i||"icon"in i||"template"in i||"text"in i||"theme"in i||"object"in i)t[e.name]="";else if("number"in i)t[e.name]=i.number?.min??0;else if("select"in i){if(i.select?.options.length){const a=i.select.options[0],r="string"==typeof a?a:a.value;t[e.name]=i.select.multiple?[r]:r}}else if("country"in i)i.country?.countries?.length&&(t[e.name]=i.country.countries[0]);else if("language"in i)i.language?.languages?.length&&(t[e.name]=i.language.languages[0]);else if("duration"in i)t[e.name]={hours:0,minutes:0,seconds:0};else if("time"in i)t[e.name]="00:00:00";else if("date"in i||"datetime"in i){const i=(new Date).toISOString().slice(0,10);t[e.name]=`${i}T00:00:00`}else if("color_rgb"in i)t[e.name]=[0,0,0];else if("color_temp"in i)t[e.name]=i.color_temp?.min_mireds??153;else if("action"in i||"trigger"in i||"condition"in i)t[e.name]=[];else{if(!("media"in i)&&!("target"in i))throw new Error(`Selector ${Object.keys(i)[0]} not supported in initial form data`);t[e.name]={}}}}else;})),t}},9032:(e,t,i)=>{i.d(t,{S:()=>a,_:()=>r});const a={calendar:"M19,19H5V8H19M16,1V3H8V1H6V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3H18V1M17,12H12V17H17V12Z",device:"M3 6H21V4H3C1.9 4 1 4.9 1 6V18C1 19.1 1.9 20 3 20H7V18H3V6M13 12H9V13.78C8.39 14.33 8 15.11 8 16C8 16.89 8.39 17.67 9 18.22V20H13V18.22C13.61 17.67 14 16.88 14 16S13.61 14.33 13 13.78V12M11 17.5C10.17 17.5 9.5 16.83 9.5 16S10.17 14.5 11 14.5 12.5 15.17 12.5 16 11.83 17.5 11 17.5M22 8H16C15.5 8 15 8.5 15 9V19C15 19.5 15.5 20 16 20H22C22.5 20 23 19.5 23 19V9C23 8.5 22.5 8 22 8M21 18H17V10H21V18Z",event:"M10,9A1,1 0 0,1 11,8A1,1 0 0,1 12,9V13.47L13.21,13.6L18.15,15.79C18.68,16.03 19,16.56 19,17.14V21.5C18.97,22.32 18.32,22.97 17.5,23H11C10.62,23 10.26,22.85 10,22.57L5.1,18.37L5.84,17.6C6.03,17.39 6.3,17.28 6.58,17.28H6.8L10,19V9M11,5A4,4 0 0,1 15,9C15,10.5 14.2,11.77 13,12.46V11.24C13.61,10.69 14,9.89 14,9A3,3 0 0,0 11,6A3,3 0 0,0 8,9C8,9.89 8.39,10.69 9,11.24V12.46C7.8,11.77 7,10.5 7,9A4,4 0 0,1 11,5M11,3A6,6 0 0,1 17,9C17,10.7 16.29,12.23 15.16,13.33L14.16,12.88C15.28,11.96 16,10.56 16,9A5,5 0 0,0 11,4A5,5 0 0,0 6,9C6,11.05 7.23,12.81 9,13.58V14.66C6.67,13.83 5,11.61 5,9A6,6 0 0,1 11,3Z",state:"M6.27 17.05C6.72 17.58 7 18.25 7 19C7 20.66 5.66 22 4 22S1 20.66 1 19 2.34 16 4 16C4.18 16 4.36 16 4.53 16.05L7.6 10.69L5.86 9.7L9.95 8.58L11.07 12.67L9.33 11.68L6.27 17.05M20 16C18.7 16 17.6 16.84 17.18 18H11V16L8 19L11 22V20H17.18C17.6 21.16 18.7 22 20 22C21.66 22 23 20.66 23 19S21.66 16 20 16M12 8C12.18 8 12.36 8 12.53 7.95L15.6 13.31L13.86 14.3L17.95 15.42L19.07 11.33L17.33 12.32L14.27 6.95C14.72 6.42 15 5.75 15 5C15 3.34 13.66 2 12 2S9 3.34 9 5 10.34 8 12 8Z",geo_location:"M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z",homeassistant:i(8076)._,mqtt:"M21,9L17,5V8H10V10H17V13M7,11L3,15L7,19V16H14V14H7V11Z",numeric_state:"M4,17V9H2V7H6V17H4M22,15C22,16.11 21.1,17 20,17H16V15H20V13H18V11H20V9H16V7H20A2,2 0 0,1 22,9V10.5A1.5,1.5 0 0,1 20.5,12A1.5,1.5 0 0,1 22,13.5V15M14,15V17H8V13C8,11.89 8.9,11 10,11H12V9H8V7H12A2,2 0 0,1 14,9V11C14,12.11 13.1,13 12,13H10V15H14Z",sun:"M12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,2L14.39,5.42C13.65,5.15 12.84,5 12,5C11.16,5 10.35,5.15 9.61,5.42L12,2M3.34,7L7.5,6.65C6.9,7.16 6.36,7.78 5.94,8.5C5.5,9.24 5.25,10 5.11,10.79L3.34,7M3.36,17L5.12,13.23C5.26,14 5.53,14.78 5.95,15.5C6.37,16.24 6.91,16.86 7.5,17.37L3.36,17M20.65,7L18.88,10.79C18.74,10 18.47,9.23 18.05,8.5C17.63,7.78 17.1,7.15 16.5,6.64L20.65,7M20.64,17L16.5,17.36C17.09,16.85 17.62,16.22 18.04,15.5C18.46,14.77 18.73,14 18.87,13.21L20.64,17M12,22L9.59,18.56C10.33,18.83 11.14,19 12,19C12.82,19 13.63,18.83 14.37,18.56L12,22Z",conversation:"M8,7A2,2 0 0,1 10,9V14A2,2 0 0,1 8,16A2,2 0 0,1 6,14V9A2,2 0 0,1 8,7M14,14C14,16.97 11.84,19.44 9,19.92V22H7V19.92C4.16,19.44 2,16.97 2,14H4A4,4 0 0,0 8,18A4,4 0 0,0 12,14H14M21.41,9.41L17.17,13.66L18.18,10H14A2,2 0 0,1 12,8V4A2,2 0 0,1 14,2H20A2,2 0 0,1 22,4V8C22,8.55 21.78,9.05 21.41,9.41Z",tag:"M18,6H13A2,2 0 0,0 11,8V10.28C10.41,10.62 10,11.26 10,12A2,2 0 0,0 12,14C13.11,14 14,13.1 14,12C14,11.26 13.6,10.62 13,10.28V8H16V16H8V8H10V6H8L6,6V18H18M20,20H4V4H20M20,2H4A2,2 0 0,0 2,4V20A2,2 0 0,0 4,22H20C21.11,22 22,21.1 22,20V4C22,2.89 21.11,2 20,2Z",template:"M8,3A2,2 0 0,0 6,5V9A2,2 0 0,1 4,11H3V13H4A2,2 0 0,1 6,15V19A2,2 0 0,0 8,21H10V19H8V14A2,2 0 0,0 6,12A2,2 0 0,0 8,10V5H10V3M16,3A2,2 0 0,1 18,5V9A2,2 0 0,0 20,11H21V13H20A2,2 0 0,0 18,15V19A2,2 0 0,1 16,21H14V19H16V14A2,2 0 0,1 18,12A2,2 0 0,1 16,10V5H14V3H16Z",time:"M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z",time_pattern:"M11,17A1,1 0 0,0 12,18A1,1 0 0,0 13,17A1,1 0 0,0 12,16A1,1 0 0,0 11,17M11,3V7H13V5.08C16.39,5.57 19,8.47 19,12A7,7 0 0,1 12,19A7,7 0 0,1 5,12C5,10.32 5.59,8.78 6.58,7.58L12,13L13.41,11.59L6.61,4.79V4.81C4.42,6.45 3,9.05 3,12A9,9 0 0,0 12,21A9,9 0 0,0 21,12A9,9 0 0,0 12,3M18,12A1,1 0 0,0 17,11A1,1 0 0,0 16,12A1,1 0 0,0 17,13A1,1 0 0,0 18,12M6,12A1,1 0 0,0 7,13A1,1 0 0,0 8,12A1,1 0 0,0 7,11A1,1 0 0,0 6,12Z",webhook:"M10.46,19C9,21.07 6.15,21.59 4.09,20.15C2.04,18.71 1.56,15.84 3,13.75C3.87,12.5 5.21,11.83 6.58,11.77L6.63,13.2C5.72,13.27 4.84,13.74 4.27,14.56C3.27,16 3.58,17.94 4.95,18.91C6.33,19.87 8.26,19.5 9.26,18.07C9.57,17.62 9.75,17.13 9.82,16.63V15.62L15.4,15.58L15.47,15.47C16,14.55 17.15,14.23 18.05,14.75C18.95,15.27 19.26,16.43 18.73,17.35C18.2,18.26 17.04,18.58 16.14,18.06C15.73,17.83 15.44,17.46 15.31,17.04L11.24,17.06C11.13,17.73 10.87,18.38 10.46,19M17.74,11.86C20.27,12.17 22.07,14.44 21.76,16.93C21.45,19.43 19.15,21.2 16.62,20.89C15.13,20.71 13.9,19.86 13.19,18.68L14.43,17.96C14.92,18.73 15.75,19.28 16.75,19.41C18.5,19.62 20.05,18.43 20.26,16.76C20.47,15.09 19.23,13.56 17.5,13.35C16.96,13.29 16.44,13.36 15.97,13.53L15.12,13.97L12.54,9.2H12.32C11.26,9.16 10.44,8.29 10.47,7.25C10.5,6.21 11.4,5.4 12.45,5.44C13.5,5.5 14.33,6.35 14.3,7.39C14.28,7.83 14.11,8.23 13.84,8.54L15.74,12.05C16.36,11.85 17.04,11.78 17.74,11.86M8.25,9.14C7.25,6.79 8.31,4.1 10.62,3.12C12.94,2.14 15.62,3.25 16.62,5.6C17.21,6.97 17.09,8.47 16.42,9.67L15.18,8.95C15.6,8.14 15.67,7.15 15.27,6.22C14.59,4.62 12.78,3.85 11.23,4.5C9.67,5.16 8.97,7 9.65,8.6C9.93,9.26 10.4,9.77 10.97,10.11L11.36,10.32L8.29,15.31C8.32,15.36 8.36,15.42 8.39,15.5C8.88,16.41 8.54,17.56 7.62,18.05C6.71,18.54 5.56,18.18 5.06,17.24C4.57,16.31 4.91,15.16 5.83,14.67C6.22,14.46 6.65,14.41 7.06,14.5L9.37,10.73C8.9,10.3 8.5,9.76 8.25,9.14Z",persistent_notification:"M13 11H11V5H13M13 15H11V13H13M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2Z",zone:"M12,2C15.31,2 18,4.66 18,7.95C18,12.41 12,19 12,19C12,19 6,12.41 6,7.95C6,4.66 8.69,2 12,2M12,6A2,2 0 0,0 10,8A2,2 0 0,0 12,10A2,2 0 0,0 14,8A2,2 0 0,0 12,6M20,19C20,21.21 16.42,23 12,23C7.58,23 4,21.21 4,19C4,17.71 5.22,16.56 7.11,15.83L7.75,16.74C6.67,17.19 6,17.81 6,18.5C6,19.88 8.69,21 12,21C15.31,21 18,19.88 18,18.5C18,17.81 17.33,17.19 16.25,16.74L16.89,15.83C18.78,16.56 20,17.71 20,19Z"},r={device:{},entity:{icon:"M11,13.5V21.5H3V13.5H11M12,2L17.5,11H6.5L12,2M17.5,13C20,13 22,15 22,17.5C22,20 20,22 17.5,22C15,22 13,20 13,17.5C13,15 15,13 17.5,13Z",members:{state:{},numeric_state:{}}},time_location:{icon:"M15,12H16.5V16.25L19.36,17.94L18.61,19.16L15,17V12M23,16A7,7 0 0,1 16,23C13,23 10.4,21.08 9.42,18.4L8,17.9L2.66,19.97L2.5,20A0.5,0.5 0 0,1 2,19.5V4.38C2,4.15 2.15,3.97 2.36,3.9L8,2L14,4.1L19.34,2H19.5A0.5,0.5 0 0,1 20,2.5V10.25C21.81,11.5 23,13.62 23,16M9,16C9,12.83 11.11,10.15 14,9.29V6.11L8,4V15.89L9,16.24C9,16.16 9,16.08 9,16M16,11A5,5 0 0,0 11,16A5,5 0 0,0 16,21A5,5 0 0,0 21,16A5,5 0 0,0 16,11Z",members:{calendar:{},sun:{},time:{},time_pattern:{},zone:{}}},other:{icon:"M16,12A2,2 0 0,1 18,10A2,2 0 0,1 20,12A2,2 0 0,1 18,14A2,2 0 0,1 16,12M10,12A2,2 0 0,1 12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12M4,12A2,2 0 0,1 6,10A2,2 0 0,1 8,12A2,2 0 0,1 6,14A2,2 0 0,1 4,12Z",members:{event:{},geo_location:{},homeassistant:{},mqtt:{},conversation:{},tag:{},template:{},webhook:{},persistent_notification:{}}}}},6052:(e,t,i)=>{var a=i(5461),r=i(9534),s=i(2518),n=i(8597),o=i(196),l=i(6580),d=i(7905),u=i(3167),c=i(3049),h=i(4449),g=(i(6494),i(920),i(9154),i(9222),i(7237)),p=i(6349),m=(i(3981),i(9760)),v=i(662),f=i(4517),k=i(1695),y=i(8226),_=i(1355),b=(i(1074),i(4392),i(1686),i(6396),i(9373),i(1673)),$=i(8712),C=i(4164),A=i(4671),M=i(9032),x=i(1447),L=i(3799),w=i(5081),V=(i(3259),i(7545));(0,a.A)([(0,o.EM)("ha-automation-trigger-calendar")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",key:"_schema",value(){return(0,w.A)((e=>[{name:"entity_id",required:!0,selector:{entity:{domain:"calendar"}}},{name:"event",type:"select",required:!0,options:[["start",e("ui.panel.config.automation.editor.triggers.type.calendar.start")],["end",e("ui.panel.config.automation.editor.triggers.type.calendar.end")]]},{name:"offset",selector:{duration:{}}},{name:"offset_type",type:"select",required:!0,options:[["before",e("ui.panel.config.automation.editor.triggers.type.calendar.before")],["after",e("ui.panel.config.automation.editor.triggers.type.calendar.after")]]}]))}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"calendar",entity_id:"",event:"start",offset:"0"}}},{kind:"method",key:"render",value:function(){const e=this._schema(this.hass.localize),t=this.trigger.offset,i=(0,V.z)(t);let a="after";("object"==typeof t&&i.hours<0||"string"==typeof t&&t.startsWith("-"))&&(i.hours=Math.abs(i.hours),a="before");const r={...this.trigger,offset:i,offset_type:a};return n.qy`
      <ha-form
        .schema=${e}
        .data=${r}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value.offset,i="before"===e.detail.value.offset_type?"-":"",a={...e.detail.value,offset:`${i}${t.hours??0}:${t.minutes??0}:${t.seconds??0}`};delete a.offset_type,(0,u.r)(this,"value-changed",{value:a})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"entity_id":return this.hass.localize("ui.components.entity.entity-picker.entity");case"event":return this.hass.localize("ui.panel.config.automation.editor.triggers.type.calendar.event")}return""}}}]}}),n.WF);var H=i(6041);const z="^[^.。,，?¿？؟!！;；:：]+$";(0,a.A)([(0,o.EM)("ha-automation-trigger-conversation")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.P)("#option_input",!0)],key:"_optionInput",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"conversation",command:""}}},{kind:"method",key:"render",value:function(){const{command:e}=this.trigger,t=e?(0,H.e)(e):[];return n.qy`${t.length?t.map(((e,t)=>n.qy`
              <ha-textfield
                class="option"
                iconTrailing
                .index=${t}
                .value=${e}
                .validationMessage=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.conversation.no_punctuation")}
                autoValidate
                validateOnInitialRender
                pattern=${z}
                @change=${this._updateOption}
              >
                <ha-icon-button
                  @click=${this._removeOption}
                  slot="trailingIcon"
                  .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
                ></ha-icon-button>
              </ha-textfield>
            `)):n.s6}
      <ha-textfield
        class="flex-auto"
        id="option_input"
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.conversation.add_sentence")}
        .validationMessage=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.conversation.no_punctuation")}
        autoValidate
        pattern=${z}
        @keydown=${this._handleKeyAdd}
        @change=${this._addOption}
      ></ha-textfield>`}},{kind:"method",key:"_handleKeyAdd",value:function(e){e.stopPropagation(),"Enter"===e.key&&this._addOption()}},{kind:"method",key:"_addOption",value:function(){const e=this._optionInput;e?.value&&((0,u.r)(this,"value-changed",{value:{...this.trigger,command:this.trigger.command.length?[...Array.isArray(this.trigger.command)?this.trigger.command:[this.trigger.command],e.value]:e.value}}),e.value="")}},{kind:"method",key:"_updateOption",value:async function(e){const t=e.target.index,i=[...Array.isArray(this.trigger.command)?this.trigger.command:[this.trigger.command]];i.splice(t,1,e.target.value),(0,u.r)(this,"value-changed",{value:{...this.trigger,command:i}})}},{kind:"method",key:"_removeOption",value:async function(e){const t=e.target.parentElement.index;if(!(await(0,x.dk)(this,{title:this.hass.localize("ui.panel.config.automation.editor.triggers.type.conversation.delete"),text:this.hass.localize("ui.panel.config.automation.editor.triggers.type.conversation.confirm_delete"),destructive:!0})))return;let i;Array.isArray(this.trigger.command)?(i=[...this.trigger.command],i.splice(t,1)):i="",(0,u.r)(this,"value-changed",{value:{...this.trigger,command:i}})}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      .layout {
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        align-items: center;
        justify-content: flex-start;
      }
      .option {
        margin-top: 4px;
      }
      mwc-button {
        margin-left: 8px;
        margin-inline-start: 8px;
        margin-inline-end: initial;
      }
      ha-textfield {
        display: block;
        margin-bottom: 8px;
        --textfield-icon-trailing-padding: 0;
      }
      ha-textfield > ha-icon-button {
        position: relative;
        right: -8px;
        --mdc-icon-button-size: 36px;
        --mdc-icon-size: 20px;
        color: var(--secondary-text-color);
        inset-inline-start: initial;
        inset-inline-end: -8px;
        direction: var(--direction);
      }
      #option_input {
        margin-top: 8px;
      }
      .header {
        margin-top: 8px;
        margin-bottom: 8px;
      }
    `}}]}}),n.WF);var Z=i(9411),q=(i(7190),i(5336)),E=i(2358);(0,a.A)([(0,o.EM)("ha-device-trigger-picker")],(function(e,t){return{F:class extends t{constructor(){super(q.nx,q.o9,(e=>({device_id:e||"",platform:"device",domain:"",entity_id:""}))),e(this)}},d:[{kind:"get",key:"NO_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.triggers.no_triggers")}},{kind:"get",key:"UNKNOWN_AUTOMATION_TEXT",value:function(){return this.hass.localize("ui.panel.config.devices.automation.triggers.unknown_trigger")}}]}}),E.V);var U=i(9451);(0,a.A)([(0,o.EM)("ha-automation-trigger-device")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Object})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_deviceId",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_capabilities",value:void 0},{kind:"field",decorators:[(0,o.wk)(),(0,p.Fg)({context:A.ih,subscribe:!0})],key:"_entityReg",value:void 0},{kind:"field",key:"_origTrigger",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"device",device_id:"",domain:"",entity_id:""}}},{kind:"field",key:"_extraFieldsData",value(){return(0,w.A)(((e,t)=>{const i=(0,U.$)(t.extra_fields);return t.extra_fields.forEach((t=>{void 0!==e[t.name]&&(i[t.name]=e[t.name])})),i}))}},{kind:"method",key:"render",value:function(){const e=this._deviceId||this.trigger.device_id;return n.qy`
      <ha-device-picker
        .value=${e}
        @value-changed=${this._devicePicked}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.device.label")}
      ></ha-device-picker>
      <ha-device-trigger-picker
        .value=${this.trigger}
        .deviceId=${e}
        @value-changed=${this._deviceTriggerPicked}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.device.trigger")}
      ></ha-device-trigger-picker>
      ${this._capabilities?.extra_fields?n.qy`
            <ha-form
              .hass=${this.hass}
              .data=${this._extraFieldsData(this.trigger,this._capabilities)}
              .schema=${this._capabilities.extra_fields}
              .disabled=${this.disabled}
              .computeLabel=${(0,q.T_)(this.hass,this.trigger)}
              .computeHelper=${(0,q.TH)(this.hass,this.trigger)}
              @value-changed=${this._extraFieldsChanged}
            ></ha-form>
          `:""}
    `}},{kind:"method",key:"firstUpdated",value:function(){this._capabilities||this._getCapabilities(),this.trigger&&(this._origTrigger=this.trigger)}},{kind:"method",key:"updated",value:function(e){if(!e.has("trigger"))return;const t=e.get("trigger");t&&!(0,q.Po)(this._entityReg,t,this.trigger)&&this._getCapabilities()}},{kind:"method",key:"_getCapabilities",value:async function(){const e=this.trigger;if(this._capabilities=e.domain?await(0,q.TB)(this.hass,e):void 0,this._capabilities){const e={...this.trigger,...this._extraFieldsData(this.trigger,this._capabilities)};(0,Z.b)(this.trigger,e)||(0,u.r)(this,"value-changed",{value:e})}}},{kind:"method",key:"_devicePicked",value:function(e){e.stopPropagation(),this._deviceId=e.target.value,void 0===this._deviceId&&(0,u.r)(this,"value-changed",{value:{...i.defaultConfig,platform:"device"}})}},{kind:"method",key:"_deviceTriggerPicked",value:function(e){e.stopPropagation();let t=e.detail.value;this._origTrigger&&(0,q.Po)(this._entityReg,this._origTrigger,t)&&(t=this._origTrigger),this.trigger.id&&(t.id=this.trigger.id),(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_extraFieldsChanged",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.trigger,...e.detail.value}})}},{kind:"field",static:!0,key:"styles",value(){return n.AH`
    ha-device-picker {
      display: block;
      margin-bottom: 24px;
    }

    ha-form {
      display: block;
      margin-top: 24px;
    }
  `}}]}}),n.WF);i(2459);var P=i(4078),T=i(2154);const F={},I=(0,T.u$)(class extends T.WL{constructor(){super(...arguments),this.st=F}render(e,t){return t()}update(e,[t,i]){if(Array.isArray(t)){if(Array.isArray(this.st)&&this.st.length===t.length&&t.every(((e,t)=>e===this.st[t])))return P.c0}else if(this.st===t)return P.c0;return this.st=Array.isArray(t)?Array.from(t):t,this.render(t,i)}}),S=async e=>e.callWS({type:"config/auth/list"});var O=i(6412),W=(i(6334),i(2506)),B=i(85);(0,a.A)([(0,o.EM)("ha-user-badge")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"user",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_personPicture",value:void 0},{kind:"field",key:"_personEntityId",value:void 0},{kind:"method",key:"willUpdate",value:function(e){if((0,r.A)(i,"willUpdate",this,3)([e]),e.has("user"))return void this._getPersonPicture();const t=e.get("hass");if(this._personEntityId&&t&&this.hass.states[this._personEntityId]!==t.states[this._personEntityId]){const e=this.hass.states[this._personEntityId];e?this._personPicture=e.attributes.entity_picture:this._getPersonPicture()}else!this._personEntityId&&t&&this._getPersonPicture()}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.user)return n.s6;const e=this._personPicture;if(e)return n.qy`<div
        style=${(0,W.W)({backgroundImage:`url(${e})`})}
        class="picture"
      ></div>`;const t=(i=this.user.name)?i.trim().split(" ").slice(0,3).map((e=>e.substring(0,1))).join(""):"?";var i;return n.qy`<div
      class="initials ${(0,m.H)({long:t.length>2})}"
    >
      ${t}
    </div>`}},{kind:"method",key:"_getPersonPicture",value:function(){if(this._personEntityId=void 0,this._personPicture=void 0,this.hass&&this.user)for(const e of Object.values(this.hass.states))if(e.attributes.user_id===this.user.id&&"person"===(0,B.t)(e)){this._personEntityId=e.entity_id,this._personPicture=e.attributes.entity_picture;break}}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      :host {
        display: contents;
      }
      .picture {
        width: 40px;
        height: 40px;
        background-size: cover;
        border-radius: 50%;
      }
      .initials {
        display: inline-block;
        box-sizing: border-box;
        width: 40px;
        line-height: 40px;
        border-radius: 50%;
        text-align: center;
        background-color: var(--light-primary-color);
        text-decoration: none;
        color: var(--text-light-primary-color, var(--primary-text-color));
        overflow: hidden;
      }
      .initials.long {
        font-size: 80%;
      }
    `}}]}}),n.WF);i(9484);let j=(0,a.A)(null,(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"noUserLabel",value:void 0},{kind:"field",decorators:[(0,o.MZ)()],key:"value",value(){return""}},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"users",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",key:"_sortedUsers",value(){return(0,w.A)((e=>e?e.filter((e=>!e.system_generated)).sort(((e,t)=>(0,O.x)(e.name,t.name,this.hass.locale.language))):[]))}},{kind:"method",key:"render",value:function(){return n.qy`
      <ha-select
        .label=${this.label}
        .disabled=${this.disabled}
        .value=${this.value}
        @selected=${this._userChanged}
      >
        ${0===this.users?.length?n.qy`<mwc-list-item value="">
              ${this.noUserLabel||this.hass?.localize("ui.components.user-picker.no_user")}
            </mwc-list-item>`:""}
        ${this._sortedUsers(this.users).map((e=>n.qy`
            <ha-list-item graphic="avatar" .value=${e.id}>
              <ha-user-badge
                .hass=${this.hass}
                .user=${e}
                slot="graphic"
              ></ha-user-badge>
              ${e.name}
            </ha-list-item>
          `))}
      </ha-select>
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,r.A)(i,"firstUpdated",this,3)([e]),void 0===this.users&&S(this.hass).then((e=>{this.users=e}))}},{kind:"method",key:"_userChanged",value:function(e){const t=e.target.value;t!==this.value&&(this.value=t,setTimeout((()=>{(0,u.r)(this,"value-changed",{value:t}),(0,u.r)(this,"change")}),0))}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      :host {
        display: inline-block;
      }
      mwc-list {
        display: block;
      }
    `}}]}}),n.WF);customElements.define("ha-user-picker",j);(0,a.A)([(0,o.EM)("ha-users-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:"picked-user-label"})],key:"pickedUserLabel",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:"pick-user-label"})],key:"pickUserLabel",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"users",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(e){(0,r.A)(i,"firstUpdated",this,3)([e]),void 0===this.users&&S(this.hass).then((e=>{this.users=e}))}},{kind:"method",key:"render",value:function(){if(!this.hass||!this.users)return n.s6;const e=this._notSelectedUsers(this.users,this.value);return n.qy`
      ${I([e],(()=>this.value?.map(((t,i)=>n.qy`
            <div>
              <ha-user-picker
                .label=${this.pickedUserLabel}
                .noUserLabel=${this.hass.localize("ui.components.user-picker.remove_user")}
                .index=${i}
                .hass=${this.hass}
                .value=${t}
                .users=${this._notSelectedUsersAndSelected(t,this.users,e)}
                .disabled=${this.disabled}
                @value-changed=${this._userChanged}
              ></ha-user-picker>
              <ha-icon-button
                .userId=${t}
                .label=${this.hass.localize("ui.components.user-picker.remove_user")}
                .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
                @click=${this._removeUser}
              >
                ></ha-icon-button
              >
            </div>
          `))))}
      <ha-user-picker
        .label=${this.pickUserLabel||this.hass.localize("ui.components.user-picker.add_user")}
        .hass=${this.hass}
        .users=${e}
        .disabled=${this.disabled||!e?.length}
        @value-changed=${this._addUser}
      ></ha-user-picker>
    `}},{kind:"field",key:"_notSelectedUsers",value(){return(0,w.A)(((e,t)=>t?e?.filter((e=>!e.system_generated&&!t.includes(e.id))):e?.filter((e=>!e.system_generated))))}},{kind:"field",key:"_notSelectedUsersAndSelected",value(){return(e,t,i)=>{const a=t?.find((t=>t.id===e));return a?i?[...i,a]:[a]:i}}},{kind:"get",key:"_currentUsers",value:function(){return this.value||[]}},{kind:"method",key:"_updateUsers",value:async function(e){this.value=e,(0,u.r)(this,"value-changed",{value:e})}},{kind:"method",key:"_userChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.index,i=e.detail.value,a=[...this._currentUsers];""===i?a.splice(t,1):a.splice(t,1,i),this._updateUsers(a)}},{kind:"method",key:"_addUser",value:async function(e){e.stopPropagation();const t=e.detail.value;if(e.currentTarget.value="",!t)return;const i=this._currentUsers;i.includes(t)||this._updateUsers([...i,t])}},{kind:"method",key:"_removeUser",value:function(e){const t=e.currentTarget.userId;this._updateUsers(this._currentUsers.filter((e=>e!==t)))}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      :host {
        display: block;
      }
      div {
        display: flex;
        align-items: center;
      }
    `}}]}}),n.WF),(0,a.A)([(0,o.EM)("ha-automation-trigger-event")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"event",event_type:""}}},{kind:"method",key:"render",value:function(){const{event_type:e,event_data:t,context:i}=this.trigger;return n.qy`
      <ha-textfield
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.event_type")}
        name="event_type"
        .value=${e}
        .disabled=${this.disabled}
        @change=${this._valueChanged}
      ></ha-textfield>
      <ha-yaml-editor
        .hass=${this.hass}
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.event_data")}
        .name=${"event_data"}
        .readOnly=${this.disabled}
        .defaultValue=${t}
        @value-changed=${this._dataChanged}
      ></ha-yaml-editor>
      <br />
      ${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.context_users")}
      <ha-users-picker
        .pickedUserLabel=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.context_user_picked")}
        .pickUserLabel=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.event.context_user_pick")}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .value=${this._wrapUsersInArray(i?.user_id)}
        @value-changed=${this._usersChanged}
      ></ha-users-picker>
    `}},{kind:"method",key:"_wrapUsersInArray",value:function(e){return e?"string"==typeof e?[e]:e:[]}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),de(this,e)}},{kind:"method",key:"_dataChanged",value:function(e){e.stopPropagation(),e.detail.isValid&&de(this,e)}},{kind:"method",key:"_usersChanged",value:function(e){e.stopPropagation();const t={...this.trigger};!e.detail.value.length&&t.context?delete t.context.user_id:(t.context||(t.context={}),t.context.user_id=e.detail.value),(0,u.r)(this,"value-changed",{value:t})}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      ha-textfield {
        display: block;
      }
    `}}]}}),n.WF),(0,a.A)([(0,o.EM)("ha-automation-trigger-geo_location")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",key:"_schema",value(){return(0,w.A)((e=>[{name:"source",selector:{text:{}}},{name:"zone",selector:{entity:{domain:"zone"}}},{name:"event",type:"select",required:!0,options:[["enter",e("ui.panel.config.automation.editor.triggers.type.geo_location.enter")],["leave",e("ui.panel.config.automation.editor.triggers.type.geo_location.leave")]]}]))}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"geo_location",source:"",zone:"",event:"enter"}}},{kind:"method",key:"render",value:function(){return n.qy`
      <ha-form
        .schema=${this._schema(this.hass.localize)}
        .data=${this.trigger}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.geo_location.${e.name}`)}}]}}),n.WF),(0,a.A)([(0,o.EM)("ha-automation-trigger-homeassistant")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",key:"_schema",value(){return(0,w.A)((e=>[{name:"event",type:"select",required:!0,options:[["start",e("ui.panel.config.automation.editor.triggers.type.homeassistant.start")],["shutdown",e("ui.panel.config.automation.editor.triggers.type.homeassistant.shutdown")]]}]))}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"homeassistant",event:"start"}}},{kind:"method",key:"render",value:function(){return n.qy`
      <ha-form
        .schema=${this._schema(this.hass.localize)}
        .data=${this.trigger}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.homeassistant.${e.name}`)}},{kind:"field",static:!0,key:"styles",value(){return n.AH`
    label {
      display: flex;
      align-items: center;
    }
  `}}]}}),n.WF);const R=[{name:"topic",required:!0,selector:{text:{}}},{name:"payload",selector:{text:{}}}];(0,a.A)([(0,o.EM)("ha-automation-trigger-mqtt")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"mqtt",topic:""}}},{kind:"method",key:"render",value:function(){return n.qy`
      <ha-form
        .schema=${R}
        .data=${this.trigger}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.mqtt.${e.name}`)}}]}}),n.WF);var N=i(6678);(0,a.A)([(0,o.EM)("ha-automation-trigger-numeric_state")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_inputAboveIsEntity",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_inputBelowIsEntity",value:void 0},{kind:"field",key:"_schema",value(){return(0,w.A)(((e,t,i,a)=>[{name:"entity_id",required:!0,selector:{entity:{multiple:!0}}},{name:"attribute",selector:{attribute:{entity_id:t?t[0]:void 0,hide_attributes:["access_token","auto_update","available_modes","away_mode","changed_by","code_arm_required","code_format","color_mode","color_modes","current_activity","device_class","editable","effect_list","effect","entity_id","entity_picture","event_type","event_types","fan_mode","fan_modes","fan_speed_list","forecast","friendly_name","frontend_stream_type","has_date","has_time","hs_color","hvac_mode","hvac_modes","icon","id","latest_version","max_color_temp_kelvin","max_mireds","max_temp","media_album_name","media_artist","media_content_type","media_position_updated_at","media_title","min_color_temp_kelvin","min_mireds","min_temp","mode","next_dawn","next_dusk","next_midnight","next_noon","next_rising","next_setting","operation_list","operation_mode","options","percentage_step","precipitation_unit","preset_mode","preset_modes","pressure_unit","release_notes","release_summary","release_url","restored","rgb_color","rgbw_color","shuffle","skipped_version","sound_mode_list","sound_mode","source_list","source_type","source","state_class","step","supported_color_modes","supported_features","swing_mode","swing_modes","target_temp_step","temperature_unit","title","token","unit_of_measurement","user_id","uuid","visibility_unit","wind_speed_unit","xy_color"]}}},{name:"mode_above",type:"select",required:!0,options:[["value",e("ui.panel.config.automation.editor.triggers.type.numeric_state.type_value")],["input",e("ui.panel.config.automation.editor.triggers.type.numeric_state.type_input")]]},...i?[{name:"above",selector:{entity:{domain:["input_number","number","sensor"]}}}]:[{name:"above",selector:{number:{mode:"box",min:Number.MIN_SAFE_INTEGER,max:Number.MAX_SAFE_INTEGER,step:.1}}}],{name:"mode_below",type:"select",required:!0,options:[["value",e("ui.panel.config.automation.editor.triggers.type.numeric_state.type_value")],["input",e("ui.panel.config.automation.editor.triggers.type.numeric_state.type_input")]]},...a?[{name:"below",selector:{entity:{domain:["input_number","number","sensor"]}}}]:[{name:"below",selector:{number:{mode:"box",min:Number.MIN_SAFE_INTEGER,max:Number.MAX_SAFE_INTEGER,step:.1}}}],{name:"value_template",selector:{template:{}}},{name:"for",selector:{duration:{}}}]))}},{kind:"method",key:"willUpdate",value:function(e){e.has("trigger")&&this.trigger&&(0,N.r)(this.trigger.for)&&(0,u.r)(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.no_template_editor_support")))}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"numeric_state",entity_id:[]}}},{kind:"method",key:"render",value:function(){const e=(0,V.z)(this.trigger.for),t=this._inputAboveIsEntity??("string"==typeof this.trigger.above&&(this.trigger.above.startsWith("input_number.")||this.trigger.above.startsWith("number.")||this.trigger.above.startsWith("sensor."))),i=this._inputBelowIsEntity??("string"==typeof this.trigger.below&&(this.trigger.below.startsWith("input_number.")||this.trigger.below.startsWith("number.")||this.trigger.below.startsWith("sensor."))),a=this._schema(this.hass.localize,this.trigger.entity_id,t,i),r={mode_above:t?"input":"value",mode_below:i?"input":"value",...this.trigger,entity_id:(0,H.e)(this.trigger.entity_id),for:e};return n.qy`
      <ha-form
        .hass=${this.hass}
        .data=${r}
        .schema=${a}
        .disabled=${this.disabled}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;this._inputAboveIsEntity="input"===t.mode_above,this._inputBelowIsEntity="input"===t.mode_below,delete t.mode_above,delete t.mode_below,""===t.value_template&&delete t.value_template,(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"entity_id":return this.hass.localize("ui.components.entity.entity-picker.entity");case"attribute":return this.hass.localize("ui.components.entity.entity-attribute-picker.attribute");case"for":return this.hass.localize("ui.panel.config.automation.editor.triggers.type.state.for");default:return this.hass.localize(`ui.panel.config.automation.editor.triggers.type.numeric_state.${e.name}`)}}}}]}}),n.WF);i(3604);const D=["added","removed"];(0,a.A)([(0,o.EM)("ha-automation-trigger-persistent_notification")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",key:"_schema",value(){return(0,w.A)((e=>[{name:"notification_id",required:!1,selector:{text:{}}},{name:"update_type",type:"multi_select",required:!1,options:[["added",e("ui.panel.config.automation.editor.triggers.type.persistent_notification.update_types.added")],["removed",e("ui.panel.config.automation.editor.triggers.type.persistent_notification.update_types.removed")],["current",e("ui.panel.config.automation.editor.triggers.type.persistent_notification.update_types.current")],["updated",e("ui.panel.config.automation.editor.triggers.type.persistent_notification.update_types.updated")]]}]))}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"persistent_notification",update_type:[...D],notification_id:""}}},{kind:"method",key:"render",value:function(){const e=this._schema(this.hass.localize);return n.qy`
      <ha-form
        .schema=${e}
        .data=${this.trigger}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.persistent_notification.${e.name}`)}},{kind:"field",static:!0,key:"styles",value(){return n.AH`
    ha-textfield {
      display: block;
    }
  `}}]}}),n.WF);var K=i(3428),Y=i(706);const G=(0,K.kp)(Y.V,(0,K.Ik)({alias:(0,K.lq)((0,K.Yj)()),platform:(0,K.eu)("state"),entity_id:(0,K.lq)((0,K.KC)([(0,K.Yj)(),(0,K.YO)((0,K.Yj)())])),attribute:(0,K.lq)((0,K.Yj)()),from:(0,K.lq)((0,K.me)((0,K.Yj)())),to:(0,K.lq)((0,K.me)((0,K.Yj)())),for:(0,K.lq)((0,K.KC)([(0,K.ai)(),(0,K.Yj)(),Y.b]))})),X="__ANY_STATE_IGNORE_ATTRIBUTES__";(0,a.A)([(0,o.EM)("ha-automation-trigger-state")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"state",entity_id:[]}}},{kind:"field",key:"_schema",value(){return(0,w.A)(((e,t,i)=>[{name:"entity_id",required:!0,selector:{entity:{multiple:!0}}},{name:"attribute",selector:{attribute:{entity_id:t?t[0]:void 0,hide_attributes:["access_token","available_modes","code_arm_required","code_format","color_modes","device_class","editable","effect_list","entity_id","entity_picture","event_types","fan_modes","fan_speed_list","friendly_name","frontend_stream_type","has_date","has_time","hvac_modes","icon","id","max_color_temp_kelvin","max_mireds","max_temp","max","min_color_temp_kelvin","min_mireds","min_temp","min","mode","operation_list","options","percentage_step","precipitation_unit","preset_modes","pressure_unit","sound_mode_list","source_list","state_class","step","supported_color_modes","supported_features","swing_modes","target_temp_step","temperature_unit","token","unit_of_measurement","visibility_unit","wind_speed_unit"]}}},{name:"from",selector:{state:{extra_options:i?[]:[{label:e("ui.panel.config.automation.editor.triggers.type.state.any_state_ignore_attributes"),value:X}],entity_id:t?t[0]:void 0,attribute:i}}},{name:"to",selector:{state:{extra_options:i?[]:[{label:e("ui.panel.config.automation.editor.triggers.type.state.any_state_ignore_attributes"),value:X}],entity_id:t?t[0]:void 0,attribute:i}}},{name:"for",selector:{duration:{}}}]))}},{kind:"method",key:"shouldUpdate",value:function(e){if(!e.has("trigger"))return!0;if(this.trigger.for&&"object"==typeof this.trigger.for&&0===this.trigger.for.milliseconds&&delete this.trigger.for.milliseconds,this.trigger&&(0,N.r)(this.trigger))return(0,u.r)(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.no_template_editor_support"))),!1;try{(0,K.vA)(this.trigger,G)}catch(F){return(0,u.r)(this,"ui-mode-not-available",F),!1}return!0}},{kind:"method",key:"render",value:function(){const e=(0,V.z)(this.trigger.for),t={...this.trigger,entity_id:(0,H.e)(this.trigger.entity_id),for:e};t.attribute||null!==t.to||(t.to=X),t.attribute||null!==t.from||(t.from=X);const i=this._schema(this.hass.localize,this.trigger.entity_id,this.trigger.attribute);return n.qy`
      <ha-form
        .hass=${this.hass}
        .data=${t}
        .schema=${i}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
        .disabled=${this.disabled}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;t.to===X&&(t.to=t.attribute?void 0:null),t.from===X&&(t.from=t.attribute?void 0:null),Object.keys(t).forEach((e=>void 0===t[e]||""===t[e]?delete t[e]:{})),(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize("entity_id"===e.name?"ui.components.entity.entity-picker.entity":`ui.panel.config.automation.editor.triggers.type.state.${e.name}`)}}]}}),n.WF),(0,a.A)([(0,o.EM)("ha-automation-trigger-sun")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",key:"_schema",value(){return(0,w.A)((e=>[{name:"event",type:"select",required:!0,options:[["sunrise",e("ui.panel.config.automation.editor.triggers.type.sun.sunrise")],["sunset",e("ui.panel.config.automation.editor.triggers.type.sun.sunset")]]},{name:"offset",selector:{text:{}}}]))}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"sun",event:"sunrise",offset:0}}},{kind:"method",key:"render",value:function(){const e=this._schema(this.hass.localize);return n.qy`
      <ha-form
        .schema=${e}
        .data=${this.trigger}
        .hass=${this.hass}
        .disabled=${this.disabled}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.sun.${e.name}`)}}]}}),n.WF);(0,a.A)([(0,o.EM)("ha-automation-trigger-tag")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_tags",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"tag",tag_id:""}}},{kind:"method",key:"firstUpdated",value:function(e){(0,r.A)(i,"firstUpdated",this,3)([e]),this._fetchTags()}},{kind:"method",key:"render",value:function(){return this._tags?n.qy`
      <ha-select
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.tag.label")}
        .disabled=${this.disabled||0===this._tags.length}
        .value=${this.trigger.tag_id}
        @selected=${this._tagChanged}
      >
        ${this._tags.map((e=>n.qy`
            <mwc-list-item .value=${e.id}>
              ${e.name||e.id}
            </mwc-list-item>
          `))}
      </ha-select>
    `:n.s6}},{kind:"method",key:"_fetchTags",value:async function(){this._tags=(await(async e=>e.callWS({type:"tag/list"}))(this.hass)).sort(((e,t)=>(0,O.S)(e.name||e.id,t.name||t.id,this.hass.locale.language)))}},{kind:"method",key:"_tagChanged",value:function(e){e.target.value&&this._tags&&this.trigger.tag_id!==e.target.value&&(0,u.r)(this,"value-changed",{value:{...this.trigger,tag_id:e.target.value}})}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      ha-select {
        display: block;
      }
    `}}]}}),n.WF);i(7984);const J=[{name:"value_template",required:!0,selector:{template:{}}},{name:"for",selector:{duration:{}}}];(0,a.A)([(0,o.EM)("ha-automation-trigger-template")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"template",value_template:""}}},{kind:"method",key:"willUpdate",value:function(e){e.has("trigger")&&this.trigger&&(0,N.r)(this.trigger.for)&&(0,u.r)(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.no_template_editor_support")))}},{kind:"method",key:"render",value:function(){const e=(0,V.z)(this.trigger.for),t={...this.trigger,for:e};return n.qy`
      <ha-form
        .hass=${this.hass}
        .data=${t}
        .schema=${J}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
        .disabled=${this.disabled}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;t.for&&Object.values(t.for).every((e=>0===e))&&delete t.for,(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.template.${e.name}`)}}]}}),n.WF),(0,a.A)([(0,o.EM)("ha-automation-trigger-time")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_inputMode",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"time",at:""}}},{kind:"field",key:"_schema",value(){return(0,w.A)(((e,t)=>{const i=t?{entity:{filter:[{domain:"input_datetime"},{domain:"sensor",device_class:"timestamp"}]}}:{time:{}};return[{name:"mode",type:"select",required:!0,options:[["value",e("ui.panel.config.automation.editor.triggers.type.time.type_value")],["input",e("ui.panel.config.automation.editor.triggers.type.time.type_input")]]},{name:"at",selector:i}]}))}},{kind:"method",key:"willUpdate",value:function(e){e.has("trigger")&&this.trigger&&Array.isArray(this.trigger.at)&&(0,u.r)(this,"ui-mode-not-available",Error(this.hass.localize("ui.errors.config.editor_not_supported")))}},{kind:"method",key:"render",value:function(){const e=this.trigger.at;if(Array.isArray(e))return n.s6;const t=this._inputMode??(e?.startsWith("input_datetime.")||e?.startsWith("sensor.")),i=this._schema(this.hass.localize,t),a={mode:t?"input":"value",...this.trigger};return n.qy`
      <ha-form
        .hass=${this.hass}
        .data=${a}
        .schema=${i}
        .disabled=${this.disabled}
        @value-changed=${this._valueChanged}
        .computeLabel=${this._computeLabelCallback}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;this._inputMode="input"===t.mode,delete t.mode,Object.keys(t).forEach((e=>void 0===t[e]||""===t[e]?delete t[e]:{})),(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.time.${e.name}`)}}]}}),n.WF);const Q=[{name:"hours",selector:{text:{}}},{name:"minutes",selector:{text:{}}},{name:"seconds",selector:{text:{}}}];(0,a.A)([(0,o.EM)("ha-automation-trigger-time_pattern")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"time_pattern"}}},{kind:"method",key:"render",value:function(){return n.qy`
      <ha-form
        .hass=${this.hass}
        .schema=${Q}
        .data=${this.trigger}
        .disabled=${this.disabled}
        .computeLabel=${this._computeLabelCallback}
        @value-changed=${this._valueChanged}
      ></ha-form>
    `}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value;(0,u.r)(this,"value-changed",{value:t})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.panel.config.automation.editor.triggers.type.time_pattern.${e.name}`)}}]}}),n.WF);var ee=i(4848),te=i(7162),ie=i(4947);const ae=["GET","HEAD","POST","PUT"],re=["POST","PUT"];(0,a.A)([(0,o.EM)("ha-automation-trigger-webhook")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_config",value:void 0},{kind:"field",key:"_unsub",value:void 0},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"webhook",allowed_methods:[...re],local_only:!0,webhook_id:""}}},{kind:"method",key:"connectedCallback",value:function(){(0,r.A)(i,"connectedCallback",this,3)([]);const e={callback:e=>{this._config=e}};(0,u.r)(this,"subscribe-automation-config",e),this._unsub=e.unsub}},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.A)(i,"disconnectedCallback",this,3)([]),this._unsub&&this._unsub()}},{kind:"method",key:"_generateWebhookId",value:function(){const e=crypto.getRandomValues(new Uint8Array(18)),t=btoa(String.fromCharCode(...e)).replace(/\+/g,"-").replace(/\//g,"_");return`${(0,ee.Y)(this._config?.alias||"","-")}-${t}`}},{kind:"method",key:"willUpdate",value:function(e){(0,r.A)(i,"willUpdate",this,3)([e]),e.has("trigger")&&(void 0===this.trigger.allowed_methods&&(this.trigger.allowed_methods=[...re]),void 0===this.trigger.local_only&&(this.trigger.local_only=!0),""===this.trigger.webhook_id&&(this.trigger.webhook_id=this._generateWebhookId()))}},{kind:"method",key:"render",value:function(){const{allowed_methods:e,local_only:t,webhook_id:i}=this.trigger;return n.qy`
      <div class="flex">
        <ha-textfield
          name="webhook_id"
          .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.webhook.webhook_id")}
          .helper=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.webhook.webhook_id_helper")}
          .disabled=${this.disabled}
          iconTrailing
          .value=${i||""}
          @input=${this._valueChanged}
        >
          <ha-icon-button
            @click=${this._copyUrl}
            slot="trailingIcon"
            .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.webhook.copy_url")}
            .path=${"M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"}
          ></ha-icon-button>
        </ha-textfield>
        <ha-button-menu multi @closed=${f.d}>
          <ha-icon-button
            slot="trigger"
            .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.webhook.webhook_settings")}
            .path=${"M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"}
          ></ha-icon-button>
          ${ae.map((t=>n.qy`
              <ha-check-list-item
                left
                .value=${t}
                @request-selected=${this._allowedMethodsChanged}
                .selected=${e.includes(t)}
              >
                ${t}
              </ha-check-list-item>
            `))}
          <li divider role="separator"></li>
          <ha-check-list-item
            left
            @request-selected=${this._localOnlyChanged}
            .selected=${t}
          >
            ${this.hass.localize("ui.panel.config.automation.editor.triggers.type.webhook.local_only")}
          </ha-check-list-item>
        </ha-button-menu>
      </div>
    `}},{kind:"method",key:"_valueChanged",value:function(e){de(this,e)}},{kind:"method",key:"_localOnlyChanged",value:function(e){if(e.stopPropagation(),this.trigger.local_only===e.detail.selected)return;const t={...this.trigger,local_only:e.detail.selected};(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_allowedMethodsChanged",value:function(e){e.stopPropagation();const t=e.target.value,i=e.detail.selected;if(i===this.trigger.allowed_methods?.includes(t))return;const a=[...this.trigger.allowed_methods??[]];i?a.push(t):a.splice(a.indexOf(t),1);const r={...this.trigger,allowed_methods:a};(0,u.r)(this,"value-changed",{value:r})}},{kind:"method",key:"_copyUrl",value:async function(e){const t=e.target.parentElement,i=this.hass.hassUrl(`/api/webhook/${t.value}`);await(0,te.l)(i),(0,ie.P)(this,{message:this.hass.localize("ui.common.copied_clipboard")})}},{kind:"field",static:!0,key:"styles",value(){return n.AH`
    .flex {
      display: flex;
    }

    ha-textfield {
      flex: 1;
    }

    ha-textfield > ha-icon-button {
      --mdc-icon-button-size: 24px;
      --mdc-icon-size: 18px;
      color: var(--secondary-text-color);
    }

    ha-button-menu {
      padding-top: 4px;
    }
  `}}]}}),n.WF);i(5067),i(2694);var se=i(1519);function ne(e){return(0,se.e)(e)&&"zone"!==(0,B.t)(e)}const oe=["zone"];(0,a.A)([(0,o.EM)("ha-automation-trigger-zone")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"get",static:!0,key:"defaultConfig",value:function(){return{platform:"zone",entity_id:"",zone:"",event:"enter"}}},{kind:"method",key:"render",value:function(){const{entity_id:e,zone:t,event:i}=this.trigger;return n.qy`
      <ha-entity-picker
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.entity")}
        .value=${e}
        .disabled=${this.disabled}
        @value-changed=${this._entityPicked}
        .hass=${this.hass}
        allow-custom-entity
        .entityFilter=${ne}
      ></ha-entity-picker>
      <ha-entity-picker
        .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.zone")}
        .value=${t}
        .disabled=${this.disabled}
        @value-changed=${this._zonePicked}
        .hass=${this.hass}
        allow-custom-entity
        .includeDomains=${oe}
      ></ha-entity-picker>

      <label>
        ${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.event")}
        <ha-formfield
          .disabled=${this.disabled}
          .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.enter")}
        >
          <ha-radio
            name="event"
            value="enter"
            .disabled=${this.disabled}
            .checked=${"enter"===i}
            @change=${this._radioGroupPicked}
          ></ha-radio>
        </ha-formfield>
        <ha-formfield
          .disabled=${this.disabled}
          .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.type.zone.leave")}
        >
          <ha-radio
            name="event"
            value="leave"
            .disabled=${this.disabled}
            .checked=${"leave"===i}
            @change=${this._radioGroupPicked}
          ></ha-radio>
        </ha-formfield>
      </label>
    `}},{kind:"method",key:"_entityPicked",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.trigger,entity_id:e.detail.value}})}},{kind:"method",key:"_zonePicked",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.trigger,zone:e.detail.value}})}},{kind:"method",key:"_radioGroupPicked",value:function(e){e.stopPropagation(),(0,u.r)(this,"value-changed",{value:{...this.trigger,event:e.target.value}})}},{kind:"field",static:!0,key:"styles",value(){return n.AH`
    label {
      display: flex;
      align-items: center;
    }
    ha-entity-picker {
      display: block;
      margin-bottom: 24px;
    }
  `}}]}}),n.WF);const le="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z",de=(e,t)=>{t.stopPropagation();const i=t.currentTarget?.name;if(!i)return;const a=t.target?.value;if((e.trigger[i]||"")===a)return;let r;void 0===a||""===a?(r={...e.trigger},delete r[i]):r={...e.trigger,[i]:a},(0,u.r)(e,"value-changed",{value:r})},ue=e=>e.preventDefault();(0,a.A)([(0,o.EM)("ha-automation-trigger-row")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"trigger",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Array})],key:"path",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"first",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"last",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_warnings",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_yamlMode",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_requestShowId",value(){return!1}},{kind:"field",decorators:[(0,o.wk)()],key:"_triggered",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_triggerColor",value(){return!1}},{kind:"field",decorators:[(0,o.P)("ha-yaml-editor")],key:"_yamlEditor",value:void 0},{kind:"field",decorators:[(0,d.I)({key:"automationClipboard",state:!1,subscribe:!0,storage:"sessionStorage"})],key:"_clipboard",value:void 0},{kind:"field",decorators:[(0,o.wk)(),(0,p.Fg)({context:A.ih,subscribe:!0})],key:"_entityReg",value:void 0},{kind:"field",key:"_triggerUnsub",value:void 0},{kind:"method",key:"render",value:function(){if(!this.trigger)return n.s6;const e=void 0!==customElements.get(`ha-automation-trigger-${this.trigger.platform}`),t=this._yamlMode||!e,i="id"in this.trigger||this._requestShowId;return n.qy`
      <ha-card outlined>
        ${!1===this.trigger.enabled?n.qy`
              <div class="disabled-bar">
                ${this.hass.localize("ui.panel.config.automation.editor.actions.disabled")}
              </div>
            `:n.s6}

        <ha-expansion-panel leftChevron>
          <h3 slot="header">
            <ha-svg-icon
              class="trigger-icon"
              .path=${M.S[this.trigger.platform]}
            ></ha-svg-icon>
            ${(0,$.g)(this.trigger,this.hass,this._entityReg)}
          </h3>

          <slot name="icons" slot="icons"></slot>

          <ha-button-menu
            slot="icons"
            @action=${this._handleAction}
            @click=${ue}
            @closed=${f.d}
            fixed
          >
            <ha-icon-button
              slot="trigger"
              .label=${this.hass.localize("ui.common.menu")}
              .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
            ></ha-icon-button>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.triggers.rename")}
              <ha-svg-icon slot="graphic" .path=${"M18,17H10.5L12.5,15H18M6,17V14.5L13.88,6.65C14.07,6.45 14.39,6.45 14.59,6.65L16.35,8.41C16.55,8.61 16.55,8.92 16.35,9.12L8.47,17M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3Z"}></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.triggers.edit_id")}
              <ha-svg-icon slot="graphic" .path=${"M10 7V9H9V15H10V17H6V15H7V9H6V7H10M16 7C17.11 7 18 7.9 18 9V15C18 16.11 17.11 17 16 17H12V7M16 9H14V15H16V9Z"}></ha-svg-icon>
            </mwc-list-item>

            <li divider role="separator"></li>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.triggers.duplicate")}
              <ha-svg-icon
                slot="graphic"
                .path=${"M11,17H4A2,2 0 0,1 2,15V3A2,2 0 0,1 4,1H16V3H4V15H11V13L15,16L11,19V17M19,21V7H8V13H6V7A2,2 0 0,1 8,5H19A2,2 0 0,1 21,7V21A2,2 0 0,1 19,23H8A2,2 0 0,1 6,21V19H8V21H19Z"}
              ></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.triggers.copy")}
              <ha-svg-icon slot="graphic" .path=${"M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"}></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${this.hass.localize("ui.panel.config.automation.editor.triggers.cut")}
              <ha-svg-icon slot="graphic" .path=${"M19,3L13,9L15,11L22,4V3M12,12.5A0.5,0.5 0 0,1 11.5,12A0.5,0.5 0 0,1 12,11.5A0.5,0.5 0 0,1 12.5,12A0.5,0.5 0 0,1 12,12.5M6,20A2,2 0 0,1 4,18C4,16.89 4.9,16 6,16A2,2 0 0,1 8,18C8,19.11 7.1,20 6,20M6,8A2,2 0 0,1 4,6C4,4.89 4.9,4 6,4A2,2 0 0,1 8,6C8,7.11 7.1,8 6,8M9.64,7.64C9.87,7.14 10,6.59 10,6A4,4 0 0,0 6,2A4,4 0 0,0 2,6A4,4 0 0,0 6,10C6.59,10 7.14,9.87 7.64,9.64L10,12L7.64,14.36C7.14,14.13 6.59,14 6,14A4,4 0 0,0 2,18A4,4 0 0,0 6,22A4,4 0 0,0 10,18C10,17.41 9.87,16.86 9.64,16.36L12,14L19,21H22V20L9.64,7.64Z"}></ha-svg-icon>
            </mwc-list-item>

            <mwc-list-item
              graphic="icon"
              .disabled=${this.disabled||this.first}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.move_up")}
              <ha-svg-icon slot="graphic" .path=${"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"}></ha-svg-icon
            ></mwc-list-item>

            <mwc-list-item
              graphic="icon"
              .disabled=${this.disabled||this.last}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.move_down")}
              <ha-svg-icon slot="graphic" .path=${"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z"}></ha-svg-icon
            ></mwc-list-item>

            <li divider role="separator"></li>

            <mwc-list-item .disabled=${!e} graphic="icon">
              ${this.hass.localize("ui.panel.config.automation.editor.edit_ui")}
              ${t?"":n.qy`<ha-svg-icon
                    class="selected_menu_item"
                    slot="graphic"
                    .path=${le}
                  ></ha-svg-icon>`}
            </mwc-list-item>

            <mwc-list-item .disabled=${!e} graphic="icon">
              ${this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
              ${t?n.qy`<ha-svg-icon
                    class="selected_menu_item"
                    slot="graphic"
                    .path=${le}
                  ></ha-svg-icon>`:""}
            </mwc-list-item>

            <li divider role="separator"></li>

            <mwc-list-item graphic="icon" .disabled=${this.disabled}>
              ${!1===this.trigger.enabled?this.hass.localize("ui.panel.config.automation.editor.actions.enable"):this.hass.localize("ui.panel.config.automation.editor.actions.disable")}
              <ha-svg-icon
                slot="graphic"
                .path=${!1===this.trigger.enabled?"M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M10,16.5L16,12L10,7.5V16.5Z":"M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4M9,9V15H15V9"}
              ></ha-svg-icon>
            </mwc-list-item>
            <mwc-list-item
              class="warning"
              graphic="icon"
              .disabled=${this.disabled}
            >
              ${this.hass.localize("ui.panel.config.automation.editor.actions.delete")}
              <ha-svg-icon
                class="warning"
                slot="graphic"
                .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
              ></ha-svg-icon>
            </mwc-list-item>
          </ha-button-menu>

          <div
            class=${(0,m.H)({"card-content":!0,disabled:!1===this.trigger.enabled})}
          >
            ${this._warnings?n.qy`<ha-alert
                  alert-type="warning"
                  .title=${this.hass.localize("ui.errors.config.editor_not_supported")}
                >
                  ${this._warnings.length&&void 0!==this._warnings[0]?n.qy` <ul>
                        ${this._warnings.map((e=>n.qy`<li>${e}</li>`))}
                      </ul>`:""}
                  ${this.hass.localize("ui.errors.config.edit_in_yaml_supported")}
                </ha-alert>`:""}
            ${t?n.qy`
                  ${e?"":n.qy`
                        ${this.hass.localize("ui.panel.config.automation.editor.triggers.unsupported_platform",{platform:this.trigger.platform})}
                      `}
                  <ha-yaml-editor
                    .hass=${this.hass}
                    .defaultValue=${this.trigger}
                    .readOnly=${this.disabled}
                    @value-changed=${this._onYamlChange}
                  ></ha-yaml-editor>
                `:n.qy`
                  ${i?n.qy`
                        <ha-textfield
                          .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.id")}
                          .value=${this.trigger.id||""}
                          .disabled=${this.disabled}
                          @change=${this._idChanged}
                        >
                        </ha-textfield>
                      `:""}
                  <div
                    @ui-mode-not-available=${this._handleUiModeNotAvailable}
                    @value-changed=${this._onUiChanged}
                  >
                    ${(0,v._)(`ha-automation-trigger-${this.trigger.platform}`,{hass:this.hass,trigger:this.trigger,disabled:this.disabled,path:this.path})}
                  </div>
                `}
          </div>
        </ha-expansion-panel>

        <div
          class="triggered ${(0,m.H)({active:void 0!==this._triggered,accent:this._triggerColor})}"
          @click=${this._showTriggeredInfo}
        >
          ${this.hass.localize("ui.panel.config.automation.editor.triggers.triggered")}
        </div>
      </ha-card>
    `}},{kind:"method",key:"updated",value:function(e){(0,r.A)(i,"updated",this,3)([e]),e.has("trigger")&&this._subscribeTrigger()}},{kind:"method",key:"connectedCallback",value:function(){(0,r.A)(i,"connectedCallback",this,3)([]),this.hasUpdated&&this.trigger&&this._subscribeTrigger()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.A)(i,"disconnectedCallback",this,3)([]),this._triggerUnsub&&(this._triggerUnsub.then((e=>e())),this._triggerUnsub=void 0),this._doSubscribeTrigger.cancel()}},{kind:"method",key:"_subscribeTrigger",value:function(){this._triggerUnsub&&(this._triggerUnsub.then((e=>e())),this._triggerUnsub=void 0),this._doSubscribeTrigger()}},{kind:"field",key:"_doSubscribeTrigger",value(){return(0,_.s)((async()=>{let e;const t=this.trigger;this._triggerUnsub&&(this._triggerUnsub.then((e=>e())),this._triggerUnsub=void 0);if(!(await(0,C.$)(this.hass,{trigger:t})).trigger.valid||this.trigger!==t)return;const i=(0,b.Dp)(this.hass,(t=>{void 0!==e?(clearTimeout(e),this._triggerColor=!this._triggerColor):this._triggerColor=!1,this._triggered=t,e=window.setTimeout((()=>{this._triggered=void 0,e=void 0}),5e3)}),t);i.catch((()=>{this._triggerUnsub===i&&(this._triggerUnsub=void 0)})),this._triggerUnsub=i}),5e3)}},{kind:"method",key:"_handleUiModeNotAvailable",value:function(e){this._warnings=(0,y._)(this.hass,e.detail).warnings,this._yamlMode||(this._yamlMode=!0)}},{kind:"method",key:"_handleAction",value:async function(e){switch(e.detail.index){case 0:await this._renameTrigger();break;case 1:this._requestShowId=!0,this.expand();break;case 2:(0,u.r)(this,"duplicate");break;case 3:this._setClipboard();break;case 4:this._setClipboard(),(0,u.r)(this,"value-changed",{value:null});break;case 5:(0,u.r)(this,"move-up");break;case 6:(0,u.r)(this,"move-down");break;case 7:this._switchUiMode(),this.expand();break;case 8:this._switchYamlMode(),this.expand();break;case 9:this._onDisable();break;case 10:this._onDelete()}}},{kind:"method",key:"_setClipboard",value:function(){this._clipboard={...this._clipboard,trigger:this.trigger}}},{kind:"method",key:"_onDelete",value:function(){(0,x.dk)(this,{title:this.hass.localize("ui.panel.config.automation.editor.triggers.delete_confirm_title"),text:this.hass.localize("ui.panel.config.automation.editor.triggers.delete_confirm_text"),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.delete"),destructive:!0,confirm:()=>{(0,u.r)(this,"value-changed",{value:null})}})}},{kind:"method",key:"_onDisable",value:function(){const e=!(this.trigger.enabled??1),t={...this.trigger,enabled:e};(0,u.r)(this,"value-changed",{value:t}),this._yamlMode&&this._yamlEditor?.setValue(t)}},{kind:"method",key:"_idChanged",value:function(e){const t=e.target.value;if(t===(this.trigger.id??""))return;this._requestShowId=!0;const i={...this.trigger};t?i.id=t:delete i.id,(0,u.r)(this,"value-changed",{value:i})}},{kind:"method",key:"_onYamlChange",value:function(e){e.stopPropagation(),e.detail.isValid&&(this._warnings=void 0,(0,u.r)(this,"value-changed",{value:e.detail.value}))}},{kind:"method",key:"_onUiChanged",value:function(e){e.stopPropagation();const t={...this.trigger.alias?{alias:this.trigger.alias}:{},...e.detail.value};(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_switchUiMode",value:function(){this._warnings=void 0,this._yamlMode=!1}},{kind:"method",key:"_switchYamlMode",value:function(){this._warnings=void 0,this._yamlMode=!0}},{kind:"method",key:"_showTriggeredInfo",value:function(){(0,x.K$)(this,{title:this.hass.localize("ui.panel.config.automation.editor.triggers.triggering_event_detail"),text:n.qy`
        <ha-yaml-editor
          readOnly
          .hass=${this.hass}
          .defaultValue=${this._triggered}
        ></ha-yaml-editor>
      `})}},{kind:"method",key:"_renameTrigger",value:async function(){const e=await(0,x.an)(this,{title:this.hass.localize("ui.panel.config.automation.editor.triggers.change_alias"),inputLabel:this.hass.localize("ui.panel.config.automation.editor.triggers.alias"),inputType:"string",placeholder:(0,k.Z)((0,$.g)(this.trigger,this.hass,this._entityReg,!0)),defaultValue:this.trigger.alias,confirmText:this.hass.localize("ui.common.submit")});if(null!==e){const t={...this.trigger};""===e?delete t.alias:t.alias=e,(0,u.r)(this,"value-changed",{value:t}),this._yamlMode&&this._yamlEditor?.setValue(t)}}},{kind:"method",key:"expand",value:function(){this.updateComplete.then((()=>{this.shadowRoot.querySelector("ha-expansion-panel").expanded=!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[L.RF,n.AH`
        ha-button-menu {
          --mdc-theme-text-primary-on-background: var(--primary-text-color);
        }
        .disabled {
          opacity: 0.5;
          pointer-events: none;
        }
        ha-expansion-panel {
          --expansion-panel-summary-padding: 0 0 0 8px;
          --expansion-panel-content-padding: 0;
        }
        h3 {
          margin: 0;
          font-size: inherit;
          font-weight: inherit;
        }
        .trigger-icon {
          display: none;
        }
        @media (min-width: 870px) {
          .trigger-icon {
            display: inline-block;
            color: var(--secondary-text-color);
            opacity: 0.9;
            margin-right: 8px;
            margin-inline-end: 8px;
            margin-inline-start: initial;
          }
        }
        .card-content {
          padding: 16px;
        }
        .disabled-bar {
          background: var(--divider-color, #e0e0e0);
          text-align: center;
          border-top-right-radius: var(--ha-card-border-radius);
          border-top-left-radius: var(--ha-card-border-radius);
        }
        .triggered {
          cursor: pointer;
          position: absolute;
          top: 0px;
          right: 0px;
          left: 0px;
          text-transform: uppercase;
          font-weight: bold;
          font-size: 14px;
          background-color: var(--primary-color);
          color: var(--text-primary-color);
          max-height: 0px;
          overflow: hidden;
          transition: max-height 0.3s;
          text-align: center;
          border-top-right-radius: var(--ha-card-border-radius, 12px);
          border-top-left-radius: var(--ha-card-border-radius, 12px);
        }
        .triggered.active {
          max-height: 100px;
        }
        .triggered:hover {
          opacity: 0.8;
        }
        .triggered.accent {
          background-color: var(--accent-color);
          color: var(--text-accent-color, var(--text-primary-color));
        }
        mwc-list-item[disabled] {
          --mdc-theme-text-primary-on-background: var(--disabled-text-color);
        }
        mwc-list-item.hidden {
          display: none;
        }
        ha-textfield {
          display: block;
          margin-bottom: 24px;
        }
        .selected_menu_item {
          color: var(--primary-color);
        }
        li[role="separator"] {
          border-bottom-color: var(--divider-color);
        }
      `]}}]}}),n.WF);(0,a.A)([(0,o.EM)("ha-automation-trigger")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.MZ)({attribute:!1})],key:"triggers",value:void 0},{kind:"field",decorators:[(0,o.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,o.MZ)({type:Array})],key:"path",value:void 0},{kind:"field",decorators:[(0,o.wk)()],key:"_showReorder",value(){return!1}},{kind:"field",decorators:[(0,d.I)({key:"automationClipboard",state:!0,subscribe:!0,storage:"sessionStorage"})],key:"_clipboard",value:void 0},{kind:"field",key:"_focusLastTriggerOnChange",value(){return!1}},{kind:"field",key:"_triggerKeys",value(){return new WeakMap}},{kind:"field",key:"_unsubMql",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,r.A)(i,"connectedCallback",this,3)([]),this._unsubMql=(0,c.m)("(min-width: 600px)",(e=>{this._showReorder=e}))}},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.A)(i,"disconnectedCallback",this,3)([]),this._unsubMql?.(),this._unsubMql=void 0}},{kind:"get",key:"nested",value:function(){return void 0!==this.path}},{kind:"method",key:"render",value:function(){return n.qy`
      <ha-sortable
        handle-selector=".handle"
        draggable-selector="ha-automation-trigger-row"
        .disabled=${!this._showReorder||this.disabled}
        @item-moved=${this._triggerMoved}
        group="triggers"
        .path=${this.path}
        invert-swap
      >
        <div class="triggers">
          ${(0,l.u)(this.triggers,(e=>this._getKey(e)),((e,t)=>n.qy`
              <ha-automation-trigger-row
                .path=${[...this.path??[],t]}
                .index=${t}
                .first=${0===t}
                .last=${t===this.triggers.length-1}
                .trigger=${e}
                @duplicate=${this._duplicateTrigger}
                @move-down=${this._moveDown}
                @move-up=${this._moveUp}
                @value-changed=${this._triggerChanged}
                .hass=${this.hass}
                .disabled=${this.disabled}
              >
                ${this._showReorder&&!this.disabled?n.qy`
                      <div class="handle" slot="icons">
                        <ha-svg-icon .path=${"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"}></ha-svg-icon>
                      </div>
                    `:n.s6}
              </ha-automation-trigger-row>
            `))}
          <div class="buttons">
            <ha-button
              outlined
              .label=${this.hass.localize("ui.panel.config.automation.editor.triggers.add")}
              .disabled=${this.disabled}
              @click=${this._addTriggerDialog}
            >
              <ha-svg-icon .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"} slot="icon"></ha-svg-icon>
            </ha-button>
          </div>
        </div>
      </ha-sortable>
    `}},{kind:"method",key:"_addTriggerDialog",value:function(){(0,g.g)(this,{type:"trigger",add:this._addTrigger,clipboardItem:this._clipboard?.trigger?.platform})}},{kind:"field",key:"_addTrigger",value(){return e=>{let t;if(e===g.u)t=this.triggers.concat((0,s.A)(this._clipboard.trigger));else{const i=e,a=customElements.get(`ha-automation-trigger-${i}`);t=this.triggers.concat({...a.defaultConfig})}this._focusLastTriggerOnChange=!0,(0,u.r)(this,"value-changed",{value:t})}}},{kind:"method",key:"updated",value:function(e){if((0,r.A)(i,"updated",this,3)([e]),e.has("triggers")&&this._focusLastTriggerOnChange){this._focusLastTriggerOnChange=!1;const e=this.shadowRoot.querySelector("ha-automation-trigger-row:last-of-type");e.updateComplete.then((()=>{e.expand(),e.scrollIntoView(),e.focus()}))}}},{kind:"method",key:"_getKey",value:function(e){return this._triggerKeys.has(e)||this._triggerKeys.set(e,Math.random().toString()),this._triggerKeys.get(e)}},{kind:"method",key:"_moveUp",value:function(e){e.stopPropagation();const t=e.target.index,i=t-1;this._move(t,i)}},{kind:"method",key:"_moveDown",value:function(e){e.stopPropagation();const t=e.target.index,i=t+1;this._move(t,i)}},{kind:"method",key:"_move",value:function(e,t,i,a){const r=(0,h.w)(this.triggers,e,t,i,a);(0,u.r)(this,"value-changed",{value:r})}},{kind:"method",key:"_triggerMoved",value:function(e){if(this.nested)return;e.stopPropagation();const{oldIndex:t,newIndex:i,oldPath:a,newPath:r}=e.detail;this._move(t,i,a,r)}},{kind:"method",key:"_triggerChanged",value:function(e){e.stopPropagation();const t=[...this.triggers],i=e.detail.value,a=e.target.index;if(null===i)t.splice(a,1);else{const e=this._getKey(t[a]);this._triggerKeys.set(i,e),t[a]=i}(0,u.r)(this,"value-changed",{value:t})}},{kind:"method",key:"_duplicateTrigger",value:function(e){e.stopPropagation();const t=e.target.index;(0,u.r)(this,"value-changed",{value:this.triggers.concat((0,s.A)(this.triggers[t]))})}},{kind:"get",static:!0,key:"styles",value:function(){return n.AH`
      .triggers {
        padding: 16px;
        margin: -16px;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      .sortable-ghost {
        background: none;
        border-radius: var(--ha-card-border-radius, 12px);
      }
      .sortable-drag {
        background: none;
      }
      ha-automation-trigger-row {
        display: block;
        scroll-margin-top: 48px;
      }
      ha-svg-icon {
        height: 20px;
      }
      .handle {
        padding: 12px;
        cursor: move; /* fallback if grab cursor is unsupported */
        cursor: grab;
      }
      .handle ha-svg-icon {
        pointer-events: none;
        height: 24px;
      }
      .buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        order: 1;
      }
    `}}]}}),n.WF)}};
//# sourceMappingURL=UN0mk8zv.js.map