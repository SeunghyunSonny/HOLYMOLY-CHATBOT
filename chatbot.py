
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging

# 가정: 로거를 설정합니다.
logger = logging.getLogger(__name__)

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

# 비동기 챗 핸들러 함수의 정의

def _generate_context(self, query, character) -> str:
    # 쿼리와 일치하는 문서를 검색하여 컨텍스트를 생성합니다.
    try:
        # 데이터베이스 검색 가정
        docs = self.db.similarity_search(query)
        docs = [d for d in docs if d.metadata["character_name"] == character.name]
        logger.info(f"Found {len(docs)} documents")

        context = "\n".join([d.page_content for d in docs])
        return context
    except Exception as e:
        logger.error(f"An error occurred while generating context: {e}")
        # 기본 컨텍스트를 반환하거나 다른 예외 처리를 수행합니다.
        return "Default context"