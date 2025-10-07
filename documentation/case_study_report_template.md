# Cyclistic Bike Share Analysis - Case Study Report

## Executive Summary

**Business Problem**: Cyclistic needs to understand how annual members and casual riders use bikes differently to design effective marketing strategies for converting casual riders to annual members.

**Analysis Approach**: Comprehensive analysis of 5,397,554 bike-share trips over 12 months using Python to clean and analyze usage patterns, with visuals saved as SVG for reproducibility.

**Key Findings**:
- Members account for 64.5% of rides; casual riders 35.5%
- Casual riders take longer rides (avg 20.2 min, median 12.0) vs members (avg 12.1 min, median 8.7)
- Weekend usage: casual 37.3%, member 23.6%; peak hour for both rider types is 17:00
- Electric bikes dominate usage (61.6%, 3,326,048 rides) vs classic bikes (38.4%, 2,071,506 rides)

**Recommendations**:
- Target weekend leisure riders with membership benefits and promotions
- Emphasize cost savings for frequent riders and commuters
- Offer member-exclusive perks (priority reservations, partner discounts)

---

## 1. Introduction

### 1.1 Background
Cyclistic is a bike-share program featuring more than 5,800 bicycles and 600 docking stations across Chicago. The company offers traditional bikes, reclining bikes, hand tricycles, and cargo bikes, making bike-share accessible to people with disabilities. The majority of riders (about 30%) use bikes to commute to work, while others ride for leisure.

### 1.2 Business Context
- **Director of Marketing**: Lily Moreno
- **Business Goal**: Design marketing strategies to convert casual riders to annual members
- **Success Metric**: Increase in annual membership conversions
- **Stakeholders**: Cyclistic executive team, marketing analytics team

### 1.3 Problem Statement
Cyclistic's finance analysts have concluded that annual members are much more profitable than casual riders. The marketing team needs to understand how annual members and casual riders use Cyclistic bikes differently to design effective conversion strategies.

### 1.4 Research Questions
1. How do annual members and casual riders use Cyclistic bikes differently?
2. Why would casual riders buy Cyclistic annual memberships?
3. How can Cyclistic use digital media to influence casual riders to become members?

---

## 2. Data Sources and Methodology

### 2.1 Data Sources
- **Primary Dataset**: Divvy's historical trip data (publicly available)
- **Data Portal**: https://www.divvybikes.com/system-data
- **Time Period**: October 2024 – September 2025
- **Data Size**: 5,397,554 trip records
- **License**: Divvy Data License Agreement

### 2.2 Data Dictionary
| Field | Type | Description |
|-------|------|-------------|
| ride_id | Character | Unique identifier for each ride |
| rideable_type | Character | Type of bike (electric, classic, docked) |
| started_at | DateTime | Start time and date |
| ended_at | DateTime | End time and date |
| start_station_name | Character | Starting station name |
| end_station_name | Character | Ending station name |
| member_casual | Character | Type of rider (member, casual) |

### 2.3 Methodology
1. **Data Collection**: Download monthly CSV files from Divvy data portal
2. **Data Cleaning**: Python (pandas) filtering and validation; remove outliers; handle missing stations as 'Unknown'
3. **Exploratory Analysis**: Python (pandas, numpy) summarization; compute rider-type comparisons and time patterns
4. **Visualization**: Matplotlib/Seaborn charts saved as SVG for reproducibility
5. **Business Recommendations**: Actionable insights for marketing team

---

## 3. Data Processing and Cleaning

### 3.1 Data Quality Assessment
- **Total Records**: 5,397,554 trip records
- **Data Completeness**: High completeness after cleaning; key fields present for analysis
- **Missing Values**: Station names with missing values set to 'Unknown'; critical fields validated
- **Outliers**: Removed rides < 1 minute and > 24 hours
- **Tables**: analysis/exploratory/missing_summary.csv

### 3.2 Cleaning Decisions Made
1. **Duration Filtering**: Removed rides < 1 minute and > 24 hours
2. **Null Handling**: Replaced missing station data with 'Unknown'
3. **Data Validation**: Ensured end time > start time
4. **Member Type**: Validated only 'member' and 'casual' values

### 3.3 Calculated Fields Added
- `ride_duration_minutes`: Trip duration in minutes
- `day_of_week`: Numeric day (0=Sunday, 6=Saturday)
- `hour_of_day`: Hour of start time (0-23)
- `month`: Month of start time (1-12)
- `day_type`: Weekend vs Weekday classification
- `time_of_day`: Morning, Afternoon, Evening, Night classification

---

## 4. Analysis and Findings

### 4.1 Ride Duration Analysis
Members vs Casual ride duration patterns were analyzed using cleaned data and summary statistics.

**Key Findings**:
- Casual riders average 20.2 minutes per ride (median 12.0)
- Members average 12.1 minutes per ride (median 8.7)
- Casual riders exhibit longer, leisure-oriented rides; members show shorter, commute-oriented rides

**Visualization**: Duration distribution and box plots
- Figures: analysis/exploratory/figures/ride_duration.svg, analysis/exploratory/figures/comparative_analysis.svg
- Tables: analysis/exploratory/duration_stats.csv

### 4.2 Time-Based Usage Patterns
**Daily Patterns**:
- Weekend usage: Casual 37.3% vs Member 23.6%
- Weekday usage is higher for members, indicating commute behavior

**Hourly Patterns**:
- Peak usage at 17:00 for both rider types

**Seasonal Patterns**:
- Monthly usage variations observed; higher ridership during warmer months (contextual)

**Visualization**: Time-of-day and day-type charts
- Figures: analysis/exploratory/figures/time_patterns.svg, analysis/exploratory/figures/comparative_analysis.svg
- Tables: analysis/exploratory/hourly_usage.csv, analysis/exploratory/daily_usage.csv, analysis/exploratory/weekend_usage.csv, analysis/exploratory/monthly_usage.csv, analysis/exploratory/time_patterns.csv

### 4.3 Geographic Analysis
**Popular Stations**:
- Top start and end stations identified with significant usage; downtown and commuter corridors dominate
- Distinct clustering patterns by rider type observed

**Visualization**: Top stations bar charts
- Figures: analysis/exploratory/figures/stations.svg
- Tables: analysis/exploratory/top_start_stations.csv, analysis/exploratory/top_end_stations.csv, analysis/exploratory/top_stations_member.csv

### 4.4 Bike Type Preferences
**Usage by Bike Type**:
- Electric Bike: 3,326,048 rides (61.6%)
- Classic Bike: 2,071,506 rides (38.4%)
- Members and casual riders both favor electric bikes; implications for fleet and pricing

**Visualization**: Member distribution and comparative charts
- Figures: analysis/exploratory/figures/member_types.svg, analysis/exploratory/figures/comparative_analysis.svg
- Tables: analysis/exploratory/bike_preferences.csv, analysis/exploratory/bike_percentages.csv, analysis/exploratory/comparison_metrics.csv

---

## 5. Key Insights and Patterns

### 5.1 Behavioral Differences
1. **Usage Purpose**:
   - Casual riders: Primarily weekend leisure
   - Members: Primarily weekday commuting

2. **Duration Patterns**:
   - Casual riders: Longer, more leisurely rides
   - Members: Shorter, more utilitarian rides

3. **Time Preferences**:
   - Casual riders: Peak usage on weekends and evenings
   - Members: Peak usage during weekday commute hours

### 5.2 Conversion Opportunities
1. **Cost-Benefit Analysis**:
   - Membership pricing is $99/year for new and returning riders (limited-time), with standard pricing listed as $143.90/year; members have free unlocks, unlimited 45‑min classic bike rides, and member ebike pricing at $0.19/min with minutes 31–45 capped at $5.70 <mcreference link="https://divvybikes.com/pricing" index="2">2</mcreference> <mcreference link="https://divvybikes.com/pricing/annual" index="4">4</mcreference>
   - Single rides cost $1 unlock + $0.19/min on classic bikes; ebikes for non‑members cost $1 unlock + $0.44/min <mcreference link="https://divvybikes.com/pricing/single-ride" index="5">5</mcreference> <mcreference link="https://divvybikes.com/pricing" index="2">2</mcreference>
   - Using observed average ride duration (20.2 min), the classic single‑ride cost is approximately $4.84 per ride; with membership at $99/year (~$8.25/month), the break‑even is about 1.7 classic rides per month; for ebike, non‑member cost is ~ $9.89 per ride versus member ebike ~$3.84 per ride, implying break‑even at ~1.36 ebike rides per month <mcreference link="https://divvybikes.com/pricing" index="2">2</mcreference> <mcreference link="https://divvybikes.com/pricing/single-ride" index="5">5</mcreference>
   - City announcement notes reduced membership pricing to $99 for new and lapsed members and minor price adjustments including member ebike rate $0.19/min <mcreference link="https://www.chicago.gov/city/en/depts/cdot/provdrs/bike/news/2025/july/-city-of-chicago-and-lyft-launch-major-divvy-membership-improvem.html" index="1">1</mcreference>

2. **Usage Thresholds**:
   - Classic bikes: At average ride length, membership becomes cost‑effective at ~2 rides/month; 4–8 rides/month yields substantial savings
   - Ebikes: At average ride length, membership becomes cost‑effective at ~2 rides/month; 3–4+ rides/month yields substantial savings

3. **Behavioral Triggers**:
   - Casual riders with increasing weekend frequency (2+ rides/month) and evening peaks are strong candidates for conversion
   - Seasonal spikes (late spring to summer) present timely promotion windows for conversion

---

## 6. Recommendations

### 6.1 Marketing Strategy Recommendations

#### 6.1.1 Target Audience Segmentation
1. **Weekend Leisure Riders**:
   - **Strategy**: Emphasize unlimited weekend access
   - **Message**: "Ride all weekend for less than the cost of two single rides"
   - **Channel**: Social media, weekend event partnerships

2. **Frequent Casual Riders**:
   - **Strategy**: Cost savings calculator and usage tracking
   - **Message**: "You could save $X per month with an annual membership"
   - **Channel**: Email marketing, in-app notifications

3. **Commuter Riders**:
   - **Strategy**: Reliability and convenience messaging
   - **Message**: "Skip the traffic, guarantee your ride"
   - **Channel**: Transit partnerships, corporate programs

#### 6.1.2 Digital Media Strategy
1. **Social Media Campaigns**:
   - Weekend adventure content for leisure riders
   - Commuter success stories for potential members
   - Cost savings testimonials

2. **Email Marketing**:
   - Usage-based conversion campaigns
   - Seasonal membership promotions
   - Member-exclusive event invitations

3. **Mobile App Features**:
   - Usage tracking and savings calculator
   - Member-exclusive bike reservations
   - Loyalty program integration

### 6.2 Product and Service Recommendations

#### 6.2.1 Membership Tiers
1. **Weekend Warrior**: Unlimited weekend rides
2. **Commuter Plus**: Weekday unlimited + weekend discounts
3. **Explorer**: Full unlimited access with premium perks

#### 6.2.2 Member Benefits
1. **Exclusive Access**: Priority bike reservations
2. **Partner Discounts**: Local business partnerships
3. **Community Events**: Member-only group rides and events

### 6.3 Implementation Roadmap

#### Phase 1: Quick Wins (1-2 months)
- [ ] Launch cost savings calculator
- [ ] Implement usage tracking notifications
- [ ] Create member-exclusive bike reservations

#### Phase 2: Campaign Launch (2-4 months)
- [ ] Deploy targeted social media campaigns
- [ ] Launch email marketing automation
- [ ] Establish corporate partnership program

#### Phase 3: Product Development (4-6 months)
- [ ] Develop membership tier options
- [ ] Create member community platform
- [ ] Implement loyalty program features

---

## 7. Success Metrics and KPIs

### 7.1 Primary Metrics
1. **Conversion Rate**: Percentage of casual riders converting to members
2. **Revenue Impact**: Increase in membership revenue
3. **Customer Lifetime Value**: Improvement in CLV

### 7.2 Secondary Metrics
1. **Engagement**: Increase in app usage and feature adoption
2. **Retention**: Annual membership renewal rates
3. **Satisfaction**: Member satisfaction scores

### 7.3 Measurement Plan
- **Baseline**: Current conversion rates and revenue
- **Testing**: A/B testing of different marketing approaches
- **Tracking**: Monthly reporting on key metrics
- **Optimization**: Continuous improvement based on results

---

## 8. Limitations and Assumptions

### 8.1 Data Limitations
1. **Privacy Constraints**: Data has been anonymized by Cyclistic
2. **Temporal Scope**: Analysis limited to 12 months of data
3. **Geographic Scope**: Limited to Chicago area

### 8.2 Assumptions Made
1. **Behavioral Consistency**: Past behavior predicts future behavior
2. **Market Conditions**: No major changes in bike-share market
3. **External Factors**: Weather and events impact usage patterns

### 8.3 Future Research Opportunities
1. **Customer Surveys**: Direct feedback from casual riders
2. **Pilot Programs**: Test different conversion strategies
3. **Competitive Analysis**: Benchmark against other bike-share programs

---

## 9. Conclusion

This analysis provides Cyclistic with data-driven insights into the behavioral differences between annual members and casual riders. The key findings reveal distinct usage patterns that can inform targeted marketing strategies for conversion.

**Key Takeaways**:
1. Casual riders and members have fundamentally different usage patterns
2. Cost savings and convenience are primary conversion drivers
3. Targeted marketing campaigns can effectively reach different rider segments

**Next Steps**:
1. Implement recommended marketing strategies
2. Monitor conversion metrics and optimize campaigns
3. Continuously analyze usage data for new insights

By leveraging these insights, Cyclistic can develop more effective marketing strategies that convert casual riders to annual members, ultimately driving increased revenue and customer loyalty.

---

## 10. Appendices

### Appendix A: Technical Documentation
- Data cleaning and analysis scripts (Python)
- EDA script: analysis/exploratory/cyclistic_eda.py
- Visualization files (SVG) in analysis/exploratory/figures
- Mirrored assets for publishing in portfolio/assets (figures and tables)
- Analysis code (R)
- Visualization files (Tableau)

### Appendix B: Additional Charts and Tables
- Detailed statistical analysis
- Geographic maps and station analysis
- Seasonal trend analysis
- Tables Index:
  - analysis/exploratory/missing_summary.csv
  - analysis/exploratory/duration_stats.csv
  - analysis/exploratory/hourly_usage.csv
  - analysis/exploratory/daily_usage.csv
  - analysis/exploratory/weekend_usage.csv
  - analysis/exploratory/monthly_usage.csv
  - analysis/exploratory/time_patterns.csv
  - analysis/exploratory/top_start_stations.csv
  - analysis/exploratory/top_end_stations.csv
  - analysis/exploratory/top_stations_member.csv
  - analysis/exploratory/bike_preferences.csv
  - analysis/exploratory/bike_percentages.csv
  - analysis/exploratory/comparison_metrics.csv

### Appendix C: Data Dictionary
- Complete field descriptions
- Data quality metrics
- Processing notes

---

*This case study demonstrates comprehensive data analysis skills including data cleaning, statistical analysis, visualization, and business recommendations. The analysis follows the complete data analysis process from problem identification to actionable insights.*
