# Agent Skills

这是一个用于收集和管理 AI Skills 的仓库。当前已整理两个技能目录，分别放在 `skills/` 下，方便统一维护、浏览和调用。

## 已收录的 Skill

### 1. draw-ui

- 仓库：`czshh0628/draw-ui`
- 位置：`skills/draw-ui`
- 作用：用于设计 App、后台、游戏界面和完整网站落地页；也支持把已有截图或设计稿还原成 HTML/CSS、现有前端项目或微信小程序页面。
- 适用场景：页面设计、UI 视觉构思、截图还原、落地页生成。

### 2. prompt-polishing

- 仓库：`czshh0628/prompt-polishing`
- 位置：`skills/prompt-polishing`
- 作用：用于把简短、含糊或不规范的需求润色成更清晰、可执行、适合 Coding Agent 理解的提示词。
- 适用场景：提示词优化、需求整理、任务描述重构。

## 目录结构

```text
skills/
├── draw-ui/
│   ├── README.md
│   ├── SKILL.md
│   └── ...
├── prompt-polishing/
│   ├── README.md
│   ├── SKILL.md
│   └── ...
└── ...
```

## 使用方式

- 每个技能都保留了独立的 README 和 SKILL.md，方便直接查看说明。
- 这个仓库本身是 skills 目录的总入口，后续可继续添加更多技能。
- 如需在某个 AI/Agent 平台中使用这些 skill，可以直接引用对应目录中的 skill 定义和说明文件。

## 说明

该仓库的定位是“技能集合”，每个子目录都是一个独立的 Skill 工程。当前已放入两项内容，后续如果有新的能力，也可以继续往 `skills/` 里扩展。
