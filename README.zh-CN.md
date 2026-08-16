# Agent Skills

[English](README.md)

面向 Codex 风格和项目级 AI 工作流的可复用 Skills。本仓库原名为 `codex-skills`，当前项目名称为 **Agent Skills**。

## 包含内容

请求符合 Skill 描述时，Codex 可以自动选择已安装的 Skill。如需明确指定，请在提示词中写出 `$skill-name`。使用下面的示例时，将方括号内容替换为你的实际任务。

| Skill | 路径 | 用途 | 实用指南 |
| --- | --- | --- | --- |
| Frontend UI Design | `skills/frontend-ui-design/SKILL.md` | 将产品目标和设计参考转化为可执行的前端 UI 指引。 | **适合：**把想法或产品需求转化为可实施的界面。<br>**示例：**`使用 $frontend-ui-design 为[目标用户]设计[页面或流程]，包含布局、组件、状态、响应式、无障碍和验收清单。`<br>**产出：**UI 规格与实现检查清单。 |
| User Taste | `skills/user-taste/SKILL.md` | 将用户已说明的偏好应用于信息不足的设计与工程判断。 | **适合：**存在多个合理方案，需要按你的既有偏好做选择。<br>**示例：**`使用 $user-taste 评审[设计、代码或方案]，推荐最符合我偏好的选择，并说明冲突和取舍。`<br>**产出：**符合个人偏好且理由清楚的建议。 |
| Luna Subagent Delegation | `skills/luna-subagent-delegation/SKILL.md` | 完整委派运行时：授权门槛、Luna 优先路由、并发安全、任务/结果契约、失败回退和主代理验收。 | **适合：**你明确希望委派任务或并行执行。<br>**示例：**`使用 $luna-subagent-delegation 将[任务]拆成边界清晰、可独立验证的子任务；主代理保留决策、整合和最终验收。`<br>**产出：**Luna 优先、工作隔离，并由主代理验证的结果。 |
| External Agent Onboarding | `skills/external-agent-onboarding/SKILL.md` | 可选附加方案：为 Luna 运行时注册并预检 Claude Code、本地模型、终端 Agent 或自定义 Agent。 | **适合：**接入用户自有执行器；必须与 Luna 核心一起安装或启用。<br>**示例：**`使用 $external-agent-onboarding 为[工作区]配置我的[Claude Code、本地模型或自定义 Agent]执行器；先只读、展示配置差异、运行预检，全部通过后再启用。`<br>**产出：**本地执行器配置、适配器设置和预检报告。 |

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
