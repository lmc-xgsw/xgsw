# -*- coding: utf-8 -*-
"""孝感水文整点到报 - GitHub Actions"""
import requests,datetime,os
CLIENT_ID=os.environ["CLIENT_ID"]
CLIENT_SECRET=os.environ["CLIENT_SECRET"]
TOKEN_URL='https://api-hbwater.wetruetech.net/api/internet-cm-authenticate/oauth2/token'
BASE='https://api-hbwater.wetruetech.net/api/internet-cm-api'

REGIONS={
    "汉川37":[
        ["62246900","麻河","雨量站"],
        ["62248900","里潭","雨量站"],
        ["62249100","韩集","雨量站"],
        ["62249500","刘家隔","雨量站"],
        ["62249700","分水","雨量站"],
        ["62251220","西江","雨量站"],
        ["62251320","南河","雨量站"],
        ["62251500","城隍","雨量站"],
        ["62251700","汈东","雨量站"],
        ["62251750","回龙","雨量站"],
        ["62251900","马鞍","雨量站"],
        ["62210800","五房台（水位）","雨量站河道"],
        ["62210820","余家咀","河道"],
        ["62212180","福星","雨量站河道"],
        ["62212300","南屏闸","雨量站闸上"],
        ["62212320","庙头","雨量站河道"],
        ["62212610","汉川闸（闸上闸位）","雨量站闸上"],
        ["62212620","汉川闸（闸下）","闸下"],
        ["62212810","民乐闸上闸位","雨量站闸上"],
        ["62212820","民乐闸下","闸下"],
        ["62209500","喻家闸","雨量站河道"],
        ["62210610","中洲桥","雨量站河道"],
        ["62210650","新堰闸","雨量站河道"],
        ["62248600","七一桥","雨量站"],
        ["62251600","同兴集","雨量站"],
        ["62210800","五房台（雨量）","雨量站河道"],
        ["62212210","万福闸（雨量）","雨量站闸上"],
        ["62212410","汉川泵站（上）","闸上"],
        ["62212420","汉川泵站（下）","闸下"],
        ["62212610","汉川闸上雨量","雨量站闸上"],
        ["62212610","汉川闸（闸上）","雨量站闸上"],
        ["62212810","民乐闸（闸上）","雨量站闸上"],
        ["62207210","新沟闸（闸上）","闸上"],
        ["62207220","新沟闸（闸下）","闸下"],
        ["62210510","汪家台","河道"],
        ["62212210","万福闸（水位）","雨量站闸上"],
        ["62212220","万福闸（闸下）","闸下"],
    ],
    "大悟25":[
        ["50202246","魏家冲-浮子","雨量站河道"],
        ["50224060","丰店","雨量站"],
        ["62234500","芳畈","雨量站"],
        ["62234100","东新","雨量站"],
        ["62234300","柳林","雨量站"],
        ["62234400","滚子河","雨量站"],
        ["50224275","刘家","雨量站"],
        ["61609000","河口桥","雨量站河道"],
        ["61634100","四姑","雨量站"],
        ["61634300","刘集","雨量站"],
        ["61634500","韩家河","雨量站"],
        ["62205400","草店（水位）","雨量站河道"],
        ["62205400","草店（雨量）","雨量站河道"],
        ["50201991","会馆","雨量站河道"],
        ["61634401","彭店","雨量站水库"],
        ["61633600","黄陂站","雨量站"],
        ["61633800","吕王城","雨量站"],
        ["61635400","夏店","雨量站"],
        ["50202245","魏家冲-气泡","雨量站河道"],
        ["62233600","大新店","雨量站"],
        ["62233800","姚家店","雨量站"],
        ["62234000","高家店","雨量站"],
        ["62233400","三里城","雨量站"],
        ["50224150","宣化店","雨量站"],
        ["61634200","河口","雨量站"],
    ],
    "孝昌20":[
        ["62237100","观音岩","雨量站"],
        ["62237300","周巷","雨量站"],
        ["62237550","邹岗","雨量站"],
        ["62237600","白沙铺","雨量站"],
        ["62236500","花西","雨量站"],
        ["62236700","卫店","雨量站"],
        ["62236900","陡山","雨量站"],
        ["62237900","双峰","雨量站"],
        ["62238200","青板桥","雨量站"],
        ["62203800","观音岩水库","雨量站"],
        ["62205350","堰口","雨量站河道"],
        ["62205500","双桥","雨量站河道"],
        ["62206500","王店","雨量站河道"],
        ["62238600","祝家湾","雨量站"],
        ["62237200","姚家山","雨量站"],
        ["62205600","花园蒸发","雨量站河道"],
        ["62205600","花园水位","雨量站河道"],
        ["62205600","花园雨量","雨量站河道"],
        ["62205600","花园流量","雨量站河道"],
    ],
    "孝南24":[
        ["62238100","肖港","雨量站"],
        ["62238300","东西杨","雨量站"],
        ["62238500","新铺","雨量站"],
        ["62238700","毛陈","雨量站"],
        ["62238900","杨店","雨量站"],
        ["62239100","闵集","雨量站"],
        ["62201500","凤凰台","雨量站河道"],
        ["62202100","三汊","雨量站河道"],
        ["62202150","星火","雨量站河道"],
        ["62205700","农三","雨量站河道"],
        ["62205900","复兴","雨量站河道"],
        ["62206610","东山头雨量","雨量站闸上"],
        ["62206610","东山头闸上水位","雨量站闸上"],
        ["62206620","东山头（闸下）","闸下"],
        ["62206580","王母湖","雨量站水库"],
        ["62206590","野猪湖","雨量站水库"],
        ["62206625","童家湖","雨量站水库"],
        ["62205750","杨家咀上","雨量站河道"],
        ["62205850","河口闸","雨量站河道"],
        ["62201800","卧龙潭","雨量站河道"],
        ["62205800","孝感浮子","河道"],
        ["62205800","孝感","河道"],
        ["62206490","滑石冲","雨量站水库"],
    ],
    "安陆18":[
        ["62236600","陈家店","雨量站"],
        ["62231300","刘家竹园","雨量站"],
        ["62231400","孛畈","雨量站"],
        ["62231600","接官厅","雨量站"],
        ["62232000","棠棣树店","雨量站"],
        ["62200810","安陆（蒸发）","雨量站闸上"],
        ["62200810","安陆（闸上闸位）","雨量站闸上"],
        ["62200840","安陆(闸下)","闸下"],
        ["62201100","双龙桥","雨量站河道"],
        ["62201300","孛畈街","雨量站河道"],
        ["62205180","郑家河（水位）","雨量站水库"],
        ["62205180","郑家河（雨量）","雨量站水库"],
        ["62200810","安陆（雨量）","雨量站闸上"],
        ["62205300","幸福","雨量站水库"],
        ["62231960","武家河","雨量站"],
        ["62200810","安陆（水位）","雨量站闸上"],
        ["62200830","安陆（电站上）","水库"],
    ],
    "应城17":[
        ["62242800","渔子河","雨量站"],
        ["62242900","陈河","雨量站"],
        ["62246100","田店","雨量站"],
        ["62246300","赵畈","雨量站"],
        ["62246500","郎君","雨量站"],
        ["62246700","天鹅","雨量站"],
        ["62233700","三合","雨量站"],
        ["62233900","东马坊","雨量站"],
        ["62208701","张万闸上","雨量站闸上"],
        ["62208702","张万闸下","雨量站闸下"],
        ["62209400","应城（雷达燕禹）","雨量站河道"],
        ["62246400","短港","雨量站"],
        ["62208620","龙赛湖（闸下）","闸下"],
        ["62209400","应城（水位）","雨量站河道"],
        ["62209400","应城（雨量）","雨量站河道"],
        ["62208610","龙赛湖（闸上）","雨量站闸上"],
        ["62208620","龙赛湖（闸下）","闸下"],
    ],
    "云梦15":[
        ["62232200","唐陈","雨量站"],
        ["62232300","曾店","雨量站"],
        ["62232500","云梦城关","雨量站"],
        ["62233100","伍洛","雨量站"],
        ["62233300","道桥","雨量站"],
        ["62233500","下辛店","雨量站"],
        ["62200900","杨林","雨量站河道"],
        ["62201600","护子潭","雨量站河道"],
        ["62201700","伍洛桥","雨量站河道"],
        ["62201900","云梦闸","雨量站河道"],
        ["62201400","隔蒲潭","雨量站河道"],
    ],
}


r=requests.post(TOKEN_URL,data={"client_id":CLIENT_ID,"client_secret":CLIENT_SECRET,"grant_type":"client_credentials"},timeout=15)
h={"Authorization":f"Bearer {r.json()["access_token"]}"}

now=datetime.datetime.utcnow()+datetime.timedelta(hours=8)
latest=now.replace(minute=0,second=0,microsecond=0)
if now.minute<5: latest-=datetime.timedelta(hours=1)
hs=latest.strftime("%Y-%m-%dT%H:%M:%S")
today=latest.strftime("%Y-%m-%d")

report={}
r=requests.get(f"{BASE}/hif/river/page?pageSize=500&sttm={today}+00:00:00",headers=h,timeout=15)
if r.json().get("code")==0:
    for rec in r.json()["data"]["records"]:
        if hs[:13]==rec.get("tm","")[:13]:
            cd=rec["stcd"]; report[cd]={"z":rec.get("z"),"q":rec.get("q")}
r=requests.get(f"{BASE}/hif/rain/page?pageSize=500&sttm={today}+00:00:00",headers=h,timeout=15)
if r.json().get("code")==0:
    for rec in r.json()["data"]["records"]:
        if hs[:13]==rec.get("tm","")[:13]:
            cd=rec["stcd"]
            if cd in report: report[cd].update({"drp":rec.get("drp")})
            else: report[cd]={"drp":rec.get("drp")}

total_all=sum(len(v) for v in REGIONS.values())
total_ok=sum(1 for v in REGIONS.values() for _,stcd,_ in v if stcd in report)

bar=""
for rn,ss in REGIONS.items():
    ok=sum(1 for _,stcd,_ in ss if stcd in report)
    color="#16a34a" if ok==len(ss) else "#ea580c" if ok>=len(ss)*0.8 else "#dc2626"
    bar+=f'<div class="stat"><div class="num" style="color:{color}">{ok}<span class="total">/{len(ss)}</span></div><div class="lab">{rn}</div></div>'

blocks=""
for rn,stations in REGIONS.items():
    ok=sum(1 for _,stcd,_ in stations if stcd in report)
    rows=""
    for cd,nm,tp in stations:
        d=report.get(cd,{}); isok=cd in report
        rows+=f'<tr><td>{cd}</td><td>{nm}</td><td class="type">{tp}</td><td class="{"ok" if isok else "miss"}">{"OK" if isok else "-"}</td><td>{d.get("z","")}</td><td>{d.get("q","")}</td><td>{d.get("drp","")}</td></tr>'
    blocks+=f'<div class="region"><div class="rh"><span>{rn}</span><span class="sub">{"OK" if ok==len(stations) else "缺"+str(len(stations)-ok)}</span></div><table><thead><tr><th>站码</th><th>站名</th><th>类型</th><th>状态</th><th>水位</th><th>流量</th><th>雨量</th></tr></thead><tbody>{rows}</tbody></table></div>'

html=f"""<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>孝感水文整点到报查询</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"Microsoft YaHei","PingFang SC",sans-serif;background:#f5f5f5;color:#333;padding:20px;max-width:1100px;margin:0 auto}}
h2{{font-size:20px;font-weight:600;margin-bottom:4px;color:#1a1a1a;text-align:center}}
.time{{font-size:13px;color:#666;margin-bottom:12px;text-align:center}}
.stats{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:12px}}
.stat{{background:#fff;border-radius:8px;padding:8px 12px;text-align:center;min-width:70px;box-shadow:0 1px 3px rgba(0,0,0,.08);border:1px solid #eee}}
.stat .num{{font-size:22px;font-weight:700}}
.stat .total{{font-size:12px;color:#999;font-weight:400}}
.stat .lab{{font-size:11px;color:#888;margin-top:2px}}
.region{{margin-bottom:8px;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.06);border:1px solid #eee}}
.rh{{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:#fafafa;font-size:14px;font-weight:600;border-bottom:1px solid #eee}}
.sub{{font-size:11px;color:#888;font-weight:400}}
table{{width:100%;border-collapse:collapse;font-size:11px}}
th{{background:#f8f8f8;padding:6px 4px;text-align:left;border-bottom:2px solid #e0e0e0;color:#666;font-weight:500}}
td{{padding:5px 4px;border-bottom:1px solid #f0f0f0;color:#444}}
tr:hover td{{background:#f0f4ff}}
td.type{{color:#888;font-size:10px}}
td.ok{{color:#16a34a;font-weight:600}}
td.miss{{color:#dc2626;font-weight:600}}
.update{{text-align:center;font-size:11px;color:#999;margin-top:8px}}
</style><meta http-equiv="refresh" content="600"></head><body>
<h2>孝感水文整点到报查询</h2>
<div class="time">{latest.strftime("%Y年%m月%d日 %H:00")} | {total_all}站 | 到报{total_ok}站 | {round(total_ok/total_all*100,1) if total_all else 0}%</div>
<div class="stats">{bar}</div>
{blocks}
<div class="update">10分钟自动刷新 | GitHub Actions每小时更新数据 | 云端托管</div>
</body></html>"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
print(f"OK: {len(html)} bytes, {total_ok}/{total_all} reported")
