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

def asset_detail(request, asset_id):
    a = get_object_or_404(Asset, id=asset_id)
    prices = a.prices.order_by("date")
    dates = [p.date.isoformat() for p in prices]
    values = [float(p.value_mru) for p in prices]
    return render(
        request,
        "core/asset_detail.html",
        {"asset": a, "dates": dates, "values": values},
    )
