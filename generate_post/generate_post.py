from post_generator import PostGenerator

def generate_post():
    generator = PostGenerator('../templates/template_instagram_story/layers')
    generator.generate_post()


if __name__ == '__main__':
    generate_post()