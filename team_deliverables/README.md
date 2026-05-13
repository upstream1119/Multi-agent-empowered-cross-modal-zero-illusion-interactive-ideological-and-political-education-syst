# team_deliverables 说明

本文件夹用于存放项目成员的阶段性交付物、汇报素材、个人说明文档和辅助脚本。

## 1. 可以放什么

- 汇报用图片、流程图、PPT 素材
- 成员阶段性说明文档
- 临时辅助脚本
- 任务交付记录
- 不直接参与系统运行的展示材料
- 个人草稿或阶段性整理文件

## 2. 不应该放什么

- 核心后端代码
- 系统正式读取的数据
- 正式 API 文件
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

成员阶段性交付物统一放在：

team_deliverables/

## 4. 成员目录规范

每个成员只在自己的目录下提交阶段性交付物：

team_deliverables/成员拼音/

每次任务按时间和任务名新建子文件夹：

YYYY-MM-任务名

示例：

team_deliverables/yanxinhao/2026-05-demo-assets/
team_deliverables/lizhuoyang/2026-05-demo-chunks/
team_deliverables/zhangbohan/2026-05-demo-graph/
team_deliverables/zhangruiyang/2026-05-demo-qa/

## 5. 每个阶段文件夹建议结构

README.md
docs/
figures/
scripts/
raw_notes/

其中：

- README.md：说明本次交付内容
- docs/：说明文档、汇报文字
- figures/：图片、流程图
- scripts/：辅助脚本
- raw_notes/：个人草稿，可选

## 6. 合并规则

成员可以先在自己的分支中整理文件。

提交前必须说明：

1. 本次新增或修改了哪些文件
2. 每个文件分别有什么作用
3. 是否会影响主项目运行
4. 哪些文件只是汇报素材
5. 哪些文件需要后续迁移到正式目录

未经负责人确认，不要把个人交付物直接散放到 docs/、scripts/、data/ 根目录。
