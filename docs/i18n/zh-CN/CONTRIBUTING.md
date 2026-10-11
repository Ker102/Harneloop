<a id="contributing"></a>
# 贡献

Harneloop 目前处于公开 alpha 阶段。在公共 API 和 harness 单元格式逐步稳定期间，欢迎聚焦具体问题的 issue 和贡献。

<a id="development-setup"></a>
## 开发环境

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m unittest discover -s tests
```

在 macOS 或 Linux 上：

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/python -m unittest discover -s tests
```

<a id="pull-requests"></a>
## Pull request

每个 pull request 应限于一种行为或一个架构范围。

进行重大架构工作前，请先提交 issue，以便就问题和兼容性影响达成一致。生命周期变更应包含测试；行为变化时，应更新面向代理的文档。

目前不要请求 CodeRabbit 自动审查。如果创建 PR 时仓库已配置 CodeRabbit，请在请求审查前添加仓库的 CodeRabbit-ignore 标签或标记。

<a id="standards"></a>
## 规范

- 框架核心应保持与任务类别无关。
- 不要在 `src/harneloop` 中引入 Blender 特有的假设。
- 添加或更新生命周期行为测试。
- 面向代理的文件应使用可读的 Markdown、YAML 或 JSON。
- 不要提交秘密信息、本地运行产物、虚拟环境或生成的包。

提交贡献即表示你同意以仓库的 [Apache License 2.0](../../../LICENSE) 授权该贡献。
