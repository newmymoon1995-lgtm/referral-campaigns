#!/usr/bin/env python3
"""
GitHub Analytics Tracker for referral-campaigns repository
Tracks repository activity, content performance, and optimal timing for updates
"""

import json
import csv
from datetime import datetime, timedelta
import os
import urllib.request
import urllib.error

class GitHubAnalytics:
    def __init__(self, repo_owner="newmymoon1995-lgtm", repo_name="referral-campaigns"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.analytics_file = "analytics_data.json"
        self.content_performance_file = "content_performance.csv"
        
    def get_repository_stats(self):
        """Get basic repository statistics"""
        try:
            with urllib.request.urlopen(self.base_url) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            stats = {
                "timestamp": datetime.now().isoformat(),
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "watchers": data.get("subscribers_count", 0),
                "open_issues": data.get("open_issues_count", 0),
                "size": data.get("size", 0),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at")
            }
            
            return stats
        except urllib.error.URLError as e:
            print(f"Error fetching repository stats: {e}")
            return None
    
    def get_traffic_stats(self):
        """Get repository traffic statistics (requires authentication)"""
        # Note: Traffic stats require authentication with a token
        # This is a placeholder for the implementation
        traffic_urls = {
            "views": f"{self.base_url}/traffic/views",
            "clones": f"{self.base_url}/traffic/clones",
            "referrers": f"{self.base_url}/traffic/popular/referrers",
            "paths": f"{self.base_url}/traffic/popular/paths"
        }
        
        print("Traffic stats require GitHub token authentication.")
        print("Set GITHUB_TOKEN environment variable to enable traffic analytics.")
        return None
    
    def get_commit_activity(self):
        """Get recent commit activity"""
        try:
            with urllib.request.urlopen(f"{self.base_url}/commits") as response:
                commits = json.loads(response.read().decode('utf-8'))
            
            recent_commits = []
            for commit in commits[:10]:  # Last 10 commits
                commit_data = {
                    "sha": commit.get("sha"),
                    "message": commit.get("commit", {}).get("message"),
                    "author": commit.get("commit", {}).get("author", {}).get("name"),
                    "date": commit.get("commit", {}).get("author", {}).get("date"),
                    "url": commit.get("html_url")
                }
                recent_commits.append(commit_data)
            
            return recent_commits
        except urllib.error.URLError as e:
            print(f"Error fetching commit activity: {e}")
            return None
    
    def get_issues_activity(self):
        """Get issues and pull requests activity"""
        try:
            with urllib.request.urlopen(f"{self.base_url}/issues") as response:
                issues = json.loads(response.read().decode('utf-8'))
            
            issues_data = []
            for issue in issues[:10]:  # Last 10 issues
                issue_data = {
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "state": issue.get("state"),
                    "created_at": issue.get("created_at"),
                    "comments": issue.get("comments"),
                    "url": issue.get("html_url")
                }
                issues_data.append(issue_data)
            
            return issues_data
        except urllib.error.URLError as e:
            print(f"Error fetching issues activity: {e}")
            return None
    
    def analyze_content_performance(self):
        """Analyze which content performs best based on file changes"""
        try:
            with urllib.request.urlopen(f"{self.base_url}/commits") as response:
                commits = json.loads(response.read().decode('utf-8'))
            
            # Track file changes
            file_changes = {}
            
            for commit in commits[:20]:  # Analyze last 20 commits
                files_url = commit.get("url", "").replace("commits", "commits")
                try:
                    with urllib.request.urlopen(files_url) as files_response:
                        files_data = json.loads(files_response.read().decode('utf-8'))
                    
                    for file in files_data.get("files", []):
                        filename = file.get("filename")
                        if filename:
                            if filename not in file_changes:
                                file_changes[filename] = {
                                    "change_count": 0,
                                    "additions": 0,
                                    "deletions": 0,
                                    "last_changed": None
                                }
                            
                            file_changes[filename]["change_count"] += 1
                            file_changes[filename]["additions"] += file.get("additions", 0)
                            file_changes[filename]["deletions"] += file.get("deletions", 0)
                            file_changes[filename]["last_changed"] = commit.get("commit", {}).get("author", {}).get("date")
                
                except urllib.error.URLError:
                    continue
            
            return file_changes
        except urllib.error.URLError as e:
            print(f"Error analyzing content performance: {e}")
            return None
    
    def determine_optimal_timing(self):
        """Analyze commit timing to determine optimal update times"""
        try:
            with urllib.request.urlopen(f"{self.base_url}/commits") as response:
                commits = json.loads(response.read().decode('utf-8'))
            
            # Analyze commit times
            commit_hours = []
            commit_days = []
            
            for commit in commits[:50]:  # Analyze last 50 commits
                date_str = commit.get("commit", {}).get("author", {}).get("date")
                if date_str:
                    try:
                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        commit_hours.append(date_obj.hour)
                        commit_days.append(date_obj.strftime("%A"))
                    except ValueError:
                        continue
            
            if not commit_hours:
                return None
            
            # Find most common hours and days
            from collections import Counter
            hour_counts = Counter(commit_hours)
            day_counts = Counter(commit_days)
            
            optimal_timing = {
                "best_hours": [hour for hour, count in hour_counts.most_common(3)],
                "best_days": [day for day, count in day_counts.most_common(3)],
                "total_commits_analyzed": len(commit_hours),
                "analysis_date": datetime.now().isoformat()
            }
            
            return optimal_timing
        except urllib.error.URLError as e:
            print(f"Error determining optimal timing: {e}")
            return None
    
    def save_analytics_data(self, data):
        """Save analytics data to JSON file"""
        try:
            # Load existing data if file exists
            existing_data = []
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    existing_data = json.load(f)
            
            # Add new data
            existing_data.append(data)
            
            # Save updated data
            with open(self.analytics_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            print(f"Analytics data saved to {self.analytics_file}")
            return True
        except Exception as e:
            print(f"Error saving analytics data: {e}")
            return False
    
    def save_content_performance(self, content_data):
        """Save content performance data to CSV file"""
        try:
            if not content_data:
                return False
            
            # Write CSV header
            with open(self.content_performance_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['File', 'Change Count', 'Additions', 'Deletions', 'Last Changed'])
                
                # Write data
                for filename, data in content_data.items():
                    writer.writerow([
                        filename,
                        data['change_count'],
                        data['additions'],
                        data['deletions'],
                        data['last_changed']
                    ])
            
            print(f"Content performance data saved to {self.content_performance_file}")
            return True
        except Exception as e:
            print(f"Error saving content performance data: {e}")
            return False
    
    def generate_analytics_report(self):
        """Generate comprehensive analytics report"""
        print("=" * 50)
        print("GITHUB ANALYTICS REPORT")
        print("=" * 50)
        print(f"Repository: {self.repo_owner}/{self.repo_name}")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Repository Stats
        print("📊 REPOSITORY STATISTICS")
        print("-" * 30)
        stats = self.get_repository_stats()
        if stats:
            print(f"⭐ Stars: {stats['stars']}")
            print(f"🍴 Forks: {stats['forks']}")
            print(f"👀 Watchers: {stats['watchers']}")
            print(f"🐛 Open Issues: {stats['open_issues']}")
            print(f"📦 Size: {stats['size']} KB")
            print(f"📅 Created: {stats['created_at']}")
            print(f"🔄 Updated: {stats['updated_at']}")
        print()
        
        # Recent Commits
        print("📝 RECENT COMMITS")
        print("-" * 30)
        commits = self.get_commit_activity()
        if commits:
            for i, commit in enumerate(commits[:5], 1):
                print(f"{i}. {commit['message'][:50]}...")
                print(f"   Author: {commit['author']}")
                print(f"   Date: {commit['date']}")
                print()
        print()
        
        # Issues Activity
        print("🐛 ISSUES ACTIVITY")
        print("-" * 30)
        issues = self.get_issues_activity()
        if issues:
            for i, issue in enumerate(issues[:5], 1):
                print(f"{i}. #{issue['number']}: {issue['title'][:40]}...")
                print(f"   State: {issue['state']} | Comments: {issue['comments']}")
                print()
        print()
        
        # Content Performance
        print("📈 CONTENT PERFORMANCE")
        print("-" * 30)
        content_perf = self.analyze_content_performance()
        if content_perf:
            # Sort by change count
            sorted_content = sorted(content_perf.items(), key=lambda x: x[1]['change_count'], reverse=True)
            
            for filename, data in sorted_content[:5]:
                print(f"📄 {filename}")
                print(f"   Changes: {data['change_count']} | +{data['additions']} -{data['deletions']}")
                print(f"   Last changed: {data['last_changed']}")
                print()
        print()
        
        # Optimal Timing
        print("⏰ OPTIMAL UPDATE TIMING")
        print("-" * 30)
        timing = self.determine_optimal_timing()
        if timing:
            print(f"🕐 Best Hours: {', '.join(map(str, timing['best_hours']))}")
            print(f"📅 Best Days: {', '.join(timing['best_days'])}")
            print(f"📊 Based on {timing['total_commits_analyzed']} commits")
        print()
        
        print("=" * 50)
        print("END OF REPORT")
        print("=" * 50)
        
        # Save data
        analytics_data = {
            "timestamp": datetime.now().isoformat(),
            "repository_stats": stats,
            "recent_commits": commits[:5] if commits else [],
            "issues_activity": issues[:5] if issues else [],
            "content_performance": content_perf,
            "optimal_timing": timing
        }
        
        self.save_analytics_data(analytics_data)
        
        if content_perf:
            self.save_content_performance(content_perf)

def main():
    """Main function to run analytics"""
    print("🚀 Starting GitHub Analytics...")
    
    # Initialize analytics
    analytics = GitHubAnalytics()
    
    # Generate report
    analytics.generate_analytics_report()
    
    print("\n💡 Tips for using this analytics:")
    print("1. Run this script weekly to track progress")
    print("2. Use content performance to focus on high-engagement files")
    print("3. Schedule updates during optimal timing hours")
    print("4. Monitor stars/forks growth trends")
    print("5. Adjust content strategy based on analytics")

if __name__ == "__main__":
    main()