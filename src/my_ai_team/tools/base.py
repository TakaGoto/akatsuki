"""Tool creation helpers."""

from agents import function_tool

# Re-export the SDK's function_tool decorator as `tool` for convenience.
# Decorate any function with @tool to make it available to agents.
#
# Example:
#   @tool
#   def search_web(query: str) -> str:
#       \"\"\"Search the web for a query.\"\"\"
#       return do_search(query)
#
tool = function_tool
