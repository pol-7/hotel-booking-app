from uuid import UUID


class ResourceNotFoundError(Exception):
    def __init__(self, resource_type: str, resource_id: UUID):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type}:{resource_id} not found.")


class NotOwnedError(Exception):
    def __init__(self, resource_type: str, user_id: UUID):
        self.resource_type = resource_type
        self.user_id = user_id
        super().__init__(
            f"resource of type {resource_type} is not owned by user:{user_id}."
        )
