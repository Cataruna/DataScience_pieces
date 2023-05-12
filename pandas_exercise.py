#Basic pandas exercises, originally solved in Jupyter

import pandas as pd
ecom = pd.read_csv('Ecommerce Purchases')


print(ecom.info())

#what is the average purchase price?
print(ecom['Purchase Price'].mean())

#what about the highest and lowest?
print(ecom['Purchase Price'].max())
print(ecom['Purchase Price'].min())

#how many people have english as their language of choice?
print(ecom[ecom['Language']=='en'].count())

#how many people are lawyers?
print(ecom[ecom['Job'] == 'Lawyer'].info())

#how many people made the purchase during AM and how many during PM?
print(ecom['AM or PM'].value_counts())

#what are the most common job titles?
print(ecom['Job'].value_counts().head(5))

#what is the purchase price from the tranzaction made from lot "90 WT"?
print(ecom[ecom['Lot']=='90 WT']['Purchase Price'])

#what is the email of the person with credit card number: "4926535242672853"
print(ecom[ecom["Credit Card"] == 4926535242672853]['Email'] )

#how many people have american express as their credit card provider and made a purchase above $95?
print(ecom[(ecom['CC Provider']=='American Express') & (ecom['Purchase Price']>95)].count())

#how many people have a credit card that expires in 2025?
print(sum(ecom['CC Exp Date'].apply(lambda x: x[3:]) == '25'))

#what are the 5 most popular email providers/hosts?
print(ecom['Email'].apply(lambda x: x.split('@')[1]).value_counts().head(5))