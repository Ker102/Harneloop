<a id="target-and-environment-onboarding"></a>
# 目标与环境入门

Harneloop 不应假定自己拥有用户的测试环境。

也不应暗示 CLI 可自动发现环境。Harneloop 存储映射。入门代理必须检查真实工作区、工具、MCP 服务器、脚本、应用端点、输出目录和产物路径，再将映射写入 harness 单元。

当前工作理解首先记录在 `operational-map.md` 中。持续更新单元改进目标、通常运行与重置方式、有用产物、脆弱假设及仍待调查事项。地图应引导代理，而非将它锁定于单一评估流程。

也记录能力缺口。操作代理可用工具与 harness 单元或目标代理环境设计的工具不同。受限代理可能没有终端、浏览器、文件系统、MCP、包管理器、视觉检查、数据库或网络能力。若缺失能力阻碍或削弱构建循环，记录缺什么、为何重要、可用工具或依赖及替代方案。

框架应先帮助代理理解：

- harness 针对什么任务构建；
- 什么算成功；
- 应收集哪些产物；
- 哪些失败模式重要；
- 是否已有测试环境。

之后代理创建尝试计划。它不是确定性测试命令，而是代理编写的工作流，用于生成和检查与目标任务相关的内容。

<a id="setup-modes"></a>
## 设置模式

<a id="existing"></a>
### 已有环境

用户已有工作环境时使用。

例如：Blender 项目已有运行场景、截图和导出日志的脚本。

代理应通过记录以下内容连接环境：

- 运行命令；
- 产物输出路径；
- 要收集的截图、渲染图、日志或结构化摘要；
- 环境特有说明。

除非检查失败或用户要求，不应重建环境。

代理应减少循环中的重复手工工作。如果重启服务、重置应用、收集产物或准备环境可安全自动化，就实现或记录。若自动化有风险、不明确或昂贵，询问用户。

能力增加应有证据支持。环境允许时可安装、启用或构建低风险本地工具。较大依赖、凭证、付费 API、外部访问、用户账户、网络扩展或安全变更应先提议。

托管或辅助设置不意味着所有组件都从零构建。搜索项目，并在有帮助时查阅外部文档、开源工具、代理技能、库、验证器、数据集、示例和既有 harness 工作。如果维护中的方案能改善预期结果或省去不必要实现，应优先采用。记录来源、相关版本、用途、许可/署名要求、兼容性假设及实测贡献。审查第三方可执行材料，并遵守风险、费用、凭证、外部访问和安全的正常权限边界。

已有环境可由命令或工具驱动。

命令驱动意味着有直接可运行命令。工具驱动意味着代理通过 MCP 服务器、浏览器自动化、设计工具插件或 Blender 插件 API 执行任务。

<a id="assisted"></a>
### 辅助设置

部分环境已有、但需识别缺失组件时使用。

代理应提出运行基线测试并捕获产物所需的最小缺失设置。

<a id="managed"></a>
### 托管设置

Harneloop 或代理需要从零创建更多环境部分时使用。

每项基础设施变更应明确且有证据支持。托管设置以后会有用，但不应成为已正常工作的用户项目的默认模式。

<a id="attempt-plans"></a>
## 尝试计划

很多 harness 任务无法简化为 `run this command`。

目标代理可能需要：

- 使用 MCP 工具；
- 编辑文件；
- 创建场景；
- 构建 UI；
- 运行浏览器；
- 请求模型生成产物；
- 视觉检查输出；
- 导出结构化摘要；
- 决定重要的后续证据。

Harneloop 将其记录为尝试计划：

```powershell
harneloop attempt plan .\unit `
  --goal "Build a Blender scene with a cube on a table." `
  --method "Use Blender MCP tools to create objects, render, and export scene summary." `
  --action "Create table, cube, camera, and light." `
  --action "Render and capture screenshot." `
  --expected-artifact render `
  --expected-artifact scene_summary `
  --success-check "Cube rests on table." `
  --success-check "Objects are visible to camera."
```

随后运行可以引用该尝试：

```powershell
harneloop run start .\unit --task "Baseline Blender spatial scene" --attempt-id attempt-0001
```

产物捕获后，添加观察：

```powershell
harneloop attempt observe .\unit attempt-0001 `
  --run-id run-0001 `
  --outcome failed `
  --summary "Render exists but cube floats above the table." `
  --finding "Likely z-coordinate placement issue."
```

这些观察可转为候选证据或回归用例。

<a id="agent-questions"></a>
## 代理问题

开始真实 harness 时，仅询问缺失信息：

- 目标任务类别是什么？
- 哪些输出产物重要？
- 是否已有工作的测试环境？
- 环境由命令、工具、手动操作驱动，还是自定义？
- 命令驱动时：哪个命令运行测试或任务？
- 工具驱动时：代理使用哪些工具？
- 截图、渲染图、日志或结构化摘要写在哪里？
- 哪些常见失败应成为回归用例？

<a id="blender-case"></a>
## Blender 案例

对于已有 Blender 项目，可能的模式为 `existing`。

交互模式可能是 `mcp`，而非 `command`。

此时可能没有直接测试命令。目标代理通过 Blender MCP 服务器和插件工具修改场景、渲染图像、截图、检查对象或导出场景摘要。

首个集成步骤不是安装 Blender 或创建新运行器，而是将 Harneloop 连接到：

- 现有 MCP/工具接口；
- 代理应使用的工具；
- 渲染图、截图、日志、场景摘要的产物路径；
- 创建场景并捕获产物的基线流程。

示例：

```powershell
harneloop environment connect .\blender-unit `
  --name "Existing Blender MCP environment" `
  --mode existing `
  --interaction-mode mcp `
  --description "Agent interacts with Blender through an MCP server and addon tools." `
  --tool create_object `
  --tool render_scene `
  --tool capture_screenshot `
  --tool export_scene_summary `
  --artifact-path "outputs/renders/*.png" `
  --note "Use MCP tools instead of looking for a single run command."
```

之后 Harneloop 负责记录运行、捕获产物、存储证据和提升 harness 变更。Blender MCP 服务器仍是执行接口。
