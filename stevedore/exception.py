class NoUniqueMatch(RuntimeError):
    """There was more than one extension, or none, that matched the query."""


class NoMatches(NoUniqueMatch):
    """There were no extensions with the driver name found."""


class MultipleMatches(NoUniqueMatch):
    """There were multiple matches for the given name."""
