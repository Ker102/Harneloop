<a id="development"></a>
# 开发

<a id="repository-layout"></a>
## 仓库结构

```text
src/harneloop/      Python reference implementation
tests/           Unit and behavior tests
docs/            Architecture and development notes
schemas/         Language-neutral data contracts
.github/         CI and repository automation
```

<a id="local-verification"></a>
## 本地验证

将检出目录安装为用户级可编辑工具，只需执行一次：

```powershell
uv tool install --editable .
```

之后，`harneloop` 命令在仓库之外仍然可用，并反映源码更改。运行以下验证：

```powershell
uv run python -m compileall src tests
uv run python -m unittest discover -s tests
harneloop doctor
```

<a id="devops-baseline"></a>
## DevOps 基础

仓库应保持以下内容：

- 使用 `src/` 的源码布局；
- 可重复的本地测试；
- 支持的 Python 版本的 CI；
- 不提交虚拟环境或运行产物；
- 明确的安全与贡献文档；
- 核心记录使用与语言无关的 schema。

<a id="runtime-data"></a>
## 运行数据

运行轨迹、复制的产物、运行记录、尝试计划和实验属于本地工作数据。除非后续打包配置明确包含它们，否则不应将其纳入 thin 可移植包。

<a id="pr-review-note"></a>
## PR 审查说明

早期原型阶段不需要 CodeRabbit 审查。如果创建 PR，请添加已配置的 CodeRabbit-ignore 标签或标记。
