from django.db.models import Sum

from order.models import ProtocolWithdrawal, StockEntry, StockWithdrawal


def get_stock_item_quantity(stock_item):
    entries = (
        StockEntry.objects.filter(stock_item=stock_item).aggregate(
            Sum("entry_quantity")
        )["entry_quantity__sum"]
        or 0
    )
    withdrawals = (
        StockWithdrawal.objects.filter(stock_item=stock_item).aggregate(
            Sum("withdraw_quantity")
        )["withdraw_quantity__sum"]
        or 0
    )
    return entries - withdrawals


def get_protocol_item_quantity(protocol_item):
    withdrawals = (
        ProtocolWithdrawal.objects.filter(protocol_item=protocol_item).aggregate(
            Sum("withdraw_quantity")
        )["withdraw_quantity__sum"]
        or 0
    )
    return protocol_item.original_quantity - withdrawals
