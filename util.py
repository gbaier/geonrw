def deumlautify(string):
    """ removes German umlauts """
    umlaut_dict = str.maketrans({
        u"Ä": "Ae",
        u"Ö": "Oe",
        u"Ü": "Ue",
        u"ä": "ae",
        u"ö": "oe",
        u"ü": "ue",
        u"ß": "ss",
    })
    return string.translate(umlaut_dict)
