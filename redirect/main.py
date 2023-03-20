from fastapi import APIRouter

router = APIRouter()


@router.get("/discord",
         response_class=RedirectResponse,
         tags=[Tags.user, Tags.redirect],
         summary="redirect to discord",
         description="redirect to the rock-paper-scissor-api server",
         response_description="discord server invite URl redirect")
async def discord():
    return "https://discord.gg/v9D5VD4Rfp"


@router.get("/youtube",
         response_class=RedirectResponse,
         tags=[Tags.user, Tags.redirect],
         summary="redirect to youtube",
         description="redirect to the youtube channel",
         response_description="youtube URL redirect")
async def youtube():
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

