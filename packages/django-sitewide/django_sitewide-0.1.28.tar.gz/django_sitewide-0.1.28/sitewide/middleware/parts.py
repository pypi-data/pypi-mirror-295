"""Static Variables and Methods for Sitewide Objects"""

from pathlib import Path
from django.conf import settings

_OBJSMAP = {
    "avatar": {
        "elements": {
            "path": {"default": "/static/imgs/avatar.svg"},
            "show": {"default": True},
            "url": {"default": "/"},
        },
        "required": ("all",),
    },
    "banner": {
        "parts": ("division", "image"),
        "elements": {"allow": {"default": ""}, "show": {"default": False}},
        "required": ("image", "show",),
    },
    "division": {
        "elements": {
            "entries": {
                "name": "parts",
                "accept": (
                    "division",
                    "hamburger",
                    "icon",
                    "image",
                    "menu",
                    "ref",
                    "text",
                ),
                "default": [],
            },
            "show": {"default": True},
            "css": {"default": ""},
            "tag": {"default": "division"},
        },
        "required": ("show", "tag"),
    },
    "email": {
        "elements": {
            "show": {"default": True},
            "value": {"default": "user@sitewide.live"},
            "url": {"default": "mailto:user@sitewide.live"},
        },
        "required": ("all",),
    },
    "footer": {
        "elements": {
            "entries": {
                "name": "sections",
                "accept": ("section",),
                "default": [],
            },
            "show": {"default": True},
        },
        "required": ("show",),
    },
    "hamburger": {
        "elements": {
            "show": {"default": True},
            "tag": {"default": "hamburger"},
        },
        "required": ("all",),
    },
    "header": {
        "elements": {
            "entries": {
                "name": "sections",
                "accept": ("section",),
                "default": [],
            },
            "show": {"default": True},
        },
        "required": ("show",),
    },
    "icon": {
        "elements": {
            "tag": {"default": "icon"},
            "hex": {"default": "ea25"},
            "url": {"default": "#"},
        },
        "required": ("all",),
    },
    "image": {
        "elements": {
            "css": {"default": ""},
            "tag": {"default": "image"},
            "path": {"default": "imgs/no_image.png"},
            "url": {"default": "#"},
        },
        "required": ("tag", "path"),
    },
    "item": {
        "parts": ("icon", "menu", "text"),
        "elements": {"indicator": {"default": "left"}, "url": {"default": "#"}},
        "required": ("text", "url"),
    },
    "logo": {
        "elements": {
            "path": {"default": "imgs/sitewide-full-logo.png"},
            "url": {"default": "/"},
        },
        "required": ("path",),
    },
    "menu": {
        "elements": {
            "entries": {"name": "items", "accept": ("item",), "default": []},
            "show": {"default": True},
            "tag": {"default": "menu"},
        },
        "required": ("show", "tag"),
    },
    "ref": {  # Use for User, Logo and Title or any referenced part
        "elements": {
            "show": {"default": True},
            "tag": {"default": ""},
        },
        "required": ("all",),
    },
    "section": {
        "parts": ("division",),
        "elements": {
            "show": {"default": True},
            "css": {"default": ""},
            "tag": {"default": "section"},
        },
        "required": ("show",),
    },
    "sidebar": {
        "parts": ("menu", "ref"),
        "elements": {"allow": {"default": ""}, "show": {"default": True}},
        "required": ("all",),
    },
    "sitewide": {
        "parts": (
            "banner",
            "footer",
            "header",
            "logo",
            "sidebar",
            "titles",
            "user",
        ),
        "elements": {
            "favicon": {"default": "imgs/sitewide-favicon-32x32.png"},
            "url": {"default": "https://pypi.org/project/django-sitewide/"},
            "project": {"default": "sitewide"},
            "niche": {"default": ""},
            "terms": {"default": {}},
        },
        "required": (
            "favicon",
            "logo",
            "niche",
            "project",
            "terms",
            "titles",
            "url",
            "user",
        ),
    },
    "text": {
        "elements": {
            "css": {"default": ""},
            "tag": {"default": "text"},
            "url": {"default": "#"},
            "value": {"default": ""},
        },
        "required": ("tag", "value"),
    },
    "titles": {
        "elements": {
            "page": {"default": "Page Title"},
            "sub": {"default": ""},
        },
        "required": ("all",),
    },
    "user": {
        "parts": ("avatar", "email", "username"),
        "elements": {"url": {"default": "user/profile"}},
        "required": ("all",),
    },
    "username": {
        "elements": {
            "show": {"default": True},
            "url": {"default": "#"},
            "value": {"default": "AnonymousUser"},
        },
        "required": ("all",),
    },
}


def entries(ref):
    """entries(x) -> str
    Get the name of the list of entries in x"""

    return (
        _OBJSMAP.get(ref, {})
        .get("elements", {})
        .get("entries", {})
        .get("name", "illegal")
    )


def iselement(ref, sub):
    """iselement(...) -> Bool
    Confirm that sub is a terminal element of ref"""

    return sub in _OBJSMAP.get(ref, {}).get("elements", {})


def isentry(ref, sub):
    """isentry(...) --> bool
    Confirm that ref accepts sub entries"""

    return sub in _OBJSMAP.get(ref, {}).get("elements", {}).get(
        "entries", {}
    ).get("accept")


def ispart(ref):
    """ispart(x) -> bool
    Confirm the x is a part"""

    return ref in _OBJSMAP


def issubpart(ref, sub):
    """issubpart(...) -> Bool
    Confirm that sub is part of ref"""

    return sub in _OBJSMAP.get(ref, {}).get("parts", {})


def istype(ref, sub, value):
    """istype(...) --> bool
    Check that the value is the right type for sub relative to ref"""

    return type(default(ref, sub)) is type(value)


def rephrase(conf, niche=None, terms=None):
    """rephrase(d) -> dict
    parse a dict and substitute all marked words with versions relevant to
    the specified niche"""

    preserve = {}
    if niche is None and terms is None:
        niche, terms = conf.pop("niche", None), conf.pop("terms", None)
        if niche and terms:
            preserve.update({"niche": niche, "terms": terms})
    parsed = {}
    if hasattr(niche, "endswith") and hasattr(terms, "keys"):
        for key, value in conf.items():
            if hasattr(value, "keys"):
                parsed[key] = rephrase(value, niche=niche, terms=terms)
            elif hasattr(value, "append"):
                parsed[key] = [
                    rephrase(pair, niche=niche, terms=terms) for pair in value
                ]
            elif hasattr(value, "endswith"):
                parsed[key] = substitute(value, terms.get(niche, {}))
            else:
                parsed[key] = value
        parsed.update(preserve)
        return parsed
    conf.update(preserve)
    return conf


def required(ref, all_=False):
    """required(x) -> Tuple
    Return a series of required attributes of x"""

    if all_ is True:
        return list(_OBJSMAP.get(ref).get("parts", ())) + list(
            _OBJSMAP.get(ref).get("elements", {}).keys()
        )
    return _OBJSMAP.get(ref)["required"] if ref in _OBJSMAP else tuple()


def substitute(text, niche_terms):
    """substitute(...) -> str
    replace all marked words in text with equivalent in niche terms"""

    if "`" in text and niche_terms:
        rephrased = ""
        for phrase in text.split("`"):
            reword = niche_terms.get(phrase.lower(), phrase)
            rephrased += reword.title() if phrase.istitle() else reword
        return rephrased
    return text


def default(ref, sub):
    """default(...) -> Value
    Get the default value of sub in ref"""

    if not iselement(ref, sub):
        raise AttributeError(f"{sub} is not an element of {ref}")
    return _OBJSMAP.get(ref)["elements"][sub].get("default")


class Part:
    """A Base Part of Sitewide"""

    def __init__(self, part, **kwargs):
        """Initialize Part"""

        if not ispart(part):
            raise NameError(f"Unrecognized Part -> {part}.")
        self.__part = part
        for attr, values in kwargs.items():
            setattr(self, attr, values)
        self.__defaults__()

    def __defaults__(self):
        """Set default values for missing/omitted mandatory attributes"""

        attribs = (
            required(self.__part, all_=True)
            if "all" in required(self.__part)
            else required(self.__part)
        )
        for attr in attribs:
            if attr == "entries":
                continue  # Values for containers must be provided explicitly
            if not hasattr(self, attr):
                if ispart(attr):
                    super().__setattr__(attr, Part(attr, **{}))
                else:
                    super().__setattr__(attr, default(self.__part, attr))

    def __populate__(self, obj_list):
        """Populate list of series of Part objects"""

        if not isinstance(obj_list, list):
            raise TypeError(f"Expected a List object. Got {type(obj_list)}")
        for obj_dict in obj_list:
            if "part" in obj_dict:
                if not isentry(self.__part, obj_dict.get("part")):
                    raise AttributeError(
                        f"{self.__part.title()} cannot accept "
                        + f"{obj_dict.pop('part')} objects"
                    )
                getattr(self, entries(self.__part)).append(
                    Part(obj_dict.pop("part"), **obj_dict)
                )
            elif entries(self.__part) in ("items", "sections"):
                getattr(self, entries(self.__part)).append(
                    Part(entries(self.__part).rstrip("s"), **obj_dict)
                )
            else:
                raise AttributeError(
                    f"Unspecified or noncompliant part for {self.__part}."
                )

    def __repr__(self):
        """String representation for Developers"""

        return f"<{__name__}.{self.__part.title()} object at {hex(id(self))}>"

    def __setattr__(self, attr, values):
        """Perform validation before setting attributes"""

        if attr == "_Part__part" and ispart(values) and not hasattr(self, attr):
            # Initialization in progress
            super().__setattr__(attr, values)
            if entries(values) != "illegal":
                super().__setattr__(entries(values), [])
        elif attr == "entries":
            self.__populate__(values)
        elif iselement(self.__part, attr):
            if not istype(self.__part, attr, values):
                raise TypeError(
                    f"{attr} of {self.__part} part expects a "
                    + f"{type(default(self.__part, attr))}. Got {type(values)}."
                )
            super().__setattr__(attr, values)
        elif issubpart(self.__part, attr):
            if not isinstance(values, dict):
                raise TypeError(
                    f"Expected a mapping objecr (dict). Got {type(values)}."
                )
            super().__setattr__(attr, Part(attr, **values))
        else:
            raise AttributeError(
                f"Unexpected attribute ({attr}) for {self.__part}"
            )


class Sitewide(Part):
    """Top level Parts of Sitewide"""

    def __init__(self, **config):
        """Initialize Sitewide"""

        config = rephrase(config)
        super().__init__("sitewide", **config)

    def __copy_user__(self, user):
        """__copy_user__(x) --> None
        Updates the user part in Sitewide with values from request.user"""

        userdict = {}
        if not hasattr(user, "email") or not hasattr(user, "username"):
            # Anonymous User
            userdict.update(
                {
                    "user:email:value": default("email", "value"),
                    "user:avatar:path": default("avatar", "path"),
                    "user:username:value": default("username", "value"),
                    "user:url": default("user", "url"),
                }
            )
        else:  # Authenticated User
            if hasattr(user, "avatar"):
                try:
                    path = user.avatar.url
                except ValueError:  # User did not upload Avatar Image
                    path = default("avatar", "path")
            userdict.update(
                {
                    "user:avatar:path": path,
                    "user:email:value": user.email,
                    "user:username:value": user.username,
                    "user:url": user.get_absolute_url(),
                }
            )
        self.update(**userdict)

    def route(self, path):
        """route(x) -> (y, z)
        where x is str path delimited by colons. Route returns a tuple where y
        is the last part in the specified path and z is the target attribute"""

        attr = "unspecified"
        part = lastpart = self
        if not path.split(":"):
            raise ValueError("Bad or unspecified path")
        for attr in path.split(":"):
            lastpart = part
            if not hasattr(part, attr):
                raise AttributeError(f"{part} has no {attr} attribute")
            part = getattr(part, attr)
        return lastpart, attr

    def update(self, **kwargs):
        """Update this live instance of Sitewide and its sub-parts"""

        for path, value in kwargs.items():
            if path == "user":
                self.__copy_user__(value)
                continue
            obj, attr = self.route(path)
            setattr(obj, attr, value)
