# **Telecom Churn Analytics:** 
## ***Building Predictive Models to Improve Customer Retention***

## 🔹 Abstract
This project explores customer churn prediction for a telecom company using the **Telecom Customer Churn dataset**. 
The analysis follows a structured workflow from **data profiling → data cleaning → EDA → feature engineering → ML modeling → churn prediction application**. 

## 🔹 Table of Contents
1. Introduction & Business Requirements  
2. Dataset Description
3. Hypothesis and Methodology
4. Exploratory Data Analysis (EDA)
5. Feature Engineering & Data Cleaning

## 🔹 1. Introduction and Business Requirements
Customer churn is a major challenge in the telecom industry. Retaining existing customers is more cost-effective than acquiring new ones. 
The goal of this project is to build a churn prediction model and identify key drivers of churn.  

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
 * Datasets used for this analysis is the retail data set from Kaggle (https://www.kaggle.com/datasets/mubeenshehzadi/customer-churn-dataset/). 

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

### Dataset Summary
- Source: Kaggle Telecom Customer Churn dataset  
- ~7,000 records, 21 features  
- Features: Tenure, Contract, Internet services, Monthly & Total Charges  
- Target: **Churn (Yes/No)**  
- Note: `customerID` identified as **PII** and removed  

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
| **H5:** Internet customers with *OnlineSecurity* and *TechSupport* add-ons are less likely to churn. | Categorical (OnlineSecurity, TechSupport vs Churn) | **Chi-Square Test** for each variable  | Checks if having add-ons reduces churn probability.| Lower churn % among customers with “Yes” → supports H5. |


## Project Plan
**Project Plan and Workflow:**  
- Data cleaning & preprocessing  
- EDA & visualization  
- Feature engineering  
- Model training & tuning (AdaBoost, RF, XGBoost)
- Evaluation & explainability with feature importance
- Dashboard presentation with streamlit

Remarks: 
1. As the dataset is more likely in non-linear patterns, Logistic Regression is not considered in model training.
2. Dashboard presentation with intuitive analytics and prediction app for non-technical stakeholders.


## 🔹 4. Exploratory Data Analysis (EDA)
- **Churn distribution**: ~26% churned (imbalanced dataset)  
- **Tenure & Contract Type**: strongest relationship with churn  
- **Churn correlation analysis**: 
    - Service Type
    - Tenure and contract Type
    - Senior Customers
    - Internet add-on serivces 
- **Visualizations**: churn rates and distribution with barplots, piecharts, boxplots and parallel categories graph  


## 🔹 5. Feature Engineering & Data Cleaning
The preprocessing pipeline is designed to transform the raw Telecom Customer Churn dataset into a clean, machine-learning-ready format. It standardises data quality, engineers meaningful service-based features, and applies robust encoding and scaling methods to support predictive modelling.

#### 1️⃣ ETL & Data Cleaning (No Scaling)
**Purpose:** Prepare raw data for analysis by removing noise and ensuring data integrity.

**Main Steps:**
- Drop personally identifiable information (`customerID`).
- ConvertI `TotalCharges` to numeric and impute missing values using: `TotalCharges` = `MonthlyCharges` * `tenure`
- Add derived features:
  - **CustomerType:** Phone only / Internet only / Both  
  - **NumInternetServices:** Count of active internet add-ons
- Handle missing values with median imputation for numerical columns.

📁 **Output:** `telecom_customer_churn_cleaned.csv`  
✅ Cleaned dataset for EDA (no scaling applied).

---

#### 2️⃣ Feature Encoding & Scaling (For Modeling)
**Purpose:** Prepare features for machine learning algorithms.

**Transformations:**
- **Numerical columns:** Standardized using `StandardScaler()`.
- **Categorical columns:** One-hot encoded using `OneHotEncoder()` (drop first to avoid multicollinearity).

📁 **Output:** `telecom_customer_churn_encoded.csv`  
✅ Fully processed dataset for ML training.

---

## Analysis techniques used
* List the data analysis methods used and explain limitations or alternative approaches.
* How did you structure the data analysis techniques. Justify your response.
* Did the data limit you, and did you use an alternative approach to meet these challenges?
* How did you use generative AI tools to help with ideation, design thinking and code optimisation?

## Ethical considerations
* Were there any data privacy, bias or fairness issues with the data?
* How did you overcome any legal or societal issues?

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