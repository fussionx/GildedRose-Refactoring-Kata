# -*- coding: utf-8 -*-
"""Unit tests for the Gilded Rose inventory rules.

Each test drives update_quality() for a single day on a single item so that a
failure points at exactly one rule. The 30-day approval test covers the
interaction of rules over time.
"""
import pytest

from gilded_rose import GildedRose, Item

AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"


def update(name, sell_in, quality):
    """Run one day of update_quality() and return (sell_in, quality)."""
    item = Item(name, sell_in, quality)
    GildedRose([item]).update_quality()
    return item.sell_in, item.quality


class TestNormalItem:
    def test_sell_in_and_quality_both_drop_by_one_each_day(self):
        assert update("+5 Dexterity Vest", 10, 20) == (9, 19)

    def test_quality_degrades_twice_as_fast_once_sell_by_date_has_passed(self):
        assert update("+5 Dexterity Vest", 0, 20) == (-1, 18)

    @pytest.mark.parametrize("sell_in", [5, 0, -3])
    def test_quality_is_never_negative(self, sell_in):
        _, quality = update("Elixir of the Mongoose", sell_in, 0)
        assert quality == 0

    def test_quality_of_one_after_sell_by_clamps_to_zero(self):
        assert update("Elixir of the Mongoose", -1, 1) == (-2, 0)


class TestAgedBrie:
    def test_quality_increases_by_one_each_day(self):
        assert update(AGED_BRIE, 2, 0) == (1, 1)

    def test_quality_increases_twice_as_fast_once_sell_by_date_has_passed(self):
        assert update(AGED_BRIE, 0, 10) == (-1, 12)

    @pytest.mark.parametrize("sell_in, quality", [(5, 50), (0, 50), (0, 49)])
    def test_quality_never_exceeds_fifty(self, sell_in, quality):
        _, new_quality = update(AGED_BRIE, sell_in, quality)
        assert new_quality == 50


class TestSulfuras:
    @pytest.mark.parametrize("sell_in", [10, 0, -1])
    def test_never_changes(self, sell_in):
        assert update(SULFURAS, sell_in, 80) == (sell_in, 80)


class TestBackstagePasses:
    # 11 is the day before the first tier boundary, so it guards the off-by-one.
    @pytest.mark.parametrize("sell_in", [15, 11])
    def test_quality_increases_by_one_when_more_than_ten_days_remain(self, sell_in):
        assert update(BACKSTAGE_PASS, sell_in, 20) == (sell_in - 1, 21)

    @pytest.mark.parametrize("sell_in", [10, 6])  # 6 is the day before the next tier
    def test_quality_increases_by_two_when_ten_days_or_less_remain(self, sell_in):
        assert update(BACKSTAGE_PASS, sell_in, 20) == (sell_in - 1, 22)

    @pytest.mark.parametrize("sell_in", [5, 1])
    def test_quality_increases_by_three_when_five_days_or_less_remain(self, sell_in):
        assert update(BACKSTAGE_PASS, sell_in, 20) == (sell_in - 1, 23)

    @pytest.mark.parametrize("sell_in, quality", [(15, 50), (10, 49), (5, 48)])
    def test_quality_never_exceeds_fifty(self, sell_in, quality):
        _, new_quality = update(BACKSTAGE_PASS, sell_in, quality)
        assert new_quality == 50

    @pytest.mark.parametrize("sell_in", [0, -1])
    def test_quality_drops_to_zero_after_the_concert(self, sell_in):
        _, quality = update(BACKSTAGE_PASS, sell_in, 40)
        assert quality == 0


def test_all_items_in_the_inventory_are_updated():
    items = [
        Item("+5 Dexterity Vest", 10, 20),
        Item(AGED_BRIE, 2, 0),
        Item(SULFURAS, 0, 80),
        Item(BACKSTAGE_PASS, 5, 20),
    ]
    GildedRose(items).update_quality()
    assert [(i.sell_in, i.quality) for i in items] == [
        (9, 19),
        (1, 1),
        (0, 80),
        (4, 23),
    ]


def test_an_empty_inventory_is_handled():
    GildedRose([]).update_quality()  # must not raise
