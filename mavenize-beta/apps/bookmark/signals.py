from django.dispatch import Signal

state_changed = Signal(providing_args=["is_done"])
