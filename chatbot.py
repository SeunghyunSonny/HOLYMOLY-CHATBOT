from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("beomi/llama-2-ko-7b")
model = AutoModelForCausalLM.from_pretrained("beomi/llama-2-ko-7b")


def get_bot_response(message: str) -> str:
    # Encode the input message
    input_ids = tokenizer.encode(message, return_tensors='pt')

    # Generate a response using the model
    output = model.generate(input_ids, max_length=50, num_return_sequences=1)

    # Decode the response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response
