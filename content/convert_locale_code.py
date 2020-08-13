def convert_locale_code(locale): 
    if locale == 'zh_CN':
        return 'zh-hans'
    elif locale == 'zh_TW':
        return 'zh-hant'
    else: 
        return locale
    