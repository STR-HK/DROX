import seaborn as sns

l = []

# for i in range(1, 10 + 1):
#     s = MyPicker.pick_color("./lip1.jpg", NUM_CLUSTERS=i, USE_CACHE=False)
#     print(s)

# import seaborn as sns
#
colors = ["#FF0B04", "#4374B3"]
palette = sns.color_palette(colors)

sns.set_palette(palette)
sns.palplot(palette)
