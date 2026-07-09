#!/usr/bin/env python3
"""
GitHub Novel Writing Agent Skills Collector (GitHub Actions Ready)

This script automatically searches and collects GitHub repositories, issues,
and discussions related to novel writing agent skills across multiple languages.

Features:
- Multi-language search queries (English, Chinese, French, German, Spanish, Italian, etc.)
- Search GitHub for novel writing related agent skills
- Collect repository information, descriptions, and topics
- Export results to JSON and Markdown formats
- Support for filtering by stars, language, and update time
- GitHub Actions compatible with environment variable outputs
- Deduplication and intelligent ranking

Usage:
    python collect_novel_writing_skills.py [--token YOUR_GITHUB_TOKEN] [--output-dir ./output]
    
For GitHub Actions:
    The script will automatically detect GITHUB_TOKEN and output results to $GITHUB_OUTPUT
"""

import os
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
import requests


class GitHubNovelWritingSkillsCollector:
    """Collector for novel writing agent skills from GitHub."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize the collector.

        Args:
            token: GitHub personal access token (optional, but increases rate limits)
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Novel-Writing-Skills-Collector'
        }

        if self.token:
            self.headers['Authorization'] = f'token {self.token}'

        # Multi-language search queries related to novel writing agent skills
        # Organized by language and category
        self.search_queries = {
            # English queries
            'english': [
                "novel writing agent skills",
                "story writing AI agent",
                "creative writing assistant",
                "fiction writing tools",
                "narrative generation agent",
                "character development AI",
                "plot outline generator",
                "world building assistant",
                "dialogue writing AI",
                "screenplay writing agent",
                "writing prompt generator",
                "story structure analyzer",
                "automated storytelling",
                "interactive fiction agent",
                "writing coach AI",
                "novel planning tool",
                "story generator AI",
                "literary creation assistant",
                "fiction plot builder",
                "character arc generator",
            ],
            # Chinese queries (中文)
            'chinese': [
                "小说写作助手",
                "写作智能体",
                "创作辅助工具",
                "故事生成器",
                "情节构思工具",
                "角色设定生成",
                "世界观构建助手",
                "对话写作 AI",
                "剧本创作工具",
                "写作灵感生成",
                "自动写小说",
                "网文写作助手",
                "小说大纲生成",
                "创意写作 AI",
                "叙事生成器",
                "小说创作插件",
                "写作技巧工具",
                "故事结构分析",
                "人物关系生成",
                "章节生成器",
            ],
            # French queries (Français)
            'french': [
                "assistant écriture roman",
                "générateur d'histoire IA",
                "outil création littéraire",
                "agent écriture créative",
                "générateur de personnages",
                "construction monde fictif",
                "aide écriture dialogue",
                "générateur intrigue roman",
                "coach écriture automatique",
                "outil narration interactive",
            ],
            # German queries (Deutsch)
            'german': [
                "Roman schreiben KI",
                "Geschichtenschreiber Agent",
                "kreatives Schreiben Tool",
                "Charakterentwicklung KI",
                "Handlungsgenerator",
                "Weltbau Assistent",
                "Dialogschreiben AI",
                "Erzählung Generator",
                "Schreibcoach automatisch",
                "interaktive Fiktion Agent",
            ],
            # Spanish queries (Español)
            'spanish': [
                "asistente escritura novela",
                "generador historias IA",
                "herramienta creación literaria",
                "agente escritura creativa",
                "desarrollo personajes IA",
                "generador trama novela",
                "construcción mundo ficticio",
                "escritura diálogos AI",
                "coach escritura automático",
                "narración interactiva agente",
            ],
            # Italian queries (Italiano)
            'italian': [
                "assistente scrittura romanzo",
                "generatore storie IA",
                "strumento creazione letteraria",
                "agente scrittura creativa",
                "sviluppo personaggi IA",
                "generatore trama romanzo",
                "costruzione mondo immaginario",
                "scrittura dialoghi AI",
                "coach scrittura automatico",
                "narrazione interattiva agente",
            ],
            # Portuguese queries (Português)
            'portuguese': [
                "assistente escrita romance",
                "gerador histórias IA",
                "ferramenta criação literária",
                "agente escrita criativa",
                "desenvolvimento personagens IA",
                "gerador enredo romance",
                "construção mundo ficcional",
                "escrita diálogos AI",
                "coach escrita automático",
                "narração interativa agente",
            ],
            # Russian queries (Русский)
            'russian': [
                "помощник написания романов",
                "генератор историй ИИ",
                "инструмент литературного творчества",
                "агент креативного письма",
                "разработка персонажей ИИ",
                "генератор сюжета романа",
                "построение вымышленного мира",
                "написание диалогов ИИ",
                "автоматический писательский тренер",
                "интерактивное повествование агент",
            ],
            # Japanese queries (日本語)
            'japanese': [
                "小説執筆アシスタント",
                "ストーリー生成 AI",
                "創作支援ツール",
                "キャラクター開発 AI",
                "プロット生成器",
                "世界観構築アシスタント",
                "対話執筆 AI",
                "物語生成エージェント",
                "自動執筆コーチ",
                "インタラクティブフィクション",
            ],
            # Korean queries (한국어)
            'korean': [
                "소설 작성 도우미",
                "스토리 생성 AI",
                "창작 글쓰기 도구",
                "캐릭터 개발 AI",
                "플롯 생성기",
                "세계관 구축 도우미",
                "대사 작성 AI",
                "이야기 생성 에이전트",
                "자동 작문 코치",
                "인터랙티브 픽션",
            ],
        }

        self.collected_data = []
        self.seen_repos: Set[str] = set()

    def search_repositories(self, query: str, min_stars: int = 0,
                           language: Optional[str] = None, 
                           sort: str = "stars",
                           order: str = "desc", per_page: int = 100,
                           max_pages: int = 5, 
                           created_after: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search GitHub repositories based on query.

        Args:
            query: Search query string
            min_stars: Minimum number of stars required
            language: Programming language filter
            sort: Sort field (stars, forks, updated)
            order: Sort order (asc, desc)
            per_page: Results per page (max 100)
            max_pages: Maximum pages to fetch
            created_after: Filter repos created after this date (YYYY-MM-DD)

        Returns:
            List of repository data dictionaries
        """
        repositories = []
        page = 1

        # Build search query with filters
        search_query = f"{query} in:name,description,readme topic"
        if language:
            search_query += f" language:{language}"
        if min_stars > 0:
            search_query += f" stars:>={min_stars}"
        if created_after:
            search_query += f" created:>{created_after}"

        print(f"Searching for: {search_query}")

        while page <= max_pages:
            try:
                url = f"{self.base_url}/search/repositories"
                params = {
                    'q': search_query,
                    'sort': sort,
                    'order': order,
                    'per_page': min(per_page, 100),
                    'page': page
                }

                response = requests.get(url, headers=self.headers, params=params, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])

                    if not items:
                        break

                    for repo in items:
                        # Skip duplicates
                        if repo['full_name'] in self.seen_repos:
                            continue
                        self.seen_repos.add(repo['full_name'])

                        repo_info = {
                            'name': repo['full_name'],
                            'description': repo.get('description', '') or '',
                            'html_url': repo['html_url'],
                            'stars': repo['stargazers_count'],
                            'forks': repo['forks_count'],
                            'language': repo.get('language', 'Unknown'),
                            'topics': repo.get('topics', []),
                            'created_at': repo['created_at'],
                            'updated_at': repo['updated_at'],
                            'owner': repo['owner']['login'],
                            'search_query': query,
                            'license': repo.get('license', {}).get('key', 'unknown') if repo.get('license') else 'unknown'
                        }
                        repositories.append(repo_info)

                    print(f"  Page {page}: Found {len(items)} repositories ({len(repositories)} new)")

                    # Check if there are more pages
                    if len(items) < per_page:
                        break

                    page += 1
                elif response.status_code == 403:
                    print(f"  Rate limit exceeded. Stopping search.")
                    # Return partial results on rate limit
                    break
                else:
                    print(f"  Error: {response.status_code} - {response.text}")
                    break

            except requests.exceptions.RequestException as e:
                print(f"  Request error: {e}")
                break

        return repositories

    def search_issues(self, query: str, state: str = "open",
                     per_page: int = 100, max_pages: int = 3) -> List[Dict[str, Any]]:
        """
        Search GitHub issues related to novel writing.

        Args:
            query: Search query string
            state: Issue state (open, closed, all)
            per_page: Results per page
            max_pages: Maximum pages to fetch

        Returns:
            List of issue data dictionaries
        """
        issues = []
        page = 1

        search_query = f"{query} in:title,body type:issue"

        while page <= max_pages:
            try:
                url = f"{self.base_url}/search/issues"
                params = {
                    'q': search_query,
                    'state': state,
                    'sort': 'created',
                    'order': 'desc',
                    'per_page': min(per_page, 100),
                    'page': page
                }

                response = requests.get(url, headers=self.headers, params=params, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])

                    if not items:
                        break

                    for issue in items:
                        issue_info = {
                            'title': issue['title'],
                            'repository': issue['repository_url'].split('/')[-2:],
                            'html_url': issue['html_url'],
                            'state': issue['state'],
                            'created_at': issue['created_at'],
                            'user': issue['user']['login'],
                            'labels': [label['name'] for label in issue.get('labels', [])],
                            'search_query': query
                        }
                        issues.append(issue_info)

                    print(f"  Issues Page {page}: Found {len(items)} issues")

                    if len(items) < per_page:
                        break

                    page += 1
                else:
                    break

            except requests.exceptions.RequestException as e:
                print(f"  Request error: {e}")
                break

        return issues

    def search_topics(self, query: str, per_page: int = 30, max_pages: int = 2) -> List[Dict[str, Any]]:
        """
        Search GitHub topics related to novel writing.

        Args:
            query: Search query string
            per_page: Results per page
            max_pages: Maximum pages to fetch

        Returns:
            List of topic data dictionaries
        """
        topics = []
        page = 1

        while page <= max_pages:
            try:
                url = f"{self.base_url}/search/topics"
                params = {
                    'q': query,
                    'per_page': min(per_page, 30),
                    'page': page
                }

                # Note: Topics search requires custom accept header
                headers = self.headers.copy()
                headers['Accept'] = 'application/vnd.github.mercy-preview+json'

                response = requests.get(url, headers=headers, params=params, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])

                    if not items:
                        break

                    for topic in items:
                        topic_info = {
                            'name': topic['name'],
                            'display_name': topic.get('display_name', topic['name']),
                            'short_description': topic.get('short_description', ''),
                            'created_by': topic.get('created_by', {}).get('login', 'unknown'),
                            'score': topic.get('score', 0)
                        }
                        topics.append(topic_info)

                    if len(items) < per_page:
                        break

                    page += 1
                else:
                    break

            except requests.exceptions.RequestException as e:
                print(f"  Request error: {e}")
                break

        return topics

    def collect_all(self, min_stars: int = 1, languages: List[str] = None, 
                   include_issues: bool = True, include_topics: bool = True,
                   created_after: Optional[str] = None) -> Dict[str, Any]:
        """
        Collect all novel writing agent skills data.

        Args:
            min_stars: Minimum stars for repositories
            languages: List of programming languages to filter
            include_issues: Whether to search issues
            include_topics: Whether to search topics
            created_after: Filter repos created after this date

        Returns:
            Dictionary containing all collected data
        """
        if languages is None:
            languages = ["Python", "JavaScript", "TypeScript", "Jupyter Notebook"]

        all_repositories = []
        all_issues = []
        all_topics = []

        print("=" * 60)
        print("Starting Novel Writing Agent Skills Collection")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Minimum stars: {min_stars}")
        print(f"Languages: {', '.join(languages)}")
        print(f"Include issues: {include_issues}")
        print(f"Include topics: {include_topics}")
        if created_after:
            print(f"Created after: {created_after}")
        print("=" * 60)

        # Count total queries
        total_queries = sum(len(queries) for queries in self.search_queries.values())
        print(f"Total search queries: {total_queries}")
        print(f"Languages covered: {', '.join(self.search_queries.keys())}")
        print("=" * 60)

        # Search repositories for each query and language
        query_count = 0
        for lang, queries in self.search_queries.items():
            print(f"\n{'='*40}")
            print(f"Processing {lang.upper()} queries ({len(queries)} queries)")
            print(f"{'='*40}")
            
            for query in queries:
                query_count += 1
                print(f"\n[{query_count}/{total_queries}] Searching: '{query}'")
                
                for language in languages:
                    repos = self.search_repositories(
                        query=query,
                        min_stars=min_stars,
                        language=language,
                        per_page=30,
                        max_pages=2,
                        created_after=created_after
                    )
                    all_repositories.extend(repos)
                    
                    # Small delay to avoid rate limiting
                    import time
                    time.sleep(0.5)

        print(f"\nTotal unique repositories found: {len(all_repositories)}")

        # Search topics (optional)
        if include_topics:
            print("\nSearching related topics...")
            topic_queries = [
                "novel-writing", "creative-writing", "storytelling",
                "写作", "小说", "创作",
                "écriture", "roman", "littérature"
            ]
            for query in topic_queries:
                topics = self.search_topics(query, per_page=20, max_pages=1)
                all_topics.extend(topics)
            print(f"Total topics found: {len(all_topics)}")

        # Search issues (optional, can be slow)
        if include_issues:
            print("\nSearching related issues...")
            issue_queries = []
            # Take first few queries from each language
            for lang, queries in self.search_queries.items():
                issue_queries.extend(queries[:3])
            
            for i, query in enumerate(issue_queries[:15]):  # Limit to 15 queries for issues
                print(f"[{i+1}/15] Searching issues: '{query}'")
                issues = self.search_issues(query, per_page=20, max_pages=1)
                all_issues.extend(issues)
                import time
                time.sleep(0.3)
            print(f"Total issues found: {len(all_issues)}")

        # Compile final data
        self.collected_data = {
            'metadata': {
                'collection_date': datetime.now().isoformat(),
                'total_repositories': len(all_repositories),
                'total_issues': len(all_issues),
                'total_topics': len(all_topics),
                'search_queries_used': {lang: len(queries) for lang, queries in self.search_queries.items()},
                'filters': {
                    'min_stars': min_stars,
                    'languages': languages,
                    'include_issues': include_issues,
                    'include_topics': include_topics,
                    'created_after': created_after
                }
            },
            'repositories': all_repositories,
            'issues': all_issues,
            'topics': all_topics
        }

        return self.collected_data

    def export_to_json(self, output_path: str) -> None:
        """Export collected data to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.collected_data, f, indent=2, ensure_ascii=False)
        print(f"\nData exported to: {output_path}")

    def export_to_markdown(self, output_path: str) -> None:
        """Export collected data to Markdown file."""
        md_content = []
        md_content.append("# Novel Writing Agent Skills Collection 📚✍️\n")
        md_content.append(f"**Collection Date:** {self.collected_data['metadata']['collection_date']}\n")
        md_content.append(f"**Total Repositories:** {self.collected_data['metadata']['total_repositories']} 🌟\n")
        md_content.append(f"**Total Issues:** {self.collected_data['metadata']['total_issues']} 💬\n")
        md_content.append(f"**Total Topics:** {self.collected_data['metadata']['total_topics']} 🏷️\n")

        md_content.append("\n## Search Queries by Language\n")
        for lang, count in self.collected_data['metadata']['search_queries_used'].items():
            md_content.append(f"- **{lang.title()}:** {count} queries")

        md_content.append("\n## Filters\n")
        md_content.append(f"- Minimum Stars: {self.collected_data['metadata']['filters']['min_stars']}")
        md_content.append(f"- Languages: {', '.join(self.collected_data['metadata']['filters']['languages'])}")
        md_content.append(f"- Include Issues: {self.collected_data['metadata']['filters']['include_issues']}")
        md_content.append(f"- Include Topics: {self.collected_data['metadata']['filters']['include_topics']}")
        if self.collected_data['metadata']['filters'].get('created_after'):
            md_content.append(f"- Created After: {self.collected_data['metadata']['filters']['created_after']}")

        md_content.append("\n---\n")
        md_content.append("## Top Repositories by Stars ⭐\n")

        # Sort repositories by stars
        sorted_repos = sorted(
            self.collected_data['repositories'],
            key=lambda x: x['stars'],
            reverse=True
        )

        for i, repo in enumerate(sorted_repos[:100], 1):  # Top 100
            description = repo['description'] if repo['description'] else 'No description'
            topics_str = ', '.join(repo['topics']) if repo['topics'] else 'None'
            md_content.append(f"\n### {i}. [{repo['name']}]({repo['html_url']}) ⭐ {repo['stars']}\n")
            md_content.append(f"**Description:** {description}\n")
            md_content.append(f"- **Language:** {repo['language']}")
            md_content.append(f"- **Forks:** {repo['forks']} 🔱")
            md_content.append(f"- **Owner:** @{repo['owner']}")
            md_content.append(f"- **Topics:** {topics_str}")
            md_content.append(f"- **License:** {repo['license']}")
            md_content.append(f"- **Last Updated:** {repo['updated_at']}")

        if self.collected_data['topics']:
            md_content.append("\n---\n")
            md_content.append("## Related Topics 🏷️\n")
            for i, topic in enumerate(self.collected_data['topics'][:30], 1):
                desc = topic['short_description'] if topic['short_description'] else 'No description'
                md_content.append(f"{i}. **{topic['name']}** - {desc} (by @{topic['created_by']})")

        if self.collected_data['issues']:
            md_content.append("\n---\n")
            md_content.append("## Related Issues 💬\n")

            for i, issue in enumerate(self.collected_data['issues'][:50], 1):
                repo_name = '/'.join(issue['repository'])
                labels_str = ', '.join(issue['labels']) if issue['labels'] else 'None'
                md_content.append(f"\n{i}. [{issue['title']}]({issue['html_url']})\n")
                md_content.append(f"   - Repository: {repo_name}")
                md_content.append(f"   - State: {issue['state']}")
                md_content.append(f"   - Author: @{issue['user']}")
                md_content.append(f"   - Created: {issue['created_at']}")
                md_content.append(f"   - Labels: {labels_str}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))

        print(f"Markdown report exported to: {output_path}")

    def export_for_github_actions(self, output_dir: str) -> Dict[str, str]:
        """
        Export data in format suitable for GitHub Actions outputs.
        
        Returns:
            Dictionary with output variables for GitHub Actions
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export main files
        json_path = os.path.join(output_dir, f'novel_writing_skills_{timestamp}.json')
        md_path = os.path.join(output_dir, f'novel_writing_skills_{timestamp}.md')
        
        self.export_to_json(json_path)
        self.export_to_markdown(md_path)
        
        # Create summary for GitHub Actions
        summary_stats = {
            'total_repos': self.collected_data['metadata']['total_repositories'],
            'total_issues': self.collected_data['metadata']['total_issues'],
            'total_topics': self.collected_data['metadata']['total_topics'],
            'languages_searched': list(self.collected_data['metadata']['search_queries_used'].keys()),
            'json_file': json_path,
            'markdown_file': md_path
        }
        
        # Write GitHub Actions output file if running in Actions
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a', encoding='utf-8') as f:
                f.write(f"total_repos={summary_stats['total_repos']}\n")
                f.write(f"total_issues={summary_stats['total_issues']}\n")
                f.write(f"total_topics={summary_stats['total_topics']}\n")
                f.write(f"json_file={json_path}\n")
                f.write(f"markdown_file={md_path}\n")
        
        return summary_stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Collect GitHub repositories and issues related to novel writing agent skills'
    )
    parser.add_argument(
        '--token',
        type=str,
        default=None,
        help='GitHub personal access token (or set GITHUB_TOKEN environment variable)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./output',
        help='Output directory for results (default: ./output)'
    )
    parser.add_argument(
        '--min-stars',
        type=int,
        default=1,
        help='Minimum number of stars for repositories (default: 1)'
    )
    parser.add_argument(
        '--languages',
        type=str,
        nargs='+',
        default=['Python', 'JavaScript', 'TypeScript', 'Jupyter Notebook'],
        help='Programming languages to filter (default: Python JavaScript TypeScript "Jupyter Notebook")'
    )
    parser.add_argument(
        '--no-issues',
        action='store_true',
        help='Skip searching issues'
    )
    parser.add_argument(
        '--no-topics',
        action='store_true',
        help='Skip searching topics'
    )
    parser.add_argument(
        '--created-after',
        type=str,
        default=None,
        help='Filter repositories created after this date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--github-actions-mode',
        action='store_true',
        help='Enable GitHub Actions specific output formatting'
    )

    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Initialize collector
    collector = GitHubNovelWritingSkillsCollector(token=args.token)

    # Collect data
    collector.collect_all(
        min_stars=args.min_stars,
        languages=args.languages,
        include_issues=not args.no_issues,
        include_topics=not args.no_topics,
        created_after=args.created_after
    )

    if args.github_actions_mode:
        summary = collector.export_for_github_actions(args.output_dir)
        print("\n" + "=" * 60)
        print("GitHub Actions Mode Summary")
        print("=" * 60)
        for key, value in summary.items():
            print(f"{key}: {value}")
    else:
        # Generate timestamp for filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Export results
        json_path = os.path.join(args.output_dir, f'novel_writing_skills_{timestamp}.json')
        md_path = os.path.join(args.output_dir, f'novel_writing_skills_{timestamp}.md')

        collector.export_to_json(json_path)
        collector.export_to_markdown(md_path)

    print("\n" + "=" * 60)
    print("Collection Complete!")
    print("=" * 60)
    print(f"Total Repositories: {collector.collected_data['metadata']['total_repositories']}")
    print(f"Total Issues: {collector.collected_data['metadata']['total_issues']}")
    print(f"Total Topics: {collector.collected_data['metadata']['total_topics']}")
    print(f"Languages Searched: {', '.join(collector.collected_data['metadata']['search_queries_used'].keys())}")
    print("=" * 60)


if __name__ == '__main__':
    main()
