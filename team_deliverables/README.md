# team_deliverables 说明

本文件夹用于存放项目成员的非核心阶段交付物、汇报素材、个人说明文档、草稿、交付记录和辅助材料。

请注意：`team_deliverables/` 不是正式代码目录，也不是系统运行数据目录。

## 1. 可以放什么

- 汇报用图片、流程图、PPT 素材
- 成员阶段性说明文档
- 任务交付记录
- 个人草稿或阶段性整理文件
- 不直接参与系统运行的展示材料
- 辅助绘图脚本，例如只用于生成汇报图片的脚本
- 还没有经过负责人审核的题库草稿、设计说明、字段说明

## 2. 不应该放什么

- 核心后端代码
- 正式 API 文件
- 正式测试代码
- 正式 ETL / 图谱构建 / 向量索引脚本
- 系统运行时会直接读取的数据
- 大型原始 PDF
- 模型权重
- 数据库文件
- 临时缓存文件
- 与项目无关的个人文件

## 3. 主目录分工

核心代码仍放在：

src/

系统正式读取的数据仍放在：

data/

正式项目文档仍放在：

docs/

正式测试与验收集仍放在：

tests/

成员非核心阶段交付物放在：

team_deliverables/

## 4. 正式代码协作流程

正式代码不要放在 `team_deliverables/`。

正确流程是：

1. 成员在自己的远程分支开发。
2. 开发完成后说明改了哪些文件、每个文件的作用、如何验证。
3. 负责人审核代码和测试结果。
4. 审核通过后合并到 `main` 的正式目录。

示例：

- 张博涵如果开发 `graph_store.py`、`graph_sim.py`，应在 `zhangbohan` 分支中开发，审核后进入 `src/graph/`。
- 李卓洋如果交付系统会读取的 `text_chunks_demo.jsonl`，审核后进入 `data/processed/`。
- 张睿扬如果题库草稿通过审核并成为正式验收集，最终进入 `tests/`。

## 5. 辅助脚本和正式脚本的区别

可以放在 `team_deliverables/` 的脚本：

- 只用于生成汇报图片的绘图脚本
- 只用于整理个人草稿的小工具
- 不被系统运行链路调用的临时辅助脚本

不应该放在 `team_deliverables/` 的脚本：

- API 服务代码
- ETL 清洗主脚本
- FAISS 索引构建脚本
- NetworkX 图谱构建脚本
- 系统运行时必须调用的脚本

## 6. 成员目录规范

每个成员只在自己的目录下提交非核心阶段交付物：

team_deliverables/成员拼音/

每次任务按时间和任务名新建子文件夹：

YYYY-MM-任务名

示例：

team_deliverables/yanxinhao/2026-05-demo-assets/
team_deliverables/lizhuoyang/2026-05-demo-chunks-notes/
team_deliverables/zhangbohan/2026-05-demo-graph-notes/
team_deliverables/zhangruiyang/2026-05-demo-qa/

## 7. 每个阶段文件夹建议结构

README.md
docs/
figures/
scripts/
raw_notes/

其中：

- README.md：说明本次交付内容
- docs/：说明文档、汇报文字
- figures/：图片、流程图
- scripts/：不参与系统运行的辅助脚本
- raw_notes/：个人草稿，可选

## 8. 提交说明要求

成员提交前必须说明：

1. 本次新增或修改了哪些文件
2. 每个文件分别有什么作用
3. 是否会影响主项目运行
4. 哪些文件只是汇报素材或草稿
5. 哪些文件后续需要迁移到正式目录

未经负责人确认，不要把个人交付物直接散放到 `docs/`、`scripts/`、`data/` 根目录。
