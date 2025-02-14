
# from django.shortcuts import render,get_object_or_404, redirect
# from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
# import json
# from jobs.custom_decorators import check_leave, change_application_status
# import torch
# from torch.utils.data import DataLoader, Dataset
# from transformers import BertTokenizer, BertForQuestionAnswering, AdamW
# # Create your views here.

# # @csrf_protect
# # def requisition(request):
# #     if not request.user.is_authenticated:
# #         return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
# #     if not request.method == 'POST':
# #         return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
# #     try:
# #         json_data = json.loads(request.body)
# #     except Exception :
# #         return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
# #    return render(request, 'ai.html')


# class QADataset(Dataset):
#     def __init__(self, data, tokenizer, max_length=512):
#         self.data = data
#         self.tokenizer = tokenizer
#         self.max_length = max_length

#     def __len__(self):
#         return len(self.data)

#     def __getitem__(self, idx):
#         example = self.data[idx]
#         inputs = self.tokenizer(
#             example["context"],
#             example["question"],
#             padding="max_length",
#             truncation=True,
#             max_length=self.max_length,
#             return_tensors="pt"
#         )

#         answer_text = example["answer"]
#         start_index = example["context"].find(answer_text)
#         end_index = start_index + len(answer_text)

#         if start_index == -1:  
#             start_index = 0
#             end_index = 0
#         inputs["start_positions"] = torch.tensor(start_index, dtype=torch.long)
#         inputs["end_positions"] = torch.tensor(end_index, dtype=torch.long)
#         return {key: val.squeeze(0) for key, val in inputs.items()}


# @csrf_protect
# def chat_page(request):
# 	if not request.user.is_authenticated:
# 		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
# 	return render(request, "chat.html")

# @csrf_protect
# def train_model(request):

# 	model_name = "bert-base-uncased"
# 	tokenizer = BertTokenizer.from_pretrained(model_name)
# 	model = BertForQuestionAnswering.from_pretrained(model_name)


# 	qa_data = [
# 	    {
# 	        "context": "The Line Manager is responsible for completing and submitting a requisition for budget approval.",
# 	        "question": "Who is responsible for submitting a requisition?",
# 	        "answer": "The Line Manager"
# 	    },
# 	    {
# 	        "context": "The Finance team receives, approves, and submits the requisition for approval.",
# 	        "question": "What happens after the requisition is submitted?",
# 	        "answer": "The Finance team receives, approves, and submits the requisition"
# 	    },
# 	    {
# 	        "context": "The CEO is responsible for reviewing and approving the final candidate selection.",
# 	        "question": "Who approves the final candidate selection?",
# 	        "answer": "The CEO"
# 	    },
# 	    {
# 	        "context": "Candidates can view the vacancy and submit their applications on the MICT SETA Vacancies portal.",
# 	        "question": "How do candidates apply for vacancies?",
# 	        "answer": "Candidates can view the vacancy and submit their applications on the MICT SETA Vacancies portal."
# 	    },
# 	    {
# 	        "context": "The HR Manager is responsible for reviewing and publishing the vacancy advert.",
# 	        "question": "Who reviews and publishes the vacancy advert?",
# 	        "answer": "The HR Manager"
# 	    },
# 	    {
# 	        "context": "The HR Team receives and screens applications, then completes the nominee form.",
# 	        "question": "What happens after candidates submit their applications?",
# 	        "answer": "The HR Team receives and screens applications."
# 	    }
# 	]

# 	train_dataset = QADataset(qa_data, tokenizer)
# 	train_dataloader = DataLoader(train_dataset, batch_size=2, shuffle=True)


# 	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 	model.to(device)

# 	optimizer = AdamW(model.parameters(), lr=5e-5)
# 	loss_fn = torch.nn.CrossEntropyLoss()


# 	num_epochs = 3
# 	for epoch in range(num_epochs):
# 		model.train()
# 		total_loss = 0
		
# 		for batch in train_dataloader:
# 			optimizer.zero_grad()
	        

# 			input_ids = batch["input_ids"].to(device)
# 			attention_mask = batch["attention_mask"].to(device)
# 			start_positions = batch["start_positions"].to(device)
# 			end_positions = batch["end_positions"].to(device)


# 			outputs = model(input_ids=input_ids, attention_mask=attention_mask, start_positions=start_positions, end_positions=end_positions)
	        
# 			loss = outputs.loss
# 			loss.backward()
# 			optimizer.step()

# 			total_loss += loss.item()

# 		print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {total_loss:.4f}")

# 	model.save_pretrained("./qa_model")
# 	tokenizer.save_pretrained("./qa_model")
# 	print("Model training complete! Saved to ./qa_model")
# 	return JsonResponse({'message': 'Model training complete', 'status': 'success'}, status=201)



# 	# Function to answer a question
# def answer_question(question):
# 	inputs = tokenizer(question, return_tensors="pt", truncation=True, max_length=512)
	    
# 	with torch.no_grad():
# 		outputs = model(**inputs)

# 	    # Get answer span
# 	answer_start = torch.argmax(outputs.start_logits)
# 	answer_end = torch.argmax(outputs.end_logits) + 1
	    
# 	answer = tokenizer.convert_tokens_to_string(
# 	        tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
# 	    )

# 	return answer

# @csrf_protect
# def chat_live(request):
# 	# Load trained model and tokenizer

# 	if not request.user.is_authenticated:
# 		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
# 	if not request.method == 'POST':
# 		return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
# 	try:
# 		json_data = json.loads(request.body)
# 	except Exception :
# 		return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})


# 	question = json_data.get('question').lower()
# 	model_path = "./qa_model"
# 	tokenizer = BertTokenizer.from_pretrained(model_path)
# 	model = BertForQuestionAnswering.from_pretrained(model_path)
# 	answer = answer_question(question)
# 	return JsonResponse({'message': answer, 'status': 'success'}, status=201)
#  