#!/usr/bin/env python
# coding: utf-8

# # DATA COLLECTION FROM EXCEL SHEET

# In[1]:


# importing important libraries for cleaning and visualizing the data  
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


# lOADING DATA
df=pd.read_csv(r"C:\Users\maqpr\Downloads\CAR DETAILS FROM CAR DEKHO.csv")


# # CLEANING DATA

# In[3]:


df.head(5)


# In[4]:


df.tail(5)


# In[5]:


df.dtypes


# In[6]:


df.info()


# In[7]:


df.describe()


# In[8]:


df.columns


# In[9]:


df['name'].nunique()


# In[10]:


df['year'].nunique()


# In[11]:


df['selling_price'].nunique()


# In[12]:


df['km_driven'].nunique()


# In[13]:


df['fuel'].nunique()


# In[14]:


df['seller_type'].nunique()


# In[15]:


df['transmission'].nunique()


# In[16]:


df['owner'].nunique()


# In[17]:


df.isnull().sum()


# In[18]:


df.isnull().sum().sum()


# In[19]:


df.shape


# In[20]:


# checking outliers
sns.boxplot(data=df)
plt.show()


# In[21]:


#There are some outliers viewed in 'selling_price' columns 


# In[22]:


#removing outliers by IQR method
Q1 = df.selling_price.quantile(0.25)
Q3 = df.selling_price.quantile(0.75)


# In[23]:


IQR = Q3 - Q1


# In[24]:


upper_outliers = Q3 + 1.5*IQR
lower_outliers = Q1 - 1.5*IQR


# In[25]:


upper_outliers,lower_outliers


# In[26]:


df2 =  df[df.selling_price<upper_outliers]


# In[27]:


df.shape


# In[28]:


df2.shape


# In[29]:


sns.boxplot(data=df2)
plt.show()


# In[30]:


# outliers removed


# In[31]:


df2.head()


# In[32]:


#ML PIPELINE
 # independent variable
X = df2.drop('selling_price',axis=1)
 # dependent variable
y = df2['selling_price']


# In[33]:


X.head()


# In[34]:


y.head()


# In[35]:


from sklearn.linear_model import LinearRegression
model1 = LinearRegression()
model1


# In[36]:


from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)


# In[37]:


from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.datasets import fetch_openml
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split , RandomizedSearchCV
from sklearn.feature_selection import SelectPercentile,chi2


# In[38]:


numeric_features = ["year", "km_driven"]
numeric_transformer = Pipeline(
    steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
)

categorical_features = ["name", "fuel", "seller_type","transmission","owner"]
categorical_transformer = Pipeline(
    steps=[
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ("selector", SelectPercentile(chi2, percentile=50)),
    ]
)
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)


# In[39]:


clf = Pipeline(
    steps=[("preprocessor", preprocessor), ("classifier", model1)]
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

clf.fit(X_train, y_train)
y_pred=clf.predict(X_test)
print("model score:" , clf.score(X_test, y_test))


# In[40]:


from sklearn.metrics import r2_score,mean_absolute_error


# In[41]:


r2_score(y_test,y_pred)


# In[42]:


mean_absolute_error(y_test,y_pred)


# In[43]:


clf


# In[44]:


import pickle


# In[45]:


pickle.dump(clf,open('Linear.pkl','wb'))


# In[46]:


pwd


# In[47]:





