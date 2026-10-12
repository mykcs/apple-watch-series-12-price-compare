"use strict";
(function(){
const M=window.TradeInModel, U=window.TradeInUI;
const host=document.getElementById("tradein-app");
if(!host||!M||!U)return;
let state=M.fresh(),careOpen=false;
const scenes=[
{id:"pass",icon:"check-circle-2",title:"能抵 7,000",sub:"现场检查通过"},
{id:"lower",icon:"trending-down",title:"只能抵更少",sub:"店员降低报价"},
{id:"repair",icon:"wrench",title:"要收 228",sub:"先问清是什么钱"},
{id:"mail",icon:"package",title:"要寄走检查",sub:"现在还不能定价"},
{id:"reject",icon:"x-circle",title:"不能折抵",sub:"准备离店",full:true}
];
const say={
 intro:"你好，我想买一台新 iPhone，同时用我现在的 iPhone 17 Pro Max 折抵。\n我看到的预估价格大概是 7,000 港币。\n不过，我的屏幕上有一点划痕。能不能麻烦你先帮我看一下，今天到底能抵多少钱？\n我想先知道价格，再决定要不要买新手机。",
 pass:"太好了。我再确认一下：你已经看过屏幕划痕了，最后就是抵 7,000 港币，对吧？后面不会再降低价格吧？",
 lower:"那这台旧手机最后能抵多少钱？这个价格已经算上划痕了吗？后面不会再扣别的钱吧？",
 repair:"你说的 228 港币，到底是修屏幕的钱，还是直接从 7,000 里面扣？我最后究竟能抵多少钱？",
 mail:"所以今天还不能确定能抵 7,000，要寄走检查才知道，对吗？如果我今天先买新手机，之后的折抵能跟这笔新机订单放在一起吗？",
 reject:"好的，明白。那我今天先不折抵。如果还想原价买新机，我会再告诉你。",
 courier:"那我该怎么寄旧手机？是去顺丰网点，还是你们安排收件？如果最后报价变低，我可以不同意，然后把旧手机拿回来吗？",
 care:"另外，我这台旧手机还有大概 11 个月的中国大陆 AppleCare+，以前已经用它修过一次。如果我现在卖掉手机，取消 AppleCare+ 还能退多少钱？我只是想先知道金额，请先不要帮我取消。如果这里查不到，能告诉我应该联系谁吗？",
 leave:"这个价格跟我想的有点不一样，我今天先不买了，谢谢你。"
};
const fmt=U.money,esc=U.esc;
const doChange=(k,v)=>{state=M.change(state,k,v);render();};
function paymentStep(d){
 let out=U.step("下一关 · 我到底怎么付钱？",
  '<p class="subtext">先问清楚要付差价，还是先付全款。现在还没有付款。</p>'+
  U.script("那我现在是只要付差价，还是先付 11,500 港币，再把旧手机的钱退给我？","你接着念")+
  U.radio("storePay",[
   {id:"unknown",title:"店员还没说清楚"},
   {id:"offset",title:"只付差价："+fmt(d.price-d.quote+d.fee)},
   {id:"full",title:"先付全款："+fmt(d.price+d.fee)+"，之后返钱"}
  ],state.storePay),"wallet");
 if(state.storePay==="offset"){
   out+=U.script("那我今天只要付 "+(d.price-d.quote+d.fee).toLocaleString("en-HK")+" 港币，对吗？这就是最后要付的总金额，没有别的费用了吧？","确认最后付款金额",true);
 }
 if(state.storePay==="full"){
   out+=U.script("那我今天先付 "+(d.price+d.fee).toLocaleString("en-HK")+" 港币，之后的 "+d.quote.toLocaleString("en-HK")+" 港币会退回我原来付新手机的那张卡吗？大概要多久？能在订单上看到吗？","必须确认退款方式",true);
   out+='<p class="subtext">店员有没有给出明确确认？</p>'+U.radio("storeRefundVerified",[
    {id:"unknown",title:"还没说清楚"},
    {id:"yes",title:"明确确认：原支付方式返款，有订单凭证"},
    {id:"no",title:"不能确认会退回原付款方式"}],state.storeRefundVerified);
   if(state.storeRefundVerified==="no")out+=U.note("先别买","无法确认原路退款，就不要把将来的折抵款当现金。你可以选择不买。","warning");
 }
 if(d.readyShop){
   out+=U.step("最后一关 · 现在买不买？",
     U.radio("shopBuy",[
      {id:"",title:"我还没决定"},
      {id:"yes",title:"接受这个价格，买新手机"},
      {id:"no",title:"先不买，带旧手机离店"}
     ],state.shopBuy),"flag-triangle-right");
 }else{
   out+='<div class="actions">'+U.action("shopBuy","no","不买了，先离店",true)+'</div>';
 }
 return out;
}
function shopFlow(d){
 let out=U.script(say[state.route],"你现在这样说");
 if(state.route==="pass"){
   out+=U.note("已经检查过划痕","现场确认折抵 HK$7,000，就不用再问一次划痕，也不重复扣 HK$228。","good");
   if(!d.careBlocked)out+=paymentStep(d);
 }else if(state.route==="lower"){
   out+=U.slider("quote","包含划痕影响的最终报价",state.quote,0,6900,100);
   out+='<p class="subtext">如果接受这个报价，预计要补 '+fmt(d.price-state.quote)+'。划痕已经算进新报价，不再额外扣钱。</p>';
   out+=U.radio("storeAccept",[
      {id:"",title:"还在考虑"},
      {id:"yes",title:"这个价格可以，继续问付款"},
      {id:"no",title:"价格太低，我不买了"}
    ],state.storeAccept);
   if(state.storeAccept==="no")out+=U.script(say.leave,"退出时可以这样说",true);
   if(state.storeAccept==="yes"&&!d.careBlocked)out+=paymentStep(d);
 }else if(state.route==="repair"){
   out+=U.radio("repair",[
     {id:"unknown",title:"店员还没说清楚是什么钱"},
     {id:"deduct",title:"直接从 HK$7,000 扣 HK$228，最后抵 HK$6,772"},
     {id:"fee",title:"另付 HK$228 修屏幕，再确认可抵 HK$7,000"}
   ],state.repair);
   if(state.repair==="fee"){
     out+=U.script("我买的是中国大陆的 AppleCare+，在香港真的能用 228 港币维修吗？修好以后旧手机就能按 7,000 港币折抵吗？","补问这一句",true);
     out+=U.radio("repairVerified",[
       {id:"unknown",title:"维修资格或最后报价还没确定"},
       {id:"yes",title:"两件事都已明确确认"},
       {id:"no",title:"不能按这个方案维修并确认折抵"}
     ],state.repairVerified);
   }
   if(d.quote!==null){
     out+='<p class="subtext">按店员的说法，预计需补 '+fmt(d.price-d.quote+d.fee)+'。HK$228 只会计算一次。</p>';
     out+=U.radio("storeAccept",[
       {id:"",title:"还在考虑"},
       {id:"yes",title:"这个金额可以，继续问付款"},
       {id:"no",title:"不接受，今天不买"}
     ],state.storeAccept);
     if(state.storeAccept==="yes"&&!d.careBlocked)out+=paymentStep(d);
   } else if(state.repairVerified==="no"){
     out+=U.note("这个维修方案没确认成功","你可以不买，不必因为店员提到 HK$228 就先去修。","warning");
     out+='<div class="actions">'+U.action("storeAccept","no","不买了",true)+'</div>';
   }else{
     out+='<div class="actions">'+U.action("shopBuy","no","我先不买了",true)+'</div>';
   }
   if(state.storeAccept==="no"||state.shopBuy==="no")out+=U.script(say.leave,"离店话术",true);
 }
 if(d.careBlocked&&d.shop){
   out+=U.note("AppleCare+ 条件未通过","你设定了旧机保障必须有退款才能卖。金额尚未确认，这一关暂时不能点「买」。","warning");
   out+='<div class="actions">'+U.action("shopBuy","no","那就不买了",true)+'</div>';
 }
 return out;
}
function mailFlow(d){
 let out=U.script(say.mail,"你现在这样说");
 out+=U.step("下一关 · 折抵的钱会退到哪里？",
 '<p class="subtext">寄走旧机前，先问清楚：你是拿回现金，还是只收到礼品卡？</p>'+
 U.radio("mailRefund",[
   {id:"unknown",title:"店员还没说清楚"},
   {id:"cash",title:"确认会关联新机订单，退回原付款方式"},
   {id:"gift",title:"只能给 Apple Store 礼品卡"},
   {id:"unlinked",title:"不能保证与今天的新机订单关联"}
 ],state.mailRefund),"wallet");
 if(state.mailRefund==="cash"){
   out+=U.script("如果我今天先付 11,500 港币，之后旧手机验过了，折抵的钱会退回我这次付款用的银行卡，对吗？能不能给我看一下订单上怎么写？","确认是原卡退款",true);
   out+=U.step("下一关 · 店员怎么回答寄送和退回？",
     '<p class="subtext">先念下面这句话。然后分别点「怎么寄」和「能不能拒绝压价」。两件事都问清楚才考虑付款。</p>'+
     U.script(say.courier,"你照着问")+
     '<p class="subtext"><strong>问题一：旧手机怎么寄？</strong></p>'+
     U.options("courier",[
       {id:"pickup",title:"安排上门收件",sub:"按 Apple 官方邮件预约快递",icon:"package"},
       {id:"dropoff",title:"自己送到指定网点",sub:"按官方指示去指定交付点",icon:"door-open"}
     ],state.courier),"package");
   if(state.courier){
     out+='<p class="subtext"><strong>问题二：验机以后如果压价，我能拒绝并拿回旧机吗？</strong></p>';
     out+=U.options("returnAllowed",[
       {id:"yes",title:"可以拒绝并拿回旧机",sub:"请店员确认如何退回",icon:"check-circle-2"},
       {id:"no",title:"不能保证把旧机退回",sub:"风险太大，先别付款",icon:"x-circle"}
     ],state.returnAllowed);
   }
   if(state.returnAllowed==="no")out+=U.note("没有退路，不建议买","旧机能否退回来还说不清，就先停在收银台之前。","warning");
   if(d.readyMail){
     out+=U.step("下一关 · 要不要冒险先付全款？",
       U.note("买完后不能把「不接受报价」当作「新机也不买」","如果后来工厂只肯给较低的价格，你能拒绝折抵并要求退回旧机；但新机已经买了，不能自动取消购机。","warning")+
       U.radio("mailBuy",[
        {id:"",title:"我还要考虑"},
        {id:"yes",title:"愿意先付 HK$11,500 买新机，再寄旧机验机"},
        {id:"no",title:"这个风险不值得，今天不买"}
       ],state.mailBuy),"flag-triangle-right");
   }else if(d.careBlocked){
     out+=U.note("旧 AppleCare+ 还没有确定能退款","你勾选了旧保修退款作为成交条件，目前先不付款。","warning");
   }
 }else if(state.mailRefund==="gift"){
   out+=U.script("如果只能给礼品卡，那我这次买手机还是得先付全款，对吗？我不想用礼品卡，所以今天先不买。","礼品卡路线：退出",true);
 }else if(state.mailRefund==="unlinked"){
   out+=U.script("那我就没办法确定这 7,000 港币能不能退回来了。我先不付钱，麻烦帮我找一位能确认这件事的同事，好吗？","没法绑定：先退出",true);
 }else{
   out+=U.script("能帮我找一位知道邮寄折抵流程的同事吗？我想问清楚再买。","还没确认：先问",true);
 }
 if(!d.mailPurchased && state.mailBuy!=="no"){
   out+='<div class="actions">'+U.action("mailBuy","no","我不买了，保留旧机",true)+'</div>';
 }
 if(d.mailPurchased){
   out+=U.step("已经付了全款 · 工厂会怎么报价？",
     '<p class="subtext">模拟下一步：旧机送达并验收。这时新机已经买下来了。</p>'+
     U.radio("factory",[
       {id:"pending",title:"还没有验机结果"},
       {id:"approved",title:"最终折抵 HK$7,000"},
       {id:"lower",title:"工厂降低了报价"},
       {id:"rejected",title:"工厂不给可接受的报价"}
     ],state.factory),"scan-eye");
   if(state.factory==="lower"){
     out+=U.slider("factoryQuote","工厂的新报价",state.factoryQuote,0,6900,100);
     out+=U.radio("factoryAccept",[
       {id:"",title:"还没决定"},
       {id:"yes",title:"可以接受低一点的价格"},
       {id:"no",title:"太低了，拒绝折抵，让他们退回旧机"}
     ],state.factoryAccept);
     if(state.factoryAccept==="yes"){
       out+=U.script("这个价格我接受了。最后的 "+state.factoryQuote.toLocaleString("en-HK")+" 港币会退回买新机的原付款方式，对吗？","接受降低报价",true);
     }else if(state.factoryAccept==="no"){
       out+=U.script("这个价格我不能接受。请不要完成折抵，麻烦按照我们确认过的流程，把旧手机寄还给我。","拒绝降低报价",true);
     }
   }
   if(d.factoryReturned){
     out+=U.note("注意：旧机不要卖，但新机已经买了","这条路线的正确结局是「已经买新机，旧机退回来」，而不是「没有买新机」。","warning");
   }
 }
 return out;
}
function careFlow(d){
 let out='<section class="care"><button class="secondary-button" type="button" data-toggle-care="1" aria-expanded="'+careOpen+'">'+U.icon("shield-check")+' 额外一关：旧 AppleCare+ 还有没有退款？ '+U.icon("chevron-down")+'</button>';
 if(careOpen){
   out+=U.script(say.care,"问旧 AppleCare+ 的话术",true);
   out+='<p class="subtext">这跟香港折抵是两笔钱。旧机以前用过维修服务，能退多少要等原计划销售方计算。</p>';
   out+='<label class="check-row"><input type="checkbox" data-check="careGate" '+(state.careGate?'checked':'')+'> 如果旧 AppleCare+ 一分钱都退不了，我就不卖旧机</label>';
   if(state.careGate){
     out+=U.radio("careStatus",[
       {id:"unknown",title:"还不知道能退多少"},
       {id:"refundable",title:"官方已经确认能退款"},
       {id:"no",title:"已经确认不退款"}
     ],state.careStatus);
     if(state.careStatus==="refundable")out+=U.slider("careRefund","已经确认的人民币退款（仅参考，不与港币混算）",state.careRefund,0,2500,50);
   }
 }
 return out+'</section>';
}
function resultFlow(d){
 const summary=d.netCash===null?"等验机":fmt(d.netCash);
 let explanation="现在还没有成交。先问清楚条件，再决定买不买。";
 if(d.outcome==="not-buy")explanation="已选择不买：今天不用付款，旧手机仍由你保管。";
 else if(d.outcome==="bought-traded")explanation="买新机并同意了旧机的最终折抵价。把 AppleCare+ 退款单独处理。";
 else if(d.outcome==="bought-standalone")explanation="买了新机，但没有折抵旧机；这是全款购机。";
 else if(d.outcome==="bought-pending")explanation="新机已付全款，旧机还没确定值多少钱。如果不满意后来报价，你可以拒绝旧机折抵，但不能因此自动取消新机购买。";
 else if(d.outcome==="bought-return-old")explanation="旧机报价不满意，拒绝折抵、等待旧机退回。但新机已经买下，仍是全款支出。";
 if(d.overBudget)explanation+=" 这比你设定的预算还高。";
 let out='<section class="result" aria-label="当前路线结局"><h3>'+U.icon(d.purchased?"flag-triangle-right":"shield-check")+' '+esc(d.outcomeLabel)+'</h3>'+
 '<div class="metric-grid"><div><span class="metric-label">现在要付</span><b>'+fmt(d.dueNow)+'</b></div>'+
 '<div><span class="metric-label">之后现金返款</span><b>'+(d.pending?"未确定":fmt(d.refundLater))+'</b></div>'+
 '<div><span class="metric-label">最后的现金补差</span><b>'+summary+'</b></div>'+
 '<div><span class="metric-label">旧机能拿回来吗？</span><b>'+(d.factoryReturned?"已拒绝，等待退回":d.mailPurchased&&d.pending?"待验机":"按路线确认")+'</b></div></div>'+
 '<div class="explain"><strong>这条路是什么意思？</strong><p>'+esc(explanation)+'</p></div></section>';
 out+=U.slider("budget","我最多愿意补多少港币？",state.budget,3500,11500,100);
 const copyTxt="香港 iPhone 换机闯关\n门店结果："+state.route+"\n现在要付："+fmt(d.dueNow)+"\n之后返现："+(d.pending?"未确定":fmt(d.refundLater))+"\n最终补差："+summary+"\n最终结局："+d.outcomeLabel+"\n提醒："+explanation;
 const copyId=window.TradeInUI.getCopy?null:null;
 // Give the copy button a route snapshot through the delegated data-copy-summary handler.
 out+='<button type="button" class="secondary-button" data-copy-summary="1">'+U.icon("copy")+' 复制我现在走的路线</button>';
 return out;
}
function render(){
 const d=M.evaluate(state);U.startRender();
 let out=U.step("第 1 关 · 店员检查屏幕以后怎么说？",
   U.script(say.intro,"刚进店，你先这样说")+
   '<p class="subtext">听完店员的话，点一个最像他回答的选项。</p>'+
   U.options("route",scenes,state.route),"scan-eye");
 if(d.shop)out+=U.step("按这个回答继续问",shopFlow(d),"message-circle");
 if(state.route==="mail")out+=U.step("要寄走检查 · 先别付全款",mailFlow(d),"package");
 if(state.route==="reject"){
   out+=U.step("不能折抵 · 你还想买吗？",
     U.script(say.reject,"你可以这样说")+
     U.radio("standaloneBuy",[
       {id:"",title:"还在考虑"},
       {id:"no",title:"不买，带旧手机离店"},
       {id:"yes",title:"仍然原价 HK$11,500 买新机，旧机保留"}
     ],state.standaloneBuy),"x-circle");
 }
 out+=careFlow(d)+resultFlow(d);
 host.innerHTML=out;
}
host.addEventListener("click",function(ev){
 const copy=ev.target.closest("[data-copy]");
 if(copy){const t=U.getCopy(Number(copy.dataset.copy));if(t)doCopy(t,copy);return;}
 const summary=ev.target.closest("[data-copy-summary]");
 if(summary){const d=M.evaluate(state);doCopy("门店结果："+state.route+"\n现在要付："+fmt(d.dueNow)+"\n之后现金退款："+(d.pending?"待确认":fmt(d.refundLater))+"\n最终现金补差："+(d.netCash===null?"待确认":fmt(d.netCash))+"\n结局："+d.outcomeLabel,summary);return;}
 if(ev.target.closest("[data-toggle-care]")){careOpen=!careOpen;render();return;}
 const option=ev.target.closest("[data-key]");
 if(option)doChange(option.dataset.key,option.dataset.value);
});
host.addEventListener("change",function(ev){
 const t=ev.target;
 if(t.matches("[data-radio]"))doChange(t.dataset.radio,t.value);
 else if(t.matches("[data-check]"))doChange(t.dataset.check,t.checked);
 else if(t.matches("[data-range]"))doChange(t.dataset.range,Number(t.value));
});
host.addEventListener("input",function(ev){
 const t=ev.target;
 if(t.matches("[data-range]")){
   const n=host.querySelector("#amount-"+t.dataset.range);
   if(n)n.textContent=(t.dataset.range==="careRefund"?"¥":"HK$")+Number(t.value).toLocaleString("en-HK");
 }
});
document.getElementById("reset-game").addEventListener("click",function(){
 state=M.fresh();careOpen=false;render();
 window.scrollTo({top:document.querySelector(".game").getBoundingClientRect().top+window.scrollY-65,behavior:"smooth"});
});
async function doCopy(text,button){
 try{
  if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(text);
  else{
   const x=document.createElement("textarea");x.value=text;x.style.position="fixed";x.style.opacity="0";
   document.body.appendChild(x);x.select();
   if(!document.execCommand("copy"))throw Error("copy refused");
   x.remove();
  }
  const prior=button.innerHTML;button.textContent="已复制";
  window.setTimeout(function(){if(button.isConnected)button.innerHTML=prior;},1200);
 }catch(err){button.textContent="复制失败，请选中文字"; }
}
render();
})();