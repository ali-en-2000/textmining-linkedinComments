from scipy.special import softmax
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from tqdm import tqdm
from tqdm.notebook import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd
import sqlite3
import os
from django.conf import settings

from .models import miningData


def mining_comments(url):
    url = url + "&utm_medium=member_desktop"
    print('step1 ' )

    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * from crawler_comment WHERE postUrl = '{}'".format(url), conn)

    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    print('step2 ' )
    

    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification. from_pretrained(MODEL)

    print('step3 ' )

    def polarity_scores_roberta(example):        
        encode_text = tokenizer(example, return_tensors='pt')
        output = model(**encode_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        scores_dict = {
            'roberta_neg': scores[0],
            'roberta_neu': scores[1],
            'roberta_pos': scores[2]
        }
        return scores_dict


    res = {}
    for i, row in tqdm(df.iterrows(), total=len(df)):
        try:
            text = row['text']
            myid = row['id']
            vader_result = sia.polarity_scores(text)
            vader_result_rename = {}
            for key, value in vader_result.items():
                vader_result_rename[f"vader_{key}"] = value

            roberta_result = polarity_scores_roberta(text)

            both = {**vader_result_rename, **roberta_result}
            res[myid] = both

        except RuntimeError:
            print(f'Broke for id {myid}')

    print('step5 ' )

    result_df = pd.DataFrame(res) .T
    result_df = result_df.reset_index().rename(columns={'index': 'id'})
    result_df = result_df.merge(df, how='left')
    
    for index, row in result_df.iterrows():
        model_instance = miningData()
        model_instance.vader_neg = row['vader_neg'] if row['vader_neg'] is not None else 0.00
        model_instance.vader_neu = row['vader_neu'] if row['vader_neu'] is not None else 0.00
        model_instance.vader_pos = row['vader_pos'] if row['vader_pos'] is not None else 0.00
        model_instance.vader_compound = row['vader_compound'] if row['vader_compound'] is not None else 0.00
        model_instance.roberta_neg = row['roberta_neg'] if row['roberta_neg'] is not None else 0.00
        model_instance.roberta_neu = row['roberta_neu'] if row['roberta_neu'] is not None else 0.00
        model_instance.roberta_pos = row['roberta_pos'] if row['roberta_pos'] is not None else 0.00
        model_instance.text = row['text']
        model_instance.author = row['author']
        model_instance.postUrl = row['postUrl']

        model_instance.save()

    print('step6 ' )

