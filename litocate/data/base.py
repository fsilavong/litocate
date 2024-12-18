from dataclasses import dataclass

@dataclass
class Paper:
    title: str
    abstract: dict
    is_peer_reviewed: bool
    metadata: dict
    