import os.path

import yaml

books = yaml.safe_load(
    open(
        os.path.join(
            os.path.dirname(__file__),
            "data/data.yml"
        )
    )
)


for i, book in enumerate(books):
    book['id'] = i


def get_sample():
    return books[:10]
