# 量化选股终端 UI — AI 接入指令

## 项目概述

这是一个量化选股终端的完整 UI 设计项目，包含桌面端和移动端两套页面。所有页面均为独立单文件 HTML，无构建依赖，可直接在浏览器打开运行。

## 项目结构

```
quant-stock-ui/
├── desktop/              桌面端 (1440px, 侧边栏240px + 顶栏64px)
│   ├── dashboard.html    综合仪表盘
│   ├── swing.html        波段选股
│   ├── longterm.html     长线选股
│   ├── etf.html          ETF策略
│   └── sim.html          模拟盘
├── mobile/               移动端 (375px, 底部Tab栏56px + 顶栏48px)
│   ├── dashboard.html    综合仪表盘
│   ├── swing.html        波段选股
│   ├── longterm.html     长线选股
│   ├── etf.html          ETF策略
│   └── sim.html          模拟盘
├── shared/
│   └── colors_and_type.css   共享设计 token
├── project.json          项目元数据
└── quant-stock-ui.design     Trae Design 画布文件
```

## 技术栈

- HTML5 单文件，无框架
- Tailwind CSS v4 (CDN)
- Chart.js 4.4.1 用于 K线/折线/饼图
- Lucide 1.8.0 用于图标
- 字体: Inter + Noto Sans SC + JetBrains Mono

## 设计规范

- 深色主题，背景 #0b0b0f
- 主色 #2dd4bf (青绿)
- A 股配色: 红涨(#ef5350) 绿跌(#26c584)
- 卡片背景 #141419，二级背景 #1c1c24
- 圆角 8px/12px
- 文字层级: #f2f2f5 / #a0a0b0 / #6c6c80

## 页面内容说明

### 综合仪表盘 (dashboard)
- 指数行情条 (上证/深证/创业板/科创50)
- 市场宽度 (上涨/下跌/涨停/跌停)
- 行业涨幅排行
- 情绪指标 (恐贪指数)
- 新闻面

### 波段选股 (swing)
- 左侧: 信号列表 (8只股票, 含信号类型/评分/价格/涨跌)
- 右侧详情: 股票头部 -> K线图 -> 建仓计划 -> 标签页
- 标签页内容: 信号详情/技术面/资金流向/基本面/订单簿
- 基本面含: 主营业务构成/财务数据表(4年)/近期重大订单/基本面摘要
- 切换个股时所有数据同步更新

### 长线选股 (longterm)
- 左侧: 股票列表 (8只, 含PE/PB/ROE/综合评分)
- 右侧详情: 股票头部 -> K线图 -> 因子评分表 -> 基本面/估值/持仓/财务数据
- 因子: 价值/质量/成长/动量

### ETF策略 (etf)
- 左侧: ETF列表 (8只, 含净值/涨跌/折溢价)
- 右侧详情: K线图 -> 重仓股表 -> 成分股/净值跟踪/折溢价/资金流向/相关性

### 模拟盘 (sim)
- 账户概览 (总资产/今日盈亏/总盈亏/可用资金/仓位)
- 持仓列表 (4只, 含成本/现价/盈亏)
- 委托/成交/资金 Tab
- 桌面端含下单面板, 移动端无下单面板

## 接入指令模板

将以下内容复制给目标 AI:

---

你是一个专业的前端开发 AI。现在需要你接手一个已完成的量化选股终端 UI 项目。

项目路径: [填写实际路径]/quant-stock-ui/

项目结构:
- desktop/ 目录: 桌面端 5 个页面 (1440px 宽)
- mobile/ 目录: 移动端 5 个页面 (375px 宽)
- shared/colors_and_type.css: 设计 token
- project.json: 完整项目元数据

请先读取 project.json 了解项目全貌，然后根据需要读取对应页面的 HTML 文件。

所有页面均为独立单文件 HTML，技术栈:
- Tailwind CSS v4 (CDN): https://cdn.tailwindcss.com
- Chart.js 4.4.1: https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js
- Lucide 1.8.0: https://unpkg.com/lucide@1.8.0

设计规范:
- 深色主题, 背景 #0b0b0f
- 主色 #2dd4bf
- A股配色: 红涨 #ef5350, 绿跌 #26c584
- CSS 变量前缀 --qs-

页面包含 8 只 A 股的完整模拟数据 (行情/财务/持仓/订单)。切换个股时 K线图和所有面板同步更新。

[在此描述你的具体需求，例如: 接入实时行情API / 替换为Vue组件 / 添加新页面 / 修改某页布局 等]

---

## 注意事项

1. 所有数据为模拟数据，非实时行情
2. 页面依赖 CDN，离线环境需替换为本地引用
3. 桌面端和移动端是独立页面，非响应式适配
4. 每个页面内嵌完整 CSS token，无需额外引入样式文件
5. K线图使用 Chart.js，数据在页面 JS 中生成
