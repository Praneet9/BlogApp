import os
from PIL import Image
from flaskblog import app


def iter_pages(pages,
               page,
               left_edge=1,
               left_current=1,
               right_current=2,
               right_edge=1):
    last = 0
    for num in range(1, pages + 1):
        if num <= left_edge or \
            (num > page - left_current - 1 and \
            num < page + right_current) or \
            num > pages - right_edge:
            if last + 1 != num:
                yield None
            yield num
            last = num


def save_picture(form_picture):
    random_hex = os.urandom(8).hex()
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',
                                picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn