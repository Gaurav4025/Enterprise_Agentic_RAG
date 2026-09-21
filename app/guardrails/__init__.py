# Re-export the public API so callers can do:
#   from app.guardrails import initialize_rails, guard
from app.guardrails.rails import initialize_rails, guard

__all__ = ["initialize_rails", "guard"]
