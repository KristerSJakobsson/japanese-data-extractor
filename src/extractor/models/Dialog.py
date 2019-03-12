
class Dialog:
    """
    This object represents a dialog with replies.
    """

    def __init__(self, id: int, tags: List[str], replies: List[str]) -> None:
        self.id = id
        self.tags = tags
        self.replies = replies
