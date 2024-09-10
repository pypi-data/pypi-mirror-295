# llmhelper

LLM helper library.

## 安装

```shell
pip install llmhelper
```

## 环境变量

- OPENAI_API_KEY
- OPENAI_BASE_URL
- OPENAI_CHAT_MODEL
- OPENAI_EMBEDDINGS_MODEL
- OPENAI_RERANK_MODEL
- LLMHELPER_REDIS_STACK_URLS

### LLMHELPER_REDIS_STACK_URLS

`LLMHELPER_REDIS_STACK_URLS`是字典类型，表示指定索引的向量数据库地址。例如：

```python
LLMHELPER_REDIS_STACK_URLS = {
  "default": "redis://localhost:6379/0",
  "kb:qa": "redis://192.168.1.31:6379/0",
  "kb:doc": "redis://192.168.1.32:6379/0",
  "ai:instruct": "redis://192.168.1.33:6379/0",
}
```

## 工具集

- exceptions
  - ParseJsonResponseError
  - ChatError
  - GetTextEmbeddingsError
  - GetRerankScoresError
  - NoneValueError
  - VectorStoreNoneValueError
  - EmbeddingsNoneValueError
  - RerankNoneValueError
- base
  - get_llmhelper_config
  - set_llmhelper_default_config
  - set_llmhelper_config
  - get_default_llm
  - get_default_chat_model
  - get_default_embeddings_model
  - get_default_rerank_model
  - get_template_engine
  - get_llm_base_url
  - get_llm_api_url
- template
  - get_template_prompt_by_django_template_engine
  - get_template_prompt_by_jinjia2
  - get_template_prompt
- llm
  - get_messages
  - parse_json_response
  - chat
  - jsonchat
  - streaming_chat
- embeddings
  - OpenAIEmbeddings
  - get_text_embeddings
- rerank
  - get_rerank_scores
- vectorestores
  - RedisVectorStore

## 版本记录

### v0.1.0

- 版本首发。

### v0.2.0

- 添加embeddings模型操作支持。
- 添加rerank模型操作支持。

### v0.3.0

- 添加向量数据库操作支持。

### v0.4.0

- 添加django_vectorstore_index_model抽象类。
