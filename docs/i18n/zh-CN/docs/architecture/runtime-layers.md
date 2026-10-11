<a id="runtime-layers"></a>
# 运行时分层

<a id="current-decision"></a>
## 当前决定

首个参考实现使用 Python。

如果以后 Harneloop 需要受保护的原生运行时，应优先选择 Rust 而非 Go。

<a id="why-rust-later"></a>
## 为什么以后选择 Rust

只有框架需要在以下方面提供更强的本地保证时，才应引入原生层：

- 生命周期完整性；
- 受保护状态边界；
- 版本快照；
- 回滚；
- 内容寻址存储；
- 产物打包；
- 文件监视；
- 子进程监督；
- 桌面打包。

对于这种产品形态，Rust 比 Go 更适合承担受保护内核的角色。

<a id="agent-boundary"></a>
## 代理边界

Rust 不应成为代理开放式设计 harness 的工作区。

代理应继续通过以下方式工作：

- Markdown 指令；
- YAML 和 JSON 清单；
- schema；
- 候选目录；
- CLI 命令；
- 产物契约。

规则仍然是：

> 代理可以在候选内自由探索。引擎控制提升。

<a id="where-go-could-still-fit"></a>
## Go 仍然适用的领域

如果 Harneloop 向这些方向发展，Go 仍适合未来的托管服务、远程工作节点协调或注册表基础设施。
