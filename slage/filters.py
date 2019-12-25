# coding: utf-8

import jinja2


@jinja2.contextfilter
def subrender(context, value):
    # Based on https://stackoverflow.com/a/48213764/1069572
    _template = context.eval_ctx.environment.from_string(value)
    result = _template.render(**context)

    return result
