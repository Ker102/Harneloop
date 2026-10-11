<a id="core-lifecycle"></a>
# 核心生命周期

<a id="harness-unit"></a>
## Harness 单元

harness 单元是一个可移植目录，包含可复用的 harness 材料和框架控制文件。

必需文件：

```text
unit/
  unit.yaml
  UNIT_AGENT.md
  operational-map.md
  candidates/
  versions/
  provenance/
```

`operational-map.md` 是单元内的导航文档，记录代理的当前理解：单元要改进什么、目标环境如何使用、哪些产物或证据有用、通常如何运行与重置、操作代理的能力缺口、单元或目标代理工具、已知脆弱点、假设、未决问题及既有证据的位置。它应引导代理，而不是成为僵硬流程。

常见可选目录：

```text
agent-facing/
observers/
validators/
regression-cases/
infrastructure/
exports/
tools/
memory/
experiments/
```

<a id="candidates"></a>
## 候选项

候选是一批连贯变更或一个假设，不是单次文件编辑或 Git 提交。应一起测试和提升的相关设置、工具、指令或验证器变更可积累在同一候选中。针对独立问题，代理可同时保留多个候选，例如目标 harness 改进和独立的评估修复。

```text
candidates/cand-0001/
  candidate.yaml
  rationale.md
  changes/
  validation/
  evidence/
  notes.md
```

候选变更通过框架应用。候选覆盖层不能编辑 `unit.yaml`、`versions/`、`provenance/`、`.evolve/` 或 `candidates/` 等受保护路径。

当前每个候选声明：

- 影响层面：`target_harness`、`evaluation`、`infrastructure` 或 `mixed`；
- 验证层级：`structural`、`targeted`、`representative` 或 `full`；
- 生命周期阶段：`accumulating`、`ready`、`validating`、`needs_rebase`、`promoted` 或 `rejected`；
- 它基于的已提升 harness 版本。

验证与风险成比例。仅元数据变更适合结构检查；独立基础设施或评估器修复适合定向检查；改变 harness 行为的工作适合代表性运行。完整回归套件用于广泛变更和发布检查点。代理可以选择更强层级，但不应为每次增量设置修改重跑整个产物基准。

评估与目标 harness 的变更通常应使用独立候选，以免修改过的评判者成为修改过的 harness 改善的唯一证据。候选可在积累相关工作时保持 `accumulating`，待足够连贯可验证时再转为 `ready`。

<a id="promotion"></a>
## 提升

提升将一个就绪候选覆盖层应用到 harness 单元，在 `versions/` 下创建可恢复快照，并更新来源记录。即使候选并行开发，已提升版本仍保持线性。

如果两个开放候选共享同一基线，提升一个会将另一个标记为 `needs_rebase`。它的文件与历史保留，但提升前必须与新版本协调并收集新证据。旧证据仍作为来源记录，不能满足新基线版本的门槛。

证据引用在附加时以及提升时再次进行完整性检查。声明的运行和产物必须存在，产物存储文件必须仍存在，直接引用的证据文件也必须存在。叙述性证据可以不包含这些引用。

<a id="run-integrity"></a>
## 运行完整性

运行仅在状态为 `running` 时可修改，此时可附加产物。第一次成功的 `run finish` 转换是终态；之后添加产物和重复结束都会被拒绝，防止悄悄改写原始结果。

<a id="rollback"></a>
## 回滚

回滚恢复先前已提升的快照。它应是带有来源记录的框架操作，而不是手工复制。

<a id="wait-and-stop"></a>
## 等待与停止

运行生命周期支持显式等待和停止。

等待涵盖产物延迟、人工审查、排队任务、冷却期和基础设施重建。

停止涵盖证据充分、进展停滞、能力边界问题、权限需求，以及下一有用步骤依赖人或外部系统的情况。

完整的产物感知演化循环见 [Harneloop 的工作方式](../framework-process.md)。
