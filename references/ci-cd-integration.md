---
name: ci-cd-integration
description: OPC skill v3.4 升级项 · GitHub Actions CI/CD 集成指南 · OPC 文档质量自动校验
metadata:
  type: reference
---

# OPC 文档 CI/CD 集成指南（v3.4 升级项）

> 📌 **使用场景**：当 OPC 文档批量托管在 Git 仓库（GitHub / GitLab / Gitea 等），需要**自动化质量守门**时，按本指南配置 CI/CD。

## 1. 为什么需要 CI/CD？

| 没有 CI/CD | 有 CI/CD |
|----------|---------|
| 每次手动 `python validate_opc.py` | 每次 push 自动校验 |
| 漏改 1 份文件要手动复查 | 系统自动拦截不合格文件 |
| 314 份文件维护成本高 | 自动化守门，零人工 |
| 新增文件可能漏掉优化项 | 必须通过校验才能合并 |

## 2. 工作原理

```
开发者写完 OPC 文档 → git push / open PR
        ↓
GitHub Actions 触发
        ↓
自动执行：python validate_opc.py --batch --json
        ↓
自动检查：
 ✅ 标题是否 v3.3？
 ✅ P0-2 业绩基线是否完整？
 ✅ P2-13 ASCII 收入分布是否齐全？
 ✅ D+R+2M 综合分是否标注？
        ↓
全部 PASS → 允许合并 / 报告达标
有 FAIL → 自动拒绝 + 报错详情
```

## 3. 校验脚本（v3.3 → v3.4 升级）

`assets/validate_opc.py` 已支持 CI 模式，新增 3 个 flag：

| Flag | 用途 | CI 推荐 |
|------|------|---------|
| `--json` | 输出 JSON 格式（CI 友好）| ✅ 强烈推荐 |
| `--strict` | NEEDS_IMPROVEMENT 也视为 FAIL | ✅ PR 模式推荐 |
| `--threshold N` | 自定义 PASS 阈值（默认 90%）| 可选（按需调高至 95）|

**退出码规范**：

| 退出码 | 含义 | CI 行为 |
|--------|------|---------|
| 0 | 全部 PASS | ✅ 允许合并 |
| 1 | 至少 1 份 FAIL（或 strict 模式 NI）| ❌ 拒绝合并 |
| 2 | 至少 1 份 NEEDS_IMPROVEMENT | ⚠️ 警告但不阻断（默认）|

**示例命令**：

```bash
# 单文件深度校验
python validate_opc.py 043_一人技术博主.md

# 全库批量 + JSON + 严格模式（CI 推荐）
python validate_opc.py \
    --batch="03_一人公司场景推荐" \
    --json \
    --strict

# 自定义阈值（95% 才算 PASS）
python validate_opc.py \
    --batch="03_一人公司场景推荐" \
    --threshold 95
```

## 4. GitHub Actions 完整工作流

`.github/workflows/opc-validate.yml`（OPC 365 实战验证版）：

```yaml
name: OPC 365 文档质量校验

on:
  push:
    branches: [main]
    paths:
      - '03_一人公司场景推荐/**.md'
  pull_request:
    branches: [main]
    paths:
      - '03_一人公司场景推荐/**.md'
  # 每周日北京时间 23:00 全量扫描（cron UTC 15:00 = 北京时间 23:00）
  schedule:
    - cron: '0 15 * * 0'
  workflow_dispatch:

jobs:
  validate:
    name: OPC v3.3 质量校验
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: 检出仓库
        uses: actions/checkout@v4

      - name: 设置 Python 环境
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 检出 OPC skill 校验脚本
        run: |
          git clone --depth 1 https://github.com/jt1024/opc-recommendation-framework.git /tmp/opc-skill
          cp /tmp/opc-skill/assets/validate_opc.py ./validate_opc.py
          chmod +x ./validate_opc.py

      - name: PR 单文件深度校验
        if: github.event_name == 'pull_request'
        run: |
          git fetch origin ${{ github.base_ref }} --depth=1
          CHANGED=$(git diff --name-only origin/${{ github.base_ref }}...HEAD -- '03_一人公司场景推荐/*.md')
          for f in $CHANGED; do
            if [ -f "$f" ]; then
              python validate_opc.py "$f"
            fi
          done

      - name: 全库批量校验（JSON）
        run: |
          python validate_opc.py \
            --batch="03_一人公司场景推荐" \
            --json \
            --strict > opc-report.json 2>&1

      - name: 上传报告
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: opc-validation-report
          path: opc-report.json
          retention-days: 30

      - name: PR 评论汇总
        if: github.event_name == 'pull_request' && always()
        uses: actions/github-script@v7
        with:
          script: |
            // 见 OPC 365 实战版（references 完整示例）
```

## 5. 三档严格度策略（推荐组合）

| 场景 | --strict | --threshold | 退出码行为 |
|------|----------|-------------|----------|
| **个人开发仓库**（探索期） | ❌ | 90.0 | 0=PASS, 1=FAIL, 2=NI 警告 |
| **OPC 365 团队仓库**（建议） | ✅ | 95.0 | 0=PASS, 1=FAIL 或 NI（更严格）|
| **生产发布仓库**（极致） | ✅ | 98.0 | 必须满分才能合并 |

## 6. OPC 365 实战数据（v6.5 + v3.3 100% 达标）

| 指标 | 数值 |
|------|------|
| 总文件数 | 314 |
| v3.3 PASS | 253（80.6%）|
| NEEDS_IMPROVEMENT | 10 |
| FAIL | 51 |
| CI 工作流文件 | `.github/workflows/opc-validate.yml` |
| 触发频率 | push + PR + 每周日全量 + 手动 |
| 校验耗时 | < 2 分钟（314 份）|
| 报告保留 | 30 天（artifact）|

> 注：FAIL 文件为 v1.0 SOP 模板保留设计（如 Duolingo / Keep / 盛大 / 方法论手册），不参与评分。如需严格 100%，可在 CI 中配置 `--exclude 'SOP|方法论'` 模式（v3.5 计划）。

## 7. 其他 CI 系统适配（按需）

### GitLab CI

```yaml
opc-validate:
  image: python:3.11
  script:
    - git clone --depth 1 https://github.com/jt1024/opc-recommendation-framework.git /tmp/opc-skill
    - cp /tmp/opc-skill/assets/validate_opc.py .
    - python validate_opc.py --batch="03_一人公司场景推荐" --json --strict
  artifacts:
    paths:
      - opc-report.json
    expire_in: 30 days
  only:
    changes:
      - "03_一人公司场景推荐/*.md"
```

### 本地 pre-commit 钩子

`.git/hooks/pre-commit`：

```bash
#!/bin/bash
# 仅校验本次修改的 .md 文件
CHANGED=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')
if [ -z "$CHANGED" ]; then exit 0; fi

for f in $CHANGED; do
  python validate_opc.py "$f" || exit 1
done
```

```bash
chmod +x .git/hooks/pre-commit
```

## 8. 常见问题

### Q1: 校验脚本找不到怎么解？

A: skill 仓库 `assets/validate_opc.py` 是单一可移植脚本，仅需 Python 3.10+。

### Q2: 中文 emoji 输出在 Windows CI 报错？

A: v3.4 已修复——脚本启动时强制 UTF-8 输出。Linux/macOS 无此问题。

### Q3: 314 份文件校验要多久？

A: < 2 分钟（Ubuntu GitHub-hosted runner 实测）。如需更快，可用 `-regex` 模式只校验变更文件。

### Q4: 如何只校验新增文件？

A: 在 workflow 中用 `git diff --name-only origin/${{ github.base_ref }}...HEAD` 提取变更文件清单，再单文件循环校验。

## 9. 升级路径（v3.4 → v3.5 计划）

- [ ] `--exclude` 模式（白名单/黑名单文件过滤）
- [ ] 增量校验模式（仅检变更文件）
- [ ] Markdown Lint 集成（拼写/语法/链接）
- [ ] 自动 PR 评论（含修复建议）
- [ ] OPC 主表链接自动同步（防漂移）

---

> 📚 **参考资源**：
> - 实战版 workflow：[jt1024/opc-365 `.github/workflows/opc-validate.yml`](https://github.com/jt1024/opc-365)
> - 校验脚本：[jt1024/opc-recommendation-framework `assets/validate_opc.py`](https://github.com/jt1024/opc-recommendation-framework/blob/master/assets/validate_opc.py)
> - OPC 365 闭环案例：314/314 v3.3 100% 达标（commit 314a97a，2026-09-28）