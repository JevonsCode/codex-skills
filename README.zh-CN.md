# Agent Skills

[English](README.md)

面向 Codex 风格和项目级 AI 工作流的可复用 Skills。本仓库原名为 `codex-skills`，当前项目名称为 **Agent Skills**。

## 包含内容

| Skill | 路径 | 用途 |
| --- | --- | --- |
| Frontend UI Design | `skills/frontend-ui-design/SKILL.md` | 将产品目标和设计参考转化为可执行的前端 UI 指引。 |
| User Taste | `skills/user-taste/SKILL.md` | 将用户已说明的偏好应用于信息不足的设计与工程判断。 |
| Luna Subagent Delegation | `skills/luna-subagent-delegation/SKILL.md` | 完整委派运行时：授权门槛、Luna 优先路由、并发安全、任务/结果契约、失败回退和主代理验收。 |
| External Agent Onboarding | `skills/external-agent-onboarding/SKILL.md` | 可选附加方案：为 Luna 运行时注册并预检 Claude Code、本地模型、终端 Agent 或自定义 Agent。 |

## 委派架构

`luna-subagent-delegation` 是可以独立工作的完整核心 Skill。它默认优先使用原生 Luna；主代理始终保留用户意图理解、架构与权限决策、结果整合、验证和最终回答。

`external-agent-onboarding` 依赖这个核心，只负责增加用户自有的外部执行器，不再重复路由和交接策略：

```text
主代理 → Luna 委派门槛 → 原生 Luna（默认）
                       ↘ 已配置的外部执行器（可选）
```

只有稳定配置、真实适配器、工作区权限匹配和预检都通过，外部执行器才进入候选。仓库内附带 Claude Code 通用适配器，用于将统一任务契约转换为非交互结构化调用并归一化结果；主代理仍须独立验收。

## 自定义配置约定

可选的 `~/.codex/executors.yaml`、Executor Task Contract、结果结构和适配器接口，都是这两份 Skill 自己实现的约定，不是 Codex 原生配置或协议。

机器专属的适配器设置应放在用户本地配置中。不要提交凭据、Token、密码、私人命令历史或个人 Shell 管道。共享配置使用具体的允许、拒绝、审批和工作区边界，拒绝规则优先级最高。

参见：

- [执行器配置约定](skills/external-agent-onboarding/references/executor-profile.md)
- [Claude Code 适配器](skills/external-agent-onboarding/references/claude-code-adapter.md)

## 安装

可以只安装 Luna 核心；如需外部执行器接入，再同时安装两份 Skill：

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/luna-subagent-delegation" ~/.codex/skills/luna-subagent-delegation
ln -s "$PWD/skills/external-agent-onboarding" ~/.codex/skills/external-agent-onboarding
```

如需项目级使用，请按照运行时约定，将 Skill 复制或链接到 `.codex/skills/` 或 `.agents/skills/`。External Agent Onboarding 不应脱离 Luna Subagent Delegation 单独安装。

## Skill 编写标准

每份 `SKILL.md` 应定义触发条件、决策规则、输出、验证和约束。共享 Skill 不应包含个人密钥、命令或未经支持的专有系统声明。

## 使用 DingDongBuddy 安装

[DingDongBuddy](https://github.com/JevonsCode/DingDongBuddy) 用于统一管理多个 Agent 的 Prompt、Skill 和 MCP 连接。可通过 GitHub 文件夹或 `SKILL.md` 链接导入：

- [Luna 子代理委派](https://github.com/JevonsCode/codex-skills/tree/main/skills/luna-subagent-delegation)
- [外部 Agent 接入向导](https://github.com/JevonsCode/codex-skills/tree/main/skills/external-agent-onboarding)

Luna 可以全局、动态或按项目启用；只有需要配置外部执行器时，才在同一作用域同时启用 onboarding。
