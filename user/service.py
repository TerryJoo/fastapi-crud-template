from crud.crud_service import CRUDService
from user.models import User


class UserService(CRUDService[User]):
    @property
    def entity(self) -> User.__class__:
        return User
