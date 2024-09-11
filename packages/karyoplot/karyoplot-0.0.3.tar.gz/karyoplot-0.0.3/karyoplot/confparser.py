import configparser
import re


from karyoplot.entities import Sequence, Canvas, Track


# Class Confiparser
class Confparser(configparser.ConfigParser):
    def __init__(self):
        configparser.ConfigParser.__init__(self)

    # Lists all the sections starting with "track_"
    def find_track(self):
        tracks = []
        for section in self.sections():
            if re.search("^track_(\S)+$", section):
                tracks.append(section)
        return tracks

    # Returns a list of track Objects
    def get_tracks(self):
        track_list = []
        for i in self.find_track():
            kwargs = dict(self.items(i))
            t = Track(i,**kwargs)
            track_list.append(t)
        return track_list

    # Returns a canvas Object
    def get_canvas(self):
        kwargs = dict(self.items("canvas"))
        c = Canvas(**kwargs)
        return c

    def get_sequence(self):
        kwargs = dict(self.items("sequence"))
        s = Sequence(**kwargs)
        return s

    # Returns zoom on sequences
    # list of tuples (chr,start,end)
    # start and end could be None
    def get_zooms(self):
        kwargs = dict(self.items("sequence"))
        if 'zoom' in kwargs:
            seqs = kwargs['zoom'].split(",")
            for seq in seqs:
                m = re.match(r"(\w+)(:)*(\d+)*(-)*(\d+)*", seq)
                if m:
                    if m.group(3) and m.group(5):
                        yield (m.group(1), int(m.group(3)), int(m.group(5)))
                    else:
                        yield (m.group(1), None, None)
        else:
            return []

