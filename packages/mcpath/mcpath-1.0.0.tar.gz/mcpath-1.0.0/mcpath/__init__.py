import sys
import os

__version__ = "1.0.0"


class MCPath:
    @property
    def root(self) -> str:
        raise NotImplementedError()

    @property
    def worlds(self) -> str:
        return None

    @property
    def resource_packs(self) -> str:
        return None

    @property
    def behavior_packs(self) -> str:
        return None

    @property
    def development_resource_packs(self) -> str:
        return None

    @property
    def development_behavior_packs(self) -> str:
        return None

    @property
    def screenshots(self) -> str:
        return None


class JEPath(MCPath):
    edition = "java"

    @property
    def worlds(self) -> str:
        return os.path.join(self.root, "saves")

    @property
    def resource_packs(self) -> str:
        return os.path.join(self.root, "resourcepacks")

    @property
    def screenshots(self) -> str:
        return os.path.join(self.root, "screenshots")


class BEPath(MCPath):
    edition = "bedrock"

    @property
    def worlds(self) -> str:
        return os.path.join(self.root, "minecraftWorlds")

    @property
    def resource_packs(self) -> str:
        return os.path.join(self.root, "resource_packs")

    @property
    def behavior_packs(self) -> str:
        return os.path.join(self.root, "behavior_packs")

    @property
    def development_resource_packs(self) -> str:
        return os.path.join(self.root, "development_resource_packs")

    @property
    def development_behavior_packs(self) -> str:
        return os.path.join(self.root, "development_behavior_packs")

    @property
    def screenshots(self) -> str:
        return os.path.join(self.root, "Screenshots")


class PREPath(BEPath):
    edition = "preview"


class EDUPath(BEPath):
    edition = "education"


if sys.platform == "win32":
    from ._windows import *
elif sys.platform == "darwin":
    from ._darwin import *
elif sys.platform == "ios" or sys.platform == "iPadOS":
    from ._ios import *
elif hasattr(sys, "getandroidapilevel"):
    from ._android import *
elif sys.platform == "linux":
    from ._linux import *
else:
    from ._dummy import *
