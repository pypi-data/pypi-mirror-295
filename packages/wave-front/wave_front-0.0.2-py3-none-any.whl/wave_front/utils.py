from h2o_wave import Q

from .ui.card import batch_rebuild, Card


async def redirect_to(q: Q, path: str, rebuild_cards: list[Card] = None):
    q.page['meta'].redirect = path

    if rebuild_cards is not None:
        await batch_rebuild(
            q,
            cards=rebuild_cards,
        )

    await q.page.save()


async def skip_loading(q: Q):
    q.page['non-existent'].items = []
    await q.page.save()
