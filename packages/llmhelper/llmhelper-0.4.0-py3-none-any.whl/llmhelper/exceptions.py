__all__ = [
    "ParseJsonResponseError",
    "ChatError",
    "GetTextEmbeddingsError",
    "GetRerankScoresError",
    "NoneValueError",
    "VectorStoreNoneValueError",
    "EmbeddingsNoneValueError",
    "RerankNoneValueError",
]


class ParseJsonResponseError(RuntimeError):
    """LLM输出不能解析为json数据。"""

    def __init__(self):
        super().__init__("LLM输出不能解析为json数据。")


class ChatError(RuntimeError):
    """大模型对话失败。"""

    def __init__(self):
        super().__init__("大模型对话失败。")


class GetTextEmbeddingsError(RuntimeError):
    """获取文本向量失败。"""

    def __init__(self):
        super().__init__("获取文本向量失败。")


class GetRerankScoresError(RuntimeError):
    """获取rerank得分失败。"""

    def __init__(self):
        super().__init__("获取rerank得分失败。")


class NoneValueError(RuntimeError):
    pass


class VectorStoreNoneValueError(NoneValueError):
    """向量数据库不允许None值进行查询和插入。"""

    def __init__(self):
        super().__init__("向量数据库不允许None值进行查询和插入。")


class EmbeddingsNoneValueError(NoneValueError):
    """None值无法进行向量化处理。"""

    def __init__(self):
        super().__init__("None值无法进行向量化处理。")


class RerankNoneValueError(NoneValueError):
    """None值无法参与重排。"""

    def __init__(self):
        super().__init__("None值无法参与重排。")
