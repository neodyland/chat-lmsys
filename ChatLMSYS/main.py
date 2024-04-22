import asyncio
import nodriver
import aiohttp
import secrets
import json

from enums import (
    Model,
)


class CloudflareException(Exception):
    pass


class ChatLMSYS:
    def __init__(self) -> None:
        self.base_url = "https://chat.lmsys.org"
        self.user_agent, self.cf_clearance = asyncio.run(self.solve_cf_clearance())

    async def solve_cf_clearance(self) -> tuple[str, str]:
        browser = await nodriver.start()
        tab = await browser.get(self.base_url)
        user_agent = str(await tab.evaluate("navigator.userAgent"))
        # await tab.verify_cf()
        # TODO: Implement the verification of the cf_clearance cookie
        await tab.sleep(3)
        for cookie in await browser.cookies.get_all():
            if cookie.name == "cf_clearance":
                return user_agent, cookie.value
        raise CloudflareException("cf_clearance cookie not found")

    async def ask(
        self, model: Model, prompt: str, session_hash: str | None = None
    ) -> str:
        session_hash = session_hash or secrets.token_hex(6)
        headears = {
            "user-agent": self.user_agent,
        }
        cookies = {
            "cf_clearance": self.cf_clearance,
        }
        async with aiohttp.ClientSession(
            base_url=self.base_url,
            cookies=cookies,
            headers=headears,
            raise_for_status=True,
        ) as session:
            json_data = {
                "data": [
                    None,
                    model.value,
                    prompt,
                    None,
                ],
                "event_data": None,
                "fn_index": 41,
                "trigger_id": 93,
                "session_hash": session_hash,
            }
            await session.post("/queue/join", json=json_data)
            params = {
                "session_hash": session_hash,
            }
            await session.get("/queue/data", params=params)
            json_data = {
                "data": [
                    None,
                    0.7,
                    1,
                    1024,
                ],
                "event_data": None,
                "fn_index": 42,
                "trigger_id": 93,
                "session_hash": session_hash,
            }
            await session.post("/queue/join", json=json_data)
            async with session.get("/queue/data", params=params) as response:
                result = json.loads((await response.text()).strip().split("\n")[-1][5:])
        return result["output"]["data"][1][0][1]


if __name__ == "__main__":
    chat = ChatLMSYS()

    async def main():
        result = await chat.ask(
            Model.LLAMA_3_70B_INSTRUCT, "PythonでHello, World!を出力してください。"
        )
        print(result)

    asyncio.run(main())
