import os
import io

from typing import List
from PIL import Image, ImageFont, ImageDraw, ImageCms

from layers import Layers


class PostGenerator:

    def __init__(self, images_path: str):
        self.layers: List[Layers] = self.load_image_layes(images_path)

    def load_image_layes(self, images_path: str):
        sub_paths = sorted(os.listdir(images_path))
        layers = []
        for sub_path in sub_paths:
            layer_path = os.path.join(images_path, sub_path)
            layer = Layers(layer_path)
            layers.append(layer)
        return layers

    def genetate_image_sequence(self):
        image_path_sequence = []
        for layer in self.layers:
            image_path = layer.get_image_path()
            image_path_sequence.append(image_path)

        return image_path_sequence

    def render_post_image(self, image_path_sequence: List[str]):
        post = Image.new('RGBA', (1080, 1920), (120, 12, 12))
        for image_path in image_path_sequence:
            if 'main' in image_path:
                post.paste(self.edit_main_ptoho(image_path), (115, 272))
            else:
                layer_image = Image.open(image_path)
                post = Image.alpha_composite(post, layer_image)
        return post

    def render_post_image_with_text(self, post: List[str]):
        font = ImageFont.truetype('../templates/template_instagram_story/fonts/BebasNeue-Regular.ttf', size=240)
        draw_text = ImageDraw.Draw(post)
        draw_text.text(
            (300, 1050),
            'FOALS',
            # Добавляем шрифт к изображению
            font=font,
            fill='#1C0606')
        return post

    def edit_main_ptoho(self, main_path):
        main_photo = Image.open(main_path)
        # cropped.save('./templates/template_instagram_story/layers/6_main_ptoho/cropped_main_photo.png')
        center_main_photo_x, center_main_photo_y = self.get_center_photo(main_photo)
        cropped = main_photo.crop((center_main_photo_x - 435, center_main_photo_y - 435, center_main_photo_x + 435,
                                   center_main_photo_y + 435))
        new_cropped = cropped.convert("RGBA")
        try:
            src_profile = ImageCms.getOpenProfile(io.BytesIO(new_cropped.info['icc_profile']))
            dst_profile = ImageCms.createProfile('sRGB')
            new_cropped = ImageCms.profileToProfile(new_cropped, src_profile, dst_profile)
        except KeyError:
            pass
        return new_cropped

    def get_center_photo(self, main_photo):
        weight, height = main_photo.size
        return (int(weight / 2), int(height / 2))

    def generate_post(self):
        # print('Generating Post!')
        image_path_sequence = self.genetate_image_sequence()
        post = self.render_post_image(image_path_sequence)
        post = self.render_post_image_with_text(post)
        post.show()
        # print(image_path_sequence)