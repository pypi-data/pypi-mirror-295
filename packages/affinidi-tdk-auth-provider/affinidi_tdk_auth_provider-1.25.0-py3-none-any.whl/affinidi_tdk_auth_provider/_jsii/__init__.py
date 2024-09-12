from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

__jsii_assembly__ = jsii.JSIIAssembly.load(
    "@affinidi-tdk/auth-provider",
    "1.25.0",
    __name__[0:-6],
    "auth-provider@1.25.0.jsii.tgz",
)

__all__ = [
    "__jsii_assembly__",
]

publication.publish()
