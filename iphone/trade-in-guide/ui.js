"use strict";
(function(){
const icons={
 "check-circle-2":'<circle cx="12" cy="12" r="10"/><path d="m8.5 12 2.3 2.3 4.7-4.8"/>',
 "trending-down":'<path d="m22 17-8-8-4 4-8-8"/><path d="M16 17h6v-6"/>',
 "wrench":'<path d="M14.7 6.3a6 6 0 0 0-7.4 7.4l-5.1 5.1a2 2 0 0 0 2.9 2.9l5.1-5.1a6 6 0 0 0 7.4-7.4L14 13l-4-3z"/>',
 "package":'<path d="m12 2 9 5-9 5-9-5z"/><path d="M3 7v10l9 5 9-5V7M12 12v10"/>',
 "x-circle":'<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6m0-6 6 6"/>',
 "message-circle":'<path d="M7.5 19.5a9 9 0 1 1 5 1.4 9 9 0 0 1-3.3-.6L3 22z"/>',
 "copy":'<rect x="8" y="8" width="13" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>',
 "alert-triangle":'<path d="m10.3 3.8-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3.2l-8-14a2 2 0 0 0-3.4 0z"/><path d="M12 9v4m0 4h.01"/>',
 "check":'<path d="m20 6-11 11-5-5"/>',
 "shield-check":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "scan-eye":'<path d="M4 4h4M4 4v4M20 4h-4m4 0v4M4 20h4m-4 0v-4m16 4h-4m4 0v-4"/><path d="M2 12s4-4 10-4 10 4 10 4-4 4-10 4-10-4-10-4z"/><circle cx="12" cy="12" r="2"/>',
 "wallet":'<rect x="2" y="5" width="20" height="15" rx="2"/><path d="M16 14h6M5 5V3h15"/>',
 "door-open":'<path d="M13 3h7v18h-7M13 3 5 5v14l8 2z"/><path d="M10 12h.01"/>',
 "lock":'<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 "chevron-down":'<path d="m6 9 6 6 6-6"/>',
 "arrow-right":'<path d="M5 12h14m-6-6 6 6-6 6"/>',
 "flag-triangle-right":'<path d="M4 22V4m0 0h16l-5 6 5 6H4"/>'
};
let copies=[];
function icon(name){return '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">'+(icons[name]||icons["check"])+'</svg>';}
function esc(t){return String(t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}
function startRender(){copies=[];}
function script(text,label,small){
 const n=copies.push(text)-1;
 return '<div class="script'+(small?' secondary':'')+'"><div class="script-heading"><span>'+icon("message-circle")+' '+esc(label||"你接着念")+'</span><button class="copy-button" type="button" data-copy="'+n+'">'+icon("copy")+' 复制</button></div><blockquote>“'+esc(text)+'”</blockquote></div>';
}
function options(key,items,value){
 return '<div class="option-grid">'+items.map(function(item){
  return '<button type="button" class="option-card'+(item.full?' full':'')+'" aria-pressed="'+(value===item.id)+'" data-key="'+key+'" data-value="'+item.id+'"><span class="option-top">'+icon(item.icon||"check-circle-2")+(value===item.id?icon("check"):"")+'</span><span class="option-title">'+esc(item.title)+'</span><small>'+esc(item.sub||"")+'</small></button>';
 }).join("")+'</div>';
}
function radio(key,items,value){
 return '<div class="radio-list" role="group">'+items.map(function(item){
 return '<label class="radio-option"><input type="radio" name="'+esc(key)+'" data-radio="'+key+'" value="'+esc(item.id)+'" '+(value===item.id?"checked":"")+'><span>'+esc(item.title)+(item.sub?'<small>'+esc(item.sub)+'</small>':'')+'</span></label>';
 }).join("")+'</div>';
}
function slider(key,text,value,min,max,step){
 return '<div class="range-box"><div class="range-line"><span>'+esc(text)+'</span><b id="amount-'+key+'">HK$'+Number(value).toLocaleString("en-HK")+'</b></div><input type="range" data-range="'+key+'" min="'+min+'" max="'+max+'" step="'+step+'" value="'+value+'" aria-label="'+esc(text)+'"></div>';
}
function note(title,body,kind){
 return '<div class="notice'+(kind?' '+kind:'')+'"><strong>'+esc(title)+'</strong><p>'+esc(body)+'</p></div>';
}
function step(title,body,ico){
 return '<section class="step-panel"><h3 class="step-title">'+icon(ico||"check-circle-2")+esc(title)+'</h3>'+body+'</section>';
}
function action(key,value,title,secondary){
 return '<button type="button" class="action'+(secondary?' alt':'')+'" data-key="'+key+'" data-value="'+value+'">'+esc(title)+(secondary?'':icon("arrow-right"))+'</button>';
}
function money(n){return 'HK$'+Number(n).toLocaleString("en-HK");}
function getCopy(index){return copies[index];}
window.TradeInUI={icon,esc,startRender,script,options,radio,slider,note,step,action,money,getCopy};
})();