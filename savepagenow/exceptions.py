class CachedPage(Exception):
    """Raised when archive.org declines to make a new capture and instead returns the cached version of most recent archive."""

    pass


class WaybackRuntimeError(Exception):
    """An error returned by the Wayback Machine."""

    pass


class BlockedByRobots(WaybackRuntimeError):
    """Raised when archive.org has been blocked by the site's robots.txt access control instructions."""

    pass


class TooManyRequests(WaybackRuntimeError):
    """Raised when archive.org when you have exceeded its throttle on request frequency. Slow it down."""

    pass
