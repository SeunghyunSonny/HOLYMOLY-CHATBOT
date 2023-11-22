import os
from typing import List, Union
from langchain.llms import HuggingFaceHub
# 필요한 모듈들을 임포트합니다.
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import BaseMessage, HumanMessage
from database.chroma import get_chroma
from models import (
    #AsyncCallbackAudioHandler,
    AsyncCallbackTextHandler,
    LLM,

)

#혹시 몰라서 제작을 넣어봄
from logger import get_logger
from utils import Character, timed
#import llama2wrapper
# 로거 인스턴스를 생성합니다.
logger = get_logger(__name__)



#llama2-wrapper = LLAMA2_WRAPPER(
#model_path = "./beomi/llama-2-ko-7b",
#backend_type = "transformers",
#load_in_8bit = True
#)


# Hugging Face API 토큰을 설정합니다. 이 토큰은 환경 변수에서 가져옵니다.
HUGGINGFACEHUB_API_TOKEN = "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"
if HUGGINGFACEHUB_API_TOKEN is None:
    logger.error("HUGGINGFACEHUB_API_TOKEN is not set in the environment variables.")
    # 적절한 예외 처리를 수행합니다. 필요에 따라 프로그램을 종료할 수 있습니다.
    raise EnvironmentError("HUGGINGFACEHUB_API_TOKEN is required.")


class LocalLlm(LLM):
    def __init__(self):
        # 로컬 언어 모델을 초기화합니다. 여기서는 Hugging Face의 특정 모델을 사용합니다.
        self.llm = HuggingFaceHub(
            repo_id="beomi/llama-2-ko-7b",  # 이 값은 실제 사용하는 모델의 식별자로 변경되어야 합니다.
            model_kwargs={"temperature": 0.5, "max_length": 64, "streaming": True}
        )

        # 추가 설정을 수행합니다.
        self.config = {"model": "local_trained_model", "temperature": 0.5, "streaming": True}
        self.db = get_chroma()  # 데이터베이스 연결을 초기화합니다.

    def get_config(self):
        # 현재 설정을 반환합니다.
        return self.config

    @timed
    async def achat(
        self,
        history: Union[List[BaseMessage], List[str]],
        user_input: str,
        user_input_template: str,
        callback: AsyncCallbackTextHandler,
        #audioCallback: AsyncCallbackAudioHandler,
        character: Character,
        metadata: dict = None,
        *args,
        **kwargs,
    ) -> str:
        try:
            # 사용자 입력을 기반으로 컨텍스트를 생성합니다.
            context = self._generate_context(user_input, character)

            # 사용자 입력을 기록에 추가합니다.
            history.append(HumanMessage(content=user_input_template.format(context=context, query=user_input)))

            # 모델을 사용하여 응답을 생성합니다.
            response = await self.llm.agenerate(
                [history],
                callbacks=[callback, StreamingStdOutCallbackHandler()],#AUDIOCALLBACK삽입
                metadata=metadata,
            )

            # 생성된 응답을 로깅하고 반환합니다.
            logger.info(f"Response: {response}")
            return response.generations[0][0].text

        except Exception as e:
            logger.error(f"An error occurred during chat generation: {e}")
            # 여기서 적절한 예외 처리를 수행하거나, 오류 메시지를 반환할 수 있습니다.
            raise  # 또는 사용자 정의 오류 메시지 반환

    def _generate_context(self, query, character: Character) -> str:
        # 쿼리와 일치하는 문서를 검색하여 컨텍스트를 생성합니다.
        try:
            docs = self.db.similarity_search(query)
            docs = [d for d in docs if d.metadata["character_name"] == character.name]
            logger.info(f"Found {len(docs)} documents")

            context = "\n".join([d.page_content for d in docs])
            return context
        except Exception as e:
            logger.error(f"An error occurred while generating context: {e}")
            # 여기서 적절한 예외 처리를 수행하거나, 기본 컨텍스트를 반환할 수 있습니다.
            raise  #
