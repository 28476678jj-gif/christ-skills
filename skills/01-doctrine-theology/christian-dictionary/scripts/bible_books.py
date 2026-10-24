#!/usr/bin/env python3
"""六十六卷书卷映射：全库单一权威数据。

CITATION_STANDARD.md 的对照表由本数据生成；verse_check.py、lint_skill.py
及技能内检索脚本统一从此导入，避免多处维护导致漂移。

每条记录：
    num     正典序号 1-66（与 biblemate SQLite 的 Book 字段一致）
    zh      中文全名（和合本通行名）
    abbr    中文规范简称
    en      英文全名
    usfx    USFX/OSIS 代码
    aliases 解析引用时接受的别名（小写匹配；含繁体常见写法与英文缩写）
"""

BOOKS = [
    {"num": 1, "zh": "创世记", "abbr": "创", "en": "Genesis", "usfx": "GEN",
     "aliases": ["创世纪", "創世記", "genesis", "gen", "ge"]},
    {"num": 2, "zh": "出埃及记", "abbr": "出", "en": "Exodus", "usfx": "EXO",
     "aliases": ["出埃及", "exodus", "exod", "ex"]},
    {"num": 3, "zh": "利未记", "abbr": "利", "en": "Leviticus", "usfx": "LEV",
     "aliases": ["leviticus", "lev", "lv"]},
    {"num": 4, "zh": "民数记", "abbr": "民", "en": "Numbers", "usfx": "NUM",
     "aliases": ["numbers", "num", "nu"]},
    {"num": 5, "zh": "申命记", "abbr": "申", "en": "Deuteronomy", "usfx": "DEU",
     "aliases": ["deuteronomy", "deut", "dt"]},
    {"num": 6, "zh": "约书亚记", "abbr": "书", "en": "Joshua", "usfx": "JOS",
     "aliases": ["約書亞記", "joshua", "josh", "jos"]},
    {"num": 7, "zh": "士师记", "abbr": "士", "en": "Judges", "usfx": "JDG",
     "aliases": ["士師記", "judges", "judg", "jdg"]},
    {"num": 8, "zh": "路得记", "abbr": "得", "en": "Ruth", "usfx": "RUT",
     "aliases": ["路得", "ruth", "ru"]},
    {"num": 9, "zh": "撒母耳记上", "abbr": "撒上", "en": "1 Samuel", "usfx": "1SA",
     "aliases": ["撒母耳記上", "1 samuel", "1 sam", "1 sa", "1samuel"]},
    {"num": 10, "zh": "撒母耳记下", "abbr": "撒下", "en": "2 Samuel", "usfx": "2SA",
     "aliases": ["撒母耳記下", "2 samuel", "2 sam", "2 sa", "2samuel"]},
    {"num": 11, "zh": "列王纪上", "abbr": "王上", "en": "1 Kings", "usfx": "1KI",
     "aliases": ["列王紀上", "1 kings", "1 kgs", "1 ki", "1kings"]},
    {"num": 12, "zh": "列王纪下", "abbr": "王下", "en": "2 Kings", "usfx": "2KI",
     "aliases": ["列王紀下", "2 kings", "2 kgs", "2 ki", "2kings"]},
    {"num": 13, "zh": "历代志上", "abbr": "代上", "en": "1 Chronicles", "usfx": "1CH",
     "aliases": ["歷代志上", "1 chronicles", "1 chr", "1 ch", "1chronicles"]},
    {"num": 14, "zh": "历代志下", "abbr": "代下", "en": "2 Chronicles", "usfx": "2CH",
     "aliases": ["歷代志下", "2 chronicles", "2 chr", "2 ch", "2chronicles"]},
    {"num": 15, "zh": "以斯拉记", "abbr": "拉", "en": "Ezra", "usfx": "EZR",
     "aliases": ["以斯拉", "ezra", "ezr"]},
    {"num": 16, "zh": "尼希米记", "abbr": "尼", "en": "Nehemiah", "usfx": "NEH",
     "aliases": ["尼希米", "nehemiah", "neh"]},
    {"num": 17, "zh": "以斯帖记", "abbr": "斯", "en": "Esther", "usfx": "EST",
     "aliases": ["以斯帖", "esther", "esth"]},
    {"num": 18, "zh": "约伯记", "abbr": "伯", "en": "Job", "usfx": "JOB",
     "aliases": ["約伯記", "job", "jb"]},
    {"num": 19, "zh": "诗篇", "abbr": "诗", "en": "Psalms", "usfx": "PSA",
     "aliases": ["詩篇", "psalms", "psalm", "ps", "psa"]},
    {"num": 20, "zh": "箴言", "abbr": "箴", "en": "Proverbs", "usfx": "PRO",
     "aliases": ["proverbs", "prov", "pr"]},
    {"num": 21, "zh": "传道书", "abbr": "传", "en": "Ecclesiastes", "usfx": "ECC",
     "aliases": ["傳道書", "ecclesiastes", "eccles", "ec"]},
    {"num": 22, "zh": "雅歌", "abbr": "歌", "en": "Song of Solomon", "usfx": "SNG",
     "aliases": ["song of solomon", "song of songs", "song", "sng", "canticles"]},
    {"num": 23, "zh": "以赛亚书", "abbr": "赛", "en": "Isaiah", "usfx": "ISA",
     "aliases": ["以賽亞書", "isaiah", "isa", "is"]},
    {"num": 24, "zh": "耶利米书", "abbr": "耶", "en": "Jeremiah", "usfx": "JER",
     "aliases": ["耶利米書", "jeremiah", "jer", "je"]},
    {"num": 25, "zh": "耶利米哀歌", "abbr": "哀", "en": "Lamentations", "usfx": "LAM",
     "aliases": ["lamentations", "lam"]},
    {"num": 26, "zh": "以西结书", "abbr": "结", "en": "Ezekiel", "usfx": "EZK",
     "aliases": ["以西結書", "ezekiel", "ezek", "eze"]},
    {"num": 27, "zh": "但以理书", "abbr": "但", "en": "Daniel", "usfx": "DAN",
     "aliases": ["daniel", "dan", "da"]},
    {"num": 28, "zh": "何西阿书", "abbr": "何", "en": "Hosea", "usfx": "HOS",
     "aliases": ["何西阿書", "hosea", "hos"]},
    {"num": 29, "zh": "约珥书", "abbr": "珥", "en": "Joel", "usfx": "JOL",
     "aliases": ["約珥書", "joel", "jl"]},
    {"num": 30, "zh": "阿摩司书", "abbr": "摩", "en": "Amos", "usfx": "AMO",
     "aliases": ["amos", "am"]},
    {"num": 31, "zh": "俄巴底亚书", "abbr": "俄", "en": "Obadiah", "usfx": "OBA",
     "aliases": ["俄巴底亞書", "obadiah", "obad", "ob"]},
    {"num": 32, "zh": "约拿书", "abbr": "拿", "en": "Jonah", "usfx": "JON",
     "aliases": ["約拿書", "jonah", "jon"]},
    {"num": 33, "zh": "弥迦书", "abbr": "弥", "en": "Micah", "usfx": "MIC",
     "aliases": ["彌迦書", "micah", "mic"]},
    {"num": 34, "zh": "那鸿书", "abbr": "鸿", "en": "Nahum", "usfx": "NAM",
     "aliases": ["那鴻書", "nahum", "nah"]},
    {"num": 35, "zh": "哈巴谷书", "abbr": "哈", "en": "Habakkuk", "usfx": "HAB",
     "aliases": ["哈巴谷書", "habakkuk", "hab", "hb"]},
    {"num": 36, "zh": "西番雅书", "abbr": "番", "en": "Zephaniah", "usfx": "ZEP",
     "aliases": ["zephaniah", "zeph", "zep"]},
    {"num": 37, "zh": "哈该书", "abbr": "该", "en": "Haggai", "usfx": "HAG",
     "aliases": ["哈該書", "haggai", "hag", "hg"]},
    {"num": 38, "zh": "撒迦利亚书", "abbr": "亚", "en": "Zechariah", "usfx": "ZEC",
     "aliases": ["撒迦利亞書", "zechariah", "zech", "zec"]},
    {"num": 39, "zh": "玛拉基书", "abbr": "玛", "en": "Malachi", "usfx": "MAL",
     "aliases": ["瑪拉基書", "malachi", "mal"]},
    {"num": 40, "zh": "马太福音", "abbr": "太", "en": "Matthew", "usfx": "MAT",
     "aliases": ["馬太福音", "matthew", "matt", "mt"]},
    {"num": 41, "zh": "马可福音", "abbr": "可", "en": "Mark", "usfx": "MRK",
     "aliases": ["馬可福音", "mark", "mrk", "mk"]},
    {"num": 42, "zh": "路加福音", "abbr": "路", "en": "Luke", "usfx": "LUK",
     "aliases": ["luke", "luk", "lk"]},
    {"num": 43, "zh": "约翰福音", "abbr": "约", "en": "John", "usfx": "JHN",
     "aliases": ["約翰福音", "john", "jhn", "jn"]},
    {"num": 44, "zh": "使徒行传", "abbr": "徒", "en": "Acts", "usfx": "ACT",
     "aliases": ["acts", "act"]},
    {"num": 45, "zh": "罗马书", "abbr": "罗", "en": "Romans", "usfx": "ROM",
     "aliases": ["羅馬書", "romans", "rom", "ro"]},
    {"num": 46, "zh": "哥林多前书", "abbr": "林前", "en": "1 Corinthians", "usfx": "1CO",
     "aliases": ["哥前", "1 corinthians", "1 cor", "1 co", "1corinthians"]},
    {"num": 47, "zh": "哥林多后书", "abbr": "林后", "en": "2 Corinthians", "usfx": "2CO",
     "aliases": ["哥後", "哥后", "2 corinthians", "2 cor", "2 co", "2corinthians"]},
    {"num": 48, "zh": "加拉太书", "abbr": "加", "en": "Galatians", "usfx": "GAL",
     "aliases": ["加拉太書", "galatians", "gal"]},
    {"num": 49, "zh": "以弗所书", "abbr": "弗", "en": "Ephesians", "usfx": "EPH",
     "aliases": ["以弗所書", "ephesians", "eph"]},
    {"num": 50, "zh": "腓立比书", "abbr": "腓", "en": "Philippians", "usfx": "PHP",
     "aliases": ["philippians", "phil", "php"]},
    {"num": 51, "zh": "歌罗西书", "abbr": "西", "en": "Colossians", "usfx": "COL",
     "aliases": ["歌羅西書", "colossians", "col"]},
    {"num": 52, "zh": "帖撒罗尼迦前书", "abbr": "帖前", "en": "1 Thessalonians", "usfx": "1TH",
     "aliases": ["帖撒羅尼迦前書", "1 thessalonians", "1 thess", "1 th", "1thessalonians"]},
    {"num": 53, "zh": "帖撒罗尼迦后书", "abbr": "帖后", "en": "2 Thessalonians", "usfx": "2TH",
     "aliases": ["帖撒羅尼迦後書", "帖撒罗尼迦後书", "2 thessalonians", "2 thess", "2 th", "2thessalonians"]},
    {"num": 54, "zh": "提摩太前书", "abbr": "提前", "en": "1 Timothy", "usfx": "1TI",
     "aliases": ["1 timothy", "1 tim", "1 ti", "1timothy"]},
    {"num": 55, "zh": "提摩太后书", "abbr": "提后", "en": "2 Timothy", "usfx": "2TI",
     "aliases": ["提摩太後書", "2 timothy", "2 tim", "2 ti", "2timothy"]},
    {"num": 56, "zh": "提多书", "abbr": "多", "en": "Titus", "usfx": "TIT",
     "aliases": ["提多書", "titus", "tit"]},
    {"num": 57, "zh": "腓利门书", "abbr": "门", "en": "Philemon", "usfx": "PHM",
     "aliases": ["腓利門書", "philemon", "philem", "phm"]},
    {"num": 58, "zh": "希伯来书", "abbr": "来", "en": "Hebrews", "usfx": "HEB",
     "aliases": ["希伯來書", "hebrews", "heb"]},
    {"num": 59, "zh": "雅各书", "abbr": "雅", "en": "James", "usfx": "JAS",
     "aliases": ["雅各書", "james", "jas"]},
    {"num": 60, "zh": "彼得前书", "abbr": "彼前", "en": "1 Peter", "usfx": "1PE",
     "aliases": ["1 peter", "1 pet", "1 pe", "1peter"]},
    {"num": 61, "zh": "彼得后书", "abbr": "彼后", "en": "2 Peter", "usfx": "2PE",
     "aliases": ["彼得後書", "2 peter", "2 pet", "2 pe", "2peter"]},
    {"num": 62, "zh": "约翰一书", "abbr": "约一", "en": "1 John", "usfx": "1JN",
     "aliases": ["約翰一書", "约翰壹书", "約翰壹書", "1 john", "1 jn", "1john"]},
    {"num": 63, "zh": "约翰二书", "abbr": "约二", "en": "2 John", "usfx": "2JN",
     "aliases": ["約翰二書", "约翰贰书", "約翰貳書", "2 john", "2 jn", "2john"]},
    {"num": 64, "zh": "约翰三书", "abbr": "约三", "en": "3 John", "usfx": "3JN",
     "aliases": ["約翰三書", "约翰叁书", "約翰叁書", "3 john", "3 jn", "3john"]},
    {"num": 65, "zh": "犹大书", "abbr": "犹", "en": "Jude", "usfx": "JUD",
     "aliases": ["猶大書", "jude", "jud"]},
    {"num": 66, "zh": "启示录", "abbr": "启", "en": "Revelation", "usfx": "REV",
     "aliases": ["啟示錄", "revelation", "rev"]},
]

# 名称（全名/简称/别名，统一小写） -> 正典序号
NAME_TO_NUM = {}
for _b in BOOKS:
    NAME_TO_NUM[_b["zh"].lower()] = _b["num"]
    NAME_TO_NUM[_b["abbr"].lower()] = _b["num"]
    NAME_TO_NUM[_b["en"].lower()] = _b["num"]
    NAME_TO_NUM[_b["usfx"].lower()] = _b["num"]
    for _a in _b["aliases"]:
        NAME_TO_NUM[_a.lower()] = _b["num"]

NUM_TO_BOOK = {_b["num"]: _b for _b in BOOKS}


def book_num(name):
    """按全名/简称/别名解析书卷序号，未命中返回 None。"""
    if not name:
        return None
    key = str(name).strip().lower().replace(".", "")
    key = " ".join(key.split())
    return NAME_TO_NUM.get(key)
