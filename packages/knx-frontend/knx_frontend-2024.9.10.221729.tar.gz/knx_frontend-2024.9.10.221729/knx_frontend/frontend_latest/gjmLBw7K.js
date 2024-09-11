export const id=5731;export const ids=[5731];export const modules={2872:(e,t,i)=>{i.d(t,{x:()=>a});const a=(e,t)=>e&&e.config.components.includes(t)},6412:(e,t,i)=>{i.d(t,{S:()=>d,x:()=>n});var a=i(5081);const o=(0,a.A)((e=>new Intl.Collator(e))),l=(0,a.A)((e=>new Intl.Collator(e,{sensitivity:"accent"}))),r=(e,t)=>e<t?-1:e>t?1:0,n=(e,t,i=void 0)=>Intl?.Collator?o(i).compare(e,t):r(e,t),d=(e,t,i=void 0)=>Intl?.Collator?l(i).compare(e,t):r(e.toLowerCase(),t.toLowerCase())},1355:(e,t,i)=>{i.d(t,{s:()=>a});const a=(e,t,i=!1)=>{let a;const o=(...o)=>{const l=i&&!a;clearTimeout(a),a=window.setTimeout((()=>{a=void 0,i||e(...o)}),t),l&&e(...o)};return o.cancel=()=>{clearTimeout(a)},o}},5206:(e,t,i)=>{var a=i(5461),o=i(9534),l=i(2518),r=i(8597),n=i(196),d=i(9760),s=i(9278),c=i(2506),h=i(5081),u=i(7626),p=i(3167),f=i(6412),m=i(1355);const b=(e,t)=>{const i={};for(const a of e){const e=t(a);e in i?i[e].push(a):i[e]=[a]}return i};var v=i(3799),k=i(1646),_=(i(9887),i(9222),i(2927),i(4292));let g;const x=()=>(g||(g=(0,_.LV)(new Worker(new URL(i.p+i.u(2321),i.b),{type:"module"}))),g);var y=i(5787);const w="zzzzz_undefined";(0,a.A)([(0,n.EM)("ha-data-table")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"columns",value(){return{}}},{kind:"field",decorators:[(0,n.MZ)({type:Array})],key:"data",value(){return[]}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"selectable",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"clickable",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"hasFab",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"appendRow",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"auto-height"})],key:"autoHeight",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:String})],key:"id",value(){return"id"}},{kind:"field",decorators:[(0,n.MZ)({type:String})],key:"noDataText",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:String})],key:"searchLabel",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:String})],key:"filter",value(){return""}},{kind:"field",decorators:[(0,n.MZ)()],key:"groupColumn",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"groupOrder",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"sortColumn",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"sortDirection",value(){return null}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"initialCollapsedGroups",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hiddenColumns",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"columnOrder",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_filterable",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_filter",value(){return""}},{kind:"field",decorators:[(0,n.wk)()],key:"_filteredData",value(){return[]}},{kind:"field",decorators:[(0,n.wk)()],key:"_headerHeight",value(){return 0}},{kind:"field",decorators:[(0,n.P)("slot[name='header']")],key:"_header",value:void 0},{kind:"field",decorators:[(0,n.wk)()],key:"_collapsedGroups",value(){return[]}},{kind:"field",key:"_checkableRowsCount",value:void 0},{kind:"field",key:"_checkedRows",value(){return[]}},{kind:"field",key:"_sortColumns",value(){return{}}},{kind:"field",key:"_curRequest",value(){return 0}},{kind:"field",key:"_lastUpdate",value(){return 0}},{kind:"field",decorators:[(0,u.a)(".scroller")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_debounceSearch",value(){return(0,m.s)((e=>{this._filter=e}),100,!1)}},{kind:"method",key:"clearSelection",value:function(){this._checkedRows=[],this._checkedRowsChanged()}},{kind:"method",key:"selectAll",value:function(){this._checkedRows=this._filteredData.filter((e=>!1!==e.selectable)).map((e=>e[this.id])),this._checkedRowsChanged()}},{kind:"method",key:"connectedCallback",value:function(){(0,o.A)(i,"connectedCallback",this,3)([]),this._filteredData.length&&(this._filteredData=[...this._filteredData])}},{kind:"method",key:"firstUpdated",value:function(){this.updateComplete.then((()=>this._calcTableHeight()))}},{kind:"method",key:"updated",value:function(){const e=this.renderRoot.querySelector(".mdc-data-table__header-row");e&&(e.scrollWidth>e.clientWidth?this.style.setProperty("--table-row-width",`${e.scrollWidth}px`):this.style.removeProperty("--table-row-width"))}},{kind:"method",key:"willUpdate",value:function(e){if((0,o.A)(i,"willUpdate",this,3)([e]),this.hasUpdated||(0,k.i)(),e.has("columns")){if(this._filterable=Object.values(this.columns).some((e=>e.filterable)),!this.sortColumn)for(const t in this.columns)if(this.columns[t].direction){this.sortDirection=this.columns[t].direction,this.sortColumn=t,(0,p.r)(this,"sorting-changed",{column:t,direction:this.sortDirection});break}const e=(0,l.A)(this.columns);Object.values(e).forEach((e=>{delete e.title,delete e.template,delete e.extraTemplate})),this._sortColumns=e}e.has("filter")&&this._debounceSearch(this.filter),e.has("data")&&(this._checkableRowsCount=this.data.filter((e=>!1!==e.selectable)).length),!this.hasUpdated&&this.initialCollapsedGroups?(this._collapsedGroups=this.initialCollapsedGroups,(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})):e.has("groupColumn")&&(this._collapsedGroups=[],(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})),(e.has("data")||e.has("columns")||e.has("_filter")||e.has("sortColumn")||e.has("sortDirection"))&&this._sortFilterData(),(e.has("selectable")||e.has("hiddenColumns"))&&(this._filteredData=[...this._filteredData])}},{kind:"field",key:"_sortedColumns",value(){return(0,h.A)(((e,t)=>t&&t.length?Object.keys(e).sort(((e,i)=>{const a=t.indexOf(e),o=t.indexOf(i);if(a!==o){if(-1===a)return 1;if(-1===o)return-1}return a-o})).reduce(((t,i)=>(t[i]=e[i],t)),{}):e))}},{kind:"method",key:"render",value:function(){const e=this.localizeFunc||this.hass.localize,t=this._sortedColumns(this.columns,this.columnOrder);return r.qy`
      <div class="mdc-data-table">
        <slot name="header" @slotchange=${this._calcTableHeight}>
          ${this._filterable?r.qy`
                <div class="table-header">
                  <search-input
                    .hass=${this.hass}
                    @value-changed=${this._handleSearchChange}
                    .label=${this.searchLabel}
                    .noLabelFloat=${this.noLabelFloat}
                  ></search-input>
                </div>
              `:""}
        </slot>
        <div
          class="mdc-data-table__table ${(0,d.H)({"auto-height":this.autoHeight})}"
          role="table"
          aria-rowcount=${this._filteredData.length+1}
          style=${(0,c.W)({height:this.autoHeight?53*(this._filteredData.length||1)+53+"px":`calc(100% - ${this._headerHeight}px)`})}
        >
          <div
            class="mdc-data-table__header-row"
            role="row"
            aria-rowindex="1"
            @scroll=${this._scrollContent}
          >
            <slot name="header-row">
              ${this.selectable?r.qy`
                    <div
                      class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                      role="columnheader"
                    >
                      <ha-checkbox
                        class="mdc-data-table__row-checkbox"
                        @change=${this._handleHeaderRowCheckboxClick}
                        .indeterminate=${this._checkedRows.length&&this._checkedRows.length!==this._checkableRowsCount}
                        .checked=${this._checkedRows.length&&this._checkedRows.length===this._checkableRowsCount}
                      >
                      </ha-checkbox>
                    </div>
                  `:""}
              ${Object.entries(t).map((([e,t])=>{if(t.hidden||(this.columnOrder&&this.columnOrder.includes(e)?this.hiddenColumns?.includes(e)??t.defaultHidden:t.defaultHidden))return r.s6;const i=e===this.sortColumn,a={"mdc-data-table__header-cell--numeric":"numeric"===t.type,"mdc-data-table__header-cell--icon":"icon"===t.type,"mdc-data-table__header-cell--icon-button":"icon-button"===t.type,"mdc-data-table__header-cell--overflow-menu":"overflow-menu"===t.type,"mdc-data-table__header-cell--overflow":"overflow"===t.type,sortable:Boolean(t.sortable),"not-sorted":Boolean(t.sortable&&!i)};return r.qy`
                  <div
                    aria-label=${(0,s.J)(t.label)}
                    class="mdc-data-table__header-cell ${(0,d.H)(a)}"
                    style=${(0,c.W)({minWidth:t.minWidth,maxWidth:t.maxWidth,flex:t.flex||1})}
                    role="columnheader"
                    aria-sort=${(0,s.J)(i?"desc"===this.sortDirection?"descending":"ascending":void 0)}
                    @click=${this._handleHeaderClick}
                    .columnId=${e}
                  >
                    ${t.sortable?r.qy`
                          <ha-svg-icon
                            .path=${i&&"desc"===this.sortDirection?"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z":"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"}
                          ></ha-svg-icon>
                        `:""}
                    <span>${t.title}</span>
                  </div>
                `}))}
            </slot>
          </div>
          ${this._filteredData.length?r.qy`
                <lit-virtualizer
                  scroller
                  class="mdc-data-table__content scroller ha-scrollbar"
                  @scroll=${this._saveScrollPos}
                  .items=${this._groupData(this._filteredData,e,this.appendRow,this.hasFab,this.groupColumn,this.groupOrder,this._collapsedGroups)}
                  .keyFunction=${this._keyFunction}
                  .renderItem=${(e,i)=>this._renderRow(t,this.narrow,e,i)}
                ></lit-virtualizer>
              `:r.qy`
                <div class="mdc-data-table__content">
                  <div class="mdc-data-table__row" role="row">
                    <div class="mdc-data-table__cell grows center" role="cell">
                      ${this.noDataText||e("ui.components.data-table.no-data")}
                    </div>
                  </div>
                </div>
              `}
        </div>
      </div>
    `}},{kind:"field",key:"_keyFunction",value(){return e=>e?.[this.id]||e}},{kind:"field",key:"_renderRow",value(){return(e,t,i,a)=>i?i.append?r.qy`<div class="mdc-data-table__row">${i.content}</div>`:i.empty?r.qy`<div class="mdc-data-table__row"></div>`:r.qy`
      <div
        aria-rowindex=${a+2}
        role="row"
        .rowId=${i[this.id]}
        @click=${this._handleRowClick}
        class="mdc-data-table__row ${(0,d.H)({"mdc-data-table__row--selected":this._checkedRows.includes(String(i[this.id])),clickable:this.clickable})}"
        aria-selected=${(0,s.J)(!!this._checkedRows.includes(String(i[this.id]))||void 0)}
        .selectable=${!1!==i.selectable}
      >
        ${this.selectable?r.qy`
              <div
                class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                role="cell"
              >
                <ha-checkbox
                  class="mdc-data-table__row-checkbox"
                  @change=${this._handleRowCheckboxClick}
                  .rowId=${i[this.id]}
                  .disabled=${!1===i.selectable}
                  .checked=${this._checkedRows.includes(String(i[this.id]))}
                >
                </ha-checkbox>
              </div>
            `:""}
        ${Object.entries(e).map((([a,o])=>t&&!o.main&&!o.showNarrow||o.hidden||(this.columnOrder&&this.columnOrder.includes(a)?this.hiddenColumns?.includes(a)??o.defaultHidden:o.defaultHidden)?r.s6:r.qy`
            <div
              @mouseover=${this._setTitle}
              @focus=${this._setTitle}
              role=${o.main?"rowheader":"cell"}
              class="mdc-data-table__cell ${(0,d.H)({"mdc-data-table__cell--flex":"flex"===o.type,"mdc-data-table__cell--numeric":"numeric"===o.type,"mdc-data-table__cell--icon":"icon"===o.type,"mdc-data-table__cell--icon-button":"icon-button"===o.type,"mdc-data-table__cell--overflow-menu":"overflow-menu"===o.type,"mdc-data-table__cell--overflow":"overflow"===o.type,forceLTR:Boolean(o.forceLTR)})}"
              style=${(0,c.W)({minWidth:o.minWidth,maxWidth:o.maxWidth,flex:o.flex||1})}
            >
              ${o.template?o.template(i):t&&o.main?r.qy`<div class="primary">${i[a]}</div>
                      <div class="secondary">
                        ${Object.entries(e).filter((([e,t])=>!(t.hidden||t.main||t.showNarrow||(this.columnOrder&&this.columnOrder.includes(e)?this.hiddenColumns?.includes(e)??t.defaultHidden:t.defaultHidden)))).map((([e,t],a)=>r.qy`${0!==a?" ⸱ ":r.s6}${t.template?t.template(i):i[e]}`))}
                      </div>
                      ${o.extraTemplate?o.extraTemplate(i):r.s6}`:r.qy`${i[a]}${o.extraTemplate?o.extraTemplate(i):r.s6}`}
            </div>
          `))}
      </div>
    `:r.s6}},{kind:"method",key:"_sortFilterData",value:async function(){const e=(new Date).getTime(),t=e-this._lastUpdate,i=e-this._curRequest;this._curRequest=e;const a=!this._lastUpdate||t>500&&i<500;let o=this.data;if(this._filter&&(o=await this._memFilterData(this.data,this._sortColumns,this._filter.trim())),!a&&this._curRequest!==e)return;const l=this.sortColumn?((e,t,i,a,o)=>x().sortData(e,t,i,a,o))(o,this._sortColumns[this.sortColumn],this.sortDirection,this.sortColumn,this.hass.locale.language):o,[r]=await Promise.all([l,y.E]),n=(new Date).getTime()-e;n<100&&await new Promise((e=>{setTimeout(e,100-n)})),(a||this._curRequest===e)&&(this._lastUpdate=e,this._filteredData=r)}},{kind:"field",key:"_groupData",value(){return(0,h.A)(((e,t,i,a,o,l,n)=>{if(i||a||o){let d=[...e];if(o){const e=b(d,(e=>e[o]));e.undefined&&(e[w]=e.undefined,delete e.undefined);const i=Object.keys(e).sort(((e,t)=>{const i=l?.indexOf(e)??-1,a=l?.indexOf(t)??-1;return i!==a?-1===i?1:-1===a?-1:i-a:(0,f.x)(["","-","—"].includes(e)?"zzz":e,["","-","—"].includes(t)?"zzz":t,this.hass.locale.language)})).reduce(((t,i)=>(t[i]=e[i],t)),{}),a=[];Object.entries(i).forEach((([e,i])=>{a.push({append:!0,content:r.qy`<div
                class="mdc-data-table__cell group-header"
                role="cell"
                .group=${e}
                @click=${this._collapseGroup}
              >
                <ha-icon-button
                  .path=${"M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"}
                  class=${n.includes(e)?"collapsed":""}
                >
                </ha-icon-button>
                ${e===w?t("ui.components.data-table.ungrouped"):e||""}
              </div>`}),n.includes(e)||a.push(...i)})),d=a}return i&&d.push({append:!0,content:i}),a&&d.push({empty:!0}),d}return e}))}},{kind:"field",key:"_memFilterData",value(){return(0,h.A)(((e,t,i)=>((e,t,i)=>x().filterData(e,t,i))(e,t,i)))}},{kind:"method",key:"_handleHeaderClick",value:function(e){const t=e.currentTarget.columnId;this.columns[t].sortable&&(this.sortDirection&&this.sortColumn===t?"asc"===this.sortDirection?this.sortDirection="desc":this.sortDirection=null:this.sortDirection="asc",this.sortColumn=null===this.sortDirection?void 0:t,(0,p.r)(this,"sorting-changed",{column:t,direction:this.sortDirection}))}},{kind:"method",key:"_handleHeaderRowCheckboxClick",value:function(e){e.target.checked?this.selectAll():(this._checkedRows=[],this._checkedRowsChanged())}},{kind:"field",key:"_handleRowCheckboxClick",value(){return e=>{const t=e.currentTarget,i=t.rowId;if(t.checked){if(this._checkedRows.includes(i))return;this._checkedRows=[...this._checkedRows,i]}else this._checkedRows=this._checkedRows.filter((e=>e!==i));this._checkedRowsChanged()}}},{kind:"field",key:"_handleRowClick",value(){return e=>{if(e.composedPath().find((e=>["ha-checkbox","mwc-button","ha-button","ha-icon-button","ha-assist-chip"].includes(e.localName))))return;const t=e.currentTarget.rowId;(0,p.r)(this,"row-click",{id:t},{bubbles:!1})}}},{kind:"method",key:"_setTitle",value:function(e){const t=e.currentTarget;t.scrollWidth>t.offsetWidth&&t.setAttribute("title",t.innerText)}},{kind:"method",key:"_checkedRowsChanged",value:function(){this._filteredData.length&&(this._filteredData=[...this._filteredData]),(0,p.r)(this,"selection-changed",{value:this._checkedRows})}},{kind:"method",key:"_handleSearchChange",value:function(e){this.filter||this._debounceSearch(e.detail.value)}},{kind:"method",key:"_calcTableHeight",value:async function(){this.autoHeight||(await this.updateComplete,this._headerHeight=this._header.clientHeight)}},{kind:"method",decorators:[(0,n.Ls)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop,this.renderRoot.querySelector(".mdc-data-table__header-row").scrollLeft=e.target.scrollLeft}},{kind:"method",decorators:[(0,n.Ls)({passive:!0})],key:"_scrollContent",value:function(e){this.renderRoot.querySelector("lit-virtualizer").scrollLeft=e.target.scrollLeft}},{kind:"field",key:"_collapseGroup",value(){return e=>{const t=e.currentTarget.group;this._collapsedGroups.includes(t)?this._collapsedGroups=this._collapsedGroups.filter((e=>e!==t)):this._collapsedGroups=[...this._collapsedGroups,t],(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})}}},{kind:"method",key:"expandAllGroups",value:function(){this._collapsedGroups=[],(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})}},{kind:"method",key:"collapseAllGroups",value:function(){if(!this.groupColumn||!this.data.some((e=>e[this.groupColumn])))return;const e=b(this.data,(e=>e[this.groupColumn]));e.undefined&&(e[w]=e.undefined,delete e.undefined),this._collapsedGroups=Object.keys(e),(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})}},{kind:"get",static:!0,key:"styles",value:function(){return[v.dp,r.AH`
        /* default mdc styles, colors changed, without checkbox styles */
        :host {
          height: 100%;
        }
        .mdc-data-table__content {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table {
          background-color: var(--data-table-background-color);
          border-radius: 4px;
          border-width: 1px;
          border-style: solid;
          border-color: var(--divider-color);
          display: inline-flex;
          flex-direction: column;
          box-sizing: border-box;
          overflow: hidden;
        }

        .mdc-data-table__row--selected {
          background-color: rgba(var(--rgb-primary-color), 0.04);
        }

        .mdc-data-table__row {
          display: flex;
          height: var(--data-table-row-height, 52px);
          width: var(--table-row-width, 100%);
        }

        .mdc-data-table__row ~ .mdc-data-table__row {
          border-top: 1px solid var(--divider-color);
        }

        .mdc-data-table__row.clickable:not(
            .mdc-data-table__row--selected
          ):hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .mdc-data-table__header-cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__header-row {
          height: 56px;
          display: flex;
          border-bottom: 1px solid var(--divider-color);
          overflow: auto;
        }

        /* Hide scrollbar for Chrome, Safari and Opera */
        .mdc-data-table__header-row::-webkit-scrollbar {
          display: none;
        }

        /* Hide scrollbar for IE, Edge and Firefox */
        .mdc-data-table__header-row {
          -ms-overflow-style: none; /* IE and Edge */
          scrollbar-width: none; /* Firefox */
        }

        .mdc-data-table__cell,
        .mdc-data-table__header-cell {
          padding-right: 16px;
          padding-left: 16px;
          min-width: 150px;
          align-self: center;
          overflow: hidden;
          text-overflow: ellipsis;
          flex-shrink: 0;
          box-sizing: border-box;
        }

        .mdc-data-table__cell.mdc-data-table__cell--flex {
          display: flex;
          overflow: initial;
        }

        .mdc-data-table__cell.mdc-data-table__cell--icon {
          overflow: initial;
        }

        .mdc-data-table__header-cell--checkbox,
        .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 16px;
          /* @noflip */
          padding-right: 0;
          /* @noflip */
          padding-inline-start: 16px;
          /* @noflip */
          padding-inline-end: initial;
          width: 60px;
        }

        .mdc-data-table__table {
          height: 100%;
          width: 100%;
          border: 0;
          white-space: nowrap;
          position: relative;
        }

        .mdc-data-table__cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.25rem;
          font-weight: 400;
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
          flex-grow: 0;
          flex-shrink: 0;
        }

        .mdc-data-table__cell a {
          color: inherit;
          text-decoration: none;
        }

        .mdc-data-table__cell--numeric {
          text-align: var(--float-end);
        }

        .mdc-data-table__cell--icon {
          color: var(--secondary-text-color);
          text-align: center;
        }

        .mdc-data-table__header-cell--icon,
        .mdc-data-table__cell--icon {
          min-width: 64px;
          flex: 0 0 64px !important;
        }

        .mdc-data-table__cell--icon img {
          width: 24px;
          height: 24px;
        }

        .mdc-data-table__header-cell.mdc-data-table__header-cell--icon {
          text-align: center;
        }

        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(
            .not-sorted
          ) {
          text-align: var(--float-start);
        }

        .mdc-data-table__cell--icon:first-child img,
        .mdc-data-table__cell--icon:first-child ha-icon,
        .mdc-data-table__cell--icon:first-child ha-svg-icon,
        .mdc-data-table__cell--icon:first-child ha-state-icon,
        .mdc-data-table__cell--icon:first-child ha-domain-icon,
        .mdc-data-table__cell--icon:first-child ha-service-icon {
          margin-left: 8px;
          margin-inline-start: 8px;
          margin-inline-end: initial;
        }

        .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: -8px;
          margin-inline-end: -8px;
          margin-inline-start: initial;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          min-width: 64px;
          flex: 0 0 64px !important;
          padding: 8px;
        }

        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          min-width: 56px;
          width: 56px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--icon-button {
          color: var(--secondary-text-color);
          text-overflow: clip;
        }

        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          width: 64px;
        }

        .mdc-data-table__cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child {
          padding-left: 16px;
          padding-inline-start: 16px;
          padding-inline-end: initial;
        }

        .mdc-data-table__cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          padding-right: 16px;
          padding-inline-end: 16px;
          padding-inline-start: initial;
        }
        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--overflow,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--overflow {
          overflow: initial;
        }
        .mdc-data-table__cell--icon-button a {
          color: var(--secondary-text-color);
        }

        .mdc-data-table__header-cell {
          font-family: Roboto, sans-serif;
          -moz-osx-font-smoothing: grayscale;
          -webkit-font-smoothing: antialiased;
          font-size: 0.875rem;
          line-height: 1.375rem;
          font-weight: 500;
          letter-spacing: 0.0071428571em;
          text-decoration: inherit;
          text-transform: inherit;
          text-align: var(--float-start);
        }

        .mdc-data-table__header-cell--numeric {
          text-align: var(--float-end);
        }
        .mdc-data-table__header-cell--numeric.sortable:hover,
        .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: var(--float-start);
        }

        /* custom from here */

        .group-header {
          padding-top: 12px;
          padding-left: 12px;
          padding-inline-start: 12px;
          padding-inline-end: initial;
          width: 100%;
          font-weight: 500;
          display: flex;
          align-items: center;
          cursor: pointer;
        }

        .group-header ha-icon-button {
          transition: transform 0.2s ease;
        }

        .group-header ha-icon-button.collapsed {
          transform: rotate(180deg);
        }

        :host {
          display: block;
        }

        .mdc-data-table {
          display: block;
          border-width: var(--data-table-border-width, 1px);
          height: 100%;
        }
        .mdc-data-table__header-cell {
          overflow: hidden;
          position: relative;
        }
        .mdc-data-table__header-cell span {
          position: relative;
          left: 0px;
          inset-inline-start: 0px;
          inset-inline-end: initial;
        }

        .mdc-data-table__header-cell.sortable {
          cursor: pointer;
        }
        .mdc-data-table__header-cell > * {
          transition: var(--float-start) 0.2s ease;
        }
        .mdc-data-table__header-cell ha-svg-icon {
          top: -3px;
          position: absolute;
        }
        .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          left: -20px;
          inset-inline-start: -20px;
          inset-inline-end: initial;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) span,
        .mdc-data-table__header-cell.sortable.not-sorted:hover span {
          left: 24px;
          inset-inline-start: 24px;
          inset-inline-end: initial;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) ha-svg-icon,
        .mdc-data-table__header-cell.sortable:hover.not-sorted ha-svg-icon {
          left: 12px;
          inset-inline-start: 12px;
          inset-inline-end: initial;
        }
        .table-header {
          border-bottom: 1px solid var(--divider-color);
        }
        search-input {
          display: block;
          flex: 1;
          --mdc-text-field-fill-color: var(--sidebar-background-color);
          --mdc-text-field-idle-line-color: transparent;
        }
        slot[name="header"] {
          display: block;
        }
        .center {
          text-align: center;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        .scroller {
          height: calc(100% - 57px);
          overflow: overlay !important;
        }

        .mdc-data-table__table.auto-height .scroller {
          overflow-y: hidden !important;
        }
        .grows {
          flex-grow: 1;
          flex-shrink: 1;
        }
        .forceLTR {
          direction: ltr;
        }
        .clickable {
          cursor: pointer;
        }
        lit-virtualizer {
          contain: size layout !important;
          overscroll-behavior: contain;
        }
      `]}}]}}),r.WF)},9887:(e,t,i)=>{var a=i(5461),o=i(1497),l=i(8678),r=i(8597),n=i(196);(0,a.A)([(0,n.EM)("ha-checkbox")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[l.R,r.AH`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `]}}]}}),o.L)},3279:(e,t,i)=>{var a=i(5461),o=i(9534),l=i(7305),r=i(8597),n=i(196);(0,a.A)([(0,n.EM)("ha-circular-progress")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:"aria-label",type:String})],key:"ariaLabel",value(){return"Loading"}},{kind:"field",decorators:[(0,n.MZ)()],key:"size",value(){return"medium"}},{kind:"method",key:"updated",value:function(e){if((0,o.A)(i,"updated",this,3)([e]),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"field",static:!0,key:"styles",value(){return[...(0,o.A)(i,"styles",this),r.AH`
      :host {
        --md-sys-color-primary: var(--primary-color);
        --md-circular-progress-size: 48px;
      }
    `]}}]}}),l.U)},9373:(e,t,i)=>{var a=i(5461),o=i(9534),l=i(4400),r=i(5050),n=i(8597),d=i(196),s=i(10);(0,a.A)([(0,d.EM)("ha-textfield")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"invalid",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"icon",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)({type:Boolean})],key:"iconTrailing",value(){return!1}},{kind:"field",decorators:[(0,d.MZ)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,d.MZ)()],key:"autocorrect",value:void 0},{kind:"field",decorators:[(0,d.MZ)({attribute:"input-spellcheck"})],key:"inputSpellcheck",value:void 0},{kind:"field",decorators:[(0,d.P)("input")],key:"formElement",value:void 0},{kind:"method",key:"updated",value:function(e){(0,o.A)(i,"updated",this,3)([e]),(e.has("invalid")&&(this.invalid||void 0!==e.get("invalid"))||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||"Invalid":""),this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(this.autocorrect?this.formElement.setAttribute("autocorrect",this.autocorrect):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}},{kind:"method",key:"renderIcon",value:function(e,t=!1){const i=t?"trailing":"leading";return n.qy`
      <span
        class="mdc-text-field__icon mdc-text-field__icon--${i}"
        tabindex=${t?1:-1}
      >
        <slot name="${i}Icon"></slot>
      </span>
    `}},{kind:"field",static:!0,key:"styles",value(){return[r.R,n.AH`
      .mdc-text-field__input {
        width: var(--ha-textfield-input-width, 100%);
      }
      .mdc-text-field:not(.mdc-text-field--with-leading-icon) {
        padding: var(--text-field-padding, 0px 16px);
      }
      .mdc-text-field__affix--suffix {
        padding-left: var(--text-field-suffix-padding-left, 12px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 12px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
        direction: ltr;
      }
      .mdc-text-field--with-leading-icon {
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 16px);
        direction: var(--direction);
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon {
        padding-left: var(--text-field-suffix-padding-left, 0px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
      }
      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--suffix {
        color: var(--secondary-text-color);
      }

      .mdc-text-field__icon {
        color: var(--secondary-text-color);
      }

      .mdc-text-field__icon--leading {
        margin-inline-start: 16px;
        margin-inline-end: 8px;
        direction: var(--direction);
      }

      .mdc-text-field__icon--trailing {
        padding: var(--textfield-icon-trailing-padding, 12px);
      }

      .mdc-floating-label:not(.mdc-floating-label--float-above) {
        text-overflow: ellipsis;
        width: inherit;
        padding-right: 30px;
        padding-inline-end: 30px;
        padding-inline-start: initial;
        box-sizing: border-box;
        direction: var(--direction);
      }

      input {
        text-align: var(--text-field-text-align, start);
      }

      /* Edge, hide reveal password icon */
      ::-ms-reveal {
        display: none;
      }

      /* Chrome, Safari, Edge, Opera */
      :host([no-spinner]) input::-webkit-outer-spin-button,
      :host([no-spinner]) input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }

      /* Firefox */
      :host([no-spinner]) input[type="number"] {
        -moz-appearance: textfield;
      }

      .mdc-text-field__ripple {
        overflow: hidden;
      }

      .mdc-text-field {
        overflow: var(--text-field-overflow);
      }

      .mdc-floating-label {
        inset-inline-start: 16px !important;
        inset-inline-end: initial !important;
        transform-origin: var(--float-start);
        direction: var(--direction);
        text-align: var(--float-start);
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--filled
        .mdc-floating-label {
        max-width: calc(
          100% - 48px - var(--text-field-suffix-padding-left, 0px)
        );
        inset-inline-start: calc(
          48px + var(--text-field-suffix-padding-left, 0px)
        ) !important;
        inset-inline-end: initial !important;
        direction: var(--direction);
      }

      .mdc-text-field__input[type="number"] {
        direction: var(--direction);
      }
      .mdc-text-field__affix--prefix {
        padding-right: var(--text-field-prefix-padding-right, 2px);
        padding-inline-end: var(--text-field-prefix-padding-right, 2px);
        padding-inline-start: initial;
      }

      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--prefix {
        color: var(--mdc-text-field-label-ink-color);
      }
    `,"rtl"===s.G.document.dir?n.AH`
          .mdc-text-field--with-leading-icon,
          .mdc-text-field__icon--leading,
          .mdc-floating-label,
          .mdc-text-field--with-leading-icon.mdc-text-field--filled
            .mdc-floating-label,
          .mdc-text-field__input[type="number"] {
            direction: rtl;
            --direction: rtl;
          }
        `:n.AH``]}}]}}),l.J)},2927:(e,t,i)=>{var a=i(5461),o=i(8597),l=i(196),r=(i(6396),i(9222),i(9373),i(3167));(0,a.A)([(0,l.EM)("search-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)()],key:"filter",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"suffix",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:String})],key:"label",value:void 0},{kind:"method",key:"focus",value:function(){this._input?.focus()}},{kind:"field",decorators:[(0,l.P)("ha-textfield",!0)],key:"_input",value:void 0},{kind:"method",key:"render",value:function(){return o.qy`
      <ha-textfield
        .autofocus=${this.autofocus}
        .label=${this.label||this.hass.localize("ui.common.search")}
        .value=${this.filter||""}
        icon
        .iconTrailing=${this.filter||this.suffix}
        @input=${this._filterInputChanged}
      >
        <slot name="prefix" slot="leadingIcon">
          <ha-svg-icon
            tabindex="-1"
            class="prefix"
            .path=${"M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z"}
          ></ha-svg-icon>
        </slot>
        <div class="trailing" slot="trailingIcon">
          ${this.filter&&o.qy`
            <ha-icon-button
              @click=${this._clearSearch}
              .label=${this.hass.localize("ui.common.clear")}
              .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              class="clear-button"
            ></ha-icon-button>
          `}
          <slot name="suffix"></slot>
        </div>
      </ha-textfield>
    `}},{kind:"method",key:"_filterChanged",value:async function(e){(0,r.r)(this,"value-changed",{value:String(e)})}},{kind:"method",key:"_filterInputChanged",value:async function(e){this._filterChanged(e.target.value)}},{kind:"method",key:"_clearSearch",value:async function(){this._filterChanged("")}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        display: inline-flex;
      }
      ha-svg-icon,
      ha-icon-button {
        color: var(--primary-text-color);
      }
      ha-svg-icon {
        outline: none;
      }
      .clear-button {
        --mdc-icon-size: 20px;
      }
      ha-textfield {
        display: inherit;
      }
      .trailing {
        display: flex;
        align-items: center;
      }
    `}}]}}),o.WF)},1424:(e,t,i)=>{i.r(t);var a=i(5461),o=i(8597),l=i(196),r=(i(3279),i(2312),i(2010),i(3799));(0,a.A)([(0,l.EM)("hass-loading-screen")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.MZ)({type:Boolean,attribute:"no-toolbar"})],key:"noToolbar",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"rootnav",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,l.MZ)()],key:"message",value:void 0},{kind:"method",key:"render",value:function(){return o.qy`
      ${this.noToolbar?"":o.qy`<div class="toolbar">
            ${this.rootnav||history.state?.root?o.qy`
                  <ha-menu-button
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                `:o.qy`
                  <ha-icon-button-arrow-prev
                    .hass=${this.hass}
                    @click=${this._handleBack}
                  ></ha-icon-button-arrow-prev>
                `}
          </div>`}
      <div class="content">
        <ha-circular-progress indeterminate></ha-circular-progress>
        ${this.message?o.qy`<div id="loading-text">${this.message}</div>`:o.s6}
      </div>
    `}},{kind:"method",key:"_handleBack",value:function(){history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[r.RF,o.AH`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }
        .toolbar {
          display: flex;
          align-items: center;
          font-size: 20px;
          height: var(--header-height);
          padding: 8px 12px;
          pointer-events: none;
          background-color: var(--app-header-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar {
            padding: 4px;
          }
        }
        ha-menu-button,
        ha-icon-button-arrow-prev {
          pointer-events: auto;
        }
        .content {
          height: calc(100% - var(--header-height));
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        #loading-text {
          max-width: 350px;
          margin-top: 16px;
        }
      `]}}]}}),o.WF)},7341:(e,t,i)=>{var a=i(5461),o=i(9534),l=i(8597),r=i(196),n=i(9760),d=i(5081),s=i(7626),c=(i(2312),i(2010),i(9222),i(9278)),h=i(2431),u=i(7515);(0,a.A)([(0,r.EM)("ha-ripple")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:"attachableTouchController",value(){return new h.i(this,this.onTouchControlChange.bind(this))}},{kind:"method",key:"attach",value:function(e){(0,o.A)(i,"attach",this,3)([e]),this.attachableTouchController.attach(e)}},{kind:"method",key:"detach",value:function(){(0,o.A)(i,"detach",this,3)([]),this.attachableTouchController.detach()}},{kind:"field",key:"_handleTouchEnd",value(){return()=>{this.disabled||(0,o.A)(i,"endPressAnimation",this,3)([])}}},{kind:"method",key:"onTouchControlChange",value:function(e,t){e?.removeEventListener("touchend",this._handleTouchEnd),t?.addEventListener("touchend",this._handleTouchEnd)}},{kind:"field",static:!0,key:"styles",value(){return[...(0,o.A)(i,"styles",this),l.AH`
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
    `]}}]}}),u.o),(0,a.A)([(0,r.EM)("ha-tab")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"active",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)()],key:"name",value:void 0},{kind:"method",key:"render",value:function(){return l.qy`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${(0,c.J)(this.name)}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?l.qy`<slot name="icon"></slot>`:""}
        <span class="name">${this.name}</span>
        <ha-ripple></ha-ripple>
      </div>
    `}},{kind:"method",key:"_handleKeyDown",value:function(e){"Enter"===e.key&&e.target.click()}},{kind:"get",static:!0,key:"styles",value:function(){return l.AH`
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
    `}}]}}),l.WF);var p=i(3799),f=i(6041),m=i(2872);const b=(e,t)=>!t.component||(0,f.e)(t.component).some((t=>(0,m.x)(e,t))),v=(e,t)=>!t.not_component||!(0,f.e)(t.not_component).some((t=>(0,m.x)(e,t))),k=e=>e.core,_=(e,t)=>(e=>e.advancedOnly)(t)&&!(e=>e.userData?.showAdvanced)(e);(0,a.A)([(0,r.EM)("hass-tabs-subpage")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"supervisor",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,attribute:"main-page"})],key:"mainPage",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0,attribute:"is-wide"})],key:"isWide",value(){return!1}},{kind:"field",decorators:[(0,r.MZ)({type:Boolean})],key:"pane",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_activeTab",value:void 0},{kind:"field",decorators:[(0,s.a)(".content")],key:"_savedScrollPos",value:void 0},{kind:"field",key:"_getTabs",value(){return(0,d.A)(((e,t,i,a,o,r)=>{const n=e.filter((e=>((e,t)=>(k(t)||b(e,t))&&!_(e,t)&&v(e,t))(this.hass,e)));if(n.length<2){if(1===n.length){const e=n[0];return[e.translationKey?r(e.translationKey):e.name]}return[""]}return n.map((e=>l.qy`
          <a href=${e.path}>
            <ha-tab
              .hass=${this.hass}
              .active=${e.path===t?.path}
              .narrow=${this.narrow}
              .name=${e.translationKey?r(e.translationKey):e.name}
            >
              ${e.iconPath?l.qy`<ha-svg-icon
                    slot="icon"
                    .path=${e.iconPath}
                  ></ha-svg-icon>`:""}
            </ha-tab>
          </a>
        `))}))}},{kind:"method",key:"willUpdate",value:function(e){e.has("route")&&(this._activeTab=this.tabs.find((e=>`${this.route.prefix}${this.route.path}`.includes(e.path)))),(0,o.A)(i,"willUpdate",this,3)([e])}},{kind:"method",key:"render",value:function(){const e=this._getTabs(this.tabs,this._activeTab,this.hass.config.components,this.hass.language,this.narrow,this.localizeFunc||this.hass.localize),t=e.length>1;return l.qy`
      <div class="toolbar">
        <slot name="toolbar">
          <div class="toolbar-content">
            ${this.mainPage||!this.backPath&&history.state?.root?l.qy`
                  <ha-menu-button
                    .hassio=${this.supervisor}
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                `:this.backPath?l.qy`
                    <a href=${this.backPath}>
                      <ha-icon-button-arrow-prev
                        .hass=${this.hass}
                      ></ha-icon-button-arrow-prev>
                    </a>
                  `:l.qy`
                    <ha-icon-button-arrow-prev
                      .hass=${this.hass}
                      @click=${this._backTapped}
                    ></ha-icon-button-arrow-prev>
                  `}
            ${this.narrow||!t?l.qy`<div class="main-title">
                  <slot name="header">${t?"":e[0]}</slot>
                </div>`:""}
            ${t&&!this.narrow?l.qy`<div id="tabbar">${e}</div>`:""}
            <div id="toolbar-icon">
              <slot name="toolbar-icon"></slot>
            </div>
          </div>
        </slot>
        ${t&&this.narrow?l.qy`<div id="tabbar" class="bottom-bar">${e}</div>`:""}
      </div>
      <div class="container">
        ${this.pane?l.qy`<div class="pane">
              <div class="shadow-container"></div>
              <div class="ha-scrollbar">
                <slot name="pane"></slot>
              </div>
            </div>`:l.s6}
        <div
          class="content ha-scrollbar ${(0,n.H)({tabs:t})}"
          @scroll=${this._saveScrollPos}
        >
          <slot></slot>
        </div>
      </div>
      <div id="fab" class=${(0,n.H)({tabs:t})}>
        <slot name="fab"></slot>
      </div>
    `}},{kind:"method",decorators:[(0,r.Ls)({passive:!0})],key:"_saveScrollPos",value:function(e){this._savedScrollPos=e.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[p.dp,l.AH`
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
      `]}}]}}),l.WF)},1646:(e,t,i)=>{i.d(t,{i:()=>a});const a=async()=>{await i.e(3331).then(i.bind(i,3331))}}};
//# sourceMappingURL=gjmLBw7K.js.map