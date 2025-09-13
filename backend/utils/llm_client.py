import os
import json
import yaml
import time
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Providers
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

# Load env vars
load_dotenv()

# Default provider
PROVIDER = os.getenv("PROVIDER", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-pro")


def load_prompt_from_yaml(yaml_path: Path) -> dict:
    """Load system & user prompts from YAML file."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        prompt_data = yaml.safe_load(f)
    if "system" not in prompt_data or "user" not in prompt_data:
        raise ValueError("❌ YAML must contain 'system' and 'user'")
    return prompt_data


def get_llm(provider: str):
    """Return the right LLM object based on provider name."""
    if provider == "ollama":
        return ChatOllama(model=OLLAMA_MODEL, temperature=0.7)
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("❌ Missing OPENAI_API_KEY in .env")
        return ChatOpenAI(model=OPENAI_MODEL, temperature=0.7, api_key=api_key)
    elif provider == "google":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("❌ Missing GOOGLE_API_KEY in .env")
        return ChatGoogleGenerativeAI(model=GOOGLE_MODEL, temperature=0.7, google_api_key=api_key)
    else:
        raise ValueError(f"❌ Unsupported provider: {provider}")


def call_llm_with_yaml_prompt(
    yaml_path: Path,
    json_input: dict,
    provider: str = PROVIDER,
    verbose: bool = True
) -> str:
    """Call chosen provider LLM using LangChain prompt."""

    # נבנה JSON יפה
    formatted_input = json.dumps(json_input, ensure_ascii=False, indent=2)
    prompt_data = load_prompt_from_yaml(yaml_path)

    system_prompt = prompt_data["system"]
    user_prompt = prompt_data["user"]  # נשאיר את {json_input} בלי להחליף

    # בונים את ה־prompt עם placeholder אמיתי
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt),
    ])

    llm = get_llm(provider)
    chain = prompt | llm | StrOutputParser()

    if verbose:
        print("🔧 Debug: Provider =", provider)
        print("🔧 Debug: Using model =",
              OLLAMA_MODEL if provider == "ollama" else
              OPENAI_MODEL if provider == "openai" else
              GOOGLE_MODEL if provider == "google" else "Unknown")
        print("🔧 Debug: Final System Prompt:\n", system_prompt)
        print("🔧 Debug: Final User Prompt Template:\n", user_prompt)
        print("🔧 Debug: Injected JSON Input:\n", formatted_input)

    # מעבירים את המשתנה ל־invoke
    start_time = time.time()
    result = chain.invoke({"json_input": formatted_input})
    duration = time.time() - start_time

    if verbose:
        print(f"✅ LLM call successful via {provider}")
        print(f"⏱️ Duration: {duration:.2f}s")
        print("📄 LLM Raw Output:\n", result)

    return result.strip()
