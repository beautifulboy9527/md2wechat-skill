# md2wechat

<div align="center">

**鐢?Markdown 鍐欏叕浼楀彿鏂囩珷锛屽儚鍙戞湅鍙嬪湀涓€鏍风畝鍗?*

[![Go Version](https://img.shields.io/badge/Go-1.24+-00ADD8?logo=go)](https://golang.org)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![GitHub Release](https://img.shields.io/badge/download-latest-green)](https://github.com/geekjourneyx/md2wechat-skill/releases)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-purple)](#-claude-code-闆嗘垚)

[蹇€熷紑濮媇(#-5鍒嗛挓蹇€熶笂鎵? 鈥?[Claude Code](#-claude-code-闆嗘垚) 鈥?[鍔熻兘浠嬬粛](#-鏍稿績鍔熻兘) 鈥?[浣跨敤璇存槑](#-浣跨敤鏂规硶) 鈥?[甯歌闂](#-甯歌闂)

---

## 馃殌 Claude Code 鐢ㄦ埛锛堟帹鑽愶級

鍦?Claude Code 涓繍琛屼互涓嬪懡浠ゅ嵆鍙娇鐢細

```bash
/plugin marketplace add geekjourneyx/md2wechat-skill
/plugin install md2wechat@geekjourneyx-md2wechat-skill
```

鐒跺悗鐩存帴瀵硅瘽锛?*"璇风敤绉嬫棩鏆栧厜涓婚灏?article.md 杞崲涓哄井淇″叕浼楀彿鏍煎紡"**

---

</div>

---

## 鉁?杩欐槸浠€涔堬紵

**md2wechat** 鏄竴涓浣犵殑寰俊鍏紬鍙峰啓浣滄洿楂樻晥鐨勭鍣ㄣ€?
> 馃挕 **涓€鍙ヨ瘽鐞嗚В**锛氱敤 Markdown 鍐欐枃绔?鈫?涓€閿浆鎹?鈫?鑷姩鍙戝埌寰俊鑽夌绠?
**閫傚悎璋佺敤锛?*

| 浣犳槸 | 鐥涚偣 | md2wechat 甯綘 |
|------|------|---------------|
| 馃摑 鍐呭鍒涗綔鑰?| 寰俊缂栬緫鍣ㄥお闅剧敤锛屾帓鐗堣姳鏃堕棿 | Markdown 鍐欎綔锛岃嚜鍔ㄦ帓鐗?|
| 馃捈 浜у搧缁忕悊 | 瑕佸彂鍏憡锛屼絾涓嶄細 HTML | 涓嶇敤瀛︿唬鐮侊紝涓€琛屽懡浠ゆ悶瀹?|
| 馃懆鈥嶐煉?绋嬪簭鍛?| 涔犳儻 Markdown锛岃鍘屽井淇＄紪杈戝櫒 | 淇濇寔浣犵殑鍐欎綔涔犳儻 |
| 馃 AI 鐢ㄦ埛 | 鐢?AI 鐢熸垚鍐呭锛屼絾瑕佹墜鍔ㄥ鍒剁矘璐?| AI 鐢熸垚 鈫?寰俊鑽夌锛屾棤缂濊鎺?|

---

## 馃幆 鏍稿績鍔熻兘

```mermaid
flowchart LR
    A[鐢?Markdown 鍐欐枃绔燷 --> B{閫夋嫨妯″紡}

    B -->|API 妯″紡| C[璋冪敤 md2wechat.cn API]
    C --> D[鑾峰彇 HTML]

    B -->|AI 妯″紡 鎺ㄨ崘| E[Claude AI 鐢熸垚 HTML]
    E --> F[绮剧編鎺掔増]

    D --> G[棰勮鏁堟灉]
    F --> G

    G --> H{婊℃剰鍚梷
    H -->|涓嶆弧鎰弢 B
    H -->|婊℃剰| I[涓婁紶鍥剧墖]
    I --> J[鍙戦€佸埌寰俊鑽夌绠盷
    J --> K[瀹屾垚]

    classDef nodeA fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    classDef nodeE fill:#fff3e0,stroke:#ff9800,color:#e65100
    classDef nodeJ fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    classDef nodeK fill:#c8e6c9,stroke:#4caf50,color:#1b5e20

    class A nodeA
    class E nodeE
    class J nodeJ
    class K nodeK
```

### 涓ょ杞崲妯″紡

| 妯″紡 | 閫傚悎璋?| 鐗圭偣 | 鏍峰紡 |
|------|--------|------|------|
| **API 妯″紡** | 杩芥眰绋冲畾銆佸揩閫?| 璋冪敤 md2wechat.cn API锛岀绾у搷搴?| 绠€娲佷笓涓?|
| **AI 妯″紡** 猸?| 杩芥眰绮剧編鎺掔増 | Claude AI 鐢熸垚锛屾牱寮忔洿涓板瘜 | 绉嬫棩鏆栧厜 / 鏄ユ棩娓呮柊 / 娣辨捣闈欒哀 |

### 瀹屾暣宸ヤ綔娴佺▼

```mermaid
flowchart LR
    A1[Markdown 鍐欎綔] --> A2[鎻掑叆鍥剧墖]
    A2 --> B1{閫夋嫨妯″紡}

    B1 -->|API| B2[md2wechat.cn]
    B1 -->|AI| B3[Claude AI]

    B2 --> B4[HTML 鐢熸垚]
    B3 --> B4

    B4 --> C1[棰勮鏁堟灉]
    C1 --> C2{婊℃剰鍚梷

    C2 -->|璋冩暣| B1
    C2 -->|OK| C3[涓婁紶鍥剧墖]
    C3 --> C4[鍙戦€佽崏绋縘
    C4 --> C5[瀹屾垚]

    classDef write fill:#e3f2fd,stroke:#2196f3,color:#0d47a1
    classDef ai fill:#fff3e0,stroke:#ff9800,color:#e65100
    classDef done fill:#e8f5e9,stroke:#4caf50,color:#1b5e20
    classDef success fill:#c8e6c9,stroke:#4caf50,color:#1b5e20

    class A1,A2 write
    class B3 ai
    class C4,C5 done
```

---

## 馃殌 5鍒嗛挓蹇€熶笂鎵?
### 绗竴姝ワ細涓嬭浇杞欢

> 馃挕 **鏈€鏂扮増鏈?*锛氳闂?[Releases 椤甸潰](https://github.com/geekjourneyx/md2wechat-skill/releases) 涓嬭浇

| 浣犵殑绯荤粺 | 涓嬭浇閾炬帴 | 瀹夎浣嶇疆 |
|----------|----------|----------|
| 馃獰 **Windows** | [涓嬭浇 .exe](https://github.com/geekjourneyx/md2wechat-skill/releases/latest/download/md2wechat-windows-amd64.exe) | 浠绘剰鏂囦欢澶癸紙鎴?`C:\Windows\System32\`锛?|
| 馃崕 **Mac Intel** | [涓嬭浇](https://github.com/geekjourneyx/md2wechat-skill/releases/latest/download/md2wechat-darwin-amd64) | `/usr/local/bin/` 鎴?`~/.local/bin/` |
| 馃崕 **Mac M1/M2** | [涓嬭浇](https://github.com/geekjourneyx/md2wechat-skill/releases/latest/download/md2wechat-darwin-arm64) | `/usr/local/bin/` 鎴?`~/.local/bin/` |
| 馃惂 **Linux** | [涓嬭浇](https://github.com/geekjourneyx/md2wechat-skill/releases/latest/download/md2wechat-linux-amd64) | `/usr/local/bin/` 鎴?`~/.local/bin/` |

**瀹夎姝ラ**锛?
<details>
<summary><b>Windows 瀹夎鏂规硶</b></summary>

1. 涓嬭浇 `md2wechat-windows-amd64.exe`
2. 閲嶅懡鍚嶄负 `md2wechat.exe`锛堝彲閫夛級
3. 鏀惧埌浠绘剰鏂囦欢澶癸紝鎴栧鍒跺埌 `C:\Windows\System32\`锛堝叏灞€鍙敤锛?4. 鎵撳紑 CMD 鎴?PowerShell锛岃緭鍏?`md2wechat --help` 娴嬭瘯

</details>

<details>
<summary><b>Mac/Linux 瀹夎鏂规硶</b></summary>

**鏂规硶涓€锛氬懡浠よ瀹夎锛堟帹鑽愶級**
```bash
# 涓嬭浇骞剁Щ鍔ㄥ埌绯荤粺鐩綍
curl -Lo md2wechat https://github.com/geekjourneyx/md2wechat-skill/releases/latest/download/md2wechat-linux-amd64
chmod +x md2wechat
sudo mv md2wechat /usr/local/bin/

# 娴嬭瘯
md2wechat --help
```

**鏂规硶浜岋細鐢ㄦ埛鐩綍瀹夎锛堟棤闇€ sudo锛?*
```bash
mkdir -p ~/.local/bin
curl -Lo ~/.local/bin/md2wechat https://github.com/geekjourneyx/md2wechat-skill/releases/latest/download/md2wechat-linux-amd64
chmod +x ~/.local/bin/md2wechat

# 娣诲姞鍒?PATH锛堝鏋滆繕娌℃湁锛?echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # 鎴?~/.zshrc
source ~/.bashrc

# 娴嬭瘯
md2wechat --help
```

</details>

> 鈿狅笍 **Mac 鐢ㄦ埛**锛氫笅杞藉悗濡傛灉鎻愮ず銆屾棤娉曟墦寮€銆嶏紝鍙抽敭鐐瑰嚮 鈫?鎵撳紑 鈫?浠嶈鎵撳紑

### 绗簩姝ワ細閰嶇疆寰俊锛堝彧闇€涓€娆★級

```bash
md2wechat config init
```

鐢ㄨ浜嬫湰鎵撳紑鐢熸垚鐨勯厤缃枃浠讹紙浼氭樉绀鸿矾寰勶級锛屽～鍏ヤ袱涓俊鎭細

| 閰嶇疆椤?| 鏄粈涔?| 鍦ㄥ摢鑾峰彇 |
|--------|--------|----------|
| AppID | 鍏紬鍙峰敮涓€鏍囪瘑 | mp.weixin.qq.com 鈫?璁剧疆涓庡紑鍙?鈫?鍩烘湰閰嶇疆 |
| Secret | API 瀵嗛挜 | 鍚屼笂锛岄渶瑕佺鐞嗗憳鏉冮檺 |

### 绗笁姝ワ細寮€濮嬩娇鐢?
```bash
# 1. 鐢?Markdown 鍐欏ソ鏂囩珷锛堝亣璁炬枃浠跺彨 article.md锛?
# 2. 棰勮鏁堟灉
md2wechat convert article.md --preview

# 3. 鍙戦€佸埌寰俊鑽夌绠?md2wechat convert article.md --draft --cover cover.jpg
```

> 馃挕 **灏忚创澹?*锛氱涓€娆′娇鐢ㄦ椂锛屽懡浠や細鑷姩寮曞浣犲畬鎴愰厤缃€?
---

## 馃摉 浣跨敤鏂规硶

### 鍩虹鍛戒护

```bash
# 棰勮杞崲鏁堟灉锛堜笉鍙戦€侊級
md2wechat convert article.md --preview

# 杞崲骞朵繚瀛樹负 HTML 鏂囦欢
md2wechat convert article.md -o output.html

# 浣跨敤 AI 妯″紡鐢熸垚绮剧編鎺掔増
md2wechat convert article.md --mode ai --theme autumn-warm --preview
```

### 瀹屾暣鍙戝竷娴佺▼

```bash
# 涓€姝ュ埌浣嶏細杞崲 + 涓婁紶鍥剧墖 + 鍙戦€佽崏绋?md2wechat convert article.md --draft --cover cover.jpg

# 娴佺▼璇存槑锛?# 1. 灏?Markdown 杞崲涓哄井淇℃牸寮?HTML
# 2. 涓婁紶灏侀潰鍥剧墖鍒板井淇＄礌鏉愬簱
# 3. 鍒涘缓鑽夌骞舵帹閫佸埌寰俊鍚庡彴
```

### AI 妯″紡涓婚閫夋嫨

| 涓婚鍚?| 鍛戒护 | 椋庢牸 | 閫傚悎鍐呭 |
|--------|------|------|----------|
| 馃煚 **绉嬫棩鏆栧厜** | `--theme autumn-warm` | 娓╂殩姗欒壊璋?| 鎯呮劅鏁呬簨銆佺敓娲婚殢绗?|
| 馃煝 **鏄ユ棩娓呮柊** | `--theme spring-fresh` | 娓呮柊缁胯壊璋?| 鏃呰鏃ヨ銆佽嚜鐒朵富棰?|
| 馃數 **娣辨捣闈欒哀** | `--theme ocean-calm` | 涓撲笟钃濊壊璋?| 鎶€鏈枃绔犮€佸晢涓氬垎鏋?|

### API 妯″紡涓婚閫夋嫨

| 涓婚鍚?| 鍛戒护 | 椋庢牸 | 閫傚悎鍐呭 |
|--------|------|------|----------|
| **榛樿** | `--mode api` 鎴栭粯璁?| 绠€娲佷笓涓?| 閫氱敤鍐呭 |
| **bytedance** | `--theme bytedance` | 瀛楄妭璺冲姩椋庢牸 | 绉戞妧璧勮 |
| **apple** | `--theme apple` | Apple 鏋佺畝椋庢牸 | 浜у搧璇勬祴 |
| **sports** | `--theme sports` | 杩愬姩娲诲姏椋庢牸 | 浣撹偛鍐呭 |
| **chinese** | `--theme chinese` | 涓浗浼犵粺鏂囧寲椋庢牸 | 鏂囧寲鏂囩珷 |
| **cyber** | `--theme cyber` | 璧涘崥鏈嬪厠椋庢牸 | 鍓嶆部绉戞妧 |

### 鍥剧墖澶勭悊

```bash
# 涓婁紶鍗曞紶鍥剧墖鍒板井淇＄礌鏉愬簱
md2wechat upload_image photo.jpg

# 涓嬭浇缃戠粶鍥剧墖骞朵笂浼?md2wechat download_and_upload https://example.com/image.jpg
```

---

## 馃 AI 妯″紡璇﹁В

### 浠€涔堟槸 AI 妯″紡锛?
**AI 妯″紡**浣跨敤 Claude 澶фā鍨嬫潵鐢熸垚绮剧編鐨勫叕浼楀彿鎺掔増锛岃€屼笉鏄畝鍗曠殑 API 杞崲銆?
```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                    AI 妯″紡宸ヤ綔娴佺▼                          鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                                                            鈹?鈹?  1. 浣犵敤 Markdown 鍐欐枃绔?                                   鈹?鈹?             鈫?                                              鈹?鈹?  2. md2wechat 鎻愬彇鏂囩珷缁撴瀯                                  鈹?鈹?             鈫?                                              鈹?鈹?  3. 鏋勫缓涓撲笟鐨勬帓鐗堟彁绀鸿瘝 (Prompt)                           鈹?鈹?             鈫?                                              鈹?鈹?  4. Claude AI 鏍规嵁鎻愮ず璇嶇敓鎴?HTML                          鈹?鈹?             鈫?                                              鈹?鈹?  5. 杩斿洖绗﹀悎寰俊瑙勮寖鐨?HTML                                 鈹?鈹?                                                            鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

### AI 妯″紡鐨勪紭鍔?
| 瀵规瘮椤?| API 妯″紡 | AI 妯″紡 |
|--------|----------|----------|
| 鍝嶅簲閫熷害 | 鈿?绉掔骇 | 馃悽 10-30绉?|
| 鎺掔増璐ㄩ噺 | 馃憤 鏍囧噯瑙勮寖 | 馃専 绮剧編澶氭牱 |
| 鏍峰紡閫夋嫨 | 2-3 绉?| 鏃犻檺鍙兘 |
| 鎴愭湰 | 浣?| 浣跨敤 Claude AI |
| 閫傚悎鍦烘櫙 | 鏃ュ父鏂囩珷 | 閲嶈鏂囩珷銆佸搧鐗屽唴瀹?|

### 鍦?Claude Code 涓娇鐢?AI 妯″紡

濡傛灉浣犱娇鐢?**Claude Code**锛孉I 妯″紡浼氳嚜鍔ㄨ皟鐢ㄥ唴缃殑 Claude锛屾棤闇€棰濆閰嶇疆锛?
```bash
# 鍦?Claude Code 涓洿鎺ヨ繍琛?md2wechat convert article.md --mode ai --theme autumn-warm
```

---

## 鈿欙笍 閰嶇疆璇存槑

### 閰嶇疆鏂囦欢浣嶇疆

```
~/.config/md2wechat/config.yaml    # 鍏ㄥ眬閰嶇疆锛堟帹鑽愶級
```

### 閰嶇疆椤硅鏄?
```yaml
# 寰俊鍏紬鍙烽厤缃紙蹇呴渶锛?wechat:
  appid: "浣犵殑AppID"
  secret: "浣犵殑Secret"

# API 閰嶇疆
api:
  md2wechat_key: "md2wechat.cn 鐨?API Key"  # API 妯″紡闇€瑕?  convert_mode: "api"                       # 榛樿妯″紡锛歛pi 鎴?ai
  default_theme: "default"                  # 榛樿涓婚
  http_timeout: 30                          # 瓒呮椂鏃堕棿锛堢锛?
# 鍥剧墖澶勭悊閰嶇疆
image:
  compress: true           # 鑷姩鍘嬬缉澶у浘
  max_width: 1920         # 鏈€澶у搴?  max_size_mb: 5          # 鏈€澶ф枃浠跺ぇ灏忥紙MB锛?```

---

## 馃搧 椤圭洰缁撴瀯

```
md2wechat-skill/
鈹溾攢鈹€ cmd/                    # 鍛戒护琛屽伐鍏?鈹?  鈹斺攢鈹€ md2wechat/         # 涓荤▼搴?鈹溾攢鈹€ internal/              # 鏍稿績鍔熻兘妯″潡
鈹?  鈹溾攢鈹€ converter/        # 杞崲鍣紙API/AI锛?鈹?  鈹溾攢鈹€ draft/            # 鑽夌鏈嶅姟
鈹?  鈹溾攢鈹€ image/            # 鍥剧墖澶勭悊
鈹?  鈹溾攢鈹€ wechat/           # 寰俊 API 灏佽
鈹?  鈹斺攢鈹€ config/           # 閰嶇疆绠＄悊
鈹溾攢鈹€ docs/                 # 璇︾粏鏂囨。
鈹?  鈹溾攢鈹€ USAGE.md          # 浣跨敤鏁欑▼
鈹?  鈹溾攢鈹€ FAQ.md            # 甯歌闂
鈹?  鈹斺攢鈹€ TROUBLESHOOTING.md # 鏁呴殰鎺掓煡
鈹溾攢鈹€ examples/             # 绀轰緥鏂囩珷
鈹溾攢鈹€ scripts/              # 瀹夎鑴氭湰
鈹斺攢鈹€ bin/                  # 缂栬瘧濂界殑浜岃繘鍒舵枃浠?```

---

## 馃敡 楂樼骇瀹夎

### 鏂瑰紡涓€锛欸o 宸ュ叿閾?
```bash
go install github.com/geekjourneyx/md2wechat-skill/cmd/md2wechat@latest
```

### 鏂瑰紡浜岋細涓€閿畨瑁呰剼鏈?
**Mac/Linux锛?*
```bash
curl -fsSL https://raw.githubusercontent.com/geekjourneyx/md2wechat-skill/main/scripts/install.sh | bash
```

**Windows PowerShell锛?*
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/geekjourneyx/md2wechat-skill/main/scripts/install.ps1'))
```

### 鏂瑰紡涓夛細浠庢簮鐮佺紪璇?
```bash
git clone https://github.com/geekjourneyx/md2wechat-skill.git
cd md2wechat-skill
make build
```

---

## 馃 Claude Code 闆嗘垚

md2wechat 鎻愪緵浜?**Claude Code Skill**锛岃浣犲湪 Claude Code 涓洿鎺ヤ娇鐢ㄨ嚜鐒惰瑷€杞崲鏂囩珷銆?
### 瀹夎鏂瑰紡

#### 鏂瑰紡涓€锛歅lugin Marketplace锛堟帹鑽愶紝鏈€绠€鍗曪級

鍦?Claude Code 涓繍琛屼互涓嬪懡浠わ細

```bash
# 娣诲姞鎻掍欢甯傚満
/plugin marketplace add geekjourneyx/md2wechat-skill

# 瀹夎鎻掍欢
/plugin install md2wechat@geekjourneyx-md2wechat-skill
```

瀹夎鍚庯紝鐩存帴鍦?Claude Code 涓璇濆嵆鍙娇鐢細

```
璇风敤绉嬫棩鏆栧厜涓婚灏?article.md 杞崲涓哄井淇″叕浼楀彿鏍煎紡
```

#### 鏂瑰紡浜岋細椤圭洰鍐呬娇鐢?
鍏嬮殕椤圭洰鍚庯紝Skill 鑷姩鍙敤锛?
```bash
git clone https://github.com/geekjourneyx/md2wechat-skill.git
cd md2wechat-skill
# 鍦?Claude Code 涓洿鎺ヤ娇鐢?```

#### 鏂瑰紡涓夛細鍏ㄥ眬瀹夎

灏?Skill 澶嶅埗鍒板叏灞€鐩綍锛?
```bash
# 澶嶅埗鍒板叏灞€鎶€鑳界洰褰?cp -r skill/md2wechat ~/.claude/skills/
```

#### 鏂瑰紡鍥涳細鍒涘缓绗﹀彿閾炬帴

```bash
ln -s /path/to/md2wechat-skill/skill/md2wechat ~/.claude/skills/md2wechat
```

### 椤圭洰缁撴瀯

```
md2wechat-skill/
鈹溾攢鈹€ .claude-plugin/        # 鎻掍欢娓呭崟
鈹?  鈹斺攢鈹€ plugin.json
鈹溾攢鈹€ skill/                 # Claude Code Skill
鈹?  鈹斺攢鈹€ md2wechat/
鈹?      鈹溾攢鈹€ SKILL.md       # 鎶€鑳藉畾涔?鈹?      鈹溾攢鈹€ references/    # 鍙傝€冩枃妗?鈹?      鈹?  鈹溾攢鈹€ themes.md      # 涓婚鎸囧崡
鈹?      鈹?  鈹溾攢鈹€ html-guide.md  # HTML 瑙勮寖
鈹?      鈹?  鈹溾攢鈹€ image-syntax.md # 鍥剧墖璇硶
鈹?      鈹?  鈹斺攢鈹€ wechat-api.md  # API 鍙傝€?鈹?      鈹斺攢鈹€ scripts/       # 鎵ц鑴氭湰
鈹斺攢鈹€ themes/                # AI 涓婚閰嶇疆
    鈹溾攢鈹€ autumn-warm.yaml
    鈹溾攢鈹€ spring-fresh.yaml
    鈹斺攢鈹€ ocean-calm.yaml
```

---

## 馃帗 浣跨敤绀轰緥

### 绀轰緥 1锛氭妧鏈崥涓?
```bash
# 鍐欏ソ鎶€鏈枃绔?vim my-tech-post.md

# 浣跨敤绠€娲佺殑 API 妯″紡杞崲
md2wechat convert my-tech-post.md --preview

# 婊℃剰鍚庡彂閫佽崏绋?md2wechat convert my-tech-post.md --draft --cover cover.jpg
```

### 绀轰緥 2锛氫骇鍝佺粡鐞嗗彂鍏憡

```bash
# AI 鐢熸垚浜у搧鍏憡鍐呭锛岀劧鍚?md2wechat convert announcement.md --mode ai --theme ocean-calm --draft --cover product-logo.png
```

### 绀轰緥 3锛氱敓娲绘柟寮忓崥涓?
```bash
# 浣跨敤鏄ユ棩娓呮柊涓婚
md2wechat travel-diary.md --mode ai --theme spring-fresh --preview
```

---

## 鉂?甯歌闂

<details>
<summary><b>Q: 蹇呴』瑕佷細缂栫▼鎵嶈兘鐢ㄥ悧锛?/b></summary>

**A: 涓嶉渶瑕侊紒** 鍙浼氱敤鍛戒护琛岋紙缁堢锛夊氨鍙互銆傚鏋滄槸 Windows 鐢ㄦ埛锛屼笅杞?.exe 鏂囦欢鍚庯紝鍦?CMD 鎴?PowerShell 涓繍琛屽懡浠ゅ嵆鍙€?</details>

<details>
<summary><b>Q: AI 妯″紡闇€瑕佷粯璐瑰悧锛?/b></summary>

**A:** AI 妯″紡浣跨敤 Claude 鑳藉姏锛?- 濡傛灉浣犲湪 **Claude Code** 涓娇鐢紝鐩存帴璋冪敤鍐呯疆 AI
- 濡傛灉浣犳兂鑷繁鎺ュ叆锛岄渶瑕侀厤缃?OpenAI 鍏煎鐨?API
</details>

<details>
<summary><b>Q: 鏀寔鍝簺 Markdown 璇硶锛?/b></summary>

**A:** 鏀寔甯哥敤璇硶锛?- 鏍囬锛? ## ###锛?- 鍒楄〃锛堟棤搴忋€佹湁搴忥級
- 绮椾綋銆佹枩浣撱€佽鍐呬唬鐮?- 浠ｇ爜鍧楋紙甯﹁娉曢珮浜級
- 寮曠敤鍧?- 鍒嗗壊绾?- 鍥剧墖銆侀摼鎺?- 琛ㄦ牸
</details>

<details>
<summary><b>Q: 鐢熸垚鐨勬枃绔犲彲浠ョ洿鎺ュ湪寰俊缂栬緫鍣ㄤ腑缂栬緫鍚楋紵</b></summary>

**A:** 鍙互锛佽崏绋垮彂閫佸悗锛屼綘鍙互鐧诲綍寰俊鍏紬骞冲彴锛屽湪鑽夌绠变腑缁х画缂栬緫銆?</details>

---

## 馃摎 鏇村鏂囨。

| 鏂囨。 | 璇存槑 |
|------|------|
| [鏂版墜鍏ラ棬鎸囧崡](QUICKSTART.md) | **寮虹儓鎺ㄨ崘锛?* 璇︾粏鐨勫浘鏂囨暀绋?|
| [瀹屾暣浣跨敤璇存槑](docs/USAGE.md) | 鎵€鏈夊懡浠ゅ拰閫夐」 |
| [甯歌闂](docs/FAQ.md) | 20+ 甯歌闂瑙ｇ瓟 |
| [鏁呴殰鎺掓煡](docs/TROUBLESHOOTING.md) | 閬囧埌闂鐪嬭繖閲?|

---

## 馃 璐＄尞

娆㈣繋鎻愪氦 Issue 鍜?Pull Request锛?
濡傛灉浣犳湁濂界殑鎯虫硶鎴栧彂鐜颁簡 bug锛岃闅忔椂鎻?issue銆?
---

## 馃搫 璁稿彲璇?
[MIT License](LICENSE)

---

## 馃懆鈥嶐煉?浣滆€?
**geekjourney** 鈥?鏋佸/鍒涗綔鑰?AI 鎺㈢储鑰?
- 馃寪 涓汉涓婚〉: [geekjourney.dev](https://geekjourney.dev)
- 馃惁 X/Twitter: [@seekjourney](https://x.com/seekjourney/)
- 馃摫 鍏紬鍙? **鏋佸鏉板凹**

---

<div align="center">

**璁╁叕浼楀彿鍐欎綔鏇寸畝鍗?* 猸?
[涓婚〉](https://github.com/geekjourneyx/md2wechat-skill) 鈥?[鏂囨。](docs) 鈥?[鍙嶉](https://github.com/geekjourneyx/md2wechat-skill/issues)

Made with 鉂わ笍 by [geekjourney](https://geekjourney.dev)

</div>
