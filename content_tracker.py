#!/usr/bin/env python3
"""
Content Performance Tracker
Tracks which content performs best and provides recommendations
"""

import json
import csv
from datetime import datetime
import os

class ContentTracker:
    def __init__(self):
        self.tracking_file = "content_performance_log.json"
        self.recommendations_file = "content_recommendations.json"
        
    def log_content_update(self, filename, update_type, description, impact_expected):
        """Log a content update for tracking"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "update_type": update_type,  # "major", "minor", "fix"
            "description": description,
            "impact_expected": impact_expected,  # "high", "medium", "low"
            "metrics_before": self.get_current_metrics(filename),
            "metrics_after": None  # To be filled later
        }
        
        # Load existing logs
        logs = []
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'r') as f:
                logs = json.load(f)
        
        # Add new log
        logs.append(log_entry)
        
        # Save updated logs
        with open(self.tracking_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        print(f"✅ Logged content update: {filename} ({update_type})")
        return log_entry
    
    def get_current_metrics(self, filename):
        """Get current metrics for a file (placeholder for actual metrics)"""
        # This would integrate with GitHub analytics in a full implementation
        return {
            "stars": 0,  # Would be repository stars
            "views": 0,  # Would be file views if available
            "engagement": 0  # Would be comments, forks, etc.
        }
    
    def update_metrics_after(self, log_entry, days_elapsed=7):
        """Update metrics after a period to measure impact"""
        # In a full implementation, this would fetch actual metrics
        log_entry["metrics_after"] = self.get_current_metrics(log_entry["filename"])
        log_entry["days_elapsed"] = days_elapsed
        
        # Calculate impact
        before = log_entry["metrics_before"]
        after = log_entry["metrics_after"]
        
        log_entry["impact_measured"] = {
            "stars_change": after["stars"] - before["stars"],
            "views_change": after["views"] - before["views"],
            "engagement_change": after["engagement"] - before["engagement"]
        }
        
        return log_entry
    
    def generate_recommendations(self):
        """Generate content recommendations based on performance"""
        recommendations = {
            "high_priority_updates": [],
            "content_to_promote": [],
            "content_to_improve": [],
            "timing_suggestions": []
        }
        
        # Load performance data
        if os.path.exists("content_performance.csv"):
            with open("content_performance.csv", 'r') as f:
                reader = csv.DictReader(f)
                content_data = list(reader)
            
            # Analyze content performance
            for row in content_data:
                change_count = int(row['Change Count'])
                filename = row['File']
                
                if change_count >= 3:
                    recommendations["content_to_promote"].append({
                        "file": filename,
                        "reason": f"High change count ({change_count}) indicates active engagement"
                    })
                elif change_count == 1:
                    recommendations["content_to_improve"].append({
                        "file": filename,
                        "reason": "Low change count suggests room for improvement"
                    })
        
        # Add timing suggestions based on analytics
        if os.path.exists("analytics_data.json"):
            with open("analytics_data.json", 'r') as f:
                analytics_data = json.load(f)
            
            if analytics_data:
                latest_analytics = analytics_data[-1]
                if latest_analytics.get("optimal_timing"):
                    timing = latest_analytics["optimal_timing"]
                    recommendations["timing_suggestions"] = [
                        f"Schedule updates during hours: {timing['best_hours']}",
                        f"Plan major releases on: {timing['best_days']}"
                    ]
        
        # Save recommendations
        with open(self.recommendations_file, 'w') as f:
            json.dump(recommendations, f, indent=2)
        
        return recommendations
    
    def display_recommendations(self):
        """Display content recommendations"""
        recommendations = self.generate_recommendations()
        
        print("=" * 50)
        print("📋 CONTENT RECOMMENDATIONS")
        print("=" * 50)
        print()
        
        if recommendations["content_to_promote"]:
            print("🚀 CONTENT TO PROMOTE:")
            print("-" * 30)
            for item in recommendations["content_to_promote"]:
                print(f"📄 {item['file']}")
                print(f"   Reason: {item['reason']}")
                print()
        
        if recommendations["content_to_improve"]:
            print("🔧 CONTENT TO IMPROVE:")
            print("-" * 30)
            for item in recommendations["content_to_improve"]:
                print(f"📄 {item['file']}")
                print(f"   Reason: {item['reason']}")
                print()
        
        if recommendations["timing_suggestions"]:
            print("⏰ TIMING SUGGESTIONS:")
            print("-" * 30)
            for suggestion in recommendations["timing_suggestions"]:
                print(f"💡 {suggestion}")
                print()
        
        print("=" * 50)
        print("END OF RECOMMENDATIONS")
        print("=" * 50)

def main():
    """Main function to run content tracker"""
    print("🎯 Content Performance Tracker")
    print()
    
    tracker = ContentTracker()
    
    # Example usage
    print("Example: Log a content update")
    print("Usage: tracker.log_content_update('README.md', 'major', 'Added success stories', 'high')")
    print()
    
    # Display current recommendations
    tracker.display_recommendations()
    
    print("\n💡 How to use:")
    print("1. Log content updates as you make them")
    print("2. Run analytics weekly: python3 github_analytics.py")
    print("3. Review recommendations regularly")
    print("4. Adjust content strategy based on data")

if __name__ == "__main__":
    main()