# GitHub Novel Writing Agent Skills Collector

自动收集 GitHub 上所有关于写小说的 agent skills 的脚本工具。

## 功能特点

- 🔍 **多关键词搜索**: 使用 15+ 个与小说写作相关的关键词进行搜索
- 📊 **智能过滤**: 支持按 stars、编程语言、更新时间等条件过滤
- 💾 **多种导出格式**: 支持导出为 JSON 和 Markdown 格式
- 🏷️ **去重处理**: 自动去除重复的仓库记录
- 📝 **Issue 收集**: 同时收集相关的 Issues 讨论

## 安装依赖

```bash
pip install requests
```

## 使用方法

### 基本用法

```bash
python collect_novel_writing_skills.py
```

### 使用 GitHub Token（推荐）

为了获得更高的 API 调用限制，建议使用 GitHub Personal Access Token：

```bash
export GITHUB_TOKEN=your_github_token_here
python collect_novel_writing_skills.py
```

或者直接在命令行中指定：

```bash
python collect_novel_writing_skills.py --token your_github_token_here
```

### 自定义参数

```bash
# 指定输出目录
python collect_novel_writing_skills.py --output-dir ./results

# 设置最低 star 数
python collect_novel_writing_skills.py --min-stars 10

# 指定编程语言
python collect_novel_writing_skills.py --languages Python JavaScript

# 组合使用
python collect_novel_writing_skills.py \
    --token your_token \
    --output-dir ./output \
    --min-stars 5 \
    --languages Python TypeScript JavaScript
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--token` | GitHub Personal Access Token | 无（或从环境变量读取） |
| `--output-dir` | 输出目录路径 | `./output` |
| `--min-stars` | 仓库最低 star 数 | `1` |
| `--languages` | 要搜索的编程语言列表 | `Python JavaScript TypeScript` |

## 搜索关键词

脚本会自动使用以下关键词进行搜索：

1. novel writing agent skills
2. story writing AI agent
3. creative writing assistant
4. fiction writing tools
5. narrative generation agent
6. character development AI
7. plot outline generator
8. world building assistant
9. dialogue writing AI
10. screenplay writing agent
11. writing prompt generator
12. story structure analyzer
13. automated storytelling
14. interactive fiction agent
15. writing coach AI

## 输出文件

脚本会生成两个文件：

1. **JSON 文件** (`novel_writing_skills_YYYYMMDD_HHMMSS.json`): 
   - 包含完整的结构化数据
   - 适合程序化处理和分析

2. **Markdown 文件** (`novel_writing_skills_YYYYMMDD_HHMMSS.md`):
   - 人类可读的报告格式
   - 包含 Top 50 仓库和 Top 30 Issues
   - 带有链接和格式化信息

## 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token"
3. 选择适当的权限（至少需要 `public_repo` 权限）
4. 复制生成的 token 并保存

## 注意事项

- **API 限制**: 
  - 未认证用户：每小时 10 次请求
  - 认证用户：每小时 5000 次请求
  
- **运行时间**: 完整搜索可能需要几分钟时间

- **网络要求**: 需要能够访问 GitHub API

## 示例输出

### JSON 结构

```json
{
  "metadata": {
    "collection_date": "2024-01-01T12:00:00",
    "total_repositories": 150,
    "total_issues": 50,
    "search_queries_used": [...],
    "filters": {...}
  },
  "repositories": [
    {
      "name": "user/repo-name",
      "description": "...",
      "html_url": "https://github.com/...",
      "stars": 100,
      "forks": 20,
      "language": "Python",
      "topics": ["ai", "writing"],
      ...
    }
  ],
  "issues": [...]
}
```

## License

MIT License

## Contributing

欢迎提交 Issue 和 Pull Request！