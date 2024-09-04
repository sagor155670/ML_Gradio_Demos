import gradio as gr
import json
import requests
import zipfile
from zipfile import ZipFile
import io,os,glob
from PIL import Image

styles = ['(No style)', 'Watercolor', 'Film Noir', 'Neon', 'Jungle', 'Mars', 'Vibrant Color', 'Snow', 'Line art', 'Analog Film', 'Cinematic', 'Craft Clay', 'Digital Art', 'Enhance', 'Isometric Style', 'Lowpoly', 'Neon Punk', 'Origami', 'Photographic', 'Pixel Art', 'Texture', 'Advertising', 'Food Photography', 'Real Estate', 'Abstract', 'Cubist', 'Graffiti', 'Hyperrealism', 'Impressionist', 'Pointillism', 'Pop Art', 'Psychedelic', 'Renaissance', 'Steampunk', 'Surrealist', 'Typography', 'Watercolor', 'Fighting Game', 'GTA', 'Super Mario', 'Minecraft', 'Pokémon', 'Retro Arcade', 'Retro Game', 'RPG Fantasy Game', 'Strategy Game', 'Street Fighter', 'Legend of Zelda', 'Architectural', 'Disco', 'Dreamscape', 'Dystopian', 'Fairy Tale', 'Gothic', 'Grunge', 'Horror', 'Minimalist', 'Monochrome', 'Nautical', 'Space', 'Stained Glass', 'Techwear Fashion', 'Tribal', 'Zentangle', 'Collage', 'Flat Papercut', 'Kirigami', 'Paper Mache', 'Paper Quilling', 'Papercut Collage', 'Papercut Shadow Box', 'Stacked Papercut', 'Thick Layered Papercut', 'Alien', 'Film Noir-2', 'HDR', 'Long Exposure', 'Neon Noir', 'Silhouette', 'Tilt-Shift', 'Digital art', 'Comic book', 'Fantasy art', 'Neonpunk', 'Isometric', 'Line art', 'Craft clay', '3d-model', 'pixel art', 'Enhance', 'sai-3d-model', 'sai-analog film', 'sai-anime', 'sai-cinematic', 'sai-comic book', 'sai-craft clay', 'sai-digital art', 'sai-enhance', 'sai-fantasy art', 'sai-isometric', 'sai-line art', 'sai-lowpoly', 'sai-neonpunk', 'sai-origami', 'sai-photographic', 'sai-pixel art', 'sai-texture', 'ads-advertising', 'ads-automotive', 'ads-corporate', 'ads-fashion editorial', 'ads-food photography', 'ads-luxury', 'ads-real estate', 'ads-retail', 'artstyle-abstract', 'artstyle-abstract expressionism', 'artstyle-art deco', 'artstyle-art nouveau', 'artstyle-constructivist', 'artstyle-cubist', 'artstyle-expressionist', 'artstyle-graffiti', 'artstyle-hyperrealism', 'artstyle-impressionist', 'artstyle-pointillism', 'artstyle-pop art', 'artstyle-psychedelic', 'artstyle-renaissance', 'artstyle-steampunk', 'artstyle-surrealist', 'artstyle-typography', 'artstyle-watercolor', 'futuristic-biomechanical', 'futuristic-biomechanical cyberpunk', 'futuristic-cybernetic', 'futuristic-cybernetic robot', 'futuristic-cyberpunk cityscape', 'futuristic-futuristic', 'futuristic-retro cyberpunk', 'futuristic-retro futurism', 'futuristic-sci-fi', 'futuristic-vaporwave', 'game-bubble bobble', 'game-cyberpunk game', 'game-fighting game', 'game-gta', 'game-mario', 'game-minecraft', 'game-pokemon', 'game-retro arcade', 'game-retro game', 'game-rpg fantasy game', 'game-strategy game', 'game-streetfighter', 'game-zelda', 'misc-architectural', 'misc-disco', 'misc-dreamscape', 'misc-dystopian', 'misc-fairy tale', 'misc-gothic', 'misc-grunge', 'misc-horror', 'misc-kawaii', 'misc-lovecraftian', 'misc-macabre', 'misc-manga', 'misc-metropolis', 'misc-minimalist', 'misc-monochrome', 'misc-nautical', 'misc-space', 'misc-stained glass', 'misc-techwear fashion', 'misc-tribal', 'misc-zentangle', 'papercraft-collage', 'papercraft-flat papercut', 'papercraft-kirigami', 'papercraft-paper mache', 'papercraft-paper quilling', 'papercraft-papercut collage', 'papercraft-papercut shadow box', 'papercraft-stacked papercut', 'papercraft-thick layered papercut', 'photo-alien', 'photo-film noir', 'photo-hdr', 'photo-long exposure', 'photo-neon noir', 'photo-silhouette', 'photo-tilt-shift', 'Space art', 'Street art', 'Baroque', 'Pointillism-2', 'Impressionist-2', 'Pop art-2', 'Minimalist-2', 'Art Deco', 'Cubist-2', 'Dada', 'Victorian', 'Art Nouveau', 'Futuristic', 'Medieval', 'Industrial', 'Vaporwave', 'Horror-2', 'Gothic', 'Steampunk', 'Retro', 'Surrealist-2', 'Realism', 'Silhouette-2', 'Collage', 'Watercolor-2', 'Calligraphy', 'Expressionist', 'Fauvist', 'Renaissance-2', 'Photorealistic', 'Symbolic', 'Avant-garde', 'Mosaic', "Trompe l'oeil", 'Rococo', 'Macabre', 'Satirical', 'Pixelated', 'Futurist', 'Primitive', 'Byzantine', 'Suprematist', 'Constructivist', 'De Stijl', 'Ukiyo-e', 'Biomechanical', 'Hyperrealism-2', 'Glitch', "Trompe-l'oeil", 'Arabesque', 'Brutalist', 'Chiaroscuro', 'Tenebrism', 'Romantic', 'Bauhaus', 'Art brut', 'Metaphysical', 'Neoplasticism', 'Hard-edge', 'Automatism', 'Tachisme', 'Lyrical abstraction', 'Color field', 'Synthetism', 'Cloisonnism', 'Assemblage', 'Vorticism', 'Op art', 'Divisionism', 'Kinetic art', 'Orphism', 'Suprematism', 'Letterism', 'Situationalist', 'Sound art', 'Land art', 'Photorealistic graffiti', 'Hypermodern', 'Virtual realism', 'Structural film', 'Process art', 'Light and space', 'Post-internet', 'Bio-art', 'Byzantine', 'Celtic', 'Native American', 'Aboriginal', 'Egyptian', 'Mayan', 'Renaissance', 'Mughal', 'Romanesque', 'Gothic-2', 'Baroque', 'Rococo', 'Pre-Raphaelite', 'Impressionist', 'Cubist', 'Surrealist', 'Futurist', 'Dada', 'Expressionist', 'Fauvist', 'Socialist Realist', 'Pop Art', 'Suprematism', 'Symbolist', 'Pre-Columbian', 'Constructivist', 'Art Nouveau', 'Precisionist', 'Neoclassical', 'Persian Miniature', 'Edo', 'Tribal-2', 'Tibetan Thangka', 'Art Deco', 'Minimalist', 'Greek Classical', 'African', 'Russian Iconography', 'Nordic', 'Inuit', 'Maori', 'Iznik', 'Ottoman', 'Hanami', 'Mandala', 'Aztec', 'Sumi-e', 'Ukiyo-e', 'Haida', 'Moorish', 'Victorian', 'Pueblo', 'Cloisonne', 'Khokhloma', 'Biedermeier', 'Goryeo', 'Han', 'Hellenistic', 'Tang', 'Ming', 'Joseon', 'Gupta', 'Pallava', 'Chola', 'Minoan', 'Mycenaean', 'Ndebele', 'San', 'Batik', 'Assyrian', 'Thracian', 'Etruscan', 'Sumerian', 'Babylonian', 'Norse', 'Olmec', 'Toltec', 'Sican', 'Nazca', 'Inca', 'Zapotec', 'Mixtec', 'Ottonian', 'Merovingian', 'Carolingian', 'Otomi', 'Huichol', 'Ainu', 'Maori', 'Aboriginal', 'Inuit', 'Saami', 'Ojibwe', 'Tlingit', 'Navajo', 'Apache', 'Zuni', 'Hopi', 'Sioux', 'Lakota', 'Yupik', 'Cherokee', 'Mohawk', 'Cree', 'Acoma', 'Laguna', 'Seminole', 'Osage', 'Anasazi', 'Mimbres', 'Pomo', 'Hohokam', 'Mississippian', 'Fremont', 'Mogollon', 'Salado', 'Zulu', 'Maasai', 'Ndebele', 'Kuba', 'Yoruba', 'Akan', 'Berber', 'Dogon', 'Fang', 'Baga', 'Blade Runner', 'Star Wars', 'Lord of the Rings', 'Matrix', 'Indiana Jones', 'Mad Max', '2001: A Space Odyssey', 'Alien-2', 'Avatar', 'Pulp Fiction', 'Kill Bill', 'Inception', 'Fight Club', 'Harry Potter', 'Marvel Cinematic Universe', 'DC Extended Universe', 'Game of Thrones', 'Twilight', 'Transformers', 'The Hunger Games', 'Pirates of the Caribbean', 'Jurassic Park', 'The Shining', 'The Godfather', 'The Dark Knight', 'Casablanca', 'Jaws', 'The Wizard of Oz', 'E.T.', 'Ghostbusters', 'Back to the Future', 'Toy Story', 'The Lion King', 'Finding Nemo', 'Shrek', 'The Little Mermaid', 'Aladdin', 'Beauty and the Beast', 'Cinderella', 'Sleeping Beauty', 'Snow White', 'Mulan', 'Pocahontas', 'The Nightmare Before Christmas', 'Frozen', 'Moana', 'Tangled', 'Zootopia', 'Coco', 'Brave', 'Inside Out', 'The Incredibles', 'Up', 'Wall-E', 'Ratatouille', 'Monsters Inc.', 'Cars', "A Bug's Life", 'James Bond', 'Fast and Furious', 'Mission Impossible', 'Jurassic World', 'Minions', 'Interstellar', 'The Grinch', 'Avengers: Endgame', 'Wonder Woman', 'The Iron Giant', 'Godzilla', 'King Kong', 'The Grand Budapest Hotel', 'Inside Llewyn Davis', 'Drive', 'The Neon Demon', 'It Follows', 'Dunkirk', 'Her', 'The Revenant', 'Whiplash', 'The Shape of Water', 'A Ghost Story', 'The Florida Project', 'La La Land', 'The Lobster', 'Ex Machina', 'Birdman', 'Gravity', 'The Tree of Life', 'Inception', 'The Social Network', 'Moonlight', 'Roma', 'Parasite', '1917', 'Jojo Rabbit', 'Joker', 'The Lighthouse', 'Once Upon a Time in Hollywood', 'The Irishman', 'Uncut Gems', 'Little Women', 'Knives Out', 'Marriage Story', 'Midsommar', 'Booksmart', 'Ford v Ferrari', 'Rocketman', 'Ad Astra', 'Waves', 'The Farewell', 'Hustlers', 'Portrait of a Lady on Fire', 'Pain and Glory', 'The Two Popes', 'A Beautiful Day in the Neighborhood', 'The Peanut Butter Falcon', 'The Goldfinch', 'High Life', 'The Nightingale', 'Yesterday', 'Doctor Sleep', 'The Farewell', 'John Wick 3', 'Us', 'The Irishman', 'Honey Boy', 'Joker', 'Uncut Gems', '1917', 'Ford v Ferrari', 'Cats', 'Jojo Rabbit', 'Parasite', 'The Lion King', 'Aladdin', 'Toy Story 4', 'Avengers: Endgame', 'Star Wars: The Rise of Skywalker', 'Downton Abbey', 'Frozen 2', 'Little Women', '2D Traditional Animation', 'CGI Animation', 'Stop-Motion Animation', 'Claymation', 'Vector Animation', 'Flash Animation', 'Rotoscope Animation', 'Cut-Out Animation', 'Sand Animation', 'Pixel Art Animation', 'Anime Style Animation', 'Manga Style Art', 'Chibi Style Art', 'Superflat', 'Ukiyo-e', 'Western Comics Art', 'Graphic Novel Art', 'Cartoon Modern', 'Abstract Animation', 'Silhouette Animation', 'Looney Tunes', 'Disney Classic', 'Studio Ghibli', 'Pixar', 'Shonen', 'Mecha', 'Shojo', 'Nickelodeon', 'Cartoon Network', 'Adult Swim', 'Adventure Time', 'Rick and Morty', 'South Park', 'The Simpsons', 'Family Guy', "Bob's Burgers", 'Gravity Falls', 'Steven Universe', 'One Piece', 'Attack on Titan', 'My Hero Academia', 'Naruto', 'Dragon Ball Z', 'Sailor Moon', 'Cowboy Bebop', 'Van Gogh', 'Warhol', 'Picasso', 'Da Vinci', 'Monet', 'Dali', 'Pollock', 'Rothko', 'Matisse', 'Banksy', 'Michelangelo', 'Kusama', 'Hokusai', "O'Keeffe", 'Cezanne', 'Hopper', 'Klimt', 'Chagall', 'Lichtenstein', 'Basquiat', 'Frida Kahlo', "Georgia O'Keeffe", 'Jackson Pollock', 'Rembrandt', 'Renoir', 'Magritte', 'Manet', 'Vermeer', 'Caravaggio', 'Rodin', 'Botticelli', 'Edward Hopper', 'Keith Haring', 'Damien Hirst', 'Yayoi Kusama', 'Francis Bacon', 'Ai Weiwei', 'Cindy Sherman', 'Frank Stella', 'Lucian Freud', 'Marc Chagall', 'Roy Lichtenstein', 'Thomas Kinkade', 'Joan Miro', 'Gerhard Richter', 'Wassily Kandinsky', 'Norman Rockwell', 'Bridget Riley', 'Piet Mondrian', 'Salvador Dali', 'Mary Cassatt', 'Diego Rivera', 'Jean-Michel Basquiat', 'Henry Moore', 'Frida Kahlo', 'Grant Wood', 'Edward Hopper', 'Andy Goldsworthy', 'Louise Bourgeois', 'Ansel Adams', 'Yoko Ono', 'Gustav Klimt', 'Jeff Koons', 'John Singer Sargent', 'Marcel Duchamp', 'Claude Monet', 'Anish Kapoor', 'Hieronymus Bosch', 'Paul Gauguin', 'Katsushika Hokusai', 'Pierre-Auguste Renoir', 'Antony Gormley', 'Kazimir Malevich', 'Jean-Antoine Watteau', 'Constantin Brancusi', 'Egon Schiele', 'Nam June Paik', 'James Whistler', 'Wassily Kandinsky', 'Lucio Fontana', 'Artemisia Gentileschi', 'Jean Dubuffet', 'Sandro Botticelli', 'Carl Andre', 'David Hockney', 'Cindy Sherman', 'Jenny Holzer', 'Dante Gabriel Rossetti', 'Zaha Hadid', 'Takashi Murakami', 'Edward Weston', 'Edvard Munch', 'Ai Weiwei', 'Georges Braque', 'Sol LeWitt', 'Mary Cassatt', 'Damien Hirst', 'Giuseppe Arcimboldo', 'Yves Klein', 'Frida Kahlo', 'Piet Mondrian', 'Bridget Riley', 'Mark Rothko', 'Joseph Beuys', 'Berthe Morisot', 'Agnes Martin', 'Yayoi Kusama', 'Andy Goldsworthy', 'Henri Cartier-Bresson', 'Marina Abramovic', 'Man Ray', 'Kathe Kollwitz', 'Robert Rauschenberg', 'Lyonel Feininger', 'Tracey Emin', 'Rene Magritte', 'Henry Moore', 'Rachel Whiteread', 'Tomma Abts', 'Max Ernst', 'Richard Serra', 'Ernst Ludwig Kirchner', 'Eva Hesse', 'Paul Cezanne', 'Francis Bacon', 'Louise Bourgeois', 'Chuck Close', 'Thomas Gainsborough', 'Gerhard Richter', 'Jean-Michel Basquiat', 'Alexander Calder', 'Jackson Pollock', 'Anselm Kiefer', 'Amedeo Modigliani', 'Gilbert & George', 'El Greco', 'Salvador Dali', 'Rembrandt van Rijn', 'Keith Haring', "Georgia O'Keeffe", 'Caravaggio', 'Louise Nevelson', 'James Turrell', 'Edouard Manet', 'Marc Chagall', 'Dan Flavin', 'Sarah Lucas', 'Johannes Vermeer', 'Tadao Ando', 'Roy Lichtenstein', 'Joseph Cornell', 'Gustave Courbet', 'Richard Long', 'Otto Dix', 'Barnett Newman', 'Sophie Calle', 'KAWS', 'Francis Picabia', 'H.R. Giger', 'Jean Arp', 'Ai Weiwei', 'Fernand Leger', 'Yoko Ono', 'Cindy Sherman', 'Nam June Paik', 'Barbara Kruger', 'Piero della Francesca', "Georgia O'Keeffe", 'Richard Hamilton', 'Kazimir Malevich', 'Grayson Perry', 'Faith Ringgold', 'Banksy', 'Tracey Emin', 'Olafur Eliasson', 'Kiki Smith', 'David Hockney', 'Chris Ofili', 'Ellsworth Kelly', 'Christo and Jeanne-Claude', 'Wayne Thiebaud', 'Jenny Holzer', 'Antony Gormley', 'Maurice Sendak', 'Portrait Photography Charismatic', 'Portrait Photography Cinematic', 'Portrait Photography Environmental', 'Photojournalism Reportage', 'Photojournalism Candid', 'Photojournalism Documentary', 'Fashion Photography Haute Couture', 'Fashion Photography Editorial', 'Fashion Photography Catalog', 'Sports Photography Action-packed', 'Sports Photography Emotional', 'Sports Photography Narrative', 'Still Life Photography Minimalistic', 'Still Life Photography Dramatic', 'Still Life Photography Rustic', 'Editorial Photography Investigative', 'Editorial Photography Lifestyle', 'Editorial Photography Opinion', 'Architectural Photography Historical', 'Architectural Photography Modernist', 'Architectural Photography Surreal', 'Steampunk-2', 'Futuristic', 'Abstract Expressionism', 'Surrealism', 'Watercolor-2', 'Pointillism', 'Cubism', 'Gothic', 'Pop Art', 'Impressionism', 'Street Art', 'Art Nouveau', 'Charcoal', 'Collage-2', 'Minimalist', 'Graffiti-2', "Trompe L'oeil", 'Fauvism', 'Hyperrealism', 'Dada', 'Calligraphy', 'Baroque', 'Op Art', 'Psychedelic', 'Scratchboard', 'Botanical Illustration', 'Lithography', 'Mosaic', 'Woodcut', 'Stencil Art', 'Rotoscoping', 'Glass Painting', 'Art Deco', 'Hard Edge Painting', 'Drybrush', 'Silhouette', 'Plein Air', 'Ink Wash', 'Body Painting', 'Spray Paint', 'Grisaille', 'Stippling', 'Pastel', 'Encaustic', 'Macrame', 'Graffiti Stencil', 'Action Painting', 'Batik', 'Folk Art', 'Glitch Art', 'Chiaroscuro', 'Gouache', 'High-Fashion', 'Casual-Chic', 'Streetwear', 'Athletic', 'Vintage', 'Bohemian', 'Minimalist', 'Preppy', 'Gothic', 'Punk', 'Grunge-2', 'Glamorous', 'Rocker', 'Hipster', 'Ethical', 'Business Casual', 'Beachwear', 'Activewear', 'Country', 'Military', 'Kawaii', 'Lolita', 'Formal', 'Tomboy', 'Normcore', 'Artistic', 'Genderless', 'Monochromatic', 'Mod', 'Harajuku', 'Cyberpunk', 'Rave', 'Hippy', 'Skater', 'Pin-Up', 'Nautical-2', 'Futuristic', 'Eccentric', 'Tailored', 'Sustainable', 'Traditional', 'Candid', 'Portrait', 'Lifestyle', 'Editorial', 'Glamour', 'Fitness', 'Boudoir', 'Silhouette', 'Maternity', 'Black and White', 'Pin-Up', 'Headshot', 'Full Body', 'High Fashion', 'Business', 'Beach', 'Lingerie', 'Athletic', 'Close-up', 'Nature', 'Studio', 'Street', 'Dance', 'Vintage', 'Low Light', 'Underwater', 'Action', 'Fashion', 'Aerial', 'Music', 'Abstract', 'Fine Art', 'Cityscape', 'Landscape', 'Macro', 'Golden Hour', 'Blue Hour', 'Night', 'Reflection', 'Backlit', 'Overhead', 'Watercolor', 'Film Noir', 'Neon', 'Jungle', 'Mars', 'Vibrant Color', 'Snow', 'Line art', 'Movie Stills', '3D Model', 'Analog Film', 'Anime', 'Comic Book', 'Fantasy Art', 'Artstyle Abstract', 'Artstyle Abstract', 'Artstyle Abstract Expressionism', 'Artstyle Abstract Expressionism', 'Artstyle Abstract Expressionism', 'Artstyle Abstract Expressionism', 'Artstyle Abstract Expressionism', 'Artstyle Abstract Expressionism', 'Artstyle Watercolor', 'Artstyle Watercolor', 'Game Gta', 'Game Retro Game', 'Artstyle Art Deco']

models = ['zavychromaxl_v60.safetensors',
'realmixXL_v10.safetensors','copaxTimelessxlSDXL1_v12.safetensors','cyberrealisticXL_v21.safetensors','albedobaseXL_v21','cartoonArcadiaSDXLSD1_v2.safetensors','leosamsHelloworldXL_helloworldXL70.safetensors','omnium_v11.safetensors','dynavisionXLAllInOneStylized_releaseV0610Bakedvae.safetensors','duchaitenAiartSDXL_v33515.safetensors','bluePencilXL_v600.safetensors' ]

apis = ['http://103.95.97.14:8023/api/generate-text2video','https://jwll7srr8e4bxm-8000.proxy.runpod.net/api/generate-text2video']

def request(api,model, prompt, neg_prompt, style_name, guidance_scale,
             seed, sampler, scheduler, steps, num_of_images, width, height):
    delete_all_files('/media/mlpc2/workspace/sagor/ML_Gradio/output')
    create_json(model, prompt, neg_prompt, style_name, guidance_scale, seed, sampler, scheduler, steps, num_of_images, width, height)
    with open('test_json.json', 'rb') as file:
        files = {'json_data': ('test_json.json', file, 'application/json')}

        response = requests.post(api, headers={
            'accept': 'application/json',
        }, files=files)
        print(response.content)
        if response.status_code == 200:
            print("Request Successfull")
            with io.BytesIO(response.content) as zip_file:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall('output')
            print("ZIP file extracted successfully!")         
        else:
            print('Request failed.')
    outputs = load_images_from_folder('/media/mlpc2/workspace/sagor/ML_Gradio/output')
    return gr.Gallery(outputs)

def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            images.append(img)
    return images


def delete_all_files(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError(f"The path {folder_path} is not a directory or does not exist.")
    
    # Construct a pattern to match all files
    pattern = os.path.join(folder_path, '*')
    
    # Get all files in the folder
    files = glob.glob(pattern)
    
    for file in files:
        try:
            if os.path.isfile(file):
                os.remove(file)
                print(f"Deleted file: {file}")
            else:
                print(f"Skipped non-file: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")


def create_json(model,prompt,neg_prompt,style_name,guidance_scale, seed, 
                sampler, scheduler, steps, num_of_images, width, height):
    try:
        seed = int(seed)
    except ValueError as e:
        seed = -1
        print("String to integer conversion failed")


    data = {
        "model" : model,
        "prompt" : prompt,
        "neg_prompt" : neg_prompt,
        "style_name" : style_name,
        "guidance_scale" : guidance_scale,
        "seed" : seed,
        "sampler" : sampler,
        "scheduler" : scheduler,
        "steps" : steps,
        "num_of_images" : num_of_images,
        "width" : width,
        "height" : height
    }
    with open("test_json.json", "w") as json_file:
        json.dump(data,json_file,indent=4)
    print("json written successfully")    

    


with gr.Blocks() as demo:
    gr.Markdown("Happy Testing!")
    with gr.Row():
        with gr.Column():
            request_url = gr.Dropdown(apis, value="https://jwll7srr8e4bxm-8000.proxy.runpod.net/api/generate-text2video", interactive= True, label="API")
            model = gr.Dropdown( models, label= 'Model',value="copaxTimelessxlSDXL1_v12.safetensors",interactive=True)
            prompt = gr.Text(label='Prompt',value="a man",interactive=True)
            neg_prompt = gr.Text(label='Negative Prompt',value="",interactive=True)
            style_name = gr.Dropdown(styles,label="Style Name",value="(No style)")
            guidance_scale = gr.Slider(minimum= 1,maximum = 30, step=0.1,value= 7.5,label="Guidance Scale", interactive=True)
            seed = gr.Text(label= "seed",value= -1 ,interactive=True)
            sampler = gr.Dropdown(["euler", "euler_ancestral", "heun", "heunpp2","dpm_2", "dpm_2_ancestral", "lms", "dpm_fast", "dpm_adaptive", "dpmpp_2s_ancestral", "dpmpp_sde", "dpmpp_sde_gpu", "dpmpp_2m", "dpmpp_2m_sde", "dpmpp_2m_sde_gpu", "dpmpp_3m_sde", "dpmpp_3m_sde_gpu", "ddpm", "lcm", "ddim", "uni_pc", "uni_pc_bh2"],
                                label="Sampler",value="dpmpp_2m_sde",interactive=True)
            scheduler = gr.Dropdown(["normal", "karras", "exponential", "sgm_uniform", "simple", "ddim_uniform"],
                                    label="Scheduler",value="karras",interactive=True)
            steps = gr.Slider(10, 50, step=1,label="Steps",value = 30, interactive=True)
            num_of_images = gr.Slider(1, 16, step=1,label="Number of Images",value = 1, interactive=True)
            width = gr.Slider(512,1536,step = 16,label="Width",value=1024 ,interactive=True)
            height = gr.Slider(512,1536,step = 16, label="Height",value = 1024, interactive=True)
        with gr.Column():
            gallary = gr.Gallery() 
            # output = gr.Text()  

            submit = gr.Button("Submit")
            submit.click(
                request,
                inputs = [request_url,model, prompt, neg_prompt, style_name, guidance_scale, seed, sampler, scheduler, steps, num_of_images, width, height],
                outputs= gallary
            )



    


demo.launch(share=True)