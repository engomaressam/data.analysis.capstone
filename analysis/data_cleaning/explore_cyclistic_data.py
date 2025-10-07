# Cyclistic Data Exploration - Python Version
# Author: Omar Essam El-Din Mohamed
# Date: Current Date
# Purpose: Explore the downloaded Cyclistic data files using Python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# =====================================================
# DATA FILE DISCOVERY
# =====================================================

def find_csv_files():
    """Find all CSV files in the raw data directory"""
    raw_dir = "data/raw"
    
    # Get all subdirectories
    subdirs = [d for d in os.listdir(raw_dir) if os.path.isdir(os.path.join(raw_dir, d))]
    
    # Find CSV files in each subdirectory
    csv_files = []
    for subdir in subdirs:
        subdir_path = os.path.join(raw_dir, subdir)
        files = glob.glob(os.path.join(subdir_path, "*.csv"))
        csv_files.extend(files)
    
    return sorted(csv_files)

# Find all CSV files
csv_files = find_csv_files()

print(f"Found {len(csv_files)} CSV files:")
for i, file in enumerate(csv_files, 1):
    print(f"{i:2d}: {file}")

# =====================================================
# SAMPLE FILE ANALYSIS
# =====================================================

def analyze_csv_file(file_path):
    """Analyze a single CSV file"""
    print("\n" + "="*80)
    print(f"ANALYZING FILE: {file_path}")
    print("="*80)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print("❌ File not found!")
        return None
    
    # Get file info
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    
    print(f"📁 File size: {file_size:.2f} MB")
    print(f"📅 Last modified: {mod_time}")
    
    try:
        # Read first few rows to check structure
        sample_data = pd.read_csv(file_path, nrows=5)
        
        print(f"📊 Columns found: {len(sample_data.columns)}")
        print("📋 Column names:")
        for i, col in enumerate(sample_data.columns, 1):
            print(f"  {i:2d}: {col}")
        
        # Check data types
        print("\n🔍 Data types:")
        for col in sample_data.columns:
            dtype = sample_data[col].dtype
            print(f"  {col:<25}: {dtype}")
        
        # Show sample data
        print("\n📄 Sample data (first 3 rows):")
        print(sample_data.head(3))
        
        return sample_data
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

# =====================================================
# ANALYZE RECENT FILES
# =====================================================

# Focus on recent files (2024 data)
recent_files = [f for f in csv_files if '2024' in f]

if recent_files:
    print("\n🎯 FOCUSING ON RECENT FILES (2024):")
    
    # Analyze first few recent files
    files_to_analyze = recent_files[:3]
    
    for file in files_to_analyze:
        analyze_csv_file(file)
else:
    print("\n⚠️ No 2024 files found. Analyzing available files...")
    files_to_analyze = csv_files[:3]
    
    for file in files_to_analyze:
        analyze_csv_file(file)

# =====================================================
# LOAD AND ANALYZE ONE COMPLETE FILE
# =====================================================

# Select a file for complete analysis
if recent_files:
    target_file = recent_files[0]  # Use first recent file
else:
    target_file = csv_files[0]     # Use first available file

print("\n" + "="*80)
print(f"COMPLETE ANALYSIS OF: {target_file}")
print("="*80)

if os.path.exists(target_file):
    # Read the complete file
    print("📥 Loading complete dataset...")
    
    try:
        # Read the file
        cyclistic_data = pd.read_csv(target_file)
        
        print(f"✅ Successfully loaded {len(cyclistic_data):,} records")
        print(f"📊 Total columns: {len(cyclistic_data.columns)}")
        
        # =====================================================
        # DATA OVERVIEW
        # =====================================================
        
        print("\n📋 DATA OVERVIEW:")
        print(f"Records: {len(cyclistic_data):,}")
        print(f"Columns: {len(cyclistic_data.columns)}")
        
        # Column information
        print("\n📝 Column Details:")
        for i, (col_name, col_data) in enumerate(cyclistic_data.items(), 1):
            non_null = col_data.notna().sum()
            null_pct = (col_data.isna().sum() / len(cyclistic_data)) * 100
            print(f"  {i:2d}. {col_name:<25} | {str(col_data.dtype):<10} | {non_null:8,} non-null ({null_pct:5.1f}% null)")
        
        # =====================================================
        # DATA QUALITY ASSESSMENT
        # =====================================================
        
        print("\n🔍 DATA QUALITY ASSESSMENT:")
        
        # Missing values summary
        missing_summary = pd.DataFrame({
            'variable': cyclistic_data.columns,
            'missing_count': cyclistic_data.isnull().sum(),
            'missing_percentage': (cyclistic_data.isnull().sum() / len(cyclistic_data)) * 100
        })
        
        print("\nMissing Values:")
        missing_with_values = missing_summary[missing_summary['missing_count'] > 0]
        if not missing_with_values.empty:
            for _, row in missing_with_values.iterrows():
                print(f"  {row['variable']:<25}: {row['missing_count']:8,} ({row['missing_percentage']:5.1f}%)")
        else:
            print("  No missing values found!")
        
        # =====================================================
        # MEMBER TYPE ANALYSIS
        # =====================================================
        
        if 'member_casual' in cyclistic_data.columns:
            print("\n👥 MEMBER TYPE DISTRIBUTION:")
            member_dist = cyclistic_data['member_casual'].value_counts(dropna=False)
            member_pct = cyclistic_data['member_casual'].value_counts(normalize=True, dropna=False) * 100
            
            for member_type, count in member_dist.items():
                pct = member_pct[member_type]
                print(f"  {str(member_type):<10}: {count:8,} ({pct:5.1f}%)")
        
        # =====================================================
        # BIKE TYPE ANALYSIS
        # =====================================================
        
        if 'rideable_type' in cyclistic_data.columns:
            print("\n🚴 BIKE TYPE DISTRIBUTION:")
            bike_dist = cyclistic_data['rideable_type'].value_counts(dropna=False)
            bike_pct = cyclistic_data['rideable_type'].value_counts(normalize=True, dropna=False) * 100
            
            for bike_type, count in bike_dist.items():
                pct = bike_pct[bike_type]
                print(f"  {str(bike_type):<15}: {count:8,} ({pct:5.1f}%)")
        
        # =====================================================
        # DATE/TIME ANALYSIS
        # =====================================================
        
        if 'started_at' in cyclistic_data.columns:
            print("\n📅 DATE/TIME ANALYSIS:")
            
            # Convert to datetime
            cyclistic_data['started_at'] = pd.to_datetime(cyclistic_data['started_at'])
            cyclistic_data['ended_at'] = pd.to_datetime(cyclistic_data['ended_at'])
            
            print("Date range:")
            print(f"  Start: {cyclistic_data['started_at'].min()}")
            print(f"  End  : {cyclistic_data['started_at'].max()}")
            
            # Calculate duration
            cyclistic_data['ride_duration_minutes'] = (
                cyclistic_data['ended_at'] - cyclistic_data['started_at']
            ).dt.total_seconds() / 60
            
            print("\nRide Duration Statistics:")
            duration_stats = cyclistic_data['ride_duration_minutes'].describe()
            print(duration_stats)
            
            # Check for invalid durations
            invalid_durations = ((cyclistic_data['ride_duration_minutes'] <= 0) | 
                               (cyclistic_data['ride_duration_minutes'] > 1440)).sum()
            print(f"Invalid durations (<= 0 or > 24 hours): {invalid_durations:,}")
            
            # Add time-based features
            cyclistic_data['hour_of_day'] = cyclistic_data['started_at'].dt.hour
            cyclistic_data['day_of_week'] = cyclistic_data['started_at'].dt.dayofweek
            cyclistic_data['is_weekend'] = cyclistic_data['day_of_week'].isin([5, 6])
            cyclistic_data['month'] = cyclistic_data['started_at'].dt.month
            
        # =====================================================
        # STATION ANALYSIS
        # =====================================================
        
        if 'start_station_name' in cyclistic_data.columns:
            print("\n🚉 STATION ANALYSIS:")
            
            # Top start stations
            top_start = (cyclistic_data['start_station_name']
                        .value_counts()
                        .head(5))
            
            print("Top 5 Start Stations:")
            for i, (station, count) in enumerate(top_start.items(), 1):
                print(f"  {i:2d}. {station:<30}: {count:6,} rides")
        
        # =====================================================
        # VISUALIZATION CREATION
        # =====================================================
        
        print("\n📊 CREATING VISUALIZATIONS:")
        
        # Create output directory
        os.makedirs("analysis/exploratory", exist_ok=True)
        
        # 1. Member Type Distribution
        if 'member_casual' in cyclistic_data.columns:
            plt.figure(figsize=(10, 6))
            member_counts = cyclistic_data['member_casual'].value_counts()
            colors = ['#FF6B6B', '#4ECDC4']
            
            plt.subplot(1, 2, 1)
            member_counts.plot(kind='bar', color=colors, alpha=0.8)
            plt.title('Member Type Distribution')
            plt.xlabel('Member Type')
            plt.ylabel('Number of Rides')
            plt.xticks(rotation=0)
            
            # Add percentage labels
            total = member_counts.sum()
            for i, v in enumerate(member_counts.values):
                plt.text(i, v + total*0.01, f'{v:,}\n({v/total*100:.1f}%)', 
                        ha='center', va='bottom')
            
            plt.subplot(1, 2, 2)
            plt.pie(member_counts.values, labels=member_counts.index, 
                   colors=colors, autopct='%1.1f%%', startangle=90)
            plt.title('Member Type Percentage')
            
            plt.tight_layout()
            plt.savefig('analysis/exploratory/member_distribution.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        # 2. Ride Duration Analysis
        if 'ride_duration_minutes' in cyclistic_data.columns:
            plt.figure(figsize=(15, 5))
            
            # Duration distribution
            plt.subplot(1, 3, 1)
            plt.hist(cyclistic_data['ride_duration_minutes'], bins=50, alpha=0.7, edgecolor='black')
            plt.title('Ride Duration Distribution')
            plt.xlabel('Duration (minutes)')
            plt.ylabel('Frequency')
            plt.xlim(0, 120)  # Focus on rides under 2 hours
            
            # Duration by member type
            plt.subplot(1, 3, 2)
            if 'member_casual' in cyclistic_data.columns:
                for member_type in cyclistic_data['member_casual'].unique():
                    if pd.notna(member_type):
                        data = cyclistic_data[cyclistic_data['member_casual'] == member_type]['ride_duration_minutes']
                        plt.hist(data, bins=30, alpha=0.7, label=member_type)
                plt.title('Duration by Member Type')
                plt.xlabel('Duration (minutes)')
                plt.ylabel('Frequency')
                plt.legend()
                plt.xlim(0, 60)  # Focus on rides under 1 hour
            
            # Box plot
            plt.subplot(1, 3, 3)
            if 'member_casual' in cyclistic_data.columns:
                cyclistic_data.boxplot(column='ride_duration_minutes', by='member_casual', ax=plt.gca())
                plt.title('Duration Box Plot by Member Type')
                plt.xlabel('Member Type')
                plt.ylabel('Duration (minutes)')
                plt.ylim(0, 60)
            
            plt.tight_layout()
            plt.savefig('analysis/exploratory/duration_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        # 3. Time-based Analysis
        if 'hour_of_day' in cyclistic_data.columns and 'member_casual' in cyclistic_data.columns:
            plt.figure(figsize=(15, 10))
            
            # Hourly usage
            plt.subplot(2, 2, 1)
            hourly_usage = cyclistic_data.groupby(['hour_of_day', 'member_casual']).size().unstack(fill_value=0)
            hourly_usage.plot(kind='line', marker='o', ax=plt.gca())
            plt.title('Ride Count by Hour of Day')
            plt.xlabel('Hour of Day')
            plt.ylabel('Number of Rides')
            plt.legend(title='Member Type')
            plt.grid(True, alpha=0.3)
            
            # Day of week usage
            plt.subplot(2, 2, 2)
            daily_usage = cyclistic_data.groupby(['day_of_week', 'member_casual']).size().unstack(fill_value=0)
            day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            daily_usage.index = day_names
            daily_usage.plot(kind='bar', ax=plt.gca())
            plt.title('Ride Count by Day of Week')
            plt.xlabel('Day of Week')
            plt.ylabel('Number of Rides')
            plt.legend(title='Member Type')
            plt.xticks(rotation=45)
            
            # Weekend vs Weekday
            plt.subplot(2, 2, 3)
            weekend_usage = cyclistic_data.groupby(['is_weekend', 'member_casual']).size().unstack(fill_value=0)
            weekend_usage.index = ['Weekday', 'Weekend']
            weekend_usage.plot(kind='bar', ax=plt.gca())
            plt.title('Weekend vs Weekday Usage')
            plt.xlabel('Day Type')
            plt.ylabel('Number of Rides')
            plt.legend(title='Member Type')
            plt.xticks(rotation=0)
            
            # Monthly usage
            plt.subplot(2, 2, 4)
            monthly_usage = cyclistic_data.groupby(['month', 'member_casual']).size().unstack(fill_value=0)
            monthly_usage.plot(kind='line', marker='o', ax=plt.gca())
            plt.title('Monthly Usage Pattern')
            plt.xlabel('Month')
            plt.ylabel('Number of Rides')
            plt.legend(title='Member Type')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('analysis/exploratory/time_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        # 4. Bike Type Analysis
        if 'rideable_type' in cyclistic_data.columns and 'member_casual' in cyclistic_data.columns:
            plt.figure(figsize=(12, 5))
            
            # Bike type usage
            plt.subplot(1, 2, 1)
            bike_usage = cyclistic_data.groupby(['rideable_type', 'member_casual']).size().unstack(fill_value=0)
            bike_usage.plot(kind='bar', ax=plt.gca())
            plt.title('Bike Type Usage by Member Type')
            plt.xlabel('Bike Type')
            plt.ylabel('Number of Rides')
            plt.legend(title='Member Type')
            plt.xticks(rotation=45)
            
            # Bike type percentages
            plt.subplot(1, 2, 2)
            bike_pct = cyclistic_data.groupby('rideable_type')['member_casual'].value_counts(normalize=True).unstack(fill_value=0)
            bike_pct.plot(kind='bar', stacked=True, ax=plt.gca())
            plt.title('Bike Type Usage Percentage')
            plt.xlabel('Bike Type')
            plt.ylabel('Percentage')
            plt.legend(title='Member Type')
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig('analysis/exploratory/bike_type_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        # =====================================================
        # SAVE RESULTS
        # =====================================================
        
        # Save data quality summary
        missing_summary.to_csv('analysis/exploratory/data_quality_summary.csv', index=False)
        
        # Save member distribution
        if 'member_casual' in cyclistic_data.columns:
            member_df = pd.DataFrame({
                'member_type': member_dist.index,
                'count': member_dist.values,
                'percentage': member_pct.values
            })
            member_df.to_csv('analysis/exploratory/member_distribution.csv', index=False)
        
        # Save sample of data for further analysis
        sample_size = min(10000, len(cyclistic_data))
        sample_data = cyclistic_data.sample(n=sample_size, random_state=42)
        sample_data.to_csv('analysis/exploratory/sample_data.csv', index=False)
        
        # Save processed data
        cyclistic_data.to_csv('analysis/exploratory/processed_data.csv', index=False)
        
        print("\n✅ Analysis complete! Results saved to analysis/exploratory/")
        print("📁 Files created:")
        print("   • analysis/exploratory/data_quality_summary.csv")
        print("   • analysis/exploratory/member_distribution.csv")
        print("   • analysis/exploratory/sample_data.csv")
        print("   • analysis/exploratory/processed_data.csv")
        print("   • analysis/exploratory/member_distribution.png")
        print("   • analysis/exploratory/duration_analysis.png")
        print("   • analysis/exploratory/time_analysis.png")
        print("   • analysis/exploratory/bike_type_analysis.png")
        
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        
else:
    print(f"❌ Target file not found: {target_file}")

# =====================================================
# SUMMARY AND NEXT STEPS
# =====================================================

print("\n" + "="*80)
print("EXPLORATION SUMMARY AND NEXT STEPS")
print("="*80)

print(f"\n📋 What we accomplished:")
print(f"   ✅ Discovered {len(csv_files)} CSV files in the dataset")
print("   ✅ Analyzed file structure and data quality")
print("   ✅ Examined member types and bike types")
print("   ✅ Assessed date/time data and ride durations")
print("   ✅ Identified top stations and usage patterns")
print("   ✅ Created comprehensive visualizations")
print("   ✅ Saved results for further analysis")

print("\n🎯 Recommended next steps:")
print("   1. Review the data quality summary and visualizations")
print("   2. Plan data cleaning strategy based on findings")
print("   3. Implement data cleaning pipeline")
print("   4. Run comprehensive statistical analysis")
print("   5. Create interactive dashboards")
print("   6. Develop business recommendations")

print("\n🚀 Ready for the next phase of your capstone project!")
