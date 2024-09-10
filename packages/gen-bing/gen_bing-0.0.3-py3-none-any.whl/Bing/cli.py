import argparse
import asyncio

from Bing import AsyncImageGenerator


def cli_cmd():
    parser = argparse.ArgumentParser(
        prog="Bing Create",
        description="A simple lightweight AI Image Generator from text description using Bing Image Creator (DALL-E 3)",
        epilog="Made by Waenara ^^",
    )

    parser.add_argument(
        "--u", help="Your _U cookie from https://bing.com/", required=True
    )

    parser.add_argument(
        "--s", help="Your SRCHHPGUSR cookie from https://bing.com/", required=True
    )

    parser.add_argument(
        "--prompt", help="Description of image to generate", required=True
    )

    parser.add_argument(
        "--number", help="How many images to generate. Default: 4", type=int, default=4
    )

    parser.add_argument(
        "--output",
        help="Directory where to save generated images. If not specified you will just get links printed out",
    )

    parser.add_argument(
        "--quiet", help="If present logging is disabled", action="store_true"
    )

    args = parser.parse_args()
    generator = AsyncImageGenerator(
        auth_cookie_u=args.u,
        auth_cookie_srchhpgusr=args.s,
        logging_enabled=not args.quiet,
    )

    async def main():
        images = await generator.generate(prompt=args.prompt, num_images=args.number)
        if args.output:
            await generator.save(images=images, output_dir=args.output)
        else:
            print("\n".join(images))

    asyncio.run(main())
