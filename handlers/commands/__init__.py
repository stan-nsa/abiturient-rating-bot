from aiogram import Router
from .main_commands import router as main_commands


router = Router()
router.include_router(main_commands)
