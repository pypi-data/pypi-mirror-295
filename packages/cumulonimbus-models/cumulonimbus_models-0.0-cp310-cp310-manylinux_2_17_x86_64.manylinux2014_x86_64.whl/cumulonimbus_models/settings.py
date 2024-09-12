import os
from typing import Final, Optional


class MySettings:
    env_prefix: Final[str] = 'CUMULONIMBUS_MODELS_'

    @property
    def base_url(self) -> Optional[str]:
        for key in os.environ:
            if key.startswith(self.env_prefix) or key.startswith(self.env_prefix.lower()):
                if key[len(self.env_prefix):] == 'BASE_URL' or key[len(self.env_prefix):] == 'base_url':
                    return os.environ[key]
        return None


