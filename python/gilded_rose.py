# -*- coding: utf-8 -*-

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"
CONJURED_PREFIX = "Conjured"

MIN_QUALITY = 0
MAX_QUALITY = 50


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater_for(item).update(item)


class ItemUpdater:
    """End-of-day rules for an ordinary item.

    Subclasses override only the part that differs for their category. Quality
    is assumed to start within [MIN_QUALITY, MAX_QUALITY] as the requirements
    state; it is clamped to that range after every change.
    """

    def update(self, item):
        self._change_quality(item, self._quality_delta(item))
        item.sell_in -= 1

    def _quality_delta(self, item):
        return -2 if self._sell_by_date_passed(item) else -1

    @staticmethod
    def _sell_by_date_passed(item):
        # sell_in is the number of days left to sell, so on the day it reaches
        # 0 the item goes past its sell-by date as this update runs.
        return item.sell_in <= 0

    @staticmethod
    def _change_quality(item, delta):
        item.quality = max(MIN_QUALITY, min(MAX_QUALITY, item.quality + delta))


class AgedBrieUpdater(ItemUpdater):
    """Appreciates at the same rate ordinary items degrade."""

    def _quality_delta(self, item):
        return 2 if self._sell_by_date_passed(item) else 1


class BackstagePassUpdater(ItemUpdater):
    """Appreciates faster as the concert approaches, then becomes worthless."""

    def _quality_delta(self, item):
        if self._sell_by_date_passed(item):
            return -item.quality
        if item.sell_in <= 5:
            return 3
        if item.sell_in <= 10:
            return 2
        return 1


class SulfurasUpdater(ItemUpdater):
    """Legendary: never has to be sold and never changes."""

    def update(self, item):
        pass


class ConjuredUpdater(ItemUpdater):
    """Degrades twice as fast as an ordinary item."""

    def _quality_delta(self, item):
        return 2 * super()._quality_delta(item)


_UPDATERS_BY_NAME = {
    AGED_BRIE: AgedBrieUpdater(),
    BACKSTAGE_PASS: BackstagePassUpdater(),
    SULFURAS: SulfurasUpdater(),
}
_CONJURED_UPDATER = ConjuredUpdater()
_DEFAULT_UPDATER = ItemUpdater()


def updater_for(item):
    """Pick the rule set that applies to an item. Updaters are stateless."""
    if item.name in _UPDATERS_BY_NAME:
        return _UPDATERS_BY_NAME[item.name]
    if item.name.startswith(CONJURED_PREFIX):
        return _CONJURED_UPDATER
    return _DEFAULT_UPDATER


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
