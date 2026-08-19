from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W,H=1920,1440
WHITE=(255,255,255); BLACK=(18,18,18); DARK=(27,27,27); RED=(181,0,0); GRAY=(105,105,105); LG=(238,238,238)
font_b='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_r='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def F(size,bold=True): return ImageFont.truetype(font_b if bold else font_r,size)

def wrap(draw,text,font,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        test=(cur+' '+w).strip()
        if draw.textbbox((0,0),test,font=font)[2] <= maxw: cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def shield(d,x,y,s=1.0):
    pts=[(x,y),(x+110*s,y+25*s),(x+100*s,y+130*s),(x+55*s,y+170*s),(x+10*s,y+130*s)]
    d.polygon(pts,fill=RED,outline=BLACK)
    d.text((x+30*s,y+38*s),'K',font=F(int(72*s)),fill=WHITE)

def scales(d,x,y,s=1.0):
    c=(95,95,95); w=max(3,int(8*s))
    d.line((x,y,x,y+230*s),fill=c,width=w)
    d.line((x-130*s,y+55*s,x+130*s,y+55*s),fill=c,width=w)
    d.ellipse((x-22*s,y+205*s,x+22*s,y+249*s),fill=c)
    for side in (-1,1):
        bx=x+side*105*s
        d.line((bx,y+55*s,bx-45*s,y+145*s),fill=c,width=max(2,int(4*s)))
        d.line((bx,y+55*s,bx+45*s,y+145*s),fill=c,width=max(2,int(4*s)))
        d.arc((bx-55*s,y+128*s,bx+55*s,y+190*s),0,180,fill=c,width=max(2,int(5*s)))

def card(city,slug,idx,title,subtitle,bullets):
    im=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(im)
    # background accents
    d.arc((-420,-300,780,950),40,310,fill=LG,width=70)
    d.arc((-290,-180,650,800),40,310,fill=(247,247,247),width=25)
    d.polygon([(1480,0),(1920,0),(1920,420)],fill=RED)
    # brand
    shield(d,90,55,0.78)
    d.text((225,78),'KVODOS',font=F(90),fill=BLACK)
    d.text((230,178),'ЮРИДИЧЕСКАЯ ЗАЩИТА',font=F(32,False),fill=GRAY)
    # headline
    y=310
    hf=F(88)
    lines=wrap(d,title,hf,1120)
    for j,line in enumerate(lines[:4]):
        d.text((110,y),line,font=hf,fill=RED if j==len(lines)-1 and len(lines)>1 else BLACK)
        y+=108
    sf=F(34,False)
    for line in wrap(d,subtitle,sf,960)[:2]:
        d.text((115,y+10),line,font=sf,fill=(55,55,55)); y+=50
    # city pill
    py=min(y+35,870)
    d.rounded_rectangle((115,py,700,py+92),radius=22,fill=RED)
    d.text((170,py+18),f'г. {city}',font=F(45),fill=WHITE)
    # bullets
    by=py+135
    bf=F(31)
    for b in bullets[:4]:
        d.ellipse((125,by+7,153,by+35),fill=RED)
        d.text((175,by),b,font=bf,fill=BLACK)
        by+=64
    # right legal objects
    d.rounded_rectangle((1270,405,1720,1015),radius=25,fill=(36,36,36),outline=(80,80,80),width=5)
    shield(d,1415,535,1.45)
    scales(d,1130,590,1.25)
    # document stack
    for k in range(5): d.rectangle((1030+k*18,990-k*18,1660+k*8,1185-k*12),fill=(249,249,249),outline=(205,205,205),width=2)
    d.text((1120,1025),'ЗАЯВЛЕНИЕ',font=F(38),fill=RED)
    d.text((1120,1085),'о внесудебном банкротстве',font=F(23,False),fill=GRAY)
    # footer
    d.rectangle((0,1240,W,H),fill=DARK)
    d.text((115,1300),'ЗАКОННО И НАДЕЖНО',font=F(33),fill=WHITE)
    d.text((660,1300),'ПО ДОГОВОРУ',font=F(33),fill=WHITE)
    d.text((1100,1300),'ОПЫТНЫЕ ЮРИСТЫ',font=F(33),fill=WHITE)
    d.text((1580,1300),'ПО ВСЕЙ РОССИИ',font=F(30),fill=WHITE)
    out=Path('avito/bankruptcy')/slug/f'{slug}_{idx}.png'; out.parent.mkdir(parents=True,exist_ok=True)
    im.save(out,optimize=True)
    print(out)

cities={
 'saratov':'Саратов',
 'novosibirsk':'Новосибирск',
 'ekaterinburg':'Екатеринбург',
 'omsk':'Омск',
 'belgorod':'Белгород',
}
sets=[
 ('ВНЕСУДЕБНОЕ БАНКРОТСТВО','Юридическая помощь при процедуре через МФЦ',['Проверка ситуации','Подготовка документов','Список кредиторов','Сопровождение']),
 ('ПОДХОДИТ ЛИ ВАМ БАНКРОТСТВО ЧЕРЕЗ МФЦ?','Предварительный анализ до подачи заявления',['Проверка оснований','Анализ ФССП','Проверка кредиторов','Консультация']),
 ('ПОДГОТОВКА ДОКУМЕНТОВ','Комплект для внесудебного банкротства',['Заявление в МФЦ','Список кредиторов','Проверка данных','Юридическая помощь']),
 ('ПОДАЧА ЧЕРЕЗ МФЦ С СОПРОВОЖДЕНИЕМ','Юрист помогает пройти этапы процедуры',['Проверка комплекта','Подготовка к подаче','Разбор этапов','Поддержка']),
 ('ВЕРНУЛИ ЗАЯВЛЕНИЕ?','Разберём причину и подготовим повторную подачу',['Анализ причины','Исправление ошибок','Новый комплект','Повторная подача']),
 ('КОНСУЛЬТАЦИЯ ПО БАНКРОТСТВУ','Онлайн помощь и понятный алгоритм действий',['Разбор ситуации','Ответы на вопросы','Работа по договору','По всей России']),
]
for slug,city in cities.items():
    for i,(t,s,b) in enumerate(sets,1): card(city,slug,i,t,s,b)
