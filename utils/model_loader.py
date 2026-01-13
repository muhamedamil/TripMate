import os
import sys
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from logger.logger import logger
from exception.exception_handling import TripMateException

load_dotenv()


class ConfigLoader:
    """
    A wrapper for loading configuration.
    """

    def __init__(self):
        """
        Initializes ConfigLoader and loads the configuration.
        """
        try:
            logger.info("Initializing ConfigLoader")
            self.config = load_config()
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def __getitem__(self, key):
        """
        Allows dictionary-like access to the configuration.
        """
        return self.config[key]


class ModelLoader(BaseModel):
    """
    A class to load LLM models based on provider.
    """

    model_provider: Literal["openai", "groq"] = "groq"
    config_loader: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        """
        Initializes the configuration loader after model initialization.
        """
        try:
            self.config_loader = ConfigLoader()
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        Load and return the LLM model based on the specified provider.

        Returns:
            BaseChatModel: The loaded LangChain chat model.

        Raises:
            TripMateException: If the model provider is invalid or loading fails.
        """
        try:
            logger.info(f"Loading LLM from provider: {self.model_provider}")

            if self.model_provider == "groq":
                groq_api_key = os.getenv("GROQ_API_KEY")
                model_name = self.config_loader["llm"]["groq"]["model_name"]
                logger.info(f"Loading Groq model: {model_name}")
                llm = ChatGroq(model=model_name, api_key=groq_api_key)
            elif self.model_provider == "openai":
                openai_api_key = os.getenv("OPENAI_API_KEY")
                model_name = self.config_loader["llm"]["openai"]["model_name"]
                logger.info(f"Loading OpenAI model: {model_name}")
                llm = ChatOpenAI(model=model_name, api_key=openai_api_key)
            else:
                raise ValueError(f"Invalid model provider: {self.model_provider}")

            logger.info("LLM loaded successfully")
            return llm
        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error
