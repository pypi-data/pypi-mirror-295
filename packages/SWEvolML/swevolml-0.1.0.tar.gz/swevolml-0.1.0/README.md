# Project description 

This Python package is designed to classify fish species, distinguishing between Bream and Smelt.
We use the KNN algorithm to implement this prediction system

# what is special about

1. This preidict system start with empty dataframe
2. This machine learning rate will increase as much as the data you put in
3. This machine will show you the ratio of correct answers to incorrect answers.Therefore, you can gauge the machine's level of growth from the accuracy rate.
5. This machine will show you the location of your data which you typed  

# System Envrioment and Dependencies for Use
![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Pandas](https://img.shields.io/badge/pandas-2.2.2-red)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.5.1-green)
![Plotext](https://img.shields.io/badge/plotext-5.2.8-yello)

# How to install
```python
$ pip install SWEvolML 
```
# How to use 
Experience the machine learning program that grows through the repeated execution of commands

```python
$ gml
길이와 무게를 입력하세요:18.5 17  # Input length and weight data separated by spaces to get the prediction.
빙어                              # ML will tell you prediction
정답을 입력하세요(y or n):y       # Input yes or no depending on whether the answer is correct or incorrect
역시 그렇군요                     # ML will answer as your respond  

                                  
[정답율]                                                              # print accuracy ratio 
[##########################################--------] 85.00%
[입력 데이터 위치]
           location of input data                                     # print location of your recent input data on scatter plot   
     ┌─────────────────────────────────┐                           
340.0┤                                B│
284.6┤                              B B│
173.8┤                                 │
118.3┤                                 │
  7.5┤SS  S           *                │
     └┬───────┬───────┬───────┬───────┬┘
    10.5    14.5    18.5    22.5   26.5
weight             length

```
