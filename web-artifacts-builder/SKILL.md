---
name: web-artifacts-builder
description: >
  Web Artifact 构建器 / 复杂交互页面：当用户要生成复杂、多组件、可交互的 HTML Artifact，
  且需要 React、Tailwind CSS、shadcn/ui、状态管理、路由或打包脚本时使用。可用中文唤起：
  “做一个复杂交互页面”“生成 React Artifact”“用 shadcn/ui 做前端 Artifact”“打包成单文件 HTML”。
  不用于简单单文件 HTML/JSX、小组件或只需静态页面的场景。
---

# Web Artifact 构建器（web-artifacts-builder）

## 目标

用 React、Tailwind CSS 和 shadcn/ui 快速构建复杂交互式 HTML Artifact，并最终打包为一个自包含的单文件 HTML。这个 Skill 适合需要状态、组件、路由或 UI 组件库的 Artifact，不负责普通应用长期工程化维护。

## 中文速查

- 中文名：Web Artifact 构建器 / 复杂交互页面
- 英文稳定名：`web-artifacts-builder`
- 你可以这样叫我：`做一个复杂交互页面`、`生成 React Artifact`、`用 shadcn/ui 做前端 Artifact`、`打包成单文件 HTML`
- 适合：多组件、状态管理、路由、shadcn/ui、Tailwind CSS、React 18、需要打包为单文件 HTML 的 Artifact
- 不适合：简单 HTML 片段、静态单页、普通网页开发；这些用更轻的方式即可

构建复杂 frontend Artifact 时按以下步骤：
1. 用 `scripts/init-artifact.sh` 初始化前端项目
2. 编辑生成的代码实现 Artifact
3. 用 `scripts/bundle-artifact.sh` 将代码打包成单文件 HTML
4. 把 Artifact 展示给用户
5. 必要时再测试

**Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

## 输入

用户至少需要给出 Artifact 的目标、主要交互、核心视图或数据结构。信息不足时，优先补问会影响整体结构的问题，例如：用户要操作什么、有哪些状态、是否需要路由、最终是展示型还是工具型。

## 输出与交付物

主交付物是打包后的 `bundle.html`。如果用户需要继续开发，也可以同时保留初始化项目目录、源代码入口和打包命令说明。

## Definition of Done / 验收标准

- `bundle.html` 已生成，且 JavaScript、CSS 和依赖被内联。
- Artifact 能在浏览器或目标 Artifact 环境中打开，不依赖后端服务。
- 核心交互、状态切换、表单或路由按用户要求可用。
- UI 避免模板化大卡片、紫色渐变和无意义装饰，文本不溢出主要容器。
- 如用户要求验证，已用本地预览、Playwright 或等价方式检查关键路径。

## 设计与风格约束

非常重要：避免常见的“AI 味”界面，不要滥用居中大卡片、紫色渐变、统一大圆角和 Inter 字体。

## 快速开始

### Step 1：初始化项目

运行初始化脚本创建 React 项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

脚本会创建一个配置完整的项目：
- ✅ React + TypeScript (via Vite)
- ✅ Tailwind CSS 3.4.1 with shadcn/ui theming system
- ✅ Path aliases (`@/`) configured
- ✅ 40+ shadcn/ui components pre-installed
- ✅ All Radix UI dependencies included
- ✅ Parcel configured for bundling (via .parcelrc)
- ✅ Node 18+ compatibility (auto-detects and pins Vite version)

### Step 2：开发 Artifact

编辑生成的文件来实现 Artifact。需要具体开发指引时，参考下方常见开发任务。

### Step 3：打包为单文件 HTML

将 React app 打包为单文件 HTML Artifact：
```bash
bash scripts/bundle-artifact.sh
```

这会生成 `bundle.html`：一个内联 JavaScript、CSS 和依赖的自包含 Artifact，可直接作为 HTML Artifact 交付。

**要求**：项目根目录必须有 `index.html`。

**脚本会做什么**：
- 安装打包依赖（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建支持路径别名的 `.parcelrc`
- 使用 Parcel 构建（不生成 source map）
- 使用 html-inline 将所有资源内联为单文件 HTML

### Step 4：交付 Artifact

最后把打包后的 HTML 文件交付给用户查看。

### Step 5：测试或预览 Artifact（可选）

这是可选步骤。只有在必要或用户要求时执行。

测试或预览 Artifact 时，可以使用可用工具（包括其他 Skills、Playwright 或 Puppeteer）。一般不要为了简单需求提前做重测试，以免拉长交付时间；如果用户要求或出现问题，再补测试。

## Reference

- **shadcn/ui components**: https://ui.shadcn.com/docs/components

## License

完整许可条款见 `LICENSE.txt`。
