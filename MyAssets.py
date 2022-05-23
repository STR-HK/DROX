from os import path

P_ICON = "./icon/"

P_ICON_MAIN = P_ICON + "/main/"

P_COVER = P_ICON_MAIN + "/cover/"
C_Cover1 = P_COVER + "Cover1.png"
C_Cover2 = P_COVER + "Cover2.png"
C_Winter = P_COVER + "Winter.jpg"
C_Heoney = P_COVER + "Heoney.jpg"

P_FOOTER = P_ICON_MAIN + "/footer/"
I_Home = P_FOOTER + "home.svg"
II_Home = P_FOOTER + "home_i.svg"
I_Search = P_FOOTER + "search.svg"
II_Search = P_FOOTER + "search_i.svg"
I_Playlist = P_FOOTER + "playlist.svg"
II_Playlist = P_FOOTER + "playlist_i.svg"
I_Single = P_FOOTER + "note.svg"
II_Single = P_FOOTER + "note_i.svg"
I_Setting = P_FOOTER + "settings.svg"
II_Setting = P_FOOTER + "settings_i.svg"
I_Hourglass = P_FOOTER + "hourglass.svg"
II_Hourglass = P_FOOTER + "hourglass_i.svg"

P_WINDOW = P_ICON + "/window/"
I_Close = P_WINDOW + "chrome-close.svg"
I_Minimize = P_WINDOW + "chrome-minimize.svg"
I_Maximize = P_WINDOW + "chrome-maximize.svg"
I_Restore = P_WINDOW + "chrome-restore.svg"


P_PROFILE = P_ICON_MAIN + "/profile/"
R_Profile = P_PROFILE + "Profile.png"
R_Mention = P_PROFILE + "Mention.jpg"

P_ANI = P_ICON_MAIN + "/ani/"
A_Loading = P_ANI + "Spinner.svg"

kaiyu = P_ICON + "kaiyu.jpg"

# for var in dir():
#     if not var.startswith("__"):
#         globals()[var] = path.abspath(var)
