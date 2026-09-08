# -*- coding: utf-8 -*-
"""波段页三类标的改造脚本（qs-ui 预览版，2026-09-09）
给8只示例票打 group 标签，desktop/mobile 列表按 趋势回调/反弹延续/低位异动 分节渲染。
只动 qs-ui 预览目录，不碰旧工作台页面。"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
GROUP_MAP = {
    '688981': 'trend', '300750': 'trend', '600276': 'trend',
    '600519': 'cont', '000858': 'cont', '300760': 'cont',
    '002594': 'low', '601012': 'low',
}
GROUPS_JS_DESKTOP = """                const GROUPS = [
                    { key: 'trend', label: '趋势回调', tag: '主力', desc: '止损-10% · 目标+20% · ≤20交易日', color: 'var(--qs-primary)' },
                    { key: 'cont', label: '反弹延续', tag: '升级单', desc: '超跌反弹确认后升级波段', color: 'var(--qs-state-warning)' },
                    { key: 'low', label: '低位异动', tag: '试运行', desc: '长期低位 + 量价异动', color: 'var(--qs-state-info)' }
                ];

"""
GROUPS_JS_MOBILE = """  const GROUPS = [
    { key: 'trend', label: '趋势回调', tag: '主力', desc: '止损-10% · 目标+20% · ≤20交易日', color: 'var(--qs-primary)' },
    { key: 'cont', label: '反弹延续', tag: '升级单', desc: '超跌反弹确认后跟进', color: 'var(--qs-state-warning)' },
    { key: 'low', label: '低位异动', tag: '试运行', desc: '长期低位 + 量价异动', color: 'var(--qs-state-info)' }
  ];

"""

DESKTOP_RENDER_OLD_START = "                function renderSidebar() {"
DESKTOP_RENDER_END_MARK = "                function ma(data, n) {"
DESKTOP_RENDER_NEW = """                function renderSidebar() {
                    const itemHtml = (s, i) => {
                        const changeColor = s.change >= 0 ? 'var(--qs-state-rise)' : 'var(--qs-state-fall)';
                        const changeSign = s.change >= 0 ? '+' : '';
                        const signalColor = s.signal === '突破' ? 'var(--qs-state-rise)' : (s.signal === '回踩' ? 'var(--qs-state-info)' : 'var(--qs-state-warning)');
                        const activeClass = i === activeIndex ? 'active' : '';
                        return `
                            <button type="button" class="qs-sidebar-item ${activeClass}" data-dom-id="swing-item-${i + 1}" data-index="${i}">
                                <div class="qs-sidebar-row">
                                    <span class="qs-sidebar-name">${s.name}</span>
                                    <span class="qs-sidebar-code qs-mono">${s.code}</span>
                                </div>
                                <div class="qs-sidebar-row">
                                    <span class="qs-sidebar-signal" style="color:${signalColor};border-color:${signalColor}35;background:${signalColor}15">${s.signal}</span>
                                    <span class="qs-sidebar-change qs-mono" style="color:${changeColor}">${changeSign}${s.change.toFixed(2)}%</span>
                                </div>
                                <div class="qs-sidebar-row">
                                    <span class="qs-sidebar-score">评分 ${s.score}</span>
                                    <span class="qs-sidebar-industry" style="color:var(--qs-primary)">${s.cycleTag}</span>
                                </div>
                            </button>
                        `;
                    };
                    sidebarList.innerHTML = GROUPS.map(g => {
                        const items = stocks.map((s, i) => ({ s: s, i: i })).filter(x => x.s.group === g.key);
                        if (!items.length) return '';
                        return `
                            <div style="padding:10px 12px 6px;border-top:1px solid var(--qs-line);">
                                <div style="display:flex;align-items:center;gap:6px;">
                                    <span class="qs-caption" style="font-weight:700;color:${g.color};">${g.label}</span>
                                    <span class="qs-caption" style="padding:1px 6px;border-radius:999px;border:1px solid ${g.color}55;color:${g.color};background:${g.color}12;">${g.tag}</span>
                                    <span class="qs-caption" style="color:var(--qs-ink-3);margin-left:auto;">${items.length} 只</span>
                                </div>
                                <div class="qs-caption" style="color:var(--qs-ink-3);margin-top:2px;">${g.desc}</div>
                            </div>
                            ${items.map(x => itemHtml(x.s, x.i)).join('')}
                        `;
                    }).join('');

                    sidebarList.querySelectorAll('.qs-sidebar-item').forEach(btn => {
                        btn.addEventListener('click', function() {
                            activeIndex = parseInt(this.dataset.index, 10);
                            renderSidebar();
                            renderDetail();
                        });
                    });
                }

                """

MOBILE_RENDER_OLD_START = "  function renderList() {"
MOBILE_RENDER_END_MARK = "  function showList() {"
MOBILE_RENDER_NEW = """  function renderList() {
    const cardHtml = (s, i) => {
      const changeColor = s.change >= 0 ? 'var(--qs-state-rise)' : 'var(--qs-state-fall)';
      const changeSign = s.change >= 0 ? '+' : '';
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
                <span class="mini-info">${s.cycleTag}</span>
              </div>
            </div>
            <span class="score-badge">${s.score}</span>
          </div>
          <div class="signal-card-mid">
            <span class="price-text qs-mono" style="color:var(--qs-ink);">${s.price.toFixed(2)}</span>
            <span class="change-text qs-mono" style="color:${changeColor};">${changeSign}${s.change.toFixed(2)}%</span>
          </div>
          <div class="signal-card-bottom">
            <span class="mini-info">${s.industry} · ${s.time}</span>
            <span class="mini-info" style="color:var(--qs-primary);">强度 ${s.strength}</span>
          </div>
        </div>
      `;
    };
    const html = GROUPS.map(g => {
      const items = stocks.map((s, i) => ({ s: s, i: i })).filter(x => x.s.group === g.key);
      if (!items.length) return '';
      return `
        <div style="margin:14px 2px 6px;">
          <div style="display:flex;align-items:center;gap:6px;">
            <span class="qs-caption" style="font-weight:700;color:${g.color};">${g.label}</span>
            <span class="qs-caption" style="padding:1px 6px;border-radius:999px;border:1px solid ${g.color}55;color:${g.color};background:${g.color}12;">${g.tag}</span>
            <span class="qs-caption" style="color:var(--qs-ink-3);margin-left:auto;">${items.length} 只</span>
          </div>
          <div class="qs-caption" style="color:var(--qs-ink-3);margin-top:2px;">${g.desc}</div>
        </div>
        ${items.map(x => cardHtml(x.s, x.i)).join('')}
      `;
    }).join('');
    document.getElementById('stockList').innerHTML = html;

    document.querySelectorAll('.signal-card').forEach(card => {
      card.addEventListener('click', function() {
        activeIndex = parseInt(this.dataset.index, 10);
        showDetail();
      });
    });
  }

  """


def patch(path, is_desktop):
    with io.open(path, encoding='utf-8') as f:
        txt = f.read()
    # 1) 每只票打 group 标签
    for code, g in GROUP_MAP.items():
        old = f"code: '{code}', name:"
        if old not in txt:
            print(f"[警告] {path} 未找到 {old}")
            continue
        txt = txt.replace(old, f"code: '{code}', group: '{g}', name:", 1)
    # 2) 替换列表渲染函数（desktop: renderSidebar→ma 之间；mobile: renderList→showList 之间）
    if is_desktop:
        i = txt.index(DESKTOP_RENDER_OLD_START)
        j = txt.index(DESKTOP_RENDER_END_MARK)
        new_block = GROUPS_JS_DESKTOP + DESKTOP_RENDER_NEW
        txt = txt[:i] + new_block + txt[j:]
        txt = txt.replace('共 8 条短线信号', '三类标的 · 8 只（示例数据）')
        txt = txt.replace('突破 / 回踩 / 量价齐升等中短线信号', '趋势回调 / 反弹延续 / 低位异动')
    else:
        i = txt.index(MOBILE_RENDER_OLD_START)
        j = txt.index(MOBILE_RENDER_END_MARK)
        new_block = GROUPS_JS_MOBILE + MOBILE_RENDER_NEW
        txt = txt[:i] + new_block + txt[j:]
        txt = txt.replace('共 8 条信号', '三类标的 · 8 只（示例）')
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(txt)
    print(f"[OK] {path} 已改造（8票分组+列表分节渲染）")


patch(os.path.join(BASE, 'desktop', 'swing.html'), True)
patch(os.path.join(BASE, 'mobile', 'swing.html'), False)
print('完成。')
