# GitHub Novel Writing Agent Skills Collector

📚✍️ 一个自动收集 GitHub 上所有关于小说写作 Agent Skills 的脚本，支持 GitHub Actions 定时运行。

An automated script that collects all novel writing agent skills from GitHub, with GitHub Actions support for scheduled runs.

## ✨ 功能特点 / Features

- **多语言搜索 / Multi-language Search**: 支持 10 种语言的搜索关键词
  - 🇬🇧 English (20 queries)
  - 🇨🇳 中文 (20 queries)
  - 🇫🇷 Français (10 queries)
  - 🇩🇪 Deutsch (10 queries)
  - 🇪🇸 Español (10 queries)
  - 🇮🇹 Italiano (10 queries)
  - 🇵🇹 Português (10 queries)
  - 🇷🇺 Русский (10 queries)
  - 🇯🇵 日本語 (10 queries)
  - 🇰🇷 한국어 (10 queries)

- **GitHub Actions 集成 / GitHub Actions Integration**
  - 每周自动运行 / Weekly automatic execution
  - 手动触发支持 / Manual trigger support
  - 可配置参数 / Configurable parameters

- **数据导出 / Data Export**
  - JSON 格式 / JSON format
  - Markdown 报告 / Markdown report
  - GitHub Actions 输出变量 / GitHub Actions output variables

- **智能过滤 / Smart Filtering**
  - 按星星数过滤 / Filter by stars
  - 按编程语言过滤 / Filter by programming language
  - 按创建日期过滤 / Filter by creation date
  - 自动去重 / Automatic deduplication

## 📦 文件结构 / File Structure

```
.
├── collect_novel_writing_skills.py    # 主脚本 / Main script
├── .github/
│   └── workflows/
│       └── collect_novel_writing_skills.yml  # GitHub Actions 配置
├── output/                           # 输出目录 / Output directory
│   ├── *.json                        # JSON 数据文件
│   └── *.md                          # Markdown 报告
└── README.md                         # 本文件
```

## 🚀 使用方法 / Usage

### 本地运行 / Run Locally

```bash
# 安装依赖 / Install dependencies
pip install requests

# 基本运行 / Basic run
python collect_novel_writing_skills.py

# 使用 GitHub Token（提高 API 限制）/ With GitHub Token (increased API limits)
export GITHUB_TOKEN=your_token_here
python collect_novel_writing_skills.py

# 自定义参数 / Custom parameters
python collect_novel_writing_skills.py \
  --min-stars 10 \
  --languages Python JavaScript TypeScript \
  --output-dir ./my_output \
  --no-issues \
  --no-topics

# GitHub Actions 模式 / GitHub Actions mode
python collect_novel_writing_skills.py --github-actions-mode
```

### 命令行参数 / Command Line Arguments

| 参数 / Argument | 说明 / Description | 默认值 / Default |
|----------------|-------------------|-----------------|
| `--token` | GitHub 个人访问令牌 / GitHub personal access token | `$GITHUB_TOKEN` 环境变量 |
| `--output-dir` | 输出目录 / Output directory | `./output` |
| `--min-stars` | 最小星星数 / Minimum stars | `1` |
| `--languages` | 编程语言过滤 / Programming languages | `Python JavaScript TypeScript Jupyter Notebook` |
| `--no-issues` | 跳过 Issues 搜索 / Skip issues search | `False` |
| `--no-topics` | 跳过 Topics 搜索 / Skip topics search | `False` |
| `--created-after` | 只收集该日期之后的仓库 / Only repos created after this date (YYYY-MM-DD) | `None` |
| `--github-actions-mode` | 启用 GitHub Actions 输出格式 / Enable GitHub Actions output format | `False` |

### GitHub Actions 使用 / Using GitHub Actions

#### 自动运行 / Automatic Execution

工作流已配置为每周一 00:00 UTC 自动运行。

The workflow is configured to run automatically every Monday at 00:00 UTC.

#### 手动触发 / Manual Trigger

1. 进入仓库的 Actions 标签页
2. 选择 "Collect Novel Writing Agent Skills" 工作流
3. 点击 "Run workflow"
4. 配置参数（可选）：
   - `min_stars`: 最小星星数
   - `languages`: 编程语言（逗号分隔）
   - `include_issues`: 是否包含 Issues
   - `include_topics`: 是否包含 Topics
5. 点击 "Run workflow"

Go to the Actions tab in your repository:
1. Select "Collect Novel Writing Agent Skills" workflow
2. Click "Run workflow"
3. Configure parameters (optional):
   - `min_stars`: Minimum number of stars
   - `languages`: Programming languages (comma-separated)
   - `include_issues`: Include issues in search
   - `include_topics`: Include topics in search
4. Click "Run workflow"

#### 自定义调度时间 / Custom Schedule

编辑 `.github/workflows/collect_novel_writing_skills.yml` 文件，修改 `cron` 表达式：

Edit `.github/workflows/collect_novel_writing_skills.yml` and modify the `cron` expression:

```yaml
on:
  schedule:
    # 每天运行 / Run daily
    - cron: '0 0 * * *'
    
    # 每月 1 号运行 / Run on 1st of every month
    - cron: '0 0 1 * *'
    
    # 每周一和周四运行 / Run every Monday and Thursday
    - cron: '0 0 * * 1,4'
```

## 📊 输出格式 / Output Format

### JSON 输出示例 / JSON Output Example

```json
{
  "metadata": {
    "collection_date": "2024-01-15T10:30:00",
    "total_repositories": 500,
    "total_issues": 150,
    "total_topics": 30,
    "search_queries_used": {
      "english": 20,
      "chinese": 20,
      "french": 10
    },
    "filters": {
      "min_stars": 1,
      "languages": ["Python", "JavaScript"],
      "include_issues": true,
      "include_topics": true
    }
  },
  "repositories": [
    {
      "name": "user/repo-name",
      "description": "A novel writing assistant",
      "html_url": "https://github.com/user/repo-name",
      "stars": 1234,
      "forks": 567,
      "language": "Python",
      "topics": ["writing", "ai", "novel"],
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2024-01-15T00:00:00Z",
      "owner": "user",
      "license": "mit"
    }
  ],
  "issues": [...],
  "topics": [...]
}
```

### Markdown 报告 / Markdown Report

生成的 Markdown 报告包含：
- 收集统计信息
- 按语言分类的搜索查询
- 按星星排序的 Top 100 仓库
- 相关 Topics
- 相关 Issues

The generated Markdown report includes:
- Collection statistics
- Search queries by language
- Top 100 repositories sorted by stars
- Related topics
- Related issues

## 🔧 配置选项 / Configuration Options

### 添加新的搜索语言 / Adding New Search Languages

在 `collect_novel_writing_skills.py` 中的 `search_queries` 字典添加新语言：

Add new languages to the `search_queries` dictionary in `collect_novel_writing_skills.py`:

```python
self.search_queries = {
    # ... existing languages ...
    
    # Add new language
    'dutch': [
        "roman schrijven assistent",
        "verhaal generator IA",
        # ... more queries
    ],
}
```

### 调整搜索参数 / Adjusting Search Parameters

修改以下参数来优化搜索结果：

Modify these parameters to optimize search results:

- `per_page`: 每页结果数（最大 100）/ Results per page (max 100)
- `max_pages`: 最大页数 / Maximum pages to fetch
- `min_stars`: 最小星星数阈值 / Minimum stars threshold
- `languages`: 要搜索的编程语言 / Programming languages to search

## ⚠️ 注意事项 / Notes

1. **API 限制 / API Limits**
   - 未认证：每小时 10 次请求 / Unauthenticated: 10 requests/hour
   - 认证后：每小时 5000 次请求 / Authenticated: 5000 requests/hour
   - 建议使用 GitHub Token / GitHub Token recommended

2. **运行时间 / Runtime**
   - 完整搜索可能需要 10-30 分钟 / Full search may take 10-30 minutes
   - 可通过减少查询数量或页数来加速 / Speed up by reducing queries or pages

3. **数据存储 / Data Storage**
   - 输出文件可能较大（几 MB 到几十 MB）/ Output files can be large (several MB to tens of MB)
   - 建议定期清理旧文件 / Regular cleanup of old files recommended

## 📝 许可证 / License

MIT License

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

Issues and Pull Requests are welcome!

## 📧 联系方式 / Contact

如有问题或建议，请开 Issue。

For questions or suggestions, please open an issue.
