# Auto Youtube lib


## How to run:
```
from youtube_auto_publish import AutoYoutube
from asyncio import run

async def test():
    video_was_send: bool = False
    number_or_tries: int = 0

    while not video_was_send:
        with AutoYoutube("youtube_username", "youtube_password", "chromedriver_executable_path") as browser:
            await browser.login()
            video_was_send = await browser.post_video(
                channel_name="top5twitchDesenv",
                video_path="/path/video name.mp4",
                video_description="this is a video description",
                tags=["#overwatch","#pvp"],
                age_restriction=True,
            )
        number_or_tries += 1

        if video_was_send or number_or_tries >= 5:
            break



if __name__ == "__main__":
    run(test())
```