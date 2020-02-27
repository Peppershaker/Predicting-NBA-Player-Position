# NBA Player Position Prediction
![bball](https://user-images.githubusercontent.com/15576531/75482451-e2891580-5972-11ea-9293-4541da04722b.jpg)

### Project Goal
* To gain a deeper understanding of player play styles. Many players in the NBA play hybrid positions, such as a mix of point guard and small forward. We want to be able to mathematically describe their play style. I.E. 30% point guard and 70% small forward.
* This project was spun out of my broader efforts to predict fantasy basketball points. I found the player labels assigned by the league only captures the position the player plays most often. Thus, when using these labels in other prediction tasks, valuable information about the player was lost. I want a probability distribution over all labels instead.

### Main Results

* ~77% top 1 accuracy, ~91% top 2 accuracy, ~99% top 3 accuracy

### Language, Technologies & Packages

* Language: Python, Bash
* Packages: SK-Learn, Pandas, Flask
* Technologies: Docker

### What was done

* Models tried: Decision Tree (Baseline), XGBoost, Random Forest, Multinomial Logistic Regression, DBSCAN /w PCA, Kernel SVM ( Gaussian RBF, polynomial with degrees two and three)
* Built web scrapers to collect NBA and ESPN data
* Exploratory data analysis to look at the structure of the data and what models are good candidates
* Deployed as API via Flask in Docker

### View the Project
1. [Getting, cleaning and loading data](https://github.com/Peppershaker/Predicting-NBA-Player-Position/blob/master/1.%20Getting%2C%20cleaning%20and%20loading%20data.ipynb)
2. [EDA](https://github.com/Peppershaker/Predicting-NBA-Player-Position/blob/master/2.%20EDA.ipynb)
3. [Modeling](https://github.com/Peppershaker/Predicting-NBA-Player-Position/blob/master/3.%20Modeling.ipynb)
4. [Deploy as web API via Dockerized Flask app](https://github.com/Peppershaker/Predicting-NBA-Player-Position/blob/master/4.%20Deploy%20as%20web%20API%20via%20dockerized%20Flask%20app.ipynb)
