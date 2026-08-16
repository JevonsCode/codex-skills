# Agent Skills

[English](README.md)

面向 Codex 风格和项目级 AI 工作流的可复用 Skills。

本仓库原名为 `codex-skills`，当前项目名称为 **Agent Skills**。

## 包含内容

| Skill | 路径 | 用途 |
| --- | --- | --- |
| Frontend UI Design | `skills/frontend-ui-design/SKILL.md` | 将产品目标、设计参考与页面需求转化为可执行的前端 UI 指引。 |\n| User Taste | `skills/user-taste/SKILL.md` | 将用户已说明的偏好与决策风格应用于 UI、架构、产品、代码、写作和设计取舍。 |
| Luna Subagent Delegation | `skills/luna-subagent-delegation/SKILL.md` | 将边界清晰、低风险、可独立验证的工作委派给 Luna Max 子代理，同时由主代理保留规划与最终验证。 |
| External Agent Onboarding | `skills/external-agent-onboarding/SKILL.md` | 指导用户配置 Claude Code、本地模型与其他外部 Agent，用于委派开发、测试和验证。 |

## 委派工作流

两份委派 Skill 可以同时安装：

1. **Luna Subagent Delegation** 处理适合并行、短且自包含的执行工作。
2. **External Agent Onboarding** 注册 Claude Code 等终端 Agent，并将耗时开发、完整测试、深度调试或复杂验证路由给符合条件的外部执行器。

主 Codex Agent 始终保留用户意图理解、架构与权限决策、结果整合和最终验证。

## 外部 Agent 配置

接入向导会在 `~/.codex/executors.yaml` 创建本地执行器配置。该配置记录能力、风险上限、允许操作与审批边界。请勿将机器专属命令、凭据或密钥提交到本仓库。

为了节省 Codex 使用量，同时不浪费外部 Agent 的能力：

- 将长时独立开发、完整测试、深度调试和复杂验证优先交给外部 Agent。
- 将小任务、延迟敏感工作、模糊需求、关键决策和最终验收保留给 Codex。

## 工作名与反馈

被委派的工作者可以使用轻量的虚构标签，例如 `🧑‍💻 林安` 或 `👮 Alex`。标签依据用户已说明或当前可见的语言偏好本地化，不推断用户真实身份。

本地名册会为相同的执行器、角色和语言复用标签。若用户因表现不佳而停用某个标签，Skill 会询问一个具体问题，保存一条简短的避免规则，并不再复用该标签。此功能不会保存角色故事、对话历史或绩效档案。

## 安装

将 Skill 目录复制或软链接到 Agent 运行时的 Skill 目录：

```bash
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/luna-subagent-delegation" ~/.codex/skills/luna-subagent-delegation
```

如需项目级使用，请按照 Agent 运行时的约定，将 Skill 目录复制到项目本地目录，例如 `.codex/skills/` 或 `.agents/skills/`。

## Skill 编写标准

每份 `SKILL.md` 应当：

1. 定义使用场景。
2. 将模糊意图转化为具体产出。
3. 包含决策规则，而不只是描述。
4. 说明交付物、验证方式与约束。
5. 避免使用受保护的品牌资产或声称复刻专有系统。


## 使用 DingDongBuddy 安装

[DingDongBuddy](https://github.com/JevonsCode/DingDongBuddy) 是用于统一管理 Prompt、Skill 和 MCP 连接的本地工具，支持多个 Agent。可在其 Skill 导入流程中，直接粘贴 GitHub Skill 文件夹链接或 `SKILL.md` 链接来安装。

可直接导入以下两份 Skill：

- [Luna 子代理委派](https://github.com/JevonsCode/codex-skills/tree/main/skills/luna-subagent-delegation)
- [外部 Agent 接入向导](https://github.com/JevonsCode/codex-skills/tree/main/skills/external-agent-onboarding)

导入后，可选择全局启用、动态交付，或仅作用于某个项目。机器专属命令和凭据应保留在本地配置中，不要写入共享 Skill。
