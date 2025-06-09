from transformers import AutoTokenizer, AutoModelForSequenceClassification

bert_model = "jvcarvoli/bertimbau-for-sentiment"
tokenizer = AutoTokenizer.from_pretrained(bert_model)
model = AutoModelForSequenceClassification.from_pretrained(bert_model, subfolder="checkpoint-1875")
