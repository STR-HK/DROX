from curses import termattrs

from regex import P
from ..palettes.core_palette import *
from ..utils.string_utils import hexFromArgb
import json

# /**
#  * Represents a Material color scheme, a mapping of color roles to colors.
#  */
# Using dictionary instead of JavaScript Object
class Scheme:
    def __init__(self, props):
        self.props = props

    def get_primary(self):
        return hexFromArgb(self.props["primary"])

    def get_primaryContainer(self):
        return hexFromArgb(self.props["primaryContainer"])

    def get_onPrimary(self):
        return hexFromArgb(self.props["onPrimary"])

    def get_onPrimaryContainer(self):
        return hexFromArgb(self.props["onPrimaryContainer"])

    def get_secondary(self):
        return hexFromArgb(self.props["secondary"])

    def get_secondaryContainer(self):
        return hexFromArgb(self.props["secondaryContainer"])

    def get_onSecondary(self):
        return hexFromArgb(self.props["onSecondary"])

    def get_onSecondaryContainer(self):
        return hexFromArgb(self.props["onSecondaryContainer"])

    def get_tertiary(self):
        return hexFromArgb(self.props["tertiary"])

    def get_onTertiary(self):
        return hexFromArgb(self.props["onTertiary"])

    def get_tertiaryContainer(self):
        return hexFromArgb(self.props["tertiaryContainer"])

    def get_onTertiaryContainer(self):
        return hexFromArgb(self.props["onTertiaryContainer"])

    def get_error(self):
        return hexFromArgb(self.props["error"])

    def get_onError(self):
        return hexFromArgb(self.props["onError"])

    def get_errorContainer(self):
        return hexFromArgb(self.props["errorContainer"])

    def get_onErrorContainer(self):
        return hexFromArgb(self.props["onErrorContainer"])

    def get_background(self):
        return hexFromArgb(self.props["background"])

    def get_onBackground(self):
        return hexFromArgb(self.props["onBackground"])

    def get_surface(self):
        return hexFromArgb(self.props["surface"])

    def get_onSurface(self):
        return hexFromArgb(self.props["onSurface"])

    def get_surfaceVariant(self):
        return hexFromArgb(self.props["surfaceVariant"])

    def get_onSurfaceVariant(self):
        return hexFromArgb(self.props["onSurfaceVariant"])

    def get_outline(self):
        return hexFromArgb(self.props["outline"])

    def get_shadow(self):
        return hexFromArgb(self.props["shadow"])

    def get_inverseSurface(self):
        return hexFromArgb(self.props["inverseSurface"])

    def get_inverseOnSurface(self):
        return hexFromArgb(self.props["inverseOnSurface"])

    def get_inversePrimary(self):
        return hexFromArgb(self.props["inversePrimary"])

    primary = property(get_primary)
    primaryContainer = property(get_primaryContainer)
    onPrimary = property(get_onPrimary)
    onPrimaryContainer = property(get_onPrimaryContainer)
    secondary = property(get_secondary)
    secondaryContainer = property(get_secondaryContainer)
    onSecondary = property(get_onSecondary)
    onSecondaryContainer = property(get_onSecondaryContainer)
    tertiary = property(get_tertiary)
    onTertiary = property(get_onTertiary)
    tertiaryContainer = property(get_tertiaryContainer)
    onTertiaryContainer = property(get_onTertiaryContainer)
    error = property(get_error)
    onError = property(get_onError)
    errorContainer = property(get_errorContainer)
    onErrorContainer = property(get_onErrorContainer)
    background = property(get_background)
    onBackground = property(get_onBackground)
    surface = property(get_surface)
    onSurface = property(get_onSurface)
    surfaceVariant = property(get_surfaceVariant)
    onSurfaceVariant = property(get_onSurfaceVariant)
    outline = property(get_outline)
    shadow = property(get_shadow)
    inverseSurface = property(get_inverseSurface)
    inverseOnSurface = property(get_inverseOnSurface)
    inversePrimary = property(get_inversePrimary)

    # /**
    #  * @param argb ARGB representation of a color.
    #  * @return Light Material color scheme, based on the color's hue.
    #  */
    @staticmethod
    def light(argb):
        core = CorePalette.of(argb)
        return Scheme(
            {
                "primary": core.a1.tone(40),
                "onPrimary": core.a1.tone(100),
                "primaryContainer": core.a1.tone(90),
                "onPrimaryContainer": core.a1.tone(10),
                "secondary": core.a2.tone(40),
                "onSecondary": core.a2.tone(100),
                "secondaryContainer": core.a2.tone(90),
                "onSecondaryContainer": core.a2.tone(10),
                "tertiary": core.a3.tone(40),
                "onTertiary": core.a3.tone(100),
                "tertiaryContainer": core.a3.tone(90),
                "onTertiaryContainer": core.a3.tone(10),
                "error": core.error.tone(40),
                "onError": core.error.tone(100),
                "errorContainer": core.error.tone(90),
                "onErrorContainer": core.error.tone(10),
                "background": core.n1.tone(99),
                "onBackground": core.n1.tone(10),
                "surface": core.n1.tone(99),
                "onSurface": core.n1.tone(10),
                "surfaceVariant": core.n2.tone(90),
                "onSurfaceVariant": core.n2.tone(30),
                "outline": core.n2.tone(50),
                "shadow": core.n1.tone(0),
                "inverseSurface": core.n1.tone(20),
                "inverseOnSurface": core.n1.tone(95),
                "inversePrimary": core.a1.tone(80),
            }
        )

    # /**
    #  * @param argb ARGB representation of a color.
    #  * @return Dark Material color scheme, based on the color's hue.
    #  */
    @staticmethod
    def dark(argb):
        core = CorePalette.of(argb)
        return Scheme(
            {
                "primary": core.a1.tone(80),
                "onPrimary": core.a1.tone(20),
                "primaryContainer": core.a1.tone(30),
                "onPrimaryContainer": core.a1.tone(90),
                "secondary": core.a2.tone(80),
                "onSecondary": core.a2.tone(20),
                "secondaryContainer": core.a2.tone(30),
                "onSecondaryContainer": core.a2.tone(90),
                "tertiary": core.a3.tone(80),
                "onTertiary": core.a3.tone(20),
                "tertiaryContainer": core.a3.tone(30),
                "onTertiaryContainer": core.a3.tone(90),
                "error": core.error.tone(80),
                "onError": core.error.tone(20),
                "errorContainer": core.error.tone(30),
                "onErrorContainer": core.error.tone(80),
                "background": core.n1.tone(10),
                "onBackground": core.n1.tone(90),
                "surface": core.n1.tone(10),
                "onSurface": core.n1.tone(90),
                "surfaceVariant": core.n2.tone(30),
                "onSurfaceVariant": core.n2.tone(80),
                "outline": core.n2.tone(60),
                "shadow": core.n1.tone(0),
                "inverseSurface": core.n1.tone(90),
                "inverseOnSurface": core.n1.tone(20),
                "inversePrimary": core.a1.tone(40),
            }
        )

    def toJSON(self):
        return json.dumps(self.props)
