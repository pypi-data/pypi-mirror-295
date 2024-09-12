from dataclasses import dataclass, field


@dataclass
class Session:
    id: str
    name: str
    clients: int
    windows: list["Window"] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"<session {self.name}>"

    def __str__(self) -> str:
        super().__repr__()
        return self.__repr__()


@dataclass
class Window:
    id: str
    is_active: bool
    name: str
    session: "Session"
    panes: list["Pane"] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"<window {self.name}>"

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Pane:
    id: str
    is_active: bool
    title: str
    pid: int
    window: "Window"

    def __repr__(self) -> str:
        return f"<pane {self.id}>"

    def __str__(self) -> str:
        return self.__repr__()
