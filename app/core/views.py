from django.shortcuts import render, get_object_or_404
from .models import Asset

def home(request):
    rows = []
    for a in Asset.objects.all():
        qs = a.prices.order_by("-date")[:2]
        last = qs[0].value_mru if qs else None
        prev = qs[1].value_mru if len(qs) > 1 else None
        var = (last - prev) if last and prev else None
        rows.append({"asset": a, "last": last, "var": var})
    return render(request, "core/home.html", {"rows": rows})


from datetime import date
from dateutil.relativedelta import relativedelta

def asset_detail(request, asset_id):
    a = get_object_or_404(Asset, id=asset_id)
    period = request.GET.get("period", "2y")

    end = date.today()
    if period == "7d": start = end - relativedelta(days=7)
    elif period == "1m": start = end - relativedelta(months=1)
    elif period == "3m": start = end - relativedelta(months=3)
    elif period == "6m": start = end - relativedelta(months=6)
    elif period == "1y": start = end - relativedelta(years=1)
    else: start = end - relativedelta(years=2)

    prices = a.prices.filter(date__gte=start).order_by("date")
    dates = [p.date.isoformat() for p in prices]
    values = [float(p.value_mru) for p in prices]

    return render(request, "core/asset_detail.html", {
        "asset": a, "dates": dates, "values": values, "period": period
    })




def compare(request):
    assets = Asset.objects.all()
    selected = request.GET.getlist("assets")
    period = request.GET.get("period", "2y")

    end = date.today()
    if period == "7d": start = end - relativedelta(days=7)
    elif period == "1m": start = end - relativedelta(months=1)
    elif period == "3m": start = end - relativedelta(months=3)
    elif period == "6m": start = end - relativedelta(months=6)
    elif period == "1y": start = end - relativedelta(years=1)
    else: start = end - relativedelta(years=2)

    series = []
    for a in assets.filter(code__in=selected):
        prices = a.prices.filter(date__gte=start).order_by("date")
        series.append({
            "label": a.code,
            "dates": [p.date.isoformat() for p in prices],
            "values": [float(p.value_mru) for p in prices],
        })

    return render(request, "core/compare.html", {
        "assets": assets, "series": series, "selected": selected, "period": period
    })

