from os.path import join as pjoin
from typing import Optional, Union

class EmailCredential:
    __slots__ = ['username', 'password']

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f"EmailCredential(username={self.username}, password=***hidden***)"

class LogConfig:
    __slots__ = ['_root_log_path', '_cache_log_path', '_email_credential']

    def __init__(self, root_log_path: str = 'logs', cache_log_path: Optional[str] = None, email_credential: Optional[Union[EmailCredential, dict]] = None) -> None:
        self._root_log_path = root_log_path
        self._cache_log_path = cache_log_path if cache_log_path is not None else pjoin(root_log_path, "cache")
        self._email_credential = self._convert_to_email_credential(email_credential)
        
    @property
    def root_log_path(self) -> str:
        return self._root_log_path
    
    @property
    def cache_log_path(self) -> str:
        return self._cache_log_path

    @property
    def email_credential(self) -> Optional[EmailCredential]:
        return self._email_credential

    @root_log_path.setter
    def root_log_path(self, value: str) -> None:
        self._root_log_path = value
        if self._cache_log_path is None:
            self._cache_log_path = pjoin(value, "cache")
    
    @cache_log_path.setter
    def cache_log_path(self, value: str) -> None:
        self._cache_log_path = value

    @email_credential.setter
    def email_credential(self, value: Optional[Union[EmailCredential, dict]]) -> None:
        self._email_credential = self._convert_to_email_credential(value)

    def _convert_to_email_credential(self, credential: Optional[Union[EmailCredential, dict]]) -> Optional[EmailCredential]:
        if isinstance(credential, dict):
            return EmailCredential(**credential)
        elif isinstance(credential, EmailCredential):
            return credential
        elif credential is None:
            return None
        else:
            raise ValueError("Invalid type for email credential")

    def __repr__(self) -> str:
        return f"LogConfig(root_log_path={self.root_log_path}, cache_log_path={self.cache_log_path}, email_credential={self.email_credential})"