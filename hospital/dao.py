from hospital import utils
def total_bill(month):
    total = 0
    month_stats = utils.stats_revenue(month)
    for s in month_stats:
        total = total + s[2]
    return total