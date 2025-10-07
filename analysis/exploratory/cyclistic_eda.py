# Cyclistic Bike Share - Comprehensive Exploratory Data Analysis
# Author: Omar Essam El-Din Mohamed
# Date: Current Date
# Purpose: Comprehensive exploratory analysis of bike-share data using Python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import os
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
# Consistent colors for member types: ['casual', 'member'] order assumed
colors = ['#FF6B6B', '#4ECDC4']
# Helper to save figures as SVG into analysis/exploratory/figures
def _save_fig(fig, filename):
    out_dir = os.path.join('analysis', 'exploratory', 'figures')
    os.makedirs(out_dir, exist_ok=True)
    fig.savefig(os.path.join(out_dir, filename), format='svg')

# =====================================================
# DATA LOADING AND PREPARATION
# =====================================================

def load_cyclistic_data(file_path):
    """Load and prepare Cyclistic data for analysis"""
    print(f"📥 Loading data from: {file_path}")
    
    # Read the data
    df = pd.read_csv(file_path)
    
    # Convert datetime columns
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    
    # Calculate ride duration
    df['ride_duration_minutes'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
    
    # Add time-based features
    df['hour_of_day'] = df['started_at'].dt.hour
    df['day_of_week'] = df['started_at'].dt.dayofweek
    df['day_name'] = df['started_at'].dt.day_name()
    df['month'] = df['started_at'].dt.month
    df['month_name'] = df['started_at'].dt.month_name()
    df['is_weekend'] = df['day_of_week'].isin([5, 6])
    df['day_type'] = df['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
    
    # Add time of day categories
    df['time_of_day'] = pd.cut(df['hour_of_day'], 
                              bins=[0, 6, 12, 18, 24], 
                              labels=['Night', 'Morning', 'Afternoon', 'Evening'],
                              include_lowest=True)
    
    print(f"✅ Successfully loaded {len(df):,} records")
    return df

# =====================================================
# DATA OVERVIEW AND QUALITY ASSESSMENT
# =====================================================

def assess_data_quality(df):
    """Comprehensive data quality assessment"""
    print("\n" + "="*60)
    print("📊 DATA QUALITY ASSESSMENT")
    print("="*60)
    
    # Basic information
    print(f"📋 Dataset Overview:")
    print(f"   • Total records: {len(df):,}")
    print(f"   • Date range: {df['started_at'].min()} to {df['started_at'].max()}")
    print(f"   • Columns: {len(df.columns)}")
    
    # Missing values
    missing_summary = pd.DataFrame({
        'variable': df.columns,
        'missing_count': df.isnull().sum(),
        'missing_percentage': (df.isnull().sum() / len(df)) * 100
    })
    
    print(f"\n🔍 Missing Values Summary:")
    missing_with_values = missing_summary[missing_summary['missing_count'] > 0]
    if not missing_with_values.empty:
        for _, row in missing_with_values.iterrows():
            print(f"   • {row['variable']:<25}: {row['missing_count']:8,} ({row['missing_percentage']:5.1f}%)")
    else:
        print("   ✅ No missing values found!")
    
    # Data types
    print(f"\n📝 Data Types:")
    for col, dtype in df.dtypes.items():
        print(f"   • {col:<25}: {dtype}")
    
    return missing_summary

# =====================================================
# MEMBER TYPE ANALYSIS
# =====================================================

def analyze_member_types(df):
    """Analyze member vs casual rider patterns"""
    print("\n" + "="*60)
    print("👥 MEMBER TYPE ANALYSIS")
    print("="*60)
    
    # Distribution
    member_dist = df['member_casual'].value_counts()
    member_pct = df['member_casual'].value_counts(normalize=True) * 100
    
    print("📊 Member Distribution:")
    for member_type, count in member_dist.items():
        pct = member_pct[member_type]
        print(f"   • {member_type:<10}: {count:8,} ({pct:5.1f}%)")
    
    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar chart
    colors = ['#FF6B6B', '#4ECDC4']
    bars = ax1.bar(member_dist.index, member_dist.values, color=colors, alpha=0.8)
    ax1.set_title('Distribution of Member Types', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Member Type')
    ax1.set_ylabel('Number of Rides')
    
    # Add percentage labels
    for bar, count, pct in zip(bars, member_dist.values, member_pct.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'{count:,}\n({pct:.1f}%)', ha='center', va='bottom')
    
    # Pie chart
    ax2.pie(member_dist.values, labels=member_dist.index, colors=colors, 
            autopct='%1.1f%%', startangle=90)
    ax2.set_title('Member Type Percentage', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    _save_fig(fig, 'member_types.svg')
    plt.show()
    
    return member_dist, member_pct

# =====================================================
# RIDE DURATION ANALYSIS
# =====================================================

def analyze_ride_duration(df):
    """Comprehensive ride duration analysis"""
    print("\n" + "="*60)
    print("⏱️ RIDE DURATION ANALYSIS")
    print("="*60)
    
    # Filter out unrealistic durations
    df_clean = df[(df['ride_duration_minutes'] > 0) & (df['ride_duration_minutes'] <= 1440)]
    
    # Statistics by member type
    duration_stats = df_clean.groupby('member_casual')['ride_duration_minutes'].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(2)
    
    print("📈 Duration Statistics by Member Type:")
    print(duration_stats)
    
    # Visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Histogram
    for i, member_type in enumerate(df_clean['member_casual'].unique()):
        data = df_clean[df_clean['member_casual'] == member_type]['ride_duration_minutes']
        ax1.hist(data, bins=30, alpha=0.7, label=member_type, color=colors[i])
    
    ax1.set_title('Distribution of Ride Durations by Member Type', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Ride Duration (minutes)')
    ax1.set_ylabel('Frequency')
    ax1.set_xlim(0, 120)  # Focus on rides under 2 hours
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Box plot
    df_clean.boxplot(column='ride_duration_minutes', by='member_casual', ax=ax2)
    ax2.set_title('Ride Duration Comparison: Members vs Casual Riders', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Member Type')
    ax2.set_ylabel('Ride Duration (minutes)')
    ax2.set_ylim(0, 60)  # Focus on rides under 1 hour
    plt.suptitle('')  # Remove default title
    
    # Violin plot
    sns.violinplot(data=df_clean, x='member_casual', y='ride_duration_minutes', ax=ax3)
    ax3.set_title('Duration Distribution Shape by Member Type', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Member Type')
    ax3.set_ylabel('Ride Duration (minutes)')
    ax3.set_ylim(0, 60)
    
    # Statistical summary
    ax4.axis('off')
    # Build a summary text block per member type
    blocks = []
    for member_type, stats in duration_stats.iterrows():
        block = "\n".join([
            f"{member_type.upper()} RIDERS:",
            f"• Average Duration: {stats['mean']:.1f} minutes",
            f"• Median Duration: {stats['median']:.1f} minutes",
            f"• Total Rides: {int(stats['count']):,}",
            f"• Standard Deviation: {stats['std']:.1f} minutes",
            ""
        ])
        blocks.append(block)
    stats_text = "\n".join(blocks)
    
    ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    ax4.set_title('Key Statistics Summary', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    _save_fig(fig, 'ride_duration.svg')
    plt.show()
    
    return duration_stats

# =====================================================
# TIME-BASED ANALYSIS
# =====================================================

def analyze_time_patterns(df):
    """Analyze time-based usage patterns"""
    print("\n" + "="*60)
    print("🕐 TIME-BASED USAGE ANALYSIS")
    print("="*60)
    
    # Hourly usage patterns
    hourly_usage = df.groupby(['hour_of_day', 'member_casual']).size().unstack(fill_value=0)
    
    # Day of week usage
    daily_usage = df.groupby(['day_name', 'member_casual']).size().unstack(fill_value=0)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_usage = daily_usage.reindex(day_order)
    
    # Weekend vs weekday usage
    weekend_usage = df.groupby(['is_weekend', 'member_casual']).size().unstack(fill_value=0)
    weekend_usage.index = ['Weekday', 'Weekend']
    
    # Monthly usage
    monthly_usage = df.groupby(['month_name', 'member_casual']).size().unstack(fill_value=0)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_usage = monthly_usage.reindex([m for m in month_order if m in monthly_usage.index])
    
    # Visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Hourly usage
    hourly_usage.plot(kind='line', marker='o', ax=ax1, color=colors)
    ax1.set_title('Ride Count by Hour of Day', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Number of Rides')
    ax1.legend(title='Member Type')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(range(0, 24, 2))
    
    # Day of week usage
    daily_usage.plot(kind='bar', ax=ax2, color=colors)
    ax2.set_title('Ride Count by Day of Week', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Day of Week')
    ax2.set_ylabel('Number of Rides')
    ax2.legend(title='Member Type')
    ax2.tick_params(axis='x', rotation=45)
    
    # Weekend vs weekday usage
    weekend_usage.plot(kind='bar', ax=ax3, color=colors)
    ax3.set_title('Weekend vs Weekday Usage', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Day Type')
    ax3.set_ylabel('Number of Rides')
    ax3.legend(title='Member Type')
    ax3.tick_params(axis='x', rotation=0)
    
    # Monthly usage
    monthly_usage.plot(kind='line', marker='o', ax=ax4, color=colors)
    ax4.set_title('Monthly Usage Pattern', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Month')
    ax4.set_ylabel('Number of Rides')
    ax4.legend(title='Member Type')
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    _save_fig(fig, 'time_patterns.svg')
    plt.show()
    
    # Summary statistics
    print("\n📊 Usage Pattern Summary:")
    print("\n🕐 Peak Usage Hours:")
    for member_type in df['member_casual'].unique():
        peak_hour = hourly_usage[member_type].idxmax()
        peak_count = hourly_usage[member_type].max()
        print(f"   • {member_type.title()}: Hour {peak_hour} ({peak_count:,} rides)")
    
    print("\n📅 Weekend vs Weekday Usage:")
    for member_type in df['member_casual'].unique():
        weekend_pct = (weekend_usage.loc['Weekend', member_type] / 
                      weekend_usage[member_type].sum()) * 100
        print(f"   • {member_type.title()}: {weekend_pct:.1f}% weekend usage")
    
    return hourly_usage, daily_usage, weekend_usage, monthly_usage

# =====================================================
# BIKE TYPE ANALYSIS
# =====================================================

def analyze_bike_types(df):
    """Analyze bike type preferences and usage patterns"""
    print("\n" + "="*60)
    print("🚴 BIKE TYPE ANALYSIS")
    print("="*60)
    
    # Bike type usage by member type
    bike_preferences = df.groupby(['rideable_type', 'member_casual']).size().unstack(fill_value=0)
    bike_percentages = df.groupby('rideable_type')['member_casual'].value_counts(normalize=True).unstack(fill_value=0)
    
    print("📊 Bike Type Usage by Member Type:")
    print(bike_preferences)
    
    print("\n📈 Bike Type Usage Percentages:")
    print(bike_percentages.round(3))
    
    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Bike type usage counts
    bike_preferences.plot(kind='bar', ax=ax1, color=colors)
    ax1.set_title('Bike Type Usage by Member Type', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Bike Type')
    ax1.set_ylabel('Number of Rides')
    ax1.legend(title='Member Type')
    ax1.tick_params(axis='x', rotation=45)
    
    # Bike type usage percentages
    bike_percentages.plot(kind='bar', stacked=True, ax=ax2, color=colors)
    ax2.set_title('Bike Type Usage Percentage', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Bike Type')
    ax2.set_ylabel('Percentage')
    ax2.legend(title='Member Type')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    return bike_preferences, bike_percentages

# =====================================================
# STATION ANALYSIS
# =====================================================

def analyze_stations(df):
    """Analyze station usage patterns"""
    print("\n" + "="*60)
    print("🚉 STATION USAGE ANALYSIS")
    print("="*60)
    
    # Top start stations
    top_start = df['start_station_name'].value_counts().head(10)
    
    print("🏆 Top 10 Start Stations:")
    for i, (station, count) in enumerate(top_start.items(), 1):
        print(f"   {i:2d}. {station:<30}: {count:6,} rides")
    
    # Top end stations
    top_end = df['end_station_name'].value_counts().head(10)
    
    print("\n🏆 Top 10 End Stations:")
    for i, (station, count) in enumerate(top_end.items(), 1):
        print(f"   {i:2d}. {station:<30}: {count:6,} rides")
    
    # Station usage by member type
    start_by_member = df.groupby(['start_station_name', 'member_casual']).size().unstack(fill_value=0)
    top_stations_member = start_by_member.loc[top_start.index[:5]]
    
    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Top start stations
    top_start.head(10).plot(kind='bar', ax=ax1, color='skyblue', alpha=0.8)
    ax1.set_title('Top 10 Start Stations', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Station Name')
    ax1.set_ylabel('Number of Rides')
    ax1.tick_params(axis='x', rotation=45)
    
    # Top stations by member type
    top_stations_member.plot(kind='bar', ax=ax2, color=colors)
    ax2.set_title('Top 5 Stations by Member Type', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Station Name')
    ax2.set_ylabel('Number of Rides')
    ax2.legend(title='Member Type')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    _save_fig(fig, 'stations.svg')
    plt.show()
    
    return top_start, top_end, top_stations_member

# =====================================================
# COMPARATIVE ANALYSIS
# =====================================================

def comparative_analysis(df):
    """Comprehensive comparative analysis between member types"""
    print("\n" + "="*60)
    print("📊 COMPARATIVE ANALYSIS: MEMBERS VS CASUAL RIDERS")
    print("="*60)
    
    # Key metrics comparison
    comparison_metrics = df.groupby('member_casual').agg(
        total_rides=('ride_id', 'count'),
        avg_duration=('ride_duration_minutes', 'mean'),
        median_duration=('ride_duration_minutes', 'median'),
        weekend_rides=('is_weekend', 'sum')
    ).round(2)
    
    comparison_metrics['weekday_rides'] = comparison_metrics['total_rides'] - comparison_metrics['weekend_rides']
    comparison_metrics['weekend_percentage'] = (comparison_metrics['weekend_rides'] / comparison_metrics['total_rides'] * 100).round(2)
    
    print("📈 Key Metrics Comparison:")
    print(comparison_metrics)
    
    # Time-based patterns
    time_patterns = df.groupby(['member_casual', 'time_of_day']).size().unstack(fill_value=0)
    time_percentages = time_patterns.div(time_patterns.sum(axis=1), axis=0) * 100
    
    print("\n🕐 Time of Day Usage Patterns:")
    print(time_percentages.round(2))
    
    # Visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Duration comparison
    comparison_metrics[['avg_duration', 'median_duration']].plot(kind='bar', ax=ax1, color=['lightblue', 'lightcoral'])
    ax1.set_title('Average vs Median Duration by Member Type', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Member Type')
    ax1.set_ylabel('Duration (minutes)')
    ax1.legend(['Average', 'Median'])
    ax1.tick_params(axis='x', rotation=0)
    
    # Weekend usage
    comparison_metrics['weekend_percentage'].plot(kind='bar', ax=ax2, color='lightgreen', alpha=0.8)
    ax2.set_title('Weekend Usage Percentage by Member Type', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Member Type')
    ax2.set_ylabel('Weekend Usage (%)')
    ax2.tick_params(axis='x', rotation=0)
    
    # Time of day patterns
    time_percentages.plot(kind='bar', ax=ax3, color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])
    ax3.set_title('Time of Day Usage Patterns', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Member Type')
    ax3.set_ylabel('Percentage of Rides')
    ax3.legend(title='Time of Day')
    ax3.tick_params(axis='x', rotation=0)
    
    # Total rides comparison
    comparison_metrics['total_rides'].plot(kind='bar', ax=ax4, color='gold', alpha=0.8)
    ax4.set_title('Total Rides by Member Type', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Member Type')
    ax4.set_ylabel('Total Rides')
    ax4.tick_params(axis='x', rotation=0)
    
    plt.tight_layout()
    _save_fig(fig, 'comparative_analysis.svg')
    plt.show()
    
    return comparison_metrics, time_patterns

# =====================================================
# MAIN EXECUTION FUNCTION
# =====================================================

def run_comprehensive_analysis(file_path):
    """Run the complete exploratory data analysis"""
    print("🚀 Starting Comprehensive Cyclistic Data Analysis")
    print("="*80)
    
    # Load data
    df = load_cyclistic_data(file_path)
    
    # Data quality assessment
    missing_summary = assess_data_quality(df)
    
    # Member type analysis
    member_dist, member_pct = analyze_member_types(df)
    
    # Ride duration analysis
    duration_stats = analyze_ride_duration(df)
    
    # Time-based analysis
    hourly_usage, daily_usage, weekend_usage, monthly_usage = analyze_time_patterns(df)
    
    # Bike type analysis
    bike_preferences, bike_percentages = analyze_bike_types(df)
    
    # Station analysis
    top_start, top_end, top_stations_member = analyze_stations(df)
    
    # Comparative analysis
    comparison_metrics, time_patterns = comparative_analysis(df)
    
    # Export tabular results to CSV for downstream use
    try:
        os.makedirs('analysis/exploratory', exist_ok=True)
        duration_stats.to_csv('analysis/exploratory/duration_stats.csv')
        comparison_metrics.to_csv('analysis/exploratory/comparison_metrics.csv')
        top_start.to_csv('analysis/exploratory/top_start_stations.csv')
        top_end.to_csv('analysis/exploratory/top_end_stations.csv')
        
        # Additional exports for report and portfolio
        missing_summary.to_csv('analysis/exploratory/missing_summary.csv', index=False)
        bike_preferences.to_csv('analysis/exploratory/bike_preferences.csv')
        bike_percentages.to_csv('analysis/exploratory/bike_percentages.csv', index=False)
        hourly_usage.to_csv('analysis/exploratory/hourly_usage.csv')
        daily_usage.to_csv('analysis/exploratory/daily_usage.csv')
        weekend_usage.to_csv('analysis/exploratory/weekend_usage.csv')
        monthly_usage.to_csv('analysis/exploratory/monthly_usage.csv')
        time_patterns.to_csv('analysis/exploratory/time_patterns.csv')
        top_stations_member.to_csv('analysis/exploratory/top_stations_member.csv')
        
        # Member distribution combining counts and percentages
        member_distribution_df = pd.DataFrame({
            'member_casual': member_dist.index,
            'count': member_dist.values,
            'percentage': [member_pct[m] for m in member_dist.index]
        })
        member_distribution_df.to_csv('analysis/exploratory/member_distribution.csv', index=False)
    except Exception as e:
        print(f"⚠️ Failed to export CSVs: {e}")
    
    # Summary insights
    print("\n" + "="*80)
    print("🎯 KEY INSIGHTS SUMMARY")
    print("="*80)
    
    print("\n1. 📊 MEMBER DISTRIBUTION:")
    for member_type, count in member_dist.items():
        pct = member_pct[member_type]
        print(f"   • {member_type.title()}: {count:,} rides ({pct:.1f}%)")
    
    print("\n2. ⏱️ DURATION PATTERNS:")
    for member_type, stats in duration_stats.iterrows():
        print(f"   • {member_type.title()}: Average {stats['mean']:.1f} minutes, Median {stats['median']:.1f} minutes")
    
    print("\n3. 🕐 USAGE PATTERNS:")
    for member_type in df['member_casual'].unique():
        weekend_pct = (weekend_usage.loc['Weekend', member_type] / weekend_usage[member_type].sum()) * 100
        peak_hour = hourly_usage[member_type].idxmax()
        print(f"   • {member_type.title()}: {weekend_pct:.1f}% weekend usage, Peak at hour {peak_hour}")
    
    print("\n4. 🚴 BIKE PREFERENCES:")
    for bike_type in df['rideable_type'].value_counts().index:
        count = df['rideable_type'].value_counts()[bike_type]
        pct = (count / len(df)) * 100
        print(f"   • {bike_type.replace('_', ' ').title()}: {count:,} rides ({pct:.1f}%)")
    
    print("\n✅ Analysis Complete! All insights generated successfully.")
    
    return {
        'data': df,
        'missing_summary': missing_summary,
        'member_distribution': member_dist,
        'duration_stats': duration_stats,
        'hourly_usage': hourly_usage,
        'daily_usage': daily_usage,
        'weekend_usage': weekend_usage,
        'monthly_usage': monthly_usage,
        'bike_preferences': bike_preferences,
        'top_stations': top_start,
        'comparison_metrics': comparison_metrics
    }

# =====================================================
# EXAMPLE USAGE
# =====================================================

if __name__ == "__main__":
    # Example usage - replace with your actual file path
    file_path = "data/processed/cyclistic_cleaned.csv"
    
    try:
        results = run_comprehensive_analysis(file_path)
        print("\n🎉 Analysis completed successfully!")
        print("📁 Results saved in the 'results' dictionary")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        print("📝 Please update the file_path variable with the correct path to your data")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        print("🔧 Please check your data format and try again")
