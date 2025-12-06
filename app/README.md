# Can you afford to live in Zurich?  
*An Analysis of Housing, Income, and Rent*

---

## 💡 About
Zurich‘s housing affordability is a growing concern. This project combines housing stock, population, rent, and income data to explore affordability and availability at the district level. The goal of the app is to identify where housing is accessible, where people are being squeezed, and where policy measures might be most necessary.

**Structure:**  
- Can you afford to live in Zurich? (Main page)  
- Housing Data Overview  
- Population Data Overview  
- Rent Data Overview  

---

## ❓ Key Questions

### How has Zurich’s housing stock developed in the last decades?
- Housing stock between 2008–2024 has grown in Zurich. Some districts expanded faster (e.g., Kreis 12 and Kreis 5) while others stagnated (e.g., Kreis 1).  
- The data also shows that apartments are not evenly distributed by size (e.g., citywide there are more 3-room apartments than 1-room or 5-room apartments). Suitability matters because a district with many cheap 1-room flats is still not suitable for someone needing a family-sized unit.

### How has Zurich’s population changed since the 1940s?
- 1970s–1980s suburbanization (“Stadtflucht”) due to rising rents and housing shortages, and lower birth rates.  
- Turnaround after 2000 due to more housing density and steady net migration gains.  
- Present-day trend: sustained growth, driven primarily by immigration.

### How do rent prices differ across districts in Zurich and how have they developed between 2022 and 2024?
- Central districts are more expensive than outer districts.  
- Nonprofit housing is cheaper than market-price housing in all districts.  
- Upper percentile rents have increased between 2022 and 2024, and smaller areas have more uncertainty.

### Where Is Rent Hitting Residents Hardest?
- Less than 30% of income spent on rent is defined as **affordable**, 30–40% as **stressful**, and above 40% as **overburdening**.  
- In many districts, especially central ones, median-income households spend more than 40% of income on rent.  
- Targeted investment in nonprofit housing could relieve pressure in key districts.

---

## 👓 Data Overview

1. **Average Rent by District**  
   - Dataset: [Bau WHG MPE Mietpreis](https://data.stadt-zuerich.ch/dataset/bau_whg_mpe_mietpreis_raum_zizahl_gn_jahr_od5161?utm_source=chatgpt.com)  
   - Description: Provides estimated rent ranges for various spatial units in Zurich, including city-wide, district, and statistical quarter levels.

2. **Population by District**  
   - Dataset: [Bevölkerung Bestand Jahr Quartier](https://data.stadt-zuerich.ch/dataset/bev_bestand_jahr_quartier_od3240?utm_source=chatgpt.com)  
   - Description: Offers data on the economic resident population of Zurich by statistical city quarter and year.

3. **Housing and Room Stock by District**  
   - Dataset: [Wohnungs- und Zimmerbestand](https://www.stadt-zuerich.ch/content/dam/web/de/politik-verwaltung/statistik-und-daten/daten/bauen-wohnen/BAU507T5073_Wohnungs-und-Zimmerbestand_nach-Zimmerzahl-Stadtquartier.xlsx)  
   - Description: District, number of rooms, and number of housing units per room category.

4. **Income by District**  
   - Dataset: [FD Median Einkommen Quartier](https://data.stadt-zuerich.ch/dataset/fd_median_einkommen_quartier_od1003?utm_source=chatgpt.com)  
   - Description: For each city-quarter in Zurich and each tax tariff (single/married/partner) — provides the 25% quantile income, median income, and 75% quantile income (taxable income) of individuals.

---

## ⚙️ Key Technical Steps
- Loading raw data from Excel/CSV files across multiple years and sources.  
- Filtering rows to keep only relevant districts and neighbourhoods.  
- Renaming columns for clarity and consistency.  
- Dropping unnecessary columns to simplify datasets.  
- Mapping neighbourhoods to districts for population data.  
- Reshaping data (wide → long) where needed for analysis.  
- Standardizing values (e.g., room numbers, rent types) for consistency.  
- Creating interactive charts with Plotly.  