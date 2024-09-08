import asyncio
import logging
import os
import re
import time

import aiofiles
import aiohttp
import requests


class ImageGenerator:
    def __init__(
        self,
        auth_cookie_u: str,
        auth_cookie_srchhpgusr: str,
        logging_enabled: bool = True,
    ):
        self.auth_cookie_u = auth_cookie_u
        self.auth_cookie_srchhpgusr = auth_cookie_srchhpgusr
        self.logging_enabled = logging_enabled

        if logging_enabled:
            logging.basicConfig(level=logging.INFO)

    def __log(self, message: str):
        if self.logging_enabled:
            logging.info(message)

    def generate(self, prompt: str, num_images: int) -> list:
        images = []
        cycle = 0
        start = time.time()

        while len(images) < num_images:
            cycle += 1

            response = requests.post(
                url=f"https://www.bing.com/images/create?q={prompt}&rt=3&FORM=GENCRE",
                data={"q": prompt, "qs": "ds"},
                cookies={
                    "_U": self.auth_cookie_u,
                    "SRCHHPGUSR": self.auth_cookie_srchhpgusr,
                },
                allow_redirects=False,
                timeout=200,
            )

            if response.status_code != 302:
                raise Exception("Request to Bing failed! (Redirect)")

            self.__log(f"Request to Bing sent! (cycle: {cycle})")

            if "being reviewed" in response.text or "has been blocked" in response.text:
                raise Exception("Prompt is being reviewed or blocked!")
            if "image creator in more languages" in response.text:
                raise Exception("Language is not supported by Bing yet!")

            result_id = (
                response.headers["Location"].replace("&nfy=1", "").split("id=")[-1]
            )
            results_url = f"https://www.bing.com/images/create/async/results/{result_id}?q={prompt}"

            self.__log(f"Awaiting generation... (cycle: {cycle})")
            start_time = time.time()
            while True:
                response = requests.get(
                    results_url,
                    cookies={
                        "_U": self.auth_cookie_u,
                        "SRCHHPGUSR": self.auth_cookie_srchhpgusr,
                    },
                )

                if time.time() - start_time > 200:
                    raise Exception("Waiting for results timed out!")

                if response.status_code != 200:
                    raise Exception(
                        "Exception happened while waiting for image generation! (NoResults)"
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
                    "No new images were generated for this cycle, please check your prompt"
                )
            images.extend(new_images)
            self.__log(
                f"Successfully finished cycle {cycle} in {round(time.time() - start_time, 2)} seconds"
            )

        self.__log(
            f"Finished generating {num_images} images in {round(time.time() - start, 2)} seconds and {cycle} cycles"
        )
        return images[:num_images]

    def save(self, images: list, output_dir: str) -> None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for image_url in images:
            response = requests.get(image_url)
            if response.status_code == 200:
                filename = f"{image_url.split('/')[-1]}"
                with open(os.path.join(output_dir, filename), "wb") as f:
                    f.write(response.content)


class AsyncImageGenerator:
    def __init__(
        self,
        auth_cookie_u: str,
        auth_cookie_srchhpgusr: str,
        logging_enabled: bool = True,
    ):
        self.auth_cookie_u = auth_cookie_u
        self.auth_cookie_srchhpgusr = auth_cookie_srchhpgusr
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

        async with aiohttp.ClientSession(
            cookies={
                "_U": self.auth_cookie_u,
                "SRCHHPGUSR": self.auth_cookie_srchhpgusr,
            }
        ) as session:
            while len(images) < num_images:
                cycle += 1

                async with session.post(
                    url=f"https://www.bing.com/images/create?q={prompt}&rt=3&FORM=GENCRE",
                    data={"q": prompt, "qs": "ds"},
                    allow_redirects=False,
                    timeout=200,
                ) as response:

                    if response.status != 302:
                        raise Exception("Request to Bing failed! (Redirect)")

                    self.__log(f"Request to Bing sent! (cycle: {cycle})")

                    response_text = await response.text()
                    if (
                        "being reviewed" in response_text
                        or "has been blocked" in response_text
                    ):
                        raise Exception("Prompt is being reviewed or blocked!")
                    if "image creator in more languages" in response_text:
                        raise Exception("Language is not supported by Bing yet!")

                    result_id = (
                        response.headers["Location"]
                        .replace("&nfy=1", "")
                        .split("id=")[-1]
                    )
                    results_url = f"https://www.bing.com/images/create/async/results/{result_id}?q={prompt}"

                    self.__log(f"Awaiting generation... (cycle: {cycle})")
                    start_time = time.time()
                    while True:
                        async with session.get(results_url) as response:

                            if time.time() - start_time > 200:
                                raise Exception("Waiting for results timed out!")

                            if response.status != 200:
                                raise Exception(
                                    "Exception happened while waiting for image generation! (NoResults)"
                                )

                            response_text = await response.text()
                            if "errorMessage" in response_text:
                                await asyncio.sleep(1)
                                continue
                            else:
                                break

                    new_images = [
                        "https://tse" + link.split("?w=")[0]
                        for link in re.findall(
                            'src="https://tse([^"]+)"', response_text
                        )
                    ]
                    if not new_images:
                        raise Exception(
                            "No new images were generated for this cycle, please check your prompt"
                        )
                    images.extend(new_images)
                    self.__log(
                        f"Successfully finished cycle {cycle} in {round(time.time() - start_time, 2)} seconds"
                    )

        self.__log(
            f"Finished generating {num_images} images in {round(time.time() - start, 2)} seconds and {cycle} cycles"
        )
        return images[:num_images]

    async def save(self, images: list, output_dir: str) -> None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        async with aiohttp.ClientSession() as session:
            for image_url in images:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        filename = f"{image_url.split('/')[-1]}"
                        async with aiofiles.open(
                            os.path.join(output_dir, filename), "wb"
                        ) as f:
                            await f.write(await response.read())
                        self.__log(f"Saved image {filename}!")
