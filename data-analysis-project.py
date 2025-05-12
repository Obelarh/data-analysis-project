import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('owid-covid-data.csv')
# print(df.head())

# Printing names of colums
# print(df.columns)

# Checking of empty rows
# print(df.isnull().sum())

# 3. Data Cleaning
# Filtering countries of interest
country = df[df['location'].isin(['United Kingdom', 'Argentina'])]
# print(country)

# Drop rows with missing 'date'
df_clean = df.dropna(subset=['date'])

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Handling missing values in the population column
df['population'] = df['population'].fillna(0)               # Fill with zero

# Confirming the changes
# print(df.isnull().sum())

# 4. Exploratory Data Analysis (EDA)

# Filter for selected countries
selected_countries = ['Nigeria', 'United Kingdom','Norway', 'Brazil', 'Argentina']
filtered_df = df[df['location'].isin(selected_countries)]

# Pivot the table: dates as index, countries as columns
pivot_df = filtered_df.pivot(index='date', columns='location', values='total_cases')

# Plot
# plt.figure(figsize=(12, 6))
# pivot_df.plot()
# plt.title("Total Cases Over Time")
# plt.xlabel("Date")
# plt.ylabel("Total Cases")
# plt.legend(title="Country")
# plt.tight_layout()
# plt.grid(True)
# plt.show()


# PLOT TOTAL DEATH OVER TIME
# Pivot table: rows = date, columns = location, values = total_deaths
pivot_deaths = filtered_df.pivot(index='date', columns='location', values='total_deaths')

# Plot total deaths over time
# plt.figure(figsize=(12, 6))
# pivot_deaths.plot()
# plt.title("Total Deaths Over Time Of Selected Countries")
# plt.xlabel("Date")
# plt.ylabel("Total Deaths")
# plt.legend(title="Country")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


# Total death over time for all countries on the CSV file

# Pivot: rows = date, columns = Location, values = total_deaths
pivot_deaths = df.pivot(index='date', columns='location', values='total_deaths')

# Plot
# plt.figure(figsize=(14, 8))
# pivot_deaths.plot(legend=True, alpha=0.7)

# plt.title("Total Deaths Over Time (All Countries)")
# plt.xlabel("Date")
# plt.ylabel("Total Deaths")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


# New cases between countries
# Pivot the table: rows = date, columns = Location, values = new_cases
pivot_new_cases = filtered_df.pivot(index='date', columns='location', values='new_cases')

# Optional: Smooth with a 7-day moving average
pivot_new_cases = pivot_new_cases.rolling(window=7).mean()

# Plot
# plt.figure(figsize=(14, 7))
# pivot_new_cases.plot()
# plt.title("Daily New COVID-19 Cases Comparison")
# plt.xlabel("Date")
# plt.ylabel("New Cases")
# plt.grid(True)
# plt.legend(title="Country")
# plt.tight_layout()
# plt.show()

# Calculate the death rate: total_deaths / total_cases. (OF SELECTED COUNTRIES)

df['total_deaths'] = df['total_deaths'].fillna(23) 
df['total_deaths'] = pd.to_numeric(df['total_deaths'], errors='coerce')
df['total_cases'] = pd.to_numeric(df['total_cases'], errors='coerce')

df['death_rate'] = df['total_deaths'] / df['total_cases']

# Confirm the 'death_rate' column is created

print(df[['total_deaths', 'total_cases', 'death_rate']].head())  # Show first few rows to check


df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces

# Calculate death rate: total_deaths / total_cases
df['death_rate'] = df['total_deaths'] / df['total_cases']

if 'death_rate' in filtered_df.columns:
    print("death_rate column is available.")
else:
    print("death_rate column is missing.")



# Pivot: rows = date, columns = location, values = death_rate
pivot_death_rate = filtered_df.pivot(index='date', columns='location', values='death_rate')

# Smooth the data with a 7-day moving average
pivot_death_rate = pivot_death_rate.rolling(window=7).mean()

# Plot
# plt.figure(figsize=(14, 7))
# pivot_death_rate.plot()
# plt.title("COVID-19 Death Rate Over Time: Selected Countries")
# plt.xlabel("Date")
# plt.ylabel("Death Rate")
# plt.grid(True)
# plt.legend(title="Country")
# plt.tight_layout()
# plt.show()