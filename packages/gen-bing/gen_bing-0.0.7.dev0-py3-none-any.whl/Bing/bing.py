import asyncio
import logging
import os
import re
import time

import aiofiles
import httpx



auth_cookie_u = "1znUiBiMtLmyiXgXVPbk6Aietr-_bXBJhLkXfqtrnHNlYejrAYeQamC02GAAFBGwvQ-cYfECQ6EJhb9V2irRjvCn2Of7jBaeNFWqReW83DWGMPDcbcyGihyr6Y1kpxSmNV_caQ1Y0iEFJGDp1yKlKUIPZpwoZ8ytiXlxMFzO2845WCGUVTo5GC35BnopTjxZv60mu7AVsPQhqz6tnW84oHA"


auth_cookie_srchhpgusr = "SRCHLANG=en&IG=70E28E77573A481A9E846CD2A2BD9914&DM=0&BRW=M&BRH=S&CW=1280&CH=585&SCW=1280&SCH=585&DPR=1.5&UTC=420&THEME=0&WEBTHEME=0&PV=15.0.0&WTS=63861286846&HV=1725690251&PRVCW=1036&PRVCH=558"



class ImageGenerator:
    def __init__(self, auth_cookie_u: str, auth_cookie_srchhpgusr: str, logging_enabled: bool = True):
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
        images = []
        cycle = 0
        start = time.time()

        while len(images) < num_images:
            cycle += 1

            try:
                response = self.client.post(
                    url=f"https://www.bing.com/images/create?q={prompt}&rt=3&FORM=GENCRE",
                    data={"q": prompt, "qs": "ds"},
                    follow_redirects=False,
                    timeout=20,
                )
                response.raise_for_status()
            except httpx.RequestError as e:
                raise Exception(f"🛑 Request failed: {e}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"🛑 HTTP error occurred: {e}")

            if response.status_code != 302:
                raise Exception("🛑 Request to https://bing.com/ failed! (Redirect)")

            self.__log(f"✅ Request to https://bing.com/ sent! (cycle: {cycle})")

            result_id = response.headers["Location"].replace("&nfy=1", "").split("id=")[-1]
            results_url = f"https://www.bing.com/images/create/async/results/{result_id}?q={prompt}"

            self.__log(f"🕗 Awaiting generation... (cycle: {cycle})")
            start_time = time.time()

            while True:
                try:
                    response = self.client.get(results_url, timeout=20)
                    response.raise_for_status()
                except httpx.RequestError as e:
                    raise Exception(f"🛑 Request failed: {e}")
                except httpx.HTTPStatusError as e:
                    raise Exception(f"🛑 HTTP error occurred: {e}")

                if time.time() - start_time > 200:
                    raise Exception("🛑 Waiting for results timed out!")

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
                raise Exception("🛑 No new images were generated for this cycle, please check your prompt")

            images.extend(new_images)
            self.__log(f"✅ Successfully finished cycle {cycle} in {round(time.time() - start_time, 2)} seconds")

        self.__log(f"✅ Finished generating {num_images} images in {round(time.time() - start, 2)} seconds and {cycle} cycles")
        return images[:num_images]

    def save(self, images: list, output_dir: str) -> None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for image_url in images:
            try:
                response = self.client.get(image_url)
                response.raise_for_status()
            except httpx.RequestError as e:
                raise Exception(f"🛑 Request failed: {e}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"🛑 HTTP error occurred: {e}")

            filename = f"{image_url.split('/id/')[1]}.jpeg"
            with open(os.path.join(output_dir, filename), "wb") as f:
                f.write(response.content)

            self.__log(f"✅ Saved image {filename}!")


class AsyncImageGenerator:
    def __init__(self, auth_cookie_u: str, auth_cookie_srchhpgusr: str, logging_enabled: bool = True):
        self.client = httpx.AsyncClient(
            cookies={"_U": auth_cookie_u, "SRCHHPGUSR": auth_cookie_srchhpgusr}
        )
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

        while len(images) < num_images:
            cycle += 1

            try:
                response = await self.client.post(
                    url=f"https://www.bing.com/images/create?q={prompt}&rt=3&FORM=GENCRE",
                    data={"q": prompt, "qs": "ds"},
                    follow_redirects=False,
                    timeout=20,
                )
                response.raise_for_status()
            except httpx.RequestError as e:
                raise Exception(f"🛑 Request failed: {e}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"🛑 HTTP error occurred: {e}")

            if response.status_code != 302:
                raise Exception("🛑 Request to https://bing.com/ failed! (Redirect)")

            self.__log(f"✅ Request to https://bing.com/ sent! (cycle: {cycle})")

            result_id = response.headers["Location"].replace("&nfy=1", "").split("id=")[-1]
            results_url = f"https://www.bing.com/images/create/async/results/{result_id}?q={prompt}"

            self.__log(f"🕗 Awaiting generation... (cycle: {cycle})")
            start_time = time.time()

            while True:
                try:
                    response = await self.client.get(results_url, timeout=20)
                    response.raise_for_status()
                except httpx.RequestError as e:
                    raise Exception(f"🛑 Request failed: {e}")
                except httpx.HTTPStatusError as e:
                    raise Exception(f"🛑 HTTP error occurred: {e}")

                if time.time() - start_time > 200:
                    raise Exception("🛑 Waiting for results timed out!")

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
                raise Exception("🛑 No new images were generated for this cycle, please check your prompt")

            images_to_add = new_images[: num_images - len(images)]
            images.extend(images_to_add)
            self.__log(f"✅ Successfully finished cycle {cycle} in {round(time.time() - start_time, 2)} seconds")

            if len(images) >= num_images:
                break

        self.__log(f"✅ Finished generating {num_images} images in {round(time.time() - start, 2)} seconds and {cycle} cycles")
        return images[:num_images]

    async def save(self, images: list, output_dir: str) -> None:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for image_url in images:
            try:
                response = await self.client.get(image_url)
                response.raise_for_status()
            except httpx.RequestError as e:
                raise Exception(f"🛑 Request failed: {e}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"🛑 HTTP error occurred: {e}")

            filename = f"{image_url.split('/id/')[1]}.jpeg"
            async with aiofiles.open(os.path.join(output_dir, filename), "wb") as f:
                await f.write(response.content)

            self.__log(f"✅ Saved image {filename}!")
