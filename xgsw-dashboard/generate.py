# -*- coding: utf-8 -*-
"""孝感水文整点到报 - GitHub Actions 自动生成"""
import requests,json,datetime,os

# ── 认证 ──
CLIENT_ID=os.environ['CLIENT_ID']
CLIENT_SECRET=os.environ['CLIENT_SECRET']
TOKEN_URL='https://api-hbwater.wetruetech.net/api/internet-cm-authenticate/oauth2/token'
BASE='https://api-hbwater.wetruetech.net/api/internet-cm-api'

# ── 测站信息（从Excel提取，按地区分组）──
REGIONS={
    '汉川':[('62233300','万家坝','雨量站'),('62232000','汉川泵站下','雨量站'),('62231600','铁李港闸','雨量站'),('62231400','安河','雨量站'),('62202150','城隍','雨量站'),('62201900','民乐闸','雨量站'),('62201500','万福台','雨量站'),('62201300','杨林步','雨量站'),('62212320','泵头','雨量站'),('62205350','双龙桥','雨量站河道'),('62210800','五房台','雨量站河道'),('62210820','余家咀','河道'),('62212180','福星','雨量站河道'),('62212210','万福闸','雨量站闸上'),('62215020','南屏闸','雨量站闸上'),('62201800','新沟潭','雨量站'),('62201700','麻河镇','雨量站'),('62248350','汉川闸','雨量站闸上'),('62248370','汉川闸','闸下'),('62248600','七一桥','雨量站'),('62251320','庙头','雨量站河道'),('62251220','喻家闸','雨量站河道'),('62251500','中洲桥','雨量站河道'),('62251600','同兴集','雨量站'),('62251900','新堰闸','雨量站河道'),('62251700','汈东','雨量站'),('62251750','回龙','雨量站'),('62242900','麻河','雨量站'),('62242800','里潭','雨量站'),('62249100','韩集','雨量站'),('62249500','刘家隔','雨量站'),('62249700','分水','雨量站'),('62251220','西江','雨量站'),('62251320','南河','雨量站'),('62251500','城隍','雨量站'),('62251750','马鞍','雨量站')],
    '大悟':[('50202246','魏家冲-浮子','雨量站河道'),('50202245','魏家冲-气泡','雨量站河道'),('50224060','丰店','雨量站'),('50201991','会馆','雨量站河道'),('50202206','大胜关','雨量站'),('50224045','汪洋潭','雨量站'),('50224150','双桥镇','雨量站'),('50224270','刘集','雨量站'),('50224275','刘家','雨量站'),('50224302','黑沟','雨量站'),('50224304','墨关','雨量站')],
    '孝昌':[('62237100','观音岩','雨量站'),('62237200','姚家山','雨量站'),('62237300','周巷','雨量站'),('62237550','邹岗','雨量站'),('62237600','白沙铺','雨量站'),('62236500','花西','雨量站'),('62236600','陈家店','雨量站'),('62236700','卫店','雨量站'),('62236900','陡山','雨量站'),('62237900','双峰','雨量站'),('62238100','肖港','雨量站'),('62238200','青板桥','雨量站'),('62238300','东西杨','雨量站'),('62238500','新铺','雨量站'),('62238600','祝家湾','雨量站'),('62238700','毛陈','雨量站'),('62238900','杨店','雨量站'),('62239100','闵集','雨量站'),('62246500','郎君','雨量站')],
    '孝南':[('62237100','观音岩','雨量站'),('62238100','肖港','雨量站'),('62238300','东西杨','雨量站'),('62238500','新铺','雨量站'),('62238700','毛陈','雨量站'),('62238900','杨店','雨量站'),('62239100','闵集','雨量站'),('62210800','五房台','雨量站河道'),('62215020','南屏闸','雨量站闸上'),('62212210','万福闸','雨量站闸上')],
    '安陆':[('50224060','丰店','雨量站'),('50202206','大胜关','雨量站'),('50224045','汪洋潭','雨量站'),('50224150','双桥镇','雨量站'),('50224270','刘集','雨量站'),('50224275','刘家','雨量站'),('50224302','黑沟','雨量站'),('50224304','墨关','雨量站')],
    '应城':[('62242800','渔子河','雨量站'),('62242900','陈河','雨量站'),('62246100','田店','雨量站'),('62246300','赵畈','雨量站'),('62246500','郎君','雨量站'),('62246700','天鹅','雨量站'),('62246400','短港','雨量站')],
    '云梦':[('62236500','花西','雨量站'),('62236700','卫店','雨量站')]
}

# ── 获取Token ──
r=requests.post(TOKEN_URL,data={'client_id':CLIENT_ID,'client_secret':CLIENT_SECRET,'grant_type':'client_credentials'},timeout=15)
h={'Authorization':f'Bearer {r.json()["access_token"]}'}

now=datetime.datetime.utcnow()+datetime.timedelta(hours=8)  # UTC+8
latest=now.replace(minute=0,second=0,microsecond=0)
if now.minute<5: latest-=datetime.timedelta(hours=1)
hs=latest.strftime('%Y-%m-%dT%H:%M:%S')
today=latest.strftime('%Y-%m-%d')

# ── 查询河道+雨量数据 ──
report={}
r=requests.get(f'{BASE}/hif/river/page?pageSize=500&sttm={today}+00:00:00',headers=h,timeout=15)
if r.json().get('code')==0:
    for rec in r.json()['data']['records']:
        if hs[:13]==rec.get('tm','')[:13]:
            cd=rec['stcd']; report[cd]={'z':rec.get('z'),'q':rec.get('q')}
r=requests.get(f'{BASE}/hif/rain/page?pageSize=500&sttm={today}+00:00:00',headers=h,timeout=15)
if r.json().get('code')==0:
    for rec in r.json()['data']['records']:
        if hs[:13]==rec.get('tm','')[:13]:
            cd=rec['stcd']
            if cd in report: report[cd].update({'drp':rec.get('drp')})
            else: report[cd]={'drp':rec.get('drp')}

# ── 统计 ──
total_all=sum(len(v) for v in REGIONS.values())
total_ok=sum(1 for v in REGIONS.values() for _,stcd,_ in v if stcd in report)

bar=''
for rn,ss in REGIONS.items():
    ok=sum(1 for _,stcd,_ in ss if stcd in report)
    color='#16a34a' if ok==len(ss) else '#ea580c' if ok>=len(ss)*0.8 else '#dc2626'
    bar+=f'<div class="stat"><div class="num" style="color:{color}">{ok}<span class="total">/{len(ss)}</span></div><div class="lab">{rn}</div></div>'

blocks=''
for rn,stations in REGIONS.items():
    ok=sum(1 for _,stcd,_ in stations if stcd in report)
    rows=''
    for cd,nm,tp in stations:
        d=report.get(cd,{}); isok=cd in report
        rows+=f'<tr><td>{cd}</td><td>{nm}</td><td class="type">{tp}</td><td class="{"ok" if isok else "miss"}">{"OK" if isok else "-"}</td><td>{d.get("z","")}</td><td>{d.get("q","")}</td><td>{d.get("drp","")}</td></tr>'
    blocks+=f'<div class="region"><div class="rh"><span>{rn}</span><span class="sub">{"已到报" if ok==len(stations) else "缺"+str(len(stations)-ok)}</span></div><table><thead><tr><th>站码</th><th>站名</th><th>类型</th><th>状态</th><th>水位</th><th>流量</th><th>雨量</th></tr></thead><tbody>{rows}</tbody></table></div>'

html=f'''<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
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
<div class="time">{latest.strftime('%Y年%m月%d日 %H:00')} | {total_all}站 | 到报{total_ok}站 | {round(total_ok/total_all*100,1) if total_all else 0}%</div>
<div class="stats">{bar}</div>
{blocks}
<div class="update">每10分钟自动刷新 | 云端托管 | 每小时更新数据</div>
</body></html>'''

with open('index.html','w',encoding='utf-8') as f:
    f.write(html)
print(f'Generated: {len(html)} bytes, {total_ok}/{total_all} reported')
