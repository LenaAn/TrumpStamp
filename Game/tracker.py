import urllib
from copy import deepcopy
from plyer import uniqueid

GA_URL = "http://www.google-analytics.com/collect"
TRACKER_ID = "UA-73301637-3"


class Tracker(object):
    def __init__(self, tracker_id, client_id, asynchronous=True):
        self.tracker_id = tracker_id
        self.client_id = client_id
        self.asynchronous = asynchronous

    def send(self, dic):
        copy_dic = deepcopy(dic)
        copy_dic.update({"tid": self.tracker_id, "cid": self.client_id, "v": "1"})
        data = urllib.urlencode(copy_dic)
        print(data)
        if self.asynchronous:
            from kivy.network.urlrequest import UrlRequest
            req = UrlRequest(GA_URL, req_body=data)
        else:
            import urllib2
            urllib2.urlopen(GA_URL, data=data).read()


tracker = Tracker(TRACKER_ID, uniqueid.id)


class BuilderMeta(type):
    def __init__(self, *args):
        class_name, bases, attributes = args
        super(BuilderMeta, self).__init__(*args)
        if "defaults" not in attributes:
            self.defaults = {}
        if not hasattr(self, 'mandatory_keys'):
            self.mandatory_keys = []


class HitBuilder(object):
    __metaclass__ = BuilderMeta
    mandatory_keys = ["t"]

    def __init__(self):
        self.params = deepcopy(type(self).defaults)

    @classmethod
    def set_defaults(cls, **kwargs):
        cls.defaults.update(kwargs)

    def set(self, **kwargs):
        self.params.update(kwargs)
        return self

    def check_mandatory_keys(self, current_type=None):
        if current_type is not None:
            if hasattr(current_type, "mandatory_keys"):
                for key in current_type.mandatory_keys:
                    if key not in self.params:
                        raise ValueError("Key {} was not set".format(key))
            for base_type in current_type.__bases__:
                self.check_mandatory_keys(base_type)
            return
        self.check_mandatory_keys(type(self))

    def build(self):
        self.check_mandatory_keys()
        return self.params


class ScreenViewBuilder(HitBuilder):
    defaults = {"aiid": "com.android.vending"}
    mandatory_keys = ["cd", "an", "aid", "av", "aiid"]

    def __init__(self):
        super(ScreenViewBuilder, self).__init__()
        self.params.update({"t": "screenview"})


class EventBuilder(HitBuilder):
    mandatory_keys = ["ea", "ec"]

    def __init__(self):
        super(EventBuilder, self).__init__()
        self.params.update({"t": "event"})
