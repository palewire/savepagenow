class CachedPage(Exception):
    """Raised when archive.org declines to make a new capture and instead returns the cached version of most recent archive."""

    pass


class WaybackRuntimeError(Exception):
    """A generic error returned by the Wayback Machine."""

    pass


class BlockedByRobots(WaybackRuntimeError):
    """Raised when archive.org has been blocked by the site's robots.txt."""

    pass


class BadGateway(WaybackRuntimeError):
    """Raised when you receive a 502 bad gateway status code."""

    pass


class Unauthorized(WaybackRuntimeError):
    """Raised when you receive a 401 unauthorized status code."""

    pass


class Forbidden(WaybackRuntimeError):
    """Raised when you receive a 403 forbidden status code."""

    pass


class TooManyRequests(WaybackRuntimeError):
    """Raised when you have exceeded the throttle on request frequency."""

    pass


class UnknownError(WaybackRuntimeError):
    """Raised when you receive a 520 unknown status code."""

    pass
