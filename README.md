# Corn

This package estimates corn row locations in images of corn fields. To use the package locally:

```sh
# Requires python 3.6.x+
python setup.py install
```

It can now be imported from your environment:

```py
from corn import finder as cf

estimated_corn_rows = cf.find_in_image("path/to/corn.jpg")

print(estimated_corn_rows)
# [
#   [rho1, theta1],
#   [rho2, theta2],
#   ...
# ]
```

Or via the provided CLI:

```py
python cli.py path/to/corn.jpg
```
