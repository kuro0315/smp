class IComponent():
    def __init__(self) -> None:
        raise NotImplementedError("IComponent is an interface.")
    
    def step(self, dt) -> None:
        raise NotImplementedError()
    