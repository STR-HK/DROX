def openr(file):
    return open(file=file, mode="r", encoding="utf-8")


def get_all(file):
    rec = []
    for line in openr(file).readlines():
        comp = line.strip()
        if comp.startswith("import") or comp.startswith("from"):
            if "My" in comp:
                # print(comp)
                print("---------------------------------------------------------------")
                module_name = comp.split(" ")[1]
                # print(f"import {module_name}")

                loc = {}

                # print(f"{module_name}.__file__")
                try:
                    exec(f"import {module_name}")
                    exec(f"loc['return'] = {module_name}.__file__")
                    # print(loc["return"])
                    rec.append(loc["return"])
                except Exception as e:
                    print(e)

    return rec


for mod in get_all("../gui.py"):
    print(mod)
