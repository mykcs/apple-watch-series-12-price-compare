# 小鹰 Osprey 系列目录与价格证据（2026-10-14）

## 目的与边界

网站新增两条**并行**选购路线：

1. `/osprey/`：**按用途选**，适合还不知道具体系列的用户。
2. `/osprey/series/`：**按系列看**，提供可搜索与筛选的系列目录、代表产品介绍和美元价格；点击具体系列后展示两款产品，并指向官方页面。现有用途决策路线不删除。

`osprey/series/catalog.json` 是唯一的目录与价格数据源。此文档不复制商品价格表，以免维护两份数字。JS 只消费本地 JSON，无跨站抓价，也不会把快照说成实时价格。

## 核对方法

- 检查日期：**2026-10-14**。
- 统一市场：Osprey 美国官网（`osprey.com`，US/EN），价格单位 **USD**。
- 价格含义：官网公开商品页或官方系列列表所列的**当日美元参考价格**。官网可能有短期促销或不同配色、尺码、存货状态；页面不得将快照视为当前结账金额，更不得未经重新核查换算为香港或中国大陆报价。
- **收录范围**：18 个常见系列/家族（男女不同版型按官网官方家族组合归并）及其 36 款代表产品；这是精选导览，不声称囊括 Osprey 所有系列和 SKU。
- 具体产品依据：优先使用 JSON 中每款产品对应的 `url` 官方产品页；如果无法可靠确定产品专属路径，则产品链接退回到经核实的同系列官方目录，并以「在官网系列中查看」明示。

## 官方系列来源

| 类别 | 系列 | 官方系列列表 |
|---|---|---|
| 日常通勤 | Daylite | https://www.osprey.com/featured/shop-by-collections/daylite |
| 日常通勤 | Arcane | https://www.osprey.com/featured/shop-by-collections/arcane |
| 日常通勤 | Aoede | https://www.osprey.com/featured/shop-by-collections/aoede |
| 日常通勤 | Metron | https://www.osprey.com/featured/shop-by-collections/metron |
| 一日徒步 | Talon / Tempest | https://www.osprey.com/featured/shop-by-collections/talon-tempest |
| 一日徒步 | Hikelite | https://www.osprey.com/featured/shop-by-collections/hikelite |
| 一日徒步 | Sportlite | https://www.osprey.com/featured/shop-by-collections/sportlite-family |
| 一日徒步 | Stratos / Sirrus | https://www.osprey.com/featured/shop-by-collections/stratos-sirrus-family |
| 一日徒步 | Manta / Mira | https://www.osprey.com/featured/shop-by-collections/manta-mira |
| 多日背负 | Kestrel / Kyte | https://www.osprey.com/featured/shop-by-collections/kestrel-kyte-family |
| 多日背负 | Atmos / Aura AG | https://www.osprey.com/featured/shop-by-collections/new-atmos-aura-ag |
| 多日背负 | Exos / Eja | https://www.osprey.com/featured/shop-by-collections/new-exos-eja |
| 多日背负 | Aether / Ariel | https://www.osprey.com/featured/shop-by-collections/aether-ariel |
| 多日背负 | Rook / Renn | https://www.osprey.com/featured/shop-by-collections/rook-renn-family |
| 旅行 | Farpoint / Fairview | https://www.osprey.com/featured/shop-by-collections/farpoint-fairview |
| 旅行 | Sojourn / Porter | https://www.osprey.com/featured/shop-by-collections/sojourn |
| 旅行 | Transporter | https://www.osprey.com/featured/shop-by-collections/transporter |
| 专业攀登 | Mutant | https://www.osprey.com/featured/shop-by-collections/new-mutant |

其他型号和专用系列以 [官网完整目录](https://www.osprey.com/featured/shop-by-collections) 为准。

## 维护规则

1. 改价格时，先核实 `catalog.json` 中**每个型号对应的官方链接**与市场，更新 `checkedAt`，再运行 `python3 scripts/validate_site.py`。
2. 不根据产品型号推断尺寸或男女版型合身结论；背负合身必须实际试背，容量可能因尺码不同而变化。
3. 每次新增系列，同时更新 **JSON、网站路由与验证**。不用为每个系列另外复制一份页面或价格账本。
4. 若以后加入 HKD/CNY/SGD，需独立记录当地真实销售来源、税费与检查日期；不得拿美国价格套用旧汇率作为当地官方售价。
5. 重命名 / 新增 URL 后必须分别验证 GitHub 测试、Vercel Production 与真实移动浏览器互动。
