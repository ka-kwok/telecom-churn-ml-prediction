# **Telecom Churn Analytics:** 
## ***Building Predictive Models to Improve Customer Retention***

## 🔹 Abstract
This project explores customer churn prediction for a telecom company using the **Telecom Customer Churn dataset**. 
The analysis follows a structured workflow from **data profiling → data cleaning → EDA → feature engineering → ML modeling → churn prediction application**. 

## 🔹 Table of Contents
1. Introduction & Business Requirements  
2. Dataset Description
3. Hypothesis and Methodology
4. 

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

    * Achieve at least X% recall on churners (to minimize missed at‑risk customers) while maintaining acceptable precision.

📈 Business Impact
* Reduce customer churn rate

* Improve retention campaign ROI

* Strengthen customer loyalty and lifetime value

🔹 2. Dataset Description 
 * Datasets used for this analysis is the retail data set from Kaggle (https://www.kaggle.com/datasets/mubeenshehzadi/customer-churn-dataset/). 

## 📄 Customer Churn Dataset Fields

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


## 🔹 3.Hypothesis and how to validate?
* H1: Customers on month-to-month contracts are more likely to churn than those on annual contracts.

* H2: Higher monthly charges are positively correlated with churn probability.

* H3: Customers with longer tenure are less likely to churn.

* H4: Customers who use multiple services (e.g., internet + phone + TV) have lower churn rates than single-service customers.

* H5: Payment method (e.g., electronic check vs. direct debit) influences churn likelihood.

## Project Plan
* Outline the high-level steps taken for the analysis.
* How was the data managed throughout the collection, processing, analysis and interpretation steps?
* Why did you choose the research methodologies you used?

## The rationale to map the business requirements to the Data Visualisations
* List your business requirements and a rationale to map them to the Data Visualisations

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