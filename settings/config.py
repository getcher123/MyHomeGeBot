class CONF:
    IGNORE_LOCAL_START_HEROKU_CONF = True
    IS_DEBUG = True
    # USE_OLD_STYLED_MSG_FMT = True  # ..
    USE_OLD_STYLED_MSG_FMT = False  # ..
    USE_OLD_STYLED_MSG_FMT_WHEN_NEW_FAILED = True  # ..
    LAPTOP_LOCALHOST_NAME = "users-MacBook-Pro.local"
    RAISE_IF_ENV_VAR_NOT_SET = True
    EXIT_IF_ENV_VAR_NOT_SET = True
    INIT_TelegramBot = True
    AUTO_CORRECT = True  # for: send_photo(... auto_correct=CONF.AUTO_CORRECT,
    # USE_SEND_PHOTO_WRAPPER = True
    USE_SEND_PHOTO_WRAPPER = False
    ALWAYS_RUN_DOCTESTS = True
    _log_call_with_call_stack = True
