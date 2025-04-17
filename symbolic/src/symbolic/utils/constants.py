import string

stop_words = {'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'do', 'da',
              'e', 'que', 'eu', 'tu', 'ele', 'ela', 'eles', 'vós', 'nós', 'você', 
              'vocês', 'me', 'te', 'lhe', 'nos', 'vos', 'lhes', 'mim', 'ti', 'si'}
punctuation = set(string.punctuation)
PREPROCESSING_COLUMN = 'cleaned_comment'
SENTIMENT_COLUMN = 'sentiment'
DEFAULT_MOVIE = 'Shrek 2'
SENTIMENT_IMAGES = {
    0: {
        'image': 'https://cdn.shopify.com/s/files/1/1061/1924/files/Neutral_Face_Emoji.png?9898922749706957214',
        'label': 'Opiniões divergentes'
    },
    1: {
        'image': 'https://cdn.shopify.com/s/files/1/1061/1924/files/Smiling_Face_Emoji.png?9898922749706957214',
        'label': 'Recomendado'
    },
    -1: {
        'image': 'https://cdn.shopify.com/s/files/1/1061/1924/files/Sad_Face_Emoji.png?9898922749706957214',
        'label': 'Não recomendado'
    }
}