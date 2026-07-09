#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @CreateTime : 2026/07/09 21:44
# @Author     : wephiles@wephiles
# @IDE        : PyCharm
# @ProjectName: practice
# @FileName   : practice/process_big_file.py
# @Description: This is description of this script.
# @Interpreter: python 3.0+
# @Motto      : You must take your place in the circle of life!
# @AuthorSite : https://github.com/wephiles or https://gitee.com/wephiles

# Copyright (c) 2026 wephiles.
# This software is licensed under the MIT license.
# See the LICENSE file for details.

import json
import os
import glob
from multiprocessing import Pool, cpu_count

CHUNK_SIZE = 500  # 每个数据块包含的行数，可根据文件大小调整


def process_chunk(args):
    """
    处理一个数据块，按 tag 值分类。
      tag > 500  → 高质量
      tag <= 500 → 低质量
    """
    lines, stem = args
    high_lines = []
    low_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            tag = data.get("tag", 0)
            if tag > 500:
                high_lines.append(line)
            else:
                low_lines.append(line)
        except json.JSONDecodeError:
            # 跳过无法解析的行
            continue
    return stem, high_lines, low_lines


def read_chunks(filepath, stem, chunk_size):
    """生成器：按块读取文件的行，避免一次性加载整个文件到内存"""
    chunk = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            chunk.append(line)
            if len(chunk) >= chunk_size:
                yield (chunk, stem)
                chunk = []
    if chunk:  # 处理文件末尾不足一个块的剩余行
        yield (chunk, stem)


def main():
    # 1. 创建输出目录
    os.makedirs("./data/High", exist_ok=True)
    os.makedirs("./data/Low", exist_ok=True)

    # 2. 查找所有 JSONL 文件
    files = sorted(glob.glob("./data/data-*.jsonl"))
    if not files:
        print("未在 ./data/ 目录下找到 JSONL 文件")
        return

    print(f"找到 {len(files)} 个文件: {[os.path.basename(f) for f in files]}")

    # 3. 收集所有数据块（每个文件按 CHUNK_SIZE 行切分成多个块）
    all_chunks = []
    for filepath in files:
        basename = os.path.basename(filepath)
        stem = os.path.splitext(basename)[0]  # 如 "data-00000"
        for chunk in read_chunks(filepath, stem, CHUNK_SIZE):
            all_chunks.append(chunk)

    print(f"共 {len(all_chunks)} 个数据块待处理")

    # 4. 使用进程池并行处理所有数据块
    results = {}  # stem -> {'high': [], 'low': []}
    num_processes = min(cpu_count(), len(all_chunks)) if all_chunks else 1

    with Pool(processes=num_processes, maxtasksperchild=10) as pool:
        for stem, high_lines, low_lines in pool.imap_unordered(process_chunk, all_chunks):
            if stem not in results:
                results[stem] = {'high': [], 'low': []}
            results[stem]['high'].extend(high_lines)
            results[stem]['low'].extend(low_lines)

    # 5. 将分类结果写入对应的输出文件
    for stem in sorted(results.keys()):
        high_path = os.path.join("./data/High", f"{stem}_high_quality.jsonl")
        low_path = os.path.join("./data/Low", f"{stem}_low_quality.jsonl")

        with open(high_path, 'w', encoding='utf-8') as f:
            for line in results[stem]['high']:
                f.write(line + '\n')

        with open(low_path, 'w', encoding='utf-8') as f:
            for line in results[stem]['low']:
                f.write(line + '\n')

        print(f"  {stem}: 高质量={len(results[stem]['high'])} 条, 低质量={len(results[stem]['low'])} 条")

    print("\n处理完成！")


if __name__ == '__main__':
    main()

# import random
# import json
#
# data_json = {
#     "workbench.colorTheme": "GitHub Dark Default",
#     "workbench.iconTheme": "material-icon-theme",
#     "material-icon-theme.enableLogging": True,
#     "files.autoSave": "afterDelay",
#     "files.autoGuessEncoding": True,
#     "workbench.list.smoothScrolling": True,
#     "editor.cursorSmoothCaretAnimation": "on",
#     "editor.smoothScrolling": True,
#     "editor.cursorBlinking": "smooth",
#     "editor.mouseWheelZoom": True,
#     "editor.formatOnPaste": True,
#     "editor.formatOnType": True,
#     "editor.formatOnSave": True,
#     "editor.wordWrap": "on",
#     "editor.guides.bracketPairs": True,
#     "editor.suggest.snippetsPreventQuickSuggestions": False,
#     "editor.acceptSuggestionOnEnter": "smart",
#     "editor.suggestSelection": "recentlyUsed",
#     "window.dialogStyle": "custom",
#     "debug.showBreakpointsInOverviewRuler": True,
#     "workbench.colorCustomizations": {
#         "terminal.background": "#00000000",
#         "editorPane.background": "#1e1e1e00",
#         "editorGroupHeader.tabsBackground": "#1e1e1e00",
#         "editorGroupHeader.noTabsBackground": "#1e1e1e00",
#         "breadcrumb.background": "#1e1e1e00",
#         "editorGutter.background": "#1e1e1e00",
#         "panel.background": "#1e1e1e00",
#         "panelStickyScroll.background": "#1e1e1e00",
#         "tab.activeBackground": "#1e1e1e00",
#         "tab.unfocusedActiveBackground": "#1e1e1e00",
#         "sideBar.background": "#1e1e1ecc",
#         "sideBarTitle.background": "#1e1e1ecc",
#         "sideBarStickyScroll.background": "#1e1e1ecc",
#         "activityBar.background": "#1e1e1ecc",
#         "editor.background": "#1e1e1ecc",
#         "editorStickyScroll.background": "#1e1e1ecc",
#         "editorStickyScrollGutter.background": "#1e1e1ecc",
#         "tab.inactiveBackground": "#1e1e1ecc",
#         "tab.unfocusedInactiveBackground": "#1e1e1ecc",
#         "inlineChat.background": "#1e1e1ee6",
#         "editorWidget.background": "#1e1e1ee6",
#         "editorHoverWidget.background": "#1e1e1ee6",
#         "editorSuggestWidget.background": "#1e1e1ee6",
#         "notifications.background": "#1e1e1ee6",
#         "notificationCenterHeader.background": "#1e1e1ee6",
#         "menu.background": "#1e1e1ee6",
#         "quickInput.background": "#1e1e1ee6",
#     },
#     "terminal.integrated.gpuAcceleration": "off",
#     "terminal.integrated.fontFamily": "Source Code Pro",
#     "terminal.integrated.fontSize": 16,
#     "terminal.integrated.lineHeight": 1,
#     "window.systemColorTheme": "dark",
#     "window.autoDetectColorScheme": False,
#     "window.controlsStyle": "custom",
#     "editor.fontSize": 15,
#     "editor.fontFamily": "'Source Code Pro', Consolas, 'Courier New', monospace",
#     "diffEditor.codeLens": True,
#     "files.insertFinalNewline": True,
#     "codesnap.showWindowTitle": True,
#     "window.zoomLevel": 1,
#     "chat.tips.enabled": False,
#     "explorer.compactFolders": False,
#     "apc.activityBar": {
#         "position": "bottom",
#         "size": 48,
#     },
#     "Codegeex.Privacy": True,
#     "Codegeex.License": "",
#     "cSpell.userWords": ["Consolas", "wephiles"],
#     "editor.defaultFormatter": "esbenp.prettier-vscode",
#     "[python]": {
#         "editor.defaultFormatter": "ms-python.black-formatter",
#     },
#     "background.enabled": True,
#     "background.fullscreen": {
#         "images": ["E:\\Pictures", "E:\\BackGround"],
#         "opacity": 0.1,
#         "size": "cover",
#         "position": "center",
#         "interval": 3600,
#         "random": True,
#     },
#     "workbench.editorAssociations": {
#         "{git,gitlens,chat-editing-snapshot-text-model,copilot,git-graph,git-graph-3}:/**/*.qrc": "default",
#         "*.copilotmd": "vscode.markdown.preview.editor",
#         "*.png": "gryc.viewer",
#         "*.qrc": "qt-core.qrcEditor",
#     },
#     "Codegeex.Comment.LanguagePreference": "中文",
#     "Codegeex.Chat.LanguagePreference": "中文",
#     "Codegeex.SidebarUI.LanguagePreference": "中文",
#     "Codegeex.OnlyKeyControl": True,
#     "codegeex.codeLens.functionQuickOptions": {
#         "explainCode": False,
#         "ghostComment": False,
#         "fixBug": False,
#         "generateUnitTest": False,
#         "reviewCode": False,
#         "codeOptimization": False,
#         "addDocString": False,
#         "addExceptionHandling": False,
#         "printLogForDebugging": False,
#         "improveRunningEfficiency": False,
#         "renameSymbols": False,
#         "newFileForDebugging": False,
#         "tryANewApproach": False,
#         "addComment": False,
#     },
#     "material-icon-theme.activeIconPack": "angular_ngrx",
#     "background.editor": {
#         "useFront": True,
#         "style": {
#             "background-position": "100% 100%",
#             "background-size": "auto",
#             "opacity": 0.1,
#         },
#         "styles": [{}, {}, {}],
#         "images": ["E:\\Pictures", "E:\\BackGround"],
#         "interval": 0,
#         "random": False,
#     },
#     "editor.inlineSuggest.edits.allowCodeShifting": "never",
#     "github.copilot.nextEditSuggestions.fixes": False,
#     "github.copilot.nextEditSuggestions.extendedRange": False,
#     "github.copilot.nextEditSuggestions.enabled": False,
#     "chat.disableAIFeatures": True,
#     "editor.unicodeHighlight.nonBasicASCII": False,
#     "qt-core.additionalQtPaths": [
#         {
#             "name": "Qt-5.15.2-win32-msvc-x86_64_from_PATH",
#             "path": "E:\\Software\\anaconda3\\Library\\bin\\qtpaths.EXE",
#         },
#     ],
# }
# for i in range(500):
#     with open('./data/data-00003.jsonl', 'a', encoding='utf-8') as fp:
#         data_json['tag'] = random.randint(0, 10_000)
#         fp.write(json.dumps(data_json, ensure_ascii=False) + '\n')
# for i in range(356):
#     with open('./data/data-00004.jsonl', 'a', encoding='utf-8') as fp:
#         data_json['tag'] = random.randint(0, 10_000)
#         fp.write(json.dumps(data_json, ensure_ascii=False) + '\n')
# for i in range(689):
#     with open('./data/data-00005.jsonl', 'a', encoding='utf-8') as fp:
#         data_json['tag'] = random.randint(0, 10_000)
#         fp.write(json.dumps(data_json, ensure_ascii=False) + '\n')
