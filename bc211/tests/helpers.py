from django.contrib.gis.geos import Point


class DefaultDictionary:
    test_dictionary = {
        'New Westminster':  Point(-122.910956, 49.205718),
        'Coquitlam':        Point(-122.793206, 49.283763),
        'Vancouver':        Point(-123.120738, 49.282729),
        'Delta':            Point(-123.026476, 49.095216),
    }
