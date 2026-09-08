# -*- coding: utf-8 -*-
"""K线真实数据补丁（desktop+mobile）：图表优先用 stocks[activeIndex].prices 真实收盘，
切换个股时同步刷新K线（window.qsUpdateKline）。"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))

DESKTOP_A_OLD = """        const basePrice = readPrice();
        const count = timeframe === 'intraday' ? 48 : (timeframe === 'month' ? 30 : (timeframe === 'week' ? 60 : 90));
        const ohlc = genOHLC(basePrice, count, timeframe);"""
DESKTOP_A_NEW = """        const basePrice = readPrice();
        const count = timeframe === 'intraday' ? 48 : (timeframe === 'month' ? 30 : (timeframe === 'week' ? 60 : 90));
        const realCloses = (typeof stocks !== 'undefined' && stocks[activeIndex] && stocks[activeIndex].prices && stocks[activeIndex].prices.length > 5) ? stocks[activeIndex].prices : null;
        const ohlc = realCloses ? realCloses.map(function(c, i) { return { x: i, o: c, h: c, l: c, c: c }; }) : genOHLC(basePrice, count, timeframe);"""
DESKTOP_B_OLD = "        setTimeout(() => { updateKlineHeader(); renderKline(currentTimeframe); }, 0);"
DESKTOP_B_NEW = """        setTimeout(() => { updateKlineHeader(); renderKline(currentTimeframe); }, 0);
        window.qsUpdateKline = function() { updateKlineHeader(); renderKline(currentTimeframe); };"""
DESKTOP_C_OLD = """                            activeIndex = parseInt(this.dataset.index, 10);
                            renderSidebar();
                            renderDetail();
                        });"""
DESKTOP_C_NEW = """                            activeIndex = parseInt(this.dataset.index, 10);
                            renderSidebar();
                            renderDetail();
                            if (window.qsUpdateKline) window.qsUpdateKline();
                        });"""

MOBILE_A_OLD = "    var ohlc = genOHLC(basePrice, count, timeframe);"
MOBILE_A_NEW = """    var realCloses = (typeof stocks !== 'undefined' && stocks[activeIndex] && stocks[activeIndex].prices && stocks[activeIndex].prices.length > 5) ? stocks[activeIndex].prices : null;
    var ohlc = realCloses ? realCloses.map(function(c, i) { return { x: i, o: c, h: c, l: c, c: c }; }) : genOHLC(basePrice, count, timeframe);"""


def patch(path, edits):
    txt = io.open(path, encoding="utf-8").read()
    for old, new in edits:
        if old not in txt:
            print(f"[警告] {path} 未找到锚点: {old[:50]!r}")
            continue
        txt = txt.replace(old, new, 1)
    io.open(path, "w", encoding="utf-8").write(txt)
    print(f"[OK] {path}")


patch(os.path.join(BASE, "desktop", "swing.html"),
      [(DESKTOP_A_OLD, DESKTOP_A_NEW), (DESKTOP_B_OLD, DESKTOP_B_NEW), (DESKTOP_C_OLD, DESKTOP_C_NEW)])
patch(os.path.join(BASE, "mobile", "swing.html"), [(MOBILE_A_OLD, MOBILE_A_NEW)])
print("完成。")
