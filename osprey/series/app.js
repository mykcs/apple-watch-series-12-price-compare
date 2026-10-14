"use strict";
const list = document.getElementById("family-list");
const browser = document.querySelector(".browser");
const detail = document.getElementById("family-detail");
const search = document.getElementById("series-search");
const count = document.getElementById("result-count");
const filters = [...document.querySelectorAll("[data-filter]")];
const state = { families: [], category: "all", query: "", selectedId: null, categories: {} };
const money = value => new Intl.NumberFormat("en-US", {style:"currency",currency:"USD",maximumFractionDigits:0}).format(value);
const make = (tag, className, value) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (value !== undefined && value !== null) node.textContent = value;
  return node;
};
const officialLink = (url, text) => {
  const a = make("a", "", text);
  a.href = url;
  a.target = "_blank";
  a.rel = "noopener noreferrer";
  return a;
};
const currentFamily = () => state.families.find(f => f.id === state.selectedId) || null;
const visibleFamilies = () => state.families.filter(f => {
  if (state.category !== "all" && f.category !== state.category) return false;
  if (!state.query) return true;
  const corpus = [f.name, f.tagline, f.intro, f.bestFor, f.caution, ...f.products.flatMap(p => [p.name, p.description])].join(" ").normalize("NFKC").toLocaleLowerCase();
  return corpus.includes(state.query);
});
function renderDetail() {
  detail.replaceChildren();
  const family = currentFamily();
  if (!family) {
    detail.append(make("div", "skeleton", "没有符合条件的系列。调整筛选或搜索后再试。"));
    return;
  }
  detail.append(make("div","step","SELECTED COLLECTION · 已选系列"));
  detail.append(make("h3","",family.name));
  detail.append(make("p","intro",family.intro));
  const why = make("div","why");
  const best = make("div");
  best.append(make("div","hint","适合什么"), make("p","",family.bestFor));
  const caution = make("div");
  caution.append(make("div","hint","先想清楚"), make("p","",family.caution));
  why.append(best,caution);
  detail.append(why);
  const bar = make("div","subhead");
  bar.append(make("h4","","这个系列的代表型号"),make("span","","美国官网价 · 2026-10-14"));
  detail.append(bar);
  for (const product of family.products) {
    const card = make("article","product");
    const row = make("div","producthead");
    row.append(make("h5","",product.name),make("div","price",money(product.priceUsd)));
    card.append(row,make("div","volume",product.volume),make("p","",product.description));
    card.append(officialLink(product.url,product.url===family.seriesUrl?"在官网系列中查看 ↗":"查看官网产品 ↗"));
    detail.append(card);
  }
  const footer = make("div","detail-footer");
  const allLink = officialLink(family.seriesUrl,"查看该系列全部型号 ↗");
  allLink.className = "series-link";
  const back = make("button","back-to-list","↑ 返回系列列表");
  back.type = "button";
  back.addEventListener("click",()=>document.getElementById("browse").scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"start"}));
  footer.append(allLink,back);
  detail.append(footer);
}
function selectFamily(id,scrollOnMobile = false) {
  if (!state.families.some(f=>f.id===id)) return;
  state.selectedId = id;
  history.replaceState(null,"","#"+encodeURIComponent(id));
  renderAll();
  if (scrollOnMobile && window.matchMedia("(max-width: 760px)").matches) {
    detail.scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"start"});
  }
}
function placeDetail() {
  const mobile = window.matchMedia("(max-width: 760px)").matches;
  if (!mobile) {
    browser.append(detail);
    return;
  }
  const selectedButton = list.querySelector('.family[aria-pressed="true"]');
  if (selectedButton) {
    selectedButton.insertAdjacentElement("afterend", detail);
  } else {
    browser.append(detail);
  }
}
window.addEventListener("resize", placeDetail);
function renderAll() {
  const visible=visibleFamilies();
  if (!visible.some(f=>f.id===state.selectedId)) state.selectedId=visible.length?visible[0].id:null;
  filters.forEach(button=>button.setAttribute("aria-pressed",String(button.dataset.filter===state.category)));
  count.textContent=visible.length+" / "+state.families.length+" 个系列";
  list.replaceChildren();
  if (!visible.length) {
    list.append(make("div","empty","没有找到相应系列。试试清空搜索词，或改成“全部”。"));
  }
  for (const f of visible) {
    const button=make("button","family");
    button.type="button";
    button.dataset.family=f.id;
    button.setAttribute("aria-pressed",String(state.selectedId===f.id));
    button.setAttribute("aria-label","查看 "+f.name+" 系列的代表产品与价格");
    button.append(make("span","category",state.categories[f.category]||f.category),make("strong","name",f.name),make("span","tagline",f.tagline));
    const from=make("div","from");
    from.append(make("span","","代表型号参考价起"),make("strong","",money(Math.min(...f.products.map(p=>p.priceUsd)))));
    button.append(from);
    button.addEventListener("click",()=>selectFamily(f.id,true));
    list.append(button);
  }
  renderDetail();
  placeDetail();
}
function showFailure(error) {
  list.replaceChildren(make("div","empty","系列资料暂时无法加载，请稍后刷新。"));
  detail.replaceChildren();
  detail.append(make("p","intro","资料加载失败；可以先从品牌官网查询。"));
  detail.append(officialLink("https://www.osprey.com/featured/shop-by-collections","打开 Osprey 官方系列目录 ↗"));
  count.textContent="读取失败";
  console.error("Osprey catalog load failed:",error);
}
filters.forEach(button=>button.addEventListener("click",()=>{
  state.category=button.dataset.filter;
  renderAll();
}));
search.addEventListener("input",()=>{
  state.query=search.value.trim().normalize("NFKC").toLocaleLowerCase();
  renderAll();
});
window.addEventListener("hashchange",()=>{
  const id=decodeURIComponent(location.hash.slice(1));
  if(state.families.some(f=>f.id===id)){
    state.category="all";
    state.query="";
    search.value="";
    state.selectedId=id;
    renderAll();
  }
});
fetch("./catalog.json",{cache:"no-store"})
  .then(r=>{if(!r.ok)throw new Error("HTTP "+r.status);return r.json();})
  .then(catalog=>{
    if(!Array.isArray(catalog.families)||catalog.families.length===0)throw new Error("empty catalog");
    state.families=catalog.families;
    state.categories=catalog.categoryLabels;
    const incoming=decodeURIComponent(location.hash.slice(1));
    state.selectedId=state.families.some(f=>f.id===incoming)?incoming:state.families[0].id;
    const total=state.families.reduce((n,f)=>n+f.products.length,0);
    document.getElementById("catalog-count").textContent=state.families.length+" 个常见系列";
    document.querySelectorAll(".meta span")[1].textContent=total+" 款代表型号";
    renderAll();
  })
  .catch(showFailure);
