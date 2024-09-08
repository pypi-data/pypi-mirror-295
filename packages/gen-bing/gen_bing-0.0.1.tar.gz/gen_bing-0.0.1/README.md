# Gen Bing

A Python library for generating and saving images using Bing's Image Creator.

## Installation

```bash
pip install gen-bing

from Bing.bing import AsyncImageGenerator

async def main():
    generator = AsyncImageGenerator(auth_cookie_u="YOUR_U_COOKIE", auth_cookie_srchhpgusr="YOUR_SRPCHPGUSR_COOKIE")
    images = await generator.generate_images(prompt="beautiful landscape", num_images=5)
    await generator.save_images(images, output_dir="images/")

import asyncio
asyncio.run(main())


from Bing.bing import SyncImageGenerator

generator = SyncImageGenerator(auth_cookie_u="YOUR_U_COOKIE", auth_cookie_srchhpgusr="YOUR_SRPCHPGUSR_COOKIE")
images = generator.generate_images(prompt="beautiful landscape", num_images=5)
generator.save_images(images, output_dir="images/")
```