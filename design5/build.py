#!/usr/bin/env python3
"""design5: 経理くん LP デザイン5案。本文は ../index.html から抜き出して使う（文言を手で写さない）。
usage: python3 build.py  → v1.html〜v5.html を生成
"""
import re, html, pathlib

HERE = pathlib.Path(__file__).parent
SRC = (HERE.parent / "index.html").read_text()
BASE = "https://yukitchy.github.io/money-setup-lp/design5/"


def grab(pat, s=SRC):
    return re.findall(pat, s, re.S)


def sec(label):
    return re.search(r'<div class="sec-label">%s</div>(.*?)(?:</section>|</div>\s*\n\s*<footer>)' % label, SRC, re.S).group(1)


C = {}
hero = re.search(r'<div class="hero">(.*?)</div>\s*\n\s*<section>', SRC, re.S).group(1)
C["kicker"] = grab(r'<div class="kicker">(.*?)</div>', hero)[0]
C["h1"] = grab(r'<h1[^>]*>(.*?)</h1>', hero)[0]
C["hero_p"] = grab(r'<p>(.*?)</p>', hero)
s = sec("CHECK"); C["check_h2"] = grab(r'<h2[^>]*>(.*?)</h2>', s)[0]; C["pains"] = grab(r'<li>(.*?)</li>', s)
s = sec("SERVICE"); C["svc_h2"] = grab(r'<h2[^>]*>(.*?)</h2>', s)[0]
C["svc"] = [dict(no=a, h3=b, p=c) for a, b, c in grab(r'<div class="no">(.*?)</div>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', s)]
C["table"] = grab(r'(<table class="view">.*?</table>)', s)[0]
C["view_note"] = grab(r'<div class="view-note">(.*?)</div>', s)[0]
s = sec("FLOW"); C["flow_h2"] = grab(r'<h2[^>]*>(.*?)</h2>', s)[0]
C["steps"] = [dict(n=a, h3=b, p=c) for a, b, c in grab(r'<div class="num[^"]*">(.*?)</div>\s*<div>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', s)]
s = sec("PROOF"); C["proof_h2"] = grab(r'<h2[^>]*>(.*?)</h2>', s)[0]
C["proof"] = [dict(h3=a, p=b) for a, b in grab(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', s)]
s = sec("FAQ"); C["faq_h2"] = grab(r'<h2[^>]*>(.*?)</h2>', s)[0]
C["faq"] = [dict(q=a, a=b) for a, b in grab(r'<summary>(.*?)</summary>\s*<p>(.*?)</p>', s)]
s = re.search(r'<div class="cta">(.*?)</div>\s*\n\s*<footer>', SRC, re.S).group(1)
C["cta_h2"] = grab(r'<h2[^>]*>(.*?)</h2>', s)[0]; C["cta_p"] = grab(r'<p>(.*?)</p>', s)
C["cta_big"] = grab(r'<div class="big">(.*?)</div>', s)[0]
s = re.search(r'<footer>(.*?)</footer>', SRC, re.S).group(1)
C["fname"] = grab(r'<div class="fname">(.*?)</div>', s)[0]; C["foot"] = grab(r'<div>(.*?)</div>', s)[0]
C["title"] = grab(r'<title>(.*?)</title>')[0]
C["desc"] = grab(r'<meta name="description" content="(.*?)">')[0]
C["ogdesc"] = grab(r'<meta property="og:description" content="(.*?)">')[0]
assert len(C["pains"]) == 5 and len(C["svc"]) == 4 and len(C["steps"]) == 5 and len(C["proof"]) == 2 and len(C["faq"]) == 5, C


def h3x(t):
    """（…）を句の切れ目で折り返せる小さな添え字にする（文言は変えない）"""
    return re.sub(r'（(.*?)）', r'<span class="paren">（\1）</span>', t)


PH = ["AIアシスタント|導入支援", "請求書の|台帳化", "月次|収支ビュー", "確定申告の|準備サポート", "相談・|現状ヒアリング",
      "導入と、|情報の線引き", "過去分の回収と|台帳化", "月次ビューの|運用開始", "申告シーズンへの|準備", "複数の仕事を、|1つの台帳で",
      "お問い合わせ窓口は|準備中です", "パソコンやAIが|苦手でも|大丈夫ですか", "収入や家計をAIに|見せるのが|不安です",
      "税理士に|お願いするのと|何が違いますか", "料金は|どのくらいですか", "どこで|受けられますか"]
PH = {x.replace("|", ""): "".join(f'<span class="ph">{t}</span>' for t in x.split("|")) for x in PH}


def phrase(out):
    """見出し・質問・CTAを句の切れ目でだけ折り返す（文言は変えない。Safariでも効く）"""
    return re.sub(r'(<h3>|<summary>|<div class="big">|</small>)([^<]+)(<)', lambda m: m[1] + (f'<span>{PH.get(m[2], m[2])}</span>' if m[1] == '<summary>' else PH.get(m[2], m[2])) + m[3], out)


FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Zen+Kaku+Gothic+New:wght@400;500;700;900&display=swap" rel="stylesheet">'

BASE_CSS = """
:root{--g:#085839;--ink:#013019;--cream:#FEF0D7;--pink:#F8CBBA;--paper:#FFFBF2;--line:#E6DCC6;--sub:#4D5E55;}
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{font-family:"Zen Kaku Gothic New","Noto Sans JP",sans-serif;color:var(--ink);font-size:16px;line-height:1.9;letter-spacing:.02em;overflow-wrap:anywhere}
img{max-width:100%;height:auto;display:block}
.lockup{display:block;width:260px;max-width:70vw;aspect-ratio:2825/600;object-fit:cover;object-position:50% 52%;mix-blend-mode:multiply}
h1,h2{white-space:nowrap;font-family:"Noto Sans JP",sans-serif}
.h1{font-size:min(var(--h1max,44px),calc((100vw - 2*var(--pad,20px)) / 13.6))}
.h2{font-size:min(var(--h2max,30px),calc((100vw - 2*var(--pad,20px)) / 14.6))}
.paren{display:inline-block;font-size:.82em}
.ph{display:inline-block}
table.view{width:100%;border-collapse:collapse;font-size:13px;background:#fff;font-variant-numeric:tabular-nums}
table.view th,table.view td{border:1px solid var(--line);padding:8px 2px;text-align:center}
table.view th{background:var(--g);color:#fff;font-weight:700;font-size:12px;letter-spacing:0}
table.view td:first-child{font-weight:700}
details summary{cursor:pointer;list-style:none}
details summary::-webkit-details-marker{display:none}
"""


def page(n, name, css, body):
    url = f"{BASE}v{n}.html"
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{C['title']}｜デザイン案{n} {name}</title>
<meta name="description" content="{C['desc']}">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:title" content="{C['title']}｜デザイン案{n} {name}">
<meta property="og:description" content="{C['ogdesc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://yukitchy.github.io/money-setup-lp/logo-lockup2.webp">
<link rel="icon" type="image/png" href="../favicon.png">
{FONTS}
<style>{BASE_CSS}{css}</style>
</head>
<body>
{phrase(body)}
</body>
</html>
"""


LOCKUP = '<img class="lockup" src="../logo-lockup2.webp" alt="経理くん" width="2825" height="600">'


def img(name, alt="", cls=""):
    return f'<img class="{cls}" src="img/{name}.webp" alt="{alt}" loading="lazy" width="800" height="800">'


SVC_IMG = ["wave", "sorting", "graph", "receipts"]


def footer():
    return f'<footer><div class="fname">{C["fname"]}</div><div>{C["foot"]}</div></footer>'


# ---------------------------------------------------------------- v1 ポップ全開
def v1():
    css = """
body{background:#FFF6E3;--pad:20px;--h1max:46px;--h2max:30px}
.w{max-width:960px;margin:0 auto;padding:0 20px}
header{padding:18px 0 6px}
.hero{display:grid;gap:8px;padding:18px 0 36px;align-items:center}
.kick{display:inline-block;background:var(--g);color:var(--cream);font-weight:700;font-size:13px;padding:4px 14px;border-radius:999px;margin-bottom:14px}
h1{font-weight:900;line-height:1.35;margin-bottom:18px}
.hero p{font-size:15.5px}.hero p+p{margin-top:12px}
.hero .chara{width:min(300px,72vw);margin:0 auto}
.talk{display:flex;align-items:flex-end;gap:10px;margin-bottom:22px}
.talk img{width:96px;flex:none}
.bub{position:relative;background:#fff;border:3px solid var(--ink);border-radius:22px;padding:10px 16px;margin-bottom:46px}
.bub::before{content:"";position:absolute;left:-15px;bottom:14px;border:9px solid transparent;border-right:12px solid var(--ink)}
.bub::after{content:"";position:absolute;left:-9px;bottom:16px;border:7px solid transparent;border-right:9px solid #fff}
.lab{font-size:11px;font-weight:900;letter-spacing:.2em;color:var(--g);line-height:1.4}
h2{font-weight:900;line-height:1.4;font-size:min(28px,calc((100vw - 84px) / (var(--n) + .6)))}
@media(max-width:519px){.talk{flex-direction:column;align-items:flex-start;gap:14px}.talk img{width:76px}.bub{margin-bottom:0}
 .bub::before{left:26px;top:-21px;bottom:auto;border:9px solid transparent;border-bottom:12px solid var(--ink)}
 .bub::after{left:28px;top:-13px;bottom:auto;border:7px solid transparent;border-bottom:9px solid #fff}}
section{padding:40px 0;border-top:3px dashed #E3D3AE}
.pains{list-style:none;display:grid;gap:12px}
.pains li{background:#fff;border:3px solid var(--ink);border-radius:18px;padding:14px 16px 14px 54px;position:relative;font-size:15px;line-height:1.7;box-shadow:4px 4px 0 var(--ink)}
.pains li::before{content:"";position:absolute;left:14px;top:14px;width:26px;height:26px;border-radius:50%;background:var(--pink);border:3px solid var(--ink)}
.pains li::after{content:"";position:absolute;left:22px;top:21px;width:9px;height:5px;border-left:3px solid var(--ink);border-bottom:3px solid var(--ink);transform:rotate(-45deg)}
.svc{display:grid;gap:18px}
.svc article{background:#fff;border:3px solid var(--ink);border-radius:24px;padding:20px;box-shadow:6px 6px 0 var(--g);display:grid;grid-template-columns:88px 1fr;gap:4px 14px;align-items:start}
.svc article img{grid-row:span 3;width:88px;background:var(--cream);border-radius:50%}
.no{font-family:"Noto Sans JP";font-weight:900;font-size:22px;color:var(--g);line-height:1}
.svc h3{font-size:18px;font-weight:900;line-height:1.4}
.svc p{font-size:14.5px;grid-column:1/-1;margin-top:8px}
.svc .tb{grid-column:1/-1;margin-top:12px}
.note{font-size:12px;color:var(--sub);margin-top:6px}
.steps{list-style:none;display:grid;gap:14px}
.steps li{background:#fff;border:3px solid var(--ink);border-radius:20px;padding:16px 16px 16px 76px;position:relative}
.steps .n{position:absolute;left:14px;top:14px;width:46px;height:46px;border-radius:50%;background:var(--g);color:var(--cream);font:900 22px/46px "Noto Sans JP";text-align:center}
.steps li:not(:last-child)::after{content:"";position:absolute;left:35px;bottom:-17px;width:4px;height:17px;background:var(--ink)}
.steps h3{font-size:16.5px;font-weight:900}.steps p{font-size:14.5px}
.proof{display:grid;gap:16px}
.proof div{background:var(--cream);border:3px solid var(--ink);border-radius:20px;padding:18px}
.proof h3{font-size:16.5px;font-weight:900;margin-bottom:6px;line-height:1.5}.proof p{font-size:14.5px}
.faq details{background:#fff;border:3px solid var(--ink);border-radius:18px;padding:14px 16px;margin-bottom:12px}
.faq summary{font-weight:900;font-size:15.5px;padding-left:34px;position:relative;line-height:1.6}
.faq summary::before{content:"Q";position:absolute;left:0;top:0;width:24px;height:24px;border-radius:50%;background:var(--g);color:#fff;font-size:13px;text-align:center;line-height:24px}
.faq p{font-size:14.5px;margin-top:10px;padding:10px 12px;background:var(--cream);border-radius:12px}
.cta{padding:40px 0 30px;border-top:3px dashed #E3D3AE}
.cta>p{font-size:15px}
.box{margin-top:22px;background:var(--g);color:var(--cream);border-radius:24px;padding:22px;display:grid;gap:8px;align-items:center}.box img{width:96px;order:-1}
@media(min-width:560px){.box{grid-template-columns:1fr 110px}.box img{order:0;width:110px}}
.box .big{font-size:18px;font-weight:900;line-height:1.5}.box p{font-size:13.5px;opacity:.9}
footer{padding:22px 0 40px;font-size:12.5px;color:var(--sub)}.fname{font-weight:900;color:var(--ink)}
@media(min-width:820px){
 .hero{grid-template-columns:1.2fr .8fr;padding:30px 0 60px}.hero .chara{width:340px}
 .svc{grid-template-columns:1fr 1fr}.pains{grid-template-columns:1fr 1fr}
 .proof{grid-template-columns:1fr 1fr}
 h2{font-size:30px}.talk img{width:120px}.bub{margin-bottom:46px}
 .faq{max-width:760px}
}
"""
    def talk(im, lab, h2):
        return f'<div class="talk">{img(im, "経理くん")}<div class="bub"><div class="lab">{lab}</div><h2 style="--n:{len(h2)}">{h2}</h2></div></div>'
    svc = "".join(
        f'<article>{img(SVC_IMG[i], "")}<div class="no">{s["no"]}</div><h3>{s["h3"]}</h3><p>{s["p"]}</p>'
        + (f'<div class="tb">{C["table"]}<div class="note">{C["view_note"]}</div></div>' if i == 2 else "")
        + "</article>" for i, s in enumerate(C["svc"]))
    body = f"""<div class="w">
<header>{LOCKUP}</header>
<div class="hero"><div><div class="kick">{C['kicker']}</div><h1 class="h1">{C['h1']}</h1>{''.join(f'<p>{p}</p>' for p in C['hero_p'])}</div>{img('wave','手を振る経理くん','chara')}</div>
<section>{talk('worried','CHECK',C['check_h2'])}<ul class="pains">{''.join(f'<li>{p}</li>' for p in C['pains'])}</ul></section>
<section>{talk('ok','SERVICE',C['svc_h2'])}<div class="svc">{svc}</div></section>
<section>{talk('invoice','FLOW',C['flow_h2'])}<ol class="steps">{''.join(f'<li><div class="n">{s["n"]}</div><h3>{s["h3"]}</h3><p>{s["p"]}</p></li>' for s in C['steps'])}</ol></section>
<section>{talk('receipts','PROOF',C['proof_h2'])}<div class="proof">{''.join(f'<div><h3>{h3x(p["h3"])}</h3><p>{p["p"]}</p></div>' for p in C['proof'])}</div></section>
<section class="faq">{talk('graph','FAQ',C['faq_h2'])}{''.join(f'<details><summary>{f["q"]}</summary><p>{f["a"]}</p></details>' for f in C['faq'])}</section>
<div class="cta">{talk('wave','CONTACT',C['cta_h2'])}{''.join(f'<p>{p}</p>' for p in C['cta_p'][:1])}<div class="box"><div><div class="big">{C['cta_big']}</div><p>{C['cta_p'][1]}</p></div>{img('ok','')}</div></div>
{footer()}
</div>"""
    return page(1, "ポップ全開", css, body)


# ---------------------------------------------------------------- v2 図解中心
def v2():
    css = """
body{background:#fff;--pad:20px;--h1max:48px;--h2max:30px}
.w{max-width:1040px;margin:0 auto;padding:0 20px}
header{padding:16px 0;border-bottom:1px solid var(--line)}
.lab{font:700 11px/1 "Noto Sans JP";letter-spacing:.24em;color:var(--g);margin-bottom:12px;display:flex;align-items:center;gap:10px}
.lab::before{content:"";width:22px;height:2px;background:var(--g)}
h1{font-weight:900;line-height:1.35;margin:10px 0 18px}
h2{font-weight:900;line-height:1.4;margin-bottom:26px}
.hero{padding:34px 0 40px}
.kick{font-weight:700;color:var(--g);font-size:14px}
.hero p{font-size:15.5px;max-width:640px}.hero p+p{margin-top:12px}
.ba{display:grid;grid-template-columns:1fr 34px 1fr;align-items:center;gap:6px;margin:28px 0 8px;background:#F7F4EC;border-radius:16px;padding:16px 10px}
.ba figure{text-align:center}.ba img{width:100%;max-width:220px;margin:0 auto}
.ba figcaption{font:900 12px/1 "Noto Sans JP";letter-spacing:.2em;margin-top:6px}
.ba .af figcaption{color:var(--g)}
.arw{height:24px;position:relative}.arw::before{content:"";position:absolute;left:0;right:8px;top:9px;height:6px;background:var(--g)}
.arw::after{content:"";position:absolute;right:0;top:0;border:12px solid transparent;border-left:14px solid var(--g);border-right:0}
section{padding:48px 0;border-top:1px solid var(--line)}
.map{display:grid;gap:10px;counter-reset:p}
.map li{list-style:none;display:grid;grid-template-columns:36px 1fr;gap:12px;align-items:start;font-size:15px;line-height:1.7;padding:12px 14px;border:1.5px solid var(--ink);border-radius:10px;background:#fff;position:relative}
.map li::before{counter-increment:p;content:counter(p);width:30px;height:30px;border-radius:50%;border:2px solid var(--ink);font:900 14px/26px "Noto Sans JP";text-align:center}
.check{display:grid;gap:18px}
.check .c{width:min(260px,64vw);margin:0 auto}
.pipe{display:grid;grid-template-columns:1fr 1fr;gap:0;margin-bottom:30px;border:2px solid var(--ink);border-radius:14px;overflow:hidden}
.pipe div{padding:12px 6px;text-align:center;font:700 13px/1.4 "Noto Sans JP";position:relative;background:#fff}
.pipe div:nth-child(even){border-left:2px solid var(--ink)}.pipe div:nth-child(n+3){border-top:2px solid var(--ink)}
@media(min-width:700px){.pipe{grid-template-columns:repeat(4,1fr)}.pipe div+div{border-left:2px solid var(--ink)}.pipe div:nth-child(n+3){border-top:0}}
.pipe div:last-child{background:var(--g);color:#fff}
.pipe small{display:block;font:900 10px/1 "Noto Sans JP";letter-spacing:.16em;color:var(--g);margin-bottom:6px}
.pipe div:last-child small{color:var(--cream)}
.svc{display:grid;gap:16px}
.svc article{border:1.5px solid var(--ink);border-radius:14px;padding:20px;position:relative;background:#fff}
.no{font:900 40px/1 "Noto Sans JP";color:var(--g);opacity:.9}
.svc h3{font-size:18px;font-weight:900;margin:8px 0 6px}
.svc p{font-size:14.5px}
.svc .big{border-color:var(--g);border-width:3px}
.chart{margin-top:16px;border:1.5px solid var(--line);border-radius:10px;padding:14px;background:#FBFAF5}
.bars{display:flex;align-items:flex-end;gap:12px;height:120px;border-bottom:2px solid var(--ink);padding:0 6px;margin-bottom:14px}
.bars div{flex:1;display:flex;gap:3px;align-items:flex-end;height:100%}
.bars i{flex:1;background:var(--g);border-radius:3px 3px 0 0}.bars i+i{background:var(--pink)}
.note{font-size:12px;color:var(--sub);margin-top:8px}
.guide{display:flex;gap:12px;align-items:center;margin-bottom:22px}
.guide img{width:84px;flex:none}
.guide h2{margin:0}
.flow{list-style:none;position:relative;display:grid;gap:0}
.flow li{display:grid;grid-template-columns:56px 1fr;gap:16px;padding-bottom:22px;position:relative}
.flow li::before{content:"";position:absolute;left:27px;top:52px;bottom:0;width:2px;background:var(--g)}
.flow li:last-child::before{display:none}
.flow .n{width:56px;height:56px;border-radius:50%;background:var(--g);color:#fff;font:900 24px/56px "Noto Sans JP";text-align:center}
.flow li:last-child .n{background:var(--ink)}
.flow h3{font-size:17px;font-weight:900;line-height:1.5;padding-top:12px}
.flow p{font-size:14.5px}
.proof{display:grid;gap:16px}
.proof>div{border-left:6px solid var(--g);padding:4px 0 4px 18px}
.proof h3{font-size:17px;font-weight:900;margin-bottom:6px;line-height:1.5}.proof p{font-size:14.5px}
.faq details{border-top:1.5px solid var(--ink);padding:16px 0}
.faq details:last-child{border-bottom:1.5px solid var(--ink)}
.faq summary{font-weight:900;font-size:15.5px;line-height:1.6;display:grid;grid-template-columns:28px 1fr}
.faq summary::before{content:"Q";color:var(--g);font-family:"Noto Sans JP"}
.faq p{font-size:14.5px;margin:8px 0 0 28px}
.cta{padding:48px 0;border-top:1px solid var(--line)}
.cta>p{font-size:15px}
.box{margin-top:20px;border:3px solid var(--g);border-radius:14px;padding:22px;display:grid;gap:8px;align-items:center}.box img{width:90px;order:-1}
@media(min-width:560px){.box{grid-template-columns:1fr 110px}.box img{order:0;width:110px}}
.box .big{font-size:18px;font-weight:900}.box p{font-size:13.5px;color:var(--sub)}
footer{padding:22px 0 40px;font-size:12.5px;color:var(--sub);border-top:1px solid var(--line)}.fname{font-weight:900;color:var(--ink)}
@media(min-width:860px){
 .hero{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;padding:60px 0}
 .ba{margin:0}
 .check{grid-template-columns:280px 1fr;align-items:center}.check .c{width:100%}
 .svc{grid-template-columns:1fr 1fr}.svc .big{grid-column:1/-1;display:grid;grid-template-columns:1fr 1.2fr;gap:0 30px}
 .svc .big .chart{grid-row:1/5;grid-column:2;margin-top:0}
 .flow{grid-template-columns:repeat(5,1fr);gap:14px}
 .flow li{grid-template-columns:1fr;gap:10px;padding:0}
 .flow li::before{left:56px;right:-14px;top:27px;bottom:auto;width:auto;height:2px}
 .flow h3{padding-top:0;font-size:16px}
 .proof{grid-template-columns:1fr 1fr;gap:30px}
 .guide img{width:110px}
}
"""
    sv = C["svc"]
    svc = "".join(
        (f'<article class="big"><div class="no">{s["no"]}</div><h3>{s["h3"]}</h3><p>{s["p"]}</p>'
         f'<div class="chart"><div class="bars">' + "".join(f'<div><i style="height:{a}%"></i><i style="height:{b}%"></i></div>' for a, b in [(70, 40), (62, 45), (78, 38), (74, 52), (85, 41), (66, 44)])
         + f'</div>{C["table"]}<div class="note">{C["view_note"]}</div></div></article>')
        if i == 2 else f'<article><div class="no">{s["no"]}</div><h3>{s["h3"]}</h3><p>{s["p"]}</p></article>'
        for i, s in enumerate(sv))
    body = f"""<header><div class="w">{LOCKUP}</div></header>
<div class="w">
<div class="hero"><div><div class="kick">{C['kicker']}</div><h1 class="h1">{C['h1']}</h1>{''.join(f'<p>{p}</p>' for p in C['hero_p'])}</div>
<div class="ba"><figure>{img('worried','散らばった書類に困る経理くん')}<figcaption>BEFORE</figcaption></figure><div class="arw"></div><figure class="af">{img('ok','整って安心した経理くん')}<figcaption>AFTER</figcaption></figure></div></div>
<section><div class="lab">CHECK</div><h2 class="h2">{C['check_h2']}</h2><div class="check">{img('worried','','c')}<ol class="map">{''.join(f'<li>{p}</li>' for p in C['pains'])}</ol></div></section>
<section><div class="lab">SERVICE</div><h2 class="h2">{C['svc_h2']}</h2>
<div class="pipe">{''.join(f'<div><small>{x["no"]}</small>{x["h3"]}</div>' for x in sv)}</div>
<div class="svc">{svc}</div></section>
<section><div class="guide">{img('graph','グラフを指す経理くん')}<div><div class="lab">FLOW</div><h2 class="h2">{C['flow_h2']}</h2></div></div>
<ol class="flow">{''.join(f'<li><div class="n">{s["n"]}</div><div><h3>{s["h3"]}</h3><p>{s["p"]}</p></div></li>' for s in C['steps'])}</ol></section>
<section><div class="lab">PROOF</div><h2 class="h2">{C['proof_h2']}</h2><div class="proof">{''.join(f'<div><h3>{h3x(p["h3"])}</h3><p>{p["p"]}</p></div>' for p in C['proof'])}</div></section>
<section class="faq"><div class="lab">FAQ</div><h2 class="h2">{C['faq_h2']}</h2>{''.join(f'<details><summary>{f["q"]}</summary><p>{f["a"]}</p></details>' for f in C['faq'])}</section>
<div class="cta"><div class="lab">CONTACT</div><h2 class="h2">{C['cta_h2']}</h2><p>{C['cta_p'][0]}</p><div class="box"><div><div class="big">{C['cta_big']}</div><p>{C['cta_p'][1]}</p></div>{img('invoice','')}</div></div>
{footer()}
</div>"""
    return page(2, "図解中心", css, body)


# ---------------------------------------------------------------- v3 クリームのやさしい紙面
def v3():
    css = """
body{background:var(--cream);--pad:28px;--h1max:40px;--h2max:26px}
.w{max-width:640px;margin:0 auto;padding:0 28px}
header{padding:28px 0 0;text-align:center}.lockup{margin:0 auto;width:230px}
h1,h2{font-family:"Zen Kaku Gothic New",sans-serif;font-weight:700}
h1{line-height:1.4;margin:6px 0 26px;text-align:center}
h2{line-height:1.5;margin-bottom:28px;text-align:center}
.hero{padding:40px 0 54px;position:relative}
.hero .chara{width:min(240px,60vw);margin:0 auto 10px}
.kick{text-align:center;font-size:13px;color:var(--g);letter-spacing:.18em;font-weight:500}
.hero p{font-size:15.5px;line-height:2}.hero p+p{margin-top:16px}
.lab{text-align:center;font-size:11px;letter-spacing:.3em;color:var(--g);font-weight:500;margin-bottom:6px}
section{padding:56px 0;position:relative}
section::before,.cta::before{content:"";display:block;width:40px;height:1px;background:var(--g);margin:0 auto 52px;opacity:.5}
.spot{width:96px;margin:0 auto 10px}
.pains{list-style:none}
.pains li{padding:14px 0 14px 30px;border-bottom:1px solid #E7D7B5;font-size:15px;line-height:1.8;position:relative}
.pains li::before{content:"";position:absolute;left:4px;top:24px;width:9px;height:9px;border-radius:50%;background:var(--pink)}
.svc article{padding:26px 0;border-bottom:1px solid #E7D7B5;display:grid;grid-template-columns:1fr 92px;gap:0 18px}
.svc article:first-child{padding-top:0}
.svc article img{grid-column:2;grid-row:1/4;width:92px}
.no{font-size:12px;letter-spacing:.2em;color:var(--g)}
.svc h3{font-size:17.5px;font-weight:700;margin:2px 0 8px;line-height:1.5}
.svc p{font-size:14.5px;line-height:1.95;grid-column:1/-1}
.svc .tb{grid-column:1/-1;margin-top:16px}
table.view{background:#FFFDF8}table.view th{background:var(--g)}
.note{font-size:12px;color:var(--sub);margin-top:8px;text-align:right}
.steps{list-style:none}
.steps li{display:grid;grid-template-columns:44px 1fr;gap:14px;padding:16px 0}
.steps .n{width:40px;height:40px;border:1px solid var(--g);border-radius:50%;text-align:center;line-height:38px;color:var(--g);font-size:17px;font-weight:700;background:#FFFBF2}
.steps h3{font-size:16.5px;font-weight:700;line-height:1.6;padding-top:6px}.steps p{font-size:14.5px;line-height:1.95}
.proof>div{background:#FFFBF2;border-radius:4px;padding:24px 22px}
.proof>div+div{margin-top:16px}
.proof h3{font-size:16.5px;font-weight:700;margin-bottom:8px;line-height:1.6}.proof p{font-size:14.5px;line-height:1.95}
.faq details{border-bottom:1px solid #E7D7B5;padding:18px 0}
.faq summary{font-weight:700;font-size:15.5px;line-height:1.7;padding-left:26px;position:relative}
.faq summary::before{content:"Q";position:absolute;left:0;color:var(--g)}
.faq p{font-size:14.5px;margin-top:8px;padding-left:26px;line-height:1.95}
.cta{padding:56px 0 30px;text-align:center}
.cta>p{font-size:15px;text-align:left}
.box{margin-top:26px;background:#FFFBF2;border:1px solid var(--g);border-radius:4px;padding:26px 22px}
.box img{width:110px;margin:0 auto 8px}
.box .big{font-size:17.5px;font-weight:700;color:var(--g)}.box p{font-size:13.5px;color:var(--sub);text-align:left;margin-top:6px}
footer{padding:30px 0 50px;font-size:12.5px;color:var(--sub);text-align:center}.fname{font-weight:700;color:var(--ink)}
.deco{position:absolute;width:76px;opacity:.95;pointer-events:none}
@media(min-width:900px){.deco{width:120px}.d1{left:-170px;top:120px}.d2{right:-170px;top:200px}.d3{left:-160px;top:100px}}
@media(max-width:899px){.deco{display:none}}
"""
    props = ["p-calc", "p-receipt", "p-envelope"]
    svc = "".join(
        f'<article><div><div class="no">{s["no"]}</div><h3>{s["h3"]}</h3></div>{img(SVC_IMG[i])}<p>{s["p"]}</p>'
        + (f'<div class="tb">{C["table"]}<div class="note">{C["view_note"]}</div></div>' if i == 2 else "")
        + "</article>" for i, s in enumerate(C["svc"]))
    body = f"""<div class="w">
<header>{LOCKUP}</header>
<div class="hero">{img('wave','手を振る経理くん','chara')}<div class="kick">{C['kicker']}</div><h1 class="h1">{C['h1']}</h1>{''.join(f'<p>{p}</p>' for p in C['hero_p'])}{img('p-receipt','','deco d1')}{img('p-calc','','deco d2')}</div>
<section>{img('p-receipt','','spot')}<div class="lab">CHECK</div><h2 class="h2">{C['check_h2']}</h2><ul class="pains">{''.join(f'<li>{p}</li>' for p in C['pains'])}</ul></section>
<section>{img('p-calc','','spot')}<div class="lab">SERVICE</div><h2 class="h2">{C['svc_h2']}</h2><div class="svc">{svc}</div>{img('p-envelope','','deco d3')}</section>
<section>{img('p-envelope','','spot')}<div class="lab">FLOW</div><h2 class="h2">{C['flow_h2']}</h2><ol class="steps">{''.join(f'<li><div class="n">{s["n"]}</div><div><h3>{s["h3"]}</h3><p>{s["p"]}</p></div></li>' for s in C['steps'])}</ol></section>
<section>{img('invoice','','spot')}<div class="lab">PROOF</div><h2 class="h2">{C['proof_h2']}</h2><div class="proof">{''.join(f'<div><h3>{h3x(p["h3"])}</h3><p>{p["p"]}</p></div>' for p in C['proof'])}</div></section>
<section class="faq"><div class="lab">FAQ</div><h2 class="h2">{C['faq_h2']}</h2>{''.join(f'<details><summary>{f["q"]}</summary><p>{f["a"]}</p></details>' for f in C['faq'])}</section>
<div class="cta"><div class="lab">CONTACT</div><h2 class="h2">{C['cta_h2']}</h2><p>{C['cta_p'][0]}</p><div class="box">{img('ok','')}<div class="big">{C['cta_big']}</div><p>{C['cta_p'][1]}</p></div></div>
{footer()}
</div>"""
    return page(3, "クリームのやさしい紙面", css, body)


# ---------------------------------------------------------------- v4 深緑のしっかり系
def v4():
    css = """
body{background:#fff;--pad:22px;--h1max:52px;--h2max:32px}
.w{max-width:1080px;margin:0 auto;padding:0 22px}
header{background:#fff;padding:14px 0}
.dark{background:var(--g);color:var(--cream)}
.deep{background:var(--ink);color:var(--cream)}
.cr{background:var(--cream)}
h1,h2{font-weight:900}
h1{line-height:1.35;margin:12px 0 22px}
h2{line-height:1.4;margin-bottom:30px}
.lab{font:700 12px/1 "Noto Sans JP";letter-spacing:.24em;margin-bottom:14px;color:var(--g)}
.dark .lab,.deep .lab{color:var(--pink)}
.hero{padding:48px 0 0;overflow:hidden}
.hero .in{display:grid;gap:10px}
.kick{display:inline-block;border:1.5px solid var(--cream);padding:3px 12px;font-size:13px;font-weight:700}
.hero p{font-size:15.5px;opacity:.95}.hero p+p{margin-top:12px}
.hero .chara{width:min(280px,66vw);margin:16px auto -6px;background:var(--cream);border-radius:50% 50% 0 0;padding:20px 20px 0}
section{padding:60px 0}
.pains{list-style:none;display:grid;gap:1px;background:rgba(254,240,215,.25);border:1px solid rgba(254,240,215,.25)}
.pains li{background:var(--g);padding:18px 18px 18px 56px;position:relative;font-size:15px;line-height:1.75}
.pains li::before{content:"";position:absolute;left:18px;top:21px;width:22px;height:22px;border:2px solid var(--pink)}
.pains li::after{content:"";position:absolute;left:23px;top:26px;width:12px;height:6px;border-left:3px solid var(--cream);border-bottom:3px solid var(--cream);transform:rotate(-45deg)}
.svc{display:grid;gap:18px}
.svc article{border:2px solid var(--ink);padding:24px 22px;background:#fff}
.no{font:900 13px/1 "Noto Sans JP";color:#fff;background:var(--g);display:inline-block;padding:6px 10px;letter-spacing:.1em}
.svc h3{font-size:19px;font-weight:900;margin:12px 0 8px}
.svc p{font-size:14.5px}
.note{font-size:12px;color:var(--sub);margin-top:8px}
.svc .tb{margin-top:14px}
.steps{list-style:none;display:grid;gap:0;counter-reset:s}
.steps li{display:grid;grid-template-columns:64px 1fr;gap:16px;padding:22px 0;border-top:1px solid rgba(254,240,215,.3)}
.steps .n{font:900 44px/1 "Noto Sans JP";color:var(--pink)}
.steps h3{font-size:17.5px;font-weight:900;margin-bottom:4px}.steps p{font-size:14.5px;opacity:.92}
.proof{display:grid;gap:18px}
.proof>div{background:#fff;padding:24px 22px;border-top:6px solid var(--g)}
.proof h3{font-size:17.5px;font-weight:900;margin-bottom:8px;line-height:1.5}.proof p{font-size:14.5px}
.pr{display:grid;gap:24px;align-items:center}.pr img{width:min(240px,60vw);margin:0 auto}
.faq details{border-bottom:2px solid var(--ink);padding:18px 0}
.faq details:first-of-type{border-top:2px solid var(--ink)}
.faq summary{font-weight:900;font-size:16px;line-height:1.6;display:grid;grid-template-columns:30px 1fr}
.faq summary::before{content:"Q";color:var(--g);font-family:"Noto Sans JP"}
.faq p{font-size:14.5px;margin:8px 0 0 30px}
.cta>.w{display:grid;gap:20px;align-items:center}
.cta p{font-size:15px}
.box{margin-top:22px;border:2px solid var(--cream);padding:24px 22px}
.box .big{font-size:19px;font-weight:900}.box p{font-size:13.5px;opacity:.85}
.cta img{width:min(220px,56vw);margin:0 auto}
footer{background:var(--ink);color:rgba(254,240,215,.75);font-size:12.5px;padding:22px;text-align:center;border-top:1px solid rgba(254,240,215,.15)}
footer .fname{color:var(--cream);font-weight:900}
@media(min-width:880px){
 .hero .in{grid-template-columns:1.3fr .7fr;align-items:end}.hero .chara{width:320px;margin:0}
 .hero .txt{padding-bottom:60px}
 .pains{grid-template-columns:1fr 1fr}.pains li:last-child{grid-column:1/-1}
 .svc{grid-template-columns:1fr 1fr}
 .steps{grid-template-columns:repeat(5,1fr);gap:24px}.steps li{grid-template-columns:1fr;border-top:3px solid var(--pink);gap:10px}
 .pr{grid-template-columns:260px 1fr}.proof{grid-template-columns:1fr 1fr}
 .cta>.w{grid-template-columns:1fr 260px}
}
"""
    svc = "".join(
        f'<article><div class="no">{s["no"]}</div><h3>{s["h3"]}</h3><p>{s["p"]}</p>'
        + (f'<div class="tb">{C["table"]}<div class="note">{C["view_note"]}</div></div>' if i == 2 else "")
        + "</article>" for i, s in enumerate(C["svc"]))
    body = f"""<header><div class="w">{LOCKUP}</div></header>
<div class="hero dark"><div class="w in"><div class="txt"><div class="kick">{C['kicker']}</div><h1 class="h1">{C['h1']}</h1>{''.join(f'<p>{p}</p>' for p in C['hero_p'])}</div>{img('wave','手を振る経理くん','chara')}</div></div>
<section class="dark" style="padding-top:20px"><div class="w"><div class="lab">CHECK</div><h2 class="h2">{C['check_h2']}</h2><ul class="pains">{''.join(f'<li>{p}</li>' for p in C['pains'])}</ul></div></section>
<section class="cr"><div class="w"><div class="lab">SERVICE</div><h2 class="h2">{C['svc_h2']}</h2><div class="svc">{svc}</div></div></section>
<section class="deep"><div class="w"><div class="lab">FLOW</div><h2 class="h2">{C['flow_h2']}</h2><ol class="steps">{''.join(f'<li><div class="n">{s["n"]}</div><div><h3>{s["h3"]}</h3><p>{s["p"]}</p></div></li>' for s in C['steps'])}</ol></div></section>
<section class="cr"><div class="w"><div class="lab">PROOF</div><h2 class="h2">{C['proof_h2']}</h2><div class="pr">{img('sorting','仕分け箱にレシートを入れる経理くん')}<div class="proof">{''.join(f'<div><h3>{h3x(p["h3"])}</h3><p>{p["p"]}</p></div>' for p in C['proof'])}</div></div></div></section>
<section class="faq"><div class="w"><div class="lab">FAQ</div><h2 class="h2">{C['faq_h2']}</h2>{''.join(f'<details><summary>{f["q"]}</summary><p>{f["a"]}</p></details>' for f in C['faq'])}</div></section>
<section class="cta dark"><div class="w"><div><div class="lab">CONTACT</div><h2 class="h2">{C['cta_h2']}</h2><p>{C['cta_p'][0]}</p><div class="box"><div class="big">{C['cta_big']}</div><p>{C['cta_p'][1]}</p></div></div>{img('ok','')}</div></section>
<footer><div class="fname">{C['fname']}</div><div>{C['foot']}</div></footer>"""
    return page(4, "深緑のしっかり系", css, body)


# ---------------------------------------------------------------- v5 雑誌・編集
def v5():
    css = """
body{background:#FBF8F1;--pad:20px;--h1max:84px;--h2max:56px}
.w{max-width:1160px;margin:0 auto;padding:0 20px}
header{display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:3px solid var(--ink)}
header .iss{font:700 11px/1.3 "Noto Sans JP";letter-spacing:.18em;text-align:right;color:var(--g)}
h1,h2{font-weight:900;letter-spacing:-.01em}
h1{line-height:1.25;margin:10px 0 0}
.h1{font-size:min(84px,calc((100vw - 40px) / 13.2))}
.h2{font-size:min(54px,calc((100vw - 40px) / 14.4))}
h2{line-height:1.3}
.hero{padding:34px 0 0}
.kick{font:700 13px/1 "Noto Sans JP";letter-spacing:.14em;color:var(--g)}
.cover{margin:26px 0 10px;background:var(--g);aspect-ratio:16/10;display:grid;place-items:center;position:relative;overflow:hidden}
.cover img{width:62%;max-width:520px;position:relative}
.cover::before{content:"";position:absolute;width:78%;aspect-ratio:1;border-radius:50%;background:var(--cream);opacity:.12}
.cap{font-size:11.5px;color:var(--sub);letter-spacing:.06em;border-top:1px solid var(--ink);padding-top:6px}
.lead{padding:22px 0 50px}
.lead p{font-size:16px;line-height:2}.lead p+p{margin-top:14px}
.lead p:first-child::first-letter{font:900 3.2em/1 "Noto Sans JP";float:left;margin:.08em .1em 0 0;color:var(--g)}
.chap{border-top:3px solid var(--ink);padding:16px 0 56px}
.chap .head{display:flex;flex-direction:column;gap:10px;margin-bottom:26px;border-bottom:1px solid var(--ink);padding-bottom:16px}
.chap .k{font:900 12px/1 "Noto Sans JP";letter-spacing:.24em;color:var(--g);writing-mode:horizontal-tb;flex:none}
.pains{list-style:none;counter-reset:p;columns:1}
.pains li{counter-increment:p;padding:14px 0;border-bottom:1px solid var(--line);font-size:15.5px;line-height:1.75;display:grid;grid-template-columns:40px 1fr;break-inside:avoid}
.pains li::before{content:"0" counter(p);font:900 15px/1.75 "Noto Sans JP";color:var(--g)}
.fig{background:var(--cream);padding:18px;margin-bottom:8px}
.fig img{width:min(300px,70%);margin:0 auto}
.svc article{padding:22px 0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:54px 1fr;gap:0 12px}
.svc .no{font:900 36px/1 "Noto Sans JP";color:var(--g);grid-row:1/3}
.svc h3{font-size:min(19px,calc((100vw - 106px) / 11.5));font-weight:900;line-height:1.4;margin-bottom:6px}
.svc p{font-size:15px}
.svc .tb{grid-column:1/-1;margin-top:14px}
table.view th{background:var(--ink)}
.note{font-size:11.5px;color:var(--sub);margin-top:6px}
.steps{list-style:none}
.steps li{display:grid;grid-template-columns:72px 1fr;gap:0 14px;padding:18px 0;border-bottom:1px solid var(--line)}
.steps .n{font:900 56px/.9 "Noto Sans JP";color:transparent;-webkit-text-stroke:1.5px var(--g)}
.steps h3{font-size:17.5px;font-weight:900}.steps p{font-size:15px}
.proof>div{padding:20px 0;border-bottom:1px solid var(--line)}
.proof h3{font-size:19px;font-weight:900;margin-bottom:8px;line-height:1.5}.proof p{font-size:15px}
.pq{font:900 22px/1.5 "Noto Sans JP";color:var(--g);border-left:6px solid var(--g);padding-left:16px;margin:4px 0 20px}
.faq details{border-bottom:1px solid var(--ink);padding:16px 0}
.faq summary{font-weight:900;font-size:16px;line-height:1.6;display:grid;grid-template-columns:34px 1fr}
.faq summary::before{content:"Q.";color:var(--g);font-family:"Noto Sans JP"}
.faq p{font-size:15px;margin:8px 0 0 34px}
.cta p{font-size:15.5px}
.box{margin-top:22px;background:var(--ink);color:var(--cream);padding:26px 22px;display:grid;gap:8px;align-items:center}.box img{width:92px;order:-1;background:var(--cream);border-radius:50%}
@media(min-width:560px){.box{grid-template-columns:1fr 110px}.box img{order:0;width:110px}}
.box .big{font-size:19px;font-weight:900}.box p{font-size:13.5px;opacity:.85}
footer{border-top:3px solid var(--ink);padding:18px 0 46px;font-size:12.5px;color:var(--sub)}.fname{font-weight:900;color:var(--ink)}
@media(min-width:900px){
 .hero{display:grid;grid-template-columns:1fr;padding-top:50px}
 .chap .head{flex-direction:row;align-items:baseline;gap:20px}
 .spread{display:grid;grid-template-columns:7fr 5fr;gap:44px;align-items:start}
 .lead{columns:2;column-gap:36px;padding-top:30px}
 .lead p+p{margin-top:0;text-indent:1em}
 .pains{columns:2;column-gap:40px}
 .svcwrap{display:grid;grid-template-columns:4fr 8fr;gap:44px;align-items:start}
 .svcwrap .fig{position:sticky;top:20px}
 .svc{columns:2;column-gap:40px}.svc article{break-inside:avoid}
 .flowwrap{display:grid;grid-template-columns:8fr 4fr;gap:44px}
 .proof{display:grid;grid-template-columns:1fr 1fr;gap:40px}
 .faq .list{columns:2;column-gap:40px}.faq details{break-inside:avoid}
 .cta .w2{display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:end}
}
"""
    def head(k, h2):
        return f'<div class="head"><span class="k">{k}</span><h2 class="h2">{h2}</h2></div>'
    svc = "".join(
        f'<article><div class="no">{s["no"]}</div><h3>{s["h3"]}</h3><p>{s["p"]}</p>'
        + (f'<div class="tb">{C["table"]}<div class="note">{C["view_note"]}</div></div>' if i == 2 else "")
        + "</article>" for i, s in enumerate(C["svc"]))
    body = f"""<div class="w">
<header>{LOCKUP}</header>
<div class="hero"><div class="kick">{C['kicker']}</div><h1 class="h1">{C['h1']}</h1>
<figure class="cover">{img('wave','手を振る経理くん')}</figure><div class="cap">FIG. 01 — 経理くん</div>
<div class="lead">{''.join(f'<p>{p}</p>' for p in C['hero_p'])}</div></div>
<section class="chap">{head('CHECK',C['check_h2'])}<div class="spread"><ul class="pains">{''.join(f'<li>{p}</li>' for p in C['pains'])}</ul><div><div class="fig">{img('worried','')}</div><div class="cap">FIG. 02</div></div></div></section>
<section class="chap">{head('SERVICE',C['svc_h2'])}<div class="svcwrap"><div><div class="fig">{img('graph','')}</div><div class="cap">FIG. 03</div></div><div class="svc">{svc}</div></div></section>
<section class="chap">{head('FLOW',C['flow_h2'])}<div class="flowwrap"><ol class="steps">{''.join(f'<li><div class="n">{s["n"]}</div><div><h3>{s["h3"]}</h3><p>{s["p"]}</p></div></li>' for s in C['steps'])}</ol><div><div class="fig">{img('sorting','')}</div><div class="cap">FIG. 04</div></div></div></section>
<section class="chap">{head('PROOF',C['proof_h2'])}<div class="proof">{''.join(f'<div><h3>{h3x(p["h3"])}</h3><p>{p["p"]}</p></div>' for p in C['proof'])}</div></section>
<section class="chap faq">{head('FAQ',C['faq_h2'])}<div class="list">{''.join(f'<details><summary>{f["q"]}</summary><p>{f["a"]}</p></details>' for f in C['faq'])}</div></section>
<section class="chap cta">{head('CONTACT',C['cta_h2'])}<div class="w2"><p>{C['cta_p'][0]}</p><div class="box"><div><div class="big">{C['cta_big']}</div><p>{C['cta_p'][1]}</p></div>{img('ok','')}</div></div></section>
{footer()}
</div>"""
    return page(5, "雑誌・編集", css, body)


if __name__ == "__main__":
    for i, f in enumerate([v1, v2, v3, v4, v5], 1):
        out = f()
        plain = re.sub(r'</?span[^>]*>', '', out)
        # 自己チェック: 原文の本文テキストが全部入っているか
        for k, v in C.items():
            for t in (v if isinstance(v, list) else [v]):
                for x in (t.values() if isinstance(t, dict) else [t]):
                    if k in ("title", "desc", "ogdesc"):
                        continue
                    assert x in plain, (i, k, x[:30])
        (HERE / f"v{i}.html").write_text(out)
        print(f"v{i}.html", len(out))


# ---------------------------------------------------------------- 見比べボード
BOARD = [
    (1, "ポップ全開", "キャラが全セクションに出て、吹き出しで見出しを案内する。太い線と影でにぎやか。"),
    (2, "図解中心", "Before/After、4つのサービスの流れ図、収支ビューのグラフ、5ステップの工程図で見せる。キャラは案内役。"),
    (3, "クリームのやさしい紙面", "クリーム地に電卓・レシート・封筒の小さな絵を置いた、静かで余白の多い1段組み。"),
    (4, "深緑のしっかり系", "深緑と濃緑を面で敷き、クリームと交互に切り替える信頼感重視の構成。キャラは要所だけ。"),
    (5, "雑誌・編集", "大きな見出しと図版、章立ての罫線で誌面のように読ませる。PCでは2段組み。"),
]


def board():
    cards = "".join(f"""<a class="card" href="v{n}.html">
<div class="shots"><img class="pc" src="img/thumb-v{n}-pc.webp" alt="案{n} PC表示" width="720" height="450" loading="lazy"><img class="sp" src="img/thumb-v{n}-sp.webp" alt="案{n} スマホ表示" width="195" height="390" loading="lazy"></div>
<div class="meta"><div class="num">{n}</div><div><h2>{name}</h2><p>{d}</p></div></div></a>""" for n, name, d in BOARD)
    css = """
body{background:var(--cream);padding:0 0 60px}
.w{max-width:1180px;margin:0 auto;padding:0 20px}
header{padding:22px 0 10px}
.ttl{font:900 min(34px,calc((100vw - 40px)/12.5))/1.35 "Noto Sans JP";white-space:nowrap;margin:18px 0 8px}
.lead{font-size:14.5px;color:var(--sub);margin-bottom:28px}
.grid{display:grid;gap:22px}
.card{display:block;text-decoration:none;color:inherit;background:#fff;border:2px solid var(--ink);border-radius:14px;overflow:hidden;transition:transform .15s}
.card:hover{transform:translateY(-3px)}
.shots{position:relative;background:#E9DFC8;border-bottom:2px solid var(--ink)}
.shots .pc{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top}
.shots .sp{position:absolute;right:12px;bottom:12px;width:24%;border:2px solid var(--ink);border-radius:10px;box-shadow:0 4px 0 rgba(1,48,25,.25)}
.meta{display:grid;grid-template-columns:44px 1fr;gap:12px;padding:16px 18px 18px}
.num{width:44px;height:44px;border-radius:50%;background:var(--g);color:var(--cream);font:900 22px/44px "Noto Sans JP";text-align:center}
.meta h2{font-size:18px;font-weight:900;line-height:1.4;white-space:normal}
.meta p{font-size:13.5px;line-height:1.75;color:var(--sub);margin-top:4px}
.foot{font-size:12.5px;color:var(--sub);margin-top:30px}
.foot a{color:var(--g)}
@media(min-width:760px){.grid{grid-template-columns:1fr 1fr}}
"""
    body = f"""<div class="w"><header>{LOCKUP}</header>
<h1 class="ttl">LPデザイン5案の見比べ</h1>
<p class="lead">本文はすべて現行ページと同じです。番号で選んでください。カードを押すと各案が開きます。</p>
<div class="grid">{cards}</div>
<p class="foot">現行の公開ページ：<a href="../">yukitchy.github.io/money-setup-lp/</a></p></div>"""
    out = page(0, "見比べボード", css, body)
    out = out.replace(f"{BASE}v0.html", BASE).replace("｜デザイン案0 見比べボード", "｜デザイン5案 見比べボード")
    (HERE / "index.html").write_text(out)
    print("index.html", len(out))


board()
