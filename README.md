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
