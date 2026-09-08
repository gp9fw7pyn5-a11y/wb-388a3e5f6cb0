# -*- coding: utf-8 -*-
"""手机选股卡改为交易三要素布局：买入≤ / 止损 / 目标 三格 + 持有期（2026-09-09）"""
import io

p = __file__.rsplit("_patch_mobile_card.py", 1)[0] + "mobile/swing.html"
BASE = io.path.dirname(p) if hasattr(io, "path") else None
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mobile", "swing.html")
txt = io.open(p, encoding="utf-8").read()

start = txt.index("const cardHtml = (s, i) => {")
end_mark = "const html = GROUPS.map(g => {"
end = txt.index(end_mark, start)

new_block = r'''const cardHtml = (s, i) => {
      const changeColor = s.change >= 0 ? 'var(--qs-state-rise)' : 'var(--qs-state-fall)';
      const changeSign = s.change >= 0 ? '+' : '';
      const num = v => Number(v).toFixed(2);
      return `
        <div class="signal-card" data-index="${i}">
          <div class="signal-card-top">
            <div>
              <div style="display:flex; align-items:center; gap:6px;">
                <span class="stock-name">${s.name}</span>
                <span class="stock-code qs-mono">${s.code}</span>
              </div>
              <div style="display:flex; align-items:center; gap:4px; margin-top:4px;">
                <span class="signal-tag ${signalTagClass(s.signal)}">${s.signal}</span>
                <span class="mini-info">持有 ${s.cycle}</span>
              </div>
            </div>
            <span class="score-badge">${s.score}</span>
          </div>
          <div style="display:flex; gap:5px; margin:8px 0 6px;">
            <div style="flex:1.2; background:var(--qs-surface-2,#1c1c24); border-radius:6px; padding:5px 4px; text-align:center;">
              <div style="font-size:9px; color:var(--qs-ink-3);">买入≤</div>
              <div class="qs-mono" style="font-size:12px; color:var(--qs-ink);">${num(s.entryPrice)}</div>
            </div>
            <div style="flex:1; background:var(--qs-surface-2,#1c1c24); border-radius:6px; padding:5px 4px; text-align:center;">
              <div style="font-size:9px; color:var(--qs-ink-3);">止损</div>
              <div class="qs-mono" style="font-size:12px; color:var(--qs-state-fall);">${num(s.stopPrice)}</div>
            </div>
            <div style="flex:1; background:var(--qs-surface-2,#1c1c24); border-radius:6px; padding:5px 4px; text-align:center;">
              <div style="font-size:9px; color:var(--qs-ink-3);">目标</div>
              <div class="qs-mono" style="font-size:12px; color:var(--qs-state-rise);">${num(s.targetPrice)}</div>
            </div>
          </div>
          <div class="signal-card-mid">
            <span class="price-text qs-mono" style="color:var(--qs-ink);">${s.price.toFixed(2)}</span>
            <span class="change-text qs-mono" style="color:${changeColor};">${changeSign}${s.change.toFixed(2)}%</span>
          </div>
          <div class="signal-card-bottom">
            <span class="mini-info">现价 · ${s.time}</span>
            <span class="mini-info" style="color:var(--qs-primary);">强度 ${s.strength}</span>
          </div>
        </div>
      `;
    };
    '''
txt = txt[:start] + new_block + txt[end:]
io.open(p, "w", encoding="utf-8").write(txt)
print("[OK] 手机选股卡已改为 买入≤/止损/目标 三格 + 持有期")
