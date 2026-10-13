# Apple 购买对比

**在线首页：** https://apple-watch-series-12-price-compare.vercel.app

三个独立页面：

- Apple Watch Series 12：/watch/
- iPhone 18 Pro Max 256GB：/iphone/
- Mac 交互选择工具：/mac/
  - MacBook Pro 芯片选择：/mac/macbook-pro/
  - Mac mini 芯片选择：/mac/mac-mini/
  - SSD 容量与速度：/mac/storage/

## 页面范围

### Apple Watch
购买选择已收口为 46 mm 原色钛金属。页面保留原色钛金属与珍珠白陶瓷的地区价格、重量、表镜 / 表背材质与 Apple 陶瓷技术证据，作为已完成决策的记录；首页顺序降到后面。

### iPhone
只比较 iPhone 18 Pro Max 256GB。中国大陆、香港、新加坡、美国免税州四地官方价，并列出 SIM / eSIM 差异。

2026-10-10 新增香港 Apple 直营购机付款计算器：本人 ZA Card（1.5% StockBack 回赠本人独享）与朋友 Chill Platinum Mastercard（额外回赠封顶、价值五五分），附苹果香港价格、银行官方依据、未证实抽奖的风险边界和可调情境。 旧机处理的六路线研究曾作为探索阶段，现依用户偏好精简为两条正式路线：A Apple Store 现场即时折抵、B Apple 官网全款＋店取＋线上验机退款。互动树固定港币余额 HK$5,080、旧机估价 HK$7,000、必买两年 AppleCare+ HK$1,799；支持模拟验机报价与保障付款时点。礼品卡与私人出售仅在历史研究记录中保留，不再作为当前购买推荐。研究快照见 [`docs/decisions/2026-10-10-iphone-hk-payment.md`](docs/decisions/2026-10-10-iphone-hk-payment.md)。

**到店话术与闯关：** [iPhone 香港换机互动路线](/iphone/trade-in-guide/) 单独保留聊天版的白色卡片、Lucide 风格图标、五种店员回复、可复制照念话术，以及按实际回答逐步展开的「买／不买」结局。它是到店现场决策工具，不会改写此页 A/B 正式财务计算与银行奖励。入口位于 `/iphone/` 上方。闯关金额沿用聊天时口头整数 HK$11,500，和正式商品价格 HK$11,499 差 HK$1，页面已明示。

**重要规则：** 现场已确认 HK$7,000 就不再问屏幕，也不二次扣费；邮寄需要先确认与新机订单关联、原付款方式退款、承运商交付方法和能否拒绝压价退回旧机。**付款前**放弃是「不买」；**付款后**拒绝工厂降低的旧机报价是「已买新机、拒绝折抵、退回旧机」，绝不把两者混同。旧中国大陆 AppleCare+ 可选为成交门槛，先确认退款，不自动取消。

**2026-10-13 实际购机结局（新增，不覆盖模拟器）：** 已购买 **iPhone 18 Pro Max · 冰川蓝 · 256GB**。本次在香港到店咨询时，店员说明需要网上下单、店内取货，因此这张网上订单没有当场旧机折抵；是否可通过香港店内直接买新机并现场抵旧机，**用户未问清**。用户计划根据 Trade In 邮件的 **8 位验证码**自行去香港顺丰点寄旧 iPhone 17 Pro Max，最终 **HK$7,000 尚未验机确认**。店员提及内地门店也可折抵，但不代表可以把内地店内折抵直接兑换成与香港订单关联的人民币现金。原话和证据边界见 [真实路线记录](docs/decisions/2026-10-13-iphone-hk-actual-route.md)，网站上的 [固定主线图](/iphone/trade-in-guide/#actual-route-20261013) 在互动模拟器上方。以用户实际已买的新机为准；旧机寄件、验机、返款与 AppleCare+ 退款仍未收口。

### Mac
当前优先级最高。除 MacBook Pro / Mac mini 的教育价、芯片、内存、SSD 外，Mac mini 页面新增实际工作流问题：当 iPhone 上的 ChatGPT 请求 GitHub 权限并触发 Passkey 时，没有内建 Touch ID 的 Mac mini 如何完成认证，以及本地、附近 iPhone、远程无人值守三种场景该如何区分。

重要：SSD 是存储介质类型，512GB / 1TB / 2TB 是容量。2025 年的 14 英寸 M5 MacBook Pro 曾有 512GB 配置；2026 年当前在售 M5 MacBook Pro 从 1TB 起。M6 Mac mini 仍有 256GB、512GB、1TB 等 SSD 配置。不是只有 1TB 才有 SSD。

## 汇率

页面统一使用 2026-09-25 汇率快照，人民币折算四舍五入到元：

- 1 HKD ≈ 0.8556 CNY
- 1 SGD ≈ 5.2556 CNY
- 1 USD ≈ 6.7114 CNY

最终价格、库存、教育资格与汇率以下单页面为准。


## 开发与 CI

开发方向、轻量价格逻辑检查与 Vercel 分工见 [`docs/dev/README.md`](docs/dev/README.md)。
