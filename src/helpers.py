import datetime


def print_break(text):
    """Helper function to print clean sections to console"""
    print("")
    print("#" * 64)
    print("# " + text)
    print("#" * 64)


def get_project_global_variables():
    """
    Returns a list of 'global variables' that are referenced in multiple
    different places. Purpose is to reduce the risk of typing in the wrong
    thing.
    """
    out = {
        "twitter_handles": ["JustinTrudeau", "AndrewScheer",
                            "ElizabethMay", "theJagmeetSingh", 
                            "MaximeBernier"],
        "start_date": datetime.date(2020, 3, 20),  # elct started on 2019-09-11
        "df_path_raw": "data/twitter-data-raw.csv",
        "df_path_clean": "data/twitter-data-clean.csv",
        "df_path_word_count": "data/word-count.csv",
        "df_path_phrase_count": "data/phrase-count.csv"
    }
    return out
