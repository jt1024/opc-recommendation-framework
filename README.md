# OPC Recommendation Framework · v3.0

> **行业场景定制化推荐文档生成框架** · 基于 OPC 043 质量基线 · 100 分制验收标准

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)]()
[![Status](https://img.shields.io/badge/status-stable-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-orange.svg)]()
[![OPC Score](https://img.shields.io/badge/OPC%20Score-100%2F100-brightgreen.svg)]()
[![Sections](https://img.shields.io/badge/sections-20-purple.svg)]()
[![Optimizations](https://img.shields.io/badge/optimizations-14-yellow.svg)]()

> **OPC 综合分**：**D4 R3 M4 = 15/20** ⭐⭐⭐ 第三梯队 · [来源：043 实践](references/043-quality-benchmark.md)

---

## 🎯 这是什么

一个用于**生成"一人公司"行业推荐文档**的写作框架，基于 OPC（One-Person Company）043 实践提炼，输出文档质量基线 **17,000-22,000 字 · 100/100 分**。

当给定 **行业场景 + 大致需求** 时，本框架输出包含：

- ✅ 20 章节完整闭环（决策层 → 方法层 → 实战层 → 权威层 + 附录）
- ✅ 14 项质量优化（P0/P1/P2 全覆盖）
- ✅ D+R+2M 综合分模型（OPC 全库统一评分）
- ✅ 用户画像匹配 · 现金流规划 · 法律合规 · 失败案例
- ✅ 100 分制验收清单 · 可作为审阅工具

---

## 📖 目录

- [TL;DR · 30 秒看懂](#-tldr--30-秒看懂)
- [为什么是 v3.0](#-为什么是-v30)
- [14 项质量优化（100 分制）](#-14-项质量优化100-分制)
- [D+R+2M 综合分模型](#-dr2m-综合分模型)
- [20 章节结构](#-20-章节结构)
- [快速开始](#-快速开始)
- [文件结构](#-文件结构)
- [方法论核心](#-方法论核心)
- [验证与发布标准](#-验证与发布标准)
- [版本演进](#-版本演进)
- [应用案例](#-应用案例)
- [相关资源](#-相关资源)
- [贡献指南](#-贡献指南)
- [许可](#-许可)

---

## ⚡ TL;DR · 30 秒看懂

| 你想知道 | 答案 |
|---------|------|
| **这是什么？** | OPC 行业推荐文档生成框架（不是工具，是结构 + 标准） |
| **给谁用？** | 给"一人公司"创业者 / 转型顾问 / AI 写作助手 |
| **输入什么？** | 行业场景 + 大致需求（如：南沙本地制造业数字化转型） |
| **输出什么？** | 17,000-22,000 字完整推荐文档（含 14 项优化 + 100 分验收） |
| **质量基线？** | 043_一人数字化转型顾问.md（D4 R3 M4 = 15/20 · 100/100 分） |
| **适用版本？** | Claude Code · MCP · 其他 LLM 客户端 |
| **什么时候用？** | 写新行业文档 / 审阅已有文档 / 客户咨询方案 |
| **什么时候不用？** | 纯理论对比 / 单一产品介绍 / 学术研究综述 |

---

## 💡 为什么是 v3.0

| 版本 | 时间 | 质量标准 | 核心升级 |
|------|------|---------|---------|
| **v1.0** | 2024-Q4 | 基础 14 章 | OPC 文档初始结构 |
| **v2.0** | 2025-H1 | 14 章 + D+R+M | 引入评分模型 + 引用源 |
| **v3.0** | 2026-09 | **20 章 + D+R+2M + 14 项优化** | 043 质量基线 · 100 分验收 |

### v3.0 的三大突破

1. **20 章节闭环**：从 v2.0 的 14 章扩展到 20 章节（引言/决策卡/读者分发/★专属建议前置 + 一→十五主体 + 附录 3 件套）
2. **D+R+2M 综合分**：M 行业成熟度双倍权重（占比 50%），统一 OPC 全库评分口径
3. **14 项质量优化**：5 P0（必含）+ 5 P1（推荐）+ 4 P2（锦上添花），每项对应可测量分值

### 043 的关键贡献

- 17,715 字完整文档（v2.0 的 7,652 字 → v3.0 的 17,715 字）
- 100/100 评分（v2.0 ~75/100 → v3.0 100/100）
- 14 项优化全部落地（成为 v3.0 框架的实证基础）

---

## 🏆 14 项质量优化（100 分制）

### 🔴 P0 · 必含（5 × 12 = 60 分）· 任一缺失直接返工

| # | 优化项 | 位置 | 作用 |
|---|--------|------|------|
| **P0-1** | 读者筛选 | 段一首 | callout 画像匹配，节省读者时间 |
| **P0-2** | 数字分布 | 业绩基线 / 附录 | 中位数 + 25/75 分位 + 拒单率 |
| **P0-3** | 本地 N 客户 | 13.9 | ≥ 20 家分组 + cold call 话术 |
| **P0-4** | 4 方案现金流 | 13.4 | 对比表 + 最坏兜底 + 心理预案 |
| **P0-5** | 失败案例 | 10.4 | 2 个失败 + 退出机制 4 步 |

### 🟡 P1 · 推荐（5 × 5 = 25 分）· 缺失 2 项以上需补强

| # | 优化项 | 位置 | 作用 |
|---|--------|------|------|
| **P1-6** | 客户原话 | 每案例末尾 | 3-4 条实战访谈（决策可信度） |
| **P1-7** | 工具上手日记 | 五、90 天 | D1/D7/D14/D30 记录 |
| **P1-8** | 9.5 法律合规 | 九章末 | 6-8 条合规事项 + 红线清单 |
| **P1-9** | 家庭决策会议 | 13.5/13.8 | 4 共识 + 4 步 + 应急金 4 级 |
| **P1-10** | 评分依据 | 附录 1 | D/R/M 各 4-5 个数据点 + 来源 |

### 🟢 P2 · 锦上添花（4 × 3.75 = 15 分）

| # | 优化项 | 位置 | 作用 |
|---|--------|------|------|
| **P2-11** | 90 天行动清单 | 13.6.1 | W1-W12 + 5 项生死线 |
| **P2-12** | 引用源分组 | 十五章 | 5 组分类（A/B/C/D/E）|
| **P2-13** | ASCII 信息图 | 决策图 + 分布 | ≥ 2 个（决策路径 + 收入分布）|
| **P2-14** | 相近场景跳转 | 附录 2 | 10 个相近场景 + 决策树 |

**总分**：P0 + P1 + P2 = **60 + 25 + 15 = 100 分**

---

## 📐 D+R+2M 综合分模型

OPC 全库统一评分标准 · **所有子文档必须内联此模型说明**

### 公式

```
OPC 综合分 = D + R + 2M
满分 20 分（M 双倍权重，占比 50%）
```

### 4 维度定义

| 字母 | 含义 | 满分 | 说明 |
|---|---|---|---|
| **D** | Demand 需求度 | 5 | 客户基数、付费意愿、复购频次、区域容量 |
| **R** | Risk 风险系数（高分=低风险）| 5 | 合规难度、获客波动、回款风险、行业周期 |
| **M** | Maturity 行业成熟度 | 5 | 工具链 / SOP / 服务链 / 客群认知（**双倍权重**）|

### 梯队划分

| 总分 | 梯队 | ⭐ |
|---|---|---|
| 18-20 | 第一梯队 | ⭐⭐⭐⭐⭐ |
| 16-17 | 第二梯队 | ⭐⭐⭐⭐ |
| 14-15 | 第三梯队 | ⭐⭐⭐ |
| 12-13 | 第四梯队 | ⭐⭐ |
| ≤ 11 | 第五梯队 | ⭐ |

### 043 实例

```
D4 R3 M4 = 15/20
       ↓
D + R + 2M = 4 + 3 + 4×2 = 15
```

| 维度 | 分值 | 依据 |
|------|----:|------|
| **D=4** | 4/5 | 南沙 + 大湾区制造业 / 跨境电商 / 服务业数字化转型需求密集 |
| **R=3** | 3/5 | 合规要求中等（数据安全/知识产权/客户隐私），但无金融级监管 |
| **M=4** | 4/5 | ERP/MES/CRM/低代码工具链成熟，1 人顾问可独立交付 |

### ⚠️ 严禁使用的错误格式

- ❌ `D4 R3 M4 M2 = 15/20`（4 个独立字母，与 D+R+2M 加权公式矛盾）
- ❌ `D + R + M + M`（未标记加权，含义模糊）
- ❌ `D+R+M1+M2`（041 老格式，非综合分）
- ❌ 单独写 `D/R/M` 数值不解释（读者无法理解）

---

## 📚 20 章节结构

```
🧭 段一：决策层（5 分钟 · 6 元素 · 17%）
├─ 🧭 读者筛选（P0-1 · callout 画像）
├─ 📖 引言（A 投资回报式 · 165-210 字）
├─ 📍 30 秒决策卡（9 行表格）
├─ 🚦 决策路径图（4 项硬筛 ASCII）
├─ 🎯 读者分发（3 档推荐路径）
└─ ★ 专属建议（前置 · 6-8 子节）

📚 段二：方法层（30 分钟 · 9 章 · 44%）
├─ 一、需求画像（时段表）
├─ 二、核心痛点（前 5 名）
├─ 三、维度适配度评分（加权矩阵）
├─ 四、最终推荐（主推 + 备选 + 不推荐）
├─ 五、90 天落地地图（6 阶段 × 2 周）
├─ 六、成本测算（TCO + ROI）
├─ 七、风险预案（双方案 · 🔴🟡🟢）
├─ 八、决策速查（5-8 子场景）
└─ 九、行业特有提醒 + 9.5 法律合规

🔬 段三：实战层（按需 · 5 章 · 32%）
├─ 十、案例实证库 + 10.4 失败案例
├─ 十一、跨场景迁移
├─ 十二、上下游关联
├─ 十三、用户专属建议（4 维深化）
└─ 十四、入局前置（资质/技能/学习）

📚 段四：权威层（独立成章 · 7%）
└─ 十五、引用来源汇总（5 组分组）

📐 附录（3 件套）
├─ 附录 0：D+R+2M 模型说明（必含）
├─ 附录 1：评分依据原始数据（P1-10）
└─ 附录 2：相近场景跳转（P2-14）
```

**总字数**：17,000-22,000 字（含表格/代码块）

---

## 🚀 快速开始

### 1. 安装（Claude Code 用户）

本 skill 默认安装于：
```
C:\Users\admin\.claude\skills\opc-recommendation-framework\
```

Claude Code 自动识别，无需额外配置。

### 2. 调用方式

**方式 A：直接调用 skill**
```
/opc-recommendation-framework
```

**方式 B：作为上下文使用**

将本目录作为 system context 加载，提示词可参考：
```markdown
你是 OPC 行业推荐文档写作助手。严格遵循 v3.0 skill 框架：
1. 参考 SKILL.md 的 20 章节结构
2. 按 references/043-quality-benchmark.md 的 14 项优化标准扩写
3. 用 references/template-checklist.md 的 100 分制自检
4. 用 assets/template-skeleton.md 的空白模板填空
5. 用 assets/scoring-matrix-template.md 的 D+R+2M 评分

当前场景：[行业名] · [细分方向] · [规模]
```

### 3. 三步生成流程

```
Step 1 · 加载骨架    → assets/template-skeleton.md
Step 2 · 按 P0 扩写  → references/043-quality-benchmark.md
Step 3 · 100 分验收  → references/template-checklist.md
```

### 4. 输出文件命名

```
[NNN]_[行业名].md

例如：
043_一人数字化转型顾问.md
051_一人跨境电商运营.md
127_一人宠物保险经纪.md
```

---

## 📂 文件结构

```
opc-recommendation-framework/
├── README.md                                  本文档
├── SKILL.md                                   v3.0 主框架（20 章节 + D+R+2M）
├── assets/
│   ├── template-skeleton.md                   20 章节空白骨架（含 14 项优化模板）
│   └── scoring-matrix-template.md             加权矩阵 + D+R+2M 综合分
└── references/
    ├── 043-quality-benchmark.md               043 质量基线（扩写模板 + 100 分审计）
    ├── template-checklist.md                  14 项优化验收清单
    ├── methodology-detailed.md                评分模型 + ROI 公式推导
    └── citation-sources.md                    顶级咨询报告库
```

### 文件用途速查

| 文件 | 用途 | 何时读 |
|------|------|--------|
| **README.md** | 项目入口 | 第一次接触项目 |
| **SKILL.md** | 框架总览 | 调用 skill 时 |
| **assets/template-skeleton.md** | 生成文档骨架 | 写新文档时 |
| **assets/scoring-matrix-template.md** | 评分公式参考 | 写 Section 3 + 综合分时 |
| **references/043-quality-benchmark.md** | 扩写参考模板 | 任何扩写环节 |
| **references/template-checklist.md** | 100 分验收 | 文档完成后 |
| **references/methodology-detailed.md** | 方法论推导 | 需要解释原理时 |
| **references/citation-sources.md** | 引用源库 | 撰写引用块时 |

---

## 🛠 方法论核心

### 1. 评分矩阵设计（Section 3）

**6-10 维度选取原则**：
- 3-4 个**核心业务能力**（50-60% 权重）
- 1-2 个**硬约束**（合规/数据安全 · 20-30% 权重）
- 1 个**经济性**（10% 权重）
- 1 个**长期价值**（10% 权重）

### 2. ROI 计算公式（Section 6）

```
ROI = (替代前成本 - 替代后成本) × 12 月 / 工具年成本
回本周期 = 工具年成本 / (替代前成本 - 替代后成本) / 12
```

**保守估计折扣**：实际节省取行业基准的 60-70%

### 3. 风险预案双方案模式（Section 7）

每个风险必须给：
- **应对**（预防措施 · 可执行清单）
- **兜底**（真出事的应急方案）

### 4. 用户专属建议结构（Section 13）

针对具体用户画像，必须包含：
```
✅ 强匹配项（4-5 条 · 画像特征映射）
⚠️ 风险点（3-4 条 · 🔴🟡🟢 标注）
💡 推荐路径（A/B/C/D 4 个方案 · 6/12 月收入）
📊 现金流规划（具体数字 · 月供匹配）
💎 一句话总结（画像+行业结合）
🎯 第一步行动（本周 3 件事）
🔥 紧迫提醒（3 条不可拖延事项）
```

### 5. 决策路径图（段一 · P2-13）

ASCII 流程图，4 项硬筛快速分流：
```
你符合 4 项硬筛吗？
├─ ✅ 全部是 → 进入段二完整方案
├─ ⚠️ 部分是 → 看 ★ 专属建议（画像匹配）
└─ ❌ 都不是 → 跳 OPC 相近场景（附录 2）
```

完整方法论详见 [references/methodology-detailed.md](references/methodology-detailed.md)

---

## ✅ 验证与发布标准

### 100 分验收流程

| 阶段 | 验收项 | 耗时 |
|------|--------|-----:|
| **第一轮** | 结构完整性 + 段一 4 元素 + P0-1 读者筛选 | 5 分钟 |
| **第二轮** | 14 项优化 P0 自检（5 项 × 12 分）| 10 分钟 |
| **第三轮** | P1 + P2 自检（9 项）| 10 分钟 |
| **第四轮** | 去重规则 + 字数控制 + emoji 规范 | 5 分钟 |
| **第五轮** | 引用完整性 + 质量评分 | 5 分钟 |
| **总计** | | **35 分钟** |

### 发布门槛

| 总分 | 评级 | 处置 |
|------|------|------|
| **≥ 90** | 优质 | ✅ 可发布 |
| **75-89** | 合格 | 🟡 需补强 |
| **< 75** | 不足 | 🔴 返工 |

### 字数控制

- 总中文字符 **17,000-22,000**
- 段一 17% / 段二 44% / 段三 32% / 段四 7%
- 每章 TLDR 严格 4 行

完整验收清单详见 [references/template-checklist.md](references/template-checklist.md)

---

## 📈 版本演进

### v3.0（2026-09 · 当前）

**核心升级**：
- ✅ 20 章节闭环（从 14 章扩展）
- ✅ D+R+2M 综合分模型（OPC 全库统一）
- ✅ 14 项质量优化（100 分制）
- ✅ 段一前置结构（决策卡 / 读者筛选 / ★ 专属建议）
- ✅ 9.5 法律合规清单（独立小节）
- ✅ 10.4 失败案例（独立小节）
- ✅ 附录 3 件套（D+R+2M + 评分依据 + 相近场景）
- ✅ 引用源 5 组分组（独立成章）

### v2.0（2025-H1）

- 14 章基础结构
- 评分矩阵（Section 3）
- ROI 计算（Section 6）
- 案例库（Section 10）

### v1.0（2024-Q4）

- OPC 文档初始 14 章

---

## 🌟 应用案例

### OPC 043 · 一人数字化转型顾问（标杆）

| 维度 | 数值 |
|------|-----:|
| **场景** | 南沙 + 大湾区企业数字化转型咨询 |
| **OPC 综合分** | D4 R3 M4 = **15/20**（第三梯队）|
| **质量评分** | **100/100** |
| **总字数** | 17,715 字 |
| **14 项优化** | 全部到位 |
| **引用源** | 15+ 条（A/B/C/D/E 5 组）|
| **法律合规** | 9.5 节 8 条 + 红线清单 |
| **失败案例** | 2 个 + 退出机制 4 步 |
| **本地客户** | 南沙 20 家分组 + 3 类 cold call 话术 |

详见 [references/043-quality-benchmark.md](references/043-quality-benchmark.md)

---

## 🔗 相关资源

### OPC 项目（外部）

- **OPC 主文档**：OPC 365 场景优先级全景索引
- **OPC 043 原文**：E:\CodeTest\OPC\03_一人公司场景推荐\043_一人数字化转型顾问.md

### 顶级咨询报告库

- 麦肯锡 McKinsey · BCG · 贝恩 Bain · 奥纬 Oliver Wyman · 罗兰贝格 Roland Berger
- 行业基准：LIMRA · MDRT · IQA
- 监管数据：国家金融监管总局 · 统计局 · 各行业协会

详见 [references/citation-sources.md](references/citation-sources.md)

---

## 🤝 贡献指南

### 添加新行业文档

1. 复制 `assets/template-skeleton.md` 为 `[NNN]_[行业名].md`
2. 按 [references/043-quality-benchmark.md](references/043-quality-benchmark.md) 的模板扩写
3. 按 [references/template-checklist.md](references/template-checklist.md) 的 100 分制自检
4. 提交 PR（标题格式：`[新行业] NNN_行业名`）

### 修订现有文档

1. 阅读 [references/043-quality-benchmark.md](references/043-quality-benchmark.md) 找出缺失优化
2. 按优化项扩写或修订
3. 重新跑 100 分验收
4. 提交 PR（标题格式：`[修订] NNN_行业名 · 优化项 P0/P1/P2-X`）

### 修改框架本身

1. 在 [GitHub Issues](https://github.com/jt1024/opc-recommendation-framework/issues) 提案
2. 讨论通过后修改 `SKILL.md` 或模板文件
3. 提供 ≥ 2 个 OPC 文档的实际验证案例
4. 提交 PR（标题格式：`[框架] v3.X 升级 · 变更说明`）

### 质量铁律

- ❌ 杜绝凑字数（[feedback-quality-over-quantity]）
- ✅ 以 043 为质量基线
- ✅ 先研究再扩写
- ✅ 一次写到位

---

## 📜 许可

本框架采用 **MIT 许可**：

```
MIT License

Copyright (c) 2026 jt1024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 致谢

- **043 实践基础**：一人数字化转型顾问场景（17,715 字 · 100/100 分）
- **OPC 365 项目**：365 个 unique 场景的语料支撑
- **Claude Code**：skill 框架的运行环境

---

## 📌 版本信息

| 项 | 值 |
|----|-----|
| **当前版本** | v3.0.0 |
| **发布日期** | 2026-09-05 |
| **下次规划** | v3.1（2026-Q4 · 增加 OPC 行业垂直模板）|
| **维护者** | jt1024 |
| **仓库** | https://github.com/jt1024/opc-recommendation-framework |

---

> ⭐ **如果这个框架对你有帮助，请在 GitHub 上 Star！**
>
> 📝 **问题反馈**：[GitHub Issues](https://github.com/jt1024/opc-recommendation-framework/issues)

---

*本 README 基于 OPC 043 v3.0 实践提炼 · 100/100 评分 · 与 SKILL.md 同步更新 · 2026-09-05*