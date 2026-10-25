"""九轉丹房 煙霧測試：python tests/smoke.py

檢查：冇 JS 錯誤、電腦同手機一屏過、投胎、彈窗分頁大細一致、開爐出丹、秘咒。
"""
import pathlib, sys
from playwright.sync_api import sync_playwright

URL = pathlib.Path(__file__).resolve().parent.parent.joinpath('index.html').as_uri()
FAST = "window.setTimeout=(f,t)=>Promise.resolve().then(f)"  # 跳過煉丹動畫
fails = []

def check(ok, msg):
    print(('OK   ' if ok else 'FAIL ') + msg)
    if not ok:
        fails.append(msg)

with sync_playwright() as p:
    b = p.chromium.launch()

    # 一屏過
    for w, h in [(1366, 768), (390, 844), (375, 667)]:
        pg = b.new_page(viewport={'width': w, 'height': h})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(300)
        sh, ih, sw, iw = pg.evaluate('[document.documentElement.scrollHeight,innerHeight,document.documentElement.scrollWidth,innerWidth]')
        check(sh <= ih and sw <= iw, f'{w}x{h} 一屏過（{sh}/{ih}, {sw}/{iw}）')
        check(not errs, f'{w}x{h} 冇 JS 錯誤 {errs}')
        pg.close()

    pg = b.new_page(viewport={'width': 1366, 'height': 768})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script(FAST)
    pg.goto(URL); pg.wait_for_timeout(300)

    # 投胎：新存檔一開就要揀資質同出身
    check(pg.is_visible('#bGo'), '新存檔彈出投胎揀資質出身')
    pg.click('[data-bid=yaonong]'); pg.click('#bGo')
    check(not pg.is_visible('#bGo') and '道德' in pg.inner_text('#stats'), '入世之後有道德狀態')

    # 秘咒
    pg.click('#openAch')
    for code in ['點石成金', '急急如律令', '丹道通神']:
        pg.fill('#cheatIn', code); pg.click('#cheatGo')
    stones = pg.inner_text('#stats')
    check('金丹' in stones, '丹道通神 → 金丹期')
    pg.click('#mtCar')
    check(not pg.is_visible('#cheatIn'), '丹途門派分頁冇秘咒欄')
    pg.click('#mtAch')

    # 彈窗分頁大細一致
    boxes = set()
    for t in ['mtBook', 'mtWx', 'mtShop', 'mtRoom', 'mtAch', 'mtCodex', 'mtLife', 'mtRel', 'mtCar']:
        pg.click('#' + t)
        boxes.add(pg.eval_on_selector('#modal>.mbox', 'e=>{const r=e.getBoundingClientRect();return [r.top,r.height,r.width].map(Math.round).join(",")}'))
    check(len(boxes) == 1, f'彈窗九個分頁大細一致 {boxes}')
    pg.click('#mClose')

    # 左上角撳自己
    pg.click('#meBtn'); pg.wait_for_timeout(50)
    check(pg.is_visible('.me-svg'), '撳左上角境界開到自己人物狀態')
    pg.click('#popClose')

    # 打坐
    pg.click('#med'); pg.wait_for_timeout(50)
    check(pg.is_visible('#card'), '打坐有結果卡')
    while pg.is_visible('#card [data-i]'):
        pg.click('#card [data-i] >> nth=0')
    if pg.is_visible('#aClose'):
        pg.click('#aClose')
    pg.wait_for_timeout(50)
    while pg.is_visible('#card [data-i]') or pg.is_visible('#aClose'):
        pg.click('#card [data-i] >> nth=0') if pg.is_visible('#card [data-i]') else pg.click('#aClose')

    # 開爐出丹
    pg.click('#go'); pg.wait_for_timeout(100)
    check(pg.is_visible('#card'), '開爐有結果卡')
    if pg.is_visible('#aStash'):
        pg.click('#aStash')
    check(not errs, f'操作過程冇 JS 錯誤 {errs}')
    b.close()

print('\n全部通過' if not fails else f'\n{len(fails)} 項失敗')
sys.exit(1 if fails else 0)
