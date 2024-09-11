import re
from typing import cast, ClassVar, Final, Optional, Pattern, Set
from cumulonimbus_models.base import Base
from cumulonimbus_models.settings import MySettings


arg_regex: Final[str] = '{[a-z][a-z_]*[a-z]}'
arg_pattern: Final[Pattern[str]] = re.compile(arg_regex)


class APIRequest(Base):
    route_format: ClassVar[str] = '/'

    @classmethod
    def format_args(cls) -> Set[str]:
        arg_matches = cast(list[str], arg_pattern.findall(cls.route_format))
        return {arg[1:-1] for arg in arg_matches}

    @classmethod
    def route(cls) -> str:
        processed_route = cls.route_format
        for arg in cls.format_args():
            processed_route = processed_route.replace(f'{{{arg}}}', f'<{arg}>')
        return processed_route


    @classmethod
    def get_url(cls, url_data: Optional[dict[str, str]] = None) -> str:
        if url_data is None:
            url_data = {}
        format_args = cls.format_args()
        for arg, val in url_data.items():
            if arg not in format_args:
                raise ValueError(f'Invalid argument: {arg}')
        found_args: Set[str] = set(url_data.keys())
        missing_args = format_args - found_args
        if missing_args:
            raise ValueError(f'Missing arguments: {missing_args}')
        return f'{MySettings().base_url}{cls.route_format.format(**url_data)}'

