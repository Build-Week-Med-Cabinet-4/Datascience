# Data Science Strain API

### Introduction

The Data Science Strain API is a tool used for medical marijuana strain recommendations. The API aims to take user input on the desired effects of marijuana as well as the patient's current medical conditions and return a JSON package containing prescribable marijuana strain names. The Data Science Strain API is part of a collaborative project to create a full web application to help users with their medical marijuana needs.

### Usage

**Python Notebooks**

Located in the "notebooks" directory of this repository is the following ".ipynb" file:

- modeling.ipynb

This file explores the data preprocessing and modeling for the strain recommendation system.

**Strain API**

Deployed on Heroku is a Flask API that takes a JSON package user input containing a key-value pair of "user_input" and a string value. The string value contains all race types, flavors, and effects desired by the user and each word is separated by ```", "``` characters. For best performance from the recommendation model, limit race types to one ```example: "indica"```, flavors to three ```example: "pine, berry, chemical"```, positive effects to five ```example: "relaxed, tingly, happy, creative, aroused"```, and medical effects to five ```example: "depression, cramps, pain, stress, muscle spasms"```.

**Race Types:**

```
["indica", "sativa", "hybrid"]
```

**Positive Effect Types:**

```
['tingly', 'euphoric', 'relaxed', 'focused', 'talkative',
'uplifted', 'aroused', 'hungry', 'energetic', 'giggly',
'sleepy', 'happy', 'creative']
```
**Medical Effect Types:**

```
['inflammation', 'seizures', 'nausea', 'depression',
 'cramps', 'pain', 'spasticity', 'eye pressure',
 'insomnia', 'headache', 'fatigue', 'muscle spasms',
 'lack of appetite', 'stress', 'headaches']
```

**Flavor Types:**

```
['lavender', 'pine', 'sweet', 'cheese', 'vanilla', 'lemon', 'orange',
 'pineapple', 'tree fruit', 'sage', 'pepper', 'pungent', 'tea',
 'nutty', 'blueberry', 'flowery', 'violet', 'rose', 'ammonia', 'honey',
 'diesel', 'chestnut', 'minty', 'plum', 'tar', 'tropical', 'earthy',
 'pear', 'coffee', 'woody', 'peach', 'skunk', 'chemical', 'strawberry',
 'apricot', 'menthol', 'tobacco', 'mint', 'citrus', 'grapefruit', 'mango',
 'grape', 'berry', 'apple', 'spicy/herbal', 'butter', 'lime', 'blue cheese']
```

**Calling the API**

Example input package POST request to ```https://med-cabinet-4-api.herokuapp.com/recommend```
```
{
"user_input": "indica, pine, berry, chemical, 
                relaxed, tingly, happy, creative, 
                aroused, depression, cramps, 
                pain, stress, muscle spasms"
}
```

Example output to be received
```
{
    "strain_five": "Blackberry Rhino",
    "strain_four": "Blackberry Chem OG",
    "strain_one": "Rare Dankness #1",
    "strain_three": "Gutbuster",
    "strain_two": "Green Love Potion"
}
```


## Overview of the Strain Recommendation Process

**Web Scrapping**

To create a dataset for use in recommendation modeling a process of website scrapping is utilized. The data gathered is from the popular marijuana website [Leafly.com](https://www.leafly.com/strains/lists) as it contains information on marijuana strain names, race, effects, flavors, descriptions, and ratings. The web scraping was done by various team members using the HTML parsing tool [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/). The result from the web scrapping process is a relatively messy dataset containing the above-listed features.

**The Dataset**

The dataset from the web scrapping process contains null values and mixed formatting within the string values of each feature. The dataset has a shape of 2,887 observations (rows) and six features (columns). The features of the dataset are strain name, race type (Indica, Sativa, or Hybrid), effects, flavors, descriptions, and ratings. The dataset is put through cleaning, feature engineering, and data preprocessing processes.

**Data Cleaning**

The cleaning process involves removing rows with missing information and the standardization of string values. All observations with missing values in the strain name and effects features are removed from the dataset (The other feature’s missing values do not affect recommendation modeling). String values within features are converted to lowercase, misspellings are corrected, and punctuation/ stop words are removed.

**Feature Engineering**

To create a more targeted recommendation process feature engineering of the effects column is done. The effects column is split into three new features "postive_effects", "negative_effects", and "medical_effects". Contents of the original effects column are compared against the predefined positive effect, negative effect, and medical effect lists of words. After comparison, the effect is moved to the correct feature. The new features contain string values of effects separated by ```", "``` characters.

**Data Preprocessing**

To prepare the data for recommendation modeling the features strain name, rating, and description are removed from the dataset. The remaining features are put through a modified one-hot encoding approach. The approach creates a new feature for each race, flavor, and effect type available in the predefined lists of words and fills in each observation’s values with zero by default. Then, for the words present in each observation the associated word feature will be changed to one. The resulting dataset is one that can be mapped within the recommendation model space as well as being optimal for user input.

**User Input**

The input JSON object received from the client comes in containing a key-value pair of ```"user_input"``` and a string value containing all desired effects and flavors requested by the patient separated by ```", "```. The user input data is converted into a list where each index represents an effect out of all total effects. Effects present in the user input string are reflected by a value of one in the created list. The resulting list is in a numerical format similar to the dataset created in the data preprocessing step.

**The Model**

The recommendation model used is sciklearn’s [Nearest Neighbor](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html) Recommender. The Nearest Neighbor model is an unsupervised learning approach that commits the input dataset to its memory and given new observations returns the observations in memory that are closets in distance to the input. Once trained within the "modeling.ipynb" file the Nearest Neighbor model is picked and saved in a directory to be referenced by the strain API after receiving user input. The model outputs the top five closest strains in space to the input observation.
