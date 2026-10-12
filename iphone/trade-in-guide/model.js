"use strict";
(function(){
const base={route:"",quote:6500,storeAccept:"",repair:"unknown",repairVerified:"unknown",storePay:"unknown",storeRefundVerified:"unknown",shopBuy:"",mailRefund:"unknown",courier:"",returnAllowed:"",mailBuy:"",factory:"pending",factoryQuote:6500,factoryAccept:"",standaloneBuy:"",careGate:false,careStatus:"unknown",careRefund:500,budget:5000};
const reset={route:["quote","storeAccept","repair","repairVerified","storePay","storeRefundVerified","shopBuy","mailRefund","courier","returnAllowed","mailBuy","factory","factoryQuote","factoryAccept","standaloneBuy"],quote:["storeAccept","storePay","storeRefundVerified","shopBuy"],storeAccept:["storePay","storeRefundVerified","shopBuy"],repair:["repairVerified","storeAccept","storePay","storeRefundVerified","shopBuy"],repairVerified:["storeAccept","storePay","storeRefundVerified","shopBuy"],storePay:["storeRefundVerified","shopBuy"],storeRefundVerified:["shopBuy"],mailRefund:["courier","returnAllowed","mailBuy","factory","factoryQuote","factoryAccept"],courier:["returnAllowed","mailBuy","factory","factoryQuote","factoryAccept"],returnAllowed:["mailBuy","factory","factoryQuote","factoryAccept"],mailBuy:["factory","factoryQuote","factoryAccept"],factory:["factoryQuote","factoryAccept"],factoryQuote:["factoryAccept"],careGate:["shopBuy","mailBuy"],careStatus:["shopBuy","mailBuy"],careRefund:["shopBuy","mailBuy"]};
const enumOptions={route:["","pass","lower","repair","mail","reject"],storeAccept:["","yes","no"],repair:["unknown","deduct","fee"],repairVerified:["unknown","yes","no"],storePay:["unknown","offset","full"],storeRefundVerified:["unknown","yes","no"],shopBuy:["","yes","no"],mailRefund:["unknown","cash","gift","unlinked"],courier:["","pickup","dropoff"],returnAllowed:["","yes","no"],mailBuy:["","yes","no"],factory:["pending","approved","lower","rejected"],factoryAccept:["","yes","no"],standaloneBuy:["","yes","no"],careStatus:["unknown","refundable","no"]};
function fresh(){return {...base};}
function change(previous,key,value){
 if(!(key in base))return {...previous};
 const s={...previous};
 if(key==="careGate")value=Boolean(value);
 else if(key==="quote"||key==="factoryQuote")value=Math.max(0,Math.min(6900,Math.round(Number(value)/100)*100));
 else if(key==="careRefund")value=Math.max(0,Math.min(2500,Math.round(Number(value)/50)*50));
 else if(key==="budget")value=Math.max(3500,Math.min(11500,Math.round(Number(value)/100)*100));
 else if(!enumOptions[key]||!enumOptions[key].includes(value))return s;
 s[key]=value;
 (reset[key]||[]).forEach(k=>s[k]=base[k]);
 return s;
}
function evaluate(s){
 const price=11500,shop=["pass","lower","repair"].includes(s.route);
 const quote=s.route==="pass"?7000:s.route==="lower"?s.quote:s.route==="repair"?(s.repair==="deduct"?6772:s.repair==="fee"&&s.repairVerified==="yes"?7000:null):null;
 const fee=s.route==="repair"&&s.repair==="fee"&&s.repairVerified==="yes"?228:0;
 const careBlocked=s.careGate&&(s.careStatus!=="refundable"||s.careRefund<=0);
 const shopAccept=s.route==="pass"||s.route==="lower"&&s.storeAccept==="yes"||s.route==="repair"&&quote!==null&&s.storeAccept==="yes";
 const readyShop=shop&&shopAccept&&quote!==null&&(s.storePay==="offset"||s.storePay==="full"&&s.storeRefundVerified==="yes")&&!careBlocked;
 const readyMail=s.route==="mail"&&s.mailRefund==="cash"&&["pickup","dropoff"].includes(s.courier)&&s.returnAllowed==="yes"&&!careBlocked;
 const shopPurchased=readyShop&&s.shopBuy==="yes",mailPurchased=readyMail&&s.mailBuy==="yes",standalonePurchased=s.route==="reject"&&s.standaloneBuy==="yes";
 const purchased=shopPurchased||mailPurchased||standalonePurchased;
 const noBuy=shop&&s.shopBuy==="no"||s.route==="lower"&&s.storeAccept==="no"||s.route==="repair"&&s.storeAccept==="no"||s.route==="mail"&&s.mailBuy==="no"||s.route==="reject"&&s.standaloneBuy==="no";
 const factorySettled=mailPurchased&&(s.factory==="approved"||s.factory==="rejected"||s.factory==="lower"&&s.factoryAccept!=="");
 const factoryCredit=mailPurchased?(s.factory==="approved"?7000:s.factory==="lower"&&s.factoryAccept==="yes"?s.factoryQuote:0):0;
 const factoryReturned=factorySettled&&(s.factory==="rejected"||s.factory==="lower"&&s.factoryAccept==="no");
 const pending=mailPurchased&&!factorySettled;
 const credit=shopPurchased?quote:factoryCredit;
 const dueNow=shopPurchased?(s.storePay==="offset"?price-quote+fee:price+fee):purchased?price:0;
 const refundLater=shopPurchased&&s.storePay==="full"?quote:mailPurchased?factoryCredit:0;
 const netCash=pending?null:!purchased?0:price-credit+(shopPurchased?fee:0);
 const outcome=noBuy?"not-buy":shopPurchased?"bought-traded":standalonePurchased?"bought-standalone":mailPurchased&&pending?"bought-pending":mailPurchased&&factoryReturned?"bought-return-old":mailPurchased&&factorySettled?"bought-traded":"undecided";
 const labels={"not-buy":"不买，带旧手机离店","bought-traded":"买了，新机付款与旧机折抵已确认","bought-standalone":"买了全价新机，旧机保留","bought-pending":"已买新机，旧机等待验机","bought-return-old":"已买新机，拒绝折抵并取回旧机","undecided":"还没决定买不买"};
 return {price,shop,quote,fee,careBlocked,readyShop,readyMail,shopPurchased,mailPurchased,purchased,noBuy,factorySettled,factoryReturned,pending,credit,dueNow,refundLater,netCash,outcome,outcomeLabel:labels[outcome],overBudget:purchased&&netCash!==null&&netCash>s.budget};
}
window.TradeInModel={fresh,change,evaluate,defaults:base};
})();