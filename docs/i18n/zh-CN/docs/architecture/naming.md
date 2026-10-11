<a id="naming"></a>
# 命名

<a id="selected-term"></a>
## 选定术语

可移植的 harness 对象称为 **harness 单元**。

一个 harness 单元是独立完整的 Harneloop 工作区，包含控制文件、面向代理的指令、候选项、版本、环境契约、运行记录和导出。

<a id="why-this-name"></a>
## 命名原因

`Harness unit` 比 `unit` 更清晰，因为无论出现在哪里，它都体现了用途。该术语也适用于视觉、代码、研究、自动化和应用代理流程，不依赖特定框架。

<a id="usage"></a>
## 用法

在用户界面文本、文档、菜单、提示词和代理指令中使用 **harness 单元**。

暂时保留 `harneloop init-unit` 和 `harneloop units` 等现有命令名，以避免不必要的改动。这些命令管理 harness 单元。

在面向用户的文本中，避免单独使用 `unit`，除非上下文已明确其含义。
