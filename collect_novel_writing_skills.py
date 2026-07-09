#!/usr/bin/env python3
"""
GitHub Novel Writing Agent Skills Collector

This script automatically searches and collects GitHub repositories, issues, 
and discussions related to novel writing agent skills.

Features:
- Search GitHub for novel writing related agent skills
- Collect repository information, descriptions, and topics
- Export results to JSON and Markdown formats
- Support for filtering by stars, language, and update time

Usage:
    python collect_novel_writing_skills.py [--token YOUR_GITHUB_TOKEN] [--output-dir ./output]
"""

import os
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional
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
        
        # Search queries related to novel writing agent skills
        self.search_queries = [
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
        ]
        
        self.collected_data = []
    
    def search_repositories(self, query: str, min_stars: int = 0, 
                           language: str = "Python", sort: str = "stars",
                           order: str = "desc", per_page: int = 100,
                           max_pages: int = 5) -> List[Dict[str, Any]]:
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
        
        print(f"Searching for: {search_query}")
        
        while page <= max_pages:
            try:
                url = f"{self.base_url}/search/repositories"
                params = {
                    'q': search_query,
                    'sort': sort,
                    'order': order,
                    'per_page': per_page,
                    'page': page
                }
                
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    
                    if not items:
                        break
                    
                    for repo in items:
                        repo_info = {
                            'name': repo['full_name'],
                            'description': repo.get('description', ''),
                            'html_url': repo['html_url'],
                            'stars': repo['stargazers_count'],
                            'forks': repo['forks_count'],
                            'language': repo.get('language', 'Unknown'),
                            'topics': repo.get('topics', []),
                            'created_at': repo['created_at'],
                            'updated_at': repo['updated_at'],
                            'owner': repo['owner']['login'],
                            'search_query': query
                        }
                        repositories.append(repo_info)
                    
                    print(f"  Page {page}: Found {len(items)} repositories")
                    
                    # Check if there are more pages
                    if len(items) < per_page:
                        break
                    
                    page += 1
                elif response.status_code == 403:
                    print(f"  Rate limit exceeded. Stopping search.")
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
                    'per_page': per_page,
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
    
    def collect_all(self, min_stars: int = 1, languages: List[str] = None) -> Dict[str, Any]:
        """
        Collect all novel writing agent skills data.
        
        Args:
            min_stars: Minimum stars for repositories
            languages: List of programming languages to filter
            
        Returns:
            Dictionary containing all collected data
        """
        if languages is None:
            languages = ["Python", "JavaScript", "TypeScript"]
        
        all_repositories = []
        all_issues = []
        
        print("=" * 60)
        print("Starting Novel Writing Agent Skills Collection")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Minimum stars: {min_stars}")
        print(f"Languages: {', '.join(languages)}")
        print("=" * 60)
        
        # Search repositories for each query and language
        for query in self.search_queries:
            print(f"\nSearching repositories for: '{query}'")
            for language in languages:
                repos = self.search_repositories(
                    query=query,
                    min_stars=min_stars,
                    language=language,
                    per_page=50,
                    max_pages=3
                )
                all_repositories.extend(repos)
        
        # Remove duplicates based on repository name
        seen = set()
        unique_repositories = []
        for repo in all_repositories:
            if repo['name'] not in seen:
                seen.add(repo['name'])
                unique_repositories.append(repo)
        
        print(f"\nTotal unique repositories found: {len(unique_repositories)}")
        
        # Search issues (optional, can be slow)
        print("\nSearching related issues...")
        for query in self.search_queries[:5]:  # Limit to first 5 queries for issues
            issues = self.search_issues(query, per_page=30, max_pages=2)
            all_issues.extend(issues)
        
        # Compile final data
        self.collected_data = {
            'metadata': {
                'collection_date': datetime.now().isoformat(),
                'total_repositories': len(unique_repositories),
                'total_issues': len(all_issues),
                'search_queries_used': self.search_queries,
                'filters': {
                    'min_stars': min_stars,
                    'languages': languages
                }
            },
            'repositories': unique_repositories,
            'issues': all_issues
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
        md_content.append("# Novel Writing Agent Skills Collection\n")
        md_content.append(f"**Collection Date:** {self.collected_data['metadata']['collection_date']}\n")
        md_content.append(f"**Total Repositories:** {self.collected_data['metadata']['total_repositories']}\n")
        md_content.append(f"**Total Issues:** {self.collected_data['metadata']['total_issues']}\n")
        
        md_content.append("\n## Search Queries Used\n")
        for i, query in enumerate(self.collected_data['metadata']['search_queries_used'], 1):
            md_content.append(f"{i}. {query}")
        
        md_content.append("\n## Filters\n")
        md_content.append(f"- Minimum Stars: {self.collected_data['metadata']['filters']['min_stars']}")
        md_content.append(f"- Languages: {', '.join(self.collected_data['metadata']['filters']['languages'])}")
        
        md_content.append("\n---\n")
        md_content.append("## Top Repositories\n")
        
        # Sort repositories by stars
        sorted_repos = sorted(
            self.collected_data['repositories'],
            key=lambda x: x['stars'],
            reverse=True
        )
        
        for i, repo in enumerate(sorted_repos[:50], 1):  # Top 50
            md_content.append(f"\n### {i}. [{repo['name']}]({repo['html_url']}) ⭐ {repo['stars']}\n")
            if repo['description']:
                md_content.append(f"**Description:** {repo['description']}\n")
            md_content.append(f"- **Language:** {repo['language']}")
            md_content.append(f"- **Forks:** {repo['forks']}")
            md_content.append(f"- **Owner:** {repo['owner']}")
            if repo['topics']:
                md_content.append(f"- **Topics:** {', '.join(repo['topics'])}")
            md_content.append(f"- **Last Updated:** {repo['updated_at']}")
        
        if self.collected_data['issues']:
            md_content.append("\n---\n")
            md_content.append("## Related Issues\n")
            
            for i, issue in enumerate(self.collected_data['issues'][:30], 1):  # Top 30
                repo_name = '/'.join(issue['repository'])
                md_content.append(f"\n{i}. [{issue['title']}]({issue['html_url']})\n")
                md_content.append(f"   - Repository: {repo_name}")
                md_content.append(f"   - State: {issue['state']}")
                md_content.append(f"   - Created: {issue['created_at']}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        
        print(f"Markdown report exported to: {output_path}")


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
        default=['Python', 'JavaScript', 'TypeScript'],
        help='Programming languages to filter (default: Python JavaScript TypeScript)'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize collector
    collector = GitHubNovelWritingSkillsCollector(token=args.token)
    
    # Collect data
    collector.collect_all(
        min_stars=args.min_stars,
        languages=args.languages
    )
    
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
    print(f"JSON Output: {json_path}")
    print(f"Markdown Output: {md_path}")
    print("=" * 60)


if __name__ == '__main__':
    main()
