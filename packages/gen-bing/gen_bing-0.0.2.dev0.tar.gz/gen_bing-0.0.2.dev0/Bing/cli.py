import argparse
import asyncio

from Bing.bing import AsyncImageGenerator


def cli_cmd():
    parser = argparse.ArgumentParser(
        description="Generate images using Bing.\n\nCreated by LuciferReborns"
    )
    parser.add_argument("prompt", help="Prompt for image generation")
    parser.add_argument("num_images", type=int, help="Number of images to generate")
    parser.add_argument("output_dir", help="Directory to save the generated images")
    parser.add_argument(
        "--auth-cookie-u", required=True, help="Authentication cookie U"
    )
    parser.add_argument(
        "--auth-cookie-srchhpgusr",
        required=True,
        help="Authentication cookie SRCHHPGUSR",
    )
    args = parser.parse_args()

    generator = AsyncImageGenerator(
        auth_cookie_u=args.auth_cookie_u,
        auth_cookie_srchhpgusr=args.auth_cookie_srchhpgusr,
    )

    print(f"Generating {args.num_images} images for prompt: '{args.prompt}'")
    images = asyncio.run(generator.generate(args.prompt, args.num_images))
    generator.save(images, args.output_dir)
    print(f"Images saved to {args.output_dir}")


if __name__ == "__main__":
    cli_cmd()
