<a id="concurrency-and-file-safety"></a>
# 并发与文件安全

代理可能连续快速或并行启动 Harneloop 命令。任何读取控制文件、计算顺序 ID 并写回文件的命令，都必须保护整个读—改—写区段。

<a id="current-rule"></a>
## 当前规则

- 共享生命周期区段使用 harness 单元锁文件。
- 持锁期间重新读取相关 YAML 或 JSON 文件。
- 持锁期间分配下一个顺序 ID。
- 通过原子替换临时文件写入 YAML 和 JSON。
- 仅在文件更新完成后释放锁。

<a id="implemented-locks"></a>
## 已实现的锁

- `runs`：分配运行 ID。
- `run-<id>`：添加产物并结束运行。
- `attempts`：分配尝试 ID。
- `attempt-<id>`：追加尝试观察记录。
- `candidates`：分配候选 ID。
- `candidate-<id>-evidence`：分配证据 ID。
- `lifecycle`：提升候选并回滚版本。
- `state`：更新 `.evolve/state.json` 和派生状态文件。

锁位于 `.evolve/locks/`，这是框架管理的运行状态，不包含在可移植包中。

<a id="rust-runtime-note"></a>
## Rust 运行时说明

目前还不需要 Rust。Python 文件锁和原子替换足以满足 alpha CLI 的需要。待产品接口稳定后，未来的 Rust 运行时可负责更严格的沙箱隔离、进程监督和更可靠的并发文件协调。
