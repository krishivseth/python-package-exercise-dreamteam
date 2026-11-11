import secrets
import string

from .scoring import _has_repetition, _has_sequence, _is_common

SYMBOLS = "!@#$%^&*-_=+?"
MIN_LENGTH = 12
MAX_LENGTH = 128
MIN_WORDS = 4
MAX_WORDS = 12

WORDS = (
    "acorn", "admiral", "algae", "almond", "amber", "anchor", "angle", "antler",
    "anvil", "apple", "apron", "arcade", "arrow", "aspen", "atlas", "attic",
    "autumn", "avocado", "badger", "bagel", "bamboo", "banjo", "barley", "basil",
    "beacon", "beaver", "bellow", "berry", "bison", "blanket", "blossom", "bonfire",
    "bramble", "breeze", "brick", "bridge", "bronze", "bucket", "buffalo", "bugle",
    "butter", "cabin", "cactus", "camel", "candle", "canoe", "canyon", "carbon",
    "carpet", "castle", "cedar", "cello", "cherry", "chimney", "cider", "cinder",
    "citrus", "clover", "cobalt", "comet", "copper", "coral", "cotton", "cougar",
    "crater", "crayon", "cricket", "crumb", "crystal", "cumin", "dagger", "daisy",
    "dolphin", "donut", "dune", "eagle", "ember", "emerald", "falcon", "feather",
    "fennel", "fiddle", "fig", "flannel", "flint", "fossil", "galaxy", "garnet",
    "gecko", "ginger", "glacier", "goblet", "goose", "granite", "grape", "gravel",
    "harbor", "harvest", "hazel", "hedgehog", "helmet", "heron", "hickory", "honey",
    "horizon", "iceberg", "igloo", "indigo", "iris", "island", "ivory", "jacket",
    "jayyu", "jelly", "juniper", "kayak", "kettle", "kiwi", "koala", "ladder",
    "lagoon", "lantern", "lemon", "lentil", "lilac", "llama", "lobster", "locket",
    "lotus", "magnet", "mango", "maple", "marble", "meadow", "melon", "mitten",
    "molar", "moose", "mosaic", "muffin", "mural", "nectar", "nickel", "noodle",
    "nutmeg", "oasis", "oatmeal", "ocean", "olive", "onion", "orbit", "orchid",
    "otter", "oyster", "paddle", "panda", "papaya", "parade", "parcel", "parrot",
    "peanut", "pebble", "pelican", "pepper", "pickle", "pigeon", "pillow", "pirate",
    "planet", "plum", "pocket", "poodle", "potato", "pretzel", "pumpkin", "puzzle",
    "quartz", "quill", "rabbit", "raccoon", "radish", "raisin", "raven", "ribbon",
    "riddle", "river", "robin", "rocket", "saddle", "salmon", "sapphire", "satchel",
    "scarf", "seashell", "sequoia", "shovel", "silver", "sketch", "sparrow", "spinach",
    "spruce", "squash", "summit","tablet", "taco", "tangerine",
    "teapot", "thimble", "thistle", "thunder", "timber", "toast", "tomato", "topaz",
    "tortoise", "trumpet", "tulip", "tundra", "turnip", "turtle", "tuxedo", "umbrella",
    "valley", "velvet", "violet", "volcano", "waffle", "walnut", "walrus", "willow",
    "window", "wizard", "yogurt", "zucchini",
)


def generate_password(length: int | None = None, symbols: bool = True, words: bool = False) -> str:
    if not isinstance(symbols, bool):
        raise TypeError("symbols must be True or False")
    if not isinstance(words, bool):
        raise TypeError("words must be True or False")
    if length is not None and (isinstance(length, bool) or not isinstance(length, int)):
        raise TypeError("length must be an integer")

    if words:
        return _generate_passphrase(5 if length is None else length, symbols)
    return _generate_characters(16 if length is None else length, symbols)


def _passes_checks(candidate: str) -> bool:
    return not (_has_repetition(candidate) or _has_sequence(candidate) or _is_common(candidate))


def _generate_characters(length: int, symbols: bool) -> str:
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        raise ValueError(f"length must be between {MIN_LENGTH} and {MAX_LENGTH}")

    groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if symbols:
        groups.append(SYMBOLS)
    pool = "".join(groups)

    while True:
        candidate = "".join(secrets.choice(pool) for _ in range(length))
        if not all(any(c in group for c in candidate) for group in groups):
            continue
        if _passes_checks(candidate):
            return candidate


def _generate_passphrase(count: int, symbols: bool) -> str:
    if not MIN_WORDS <= count <= MAX_WORDS:
        raise ValueError(f"word count must be between {MIN_WORDS} and {MAX_WORDS}")

    rng = secrets.SystemRandom()
    while True:
        chosen = rng.sample(WORDS, count)
        if symbols:
            candidate = "-".join(chosen)
        else:
            candidate = "".join(word.capitalize() for word in chosen)
        if _passes_checks(candidate):
            return candidate
