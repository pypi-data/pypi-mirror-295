import asyncio
import logging
import os
import re
import time

import aiofiles
import httpx


class ImageGenerator:
    """
    Synchronous AI Image Creator by Microsoft Bing Image Creator (https://bing.com/images/create/).
    :param auth_cookie_u: Your https://bing.com/ _U auth cookie.
    :param auth_cookie_srchhpgusr: Your https://bing.com/ SRCHHPGUSR auth cookie.
    :param logging_enabled: Identifies whether logging is enabled or not.
    """

    def __init__(
        self,
        auth_cookie_u: str,
        auth_cookie_srchhpgusr: str,
        logging_enabled: bool = True,
    ):
        self.client = httpx.Client(
            cookies={"_U": auth_cookie_u, "SRCHHPGUSR": auth_cookie_srchhpgusr}
        )

        self.logging_enabled = logging_enabled
        if logging_enabled:
            logging.basicConfig(level=logging.INFO)

    def __log(self, message: str):
        if self.logging_enabled:
            logging.info(message)

    def generate(self, prompt: str, num_images: int) -> list:
        """
        Generates AI images from a prompt.
        :param prompt: Description of image you want to generate.
        :param num_images: Number of images to generate.
        :return: List of generated image URLs.
        """
        images = []
        cycle = 0
        start = time.time()

        while len(images) < num_images:
            cycle += 1

            response = self.client.post(
                url=f"https://www.bing.com/images/create?q={prompt}&rt=3&FORM=GENCRE",
                data={"q": prompt, "qs": "ds"},
                follow_redirects=False,
                timeout=200,
            )

            if response.status_code != 302:
                raise Exception("🛑 Request to https://bing.com/ failed! (Redirect)")

            self.__log(f"✅ Request to https://bing.com/ sent! (cycle: {cycle})")

            if "being reviewed" in response.text or "has been blocked" in response.text:
                raise Exception("🛑 Prompt is being reviewed or blocked!")
            if "image creator in more languages" in response.text:
                raise Exception("🛑 Language is not supported by Bing yet!")

            result_id = (
                response.headers["Location"].replace("&nfy=1", "").split("id=")[-1]
            )
            results_url = f"https://www.bing.com/images/create/async/results/{result_id}?q={prompt}"

            self.__log(f"🕗 Awaiting generation... (cycle: {cycle})")
            start_time = time.time()
            while True:
                response = self.client.get(results_url)

                if time.time() - start_time > 200:
                    raise Exception("🛑 Waiting for results timed out!")

                if response.status_code != 200:
                    raise Exception(
                        "🛑 Exception happened while waiting for image generation! (NoResults)"
                    )

                if "errorMessage" in response.text:
                    time.sleep(1)
                    continue
                else:
                    break

            new_images = [
                "https://tse" + link.split("?w=")[0]
                for link in re.findall('src="https://tse([^"]+)"', response.text)
            ]
            if not new_images:
                raise Exception(
                    "🛑 No new images were generated for this cycle, please check your prompt"
                )
            images.extend(new_images)
            self.__log(
                f"✅ Successfully finished cycle {cycle} in {round(time.time() - start_time, 2)} seconds"
            )

        self.__log(
            f"✅ Finished generating {num_images} images in {round(time.time() - start, 2)} seconds and {cycle} cycles"
        )
        return images[:num_images]

    def save(self, images: list, output_dir: str) -> None:
        """
        Saves generated images to a folder.
        :param images: List of generated image URLs.
        :param output_dir: Directory where to save generated images.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for image_url in images:
            response = self.client.get(image_url)
            if response.status_code != 200:
                raise Exception(
                    "🛑 Exception happened while saving image! (Response was not ok)"
                )

            filename = f"{image_url.split('/id/')[1]}.jpeg"
            with open(os.path.join(output_dir, filename), "wb") as f:
                f.write(response.content)

            self.__log(f"✅ Saved image {filename}!")


class AsyncImageGenerator:
    def __init__(
        self,
        auth_cookie_u: str,
        auth_cookie_srchhpgusr: str,
        logging_enabled: bool = True,
    ):
        self.cookies = {"_U": auth_cookie_u, "SRCHHPGUSR": auth_cookie_srchhpgusr}
        self.logging_enabled = logging_enabled
        if logging_enabled:
            logging.basicConfig(level=logging.INFO)

    def __log(self, message: str):
        if self.logging_enabled:
            logging.info(message)

    async def generate(self, prompt: str, num_images: int) -> list:
        images = []
        cycle = 0
        start = time.time()

        async with httpx.AsyncClient(cookies=self.cookies) as client:
            while len(images) < num_images:
                cycle += 1

                response = await client.post(
                    url=f"https://www.bing.com/images/create?q={prompt}&rt=3&FORM=GENCRE",
                    data={"q": prompt, "qs": "ds"},
                    follow_redirects=False,
                    timeout=20,
                )

                if response.status_code != 302:
                    raise Exception(
                        "🛑 Request to https://bing.com/ failed! (Redirect)"
                    )

                self.__log(f"✅ Request to https://bing.com/ sent! (cycle: {cycle})")

                result_id = (
                    response.headers["Location"].replace("&nfy=1", "").split("id=")[-1]
                )
                results_url = f"https://www.bing.com/images/create/async/results/{result_id}?q={prompt}"

                self.__log(f"🕗 Awaiting generation... (cycle: {cycle})")
                start_time = time.time()

                while True:
                    response = await client.get(results_url, timeout=20)

                    if time.time() - start_time > 200:
                        raise Exception("🛑 Waiting for results timed out!")

                    if response.status_code != 200:
                        raise Exception(
                            "🛑 Exception happened while waiting for image generation! (NoResults)"
                        )

                    if "errorMessage" in response.text:
                        await asyncio.sleep(1)
                        continue
                    else:
                        break

                new_images = [
                    "https://tse" + link.split("?w=")[0]
                    for link in re.findall('src="https://tse([^"]+)"', response.text)
                ]
                if not new_images:
                    raise Exception(
                        "🛑 No new images were generated for this cycle, please check your prompt"
                    )
                images_to_add = new_images[: num_images - len(images)]
                images.extend(images_to_add)
                self.__log(
                    f"✅ Successfully finished cycle {cycle} in {round(time.time() - start_time, 2)} seconds"
                )
                if len(images) >= num_images:
                    break

        self.__log(
            f"✅ Finished generating {num_images} images in {round(time.time() - start, 2)} seconds and {cycle} cycles"
        )
        return images[:num_images]

    async def save(self, images: list, output_dir: str) -> None:
        """
        Saves generated images to a folder.
        :param images: List of generated image URLs.
        :param output_dir: Directory where to save generated images.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for image_url in images:
            response = await self.client.get(image_url)
            if response.status_code != 200:
                raise Exception(
                    "🛑 Exception happened while saving image! (Response was not ok)"
                )

            filename = f"{image_url.split('/id/')[1]}.jpeg"
            async with aiofiles.open(os.path.join(output_dir, filename), "wb") as f:
                await f.write(response.content)

            self.__log(f"✅ Saved image {filename}!")
