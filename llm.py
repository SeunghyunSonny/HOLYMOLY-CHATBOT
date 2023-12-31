

import os
from typing import List, Union
from langchain.llms import HuggingFaceHub
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import BaseMessage, HumanMessage
from models import AsyncCallbackTextHandler, LLM
from logger import get_logger
from utils import Character
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM


# 로거 인스턴스를 생성합니다.
logger = get_logger(__name__)

# Hugging Face API 토큰을 환경 변수에서 가져옵니다.
HUGGINGFACEHUB_API_TOKEN = "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"
tokenizer = AutoTokenizer.from_pretrained("beomi/llama-2-ko-7b")
model = AutoModelForCausalLM.from_pretrained("beomi/llama-2-ko-7b")

pipe = pipeline("text-generation", model="beomi/llama-2-ko-7b")

class LocalLlm(LLM):
    def __init__(self):
        # 로컬 언어 모델을 초기화합니다. 여기서는 Hugging Face의 특정 모델을 사용합니다.
        self.llm = HuggingFaceHub(
            repo_id="beomi/llama-2-ko-7b",  # 'gpt2'는 Hugging Face에 있는 실제 모델 ID로 가정합니다.
            huggingfacehub_api_token="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",# API 토큰 사용
            temperture = 0.7,  # 온도 설정 (0.0 ~ 1.0,
            max_token=100  # 최대 토큰 수 설정 (0 ~ 4096

        )

        # 추가 설정을 수행합니다.
        self.config = {}# 데이터베이스 연결을 초기화합니다.
        self.db = None

    def get_config(self):
        # 현재 설정을 반환합니다.
        return self.config

    async def achat(
            self,
            history: Union[List[BaseMessage], List[str]],
            user_input: str,
            user_input_template: str,
            callback: AsyncCallbackTextHandler,
            character: None,
            metadata: dict = None,
            *args,
            **kwargs,
    ) -> str:
        try:
            # 사용자 입력을 기반으로 컨텍스트를 생성합니다.
            context = self._generate_context(user_input, None)

            # 사용자 입력을 기록에 추가합니다.
            history.append(HumanMessage(content=user_input_template.format(context=context, query=user_input)))

            # 모델을 사용하여 응답을 생성합니다.
            response = await self.llm.agenerate(
                [history],
                callbacks=[callback, StreamingStdOutCallbackHandler()],
                metadata=metadata,
            )

            # 생성된 응답을 로깅하고 반환합니다.
            logger.info(f"Response: {response}")
            return response.generations[0][0].text

        except Exception as e:
            logger.error(f"An error occurred during chat generation: {e}")
            # 오류 메시지를 반환합니다.
            return "An error occurred during chat generation."

    def _generate_context(self, query, character: Character) -> str:
        # 쿼리와 일치하는 문서를 검색하여 컨텍스트를 생성합니다.
        try:
            pass
           # docs = self.db.similarity_search(query)
            #docs = [d for d in docs if d.metadata["character_name"] == character.name]
           # logger.info(f"Found {len(docs)} documents")

           # context = "\n".join([d.page_content for d in docs])
           # return context
        except Exception as e:
           logger.error(f"An error occurred while generating context: {e}")
            # 기본 컨텍스트를 반환하거나 다른 예외 처리를 수행합니다.
           return "An error occurred while generating context."
