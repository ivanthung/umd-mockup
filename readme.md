**Project Title: Streamlit Urban Mining Potential Assessment App**

**Overview**

This Streamlit application provides valuable insights for urban planners, policymakers, and businesses interested in exploring the circular economy potential within the built environment of Amsterdam. The app draws upon real-world data and interactive visualizations to:

* **Identify potential urban mining resources:** Explore material flows and the availability of reusable materials within the city.
* **Analyze scenarios and trade-offs:** Compare different development scenarios based on building types, material impact, and housing typologies.
* **Evaluate circular economy options:** Assess the potential for reuse, recycling, and repurposing of materials.
* **Generate AI-powered reports:** Obtain concise summaries of key findings, with tailored recommendations for specific stakeholders.

**Getting Started**

1. **Prerequisites**
   * Python 3.10.6
   * Poetry (package installer for Python)
   * make utility (pre-installed on Mac)
   * Pyenv (for managing Python versions)

2. **Installation**

   ```bash
   # Setting up the virtual env and installing dependencies
   pyenv install 3.10.6
   pyenv virtualenv 3.10.6 mock_up_umdashboard
   pyenv activate mock_up_umdashboard
   poetry install
   
   ```

3. **Adding dependencies**

   ```bash
   # Adding new dependencies
   poetry add <package_name>
   ```

3. **Running the App**

   ```bash
   streamlit run Start.py
   ```

   This will open the app in your web browser.

4. **Running the App**


**Structure**

The project follows a modular structure for maintainability and clarity:

* **`/Users/ivanthung/code/mock_up_umdashboard/Start.py`:** Contains the code for the initial landing page of the application.
* **`/Users/ivanthung/code/mock_up_umdashboard/utils/`:**  This directory houses utility modules:
    * **`ai_report.py`:** Handles interaction with the AI model for report generation.
    * **`buildingdata.py`:** Classes and functions for managing building data.
    * **`calculations.py`:**  Performs necessary calculations for scenarios and visualizations.
    * **`reportgenerator.py`:**  Generates PDF reports from the provided data and figures.
    * **`utils.py`:** Common utilities for maps, data loading, etc.
    * **`column_configs.py`:** Specific column configurations for dataframes and visualizations used in the app.
    * **`data_manager.py`:** Loads and manages data (BAG dataset, scenarios) in the session state.
* **`/Users/ivanthung/code/mock_up_umdashboard/pages/`:** Contains individual pages of the Streamlit app:

**Data**

* **`spatial_data/final/bag-ams-zuidoost-platdak-buurt.shp`:** Sample BAG dataset (shapefile format). Replace with your comprehensive dataset.
* **`scenarios/scenario_data.pickle`:** (If applicable) Stores saved user-generated scenarios for future use.

**Dependencies:**

See the `requirements.txt` file for a complete list of dependencies.
