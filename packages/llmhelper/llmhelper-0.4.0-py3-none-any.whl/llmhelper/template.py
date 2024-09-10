from zenutils import importutils
from .base import get_template_engine
from .base import set_llmhelper_default_config

__all__ = [
    "get_template_prompt_by_django_template_engine",
    "get_template_prompt_by_jinjia2",
    "get_template_prompt",
]


def get_template_prompt_by_django_template_engine(
    template_name: str,
    prompt: str = None,
    **context,
):
    """使用django模板引擎生成最终提示词。"""
    from django.template.loader import render_to_string

    return render_to_string(
        template_name=template_name,
        context={
            "prompt": prompt,
            **context,
        },
    )


def get_template_prompt_by_jinjia2(
    template_name: str,
    prompt: str = None,
    **context,
):
    """使用jinja2模板引擎生成最终提示词。"""
    from jinja2 import Environment
    from jinja2 import FileSystemLoader

    environment = Environment(loader=FileSystemLoader("templates/"))
    tempalte = environment.get_template(template_name)
    return tempalte.render(prompt=prompt, **context)


def get_template_prompt(
    template_name: str,
    prompt: str = None,
    template_engine=None,
    **context,
):
    """根据提示词模板、用户问题和其它参数，生成最终的提示词。"""
    if template_engine:
        if callable(template_engine):
            return template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )
        else:
            template_engine = importutils.import_from_string(template_engine)
            return template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )
    else:
        template_engine = get_template_engine()
        if not template_engine:
            return get_template_prompt_by_django_template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )
        elif callable(template_engine):
            return template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )
        else:
            template_engine = importutils.import_from_string(template_engine)
            return template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )


set_llmhelper_default_config(
    "template_engine",
    get_template_prompt_by_django_template_engine,
)
