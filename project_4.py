"""
============================================================
  AeroPulse — Airline Operations & Revenue Intelligence
  Author  : Srinagadivya Chunchula
  Tools   : Python, Pandas, Matplotlib, SQLAlchemy, MySQL
============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ──────────────────────────────────────────────
# STEP 1 : DATA LOADING
# ──────────────────────────────────────────────
def load_flight_data():
    """Load CSV dataset and normalize column names."""
    # ✅ Update path if your CSV is in a different location
    df = pd.read_csv("Airline_Operations_Revenue_Intelligence.csv")
    df.columns = df.columns.str.strip().str.lower()
    print("✅ Flight Dataset Loaded Successfully")
    print("   Shape   :", df.shape)
    print("   Columns :", df.columns.tolist())
    return df


# ──────────────────────────────────────────────
# STEP 2 : DATA CLEANING & PREPROCESSING
# ──────────────────────────────────────────────
def clean_flight_data(df):
    """Clean raw flight data — dates, nulls, duplicates, outliers."""
    print("\n=== Data Cleaning & Preprocessing ===")

    # Convert flight_date to datetime
    df['flight_date'] = pd.to_datetime(df['flight_date'], format="mixed", dayfirst=True)

    # Remove invalid routes (origin same as destination)
    df = df[df['origin'] != df['destination']]

    # Fill missing delay values with 0 (no delay info = assume on-time)
    df['delay_minutes'] = df['delay_minutes'].fillna(0)

    # Fill missing revenue with median revenue
    df['revenue'] = df['revenue'].fillna(df['revenue'].median())

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Outlier treatment using IQR method on delay_minutes
    Q1    = df['delay_minutes'].quantile(0.25)
    Q3    = df['delay_minutes'].quantile(0.75)
    IQR   = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df    = df[(df['delay_minutes'] >= lower) & (df['delay_minutes'] <= upper)]

    print("✅ Cleaned Records:", len(df))
    return df


# ──────────────────────────────────────────────
# STEP 3 : FEATURE ENGINEERING
# ──────────────────────────────────────────────
def engineer_features(df):
    """Create new useful columns from existing data."""
    print("\n=== Feature Engineering ===")

    # Route = Origin + Destination
    df['route'] = df['origin'] + " → " + df['destination']

    # Load Factor = how full the flight was
    df['load_factor'] = df['passenger_count'] / df['seat_capacity']

    # Delay Category
    def delay_category(delay):
        if delay <= 5:
            return 'On-Time'
        elif delay <= 30:
            return 'Minor Delay'
        else:
            return 'Major Delay'

    df['delay_category'] = df['delay_minutes'].apply(delay_category)

    # Day Type (Weekday / Weekend)
    df['day_type'] = df['flight_date'].dt.dayofweek.apply(
        lambda x: 'Weekend' if x >= 5 else 'Weekday'
    )

    print("✅ New columns: route, load_factor, delay_category, day_type")
    return df


# ──────────────────────────────────────────────
# STEP 4 : EXPLORATORY DATA ANALYSIS (EDA)
# ──────────────────────────────────────────────
def perform_eda(df):
    """Analyse key business metrics from flight data."""
    print("\n=== Exploratory Data Analysis ===")

    # Average delay per route (highest first)
    route_delay = df.groupby('route')['delay_minutes'].mean().sort_values(ascending=False)

    # Average load factor per aircraft type
    aircraft_load = df.groupby('aircraft_type')['load_factor'].mean()

    # Total revenue per route (highest first)
    route_revenue = df.groupby('route')['revenue'].sum().sort_values(ascending=False)

    # Count of each delay category
    delay_distribution = df['delay_category'].value_counts()

    print("\n📍 Top 5 Delay Routes:")
    print(route_delay.head(5).to_string())

    print("\n📍 Load Factor by Aircraft Type:")
    print(aircraft_load.to_string())

    print("\n📍 Top 5 Revenue Routes:")
    print(route_revenue.head(5).to_string())

    print("\n📍 Delay Category Distribution:")
    print(delay_distribution.to_string())

    return route_delay, aircraft_load, route_revenue, delay_distribution


# ──────────────────────────────────────────────
# STEP 5 : VISUALIZATION DASHBOARD
# ──────────────────────────────────────────────
def create_dashboard(df, route_delay, aircraft_load, route_revenue, delay_distribution):
    """Create and save a 5-panel operations dashboard."""
    print("\n=== Data Visualization Dashboard ===")

    fig, axes = plt.subplots(2, 3, figsize=(20, 11))
    fig.suptitle('AeroPulse — Airline Operations & Revenue Intelligence',
                 fontsize=16, fontweight='bold', y=1.01)
    fig.patch.set_facecolor('#f9f9f9')

    # ── Chart 1 : Top 10 Routes by Avg Delay ──
    ax1 = axes[0, 0]
    route_delay.head(10).plot(kind='bar', color='#E84855', ax=ax1, width=0.6)
    ax1.set_title('Top 10 Routes by Avg Delay', fontweight='bold')
    ax1.set_ylabel('Delay (Minutes)')
    ax1.set_xlabel('')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)

    # ── Chart 2 : Load Factor by Aircraft Type ──
    ax2 = axes[0, 1]
    aircraft_load.plot(kind='bar', color='#2E86AB', ax=ax2, width=0.5)
    ax2.set_title('Load Factor by Aircraft Type', fontweight='bold')
    ax2.set_ylabel('Avg Load Factor')
    ax2.set_xlabel('')
    ax2.axhline(0.6, color='red', linestyle='--', linewidth=1.2, label='60% threshold')
    ax2.legend(fontsize=8)
    ax2.grid(axis='y', alpha=0.3)
    ax2.tick_params(axis='x', rotation=30)

    # ── Chart 3 : Top 10 Revenue Routes ──
    ax3 = axes[0, 2]
    route_revenue.head(10).plot(kind='bar', color='#3BB273', ax=ax3, width=0.6)
    ax3.set_title('Top 10 Revenue Routes', fontweight='bold')
    ax3.set_ylabel('Total Revenue (₹)')
    ax3.set_xlabel('')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(axis='y', alpha=0.3)

    # ── Chart 4 : Delay Category Distribution ──
    ax4 = axes[1, 0]
    colors_cat = {'On-Time': '#3BB273', 'Minor Delay': '#F4A261', 'Major Delay': '#E84855'}
    bar_colors = [colors_cat.get(c, '#9B59B6') for c in delay_distribution.index]
    delay_distribution.plot(kind='bar', color=bar_colors, ax=ax4, width=0.5)
    ax4.set_title('Delay Category Distribution', fontweight='bold')
    ax4.set_ylabel('Number of Flights')
    ax4.set_xlabel('')
    ax4.tick_params(axis='x', rotation=0)
    ax4.grid(axis='y', alpha=0.3)
    for bar in ax4.patches:
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 f'{int(bar.get_height()):,}', ha='center', fontsize=9)

    # ── Chart 5 : Delay vs Load Factor Scatter ──
    ax5 = axes[1, 1]
    scatter = ax5.scatter(df['delay_minutes'], df['load_factor'],
                          alpha=0.4, color='#7c6af7', s=18)
    ax5.set_xlabel('Delay Minutes')
    ax5.set_ylabel('Load Factor')
    ax5.set_title('Delay vs Load Factor', fontweight='bold')
    ax5.axhline(0.6, color='red', linestyle='--', linewidth=1, alpha=0.7, label='60% load')
    ax5.legend(fontsize=8)
    ax5.grid(alpha=0.3)

    # ── Chart 6 : Weekday vs Weekend Revenue ──
    ax6 = axes[1, 2]
    day_rev = df.groupby('day_type')['revenue'].sum()
    day_rev.plot(kind='pie', autopct='%1.1f%%', colors=['#2E86AB', '#F4A261'],
                 ax=ax6, startangle=90)
    ax6.set_title('Revenue: Weekday vs Weekend', fontweight='bold')
    ax6.set_ylabel('')

    plt.tight_layout()
    plt.savefig("aeropulse_operations_dashboard.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Dashboard saved: aeropulse_operations_dashboard.png")


# ──────────────────────────────────────────────
# STEP 6 : SQL DATABASE INTEGRATION
# ──────────────────────────────────────────────
def database_integration(df):
    """Load cleaned data into MySQL and run SQL queries."""
    print("\n=== SQL Database Integration ===")

    # ✅ Update your MySQL password below
    engine = create_engine(
        "mysql+mysqlconnector://root:root%40123@localhost/dataanalysisproject"
    )

    # Load dataframe into MySQL table
    df.to_sql(name="flight_operations", con=engine, if_exists="replace", index=False)
    print("✅ Flight data loaded into MySQL successfully")

    # SQL Query — Top 5 highest delay routes
    query = """
        SELECT route,
               ROUND(AVG(delay_minutes), 2) AS avg_delay,
               COUNT(*)                      AS total_flights
        FROM   flight_operations
        GROUP  BY route
        ORDER  BY avg_delay DESC
        LIMIT  5;
    """
    result = pd.read_sql(query, engine)
    print("\n📊 Highest Delay Routes (from MySQL):")
    print(result.to_string(index=False))


# ──────────────────────────────────────────────
# STEP 7 : BUSINESS INSIGHTS
# ──────────────────────────────────────────────
def generate_insights(df):
    """Print key actionable business insights."""
    print("\n=== Key Business Insights ===")

    # Top 3 delay routes
    high_delay = (df.groupby('route')['delay_minutes']
                  .mean()
                  .sort_values(ascending=False)
                  .head(3))
    print("\n🔴 Routes with consistently HIGH delays:")
    for route, delay in high_delay.items():
        print(f"   → {route} : {delay:.1f} min avg delay")

    # Low load factor flights
    low_load = df[df['load_factor'] < 0.6]
    print(f"\n⚠️  Flights below 60% seat capacity: {len(low_load):,}")
    print(f"   Revenue at risk (low load): ₹{low_load['revenue'].sum():,.2f}")

    # Top revenue route
    top_route = df.groupby('route')['revenue'].sum().idxmax()
    top_rev   = df.groupby('route')['revenue'].sum().max()
    print(f"\n💰 Top revenue route  : {top_route}")
    print(f"   Total revenue       : ₹{top_rev:,.2f}")

    # On-time performance
    on_time_pct = (df['delay_category'] == 'On-Time').mean() * 100
    print(f"\n✅ On-Time Performance : {on_time_pct:.1f}%")


# ──────────────────────────────────────────────
# MAIN — Run All Steps
# ──────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  AeroPulse — Airline Operations & Revenue Intelligence")
    print("=" * 60)

    df = load_flight_data()
    df = clean_flight_data(df)
    df = engineer_features(df)

    route_delay, aircraft_load, route_revenue, delay_distribution = perform_eda(df)

    generate_insights(df)
    database_integration(df)
    create_dashboard(df, route_delay, aircraft_load, route_revenue, delay_distribution)

    print("\n" + "=" * 60)
    print("  ✅ AeroPulse Project Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
