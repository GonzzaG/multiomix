class FSExperimentFailed(Exception):
    """Raised when the experiment has failed for some reason"""
    pass


class NoSamplesInCommon(Exception):
    """Raised when the experiment has no samples in common between its bots sources"""
    pass


class FSExperimentStopped(Exception):
    """Raised when user stops the experiment"""
    pass
