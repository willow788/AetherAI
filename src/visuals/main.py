import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

# Set style for prettier visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = '#f8f9fa'
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

# Custom color palette
colors = sns.color_palette("husl", 8)
primary_color = '#2E86AB'
secondary_color = '#A23B72'
accent_color = '#F18F01'

df = pd.read_csv('features.csv')
df["window_start"] = pd.to_datetime(df["window_start"])

print(df.head())
print(f"\nDataset spans from {df['window_start'].min()} to {df['window_start'].max()}")

# Create a comprehensive dashboard with multiple visualizations
fig = plt.figure(figsize=(16, 12))
fig.suptitle('AetherAI - User Behavior Analytics Dashboard', fontsize=20, fontweight='bold', y=0.995)

# 1. Typing Rate Over Time
ax1 = plt.subplot(3, 3, 1)
ax1.fill_between(df["window_start"], df["typing_rate"], alpha=0.3, color=primary_color)
ax1.plot(df["window_start"], df["typing_rate"], color=primary_color, linewidth=2.5, label='Typing Rate')
ax1.set_ylabel("Typing Rate (keys/sec)", fontweight='bold')
ax1.set_title("Typing Activity Over Time", fontweight='bold', fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
ax1.tick_params(axis='x', rotation=45)

# 2. App Switches Over Time
ax2 = plt.subplot(3, 3, 2)
ax2.bar(df["window_start"], df["app_switches"], color=secondary_color, alpha=0.7, edgecolor='black', linewidth=0.5)
ax2.set_ylabel("Number of Switches", fontweight='bold')
ax2.set_title("Application Switches", fontweight='bold', fontsize=11)
ax2.grid(True, alpha=0.3, axis='y')
ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
ax2.tick_params(axis='x', rotation=45)

# 3. Interaction Intensity
ax3 = plt.subplot(3, 3, 3)
scatter = ax3.scatter(df["window_start"], df["interaction_intensity"], 
                      c=df["interaction_intensity"], cmap='RdYlGn', 
                      s=150, alpha=0.7, edgecolors='black', linewidth=0.5)
ax3.set_ylabel("Intensity Score", fontweight='bold')
ax3.set_title("Interaction Intensity Heatmap", fontweight='bold', fontsize=11)
ax3.grid(True, alpha=0.3)
cbar = plt.colorbar(scatter, ax=ax3)
cbar.set_label('Intensity', fontweight='bold')
ax3.xaxis.set_major_locator(mdates.AutoDateLocator())
ax3.tick_params(axis='x', rotation=45)

# 4. Idle vs Active Time
ax4 = plt.subplot(3, 3, 4)
ax4.fill_between(df["window_start"], 0, df["idle_time"], alpha=0.5, color='#FF6B6B', label='Idle Time')
ax4.fill_between(df["window_start"], df["idle_time"], df["idle_time"] + df["active_time"], 
                 alpha=0.5, color='#4ECDC4', label='Active Time')
ax4.set_ylabel("Time (seconds)", fontweight='bold')
ax4.set_title("Activity Timeline", fontweight='bold', fontsize=11)
ax4.legend(loc='upper right', framealpha=0.95)
ax4.grid(True, alpha=0.3, axis='y')
ax4.xaxis.set_major_locator(mdates.AutoDateLocator())
ax4.tick_params(axis='x', rotation=45)

# 5. Total Keys vs Mouse Interactions
ax5 = plt.subplot(3, 3, 5)
ax5.plot(df["window_start"], df["total_keys"], marker='o', color=primary_color, 
         linewidth=2, markersize=6, label='Keys Pressed', alpha=0.8)
ax5_twin = ax5.twinx()
ax5_twin.plot(df["window_start"], df["total_mouse"], marker='s', color=secondary_color, 
              linewidth=2, markersize=6, label='Mouse Clicks', alpha=0.8)
ax5.set_ylabel("Keys Pressed", fontweight='bold', color=primary_color)
ax5_twin.set_ylabel("Mouse Clicks", fontweight='bold', color=secondary_color)
ax5.set_title("Input Methods Comparison", fontweight='bold', fontsize=11)
ax5.grid(True, alpha=0.3)
ax5.xaxis.set_major_locator(mdates.AutoDateLocator())
ax5.tick_params(axis='x', rotation=45)

# 6. Session Duration
ax6 = plt.subplot(3, 3, 6)
colors_dur = plt.cm.viridis(df["total_duration"] / df["total_duration"].max())
ax6.bar(range(len(df)), df["total_duration"], color=colors_dur, edgecolor='black', linewidth=0.5)
ax6.set_ylabel("Duration (seconds)", fontweight='bold')
ax6.set_xlabel("Session Index", fontweight='bold')
ax6.set_title("Session Duration Distribution", fontweight='bold', fontsize=11)
ax6.grid(True, alpha=0.3, axis='y')

# 7. Top Applications (Pie Chart)
ax7 = plt.subplot(3, 3, 7)
top_apps = df["dominant_app"].value_counts().head(6)
colors_pie = sns.color_palette("Set2", len(top_apps))
wedges, texts, autotexts = ax7.pie(top_apps.values, labels=None, autopct='%1.1f%%',
                                     colors=colors_pie, startangle=90,
                                     wedgeprops=dict(edgecolor='white', linewidth=2))
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(9)
ax7.set_title("Top Applications Usage", fontweight='bold', fontsize=11)
# Add legend with app names (shortened)
app_labels = [app[:30] + '...' if len(app) > 30 else app for app in top_apps.index]
ax7.legend(app_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)

# 8. Typing Rate Distribution (Histogram)
ax8 = plt.subplot(3, 3, 8)
ax8.hist(df["typing_rate"], bins=15, color=accent_color, alpha=0.7, edgecolor='black', linewidth=1.2)
ax8.axvline(df["typing_rate"].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["typing_rate"].mean():.3f}')
ax8.axvline(df["typing_rate"].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["typing_rate"].median():.3f}')
ax8.set_xlabel("Typing Rate (keys/sec)", fontweight='bold')
ax8.set_ylabel("Frequency", fontweight='bold')
ax8.set_title("Typing Rate Distribution", fontweight='bold', fontsize=11)
ax8.legend(fontsize=9)
ax8.grid(True, alpha=0.3, axis='y')

# 9. Correlation Heatmap
ax9 = plt.subplot(3, 3, 9)
numeric_cols = df[['typing_rate', 'interaction_intensity', 'app_switches', 'idle_time', 'active_time']].corr()
im = ax9.imshow(numeric_cols, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
ax9.set_xticks(range(len(numeric_cols.columns)))
ax9.set_yticks(range(len(numeric_cols.columns)))
labels = ['Typing', 'Intensity', 'Switches', 'Idle', 'Active']
ax9.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
ax9.set_yticklabels(labels, fontsize=9)
ax9.set_title("Metric Correlation Matrix", fontweight='bold', fontsize=11)
# Add correlation values
for i in range(len(numeric_cols)):
    for j in range(len(numeric_cols)):
        text = ax9.text(j, i, f'{numeric_cols.iloc[i, j]:.2f}',
                       ha="center", va="center", color="black", fontsize=8, fontweight='bold')
cbar = plt.colorbar(im, ax=ax9)
cbar.set_label('Correlation', fontweight='bold')

plt.tight_layout()
plt.savefig('analytics_dashboard.png', dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
print("\n✓ Dashboard saved as 'analytics_dashboard.png'")
plt.show()

# Print statistics
print("\n" + "="*60)
print("BEHAVIOR ANALYTICS SUMMARY")
print("="*60)
print(f"Total Sessions: {len(df)}")
print(f"Average Typing Rate: {df['typing_rate'].mean():.4f} keys/sec")
print(f"Average App Switches per Session: {df['app_switches'].mean():.2f}")
print(f"Average Interaction Intensity: {df['interaction_intensity'].mean():.4f}")
print(f"\nTop 5 Applications:")
for idx, (app, count) in enumerate(df["dominant_app"].value_counts().head(5).items(), 1):
    print(f"  {idx}. {app[:50]}... ({count} sessions)")
print("="*60)
