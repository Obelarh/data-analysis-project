import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('owid-covid-data.csv')
print(df.head())

# Printing names of colums
print(df.columns)

# Checking of empty rows
print(df.isnull().sum())

# 3. Data Cleaning
# Filtering countries of interest
country = df[df['location'].isin(['United Kingdom', 'Argentina'])]
print(country)

# Drop rows with missing 'date'
df_clean = df.dropna(subset=['date'])

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Handling missing values in the population column
df['population'] = df['population'].fillna(0)               # Fill with zero

# Confirming the changes
print(df.isnull().sum())

# 4. Exploratory Data Analysis (EDA)

# Filter for selected countries
selected_countries = ['Nigeria', 'United Kingdom','Norway', 'Brazil', 'Argentina']
filtered_df = df[df['location'].isin(selected_countries)]

# Pivot the table: dates as index, countries as columns
pivot_df = filtered_df.pivot(index='date', columns='location', values='total_cases')

# Plot
plt.figure(figsize=(12, 6))
pivot_df.plot()
plt.title("Total Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.legend(title="Country")
plt.tight_layout()
plt.grid(True)
plt.show()


# PLOT TOTAL DEATH OVER TIME
# Pivot table: rows = date, columns = location, values = total_deaths
pivot_deaths = filtered_df.pivot(index='date', columns='location', values='total_deaths')

# Plot total deaths over time
plt.figure(figsize=(12, 6))
pivot_deaths.plot()
plt.title("Total Deaths Over Time Of Selected Countries")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.legend(title="Country")
plt.grid(True)
plt.tight_layout()
plt.show()


# Total death over time for all countries on the CSV file

# Pivot: rows = date, columns = Location, values = total_deaths
pivot_deaths = df.pivot(index='date', columns='location', values='total_deaths')

# Plot
plt.figure(figsize=(14, 8))
pivot_deaths.plot(legend=True, alpha=0.7)

plt.title("Total Deaths Over Time (All Countries)")
plt.xlabel("Date")
plt.ylabel("Total Deaths")
plt.grid(True)
plt.tight_layout()
plt.show()


# New cases between countries
# Pivot the table: rows = date, columns = Location, values = new_cases
pivot_new_cases = filtered_df.pivot(index='date', columns='location', values='new_cases')

# Optional: Smooth with a 7-day moving average
pivot_new_cases = pivot_new_cases.rolling(window=7).mean()

# Plot
plt.figure(figsize=(14, 7))
pivot_new_cases.plot()
plt.title("Daily New COVID-19 Cases Comparison")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.grid(True)
plt.legend(title="Country")
plt.tight_layout()
plt.show()

# Calculate the death rate: total_deaths / total_cases. (OF SELECTED COUNTRIES)


# Clean column names
df.columns = df.columns.str.strip()

# Ensure 'total_cases' and 'location' are present and clean
df['total_cases'] = pd.to_numeric(df['total_cases'], errors='coerce')

# Drop rows where total_cases or location is missing
df = df.dropna(subset=['total_cases', 'location'])

# Get the latest total cases for each country (by last available date)
latest_data = df.sort_values('date').groupby('location').last()

# Sort countries by total_cases in descending order and get top 10
top_countries = latest_data.sort_values('total_cases', ascending=False).head(10)

# Plot a bar chart
plt.figure(figsize=(12, 6))
plt.bar(top_countries.index, top_countries['total_cases'], color='skyblue')
plt.title("Top 10 Countries by Total COVID-19 Cases")
plt.ylabel("Total Cases")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 5. Visualizing Vacinnation Progress Data

selected_countries = ['Nigeria', 'United States', 'Brazil', 'India', 'United Kingdom']
filtered_df = df[df['location'].isin(selected_countries)]

# Drop rows with missing total_vaccinations
filtered_df = filtered_df.dropna(subset=['total_vaccinations'])

# Pivot table for plotting
pivot_vax = filtered_df.pivot(index='date', columns='location', values='total_vaccinations')

# Plotting
plt.figure(figsize=(12, 6))
pivot_vax.plot(ax=plt.gca())
plt.title("Cumulative COVID-19 Vaccinations Over Time")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.legend(title='Country')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


# Drop rows with missing values in required columns
df = df.dropna(subset=['total_vaccinations', 'population'])

# Calculate % vaccinated
df['percent_vaccinated'] = (df['total_vaccinations'] / df['population']) * 100

# Get the latest record per country (if data includes multiple dates)
latest = df.sort_values('date').groupby('location').tail(1)

# Optional: filter for specific countries
selected_countries = ['United Kingdom', 'Nigeria', 'Brazil', 'Argentina']
latest = latest[latest['location'].isin(selected_countries)]

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=latest, x='location', y='percent_vaccinated', hue='location', palette='viridis', legend=False)
plt.title('Percentage of Population Vaccinated (at least one dose)')
plt.ylabel('Vaccinated (%)')
plt.xlabel('Country')
plt.tight_layout()
plt.show()