from llama_cpp import Llama
from llama_cpp_agent import LlamaCppAgent, MessagesFormatterType
from llama_cpp_agent.providers import LlamaCppPythonProvider
from llama_cpp_agent.chat_history import BasicChatHistory
from llama_cpp_agent.chat_history.messages import Roles

SYSTEM_PROMPT = "analyze sentiment" #Customize system prompt to fit your need
CHAT_TEMPLATE = MessagesFormatterType.LLAMA_3  #Prompt format to use
MODEL_PATH = "Llama-3.2-1B-Instruct-Q4_K_M.gguf" #Llama-3.2-1B-Instruct-Q4_K_M.gguf used for chat bot style interaction https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf
TEMPERATURE=0.3  #For small models, low temperature is often better
MAX_NEW_TOKENS = 1024  #Max tokens to output
CONTEXT_WINDOW=8000 #Max context window. Up to 128k. The higher the value, the more GPU memory you will need
N_GPU_LAYERS=-1  #Number of layers to put on GPU. -1 = all
N_BATCH=1024  #Increase if long prompts and you need faster inference.

llm = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=N_GPU_LAYERS,
    n_batch=N_BATCH,
    n_ctx=CONTEXT_WINDOW

)

provider = LlamaCppPythonProvider(llm)
settings = provider.get_provider_default_settings()
settings.temperature = TEMPERATURE
settings.max_tokens = MAX_NEW_TOKENS
settings.stream = True

agent = LlamaCppAgent(
    provider,
    system_prompt=SYSTEM_PROMPT,
    predefined_messages_formatter_type=CHAT_TEMPLATE,
    debug_output=False
)

prompt = "does this sound positive or negative: I don't like bananas"

response = agent.get_chat_response(
    prompt,
    llm_sampling_settings=settings,
    #chat_history=chat_history, Not useful here but to be used if you want to keep track of previous prompts
    returns_streaming_generator=True,
    print_output=False
)


for chunk in response:
    print(chunk)