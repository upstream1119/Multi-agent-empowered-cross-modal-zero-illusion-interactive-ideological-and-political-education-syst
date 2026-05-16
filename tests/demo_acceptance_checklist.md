# 多智能体跨模态零幻觉思政系统 Demo 演示验收核对清单
## 一、前置环境准备核对
- [ ] 已拉取最新 pengyihan 分支，40条 text_chunks_demo.jsonl 正常加载
- [ ] 本地切换至 zhangruiyang 分支，所有修改仅提交当前分支
- [ ] 混合检索 Mock 服务启动正常，检索接口无报错
- [ ] 所有 JSONL 数据通过 validate_jsonl.py 格式强校验
- [ ] 统一约定：暂不使用 citation.page 字段，仅使用 citation.doc + citation.section

## 二、展示问题集交付验收
- [ ] 完成 8 条标准演示问题编写，数量符合 8-10 条要求
- [ ] 每条问题完整包含全部必填字段：query、expected_entities、expected_citation_keywords、min_hybrid_hits、expected_chunk_ids、expected_citation_sections、is_core_demo、is_suitable_for_demo
- [ ] expected_chunk_ids 与 text_chunks_demo.jsonl 中的真实 chunk ID 完全匹配
- [ ] expected_citation_sections 与文本块中的 citation.section 精准对应
- [ ] 明确标记 3 条核心必演问题（is_core_demo=true），且必演问题均标记为适合演示（is_suitable_for_demo=true）
- [ ] 问题贴合思政历史场景，匹配现有演示文本内容，无脱离文本的无效问题

## 三、混合检索能力校验
- [ ] 调用检索接口可正常召回满足 min_hybrid_hits 数量的文本块
- [ ] 实际命中的 chunk ID 包含 expected_chunk_ids 中的至少1个（达标）
- [ ] 预期实体可在检索结果内容中精准匹配命中
- [ ] 预期引用关键词可在 citation 溯源内容中匹配成功
- [ ] 检索返回的 citation.section 包含 expected_citation_sections 中的内容
- [ ] 检索返回字段完整：内容、来源、段落、ChunkID、引用信息齐全
- [ ] 无无效幻觉内容，所有回答严格依赖检索原文生成

## 四、API 接口统一验收
- [ ] 问答请求入参格式统一规范
- [ ] 检索结果出参结构与预定义返回结构完全对齐
- [ ] 多轮历史对话上下文关联调用正常
- [ ] 实体抽取、关键词溯源字段返回稳定可用
- [ ] 批量评测、单条调试接口均可正常调用

## 五、演示现场前置检查
- [ ] 3条核心必演问题（is_core_demo=true）本地预跑全部通过
- [ ] 每条演示问题确认溯源来源清晰可查，expected_chunk_ids 和 expected_citation_sections 均匹配成功
- [ ] 演示流程顺序梳理完成，优先演示3条核心必演问题，无顺序冲突
- [ ] 关键演示节点截图点位提前规划完毕
- [ ] 自动验收脚本可对展示问题批量执行评测，新增字段可正常识别

## 六、最终提交规范
- [ ] 演示问题 JSON 文件提交至 zhangruiyang 分支 tests 目录
- [ ] 本验收清单文档提交至项目根目录
- [ ] 提交前确认无代码冲突、无冗余测试数据
- [ ] 确认完成后可申请分支合并与联合调试
