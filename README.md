# Chapter18: Topic-Modeling
## http://www.datascience-in-tourism.com/

***Author***
Roman Egger - Salzburg University of Applied Sciences, Innovation and Management in Tourism

![paris.jpg](https://github.com/DataScience-in-Tourism/Chapter-18-Topic-Modeling/blob/main/data/paris.jpg)

### Abstract

Due to the rapid growth of texts in today’s society, much of which is produced via online social networks in the form of user-generated content, extracting useful information from unstructured text poses quite a challenge. However, thanks to the rapid development of natural language processing algorithms, including topic modelling techniques that help to discover latent topics in text documents such as online reviews or Twitter and Facebook posts, this challenge can be confronted. As such, topic modelling approaches have been gaining popularity in the field of tourism; yet, often little insight is given into the creation process and the quality of topic modeling results. Thus, this chapter aims to introduce several topic modelling algorithms, to explain their intuition in a brief and concise manner, and to provide tips and hints in relation to the necessary (pre-)processing steps, proper hyperparameter tuning, and comprehensible evaluation of the results.

In this Jupyter Notebooks, we will do a complete topic modelling walkthrough with a dataset from airbnb using five different topic-modeling approches: 
* Latent Dirichlet Allocation (LDA)
* None- Negative Matrix Factorizaton (NMF) 
* Correlation Expanation CorEX
* Top2Vec
* BERTopic

The dataset we will use to extract topics from was crawled by the author and contains 2890 descriptions of airbnb-Experiences from the following European cities: Amsterdam, Athens, Berlin, Brussels, Copenhagen, Helsinki, London, Madrid, Oslo, Paris, Prague, Rome, Stockholm, Viwenna and Warsaw.

### Environment Setup

This notebooks were created using `Python 3.6`.  To set-up your local environment run in terminal the commands below:

```bash
# Clone the repository.

# (Windows Optional) Create a new Python environment and activate it.
python -m venv .env
.env\Scripts\activate

# (Ubuntu Optional) Create a new Python environment and activate it.
python3 -m venv .env
source .env/bin/activate

# Install the dependencies.
pip install -r requirements.txt

# Use your preferred IDE in order to run the notebooks
```
