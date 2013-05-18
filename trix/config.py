# Trix configuration / management.

class Configuration:

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def merge(self, object):
        self.__dict__.update(object.__dict__)

    def __repr__(self):
      data = self.__dict__
      information = " ".join(["%s=%r" % (k, data[k]) for k in data])
      return "<trix.config.Configuration %s>" % information

defaults = Configuration(width=11, buffer=1, input_file=None, output_file=None, agent='default')