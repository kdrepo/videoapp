from django import template

register = template.Library()

@register.filter
def time_in_seconds(value):
    """Convert HH:MM:SS to total seconds."""
    try:
        h, m, s = map(int, value.split(':'))
        return h * 3600 + m * 60 + s
    except ValueError:
        return 0  # Return 0 if the format is invalid
