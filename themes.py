import random

THEMES = {
    "Fruits & Vegetables": [
        "APPLE", "BANANA", "CARROT", "LEMON", "ONION", "PEACH", "POTATO",
        "TOMATO", "CELERY", "CUCUMBER", "GARLIC", "GINGER", "KALE",
        "PEPPER", "PUMPKIN", "SPINACH", "ZUCCHINI"
    ],
    "Space": [
        "COMET", "EARTH", "GALAXY", "MOON", "NEBULA", "ORBIT", "PLUTO",
        "STAR", "SUN", "UNIVERSE", "ASTEROID", "COSMOS", "GRAVITY", "METEOR",
        "PLANET", "SUPERNOVA", "TELESCOPE", "WORMHOLE"
    ],
    "Oceans": [
        "ANEMONE", "CORAL", "DOLPHIN", "JELLYFISH", "KELP", "OCTOPUS", "ORCA",
        "SALMON", "SHARK", "WHALE", "ALGAE", "CLAM", "CRAB", "LOBSTER",
        "MANTA", "RAID", "SEAHORSE", "SEAL", "STINGRAY", "TURTLE"
    ],
    "Animals": [
        "BUTTERFLY", "CHEETAH", "CHIMPANZEE", "CORAL", "DOLPHIN", "ELEPHANT",
        "FALCON", "GECKO", "GORILLA", "HYENA", "IGUANA", "JAGUAR", "KANGAROO",
        "LEOPARD", "MEERKAT", "OKAPI", "PANGOLIN", "QUAIL", "REINDEER",
        "SLOTH", "TIGER", "WHALE", "YAK", "ZEBRA"
    ],
    "Colors": [
        "AMBER", "AVOCADO", "BURGUNDY", "CARMINE", "CERULEAN", "CHARCOAL",
        "CINNAMON", "CORAL", "CRIMSON", "EMERALD", "GOLD", "INDIGO", "JADE",
        "LAVENDER", "LIME", "MALACHITE", "MAROON", "NAVY", "OLIVE", "ORANGE",
        "PERIDOT", "PINK", "RUBY", "RUST", "SAPPHIRE", "SCARLET", "TEAL",
        "TURQUOISE", "ULTRAMARINE", "VERMILION", "VIOLET", "WHITE", "WINE",
        "YELLOW"
    ],
    "Weather": [
        "BLIZZARD", "BREEZE", "CIRRUS", "CLOUD", "DEW", "DOWNPOUR", "DUSTSTORM",
        "ECLIPSE", "FOG", "FREEZING", "HAIL", "HURRICANE", "LIGHTNING",
        "MONSOON", "RAIN", "RAINBOW", "SLEET", "STORM", "SYNOPTIC", "TORNADO",
        "TROPICAL", "TYPHOON", "WIND", "WINDSTORM"
    ],
    "Cooking": [
        "BAKING", "BOILING", "BRISKET", "CHOP", "COOKING", "DEGLAZE", "DRIED",
        "FILLET", "FRIING", "GRILL", "GUSTO", "HERBS", "KETCHUP", "MARINATE",
        "ORANGE", "PAPRIKA", "PASTE", "PEPPER", "POACH", "PURITY", "REDUCTION",
        "SAUCE", "SAUTE", "SEASON", "SEAR", "SIMMER", "SLICED", "SPICE",
        "SPONGE", "STEAM", "STEW", "STIR", "TENDERIZE", "TOMATO", "VERMICELLI",
        "VINEGAR", "YOLK"
    ],
    "Body Parts": [
        "ANKLE", "ARM", "BRAIN", "CARDIO", "CARPAL", "CHEST", "CHIN", "CLAVICLE",
        "COLON", "ELBOW", "ESOPHAGUS", "FEMUR", "FIBULA", "FOREARM", "GALLBLADDER",
        "HEART", "HIP", "HUMERUS", "INTESTINE", "JAW", "KNEE", "LIVER", "LUNGS",
        "METACARPAL", "MOUTH", "NAVEL", "NECK", "NOSE", "ORGAN", "PATELLA",
        "PHALANGE", "PINNA", "PULSE", "RECTOR", "RENAL", "RIBCAGE",
        "SCAPULA", "SHIN", "SHOULDER", "SINUS", "SKELETON", "SKULL", "SPINE",
        "STAMINA", "STERNUM", "STOMACH", "SWEAT", "TARSAL", "TEETH", "THIGH",
        "THROAT", "THUMB", "TIBIA", "TOE", "TONGUE", "TOOTH", "TORSO", "TRACHEA",
        "ULNA", "URETER", "URETHRA", "UMBILICAL", "VEIN", "VESICLE", "WRIST"
    ],
    "Clothing": [
        "ACCENT", "ANKLE", "BUTTON", "COAT", "CORSET", "CUFF", "DRESS", "EARMUFFS",
        "FOOTWEAR", "HOOD", "HOSE", "HOSEAS", "JACKET", "JEWELRY", "JODHPURS",
        "KIMONO", "KNEE", "LATCHE", "LEG", "LEGGINGS", "LACE", "LAPEL", "PANTS",
        "PEASANT", "PECO", "PONCHO", "POUCH", "PULLOVER", "RIBBON", "RIFLE",
        "ROBE", "ROBEAS", "ROPE", "SANDAL", "SCARF", "SEAM", "SHIRT", "SHOES",
        "SHOULDER", "SHROUD", "SKIRT", "SLIPPER", "SMOCK", "SOCK", "SOLAR", "STOCKINGS",
        "STRAP", "SUIT", "SUNDER", "SWIM", "SWIMWEAR", "TIE", "TIEING", "TIGHT",
        "TROUSER", "TUNIC", "VEST", "WEAR", "WEAVE", "WOOL", "WRAP"
    ],
    "Musical Terms": [
        "ACCORDION", "ADAGIO", "ALLEGRO", "ARPEGGIO", "AUDIENCE", "AUDITORY",
        "BAND", "BANDURA", "BARITONE", "BASS", "BASSOON", "BELL", "BIBOP", "BLARE",
        "BLAST", "BLASTED", "BONGO", "BRAID", "BRASS", "BRASSIERE", "BREATH",
        "BREATHING", "BRIDGE", "BROOD", "BROODING", "BUCKSHOT", "BUCKWHEAT",
        "BUDGE", "BUFFET", "BUGLE", "BULB", "BULL", "BURLAP", "BURLESQUE", "BURN",
        "BURNING", "BUTTER", "BUTTERMILK", "BUTTERY", "CACTUS", "CAIN", "CAKE",
        "CALF", "CALIBER", "CALL", "CALLIOPE", "CALLING", "CALLUSED", "CALM",
        "CALMING", "CAMERA", "CAMP", "CAMPER", "CAN", "CANAPE", "CANCEL", "CANDID",
        "CANDY", "CANE", "CANON", "CANOPUS", "CANOPY", "CANTATA", "CANTER",
        "CANTO", "CANTOR", "CANYON", "CAP", "CAPACITY", "CAPE", "CAPER", "CAPITAL"
    ]
}


def get_words_for_theme(theme_name: str, count: int = 7) -> list[str]:
    """Select random words from a theme, ensuring they're 4-8 characters."""
    words = THEMES.get(theme_name, [])
    filtered = [w for w in words if 4 <= len(w) <= 8]
    return random.sample(filtered, min(count, len(filtered)))


def get_random_theme() -> str:
    """Return a random theme name."""
    return random.choice(list(THEMES.keys()))


def generate_puzzle() -> dict:
    """Generate a valid puzzle with a spangram and 6 themed words."""
    theme = get_random_theme()
    words = get_words_for_theme(theme, 7)
    
    words_sorted = sorted(words, key=len, reverse=True)
    spangram = words_sorted[0]
    themed_words = words_sorted[1:]
    
    return {
        "theme": theme,
        "spangram": spangram,
        "themed_words": themed_words,
        "grid_size": (6, 8)
    }
