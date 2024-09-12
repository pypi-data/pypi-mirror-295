# import logging

from django import template
from django.conf import settings as user_settings

from sorl.thumbnail import get_thumbnail, delete

from django_easy_instagram import settings
from django_easy_instagram.scraper import get_posts

register = template.Library()


class InstagramUserRecentMediaNode(template.Node):

    def __init__(self, var_name):
        self.var_name = var_name
        self.username = template.Variable(var_name)

    def render(self, context):

        try:
            context['recent_media'] = get_posts(self.username.resolve(context))
        except template.base.VariableDoesNotExist:
            logger.warning(
                " variable name \"{}\" not found in context!"
                " Using a raw string as input is DEPRECATED."
                " Please use a template variable instead!".format(self.var_name)
            )

            context['recent_media'] = get_posts(username=self.var_name)

        return ''


@register.tag
def instagram_user_recent_media(parser, token):
    try:
        tagname, username = token.split_contents()

        return InstagramUserRecentMediaNode(username)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )


@register.filter(name='local_cache')
def local_cache(value, size="600x600"):
    im = get_thumbnail(value, size, crop='center', quality=settings.INSTAGRAM_CACHE_QUALITY)
    return im.url
