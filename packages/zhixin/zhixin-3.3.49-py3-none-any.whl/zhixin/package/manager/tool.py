from zhixin.package.manager.base import BasePackageManager
from zhixin.package.meta import PackageType
from zhixin.project.config import ProjectConfig


class ToolPackageManager(BasePackageManager):  # pylint: disable=too-many-ancestors
    def __init__(self, package_dir=None):
        super().__init__(
            PackageType.TOOL,
            package_dir
            or ProjectConfig.get_instance().get("zhixin", "packages_dir"),
        )

    @property
    def manifest_names(self):
        return PackageType.get_manifest_map()[PackageType.TOOL]
