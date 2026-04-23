import json
import os
import sys

def validate_jsonl(file_path):
    print(f"🚀 [多智能体思政系统] 开启数据硬核质检: {file_path}")
    seen_ids = set()
    errors = 0
    
    if not os.path.exists(file_path):
        print(f"❌ 找不到文件: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if not line.strip(): continue
            try:
                data = json.loads(line)
                
                # 1. 必填字段硬校验
                required_fields = ['id', 'source', 'source_type', 'title', 'text', 'chunk_type', 'topic']
                for field in required_fields:
                    if field not in data or data[field] is None or str(data[field]).strip() == "":
                        print(f"❌ 行 {i}: 缺失核心字段或内容为空 -> {field}")
                        errors += 1
                
                # 2. ID 唯一性校验
                curr_id = data.get('id')
                if curr_id in seen_ids:
                    print(f"❌ 行 {i}: ID 冲突/重复 -> {curr_id}")
                    errors += 1
                seen_ids.add(curr_id)
                
                # 3. Citation 对象化与完整性校验
                citation = data.get('citation')
                if not citation or not isinstance(citation, dict):
                    print(f"❌ 行 {i}: citation 缺失或不是对象格式 {{}}")
                    errors += 1
                else:
                    doc = citation.get('doc')
                    section = citation.get('section')
                    if doc is None or str(doc).strip() == "":
                        print(f"❌ 行 {i}: citation.doc 缺失，无法进行零幻觉溯源")
                        errors += 1
                    if section is None or str(section).strip() == "":
                        print(f"❌ 行 {i}: citation.section 缺失；若原始数据无天然 section，应由 ETL 自动生成")
                        errors += 1
                    
            except json.JSONDecodeError:
                print(f"❌ 行 {i}: 发现无效的 JSON 格式，请检查逗号或括号")
                errors += 1

    if errors == 0:
        print(f"✅ 质检通过！{len(seen_ids)} 条数据已就绪，可进入本地索引阶段。")
    else:
        print(f"🛑 质检未通过！累计发现 {errors} 处违规。请务必修正后再提交！")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_jsonl.py <path_to_jsonl>")
    else:
        validate_jsonl(sys.argv[1])
