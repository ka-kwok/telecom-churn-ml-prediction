# **Telecom Churn Analytics:** 
## ***Building Predictive Models to Improve Customer Retention***

## 🔹 Abstract
This project explores customer churn prediction for a telecom company using the **Telecom Customer Churn dataset**. 
The analysis follows a structured workflow from **data profiling → data cleaning → EDA → feature engineering → ML modeling → churn prediction application**. 

## 🔹 Table of Contents
1. [Introduction & Business Requirements](#🔹-1-introduction-and-business-requirements)  
2. [Dataset Description](#🔹-2-data-description)
3. [Hypothesis and Methodology]((#🔹-3-hypothesis-and-methodology))
4. [Exploratory Data Analysis (EDA)]((#🔹-4-exploratory-data-analysis-eda))
5. [Feature Engineering & Data Cleaning](#🔹-5-feature-engineering--data-cleaning)
6. [Model Development & Evaluation](#🔹-6-model-development--evaluation)
7. [Explainability & Insights](#🔹-7-explainability--insights)
8. [Ethical Considerations & Data Governance](#🔹-8-ethical-considerations--data-governance)
9. [Project Plan](#🔹-9-project-plan)
10. 


## 🔹 1. Introduction and Business Requirements
Customer churn is a major challenge in the telecom industry. Retaining existing customers is more cost-effective than acquiring new ones. 

The project aims to identify key drivers of customer churn and develop a predictive model. Insights will inform business decisions, enhance retention strategies, and improve marketing effectiveness and product ROI.

✅ Key Requirements
* Accurate Churn Prediction

    * Develop a model to predict whether a customer is likely to churn in the next billing cycle.

* Key Driver Identification

    * Pinpoint the most influential demographic and subscription attributes driving churn.

* Actionable Insights

    * Translate model outputs into retention strategies (e.g., targeted offers, loyalty programs).

* Seamless Integration

    * Deploy the model into existing CRM and marketing systems for real‑time use.

* Performance Metrics

    * Achieve at least 80% recall on churners (to minimize missed at‑risk customers) while maintaining acceptable precision.

📈 Business Impact
* Reduce customer churn rate

* Improve retention campaign ROI

* Strengthen customer loyalty and lifetime value

## 🔹 2. Dataset Description 
 ### Dataset Summary
- Source: Kaggle [Telecom Customer Churn dataset](https://www.kaggle.com/datasets/mubeenshehzadi/customer-churn-dataset/))  
- ~7,000 records, 21 features  
- Features: Tenure, Contract, Internet services, Monthly & Total Charges, etc
- Target: **Churn (Yes/No)**  
- Note: `customerID` identified as **PII** and removed  

### 📄 Customer Churn Dataset Fields

- **`customerID`**: Unique ID assigned to each customer  
- **`gender`**: Gender of the customer (`Male`, `Female`)  
- **`SeniorCitizen`**: Whether the customer is a senior citizen (`1` = Yes, `0` = No)  
- **`Partner`**: If the customer has a partner (`Yes`/`No`)  
- **`Dependents`**: If the customer has dependents (`Yes`/`No`)  
- **`tenure`**: Number of months the customer remained with the company  
- **`PhoneService`**: Whether the customer has a phone service (`Yes`/`No`)  
- **`MultipleLines`**: Customer possesses multiple phone lines (`No`, `Yes`, `No phone service`)  
- **`InternetService`**: Type of internet service (`DSL`, `Fiber optic`, `No`)  
- **`OnlineSecurity`**: Whether the customer has online security add‑on (`Yes`, `No`, `No internet`)  
- **`OnlineBackup`**: Whether the customer has online backup service (`Yes`, `No`, `No internet`)  
- **`DeviceProtection`**: Device protection plan (`Yes`, `No`, `No internet`)  
- **`TechSupport`**: Tech support service (`Yes`, `No`, `No internet`)  
- **`StreamingTV`**: Access to streaming TV (`Yes`, `No`, `No internet`)  
- **`StreamingMovies`**: Access to streaming movies (`Yes`, `No`, `No internet`)  
- **`Contract`**: Contract type (`Month-to-month`, `One year`, `Two year`)  
- **`PaperlessBilling`**: Whether billing is paperless (`Yes`/`No`)  
- **`PaymentMethod`**: Method of payment (`Electronic check`, `Mailed check`, `Bank transfer`, `Credit card`)  
- **`MonthlyCharges`**: Amount charged to the customer monthly  
- **`TotalCharges`**: Total amount charged during the customer’s tenure  
- **`Churn`**: Whether the customer left the company (`Yes` = churned, `No` = retained)



## 🔹 3.Hypothesis and Methodology
**H1:** Customers on **`month-to-month`** contracts are more likely to churn than those on annual contracts.

**H2:** Customers with longer **`tenure`** are less likely to churn.

**H3:** **`SeniorCitizen`** Customers are more likey to churn.

**H4:** Customers who use **`fiber optic`** internet services have higer churn rates.

**H5:** Internet Customers with add-ons services like **`OnlineSecurity`** and **`TechSupport`** are less likey to churn.

## 📌 Hypothesis Validation

| **Hypothesis** | **Variable Type(s)** | **Test Type** | **Purpose** | **Interpretation**  |
| --- | --- | --- | --- | --- |
| **H1:** Customers on *month-to-month* contracts are more likely to churn. | Categorical (Contract Type vs Churn)| **Chi-Square Test of Independence** | Tests whether churn rate depends on contract type. | Significant p-value → churn is associated with contract type. |
| **H2:** Customers with longer *tenure* are less likely to churn.| Continuous (Tenure) vs Binary (Churn)  | **Independent Samples t-test** or **Mann–Whitney U test** (if not normal) | Compares average tenure between churned and non-churned customers. | Lower mean tenure among churned → supports H2. |
| **H3:** *SeniorCitizen* customers are more likely to churn.  | Binary (SeniorCitizen) vs Binary (Churn)| **Chi-Square Test**  | Checks if churn is associated with senior status. | Significant p-value → churn depends on senior status. |
| **H4:** Customers with *fiber optic* internet have higher churn rates.| Categorical (InternetService vs Churn)| **Chi-Square Test**  | Tests whether churn depends on internet service type. | Higher churn % among “Fiber optic” → supports H4. |
| **H5:** Internet customers with *OnlineSecurity* and *TechSupport* add-ons are less likely to churn. | Categorical (OnlineSecurity, TechSupport vs Churn) | **Chi-Square Test** for each variable  | Checks if having add-ons reduces churn probability.| Lower churn % among customers with these add-on service → supports H5. |


## 🔹 4. Exploratory Data Analysis (EDA)
The exploratory data analysis phase provides critical insights into the underlying patterns and relationships that influence customer churn. This step lays the foundation for feature selection, model design, and business strategy.

#### **Churn Distribution**
* Approximately 26% of customers have churned, indicating a class imbalance that must be addressed during modeling.

* This imbalance suggests that churn is a relatively rare event, making precision and recall especially important for predictive performance.

#### **Key Feature Relationships**
* **Tenure and Contract Type** emerge as **the strongest predictors of churn**. Customers with shorter tenure and month-to-month contracts are significantly more likely to churn.

* **Senior Customers** show a higher churn rate, possibly due to lower engagement with digital services or support limitations.

* **Service Type** (e.g., `fiber optic` vs `DSL`) and **Internet Add-on Services** (like `OnlineSecurity` and `TechSupport`) also show meaningful correlations with churn behaviour.

#### **Churn Correlation Analysis**

* A correlation matrix and statistical tests reveal strong associations between churn and:

    * **Contract Type**: Month-to-month contracts are highly correlated with churn.

    * **Tenure**: Shorter tenure increases churn likelihood.

    * **SeniorCitizen**: Older customers show distinct churn patterns.

    * **Internet Add-ons**: Lack of services like Online Security and Tech Support correlates with higher churn.

    * **Payment Method**: SHAP analysis later identifies Electronic Check as a strong churn indicator.

#### **Visualizations**

To support these findings, a variety of visual tools were used:

* **Barplots**: Show churn rates across categorical features like contract type and payment method.

* **Piecharts**: Illustrate churn proportions and service usage.

* **Boxplots**: Compare tenure and monthly charges between churned and retained customers.

* **Parallel Categories Graph**: Visualizes multi-feature interactions, revealing how combinations of contract type, service usage, and payment method influence churn.

## 🔹 5. Feature Engineering & Data Cleaning
The preprocessing pipeline is designed to transform the raw Telecom Customer Churn dataset into 2 datasets: clean for EDA visualization and encoded with machine-learning-ready format. These standardise data quality, engineers meaningful service-based features, and applies robust encoding and scaling methods to support predictive modelling.

# Dataset A: ETL & Data Cleaning (No Scaling)

## Purpose
Prepare raw telecom churn data for analysis by ensuring consistency, handling missing values, and engineering meaningful features.

## Key Steps
### 1. Data Cleaning
- Removed personally identifiable information (`customerID`) to ensure compliance with data governance.  
- Converted `TotalCharges` to numeric and handled invalid or missing entries.

### 2. Missing Value Handling
- Imputed missing `TotalCharges` values using the relationship:  
  `TotalCharges = MonthlyCharges * tenure`  
- Applied median imputation for remaining numerical fields.

### 3. Feature Engineering
- **CustomerType:** Classified customers as *Phone only*, *Internet only*, or *Both* based on service subscriptions.  
- **NumInternetServices:** Counted active internet add-ons such as *OnlineSecurity*, *TechSupport*, and *StreamingTV*.

## Notes
Scaling is not applied at this stage to preserve the original data distribution for exploratory analysis and statistical testing.

## Output File
`telecom_customer_churn_cleaned.csv`


#### Dataset B: Feature Encoding & Scaling (For Modeling)
**Purpose:** Prepare encoded features for machine learning training.

**Transformations:**
- **Numerical columns:** Standardized using `StandardScaler()`.
- **Categorical columns:** One-hot encoded using `OneHotEncoder()` (drop first to avoid multicollinearity).

**Output:** `telecom_customer_churn_encoded.csv`  

## 🔹 6. Model Development & Evaluation

Models compared:  
- Logistic Regression (best)  
- Adaboost  
- XGBoost  

| Model                   | Accuracy | Precision | Recall  | F1   | ROC-AUC |
|-------------------------|----------|-----------|---------|------|---------|
| **Logistic Regression** | **0.82** | **0.69**  | **0.54**| 0.60 | 0.85    |
| Adaboost                | 0.81     | 0.69      | 0.50    | 0.58 | **0.85**|
| XGBoost                 | 0.81     | 0.67      | 0.50.   | 0.58 | 0.85    |


## 🔹 7. Explainability & Insights

#### **SHAP Analysis findings:**
🔴 **Top Churn Risk Factors (Red = High Impact):**
* Tenure (Most Important)
    * Low tenure (blue dots on right) = HIGH churn risk
    * High tenure (red dots on left) = LOW churn risk
    * Business insight: New customers are your highest risk segment

* Payment Method - Electronic Check
    * Customers using electronic check have higher churn probability
    * This payment method appears less stable than others

* Internet Service - Fiber Optic

    * Despite being premium service, fiber customers show higher churn
    * May indicate service quality or pricing issues

🔵 **Top Churn Protection Factors (Blue = Low Impact):**
* Contract - Two Year
    * Long-term contracts significantly reduce churn risk
    * Strongest retention tool available

* Online Security & Tech Support
    * These add-on services provide strong churn protection
    * Customers with these services are much less likely to leave

**SHAP Plot Types Generated:**
* Beeswarm Plot: Shows feature impact distribution across all customers
* Waterfall Plot: Explains one specific customer's prediction

**Key Business Insights:**

High-Risk Customer Profile:

* New customers (low tenure)
* Electronic check payment method
* Fiber optic internet service
* No add-on security services

Low-Risk Customer Profile:

* Long-term customers (high tenure)
* Two-year contracts
* Online security and tech support services
* Non-electronic payment methods

**Strategic Recommendations:**

* Early Intervention: Focus retention efforts on customers with < 12 months tenure
* Payment Method: Encourage migration from electronic check to more stable payment methods
* Service Bundling: Promote OnlineSecurity and TechSupport as retention tools
* Contract Strategy: Incentivize longer-term contracts with discounts
* Fiber Service Review: Investigate quality issues and review pricing strategy affecting fiber optic customers


## 🔹 8. Ethical Considerations & Data Governance
####  Ethical Handling of Personal Identifiers

The variable `customerID` was removed during data preprocessing to eliminate any potential personally identifiable information (PII). This ensures that no individual customer can be directly identified from the dataset, aligning the project with data privacy regulations such as GDPR and CCPA. By anonymizing the dataset, the analysis focuses solely on behavioral and service-related patterns, maintaining both ethical integrity and data governance compliance.

#### Ethical Considerations of Demographic Attributes

The feature `SeniorCitizen` and `gender` were initially included during exploratory analysis to understand demographic patterns influencing customer churn. Statistical tests indicated a measurable difference in churn behavior between senior and non-senior customers, offering valuable business insights for designing age-friendly retention programs.

However, to ensure compliance with ethical AI principles and avoid potential age-related and gender-related bias, these attributes were excluded from the final predictive model. The decision prevents the model from making churn predictions based on age and gender proxies, aligning with data governance standards such as GDPR’s fairness principle and responsible AI practices.

This approach maintains analytical transparency while safeguarding against discrimination, ensuring that predictions are driven by behavioral and service-related features rather than demographic attributes.

## 🔹 9. Project Plan
**Implementation & Maintenance Workflow:**  
- Ideation and Project Setup
- Data cleaning and preprocessing  
- Exploratory Data Analysis (EDA) and visualization  
- Feature engineering and data transformation  
- Model training and hyperparameter tuning (Logistic Regression, AdaBoost, Random Forest, XGBoost)  
- Model evaluation and explainability (confusion matrix, feature importance, SHAP)  
- Dashboard development using Streamlit for interactive churn prediction and monitoring  
- Model retraining scheduled monthly with new data  
- Continuous monitoring for data drift and retraining as needed  
- Future enhancement: Full deployment as a Streamlit-based monitoring dashboard  

### Agile Methodology

This project follows an **Agile Data Science** approach with short, iterative development cycles.  
Each sprint focuses on one phase — from data cleaning to model deployment — allowing continuous feedback, testing, and improvement.  

- **Sprint 1:** Ideation  
- **Sprint 2:** Project Setup  
- **Sprint 3:** ETL 
- **Sprint 4:** EDA and Data Visualization  
- **Sprint 5:** Predictive Model training and evaluation  
- **Sprint 6:** Streamlit Dashboard Design and Deployment
- **Sprint 7:** Documentation and Review

For more details, please visit the [Project Kanban Board](https://github.com/users/ka-kwok/projects/8) on Github.

This iterative workflow with sub-tasks on each sprint ensures flexibility, rapid experimentation, and continuous model improvement based on new data and stakeholder feedback.

## Dashboard Design
* List all dashboard pages and their content, either blocks of information or widgets, like buttons, checkboxes, images, or any other item that your dashboard library supports.
* Later, during the project development, you may revisit your dashboard plan to update a given feature (for example, at the beginning of the project you were confident you would use a given plot to display an insight but subsequently you used another plot type).
* How were data insights communicated to technical and non-technical audiences?
* Explain how the dashboard was designed to communicate complex data insights to different audiences. 

## Unfixed Bugs
* Please mention unfixed bugs and why they were not fixed. This section should include shortcomings of the frameworks or technologies used. Although time can be a significant variable to consider, paucity of time and difficulty understanding implementation are not valid reasons to leave bugs unfixed.
* Did you recognise gaps in your knowledge, and how did you address them?
* If applicable, include evidence of feedback received (from peers or instructors) and how it improved your approach or understanding.

## Development Roadmap
* What challenges did you face, and what strategies were used to overcome these challenges?
* What new skills or tools do you plan to learn next based on your project experience? 

## Deployment
### Heroku

* The App live link is: https://YOUR_APP_NAME.herokuapp.com/ 
* Set the runtime.txt Python version to a [Heroku-20](https://devcenter.heroku.com/articles/python-support#supported-runtimes) stack currently supported version.
* The project was deployed to Heroku using the following steps.

1. Log in to Heroku and create an App
2. From the Deploy tab, select GitHub as the deployment method.
3. Select your repository name and click Search. Once it is found, click Connect.
4. Select the branch you want to deploy, then click Deploy Branch.
5. The deployment process should happen smoothly if all deployment files are fully functional. Click now the button Open App on the top of the page to access your App.
6. If the slug size is too large then add large files not required for the app to the .slugignore file.


## Main Data Analysis Libraries
* Here you should list the libraries you used in the project and provide an example(s) of how you used these libraries.


## Credits 

* In this section, you need to reference where you got your content, media and extra help from. It is common practice to use code from other repositories and tutorials, however, it is important to be very specific about these sources to avoid plagiarism. 
* You can break the credits section up into Content and Media, depending on what you have included in your project. 

### Content 

- The text for the Home page was taken from Wikipedia Article A
- Instructions on how to implement form validation on the Sign-Up page was taken from [Specific YouTube Tutorial](https://www.youtube.com/)
- The icons in the footer were taken from [Font Awesome](https://fontawesome.com/)

### Media

- The photos used on the home and sign-up page are from This Open-Source site
- The images used for the gallery page were taken from this other open-source site



## Acknowledgements (optional)
* Thank the people who provided support through this project.


# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)