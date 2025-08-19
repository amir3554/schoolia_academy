from django.template import library

register = library.Library()

@register.filter('currency')
def currency(value):
    try:
        # Convert to float first if it's a string
        numeric_value = float(value) if isinstance(value, str) else value
        return f"{numeric_value:.2f}"
    except (ValueError, TypeError):
        return value