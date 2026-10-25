# CLAUDE.md · 九轉丹房開發說明

畀喺 Claude Code 繼續開發用。玩法說明睇 `README.md`。

## 項目概覽

- **係咩**：修仙煉丹模擬網頁遊戲，廣東話介面。
- **技術**：單一檔案 `index.html`（HTML＋CSS＋原生 JS，大約 2300 行），冇 build、冇框架、冇依賴。只載 Google Fonts（Ma Shan Zheng 標題、Noto Serif TC 內文）。
- **存檔**：瀏覽器 `localStorage`，key 係 `dan-sim-v2`。
- **GitHub**：`fiveathree/dan`，分支 `main`。
- **用戶**：唔係技術人員，用廣東話溝通；要佢自己做嘅設定步驟要由頭逐步講，按鈕／選單名要準確。

## 硬性要求（用戶親口提過）

1. **一屏過**：電腦同手機都唔可以成頁上下或者左右碌。內容多就喺面板或彈窗入面碌。
   - 改完版面一定要量 `document.documentElement.scrollHeight === innerHeight`（1366×768、390×844、375×667）。
   - 375×667 嘅「火候丹爐」分頁而家會長少少，要碌少少，屬已知問題。
2. **丹爐放中間**：左丹方、中丹爐、右藥櫃。
3. **彈窗（`#modal`）固定大細**，頂部分頁條固定位置，內容喺 `.mscroll` 入面碌。
4. 文字用廣東話口語，正體字。
5. 新功能要有**秘咒**或者方法方便測試。

## 畫面結構（HTML id）

| 區域 | id／class | 說明 |
|---|---|---|
| 頂部 | `header.top`、`#stats`、`.hbtns` | 狀態列由 `renderStats()` 生成；掣：`#asc` 渡劫飛升（渡劫圓滿先顯示）、`#med` 打坐、`#task` 斬妖、`#herb` 採藥、`#grab` 擄人（魔頭先顯示）、`#openBook`、`#openShop`、`#openRel` 人物、`#openCar`、`#openAch` |
| 左面板 | `#pRecipe` | 丹道 `#paths`、心法 `#arts`、火種 `#fires`、火候 `#heat`、丹爐 `#furns`。`.g1`／`.g2` 用嚟喺手機分兩個分頁 |
| 中 | `#stage` | `<canvas id="cv">` 爐火動畫、`#log` 爐火紀錄、`#ov > #card` 疊層卡（出丹、結果、死亡、奇遇選擇） |
| 人物 | 關係圖中間「你」`data-k=me` → `showMe()`／`meSvg()` 打坐圖同裝備；電腦版頂部 `#openRel` 隱藏，用開爐格 `#dockRel` |
| 中 | `#innerRow` | 三格：`[data-cell=dl]` 道侶、`[data-cell=inner]` 入室、`[data-cell=jm]` 記名 |
| 中 | `.dock` | `#order` 投料、`#wxBar` 五行、`#yyNeedle` 陰陽、`#rate` 成功率、`#yield` 出丹、`#cost`、`#go` 開爐、`#dockRel`／`#dockShop`／`#dockRoom`／`#dockCar`／`#dockBook`（手機隱藏） |
| 右面板 | `#pShelf` | `#shelf` 藥櫃、`#ingTip` |
| 大彈窗 | `#modal` | 分頁 `#mtBook #mtShop #mtRoom #mtAch #mtCodex #mtLife #mtRel #mtCar`；內容 `#mTitle #mBody`；秘咒 `#cheatIn`；訊息 `#mMsg` |
| 小彈窗 | `#pop` | `#popBody`；用嚟顯示弟子、抽籤、道侶、記名管理 |
| 提示 | `#toast` | `toast(msg, ms)` |

手機斷點：`max-width:860px`（單欄、分頁）、`max-width:860px and max-height:720px`（矮機再壓縮）、`max-width:360px`。

## JS 結構

全部包喺一個 IIFE 入面。**注意：** 好多模組係用 patch 腳本插喺 `const P=()=>save.player;` 下面，所以檔案入面嘅次序同開發次序相反；全部用 function declaration，執行時先會用到，次序冇問題。

用 `/* ---------- 名 ---------- */` 分段，主要段落：

| 段落 | 內容 |
|---|---|
| 資料 | `EL GEN CTRL PATHS ARTS FIRES FURN ING REALMS LIFE GRADES NAMES SPECIAL ALL_PILLS` |
| 境界、打坐、渡劫 | `TOP=8`（渡劫）、`realmName(r,cult)` 小境界、`breakthrough()`（所有加修為都要經佢，封頂渡劫圓滿）、`canAscend() ascendChance() showAscend()`、`meditate()`、`MED_EV`、`pickW()` |
| 師傅 | `MS()`、`makeMaster() showMaster() masterAction()` |
| 人物恩怨 | `NPCS() addNPC({key?,name,rel,note,lv?}) delNPC() showNPC() npcAction()`；`rel`：you 知己／chou 仇人／dui 對手／qdl 前道侶／pan 叛徒／qms 斷絕師徒 |
| 家中奇遇 | `HOME_EV`（物件，`w`、`cond()`、`run(lines)`）、`queueHome()`（yearTick 每年 22%）、`flushEvents()`／`kickEvents()`：等冇彈窗先顯示 |
| 人物關係圖 | `relNodes() renderRel() onRelClick()`，SVG |
| 解鎖與成就 | `START`（開局解鎖）、`ACHS`（成就，`u` 欄係解鎖項目）、`checkAch()` |
| 存檔 | `newPlayer() newSave() persist()`、舊等級換算（`gver`） |
| 道德 | `moral() addMoral(n)`（回傳「，道德 ±n」字串，直接接落訊息）、`stance()` zheng／fan／wu、`wanted()`（≤ −50 通緝）、`moralTick()`、`fightWin(base, lv)` 打架勝算 |
| 投胎 | `IDS` 出身、`P_APT` 玩家資質倍數同代價、`showBirth() applyBirth()`、`ready()`（未投胎、煉緊、死咗都唔准郁）、`cultMul()` |
| 後代 | `KIDS() newKid(dl) showKid() kidAction() inherit(id)` |
| 武學 | `mfx()` 匯總藏書 `mx`（按修煉階段乘 `WX_ST` 比例）：atk 戰力、dodge 身法、nei 修為%、xin 心魔減免%、herb、detox；進度 `WXP()`、`wxStage() wxTrain(id, base) trainWx(id)`，主修 `pl.wxMain` 打坐順便練 |
| 委託 | `ORD() orderPool() newOrder() orderTick() huntHerbs() applyOrder() renderOrders() orderFor(p) showDeliver(id) deliverScore()` |
| 宗門階級 | `RANKS RANK_GX STIPEND UPKEEP`、`newSectTask() taskReady(t,ex) submitTask(ex) rankUps() sectTick()`（每年：月俸、俸祿、任務過期、大比、挖角）、`switchSect()`、自創宗門 `STASK() ownTaskTick() rankOf(m) promoGate(m)`、`renderSectTasks()`；大比／挖角係 `HOME_EV` 入面 `w:0` 嘅事件，用 `queueEv(k)` 排 |
| 籠絡弟子 | 送靈石、送藥、傳功、大弟子 `headD()`；`askConfirm(問, 說明, 確定動作, id, 返轉頭動作)` 唔可以返轉頭嘅動作先彈窗問 |
| 丹價行情 | `prices()` 行情指數、`retailPrice()`、`makeShopPill()` |
| 丹室、丹瓶、儲物袋、兵器防具 | `DR()`（`wpn` `arm` 等級）、`ROOM_LV BOTTLES BAGS WEAPONS ARMORS`、`buyGear(kind)`、`storePill() roomDecay() bagAdd()`、`renderRoom() renderMarket() renderStock()` |
| 丹市 | `basePrice() satMult() quoteN() doSell(n,auto,quiet)`、黑市事件 |
| 道侶 | `DL()`、`DL_KIND`、`dlTick() showDL() giftPill()` |
| 奇遇 | `ADV` 陣列（`w` 權重、`ctx` herb／yao／both、`run(lines)` 可回傳 `{lines, choice, death}`）、`adventure() resolveAdv()` |
| 忠誠度、升降 | `loy() addLoy() loyMult() loyBase() promote() demote() loyTick()` |
| 生平 | `LN()` 每世計數、`bio()`、`bioTrack()`（喺 `afterAction` 比較前後狀態自動記大事）、`lifeRecord() renderLives()` |
| 入室弟子 | `APT` 資質、`rollApt()` 抽籤連保底、`yearTick()`（每年：入室修煉壽元、忠誠、道侶、丹市、行情、丹室流失、慕名求見） |
| 中間三格 | `renderInner() showInnerList() showJiming() showDLCell() showDisciple() showDraw() onPopClick()` |
| 魔頭 | `MO()`、`becomeMo() reform() grab() moTick()`、牢房 |
| 藏書與丹書 | `BOOKS`、`bookFx()`、`recipes() mastery()`、`previewRecipe()`、`applyRecipe()`、`recordBrew()`、`gradeFromQ() nameFor()`、商行藏書 |
| 丹途 | `CERT SKILL_N SECTS SECT_LV PERS ROLES`、`C()`、`capOf() innerCap()`、`team()`（所有加成匯總）、`careerAfterBrew()`、考證、入會、開宗 |
| 核心演算 | `analyse()` → `{Q, S, boom, ideal, dev, dom, flags, notes, mName, mCount…}`；`successRate()`、`yieldCount()` |
| 煉丹 | `brew() → turnMsg() → finish() → makePill()` |
| 疊層卡 | `openOverlay() showPill() showOutcome() useOne()` |
| 食丹 | `effects(p, realm)`、`eat() test() testBy() testByMortal()` |
| 生死 | `checkLife() endLife() showDeath()`、轉世 |
| 彈窗 | `renderModal() openTab()`、`cheat()` |

### 核心流程

- **任何改變狀態嘅動作之後都要叫 `afterAction()`**：

  ```js
  afterAction() = moTick(); yearTick(); bioTrack(); checkLife(); checkAch(); fixCfg(); persist(); renderAll(); kickEvents();
  ```

- **時間**：用 `P().age += 1` 代表過一年，之後叫 `afterAction()`。每年要做嘅嘢放喺 `yearTick()` 個 while 迴圈入面（用 `pl.ly` 計過咗幾多年）。
- **修為**：正數修為一律經 `gainCult()`（已乘 `cultMul()`＝資質×內功）；食丹喺 `eat()` 另外乘。
- **加成**：所有弟子、門派、道侶、牢房嘅加成都匯總喺 `team()`，回傳 `{q, stab, disc, inc, pres, helpers, wild}`。藏書加成係 `bookFx()`，熟練度喺 `analyse()` 入面計。
- **加修為**：一律用 `gainCult(n)`（內部叫 `breakthrough()`），唔好自己寫 `while(cult>=100)` 迴圈。境界最高自動去到 `TOP`（渡劫），飛升要經 `showAscend()` 將 `realm` 設做 9。
- **家中奇遇**：`yearTick` 入隊，`flushEvents` 會等 `#ov`、`#pop`、`#modal` 全部閂咗先彈出。新增事件加入 `HOME_EV`。
- **品級**：`gradeFromQ(Q, fire, furn)`，門檻係 Q＜15 廢丹、＜45 下品、＜80 中品、＜120 上品、其餘仙丹。
- **手上丹藥**：`current = {name, kind, grade, gradeName, Q, path, dom, tox, yy, demon, art, desc, elHex, count}`。`kind` 係 normal／waste／raw／burnt／chicken／meng，失敗品見 `FAIL_KINDS`。用 `useOne()` 扣一粒。
- **結果顯示**：用 `showOutcome(title, [[文字, 'good'|'bad']], fx)`；如果 `current` 仲有剩，會自動顯示「處理剩低」掣。
- **小彈窗動作**：用 `data-a` 屬性，喺 `onPopClick()` 分派（籠絡動作經 `onLoyClick()`）。大彈窗各分頁有自己嘅 click handler：`onCareerClick`、`onBookClick`、`onRoomClick`。

## 存檔結構

```js
save = {
  gver: 2, rver: 2 /* 九境界遷移 */, npcId, cheat, lives, shidi /* 累計試死，畀成就用 */,
  codex: [丹名], ach: [成就id], st: {各種累計計數},
  books: [書id], recipes: {丹名: {cfg, src, g}}, mastery: {丹名: 次數},
  history: [前世紀錄], shop: {age, life, stock}, market: {丹名: 已賣量}, prices: {丹名: {i, prev}},
  dead?: {title, text, win},
  player: {                       // 每一世，轉世重置
    realm /* 0 煉氣…8 渡劫、9 飛升 */, cult, tox, demon, age, lifeBonus, stones, alive,
    master: {name, sect, realm, aff, since, left}|null, npcs: [{id, key?, name, rel, note, aff, since, lv?}], evq: [家中奇遇 key],
    car: {skill, sxp, cert, aff /* null|xie|sect|own */, sect, sectName, lvl, pres,
          rank /* 0-4 */, gx /* 功勞 */, fail, task: {kind, g, n, left}, dabi, stasks: [{kind, who, last}],
          members: [記名], inner: [入室], cands: [招募候選], visitors: [慕名求見], pity, head, nid},
    mo: {on, infamy, prisoners, caught, killed, last, nid},
    dl: 道侶|null, bag: {藥材id: 數量}, dr: {lvl, stacks, bottle, bagLv},
    n: {每世計數}, bio: [{a, t}], bt: {bioTrack 上次狀態}, ly: 上次 yearTick 年歲,
    born /* false＝未揀資質出身 */, apt /* 0-4 */, id /* IDS key */, moral /* −100..100 */,
    kids: [{id, name, f, apt, age, sk, par}], orders: [{id, who, name, g, need, fair, wait, cfg, special}],
    unl: [上山搵藥解鎖嘅藥材id], wx: {武學書id: 0-100}, wxMain, npcs: [{…, mo /* 魔道中人 */, dk /* 道侶種類 */, vis /* 拜訪次數 */}]
  }
}
```

- 舊存檔冇 `born`：載入時當佢係中等資質散修（`born:true, apt:1, id:'sanxiu'`）。新一世 `newPlayer()` 係 `born:false`，啟動時會彈 `showBirth()`。
- 唔好隨便改存檔 key。要改格式就加遷移（參考 `gver` 嘅等級換算），因為用戶部機有舊存檔。
- 弟子物件：`{id, name, f, pers, skill, xp, realm, role, loy, gifts, fame?, apt?, age?, cult?, hao?, rk? /* 記名弟子階級 0-2 */, gx? /* 功勞 */}`；入室弟子一定有 `apt`、`age`、`cult`。

## 設計

- **主題**：單一深色主題，丹房暗木配青銅同硃砂。顏色全部用 `:root` 嘅 token（`--ink --panel --panel2 --line --bronze --cinnabar --jade --paper --muted`，五行 `--el-m/w/s/f/e`）。
- **元件**：`.btn`、`.chip[aria-pressed]`、`.tag(.good/.bad)`、`.mem` 卡、`.testers .tester` 揀人清單、`.draw-acts` 掣組、`.mkt` 表格、`.dz` 中間格。
- 要支援 `prefers-reduced-motion`。

## 測試

用 Playwright（Python）：

```bash
pip install playwright --break-system-packages && python -m playwright install chromium
python tests/smoke.py
```

- `tests/smoke.py` 會檢查：冇 JS 錯誤；電腦同手機一屏過；新存檔彈投胎；所有彈窗分頁大細一樣；丹途門派冇秘咒欄；打坐、開爐出丹；秘咒有效。新存檔一定要先撳 `#bGo` 入世先玩得。
- 測試用秘咒：`急急如律令 點石成金 丹道通神 走火入魔 天劫將至 大仁大義 大奸大惡 有求必應 開枝散葉 魔女知己 壽元將盡 武學大成 拜入山門 宗門大比 五年大比 有人挖角`（喺 `cheat()`）。
- 測試小技巧：加 `page.add_init_script("window.setTimeout=(f,t)=>Promise.resolve().then(f)")` 可以跳過煉丹動畫，即刻出結果。
- 改完 JS 先用 node 做語法檢查：

  ```bash
  node -e "const s=require('fs').readFileSync('index.html','utf8');new Function(s.match(/<script>([\s\S]*)<\/script>/)[1]);console.log('ok')"
  ```

## 數值平衡（現狀）

- **開局**：16 歲、600 靈石、煉氣期、壽元 120。
- **賣丹**：參考價 `GRADE_BASE=[1,15,60,220,1200]`，再乘行情（0.5 至 1.8），飽和係 `1/(1+已賣量×0.12)`，每年已賣量 ×0.75。
- **境界**：`REALMS` 十個（含飛升），`LIFE=[120,220,500,1000,2000,3500,5000,8000,12000,99999]`。食丹修為 ÷ `(1+境界×0.8)`。
- **自然消退**：毒每年 −2、心魔每年 −1；打坐心魔 −10 至 −20、毒 −8。
- **入室弟子修為**：每年 `(1.2+丹術×0.12) × 資質倍數 ÷ (1+境界×1.2)`，刻意慢過玩家。
- **奇遇**：採藥 55%、斬妖 50% 機會觸發；致命機率大約每次出行 0.5% 至 1%。
- **黑市事件**：埋伏 8%（＋惡名×0.3%），黑吃黑 7%，大客 6%，官差 5%。

## 部署

- 而家用戶喺 claude.ai 用 Artifact 試玩。Artifact 版本係由 `index.html` 去掉 `<!doctype>`、`<html>`、`<head>`、`<body>` 外殼生成。
- 想有公開網址，可以用 GitHub Pages（repo Settings → Pages → Branch: main / root）或者 Cloudflare Pages，兩樣都唔使 build。

## Commit

- Commit 訊息用廣東話簡述改咗咩。
- push 之前用 `git pull` 同步。
