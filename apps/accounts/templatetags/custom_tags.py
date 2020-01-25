from __future__ import unicode_literals

from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def optional_app_register(request):
    """
    Include a login snippet if REST Registration App login view is in the URLconf.
    """
    try:
        register_url = reverse('rest_registration:register')
    except NoReverseMatch:
        return ''

    snippet = "<li><a href='{href}?next={next}'>Register</a></li>"
    snippet = format_html(snippet, href=register_url, next=escape(request.path))

    return mark_safe(snippet)


@register.simple_tag
def optional_app_login(request):
    """
    Include a login snippet if REST Registration App login view is in the URLconf.
    """
    try:
        login_url = reverse('rest_registration:login')
    except NoReverseMatch:
        return ''

    snippet = "<li><a href='{href}?next={next}'>Log in</a></li>"
    snippet = format_html(snippet, href=login_url, next=escape(request.path))

    return mark_safe(snippet)


@register.simple_tag
def optional_app_logout(request, user):
    """
    Include a logout snippet if REST Registration App logout view is in the URLconf.
    """
    try:
        logout_url = reverse('rest_registration:logout')
    except NoReverseMatch:
        snippet = format_html('<li class="navbar-text">{user}</li>', user=escape(user))
        return mark_safe(snippet)

    snippet = """<li class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            {user}
            <b class="caret"></b>
        </a>
        <ul class="dropdown-menu">
            <li><a href='{href}?next={next}'>Log out</a></li>
        </ul>
    </li>"""
    snippet = format_html(snippet, user=escape(user), href=logout_url, next=escape(request.path))

    return mark_safe(snippet)
