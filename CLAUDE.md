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
| 頂部 | `header.top`、`#stats`、`.hbtns` | 狀態列由 `renderStats()` 生成（境界名 `#meBtn` 同 `h1` 撳落開 `showMe()`）；掣：`#asc` 渡劫飛升（渡劫圓滿先顯示）、`#med` 打坐、`#task` 斬妖、`#herb` 採藥、`#grab` 擄人（魔頭先顯示）、`#openBook`、`#openShop`、`#openRel` 人物、`#openCar`、`#openAch` |
| 左面板 | `#pRecipe` | 丹道 `#paths`、心法 `#arts`、火種 `#fires`、火候 `#heat`、丹爐 `#furns`。`.g1`／`.g2` 用嚟喺手機分兩個分頁 |
| 中 | `#stage` | `<canvas id="cv">` 爐火動畫、`#quests` 任務欄（`questList() renderQuests()`，手機縮做一粒掣）、`#log` 爐火紀錄、`#ov > #card` 疊層卡（出丹、結果、死亡、奇遇選擇） |
| 人物 | 關係頁 `relGroups() renderRel()`：上半 org chart（`.org-row`），下半江湖分組卡片（家人、師門、朋友、仇敵、其他），撳 `[data-k]` 經 `onRelClick()` 分派；最頂「你」`data-k=me` → `showMe()`／`meSvg()` 打坐圖同裝備；電腦版頂部 `#openRel` 隱藏，用開爐格 `#dockRel` |
| 中 | `#innerRow` | 六格（`renderInner()`）：`[data-cell=dl]` 道侶、`kid` 子女（`showKids()`）、`head` 親傳、`inner` 入室、`wai` 外門、`jm` 記名；手機只顯示名同人數 |
| 中 | `.dock` | `#order` 投料、`#wxBar` 五行、`#yyNeedle` 陰陽、`#rate` 成功率、`#yield` 出丹、`#cost`、`#go` 開爐、`#dockRel`／`#dockShop`／`#dockRoom`／`#dockCar`／`#dockBook`（手機隱藏） |
| 右面板 | `#pShelf` | `#shelf` 藥櫃、`#ingTip` |
| 主視窗 | `#modal` | 兩層導航：`#mSec` 六大區（`#ms_dan` `#ms_xiu` `#ms_ren` `#ms_zong` `#ms_chan` `#ms_ji`）、`#mSub` 子分頁（`#ml_<leaf>`）；`#mTitle #mBody`；秘咒 `#cheatIn` 只喺紀錄區顯示；訊息 `#mMsg` |
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
| 後代 | 子女入門 `kidJoin(id)`（弟子 `kidOf`、子女 `disc`）、`kidDisc(k)`；`KIDS() newKid(dl) showKid() kidAction()`（陪伴、家學、零用錢、書院、餵靈丹）`kidTick()` 親情 `kAff(k)`、`inherit(id)` |
| 武學 | `mfx()` 匯總藏書 `mx`（按修煉階段乘 `WX_ST` 比例）：atk 戰力、dodge 身法、nei 修為%、xin 心魔減免%、herb、detox；進度 `WXP()`、`wxStage() wxTrain(id, base) trainWx(id)`，主修 `pl.wxMain` 打坐順便練 |
| 委託 | 滿意度 `sat(o)`、`orderWoo(a,id)`（送禮、拜訪、送樣辦）、急單 `o.urgent`；`ORD() orderPool() newOrder() orderTick() huntHerbs() applyOrder() renderOrders() orderFor(p) showDeliver(id) deliverScore()` |
| 請求 | `REQS() newReq() reqTick() reqReady() showReq() doReq(id, yes)`；`pl.reqs: [{id, src:'npc'|'disc', ref, name, kind, g, n, left}]` |
| 宗門大山 | 拖放：`.mt-n.drag` pointer 事件（`mtDrag`、`mtPt()`、`mtTier()`、`MT_TIERS`）→ `moveRank(id, r)`；`mtDragEnd` 避免拖完當撳；`sectMountain()`：SVG 大山，掌門寶座喺頂，`rankOf()` 分層；撳人經 `hubKey()`；喺 `門派` leaf 最頂 |
| 宗門賞罰 | `sectReward(tier, force)`（靈石、藥材、書、延壽丹、`giveXianqi()` 仙器）、`sectPunish('late'|'jie')`、`sectLog()` 寫入 `car.log` |
| 名聲 | `FM()`（`pl.fm={g 美名, b 臭名}`）、`addFame(g,b)` 回傳「，美名 +n」字串、`fameTick()` 排美名／臭名事件（`HOME_EV` 嘅 `fg*`、`fb*`）、影響 `capOf() innerCap()`、慕名、委託 |
| 開宗地圖 | `LOCS`（x、y、res、comp、fx）、`locOf()`、`showMap()` `mapSvg()`、`createSect(name, loc)`；`car.loc`；踢館 `HOME_EV.rival`、`sectLvUp(msgs)` |
| 安排工作 | `DL_JOBS KID_JOBS dlJob() kidJob() jobTick() showJobs() setJob()`；道侶 `dl.job`、子女 `kid.job` |
| 任務榜 | 自創宗門 `STASK()` 發佈制（`t.on`），`ownTaskTick()` 弟子自己接 |
| 委派 | `deleSel(key, cur, 難度, 排除)` 下拉、`setDele()`、`deleTick()` 每年結算、`delChance(m, d)`；key 係 `t:序號`／`o:委託id`／`r:請求id`，物件上 `dz`＝弟子 id |
| 宗門階級 | `TQ()`（`car.tasks` 任務隊列，每年派一項，最多三項）、`RANKS RANK_GX STIPEND UPKEEP`、`newSectTask() taskReady(t,ex) submitTask(ex) rankUps() sectTick()`（每年：月俸、俸祿、任務過期、大比、挖角）、`switchSect()`、自創宗門 `STASK() ownTaskTick() rankOf(m) promoGate(m)`、`renderSectTasks()`；大比／挖角係 `HOME_EV` 入面 `w:0` 嘅事件，用 `queueEv(k)` 排 |
| 籠絡弟子 | 送靈石、送藥、傳功、大弟子 `headD()`；`askConfirm(問, 說明, 確定動作, id, 返轉頭動作)` 唔可以返轉頭嘅動作先彈窗問 |
| 丹價行情 | `prices()` 行情指數、`retailPrice()`、`makeShopPill()` |
| 丹室、丹瓶、儲物袋、兵器防具 | `DR()`（`wpn` `arm` 等級）、`ROOM_LV BOTTLES BAGS WEAPONS ARMORS`、`buyGear(kind)`、`storePill() roomDecay() bagAdd()`、`renderRoom() renderMarket() renderStock()` |
| 丹市 | `basePrice() satMult() quoteN() doSell(n,auto,quiet)`、黑市事件 |
| 道侶 | `DL()`、`DL_KIND`、`dlTick() showDL() giftPill()` |
| 奇遇 | `ADV` 陣列（`w` 權重、`ctx` herb／yao／both、`run(lines)` 可回傳 `{lines, choice, death}`）、`adventure() resolveAdv()` |
| 弟子幫手 | `isZp(m)` 正派心性、`noDrift(m)`（正派同親傳忠誠唔跌）、`daiBrew()` 親傳代煉（`car.daiOn`）、`discYear()` 營運收入／代交任務／採藥／弟子奇遇，全部用 `log()` 一行字 |
| 忠誠度、升降 | `loy() addLoy() loyMult() loyBase() promote() demote() loyTick()` |
| 生平 | `LN()` 每世計數、`bio()`、`bioTrack()`（喺 `afterAction` 比較前後狀態自動記大事）、`lifeRecord() renderLives()` |
| 入室弟子 | `APT` 資質、`rollApt()` 抽籤連保底、`yearTick()`（每年：入室修煉壽元、忠誠、道侶、丹市、行情、丹室流失、慕名求見） |
| 任務（外務） | `MS_T`、`MSN()`（`pl.msn={offers, active}`）、`newMission() missionTick() msChance() msScore() showMissions() msAction()`；`onMs(m)` 出任務嘅人唔計日常工作；hub key `ms2` |
| 工作版 | `showJobs()` 分組、`canUp/canDown rankUp/rankDown`、`autoJobs()` |
| 傳授 | `teachTarget(who) teachWho(cat,sel) showTeach() teachBook()`；人物 `bk` 已學書、`wx` 武學數 |
| 人物中心 | `HUB` 身份 tab、`hubPeople(cat)`、`hubPop(cat, sel, 詳情html)`（闊版 pop，上 tab、左名單、右詳情）、`hubShow(cat, id)` 路由、`openHub()`、`orgHtml()`、`hubKey()`；各詳情（`showDL showKid showMaster showNPC showDisciple showJobs showJiming`）都經 `hubPop` 出；工作掣 `jobChips(who, map, cur)` + `setJob()` |
| 丹書 | `renderBooks()` 子分頁 `bookSub`（rec ord lib self cx）＋ `bookSel`、`recDetail()`、`orderCard()`、`quickBrew(name)` 配好即煉；`mtCodex` 跳去 `bookSub='cx'` |
| 丹室畫面 | `renderRoom()`（冇存貨嘅丹方放 `.slot.ghost` 空瓶，撳 `rbrew` 即煉）：`ROOM_SLOTS ROOM_SKIN BOTTLE_SKIN GRADE_COL bottleSvg()`、`roomSel` |
| 中間六格 | `renderInner() showKids() showInnerList() showJiming() showDLCell() showDisciple() showDraw() onPopClick()` |
| 魔頭 | `MO()`、`becomeMo() reform() grab() massacre()`（屠村）`moTick()`（奴隸挖礦、放血、逃走、圍剿）、`sacrifice(id)`、`P_ROLES`、`PRISON_CAP=Infinity`；入魔時 `renderAll()` 喺 `<html>` 加 `.mo`（白骨主題 token）、改標題同斬妖掣；`xieN()` 丹協／魔協；藥材 `xuerou` 只有魔頭解鎖 |
| 藏書與丹書 | `BOOKS`、`bookFx()`、`recipes() mastery()`、`previewRecipe()`、`applyRecipe()`、`recordBrew()`、`gradeFromQ() nameFor()`、商行藏書 |
| 丹途 | `CERT SKILL_N SECTS SECT_LV PERS ROLES`、`C()`、`capOf() innerCap()`、`team()`（所有加成匯總）、`careerAfterBrew()`、考證、入會、開宗 |
| 核心演算 | `analyse()` → `{Q, S, boom, ideal, dev, dom, flags, notes, mName, mCount…}`；`successRate()`、`yieldCount()` |
| 煉丹 | `brew() → turnMsg() → finish() → makePill()` |
| 疊層卡 | `openOverlay() showPill() showOutcome() useOne()` |
| 食丹 | `effects(p, realm)`、`eat() test() testBy() testByMortal()` |
| 生死 | `checkLife() endLife() showDeath()`、轉世 |
| 導航 | `SECS`（區同子分頁 leaf）、`mTab`＝而家 leaf、`secLast` 記住每區上次分頁、`TAB_ALIAS`（舊名 shop→mkt、rel→people、codex→book）、`drawNav() renderModal() openTab(leaf)`；`#mBody` click 按 leaf 分派（people→`onPopClick`、car/sect/pr→`onCareerClick`、book/wx→`onBookClick`、產業→`onBookClick`+`onRoomClick`）；人物中心 `hubPop()` 直接畫入主視窗 |

### 核心流程

- **任何改變狀態嘅動作之後都要叫 `afterAction()`**：

  ```js
  afterAction() = moTick(); yearTick(); bioTrack(); checkLife(); checkAch(); fixCfg(); persist(); renderAll(); kickEvents();
  ```

- **時間**：開爐用 `nextSeason()`（`pl.season` 0-3，四季先 `age+1`）；其他動作用 `P().age += 1` 代表過一年，之後叫 `afterAction()`。每年要做嘅嘢放喺 `yearTick()` 個 while 迴圈入面（用 `pl.ly` 計過咗幾多年）。
- **瓶頸**：`breakthrough()` 只會將修為封頂 100，唔會自動升境界；`atNeck()` 判斷瓶頸，`tryBreak(機會, 點樣)` 喺食丹、打架贏、論道、雙修、打坐、`neckGo()` 閉關衝關度試突破，回傳一句訊息（冇突破就係空字串）。左上角 `#neckBtn` → `showNeck()`。
- **修為**：正數修為一律經 `gainCult()`（已乘 `cultMul()`＝資質×內功）；食丹喺 `eat()` 另外乘。
- **親傳**：親傳弟子仲喺 `inner()` 陣列入面，但唔計入入室名額，用 `innerN()` 數入室人數。
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
          rank /* 0-4 */, gx /* 功勞 */, fail, log: [賞罰紀錄], tasks: [{kind, g, n, left, dz}], dabi, stasks: [{kind, who, last}],
          members: [記名], inner: [入室], cands: [招募候選], visitors: [慕名求見], pity, head, nid},
    mo: {on, infamy, prisoners, caught, killed, last, nid},
    dl: 道侶|null, bag: {藥材id: 數量}, dr: {lvl, stacks, bottle, bagLv},
    n: {每世計數}, bio: [{a, t}], bt: {bioTrack 上次狀態}, ly: 上次 yearTick 年歲,
    born /* false＝未揀資質出身 */, apt /* 0-4 */, id /* IDS key */, moral /* −100..100 */,
    kids: [{id, name, f, apt, age, sk, par, aff /* 親情 */, school}], orders: [{id, who, name, g, need, fair, wait, cfg, special, sat, urgent}],
    unl: [上山搵藥解鎖嘅藥材id], wx: {武學書id: 0-100}, wxMain, npcs: [{…, mo /* 魔道中人 */, dk /* 道侶種類 */, vis /* 拜訪次數 */}]
  }
}
```

- 舊存檔冇 `born`：載入時當佢係中等資質散修（`born:true, apt:1, id:'sanxiu'`）。新一世 `newPlayer()` 係 `born:false`，啟動時會彈 `showBirth()`。
- 所有浮窗（`#modal>.mbox`、`.pbox`）固定同一大細 `min(940px,100%) × min(720px,100%)`，內容喺 `.mscroll`／`#popBody` 入面碌。
- 弟子階級固定係 記名 → 外門 → 內門 → 入室 → 親傳（`RANKS`），五個名唔可以撞名；升降用 `upRank() downRank() canUp() canDown() rankUp() rankDown()`，掣上面一定寫下一級嘅名。
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

- `tests/smoke.py` 會檢查（導航用 `#ms_<區>`、`#ml_<leaf>`）：冇 JS 錯誤；電腦同手機一屏過；新存檔彈投胎；所有彈窗分頁大細一樣；丹途門派冇秘咒欄；打坐、開爐出丹；秘咒有效。新存檔一定要先撳 `#bGo` 入世先玩得。
- 測試用秘咒：`急急如律令 點石成金 丹道通神 走火入魔 天劫將至 大仁大義 大奸大惡 有求必應 開枝散葉 魔女知己 壽元將盡 武學大成 拜入山門 宗門大比 五年大比 有人挖角 有事相求 桃李天下 修為圓滿 名滿天下 臭名遠播 踢館 天賜良緣 江湖告急`（喺 `cheat()`）。
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
