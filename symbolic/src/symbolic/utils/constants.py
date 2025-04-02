import string

stop_words = {'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'do', 'da',
              'e', 'que', 'eu', 'tu', 'ele', 'ela', 'eles', 'vós', 'nós', 'você', 
              'vocês', 'me', 'te', 'lhe', 'nos', 'vos', 'lhes', 'mim', 'ti', 'si'}
punctuation = set(string.punctuation)
PREPROCESSING_COLUMN = 'cleaned_comment'
SENTIMENT_COLUMN = 'sentiment'