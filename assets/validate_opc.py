#!/usr/bin/env python3
"""
validate_opc.py · OPC 文档质量校验脚本（v3.0 · 043 质量基线版）

用法：
    python validate_opc.py <path-to-markdown-file>
    python validate_opc.py --batch <directory>

校验维度（14 项质量优化 + 20 章节结构）：
    P0（5 项 × 12 分）：读者筛选 / 数字分布 / 本地客户 / 4 方案现金流 / 失败案例
    P1（5 项 × 5 分）：客户原话 / 工具日记 / 法律合规 / 家庭会议 / 评分依据
    P2（4 项 × 3.75 分）：90 天清单 / 引用源分组 / ASCII 信息图 / 相近场景跳转

退出码：
    0 = PASS（≥ 90 分）
    1 = FAIL（< 75 分）
    2 = NEEDS IMPROVEMENT（75-89 分）
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional


# ============================================================
# 数据类
# ============================================================

@dataclass
class CheckResult:
    """单项检查结果"""
    name: str
    category: str  # P0 / P1 / P2 / STRUCT / META
    passed: bool
    score: int  # 本项得分
    max_score: int  # 本项满分
    message: str = ""  # 通过则空，失败则说明原因
    fix_hint: str = ""  # 修复建议


@dataclass
class ValidationReport:
    """总报告"""
    file: str
    results: List[CheckResult] = field(default_factory=list)
    total_score: int = 0
    max_score: int = 100
    tier: str = ""

    def add(self, r: CheckResult):
        self.results.append(r)
        self.total_score += r.score

    def compute_tier(self) -> str:
        # 动态计算实际满分（v3.1 修复：max_score 不再硬编码 100）
        actual_max = sum(r.max_score for r in self.results) or self.max_score
        pct = self.total_score / actual_max * 100
        if pct >= 90:
            self.tier = "PASS · 可发布"
        elif pct >= 75:
            self.tier = "NEEDS_IMPROVEMENT · 需补强"
        else:
            self.tier = "FAIL · 返工"
        return self.tier

    @property
    def actual_max_score(self) -> int:
        """实际满分（所有检查项 max_score 之和）"""
        return sum(r.max_score for r in self.results) or self.max_score
        return self.tier


# ============================================================
# 工具函数
# ============================================================

def count_chinese(text: str) -> int:
    """统计中文字符数"""
    return len(re.findall(r'[一-鿿]', text))


def strip_markdown(text: str) -> str:
    """去除 markdown 标记，便于文本匹配"""
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[#*_>|]', '', text)
    return text


def section_exists(text: str, pattern: str) -> bool:
    """判断某个章节标题是否存在"""
    return bool(re.search(pattern, text, re.MULTILINE))


# ============================================================
# META · 元信息校验（10 分）
# ============================================================

def check_title_version(text: str) -> CheckResult:
    """#1 标题必须含 v3.0 · 043 质量基线版"""
    title_match = re.search(r'^# .+', text, re.MULTILINE)
    if not title_match:
        return CheckResult("标题版本号", "META", False, 0, 5,
                           "未找到一级标题", "首行应为 # 标题（v3.0 · 043 质量基线版）")
    title = title_match.group(0)
    if "v3.0" in title and "043" in title and "质量基线" in title:
        return CheckResult("标题版本号", "META", True, 5, 5)
    return CheckResult("标题版本号", "META", False, 0, 5,
                       f"标题不符合 v3.0 格式：{title}",
                       "改为 # 标题（v3.0 · 043 质量基线版）")


def check_word_count(text: str) -> CheckResult:
    """#2 字数必须在 17,000-23,000 中文字符范围

    v3.1 升级：要求声明使用精确措辞（"中文字符" / "中文" / "CJK"），
    避免 "X 字" 这种含数字/英文/标点的歧义形式。
    """
    actual = count_chinese(text)
    # 匹配声明：要求至少包含"中文字符|中文|CJK|Chinese"等精确措辞
    precise_pattern = r'总字数\*\*[：:]\s*约?\s*[\d,]+\s*(中文字符|中文\s*字符|CJK\s*字符|Chinese)'
    precise_match = re.search(precise_pattern, text)
    # 兼容模式：只匹配数字 + 字（但会被标记为措辞不精确）
    loose_pattern = r'总字数\*\*[：:]\s*约?\s*([\d,]+)'
    loose_match = re.search(loose_pattern, text)

    declared = None
    if precise_match:
        # 提取数字
        num_match = re.search(r'([\d,]+)', precise_match.group())
        declared = int(num_match.group(1).replace(',', '')) if num_match else None
    elif loose_match:
        # 措辞不精确，标记但仍提取数字
        declared = int(loose_match.group(1).replace(',', ''))

    phrasing_ok = precise_match is not None
    in_range = 17000 <= actual <= 23000
    declared_match_ok = declared is None or abs(declared - actual) <= 500

    # 计算得分
    score = 0
    issues = []
    if phrasing_ok:
        score += 2
    else:
        issues.append("措辞不精确（应为'中文字符'，而非'字'）")
    if in_range:
        score += 2
    else:
        issues.append(f"实际 {actual:,} 字超出 17,000-23,000 范围")
    if declared_match_ok:
        score += 1
    elif declared:
        issues.append(f"声明 {declared:,} 字与实际相差 {abs(declared - actual):,}")

    passed = score >= 5
    if passed:
        return CheckResult(
            "字数声明", "META", True, 5, 5,
            message=f"实际 {actual:,} 中文字符" + (f"，声明 {declared:,}" if declared else "")
        )
    return CheckResult(
        "字数声明", "META", False, score, 5,
        "; ".join(issues), "改用'X 中文字符（含表格与代码块）'格式声明"
    )


# ============================================================
# STRUCT · 结构校验（20 分）
# ============================================================

def check_chapter_sequence(text: str) -> CheckResult:
    """检查 1→15 章连续无重号"""
    # 匹配 "## 一、" 到 "## 十五、" 的章节标题
    expected = ['一', '二', '三', '四', '五', '六', '七', '八', '九',
                '十', '十一', '十二', '十三', '十四', '十五']
    found = []
    for cn in expected:
        pattern = rf'^##\s+{re.escape(cn)}、'
        if re.search(pattern, text, re.MULTILINE):
            found.append(cn)
    if len(found) == 15:
        return CheckResult("章节连续 1→15", "STRUCT", True, 10, 10)
    missing = [c for c in expected if c not in found]
    extra = [c for c in found if c not in expected]
    msg = f"缺失章节：{missing}" if missing else ""
    if extra:
        msg += f" 异常章节：{extra}"
    return CheckResult("章节连续 1→15", "STRUCT", False, 0, 10,
                       msg or f"仅找到 {len(found)}/15 章",
                       "确保引言后按 一→十五 顺序排列，无跳号")


def check_ch13_order(text: str) -> CheckResult:
    """#4 第十三章 13.5→13.9 子节顺序（v3.2 接受多套措辞）"""
    # v3.2 升级：每个子节接受多个关键词（避免措辞差异导致误报）
    expected_order = [
        ('13.5', r'家庭决策会议|家庭会议|家庭'),
        ('13.6', r'第一步行动|行动清单|90\s*天行动|90天行动'),
        ('13.7', r'给你独特建议|独特建议|差异化|差异化卖点|护城河'),
        ('13.8', r'紧迫提醒|三个紧迫|紧迫|紧迫性'),
        ('13.9', r'南沙|本地|目标客户|本范本|客户范本'),  # 本地名可能不同
    ]

    # 找到第十三章的范围
    m13_start = re.search(r'##\s*十三、', text)
    m13_end = re.search(r'##\s*十四、', text)
    if not m13_start or not m13_end:
        return CheckResult("第十三章顺序", "STRUCT", False, 0, 10,
                           "未找到第十三章或第十四章边界", "确保 1→15 章节连续")

    ch13 = text[m13_start.start():m13_end.start()]

    positions = []
    for num, keyword in expected_order:
        # v3.2 升级：keyword 是 regex（已含 | 或其他元字符），直接编译不再 re.escape
        # 必须以 ### 13.X 开头（避免误匹配正文中的关键词）
        pat = rf'###\s+{re.escape(num)}[\S\s]{{0,100}}{keyword}'
        match = re.search(pat, ch13)
        if match:
            positions.append((num, match.start()))
        else:
            return CheckResult("第十三章顺序", "STRUCT", False, 0, 10,
                               f"未找到 {num}（{keyword}）",
                               f"按 13.5 家庭会议 / 13.6 行动 / 13.7 独特 / 13.8 紧迫 / 13.9 本地 顺序排列")

    # 检查顺序是否递增
    sorted_positions = sorted(positions, key=lambda x: x[1])
    actual_order = [p[0] for p in sorted_positions]
    expected_nums = [e[0] for e in expected_order]

    if actual_order == expected_nums:
        return CheckResult("第十三章顺序", "STRUCT", True, 10, 10)
    return CheckResult("第十三章顺序", "STRUCT", False, 0, 10,
                       f"实际顺序 {actual_order} ≠ 模板 {expected_nums}",
                       "重排为 13.5 家庭会议 → 13.6 行动 → 13.7 独特 → 13.8 紧迫 → 13.9 本地")


def check_no_opc_table_duplicate(text: str) -> CheckResult:
    """v3.2 新增：检查 OPC 主表副本残留
    常见问题：agent 在优化过程中误把 OPC 主表内容（一~十二章 + 完整 13.5-13.9）重复粘贴到 OPC 推荐文档末尾
    检测策略：相同章节编号出现 ≥ 3 次才算重复（如「## 一、」出现 3 次）；相似度阈值 0.92
    """
    # 找出所有"## 一、"或"## 二、"开头位置（章节一级标题），并按编号分组
    chapter_positions = {}  # {'一': [pos1, pos2, ...], '二': [...]}
    for m in re.finditer(r'^##\s+([一二三四五六七八九十]+)、', text, re.MULTILINE):
        num = m.group(1)
        chapter_positions.setdefault(num, []).append(m.start())

    # 找出编号出现 ≥ 3 次的章节（一/二/三/四 等正常章节通常只出现 1-2 次）
    duplicates = []
    for num, positions in chapter_positions.items():
        if len(positions) >= 3:
            # 比较这些重复位置的内容相似度
            chunks = [text[p:p + 200] for p in positions]
            from difflib import SequenceMatcher
            for i in range(1, len(chunks)):
                sim = SequenceMatcher(None, chunks[0][:100], chunks[i][:100]).ratio()
                if sim > 0.92:
                    duplicates.append((num, len(positions), round(sim, 2)))

    if duplicates:
        return CheckResult("OPC 主表副本", "STRUCT", False, 0, 5,
                           f"检测到 OPC 主表副本残留：章节 {duplicates[0][0]} 出现 {duplicates[0][1]} 次（相似度 {duplicates[0][2]}）",
                           "删除重复的 OPC 主表副本（一~十二章 + 13.5-13.9 重复段，如「对 38 岁南沙+300 万房贷」）")
    return CheckResult("OPC 主表副本", "STRUCT", True, 5, 5)


# ============================================================
# P0 · 5 项核心优化（60 分）
# ============================================================

def check_p0_1_reader_filter(text: str) -> CheckResult:
    """P0-1 读者筛选 ✅/⚠️/❌ 三档（v3.2 兼容 Markdown 加粗写法）"""
    # v3.2 升级：接受 ✅/⚠️/❌ 后接 ** 加粗（兼容多种写法）
    # 匹配模式：✅ [可选 **] 强烈适合 [可选 你/你：
    has_strong = bool(re.search(r'✅\s*\**\s*强烈适合', text))
    has_partial = bool(re.search(r'⚠️\s*\**\s*部分适合', text))
    has_no = bool(re.search(r'❌\s*\**\s*不适合', text))
    if has_strong and has_partial and has_no:
        return CheckResult("P0-1 读者筛选", "P0", True, 12, 12)
    missing = []
    if not has_strong: missing.append("✅ 强烈适合")
    if not has_partial: missing.append("⚠️ 部分适合")
    if not has_no: missing.append("❌ 不适合")
    return CheckResult("P0-1 读者筛选", "P0", False, 0, 12,
                       f"缺失：{missing}",
                       "引言开头加 ✅/⚠️/❌ 三档读者筛选（兼容 ✅ **强烈适合** 加粗写法）")


def check_p0_2_number_distribution(text: str) -> CheckResult:
    """P0-2 数字分布 · 业绩基线必须有 中位数 + 25/75 分位 + 拒单率"""
    has_median = bool(re.search(r'中位数\s*[\d.]+', text))
    has_p25 = bool(re.search(r'25\s*%?\s*分位|25%分位|25 分位', text))
    has_p75 = bool(re.search(r'75\s*%?\s*分位|75%分位|75 分位', text))
    has_rejection = bool(re.search(r'拒单率', text))
    has_distribution_chart = bool(re.search(r'█', text))  # ASCII 信息图

    score = 0
    issues = []
    if has_median: score += 3
    else: issues.append("中位数")
    if has_p25: score += 3
    else: issues.append("25 分位")
    if has_p75: score += 3
    else: issues.append("75 分位")
    if has_rejection: score += 2
    else: issues.append("拒单率")
    if has_distribution_chart: score += 1
    else: issues.append("收入分布 ASCII 图")

    if score >= 10:
        return CheckResult("P0-2 数字分布", "P0", True, 12, 12)
    return CheckResult("P0-2 数字分布", "P0", False, score, 12,
                       f"缺失：{issues}", "业绩基线加中位数 + 25/75 分位 + 拒单率 + ASCII 图")


def check_p0_3_local_customers(text: str) -> CheckResult:
    """P0-3 本地 20 客户范本 · 至少 15 家虚拟客户 + cold call 话术"""
    # 计数表格行中的虚拟公司画像
    customer_section = re.search(r'13\.9[\s\S]*?(?=##\s+十四|##\s+附录|$)', text)
    if not customer_section:
        # 退而求其次：搜索整个文档的本地客户小节
        customer_section_text = text
        # 至少找到 "本地" + "客户" 关键词
        if '本地' not in text and '客户' not in text:
            return CheckResult("P0-3 本地 20 客户", "P0", False, 0, 12,
                               "未找到本地客户小节", "第十三章末尾加本地 20 客户范本")
    else:
        customer_section_text = customer_section.group(0)

    # 至少 15 行表格中的客户（每行 1 个虚拟公司）
    # 简单启发式：匹配"虚拟公司画像"或"| 1 |"到"| 20 |"
    has_table = bool(re.search(r'\|\s*\d+\s*\|', customer_section_text))
    has_cold_call = bool(re.search(r'cold\s*call|coldcall|冷电话|陌生拜访', text, re.IGNORECASE))
    has_industry_group = len(re.findall(r'13\.9\.\d+|13\.9\s+\d+\s+类', text)) >= 3

    score = 0
    issues = []
    if has_table: score += 6
    else: issues.append("客户表格")
    if has_cold_call: score += 4
    else: issues.append("cold call 话术")
    if has_industry_group: score += 2
    else: issues.append("按行业分组")

    if score >= 10:
        return CheckResult("P0-3 本地 20 客户", "P0", True, 12, 12)
    return CheckResult("P0-3 本地 20 客户", "P0", False, score, 12,
                       f"缺失：{issues}", "13.9 加 20 家本地客户范本 + cold call 话术 + 行业分组")


def check_p0_4_four_scenarios(text: str) -> CheckResult:
    """P0-4 4 方案现金流对比 + 最坏兜底"""
    # 查找 "A. 兼职 / B. 周末 / C. 全职 / D. 合伙" 或类似 4 方案
    has_4_scenarios = bool(re.search(r'方案\s*[ABCD]', text)) or \
                      bool(re.search(r'[ABCD][、. ]\s*(兼职|周末|全职|合伙|轻|中|高)', text))
    has_worst_case = bool(re.search(r'最坏情况|最坏兜底|连续\s*6\s*月\s*0\s*收入|启动期.*0\s*收入', text))
    has_emergency = bool(re.search(r'退路\s*[A-D]|[1-4]\b', text)) or \
                    bool(re.search(r'副业组合|外包过渡|退回职场', text))

    score = 0
    issues = []
    if has_4_scenarios: score += 5
    else: issues.append("4 方案对比表")
    if has_worst_case: score += 4
    else: issues.append("最坏情况兜底")
    if has_emergency: score += 3
    else: issues.append("退路预案")

    if score >= 10:
        return CheckResult("P0-4 4 方案现金流", "P0", True, 12, 12)
    return CheckResult("P0-4 4 方案现金流", "P0", False, score, 12,
                       f"缺失：{issues}", "13.4 加 4 方案对比 + 最坏情况 + 退路预案")


def check_p0_5_failure_cases(text: str) -> CheckResult:
    """P0-5 失败案例与退出机制 · 至少 2 个失败案例 + 退出机制"""
    has_failure_section = bool(re.search(r'10\.4|失败案例', text))
    # 至少出现 2 次"失败案例"
    failure_count = len(re.findall(r'失败案例\s*[12]', text))
    has_exit_mechanism = bool(re.search(r'退出机制|暂停接单|重新启动.*硬筛', text))
    has_comparison_table = bool(re.search(r'失败案例.*vs.*成功案例|失败.*vs.*成功', text))

    score = 0
    issues = []
    if has_failure_section: score += 3
    else: issues.append("10.4 失败案例章节")
    if failure_count >= 2: score += 4
    else: issues.append(f"2 个失败案例（当前 {failure_count}）")
    if has_exit_mechanism: score += 3
    else: issues.append("退出机制 4 步")
    if has_comparison_table: score += 2
    else: issues.append("失败 vs 成功对比表")

    if score >= 10:
        return CheckResult("P0-5 失败案例", "P0", True, 12, 12)
    return CheckResult("P0-5 失败案例", "P0", False, score, 12,
                       f"缺失：{issues}", "10.4 加 2 个失败案例 + 退出机制 + 对比表")


# ============================================================
# P1 · 5 项重要优化（25 分）
# ============================================================

def check_p1_6_customer_quotes(text: str) -> CheckResult:
    """P1-6 客户原话 · 每个案例至少 3 条实战访谈"""
    quote_count = len(re.findall(r'客户\s*[A-Z\d]|客户\s*[一-鿿]', text))
    has_quote_format = bool(re.search(r'"|"|「', text))
    return CheckResult(
        "P1-6 客户原话",
        "P1",
        quote_count >= 9 and has_quote_format,  # 3 案例 × 3 条
        5 if quote_count >= 9 and has_quote_format else min(quote_count // 2, 4),
        5,
        f"客户原话计数 {quote_count}（建议 ≥9）",
        "每案例加 3 条客户原话或同行访谈"
    )


def check_p1_7_tool_diary(text: str) -> CheckResult:
    """P1-7 工具上手真实日记 · D1/D7/D14/D30"""
    has_diary_section = bool(re.search(r'工具上手真实日记|工具.*上手日记', text))
    has_d1 = bool(re.search(r'\bD1\b', text))
    has_d7 = bool(re.search(r'\bD7\b', text))
    has_d14 = bool(re.search(r'D14', text))
    has_d30 = bool(re.search(r'D30', text))
    has_learning_curve = bool(re.search(r'学习曲线', text))

    score = 0
    issues = []
    if has_diary_section: score += 1
    else: issues.append("工具上手日记章节")
    if all([has_d1, has_d7, has_d14, has_d30]): score += 3
    else:
        for tag, present in [("D1", has_d1), ("D7", has_d7), ("D14", has_d14), ("D30", has_d30)]:
            if not present: issues.append(tag)
    if has_learning_curve: score += 1
    else: issues.append("学习曲线")

    if score >= 4:
        return CheckResult("P1-7 工具上手日记", "P1", True, 5, 5)
    return CheckResult("P1-7 工具上手日记", "P1", False, score, 5,
                       f"缺失：{issues}", "14.2 加 3 个工具 × D1/D7/D14/D30 上手日记")


def check_p1_8_legal_compliance(text: str) -> CheckResult:
    """P1-8 9.5 法律合规清单 · 8 条 + 红线检查 + 应急"""
    has_95_section = bool(re.search(r'9\.5', text))
    compliance_count = len(re.findall(r'\|\s*\d+\s*\|[^|]+\|[^|]+\|[^|]+\|', text))
    has_red_line = bool(re.search(r'合规红线|红线检查', text))
    has_emergency = bool(re.search(r'合规应急|应急流程', text))

    score = 0
    issues = []
    if has_95_section: score += 1
    else: issues.append("9.5 章节")
    if compliance_count >= 8: score += 2
    else: issues.append(f"8 条合规事项（当前 {compliance_count}）")
    if has_red_line: score += 1
    else: issues.append("红线检查清单")
    if has_emergency: score += 1
    else: issues.append("应急流程")

    if score >= 4:
        return CheckResult("P1-8 法律合规", "P1", True, 5, 5)
    return CheckResult("P1-8 法律合规", "P1", False, score, 5,
                       f"缺失：{issues}", "9.5 加 8 条合规事项 + 红线检查 + 应急流程")


def check_p1_9_family_meeting(text: str) -> CheckResult:
    """P1-9 家庭决策会议 · 4 项共识 + 4 步沟通 + 应急金 4 级"""
    has_meeting_section = bool(re.search(r'家庭决策会议|家庭会议', text))
    has_4_consensus = bool(re.search(r'4\s*项.*共识|4\s*项硬共识', text))
    has_4_steps = bool(re.search(r'4\s*步.*沟通|沟通脚本|第一步.*第二步.*第三步.*第四步', text))
    has_4_levels = bool(re.search(r'应急金.*4\s*级|🟢.*🟡.*🟠.*🔴', text))

    score = 0
    issues = []
    if has_meeting_section: score += 1
    else: issues.append("家庭决策会议章节")
    if has_4_consensus: score += 2
    else: issues.append("4 项共识")
    if has_4_steps: score += 1
    else: issues.append("4 步沟通脚本")
    if has_4_levels: score += 1
    else: issues.append("应急金 4 级")

    if score >= 4:
        return CheckResult("P1-9 家庭会议", "P1", True, 5, 5)
    return CheckResult("P1-9 家庭会议", "P1", False, score, 5,
                       f"缺失：{issues}", "13.5 加 4 项共识 + 4 步沟通 + 应急金 4 级")


def check_p1_10_score_basis(text: str) -> CheckResult:
    """P1-10 评分依据原始数据 · 附录 1"""
    has_appendix_1 = bool(re.search(r'附录\s*1|附录一|评分依据', text))
    has_d_basis = bool(re.search(r'D\s*=\s*[1-5].*评分依据|D\s*=\s*[1-5].*依据|D\s*=\s*\d+[\s\S]{0,100}评分逻辑', text))
    has_r_basis = bool(re.search(r'R\s*=\s*[1-5].*评分依据|R\s*=\s*\d+[\s\S]{0,100}评分逻辑', text))
    has_m_basis = bool(re.search(r'M\s*=\s*[1-5].*评分依据|M\s*=\s*\d+[\s\S]{0,100}评分逻辑', text))

    score = 0
    issues = []
    if has_appendix_1: score += 1
    else: issues.append("附录 1")
    if all([has_d_basis, has_r_basis, has_m_basis]): score += 4
    else:
        for k, p in [("D", has_d_basis), ("R", has_r_basis), ("M", has_m_basis)]:
            if not p: issues.append(f"{k} 评分依据")

    if score >= 4:
        return CheckResult("P1-10 评分依据", "P1", True, 5, 5)
    return CheckResult("P1-10 评分依据", "P1", False, score, 5,
                       f"缺失：{issues}", "附录 1 加 D/R/M 每个数值的 4-5 个数据点")


# ============================================================
# P2 · 4 项加分优化（15 分）
# ============================================================

def check_p2_11_90day(text: str) -> CheckResult:
    """P2-11 90 天行动清单 · W1-W12 + 5 项生死线"""
    has_90d = bool(re.search(r'90\s*天行动清单|90\s*Day|90d', text, re.IGNORECASE))
    has_w1_w12 = bool(re.search(r'W1-W12|W1[–—~]W12|第\s*1\s*月.*第\s*2\s*月.*第\s*3\s*月', text))
    has_death_line = bool(re.search(r'生死线', text))
    has_5_lines = len(re.findall(r'W\d+|M\d+.*生死线|生死线.*[WMP]\d+', text)) >= 5

    score = 0
    issues = []
    if has_90d: score += 1
    else: issues.append("90 天行动清单")
    if has_w1_w12: score += 1
    else: issues.append("W1-W12 拆解")
    if has_death_line: score += 1
    else: issues.append("生死线")
    if has_5_lines: score += 0.75
    else: issues.append("5 项生死线")

    if score >= 3.5:
        return CheckResult("P2-11 90 天清单", "P2", True, 3.75, 3.75)
    return CheckResult("P2-11 90 天清单", "P2", False, score, 3.75,
                       f"缺失：{issues}", "13.6.1 或 ★ 段加 W1-W12 拆解 + 5 项生死线")


def check_p2_12_citation_groups(text: str) -> CheckResult:
    """P2-12 引用源 A/B/C/D/E 5 组分组"""
    has_chapter_15 = bool(re.search(r'##\s*十五、', text))
    has_group_a = bool(re.search(r'A\s*组.*法规', text))
    has_group_b = bool(re.search(r'B\s*组.*报告|咨询报告', text))
    has_group_c = bool(re.search(r'C\s*组.*区域|官方数据', text))
    has_group_d = bool(re.search(r'D\s*组.*工具', text))
    has_group_e = bool(re.search(r'E\s*组.*复核', text))

    score = 0
    issues = []
    if has_chapter_15: score += 0.75
    else: issues.append("第十五章独立成章")
    groups = sum([has_group_a, has_group_b, has_group_c, has_group_d, has_group_e])
    score += (groups / 5) * 3
    if groups < 5:
        missing = []
        if not has_group_a: missing.append("A 法规")
        if not has_group_b: missing.append("B 报告")
        if not has_group_c: missing.append("C 区域")
        if not has_group_d: missing.append("D 工具")
        if not has_group_e: missing.append("E 复核")
        issues.extend(missing)

    if score >= 3.5:
        return CheckResult("P2-12 引用源分组", "P2", True, 3.75, 3.75)
    return CheckResult("P2-12 引用源分组", "P2", False, score, 3.75,
                       f"缺失：{issues}", "第十五章加 A/B/C/D/E 5 组分类")


def check_p2_13_ascii_charts(text: str) -> CheckResult:
    """P2-13 ASCII 信息图 · 决策路径 + 收入分布"""
    has_decision_path = bool(re.search(r'决策路径图|4\s*项硬筛', text))
    has_revenue_chart = bool(re.search(r'█', text))
    has_other_chart = len(re.findall(r'```[\s\S]{20,200}```', text)) >= 3

    score = 0
    if has_decision_path: score += 1.25
    if has_revenue_chart: score += 1.25
    if has_other_chart: score += 1.25

    if score >= 3.5:
        return CheckResult("P2-13 ASCII 信息图", "P2", True, 3.75, 3.75)
    return CheckResult("P2-13 ASCII 信息图", "P2", False, score, 3.75,
                       "至少 2 个 ASCII 信息图（决策路径 + 收入分布）",
                       "决策卡后加决策路径图 + 业绩基线加收入分布图")


def check_p2_14_similar_scenes(text: str) -> CheckResult:
    """P2-14 相近场景跳转 · 附录 2 · 10 个场景"""
    has_appendix_2 = bool(re.search(r'附录\s*2|附录二|相近场景', text))
    scene_count = len(re.findall(r'\|\s*\*?\*?\d+\*?\*?\s*\|', text))
    has_decision_tree = bool(re.search(r'跳转决策树|决策树', text))

    score = 0
    if has_appendix_2: score += 1.25
    if scene_count >= 10: score += 1.25
    else: pass
    if has_decision_tree: score += 1.25

    if score >= 3.5:
        return CheckResult("P2-14 相近场景", "P2", True, 3.75, 3.75)
    return CheckResult("P2-14 相近场景", "P2", False, score, 3.75,
                       "附录 2 加 10 个相近场景 + 跳转决策树",
                       "附录 2 加 10 个相邻赛道 + 决策树")


# ============================================================
# 关键反模式（must-not-have）
# ============================================================

def check_anti_patterns(text: str) -> CheckResult:
    """禁止占位符残留 + 星级与梯队错配 + 章节数错误"""
    issues = []

    # 占位符检测（仅检测明确模板残留，忽略 cold call 等正当脚本占位）
    # "第 N 梯队" / "第 N 章" 等明显是模板残留
    if re.search(r'第\s*[N?X]\s*梯队', text):
        issues.append("'第 N 梯队' 模板残留")
    if re.search(r'第\s*N\s*章(?!节)', text):  # "第 N 章" 但非"第 N 章节"
        issues.append("'第 N 章' 模板残留")
    if re.search(r'#NNN|#\s*N\s*N\s*N|#\?\?\?', text):
        issues.append("编号占位符 #NNN / #??? 残留")
    # TODO / FIXME / TBD 是通用占位符
    if re.search(r'\bTODO\b|\bFIXME\b|\bTBD\b', text):
        for kw in ['TODO', 'FIXME', 'TBD']:
            if re.search(rf'\b{kw}\b', text):
                issues.append(f"占位符 {kw} 残留")

    # 星级与梯队匹配：D4 R3 M4 = 15 → 应为 ⭐⭐⭐（第三梯队 3 星）
    score_pattern = re.search(r'D\s*([1-5])\s*R\s*([1-5])\s*M\s*([1-5])\s*=\s*(\d+)', text)
    if score_pattern:
        d, r, m, total = (int(x) for x in score_pattern.groups())
        expected_total = d + r + 2 * m
        if total != expected_total:
            issues.append(f"D{d} R{r} M{m} = {total}，但 D+R+2M 应为 {expected_total}")
        expected_stars = (
            5 if total >= 18 else
            4 if total >= 16 else
            3 if total >= 14 else
            2 if total >= 12 else 1
        )
        # 查找附近的 ⭐ 数量
        nearby = text[score_pattern.start():score_pattern.start() + 300]
        star_count = nearby.count('⭐')
        if star_count > 0 and star_count != expected_stars:
            issues.append(f"D+R+2M={total} 应显示 {expected_stars}⭐，实际 {star_count}⭐")

    # 章节数描述错误
    if re.search(r'完整\s*14\s*章', text):
        issues.append("'完整 14 章' 应改为 '完整 15 章'")

    if issues:
        return CheckResult("反模式检测", "META", False, 0, 0,
                           "; ".join(issues), "参考 references/forbidden-patterns.md")
    return CheckResult("反模式检测", "META", True, 0, 0, "无占位符/无错配")


# ============================================================
# 表格格式检测（v3.1 升级 · 001 实战反馈）
# ============================================================

def check_table_blank_line(text: str) -> CheckResult:
    """Markdown 表格前必须有空行（避免 '|...|' 被识别为段落文本而不渲染）

    扫描所有 |...| 开头的表格行（| 数量 ≥3），若前一行非空且非标题行 → 报警。
    """
    lines = text.split('\n')
    issues = []  # (行号, 前一行内容)
    in_table = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # 判断是否为表格行：以 | 开头/结尾 且 至少 3 个 |
        is_table_row = (
            (stripped.startswith('|') or stripped.endswith('|'))
            and stripped.count('|') >= 3
        )

        if is_table_row and not in_table:
            # 表格第一行 → 检查前一行
            if i > 1:
                prev = lines[i - 2].strip()
                if prev != '' and not prev.startswith('#') and not prev.startswith('|'):
                    issues.append((i, prev[:50]))
            in_table = True
        elif not is_table_row and in_table:
            in_table = False

    if issues:
        line_nums = ', '.join(f'L{n}' for n, _ in issues[:5])
        return CheckResult(
            "表格前空行", "STRUCT", False, 0, 5,
            f"发现 {len(issues)} 个表格前缺空行（{line_nums}）",
            "在每个 |...| 表格前加一行空行"
        )
    return CheckResult("表格前空行", "STRUCT", True, 5, 5, "所有表格前均有空行")


# ============================================================
# ★ 段字数自洽（v3.1 升级 · 001 实战反馈）
# ============================================================

def check_star_section_count(text: str) -> CheckResult:
    """★ 段字数声明 vs 实际偏差 ≤ 100 字

    ★ 段独立声明"约 X 字"时，必须与实际中文字数一致（偏差 ≤ 100）。
    """
    star_match = re.search(r'## ★ 对.*?(?=\n## |\Z)', text, re.DOTALL)
    if not star_match:
        return CheckResult(
            "★ 段字数自洽", "META", False, 0, 3,
            "未找到 ★ 段（'## ★ 对' 开头）",
            "★ 段是 OPC 文档决策核心，必含"
        )

    star_section = star_match.group()
    actual = count_chinese(star_section)

    # 在 ★ 段内查找字数声明（"约 X 字" / "X 字"）
    declared_match = re.search(r'约?\s*([\d,]+)\s*字', star_section)
    declared = int(declared_match.group(1).replace(',', '')) if declared_match else None

    if declared is None:
        return CheckResult(
            "★ 段字数自洽", "META", True, 3, 3,
            f"★ 段 {actual:,} 字（未声明具体字数）"
        )

    diff = abs(declared - actual)
    if diff <= 100:
        return CheckResult(
            "★ 段字数自洽", "META", True, 3, 3,
            f"★ 段 {actual:,} 字，声明 {declared:,} 字（偏差 {diff}）"
        )

    return CheckResult(
        "★ 段字数自洽", "META", False, 0, 3,
        f"★ 段实际 {actual:,} 字，声明 {declared:,} 字，偏差 {diff}",
        "★ 段字数与实际偏差 > 100，重新统计并更新声明"
    )


# ============================================================
# ★ 段子节顺序（v3.1 升级 · 避免 043 文档 13.5/13.6 错位问题）
# ============================================================

def check_star_section_order(text: str) -> CheckResult:
    """★ 段子节顺序校验（强匹配 → 风险点 → 推荐路径 → ... → 一句话总结）

    v3.1 修复：只匹配 ### 三级标题中的关键词（避免正文中提到"现金流""风险"等
    关键字造成误报）。
    """
    star_match = re.search(r'## ★ 对.*?(?=\n## |\Z)', text, re.DOTALL)
    if not star_match:
        return CheckResult(
            "★ 段子节顺序", "STRUCT", False, 0, 5,
            "未找到 ★ 段，跳过顺序校验",
            "★ 段是 OPC 文档核心，必含"
        )

    star_section = star_match.group()

    # 提取所有 ### 三级标题（带位置）
    heading_pattern = re.compile(r'^###\s+([^\n]+)', re.MULTILINE)
    headings = [(m.start(), m.group(1)) for m in heading_pattern.finditer(star_section)]

    # 子节关键词映射（每个子节匹配 1 个标题）
    expected_keywords = [
        (r'强匹配', 1, '强匹配项'),
        (r'风险', 2, '风险点'),
        (r'推荐路径', 3, '推荐路径'),
        (r'现金流', 4, '现金流规划'),
        (r'家庭决策|家庭共识|配偶', 5, '家庭决策会议'),
        (r'90\s*天|第一步行动', 6, '90 天清单'),
        (r'一句话总结', 7, '一句话总结'),
    ]

    positions = []  # [(order, position, name)]
    for kw_pattern, order, name in expected_keywords:
        for pos, heading_text in headings:
            if re.search(kw_pattern, heading_text):
                positions.append((order, pos, name))
                break  # 只取第一次出现

    if len(positions) < 4:
        return CheckResult(
            "★ 段子节顺序", "STRUCT", False, 0, 5,
            f"★ 段只检测到 {len(positions)}/{len(expected_keywords)} 个核心子节",
            "★ 段需含 强匹配 / 风险 / 路径 / 现金流 / 家庭 / 90天 / 总结"
        )

    # 检查顺序是否单调递增
    positions.sort(key=lambda x: x[1])
    orders_in_order = [p[0] for p in positions]

    is_sorted = all(orders_in_order[i] <= orders_in_order[i + 1] for i in range(len(orders_in_order) - 1))

    if is_sorted:
        return CheckResult(
            "★ 段子节顺序", "STRUCT", True, 5, 5,
            f"★ 段子节顺序正确（{len(positions)}/{len(expected_keywords)} 个核心子节）"
        )

    # 找出顺序错位的子节
    disordered = []
    for i in range(len(orders_in_order) - 1):
        if orders_in_order[i] > orders_in_order[i + 1]:
            disordered.append(
                f"{expected_keywords[orders_in_order[i]-1][2]} 早于 {expected_keywords[orders_in_order[i+1]-1][2]}"
            )

    return CheckResult(
        "★ 段子节顺序", "STRUCT", False, 0, 5,
        f"★ 段子节顺序错位：{'; '.join(disordered[:3])}",
        "★ 段子节应按 强匹配→风险→路径→现金流→家庭→90天→总结 顺序排列"
    )


# ============================================================
# 主入口
# ============================================================

def validate_file(filepath: Path) -> ValidationReport:
    """对单个文件执行全部校验"""
    text = filepath.read_text(encoding='utf-8')
    report = ValidationReport(file=str(filepath))

    # META（10 分）
    report.add(check_title_version(text))
    report.add(check_word_count(text))

    # STRUCT（20 分）
    report.add(check_chapter_sequence(text))
    report.add(check_ch13_order(text))
    report.add(check_no_opc_table_duplicate(text))  # v3.2 新增

    # P0（60 分）
    report.add(check_p0_1_reader_filter(text))
    report.add(check_p0_2_number_distribution(text))
    report.add(check_p0_3_local_customers(text))
    report.add(check_p0_4_four_scenarios(text))
    report.add(check_p0_5_failure_cases(text))

    # P1（25 分）
    report.add(check_p1_6_customer_quotes(text))
    report.add(check_p1_7_tool_diary(text))
    report.add(check_p1_8_legal_compliance(text))
    report.add(check_p1_9_family_meeting(text))
    report.add(check_p1_10_score_basis(text))

    # P2（15 分）
    report.add(check_p2_11_90day(text))
    report.add(check_p2_12_citation_groups(text))
    report.add(check_p2_13_ascii_charts(text))
    report.add(check_p2_14_similar_scenes(text))

    # 反模式（仅警告，不计分）
    report.add(check_anti_patterns(text))

    # v3.1 新增：表格格式 + ★ 段自洽 + ★ 段子节顺序
    report.add(check_table_blank_line(text))
    report.add(check_star_section_count(text))
    report.add(check_star_section_order(text))

    report.compute_tier()
    return report


def print_report(report: ValidationReport, verbose: bool = True):
    """打印单份报告"""
    print("=" * 70)
    print(f"📄 {report.file}")
    print("=" * 70)

    # 按类别分组
    by_category = {}
    for r in report.results:
        by_category.setdefault(r.category, []).append(r)

    category_labels = {
        'META': '📋 元信息',
        'STRUCT': '🏗️ 结构',
        'P0': '🔴 P0 必含项（5 × 12 = 60 分）',
        'P1': '🟡 P1 重要项（5 × 5 = 25 分）',
        'P2': '🟢 P2 加分项（4 × 3.75 = 15 分）',
    }

    for cat in ['META', 'STRUCT', 'P0', 'P1', 'P2']:
        if cat not in by_category:
            continue
        print(f"\n{category_labels[cat]}")
        print("-" * 70)
        for r in by_category[cat]:
            status = "✅" if r.passed else "❌"
            score_str = f"{r.score}/{r.max_score}" if r.max_score > 0 else "—"
            print(f"  {status} {r.name:<25} {score_str:>10}")
            if not r.passed and r.message:
                print(f"     └─ {r.message}")
            if not r.passed and r.fix_hint:
                print(f"     💡 {r.fix_hint}")

    print("\n" + "=" * 70)
    actual_max = report.actual_max_score
    pct = report.total_score / actual_max * 100
    print(f"📊 总分: {report.total_score:.2f} / {actual_max} ({pct:.0f}%)")
    print(f"🎯 评级: {report.tier}")
    print("=" * 70)

    # 反模式警告
    anti = next((r for r in report.results if r.name == "反模式检测"), None)
    if anti and not anti.passed:
        print(f"\n⚠️  反模式警告: {anti.message}")


def main():
    parser = argparse.ArgumentParser(
        description='OPC 文档质量校验（v3.0 · 043 质量基线版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python validate_opc.py /path/to/043_xxx.md
  python validate_opc.py --batch /path/to/opc-365/03_一人公司场景推荐/
        """
    )
    parser.add_argument('path', nargs='?', help='单个 .md 文件路径')
    parser.add_argument('--batch', metavar='DIR', help='批量校验目录下所有 .md 文件')
    parser.add_argument('--quiet', action='store_true', help='仅输出汇总，不显示详细报告')

    args = parser.parse_args()

    if not args.path and not args.batch:
        parser.print_help()
        sys.exit(1)

    files = []
    if args.path:
        p = Path(args.path)
        if not p.exists():
            print(f"❌ 文件不存在: {p}", file=sys.stderr)
            sys.exit(1)
        files.append(p)
    if args.batch:
        d = Path(args.batch)
        if not d.is_dir():
            print(f"❌ 目录不存在: {d}", file=sys.stderr)
            sys.exit(1)
        files.extend(d.glob('**/*.md'))

    if not files:
        print("未找到任何 .md 文件", file=sys.stderr)
        sys.exit(1)

    # 批量模式：只输出汇总
    if args.batch:
        print(f"📁 批量校验: {len(files)} 个文件\n")
        summary = []
        for f in files:
            try:
                report = validate_file(f)
                summary.append((f, report))
                if not args.quiet:
                    print_report(report)
                    print()
            except Exception as e:
                print(f"❌ {f}: 解析失败 - {e}", file=sys.stderr)

        # 汇总表
        print("\n" + "=" * 70)
        print("📊 批量汇总")
        print("=" * 70)
        print(f"{'文件':<60} {'分数':>8} {'评级':<20}")
        print("-" * 70)
        for f, r in summary:
            pct = r.total_score / r.max_score * 100
            print(f"{f.name:<60} {pct:>6.0f}%  {r.tier:<20}")

        # 退出码
        any_fail = any(r.tier.startswith("FAIL") for _, r in summary)
        any_warn = any(r.tier.startswith("NEEDS") for _, r in summary)
        if any_fail:
            sys.exit(1)
        elif any_warn:
            sys.exit(2)
        sys.exit(0)

    # 单文件模式
    report = validate_file(files[0])
    print_report(report)

    if report.tier.startswith("FAIL"):
        sys.exit(1)
    elif report.tier.startswith("NEEDS"):
        sys.exit(2)
    sys.exit(0)


if __name__ == '__main__':
    main()
