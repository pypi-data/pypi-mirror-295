"""
Tags for rendering dash apps
"""


from django import template


register = template.Library()


@register.inclusion_tag("dpwagtail/tags/dpw_instance.html", takes_context=True)
def dpd_instance(context, dash_instance):
    request = context.get('request')
    app_args = dash_instance.resolve_instance(request)
    name, ivalue = app_args

    if name == 'da':
        is_dash_app = True
    if name == 'name':
        is_stateless_app = True

    return locals()


@register.inclusion_tag("dpwagtail/tags/dpd_page_short_listing.html", takes_context=True)
def dpd_page_short_listing(context, dpd_page):

    return locals()


@register.inclusion_tag("dpwagtail/tags/dpd_blog_page_short_listing.html", takes_context=True)
def dpd_blog_page_short_listing(context, dpd_page):

    return locals()


@register.inclusion_tag("dpwagtail/tags/dpd_blog_body.html", takes_context=True)
def dpd_blog_body(context, dpd_page_body):

    return locals()


@register.inclusion_tag("dpwagtail/tags/dpd_blog_block.html", takes_context=True)
def dpd_blog_block(context, block):

    btype = block.block_type
    if btype == 'heading':
        insert_header = True

    if btype == 'paragraph':
        insert_para = True

    if btype == 'dash_instance':
        insert_da = True

    return locals()

