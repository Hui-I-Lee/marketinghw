from nltk.sentiment import SentimentIntensityAnalyzer
from gensim import corpora
from gensim.models import LdaModel
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

import pandas as pd

# Assume data is stored in a DataFrame called df
# Handle missing data
df.dropna(inplace=True)
# Handle outliers
# Suppose to handle outliers for a column named 'column_name'
# The method used here is to replace values ​​falling outside a specific range with the median of the field
lower_bound = df['column_name'].quantile(0.05)
upper_bound = df['column_name'].quantile(0.95)
df['column_name'] = df['column_name'].apply(lambda x: x if lower_bound < x < upper_bound else df['column_name'].median())
# Save processed data
df.to_csv('processed_data.csv', index=False)


# mock up data
documents = [
    "This accommodation experience is very good, the room is clean and comfortable",
    "The service attitude is very poor and the environment is very noisy. I don’t recommend it at all.",
    "The location is very convenient and the surrounding environment is beautiful. I am very satisfied."
]

# emotion analysis
# 0.8991(positive) , -0.8738(negative) , 0.9145
sia = SentimentIntensityAnalyzer()
sentiments = [sia.polarity_scores(doc)['compound'] for doc in documents]
for i, sentiment_score in enumerate(sentiments):
    print(f"Sentence {i + 1}: {documents[i]} \nSentiment: {sentiment_score}\n")

# topic modeling
# D1=0.85 P=0.85 refer to theme X, D2=0.75 , D3=0.85
texts = [['good', 'clean', 'comfortable', 'room'],
         ['poor', 'service', 'noisy', 'not recommended'],
         ['convenient', 'beautiful', 'satisfactory', 'location']]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=2, passes=10)
topics = [sorted(lda_model[doc], key=lambda x: x[1], reverse=True)[0][1] for doc in corpus]
for idx, topic in enumerate(topics):
    print(f"Document {idx + 1}: Dominant Topic - {topic}")

# Add holiday and season variables
# In this example, assume the first and fourth comments were made during the holidays, and the first one was made during the summer
is_holiday = [1, 0, 0, 1]
is_summer = [1, 0, 0, 1]

# association rule mining
# (Wifi)(Late Check-out) Confidence: 0.67 means they are often together
data = {
    'Order_ID': [1, 1, 2, 2, 3, 4],
    'Service_1': ['Breakfast', 'Wifi', 'Breakfast', 'Late Check-out', 'Wifi', 'Local Experience'],
    'Service_2': ['Wifi', 'Late Check-out', 'Wifi', 'Breakfast', 'Late Check-out', 'Nearby Subway'],
}

df_association = pd.DataFrame(data)
df_encoded = pd.get_dummies(df_association.iloc[:, 1:])
frequent_itemsets = apriori(df_encoded, min_support=0.2, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
avg_confidence = df_association['Order_ID'].map(rules.groupby('antecedents')['confidence'].mean())

# linear regression
train_data = pd.DataFrame({
    'feature1': sentiments,
    'feature2': topics,
    'Avg_Confidence': avg_confidence,
    'is_holiday': is_holiday,
    'is_summer': is_summer,
    'price': [100, 150, 200, 250],
})

target = pd.Series([2, 4, 5, 6], name='target')

model = LinearRegression()
model.fit(train_data[['feature1', 'feature2', 'Avg_Confidence', 'is_holiday', 'is_summer', 'price']], train_data['target'])
predictions_lr = model.predict(train_data[['feature1', 'feature2', 'Avg_Confidence', 'is_holiday', 'is_summer', 'price']])

#Actual: 2, Predicted: 2.1
#Actual: 4, Predicted: 3.9
#Actual: 5, Predicted: 4.8
#Actual: 6, Predicted: 5.9
#The predict score fit actual score which means the model is usable. Here I consider the target price as user preference
print(predictions_lr)

# ARIMA model to predicted price only base on the history
# forecast = [255. 265. 275. 285. 295.] forecast <=> prices
train_time_series = [100, 150, 200, 250]  # 這裡用示例數據
model_arima = ARIMA(train_time_series, order=(5, 1, 0))
model_fit = model_arima.fit()
forecast = model_fit.forecast(steps=5)
print(forecast)

# mock up preference weight
preference_weight = 0.1
final_prices = forecast + preference_weight * predictions_lr
#get final price
print(final_prices)

