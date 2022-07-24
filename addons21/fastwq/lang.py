# -*- coding:utf-8 -*-
#
# Copyright (C) 2018 sthoo <sth201807@gmail.com>
#
# Support: Report an issue at https://github.com/sth2018/FastWordQuery/issues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version; http://www.gnu.org/copyleft/gpl.html.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from anki.lang import currentLang

try:
    basestring
except NameError:
    basestring = str

__all__ = ["_", "_cl", "_sl"]

# Language Define, [Key, zh_CN, en]
_arr = [
    ["CHECK_FILENAME_LABEL", "使用文件名作为标签", "Use the Filename as Label"],
    ["EXPORT_MEDIA", "导出媒体文件", "Export Media Files"],
    ["DICTS_FOLDERS", "字典文件夹", "Dictionary Folder"],
    ["CHOOSE_NOTE_TYPES", "选择笔记类型", "Choose Note Type"],
    ["CURRENT_NOTE_TYPE", "当前类型", "Current type"],
    ["MDX_SERVER", "MDX服务器", "MDX server"],
    ["USE_DICTIONARY", "使用字典", "Use dict"],
    ["UPDATED", "更新", "Updated"],
    ["CARDS", "卡片", "Cards"],
    ["FAILURE", "失败", "Failure"],
    ["SUCCESS", "成功", "Success"],
    ["QUERIED", "查询", "Queried"],
    ["FIELDS", "字段", "Fields"],
    ["WORDS", "单词", "Words"],
    ["NOT_DICT_FIELD", "忽略", "Ignore"],  # 不是字典字段
    ["NOTE_TYPE_FIELDS", "<b>笔记字段</b>", "<b>Note Fields</b>"],
    ["DICTS", "<b>字典</b>", "<b>Dictionary</b>"],
    ["DICT_FIELDS", "<b>字典字段</b>", "<b>Fields</b>"],
    [
        "RADIOS_DESC",
        "<b>单选框选中为待查询单词字段</b>",
        "<b> Select the field to be queried with single selection.</b>",
    ],
    ["NO_QUERY_WORD", "查询字段无单词", "The query field is empty"],
    [
        "CSS_NOT_FOUND",
        "没有找到CSS文件，请手动选择",
        "No CSS file found, please select one manually.",
    ],
    ["ABOUT", "关于", "About"],
    ["REPOSITORY", "项目地址", "Project Repo"],
    ["FEEDBACK", "反馈", "Feedback"],
    ["VERSION", "版本", "Current Version"],
    ["LATEST_VERSION", "已经是最新版本.", "You are using the lastest version."],
    ["ABNORMAL_VERSION", "当前版本异常.", "The current version is abnormal."],
    ["CHECK_FAILURE", "版本检查失败.", "Version check failed."],
    ["NEW_VERSION", "检查到新版本:", "New version available:"],
    ["UPDATE", "更新", "Update"],
    ["AUTO_UPDATE", "自动检测新版本", "Auto check new version"],
    ["CHECK_UPDATE", "检测更新", "Check Update"],
    ["IGNORE_MDX_WORDCASE", "忽略本地词典单词大小写", "Ignore MDX dictionary word case"],
    ["FORCE_UPDATE", "强制更新字段", "Forced Updates of all fields"],
    ["IGNORE_ACCENTS", "忽略声调", "Ignore Accents"],
    ["SKIP_VALUED", "跳过有值项", "Skip non-empty"],
    ["SKIPED", "略过", "Skipped"],
    ["SETTINGS", "参数", "Settings"],
    ["THREAD_NUMBER", "线程数", "Number of Threads"],
    ["INITLIZING_DICT", "初始化词典...", "Initlizing Dictionary..."],
    ["PLS_SET_DICTIONARY_FIELDS", "请设置字典和字段", "Please set the dictionary and fields."],
    ["CONFIG_INDEX", "配置 %s", "Config %s"],
    ["SELECT_ALL", "全选", "All"],
    ["DICTS_NAME", "字典名称", "Dictionary Name"],
    ["EDIT", "编辑", "Edit"],
    ["QUERY", "查询", "Query"],
    ["QUERY_SELECTED", "查询选中项", "Query Selected"],
    ["ALL_FIELDS", "所有字段", "All Fields"],
    ["CURRENT_FIELDS", "当前字段", "Current Fields"],
    ["OPTIONS", "选项", "Options"],
    ["CLOZE_WORD", "单词填空", "Cloze word"],
    ["CLOZE_WORD_FORMAT", "单词填空格式", "Cloze word formater"],
    ["SOUND_FORMAT", "发音格式化", "Sound formater"],
    ["BRE_PRON", "英式发音", "British Pronunciation"],
    ["AME_PRON", "美式发音", "American Pronunciation"],
    ["PRON", "发音", "Audio Pronunciation"],
    ["EXAMPLE", "例句", "Examples"],
    ["TRANS", "翻译", "Translation"],
    ["DEF", "释义", "Definition"],
    ["PHON", "音标", "Phonetic Symbols"],
    ["BRE_PHON", "英式音标", "Phonetic Symbols (UK)"],
    ["BRE_PHON_NO_PREFIX", "英式音标无前缀", "Phonetic Symbols (UK) no prefix"],
    ["AME_PHON", "美式音标", "Phonetic Symbols (US)"],
    ["AME_PHON_NO_PREFIX", "美式音标无前缀", "Phonetic Symbols (US) no prefix"],
    ["IMAGE", "图片", "Images"],
]

_trans = {item[0]: {"zh_CN": item[1], "en": item[2]} for item in _arr}


def _(key, lang=currentLang):
    """get local language string"""
    if lang != "zh_CN" and lang != "en":
        lang = "en"

    def disp(s):
        return s.lower().capitalize()

    if key not in _trans or lang not in _trans[key]:
        return disp(key)
    return _trans[key][lang]


def _cl(labels, lang=currentLang):
    """get local language string from labels"""
    if isinstance(labels, basestring):
        return _(labels)
    if lang != "zh_CN" and lang != "en":
        lang = "en"
    return labels[0] if lang == "zh_CN" else labels[1]


def _sl(key):
    return _trans[key].values()
