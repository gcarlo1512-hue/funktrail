
from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

PHOTOS_FOLDER = os.path.join(app.static_folder, 'photos')
VIDEOS_FOLDER = os.path.join(app.static_folder, 'videos')
CONTACT_FOLDER = os.path.join(app.static_folder, 'contact')

@app.route('/')
def index():
    cover_image = url_for('static', filename='img/copertina.jpg')
    return render_template('index.html', cover_image=cover_image)

@app.route('/photos')
def photos_page():
    photos = os.listdir(PHOTOS_FOLDER)
    photo_urls = [url_for('static', filename=f'photos/{p}') for p in photos if p.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
    return render_template('photos.html', photos=photo_urls)

@app.route('/videos')
def videos_page():
    videos = [
        v for v in os.listdir(VIDEOS_FOLDER)
        if os.path.isfile(os.path.join(VIDEOS_FOLDER, v))
        and v.lower().endswith(('.mp4', '.mov', '.avi', '.webm', '.mkv'))
        and not v.startswith('.')  # ← ignora .DS_Store e altri file nascosti
    ]

    video_urls = []
    for v in videos:
        name = os.path.splitext(v)[0]
        video_urls.append({
            'video': url_for('static', filename=f'videos/{v}'),
            'thumb': url_for('static', filename=f'photos/{name}.jpg')
                      if os.path.exists(os.path.join(PHOTOS_FOLDER, f'{name}.jpg'))
                      else url_for('static', filename='img/anteprima.jpg'),
            'name': name
        })
    return render_template('videos.html', videos=video_urls)


@app.route('/shop')
def shop_page():
    shop_folder = os.path.join(app.static_folder, 'shop')
    shop_items = []

    price_list = {
        'maglietta': '20.00',
        'cd_funk': '15.00',
        'poster': '10.00',
        'cappellino': '12.00'
    }

    if os.path.exists(shop_folder):
        for f in sorted(os.listdir(shop_folder)):
            file_path = os.path.join(shop_folder, f)
            if os.path.isfile(file_path) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                name = os.path.splitext(f)[0]
                shop_items.append({
                    'name': name,
                    'image': url_for('static', filename=f'shop/{f}'),
                    'price': price_list.get(name, 'N.D.')
                })

    return render_template('shop.html', products=shop_items)

@app.route('/contact')
def contact_page():
    contact_path = os.path.join(app.static_folder, 'contact', 'contatti.txt')

    try:
        with open(contact_path, 'r', encoding='utf-8') as f:
            contact_info = f.read()
    except FileNotFoundError:
        contact_info = "Contact file not found. Please create static/contact/contatti.txt"

    return render_template('contact.html', contact_info=contact_info)



@app.route('/biografia')
def biografia_page():
    return render_template('biografia.html')

@app.route('/concerti')
def concerti_page():
    return render_template('concerti.html')

if __name__ == '__main__':
    app.run(debug=True)
