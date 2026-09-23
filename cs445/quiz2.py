import sys, importlib

pkgs = [
    "jupyterlab",
    "nbgrader",
    "matplotlib",
    "pandas",
    "sklearn",
    "torch",
    "torchvision",
]
vers = {}
# for p in pkgs:
#     try:
#         m = importlib.import_module(p)
#         vers[p] = getattr(m, "__version__", "ok")
#     except Exception as e:
#         vers[p] = f"ERR:{type(e).__name__}"
# print("Python", sys.version.split()[0])
# print(*[f"{k}: {vers[k]}" for k in pkgs], sep="\n")

import numpy as np
# a = np.array([2.0, 4.0, 6.0, 8.0])
# b = a[0:2]
# b[1] = -1.0
# print(a)
a = np.array([[1, -2, 3], [3, 4, -1]])
print a[:, 1]