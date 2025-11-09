
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
    # 🔹 VIDEO LOCALI (MP4)
    videos = [
        v for v in os.listdir(VIDEOS_FOLDER)
        if os.path.isfile(os.path.join(VIDEOS_FOLDER, v))
        and v.lower().endswith(('.mp4', '.mov', '.avi', '.webm', '.mkv'))
        and not v.startswith('.')
    ]

    video_items = []

    for v in videos:
        name = os.path.splitext(v)[0]

        # ✅ MODIFICA A: controlla se il video e la foto esistono
        video_path = os.path.join(VIDEOS_FOLDER, v)
        thumb_path = os.path.join(PHOTOS_FOLDER, f'{name}.jpg')

        thumb_url = (
            url_for('static', filename=f'photos/{name}.jpg')
            if os.path.exists(video_path) and os.path.exists(thumb_path)
            else url_for('static', filename='img/anteprima.jpg')
        )

        # ✅ MODIFICA B: usa thumb_url corretto
        video_items.append({
            'type': 'local',
            'video': url_for('static', filename=f'videos/{v}'),
            'thumb': thumb_url,
            'name': name
        })

    # ✅ MODIFICA C: aggiunti video YouTube
    youtube_videos = [
        {
            'type': 'youtube',
            'id': 'SZEfi21a0_o',
            'name': 'FunkTrail Live (youtube)'
        },
        {
            'type': 'youtube',
            'id': 'V_o3H1pV-jo',
            'name': 'Always There (youtube)'
        },
        {
            'type': 'youtube',
            'id': 'xxZFpIjrGj0', 
            'name': 'Sweet Little Sister (youtube)'
        },
        {
            'type': 'youtube',
            'id': '7xJW4pXZAjw',
            'name': 'Street Life (youtube)'
        }        
    ]

    # ✅ MODIFICA D: unisci video locali e YouTube
    all_videos = video_items + youtube_videos

    return render_template('videos.html', videos=all_videos)





@app.route('/shop')
def shop_page():
    shop_folder = os.path.join(app.static_folder, 'shop')
    shop_items = []

    price_list = {
        'cappellino': '20.00',
        'logo': '15.00',
        'maglietta': '10.00',
        'orologio': '12.00',
        'poster': '30.00',
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
    bio_folder = os.path.join(app.static_folder, 'biografia')
    bio_blocks = []

    if os.path.exists(bio_folder):
        for file in sorted(os.listdir(bio_folder)):
            if file.lower().endswith('.txt'):
                base_name = os.path.splitext(file)[0]
                txt_path = os.path.join(bio_folder, file)
                img_path = os.path.join(bio_folder, base_name + '.jpg')

                # 🔹 legge il testo dal file .txt
                with open(txt_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                # 🔹 controlla se esiste la foto corrispondente
                if os.path.exists(img_path):
                    image_url = url_for('static', filename=f'biografia/{base_name}.jpg')
                else:
                    image_url = url_for('static', filename='img/default_bio.jpg')  # immagine di riserva

                bio_blocks.append({'text': text, 'image': image_url})
    else:
        bio_blocks = [{'text': 'Nessun contenuto trovato.', 'image': url_for('static', filename='img/default_bio.jpg')}]

    return render_template('biografia.html', bio_blocks=bio_blocks)


@app.route('/concerti')
def concerti_page():
    return render_template('concerti.html')

if __name__ == '__main__':
    app.run(debug=True)
