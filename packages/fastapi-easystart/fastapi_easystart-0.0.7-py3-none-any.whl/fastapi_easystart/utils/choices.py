from enum import Enum


class CustomRobotTagsEnum(str, Enum):
    DEFAULT = "default"
    ALL = "all"
    NOINDEX = "noindex"
    NOFOLLOW = "nofollow"
    NONE = "none"
    NOARCHIVE = "noarchive"
    NOSNIPPET = "nosnippet"
    NOODP = "noodp"
    NOTRANSLATE = "notranslate"
    NOIMAGEINDEX = "noimageindex"
    UNAVAILABLE_AFTER = "unavailable_after"


class CustomRobotTagsChoices:
    choices = {
        'default': [CustomRobotTagsEnum.DEFAULT.value],
        'all': [
            CustomRobotTagsEnum.ALL.value,
            CustomRobotTagsEnum.NOINDEX.value,
            CustomRobotTagsEnum.NOFOLLOW.value,
            CustomRobotTagsEnum.NONE.value,
            CustomRobotTagsEnum.NOARCHIVE.value,
            CustomRobotTagsEnum.NOSNIPPET.value,
            CustomRobotTagsEnum.NOODP.value,
            CustomRobotTagsEnum.NOTRANSLATE.value,
            CustomRobotTagsEnum.NOIMAGEINDEX.value,
            CustomRobotTagsEnum.UNAVAILABLE_AFTER.value,
        ]
    }
