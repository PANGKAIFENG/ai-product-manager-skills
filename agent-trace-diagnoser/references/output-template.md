# Output Template

Default to Chinese when the user writes Chinese.

```markdown
**核心结论**
<1-2 句话说明真正主因。明确区分“主链路失败”和“fallback 后暴露的问题”。>

**证据链**
- <按时间顺序列出关键 trace 事实。每条标注 confirmed / inferred / needs verification。>
- <包括命中的 skill/tool、失败命令、错误码、fallback 转换、最终错误。>

**不是主因但会放大的问题**
- <列出环境权限、缺少工具、大小限制、临时目录、输出策略等次要问题。>

**可能对应的代码位置**
- `<absolute/path/to/file.ext>:<line>` - <为什么这行相关；置信度：high/medium/low>
- `<absolute/path/to/file.ext>:<line>` - <这是主因、fallback 问题还是环境问题>

If exact code was not read:

- `<likely/source/path>` - <根据 runtime path / error string 推断，尚未验证>

**修复建议**
- <最小修复建议 1：行为、位置、原因。>
- <最小修复建议 2：fallback/guardrail/eval。>

**建议补的回归验证**
- <用这个 trace 或最小 fixture 验证主链路。>
- <验证不会再走错误 fallback，或 fallback 会输出正确限制说明。>
```

## Wording Rules

- Say "主因不是 X，而是 Y" when the trace shows a misleading final error.
- Say "可能对应" or "likely source location" when line mapping is inferred.
- Say "我没有修改文件" when the user requested read-only diagnosis.
- Avoid saying "已修复" unless code changes and verification actually happened.
