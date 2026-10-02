#!/usr/bin/env python3
"""课程与练习页产物自检——每次产出配对文件后运行：

    python check-lesson.py <课程.html> <练习页.html>

检查项：
  1  两文件存在且非空
  2  公式外链：含 src/katex/ 引用时，所在目录 src/katex/ 三件资产可达
  3  占位残留：无 "{课程标题}" 等未替换占位、无内联占位注释
  4  课程大纲锚点与正文 id 一一对应
  5  练习页题目数 ≤4，每题恰好 4 个选项（radio），含"不知道"末项
  6  有公式外链时渲染调用（renderMathInElement）在位

退出码 0 = 通过；1 = 有问题（逐项打印 ✗ 与原因）。
"""
import io
import os
import re
import sys

KATEX_FILES = ["katex.embed.css", "katex.min.js", "auto-render.min.js"]
PLACEHOLDERS = ["{课程标题}", "{课程主题}", "{N}", "内联 katex", "粘贴内联"]


def check(course_path, quiz_path):
    problems = []

    def item(ok, label, detail=""):
        print(("  ✓ " if ok else "  ✗ ") + label + ("" if ok else " —— " + detail))
        if not ok:
            problems.append(label)

    # 1 存在且非空
    texts = {}
    for p in (course_path, quiz_path):
        ok = os.path.isfile(p) and os.path.getsize(p) > 1024
        item(ok, f"文件就绪：{p}", "不存在或过小（<1KB，疑似半截产出）")
        if ok:
            texts[p] = io.open(p, encoding="utf-8").read()

    if len(texts) != 2:
        return problems

    course, quiz = texts[course_path], texts[quiz_path]

    # 2 公式外链资产
    for name, html in (("课程", course), ("练习页", quiz)):
        base = os.path.dirname(os.path.abspath(
            quiz_path if name == "练习页" else course_path))
        if "src/katex/" in html:
            missing = [f for f in KATEX_FILES
                       if not os.path.isfile(os.path.join(base, "src", "katex", f))]
            item(not missing, f"{name}公式外链资产可达（src/katex/ 三件）",
                 "缺少：" + ", ".join(missing) + "——用 Bash 把技能 assets/katex/ 复制到 lessons/src/katex/")
            has_call = "renderMathInElement" in html
            item(has_call, f"{name}渲染调用在位", "有 src/katex/ 外链但缺 renderMathInElement 调用")
        else:
            print(f"  · {name}无公式外链（纯文字课程），跳过资产检查")

    # 3 占位残留
    for name, html in (("课程", course), ("练习页", quiz)):
        found = [ph for ph in PLACEHOLDERS if ph in html]
        item(not found, f"{name}无占位残留", "残留：" + ", ".join(found))

    # 4 课程锚点
    m = re.search(r'class="toc".*?</nav>', course, re.S)
    if m:
        hrefs = re.findall(r'href="#([^"]+)"', m.group(0))
        ids = set(re.findall(r'<(?:h[234]|section)[^>]*\sid="([^"]+)"', course))
        bad = [h for h in hrefs if h not in ids]
        item(not bad, "课程大纲锚点与正文 id 一致", "失配：" + ", ".join(bad))
    else:
        item(False, "课程含大纲（.toc）", "未找到 .toc 导航——课程应以 template.html 为骨架")

    # 5 题数与选项
    qitems = re.findall(r'<div class="q-item"[^>]*>', quiz)
    item(len(qitems) <= 4, f"练习页题目数 ≤4（实测 {len(qitems)}）")
    radios_per_q = [len(re.findall(r'name="q%d"' % i, quiz)) for i in range(len(qitems))]
    bad_q = [i + 1 for i, n in enumerate(radios_per_q) if n != 4]
    item(not bad_q, "每题恰好 4 个选项", "异常题号：" + ", ".join(map(str, bad_q)))
    item("不知道" in quiz, "选项含\"不知道\"末项")

    return problems


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    print(f"产物自检：{sys.argv[1]} + {sys.argv[2]}")
    problems = check(sys.argv[1], sys.argv[2])
    if problems:
        print(f"\n未通过：{len(problems)} 项 —— 修复后再继续下一小节")
        sys.exit(1)
    print("\n全部通过 —— 可以继续下一小节")


if __name__ == "__main__":
    main()
