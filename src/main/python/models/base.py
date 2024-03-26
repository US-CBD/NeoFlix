class Base:
    def __init__(self, repository):
        self.repository = repository

    def save(self):
        self.repository.create_or_update(self)

    def delete(self):
        self.repository.delete(self)

    def to_node(self):
        raise NotImplementedError("This method must be implemented in the child class")

    @staticmethod
    def from_node(self, node):
        raise NotImplementedError("This method must be implemented in the child class")