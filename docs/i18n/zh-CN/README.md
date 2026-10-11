<div align="center">

<h1><img src="../../assets/harneloop-mark.svg" alt="" width="56" height="56" align="absmiddle" /> Harneloop</h1>

<p>面向 AI 代理、感知产物的 harness 演化。</p>

<p><a href="https://harneloop.kaelux.dev/">网站</a> · <a href="#agent-quick-start">快速开始</a> · <a href="#documentation">文档</a></p>

</div>

<!-- i18n-switcher:start -->
[English](../../../README.md) | [Español](../es/README.md) | 简体中文 | [Français](../fr/README.md) | [日本語](../ja/README.md) | [Deutsch](../de/README.md) | [Português (Brasil)](../pt-BR/README.md)
<!-- i18n-switcher:end -->

**帮助 AI 代理从失败中学习。**

代理可能完成任务并宣称成功，却留下有问题的代码、质量欠佳的渲染图或无法工作的流程。Harneloop 为你现有的代理提供结构化方法，让它检查结果、回顾操作、找出可能的错误并测试更好的做法。

代理改进的是它的 **harness**：模型周围的指令、工具、上下文和检查。模型本身无需重新训练。只有测试支持某项变更后，它才成为工作版本。

<a id="what-can-you-use-it-for"></a>
## 可以用它做什么？

当代理反复犯类似错误，且你能检查其产出时，可以使用 Harneloop。例子包括代码与测试、浏览器流程、生成文档和视觉任务。首个公开案例是使用 ViperMesh 构建 Blender 场景；其他任务类别仍有待测试和贡献。

<a id="how-it-works"></a>
## 工作方式

1. **尝试任务。**保留输出和代理采取的步骤。
2. **检查结果。**检查产物本身，而不是相信代理的完成声明。
3. **回顾过程。**将问题关联到工具调用、缺失上下文、指令或环境决策。
4. **测试改进。**让代理提出变更并重跑相关检查。
5. **保留有效做法。**保留有证据支持的改进及可恢复版本。

<p align="center">
  <a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4">
    <img src="https://harneloop.kaelux.dev/media/harneloop-video-poster.png" alt="观看 Harneloop 的工作方式：从目标到可复用 harness" width="900" />
  </a>
</p>

<p align="center"><a href="https://harneloop.kaelux.dev/media/harneloop-how-it-works.mp4"><img src="../../assets/readme-play.svg" alt="" width="18" height="18" align="absmiddle" /> 观看 Harneloop 的工作方式 - 3:40</a></p>

每类任务都有一个 **harness 单元**：将目标、工具、尝试、证据和改进放在一起的可移植工作区。你可以暂停并稍后继续，而不必从头调查。

<a id="try-harneloop"></a>
## 试用 Harneloop

使用隔离的工具环境[从 PyPI 安装](https://pypi.org/project/harneloop/)：

```bash
uv tool install harneloop
harneloop setup
```

也可在 Python 环境中使用 `python -m pip install harneloop`。要求与源码安装选项见[安装并开始](#install-and-start)。

然后向有相应能力的代理提供仓库链接和要改进的任务。[代理快速开始](#agent-quick-start)含可直接使用的提示词。

**状态：**公开 alpha。核心循环可用；欢迎更广泛的任务验证与贡献。[报告问题或分享用例](https://github.com/Ker102/Harneloop/issues)。

<a id="evidence-from-a-real-case-study"></a>
## 真实案例的证据

Harneloop 被用于开发定制的 ViperMesh harness 单元，处理 Blender 空间推理和场景构建任务。比较将执行模型固定为 **GPT-5.5 High**，对照 **Anthropic x Blender MCP server baseline** 测试演化后的 ViperMesh harness，使 harness 成为主要变化的系统层。

- 在 **7 项中的 6 项**可比实时任务上，ViperMesh 更快，**平均加速 2.534x**。
- 在七对实时渲染结果中，初步中立 LLM 视觉评估提高了 **8.19 分**。
- 在七项可比基准中，执行代理累计 token 使用量**降低 90.91%**，总计约 **175K 对比 1.9M tokens**。

Harneloop 并未自行生成场景。它组织证据与产物循环，暴露弱点、指导工具和 harness 开发，并验证这些变更是否改善基准。方法、局限及完整结果见 [ViperMesh 案例研究](https://kristoferjussmann.me/case-studies/vipermesh)。

这些结果直接提供了实证，表明 Harneloop 的流程可在真实且产物密集的代理环境中发挥作用：执行模型不变，演化后的 harness 在速度、视觉表现和 token 效率方面产生了可测量收益。

<a id="demonstration-vipermesh-mcp"></a>
### 演示：ViperMesh MCP

[观看使用 ViperMesh MCP 演示 Harneloop](https://www.youtube.com/watch?v=bs74QJ6UD5E&t=2s)。

Blender 场景构建是检查代理产出并改进其工具与指令的具体用例。框架介绍见 [Harneloop 案例](https://kristoferjussmann.me/case-studies/harneloop/#harneloop-demo)，测量结果见 [ViperMesh 基准研究](https://kristoferjussmann.me/case-studies/vipermesh/)。[公开 Blender 连接器](https://github.com/Ker102/vipermesh-blender)独立于完整工作室和接受基准测试的 harness 提供。

<a id="start-here"></a>
## 从这里开始

- **通过代理使用 Harneloop：**[代理快速开始](#agent-quick-start)
- **自行安装：**[安装并开始](#install-and-start)
- **了解 harness 单元：**[什么是 harness 单元？](#what-is-a-harness-unit)
- **了解循环：**[简明生命周期](#the-lifecycle-made-simple)
- **实测证据：**[ViperMesh 案例研究](https://kristoferjussmann.me/case-studies/vipermesh)
- **连接真实环境：**[环境设置](#environment-setup)
- **更改默认值：**[配置](#configuration)
- **技术架构：**[核心生命周期](docs/architecture/core-lifecycle.md)、[运行时分层](docs/architecture/runtime-layers.md)和[并发](docs/architecture/concurrency.md)
- **完整代理指令：**[代理入门](docs/agent-onboarding.md)
- **可视化流程：**[工作方式](#how-it-works)、[可编辑精简图](docs/framework-process-compact.md)和[详细框架图](docs/framework-process.md)

<a id="why-harneloop-exists"></a>
## Harneloop 为什么存在

模型常常重复相同的失败，因为一次尝试中的有用经验没有成为工作环境中经过测试的一部分。增大提示词或收集评估分数并不能解决整个问题。

模型只是代理性能的一部分。周围的 harness 决定它看到的上下文、可用工具、与环境的交互、记忆内容、结果检查方式，以及错误能否成为持久改进。对于许多特定任务问题，harness 因而是最有杠杆作用的改进层：无需重新训练模型即可取得显著收益，每项变更仍可检查、测试、撤销和移植。

Harneloop 让这项工作结构化且高效。它不只是积累一次性提示词修改，而是让代理开发多个独立 harness 单元，通过真实尝试测试变更，保留证据和历史，并将每个成功的 harness 作为完整包继续使用或导出。

Harneloop 为操作代理提供受控的改进循环：

- 处理真实任务，而不只是合成基准；
- 捕获渲染图、截图、文件、轨迹、日志、结构化状态或其他产物；
- 从视觉、结构或行为角度检查产物；
- 将欠佳结果追溯到指令、工具、上下文、检索、环境或模型限制；
- 将改进开发为隔离的候选补丁；
- 通过新尝试和回归用例测试候选；
- 仅提升有有效证据支持的变更；
- 保留可恢复版本，并将最终 harness 打包复用。

代理可在 harness 工作区内自由推理和实验。Harneloop 控制完整性敏感边界：记录、受保护状态、证据、提升、快照、回滚和打包。

<details>
<summary>研究背景：为何先改进 harness 而非权重？</summary>

<a id="why-improve-the-harness-before-the-weights"></a>
### 为何先改进 harness 而非权重？

代理接口、检索、工具和迭代反馈方面的研究表明，改变模型周围的系统可在不改变权重的情况下显著改善任务表现。当上下文、检索、工具、反馈或环境交互是主要瓶颈时，harness 层方法可以超过微调，有时幅度很大，同时保留基础模型的通用能力。Harneloop 源于构建代理 harness 时遇到的实际问题；以下工作独立支持其 harness 优先方向：

- [Self-Harness](https://arxiv.org/abs/2606.09498) 发现代理可从执行轨迹中挖掘弱点、提出 harness 变更、通过回归测试验证，并提高三类模型在留出测试上的通过率。
- [SWE-agent](https://arxiv.org/abs/2405.15793) 表明，为任务专门设计的代理—计算机接口显著改善了语言模型浏览仓库、编辑代码和执行测试的能力。
- [Reflexion](https://arxiv.org/abs/2303.11366) 通过试错、语言反馈和情景记忆，而非权重更新，改进代理。
- [Self-Refine](https://arxiv.org/abs/2303.17651) 报告，通过迭代反馈与改进，无需额外训练，在七项评估任务上取得约 20 个百分点的平均绝对提升。
- [Fine-Tuning or Retrieval?](https://aclanthology.org/2024.emnlp-main.15/) 发现，在其评估的知识注入任务中，无论已有还是新知识，RAG 均持续优于无监督微调。
- [Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?](https://arxiv.org/abs/2405.05904) 发现，模型难以通过监督微调获取新的事实知识，且随着学习新知识而更易产生幻觉。

结合 ViperMesh 案例，这支持实用的 harness 优先策略：**先优化 harness、测量结果，只有证据显示 harness 达到有效极限时，才修改模型权重。** harness 变更更易快速检查、撤销、复用与验证，在适用任务上可比权重修改带来更大收益，而无需永久改变基础模型。

这并不证明 harness 总能超过所有可能的微调方法。微调仍可用于行为、风格、延迟、专用表示，或无法在推理时有效提供的能力。强大的 harness 与合适的微调也可互补。

</details>

<a id="what-is-a-harness-unit"></a>
## 什么是 harness 单元？

**harness 单元**是用于改进一类任务的可移植工作区。各单元独立发展，并保留自己的目标定义、环境地图、harness 材料、实验、证据、回归用例和已提升版本。

新单元以如下结构开始：

```text
my-harness-unit/
  unit.yaml                 identity and current version
  UNIT_AGENT.md             instructions for agents entering the unit
  operational-map.md        current understanding of tools, artifacts, and workflow
  target/                   task goal and suggested first tests
  environment/              contract for commands, MCP tools, apps, and artifact paths
  agent-facing/             promoted instructions and context
  tools/                    unit-specific helper tools
  observers/                ways to inspect outputs
  validators/               deterministic or agent-driven checks
  regression-cases/         failures that future candidates should not repeat
  candidates/               isolated proposed harness changes
  runtime/                  local runs and captured artifacts
  versions/                 restorable promoted snapshots
  provenance/               human-readable change history
```

这不是限制性的模板。代理可以添加研究、脚本、检索数据、基础设施声明、记忆、自定义观察器或全新目录。框架只保护让单元可理解、可恢复所必需的文件与生命周期规则。

<a id="portable-unit-versus-local-working-data"></a>
### 可移植单元与本地工作数据

可复用的 harness 材料属于可移植单元；原始轨迹、临时实验、缓存、秘密信息、未提升候选和所有历史渲染图则不属于它。

默认 `thin` 包包含重建或集成 harness 所需的已提升知识与契约。运行证据保留在本地，除非未来打包配置明确包含。

<a id="the-lifecycle-made-simple"></a>
## 简明生命周期

1. **描述目标。**用户说明代理应在哪方面提升。
2. **映射环境。**操作代理发现真实任务如何执行以及有用证据来自哪里。
3. **协调假设。**首次真实运行前，重要上下文须确认、委托，或明确标为推断。
4. **运行基线。**代理在修改 harness 前先尝试任务。
5. **检查并作结论。**评估产物，并明确接受、变更、重跑、请求输入或停止。
6. **必要时创建或扩展候选。**相关变更积累为连贯的隔离批次；独立问题可有并行候选。
7. **按风险验证。**代理使用结构、定向、代表性或完整检查并附加证据。
8. **提升、修订、等待或停止。**有支持的改进成为一个版本；弱候选被修订或拒绝。
9. **导出或打包。**已提升 harness 可应用于编码代理、应用代理或其他兼容环境。

已结束运行不可变。候选证据在附加时及提升时再次检查，因此已删除运行、缺失产物或证据文件不能支持发布。

候选不是每次提交的包装。设置或工具候选可收集多个相关变更并接受定向冒烟测试；改变 harness 行为的候选可能需要真实产物尝试与回归。目标 harness、评估和基础设施可独立推进。一个候选提升后，基于旧版本的并行候选须变基并提供新证据，才能随后提升。

README 顶部的视频解释循环。[精简生命周期文档](docs/framework-process-compact.md)包含可编辑 Mermaid 图；[详细流程图](docs/framework-process.md)涵盖能力缺口、人工输入、等待、停止及完整的产物感知循环。

<a id="what-makes-it-different"></a>
## 有何不同？

<a id="artifact-aware"></a>
### <img src="../../assets/readme-observe.svg" alt="" width="18" height="18" align="absmiddle" /> 感知产物

Harneloop 将产出本身视为证据。代理可检查图像、场景、UI、文档、生成仓库、运行轨迹、数据库状态或其他有用输出，而不是相信自身文字报告。

<a id="harness-building-not-only-scoring"></a>
### <img src="../../assets/readme-improve.svg" alt="" width="18" height="18" align="absmiddle" /> 构建 harness，不只是评分

目的不只是报告代理失败。操作代理诊断失败并开发具体 harness 变更，可涉及提示词、原则、示例、检索、工具、观察器、验证器、回归用例或环境自动化。

<a id="evidence-gated-self-improvement"></a>
### <img src="../../assets/readme-verify.svg" alt="" width="18" height="18" align="absmiddle" /> 以证据为门槛的自我改进

当前代理不能自由重写已提升 harness。它创建候选、测试、附加证据，再通过框架提升。每个已提升版本都可检查和恢复。

<a id="environment-agnostic"></a>
### 不依赖环境

核心不依赖 Blender、SVG、Python 代理或特定模型供应商。单元可使用终端命令、MCP 服务器、浏览器自动化、桌面应用、API、手动步骤或自定义工具接口。

<a id="reasoning-remains-open-ended"></a>
### 推理保持开放

Harneloop 组织生命周期，却不将操作代理变成固定脚本。代理仍选择适合任务的测试、产物、评估策略、工具和停止点。

<a id="agent-quick-start"></a>
## 代理快速开始

Harneloop 主要面向通过与具有文件系统和终端访问权限的代理对话来使用。

向代理提供仓库和类似这样的提示词：

```text
Read this repository's README.md and docs/agent-onboarding.md.
Use Harneloop to create a harness unit that improves an agent at: [describe the task].

Inspect my existing environment before deciding how to test it. Ask only for context
that can materially change the work, and do not silently treat assumptions as confirmed.
Run a baseline, inspect its artifacts, and conclude the attempt before deciding whether
a candidate is needed. Do not promote a candidate without evidence.
```

代理接下来应：

1. 如需，安装 Harneloop 工具并运行 `harneloop doctor`。
2. 阅读 `harneloop onboard --format json` 或[入门指南](docs/agent-onboarding.md)。
3. 创建或继续临时 harness 单元，并检查真实环境。
4. 通过自适应需求收集检查点协调已确认、已委托、推断和未知的上下文。
5. 将当前理解更新到 `operational-map.md`。
6. 执行基线并检查产生的产物。
7. 接受当前 harness 或提出改进前，先为尝试作结论。

<a id="instructions-for-agents-reading-this-repository"></a>
### 给阅读此仓库的代理的指令

如果你是操作代理：

- 不要假定每项任务都有测试命令。
- 不要假定 Harneloop 会替你发现端点、工具、截图或产物路径。
- 进入单元或恢复丢失上下文时，运行 `harneloop brief <unit>` 并阅读 `AGENTS.md`、`UNIT_AGENT.md` 和 `operational-map.md`。
- 单元简报仅适用于该 harness 单元的工作；无关项目工作不在其范围内。
- 使用 `harneloop intake status`，仅提出可能实质影响工作的未决问题。
- 使用 `harneloop candidate list <unit>` 恢复所有开放工作；不要假定单元只能有一个活动候选。
- 将相关变更组成连贯候选，按影响调整验证，而不是每次设置编辑后执行完整基准。
- 尽可能将评估器与目标 harness 的变更分开，保持证据可信。
- 检查真实环境，将其映射到 `target/` 和 `environment/`。
- 当确定性检查无法判断质量时，优先检查真实产物。
- 将自身能力与正在为目标代理设计的工具分开。
- 追求最佳已验证结果，而非全部重建：研究并复用合适的工具、技能、库、示例和既有工作，记录来源并遵守许可、安全、费用和权限边界。
- 将提议的 harness 变更放入候选工作区。
- 对运行、产物、证据、提升、回滚、等待、停止和恢复使用 Harneloop 命令。
- 添加凭证、付费服务、外部访问、安全敏感工具或昂贵基础设施前先询问。
- 假设、产物路径、工具或自动化变化时，更新操作地图。
- 不要在运行结束时就停止：检查产物，并使用 `harneloop attempt conclude` 记录明确决定。

机器可读入门信息可通过以下命令获得：

```bash
harneloop onboard --format json
```

<a id="install-and-start"></a>
## 安装并开始

Harneloop 已[发布到 PyPI](https://pypi.org/project/harneloop/)。通过 [uv](https://docs.astral.sh/uv/getting-started/installation/) 安装为隔离工具，或在 Python 环境中使用 `python -m pip install harneloop`。`harneloop` 命令面向 Windows、macOS 和 Linux。

```bash
uv tool install harneloop
harneloop doctor
harneloop setup
```

未发布的源码构建可使用 `uv tool install git+https://github.com/Ker102/Harneloop.git`。

如果 `uv` 提示工具目录不在 `PATH` 中，运行 `uv tool update-shell` 并打开新终端。使用克隆仓库的贡献者可用 `uv tool install --editable .` 安装当前检出目录；参见[开发环境](docs/development.md)。

`harneloop setup` 打开面向人的引导式 CLI。在终端中不带子命令运行 `harneloop` 会打开更完整的交互菜单。代理可直接使用明确的非交互命令。

有用的初始命令：

```bash
harneloop onboard
harneloop template list
harneloop units list
harneloop settings show
```

通过 `harneloop setup` 或 `harneloop init-unit` 创建的 harness 单元自动注册。已有单元可用以下命令注册一次：

```bash
harneloop units register /path/to/my-unit
```

注册后，从任意目录使用单元 ID 或名称，而不是相对路径：

```bash
harneloop units list
harneloop status my-unit --format markdown
harneloop environment status my-unit
```

<a id="what-the-agent-asks-you"></a>
## 代理会问什么

新单元入门刻意保持简短。代理应收集五项上下文：

1. 这个 harness 应帮助代理在哪方面变得更好？
2. harness 将在哪里使用？
3. 成功由你定义、代理提议，还是在基线后决定？
4. 验证应优先质量、视觉证据、平衡，还是资源效率？
5. 测试环境是否已存在、部分存在，或需要构建？

你无需事先知道完美的测试或产物。适当时，代理应在检查任务与环境后提出方案。只有细节相关时才询问约束、受保护区域、费用限制或人工审查。

<a id="environment-setup"></a>
## 环境设置

Harneloop 记录环境映射；操作代理创建该映射。

CLI 不会自动知道哪个 MCP 工具控制应用、渲染结果保存在哪、浏览器流程如何重置，或哪种数据库状态证明成功。代理必须检查真实工作区并将这些细节关联到 harness 单元。

支持三种设置模式：

| 模式 | 使用场景 | 代理行为 |
|---|---|---|
| `existing` | 任务环境已正常工作 | 连接并记录；不要无故重建 |
| `assisted` | 已有部分组件 | 找出并添加基线所需的最小缺失设置 |
| `managed` | 需要创建环境 | 显式构建并记录基础设施变更 |

环境可由命令、MCP、手动操作驱动，或完全自定义。例如 Blender harness 可使用现有 MCP 服务器，而没有单一运行命令。代理可调用工具、渲染场景、捕获截图与结构化场景状态，再将输出附加到 Harneloop 运行。

详细示例见[环境入门](docs/environment-onboarding.md)。

<a id="configuration"></a>
## 配置

多数用户应从默认值开始。最初有用的配置通常在 harness 单元内部，而非全局设置。

<a id="harness-unit-configuration"></a>
### Harness 单元配置

| 文件或区域 | 何时修改 |
|---|---|
| `operational-map.md` | 工具、产物位置、假设、约束或工作流变化 |
| `target/brief.yaml` | 任务类别、成功定义、预期产物或已知风险变化 |
| `environment/contract.yaml` | 命令、MCP 工具、设置模式、交互模式或输出路径变化 |
| `agent-facing/` | 已测试候选提升新指令或可复用上下文 |
| `observers/` 和 `validators/` | 单元需要更好的产物检查或确定性检查 |
| `regression-cases/` | 发现的失败应在未来迭代中测试 |
| `tools/` 和 `infrastructure/` | 更好表现需要单元专用能力或服务 |

不要手动编辑框架管理的 `.evolve/`、`versions/`、`provenance/`、`runtime/` 或候选元数据。使用 CLI 生命周期命令。

<a id="global-preferences"></a>
### 全局偏好

使用 `harneloop settings show` 查看偏好，修改示例如下：

```bash
harneloop settings set validation.prefer_visual_artifacts true
harneloop settings set agent_behavior.autonomy_level balanced
harneloop settings set runtime.token_efficiency_mode false
```

主要偏好组包括：

- `agent_behavior`：自主性、风险操作确认和提升严格性；
- `validation`：代理决定的验证、视觉产物偏好和资源模式；
- `export`：默认目标适配器和打包配置；
- `runtime`：遥测详细程度、token 效率模式和本地单元注册行为。

在 alpha 中，偏好是 CLI 和操作代理的持久默认值与指导。并非每条引擎命令都已自动强制每项偏好。除非使用明确的开发覆盖选项，否则提升必须有证据。

<a id="example-use-cases"></a>
## 用例示例

- 改进 Blender 或 CAD 代理的空间推理与场景构建。
- 通过审查渲染产物改进 SVG、图像、幻灯片、文档或 UI 生成。
- 为反复出现实现或调试失败的仓库构建编码代理 harness。
- 利用截图、DOM 状态、轨迹和任务结果改进浏览器自动化。
- 为基于 MCP 的代理开发更好的工具选择与恢复行为。
- 演化研究或数据处理流程中的检索、示例、验证器和上下文。
- 构建可复用内部 harness，再导出到 Codex、Cursor 或自定义应用代理。

Harneloop 最适合重复任务、可检查输出且失败可转化为持久改进的场景。对不会复用经验的一次性任务，没有必要使用。

<a id="core-cli-lifecycle"></a>
## CLI 核心生命周期

显式命令面向代理、自动化和技术用户：

```bash
harneloop init-unit ./my-unit --id my-unit --name "My Harness Unit" --template artifact-review
harneloop target set my-unit --task "..." --success "..."
harneloop environment connect my-unit --name "..." --mode existing --description "..."
harneloop attempt plan my-unit --goal "..." --method "..."
harneloop run start my-unit --task "Baseline attempt"
harneloop artifact add my-unit run-0001 ./output.png --kind image
harneloop run finish my-unit run-0001 --status succeeded --summary "Baseline captured"
harneloop candidate create my-unit --summary "Improve artifact construction" --plane target_harness --validation-tier representative
harneloop run start my-unit --task "Test candidate improvement" --candidate-id cand-0001
harneloop artifact add my-unit run-0002 ./improved-output.png --kind image
harneloop run finish my-unit run-0002 --status succeeded --summary "Candidate result captured"
harneloop candidate evidence add my-unit cand-0001 --kind artifact_review --summary "..." --run-id run-0002 --artifact-id artifact-0001 --validation-tier representative
harneloop candidate stage my-unit cand-0001 ready
harneloop promote my-unit cand-0001 --version 0.1.0
harneloop export my-unit --adapter codex
harneloop package my-unit --output ./my-unit-0.1.0.tar.gz
```

此序列仅为示例，而非固定步骤。工具驱动代理可在 `run start` 与 `run finish` 之间执行多种操作、捕获多个产物、创建多个尝试或等待外部结果。

<a id="safety-and-integrity"></a>
## 安全与完整性

- YAML 和 JSON 控制文件以原子方式写入。
- 并发 ID 分配与读—改—写操作使用 harness 本地锁。
- 已结束运行不能修改或再次结束。
- 候选覆盖层不能修改受保护框架状态。
- 证据引用在附加与提升时必须存在。
- 候选证据必须匹配当前基线版本及声明的验证层级。
- 并行候选在其他候选提升后仍保留，但自身提升前须变基并收集新证据。
- 已提升版本保存为可恢复快照。
- 回滚是有记录的框架操作。
- thin 包不含运行数据、候选、缓存和常见秘密文件。

<a id="documentation"></a>
## 文档

- [Harneloop 的工作方式](docs/framework-process.md)
- [代理入门](docs/agent-onboarding.md)
- [环境入门](docs/environment-onboarding.md)
- [核心生命周期](docs/architecture/core-lifecycle.md)
- [运行时分层和未来 Rust 边界](docs/architecture/runtime-layers.md)
- [并发与文件安全](docs/architecture/concurrency.md)
- [产品原则](docs/product-principles.md)
- [本地演示](docs/demo-first-test.md)
- [开发说明](docs/development.md)

<a id="contributing"></a>
## 贡献

欢迎贡献、问题报告和独立的 harness 单元案例。尤其有用的贡献包括：

- 在现有案例之外的任务类别中测试 Harneloop；
- 报告可复现的生命周期、可移植性或代理入门失败；
- 改进目标代理适配器、验证器、打包及跨平台行为；
- 贡献聚焦的文档、示例或回归覆盖。

重大变更前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。架构工作先开 issue，讨论范围和兼容性影响。安全问题应遵循 [SECURITY.md](SECURITY.md)，不要使用公开 issue。

<a id="development"></a>
## 开发

在仓库中运行测试套件：

```bash
python -m unittest discover -s tests
```

项目当前使用 Python 3.11 或更新版本。产品接口稳定后，未来 Rust 运行时可能承担更强的受保护生命周期、打包、文件监视或桌面分发职责。

Harneloop 是 alpha 和公开发布所选的产品名称。包、CLI、harness 单元元数据、文档和仓库均使用同一名称。

<a id="license"></a>
## 许可证

Harneloop 以 [Apache License 2.0](../../../LICENSE) 授权。
