#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json

def main(TL):
    """"""
    entryLIST = []
    tlLIST = TL.split("\n")
    for t in tlLIST:
        entry = t.split(",")
        entryLIST.append([list(entry[0]), entry[1].strip().split(" ")])

    #for e in entryLIST:
        #if len(e[0]) != len(e[1]):
            #print(e)

    tlDICT = {}
    for e in entryLIST:
        for c in e[0]:
            if c in tlDICT:
                pass
            else:
                tlDICT[c] = []
            tlDICT[c].append(e[1][e[0].index(c)])
    for k in tlDICT:
        tlDICT[k] = max(set(tlDICT[k]), key = tlDICT[k].count)
    #print(tlDICT)
    s = """建均醮聞撞沬倉椪容卸姦游消描他雙悽檨津稀囝查基胞告掀鑠靈爬傀搐甍嚙紅低窗臍糠盜虱裕櫃險頸鞭帶奇釘佑滅厄獄唌謝茈罟弱撈葩檫百逐切文福怨仕板繃窣捻條輾組幡銀育共梨成株霸易晃掰便抑墟墨連惜詳跕值爐恐欱?區貪記嫣占泅目奶哽卵㨑闊小在晬擘雷二濫躇約竅覽微道熨甌痔泱綴藥阻般炎崩卷扇埠巧湧迷裘醬碗美好帕皂冗詼簽偷敏介巡堵癌權添膎沉慰州俺…背勾漏享趖吧慶嚵烌光耙裼3排傑素癀誤主去餅禍謙獵齧隍荏然礪捧轎塗羊休伐挽喈訪儱圳屍供反庭復躘阿閒擢穢嘉翠辯勻淘啊柙離蛄t兵頦譬訕片苗卑古淹了樓北饞幌儑𢲸蚓土總賊卿菁柄豹埃煡躼免疑視拘綵繐神后路歡篱燉臘肚梳舂蹤𨂿旱挕子攔刻茶槺拌栓搙宅松揮科牲𦉎捆佳猴撐埕鴨吹抱扦效雲姐作探疧洋廢生痠跔菜位械兄葬僚分妥忠鞘測檔勼脬哹突膽蛾鬼痲辦浮仙司顎欄受速為叩囂早拋禿怦拎翕？擂靴瓣性臣㨂橐胸蒜篩瀾細浪黜鸕星夏境腦藍枸甚扷涉親極耕季銃傲貿侯芽繼慨薸渡惱巷吮普伸齁聳貝媌傱馝蠅做契麴陷牆𤶃驛味裁幔空爁搟遊腡藐𠞩藤准城躡崎芟閏天索循吶唱烏算飄滲蹊鯊況大惰步眾糙秀帖坯脈寨籃剿遙懇僥艱稿嗽侮盪抿堅激定芒找娶匙毬豆刜戊令鴆臺糖榔聿剉夕繭鹹缽芎缺\ue703顧少痣湢枉薯脊沕泳呼趨態母鞦克活虎丙姑聘沛階昭羞襪忝旋棄草冤療就獨胡那火肥華儡宛叔則唉依詭遹腸敧庚歁嶺廍郎擒接雁攢揤替倏晶蟲論旗諾蔬揲川研煞噹溝求夭狗染賞件樹仿箍漉虼鉛啄宵譜婚量抽巾避較罾蹄𧉟引瑰縋角箱宴鈃尿卡葵輦剃螕姆瞭弓瞞怪鳳吸務溫娘盒服漖一學鋤備唸暈辭瘦膨䆀裾夢飼槍鵁搣悲蒂枴互碑除趺寄嚾焦：閃勥看尋室即瘰賠𥐵獎漂振座柑灇卦狽帆𥰔酉脅祈榕膁三韌揹薟睨耍乩戇野西種萄和災才判舖編居喝討纖擦魄詩輕孽病桮謔掜揀柿荍梢怙\u3000'
 '鵤故機傅喨雅彬箔動罵斟䖙禪眼糜鈍氅殘苴南拗直敗贊咯萎斤櫳複猌膚底省印疏，誌屐𪁎冒遇軀煎羹戥抌概桔販(亥鼾英塔筊骿屑敵違蝶前撮鰻呿宗豸優掉山抹灘褪應樸𡳞碭夫糍束奉菊出蚤下歐走趕蔗胎桷慷奴戶丑守挂炭魂篡馬剺采舌園剋伴哭瑯負嚨沾穡嬌鮑歲挐短宣象源謼壁汫狡傍啉改仆拳哖熟喑塚旅千罐賭繞咒㴘佩我蝦鍋熬配墾椏臨缸床黗縣布辱夠喜強獻粧響迫逞𩚨蠓蛋枕笱柝咂站縖譎𣛮宿痧扛贏簷b漚菱憐唚操立掩快申房胘墜隙翸女諍賢流䫌技盡嫂痰置邱紫蕉笑頷午祠己雹敨麗桌償鈷真啦心毒吭戛搝箬尺伯櫻拇規砧癢曉挓挔儼始䀐𧿬碎順畏王櫓辛往儉徒花陽刮鑼幾兆紳擾炕蜷窟絕億嘩燜昏𪐞凊撆難海績箸月票減媒蛤砂瘡曆聖掌猛岫具錯揫溡渴羅厭冇秦鋪㴙卜椅播哀牡俗嬸喔屁持杉爆鬆鑾妖á燖䘥碼覺延吊閣欲由攑惶字現鞍企踮杏疾𩛩箠氏鈴遍薑餡失塌面糝憑扭世打跂跍呧每裝𠞭符哪惝撫抨「潲群答史頻贌㧌捷鬍體酥尚喘訴謎輩班捙疼恂搵手乖-歷í競滷穎墓包酸吉逍橂哲也騎泄貓噓絳高胃撇題蘋致枝湖掛紀武竟顢嚓穩猜胚歕物插評礁昧計焐枵足憢該鋼筧逼袚頇搧侗簇院爛飢言爺衛薄鶖扳捾膩架丟撋冠雀鬧鄰還專熥h胴叉從柳坎解多牢威聬閘半內煏皺降奒碇丈鼎苛0釣磨破哥蠻慼翹」本薰彩鍊削屈奕席襞而變魔薦業酬愣朗勵報尾仁囡校治如栗噗曜警奸舒債困壬社筍曷砛淋彼財惡榮健烘揚元息抓痀㧣今檀膠偌粞疔抗溼過穀磅堆招樣卌跳硩搜孩酌工蕗諸宋屏辰疲紗摻晉拂龍戳顏剾莫辣噪藃退煨簾垃回據煉薪氣麒挃虛擇俳章鋟奈蟄邀臢鬖課搢停睫黹熔壘肺丸比參冰脂語掙聽鎖制𠯗墳a攕稽嘔產度遏拭頕青蕊註必姓脆甕嗄舍護悔稜艋上同沙軍仗塭莊捎蔥蹓熱呴坦裂妻襟睭李試賴口矮閂整捏眩濁蹁義懸爍篾礤蔓管波保棋𡢃笒思首癬𦊓譯協繡啾糾廟幫盲爹付祥腫攄沖朋棉㨻哺碰幽烈瞪菇忘問潭齴春帽剔汁鬃尪錚貴泰芝翻颱蟮籌傷勒軟萬窸派迸匪粒俐洪略揭涗獅壞。楚車閉八殗雕扎\uf5e9罪妣身蛀腌按慾凍勢𥍉狂媠局泡私界憂痕程甘霎抄埤勇偕佈都岩似挑術跟勞煽撥鬚借先瓜典橫簫醫猫悟𤆬怫齆徙滿露嚇損裹檠抐廕絆絚溪慈杞罩孤𢼌特挩搭剪浞稱屜剷識熁覕摺簿糕禽表敱市弔𢯾皮墘炰斥誠遨幼聲楹死咍救愁拈孝糞槌團佛聊止祿審紬莽飫寬熄於郵芡昨奏伍狹罰杙𣮈嘻錘茂滋栽五─擴㾀漸蝒淨瀳賤談戽升痴佗湯買刁擤闔犯膭旁赴滂匾貢莓鐘核畚喪擺斜密修既糊躽𩑾鋏凌泉痟髻纏街嘈櫞項乏策駛傳恬筅骰呸啼拉撩黐噁滓侍塞脾捨噸炤暖燥崁且鈕袋肛君絲峇募巴偏袱㔂o年鴒施圾仇戀划n爪仔慮秒餌扣擋聰咳摵騷監帝讚不若敢籠膿織吟噷哈桃阮龜再系沐洞扯縭蚶鹽用顫永係份蔭僻話棗扁𦜆蓄儳錐錦因線要厚嘆額但豪到四嬰垂貨埽尖堪撨楦嗾癮恭擠命硞嘹貧飲廉倒已紺姻伻冊妾銅欶忌中將併剩榫剝宮絃跪濆鯪礐擊以棕貺髡啥羨鬢飆乍罨送灣刣理勤喲瘸龐鄙遣欺娗晏誦疊呢褒善亦杓鱗示嫌睏遵附賜國憲赦尊畢搤跤椒果賓洗盼形婸讓逃庫攏𣻸鯉攪酺蛆漿扲六類採毋發陸宕壇繳跡韆笨溜肅捽翼信榴倯慎挾掂池擲滾籤襇韭鮫囊隱娥揣徛戰醉觀挲確嗙驕i士鑽祧蜂眵劇夜捔燃畫笠鬥叫漠溶鬱盟括浴統框醴酵縒睚端議倍爭照末杮縮誘叨哎粿騙液杆淺番漲調場別籬塑眉常肢愈壺藕衣疶留蓆𥴊給蝹麩乞扒自囤沿知糋朝疤趣眷拒針梯𧿳推荒拹讀唏處盆吐齒島尼澀佇凶芹慄精窮褂滯費寧䠡緟革欹鰇貼哉蛇簡虯霆臊仄稅腿官滴疕香軁漁癉蔫枇煙劍揌佮炒撬揬懶揉ú淚臉利蕎胳柯俍隨蟳枷寒纓泔箕赤田淑鏨呔至躄餃帚例縛者𨂾這肉質挨韻錢琴劃厲濟襻圈之觳鑢鉼痺籗璇匼扞搖硯胭䈄掠彙胛齪糴乙選召絹苔㤉濾障任；蟯爽奢頭式渺滒焠匠㨨𧮙芬𠕇防虧蹧圍拔匹蚵望鵝逢攻段拑炊礦棺賒鴉掣平芋各捶林害鞏榜揈旦冷敬刺次汰白鶿運芥偝填痛稻男邪代刊虐牚橛涼洩屬猶屘飽造通圖囚唔轟夥綜刐餾書鐵欸倚詬症齊篋固暢完鉤授慕庄演呆廳燭緻箅壅k盤豉臟獠蘆粗迌兔噴鉎棟嗚挵荷挌趼鑄診嘖陰支喙個射寵著个僆奪股催當呲範慣煠蛛搶翁品乜喻遠抵輪吱 '
 '銷礎智祝坐慢商電癖陳玉怎煬玩篇澄掇漩舅桸珠腑純鮮恨閻亭袂公丹硬碡窞詞維零根紙牙喃圇暫烰彎勍木粽村人撓謄割噤絨呻曝副攝只委歹家葫差浡掔蝝急蓑鹿石款麟凹擗領菩址罕脹愛遐抔正礬絞適\uf5e7富蟶潑瀉狐鱸拖終諒越櫼寸暴麥摁茄餲晟弟鑑明部貫食號囉倌博歇癗拾候脰雺跑懊康雞磚相達晾綹摠雨悾翱扮濺姨蜘是住咖烙民耐覆呵預煮煩坷許ó鼓未粅點侵噭此捀助么追傘父\uf5ef唯藝盹時隔請益苦掖篙收斗賺祟入𨑨藏展癆隊腰扴𣁳佔枋功瓦歌良伙桶雜注節頓清凡投啞腹楞金杜楊取嗤紋m摖鋩𤺪跋訓狸久託念賰縫橋血軋馴楗咱柏堡吞啡嫖級寫案戈開締箭養炱迎舺敆炮巳頂熊魯盛台蟻鉗壓創聯癩殿對嘛穗油敲絡飛賀賽迵肨飯毀習秤唬媽導嗺趁鳥踏蓋努㽎爾祕輯囫醃㧎沢遮坱祭累\uf5ea玻誡亮晝勉吩衷豐犁弄毯九丁靠誣顯姊菝擽名牽凝鬮齷薩捥友爿玲諞托柚掃伨啟殕沃葡婿捅等斡䢢筆乾𤲍\ue701途里寶擔腔篤稟扱攀捋幹捌謠版捲陪圓寺膣實蹛犧序緝蜜捒幕砉霞滇瓷牧濕燕淡芳轉交孔化兌卻嗣洒掮蹟蓬結鋸叮撙所唷拜童垺又喀霖坩怐週待牌詈啖犅魚矣姒碌皇奮慧瘋掘彈危黃瞌沫逝甜跎寡教埔嘟譴店霧磟落外港錶柱黏第摸柔溢限咧侹呾燒拍師錫篷舀荔匯衝事力船載鴛駕瓤蝨館禁驚吳寮需撚紡贖起摃日耳\ue705鴿嗹褙劌黨塊璋艾妝董觸酷髓器見張農㧒喉囷妙罷湠挖氛孵皆銎粩屧醒把喋歪太螺串寅朒辮意方厘吼霜綿臭懂焙桑長遷嘐兒嫁志水暗鞋鄉蠘府脣庇察醋玫江躊瘤員十踅經合茫熗戲嗲壙搬貯咐斑兇何饒揜涎眠會籮某嗦灶顛誇摔曖撒囥桿撏兩渧牛繚屎假欉鍥欣設幸姼寢鱉l安槓補疳卯曲非租怖矸汗陵裙僫數婦滑豚喊u撠擸蟬拐標禮豬地忤搪蜊撟蕹鼠、哼櫥綠噍戮礱責湳汙丼予㧻吵音鑿潦咾督驅膏初營坵腥冬蝕柴桱遭換夾涵嚷爸䘼仝脯毿風封鼻禱碟洲堂耎決祀宜磕裡充秋蛟剁𢪱指1誰後澹偃踢喢擉狀句燙邊繩深貸漢唿鯮鴦渣焱驗搦雪來製集嚴齣懵講痚潢澍攬客呃吠紲甲存撼東希脽兼棍潤行究井促更迒辜咇婆嘿呱秫愖瓶蓮際粟放倖倫乎坤漳疥慘謀跙並讖頁\uf5ee諺全坪考琢妒料納𠢕隆錄聚戴斯豔超最拊栱懷感衫泏臆恩歸政閹銬婢揻提僭摳捗列朱g羌跩妗戌色魍埋加鏢伶米珍遂踩暝透颺得近挺汽七聾賣幅抉胿疱刑刀窒貞劫嬈蹔曆券肝訂曾蕩眯慒漆垢散罔肯輸葉麻胮膜奅佬澳緣鎮蠟秧駐鷹賑抾棚斷燈趒認雖摘憤褲薅釧恥德酒折押族殺紮周咻盍楔使培關可能樂向狼檳鍾單紛杖蹽璃瀨裒襀閬緊夯柩躂俏殼魩你籲廿岸旺簸悶批蚻材新諧喂願右糶捘唅鉸植曠盞舉矩披格炸握坑喌畜徵礙筋央律拚興斬s拆歉倩羶囮型碓鍤價！蘭覓忍坉允紩河齋懍尻續影佯控贈廂期資祖層摒網繏腳遺蹺脫積孫梅廚貶滸晡妃拄挼無穿玄欠郊援檢伊模鏡靜說杯衰嬭厝廣噯沓恁咬證被增遛𤉙眨舞肩筒重亂隻練攤擛挈像左估臁兜惹町亡揍2另蹬耽譀捐鱟壽其餓舐套樠緩窯餒訣想襲浸門舊舟褫陣承磺妨糧球虹廠摧腎的餐麵干竹勸洘疫雄執職卒有涸情準灌原扶獸逆槽痱搩妹景屆環紹墊莢篦粕老哩進法腐毛趙粉\ue35c笆跛肭誓稈骨戒匏甪貌間穴含"""
    for i in s:
        if i in tlDICT:
            pass
        else:
            print(i)
    with open("TL.json", "w", encoding="utf-8") as f:
        json.dump(tlDICT, f, ensure_ascii=False)
    return None


if __name__ == "__main__":
    TL = """一,tsit
一,it
一刀兩斷,it to liong tuan
一下,tsit e
一月日,tsit gueh jit
一日到暗,tsit jit kau am
一世人,tsit si lang
一半,tsit puann
一半个仔,tsit puann e a
一半日仔,tsit puann jit a
一四界,tsit si ke
一旦,it tan
一生,it sing
一目𥍉仔,tsit bak nih a
一甲子,tsit kah tsi
一百空一,tsit pah khong it
一來,it lai
一定,it ting
一直,it tit
一律,it lut
一致,it ti
一面,tsit bin
一垺屎,tsit pu sai
一屑仔,tsit sut a
一家伙仔,tsit ke hue a
一般,it puann
一粒一,it liap it
一睏仔,tsit khun a
一概,it khai
一路,tsit loo
一寡, tsit kua
一寡仔,tsit kua a
一對時,tsit tui si
一霎仔久,tsit tiap a ku
一點仔,tsit tiam a
一礐屎,tsit hak sai
一觸久仔,tsit tak ku a
乙,it
丁,ting
七,tshit
九,kau
九,kiu
了,liau
二,ji
人,jin
人,lang
入,jip
八,pat
八,peh
刀,to
刁,tiau
力,lat
力,lik
十,tsap
十,sip
卜,poh
卜,pok
又,iu
十一哥,tsap it ko
了了,liau liau
了了, liau liau
人人,lang lang
十二分,tsap ji hun
十二生相,tsap ji senn siunn
十二指腸,sip ji tsi tng
二九暝,ji kau me
十八骰仔,sip pat tau a
十八變,tsap peh pian
七夕,tshit siah
了工,liau kang
人工,lang kang
人才,lang tsai
入土,jip thoo
刁工,thiau kang
人中,jin tiong
七孔,tshit khong
九孔,kau khang
二手,ji tshiu
入木,jip bok
八仙,pat sian
刀仔,to a
八仙桌,pat sian toh
八仙綵,pat sian tshai
刁古董,tiau koo tong
了本,liau pun
人民,jin bin
人生,jin sing
刀石,to tsioh
十全,tsap tsng
十全,sip tsuan
八字,peh ji
七字仔,tshit ji a
十字架,sip ji ke
八字跤,pat ji kha
十字路,sip ji loo
七早八早,tshit tsa peh tsa
入耳,jip ni
刀肉,to bah
七老八老,tshit lau peh lau
了尾仔囝,liau bue a kiann
二步七仔, ji poo tshit a
八角,peh kak
十足,tsap tsiok
九芎仔,kiu kiong a
人事,jin su
八卦,pat kua
卜卦,pok kua
二房,ji pang
人物,jin but
十花五色,tsap hue goo sik
入門,jip mng
人客,lang kheh
了後,liau au
七星,tshit tshenn
二指,ji tsainn
刁持,tiau ti
刁故意,tiau koo i
刀柄,to penn
八珍,pat tin
人面,lang bin
人倫,jin lun
人員,jin uan
入厝,jip tshu
七娘媽,tshit niu ma
七娘媽生,tshit niu ma senn
人家,jin ke
人家厝仔,jin ke tshu a
八家將,pat ka tsiong
人格,jin keh
人氣,jin khi
刀砧,to tiam
人馬,jin ma
入院,jip inn
人參,jin sim
人情,jin tsing
人情世事,jin tsing se su
入教,jip kau
人望,jin bong
人造,jin tso
刀喙,to tshui
入場,jip tiunn
了然,liau jian
力量,lik liong
刁意故,thiau i koo
七爺,tshit ia
刀銎,to khing
又閣,iu koh
人影,lang iann
九層塔,kau tsan thah
人範,lang pan
人緣,lang ian
入學,jip oh
入選,jip suan
了錢,liau tsinn
人頭,lang thau
力頭,lat thau
入殮,jip liam
入聲,jip siann
刁難,thiau lan
人權,jin khuan
丈,tng
三,sam
三,sann
上,tsiunn
上,tshiunn
上,siong
下,e
下,ha
下,he
低,ke
个,e
丸,uan
久,ku
么,io
乞,khit
也,ia
亡,bong
凡,huan
凡,huan
千,tshian
千,tshing
叉,tshe
口,khau
土,thoo
士,su
大,ta
大,tai
大,tua
女,li
女,lu
子,tsi
子,tsu
子,ji
寸,tshun
小,siau
小,sio
山,san
山,suann
工,kang
工,kong
己,ki
巳,tsi
巾,kin
干,kan
弓,king
才,tsai
才,tsiah
才,tshai
下𦜆,e ham
丈人,tiunn lang
三八,sam pat
土人,thoo lang
大人,tai jin
大人,tua lang
大力,tua lat
小人,siau jin
川七,tshuan tshit
工人,kang lang
丈人公,tiunn lang kong
三七仔,sam tshit a
丈人爸,tiunn lang pa
三八氣,sam pat khui
丈人媽,tiunn lang ma
上久,siong ku
上山,tsiunn suann
下山,ha san
久久,ku ku
大下,tua e
小口,sio khau
小工,sio kang
才子,tsai tsu
大丈夫,tai tiong hu
干干仔,kan kan a
三山國王,sam san kok ong
千千萬萬,tshian tshian ban ban
上山頭,tsiunn suann thau
丈公,tiunn kong
上元,siong guan
下元,ha guan
下勻,e un
大不了,tai put liau
三不五時,sam put goo si
土公仔,thoo kong a
小丑仔,siau thiu a
土公仔性,thoo kong a sing
上元暝,siong guan me
上午,siong ngoo
上天,siong thian
上手,tsiunn tshiu
上水,tshiunn tsui
下午,ha ngoo
下手,he tshiu
下手,e tshiu
下水,ha sui
土木,thoo bok
大方,tai hong
大日,tua jit
大月,tua gueh
寸尺,tshun tshioh
小心,sio sim
小月,sio gueh
小木,sio bak
工夫,kang hu
三太子,sam thai tsu
上尺工,siang tshe kong
三心兩意,sam sim liong i
大心氣,tua sim khui
千斤秤,tshian kin tshin
三文魚,sam bun hi
下水湯,ha sui thng
大爿,tua ping
丸仔,uan a
大兄,tua hiann
工仔,kang a
巾仔,kin a
弓仔,king a
大主大意,tua tsu tua i
大代誌,tua tai tsi
上加,siong ke
上北,tsiunn pak
下司,e si
土包仔,thoo pau a
小可仔,sio khua a
大四界,tua si ke
上卌袂攝,tsiunn siap be liap
下半暝,e puann me
上市,tsiunn tshi
下本,he pun
大本,tua pun
小旦,sio tuann
上目,tsiunn bak
口白,khau peh
大目,tua bak
小生,sio sing
小玉仔,sio giok a
小白菜,sio peh tshai
大甲蓆,tai kah tshioh
上任,tsiunn jim
久仰,kiu giong
干休,kan hiu
大名,tua mia
大囝,tua kiann
小名,sio mia
小囝,sio kiann
大同仔,tai tong a
上好,siong ho
也好,ia ho
土地,thoo te
土地公,thoo ti kong
下早仔,e tsai a
大耳,tua hinn
大舌,tua tsih
大伯,tua peh
大位,tua ui
工作,kang tsok
山伯英台,san phik ing tai
大妗,tua kim
山尾溜,suann bue liu
子弟,tsu te
小弟,sio ti
子弟戲,tsu te hi
三更,sann kenn
三更半暝,sann kenn puann me
口灶,khau tsau
小肚,sio too
大肚胿,tua too kui
三角,sann kak
久見,kiu kian
山谷,suann kok
川芎,tshuan kiong
川貝,tshuan pue
干貝,kan pue
千里眼,tshian li gan
三角窗,sann kak thang
三角褲,sann kak khoo
千里鏡,tshian li kiann
久來,ku lai
口供,khau king
大使,tai sai
小事,sio su
小使,siau su
工事,kang su
女兒,lu ji
小叔,sio tsik
小管仔,sio kng a
小兒科,sio ji kho
小兒麻痺,sio ji ba pi
山坪,suann phiann
丈姆,tiunn m
大姆,tua m
大姊,tua tsi
大姑,tua koo
小妹,sio mue
小姐,sio tsia
小姑,sio koo
丈姆婆,tiunn m po
下底,e te
大官,ta kuann
大官虎,tua kuann hoo
土性,thoo sing
下性命,he senn mia
大房,tua pang
大拖,tua thua
下昏,e hng
山東白仔,suann tang peh a
下昏暗,e hng am
乞的,khit e
土直,thoo tit
三肢手,sann ki tshiu
久長,ku tng
千金,tshian kim
三長兩短,sann tng nng te
上青苔,tshiunn tshenn thi
久長病,ku tng penn
千金譜,tshian kim phoo
大便,tai pian
大前年,tua tsun ni
大姨,tua i
上帝,siong te
上帝公,siong te kong
三思,sam su
大後日,tua au jit
大後年,tua au ni
山後鳥,suann au tsiau
也是,ia si
才是,tsiah si
大昨日,tua tsoh jit
大某,tua boo
山洞,suann tong
三牲,sam sing
三界公,sam kai kong
三界娘仔,sam kai niu a
山珍海味,san tin hai bi
山苳蒿,suann tang o
低音,ke im
乞食,khit tsiah
口面,khau bin
口音,khau im
乞食命,khit tsiah mia
大面神,tua bin sin
乞食琴,khit tsiah khim
乞食頭,khit tsiah thau
土匪,thoo hui
大厝,tua tshu
大哥,tua ko
低厝仔,ke tshu a
大娘姑,tua niu koo
口座,khau tso
土師,thoo sai
大孫,tua sun
大家,ta ke
子宮,tsu kiong
山崁,suann kham
大家口,tua ke khau
大家官,ta ke kuann
子時,tsu si
上桌,tsiunn toh
口氣,khau khi
大氣,tai khi
大氣,tua khui
大氣喘,tua khui tshuan
干涉,kan siap
低級,ke kip
大陣,tua tin
小鬼仔殼,siau kui a khak
三除四扣,sann tu si khau
上崎,tsiunn kia
山崙,suann lun
才情,tsai tsing
三教,sam kau
下晝,e tau
下晡,e poo
小票,sio phio
三絃,sam hian
大細,tua se
大細心,tua se sim
大細目,tua se bak
山頂,suann ting
工場,kang tiunn
大富,tua pu
大寒,tua kuann
大富大貴,tua hu tua kui
大摒掃,tua piann sau
上殕,tshiunn phu
下港,e kang
大港,tua kang
大湧,tua ing
干焦,kan na
下痟,ha siau
口琴,khau khim
工程,kang ting
工程師,kang ting su
上等,siong ting
大筒,tua tang
小等,sio tan
土菝仔,thoo puat a
上訴,siong soo
大量,tai liong
弓開,king khui
凡勢,huan se
山勢,suann se
土想,thoo siunn
下暗,e am
工會,kang hue
工業,kang giap
才會,tsiah e
山溝,suann kau
山盟海誓,san bing hai se
下落,he loh
千萬,tshian ban
大腸,tua tng
大舅,tua ku
小腸,sio tng
山腰,suann io
大腹肚,tua pak too
口試,khau tshi
下跤,e kha
土話,thoo ue
大話,tua ue
山貉,suann ho
山賊,suann tshat
山跤,suann kha
下跤手人,e kha tshiu lang
大跤胴,tua kha tang
三跤馬,sann kha be
三跤貓,sann kha niau
低路,ke loo
大路,tua loo
小路,sio loo
大道公,tai to kong
三頓,sann tng
山雺,suann bong
大鼓,tua koo
大壽,tua siu
大漢,tua han
大箍,tua khoo
大箍呆,tua khoo tai
上緊,siong kin
大腿,tua thui
大腿骨,tua thui kut
上蓋,siong kai
小說,sio suat
大銀,tua gin
小銀,sio gin
亡魂,bong hun
大餅,tua piann
三層,sam tsan
工寮,kang liau
工廠,kang tshiunn
三層肉,sam tsan bah
大廣絃,tua kong hian
小數,sio soo
干樂,kan lok
大熱,tua juah
大範,tua pan
山線,suann suann
三線路,sam suann loo
上課,siong kho
工課,khang khue
才調,tsai tiau
大賣,tua be
小賣,sio be
山豬,suann ti
下輩,e pue
三輪車,sann lian tshia
下頦,e hai
大學,tai hak
小學,sio hak
弓蕉,king tsio
弓蕉油,king tsio iu
山貓,suann niau
口頭,khau thau
山頭,suann thau
工頭,kang thau
上頭仔,siong thau a
大頭拇,tua thau bu
大頷胿,tua am kui
大頭菜,tua thau tshai
大戲,tua hi
山嶺,suann nia
土檨仔,thoo suainn a
上濟,siong tse
上聲,siong siann
大聲,tua siann
大膽,tua tann
大聲話,tua siann ue
下擺,e pai
小嬸,sio tsim
土雞仔,thoo ke a
下顎,e kok
工藝,kang ge
下願,he guan
大龐,tua phiang
大麵,tua mi
大欉,tua tsang
大廳,tua thiann
不,put
丑,thiu
中,ting
中,tiong
中,tiong
丹,tan
之,tsi
予,hoo
五,goo
五,ngoo
井,tsenn
仁,jin
仄,tseh
仆,phak
仇,siu
今,tann
允,in
內,lai
內,lue
公,kang
公,kong
六,lak
六,liok
冇,phann
冗,ling
冗,liong
凶,hiong
分,hun
分,pun
切,tshiat
勻,un
勼,kiu
勾,kau
內䘥仔,lai kah a
中人,tiong lang
允人,in lang
不才,put tsai
內山,lai suann
內才,lai tsai
分寸,hun tshun
不三不四,put sam put su
不仁,put jin
中元,tiong guan
五仁,ngoo jin
仁丹,jin tan
內公,lai kong
公元,kong guan
公分,kong pun
公分,kong hun
勻勻仔,un un a
勻勻仔火,un un a hue
五分仔車,goo hun a tshia
不中用,put tiong iong
五分車,goo hun tshia
不止,put tsi
中心,tiong sim
井水,tsenn tsui
內心,lue sim
公文,kong bun
公斤,kong kin
冇手,phann tshiu
切手,tshiat tshiu
勼手,kiu tshiu
勼水,kiu tsui
勾引,kau in
六月天,lak gueh thinn
不止仔,put tsi a
六月冬,lak gueh tang
五日節,goo jit tseh
五月節,goo gueh tseh
丑仔,thiu a
今仔,tann a
今仔日,kin a jit
勻仔是,un a si
中古,tiong koo
內外,lai gua
五加皮,ngoo ka pi
內奶,lai ling
公平,kong penn
公母,kang bo
公民,kong bin
中用,tiong iong
中立,tiong lip
丹田,tan tian
公用,kong iong
冇石仔,phann tsioh a
予伊,hoo i
介在,kai tsai
公共,kong kiong
六合,liok hap
今年,kin ni
內地,lai te
凶年,hiong ni
中旬,tiong sun
冗早,liong tsa
不死鬼,put su kui
內行,lai hang
內行的,lai hang e
不而過,put ji ko
不但,put tan
分伻,pun phenn
分別,hun piat
不孝,put hau
不求人,put kiu jin
公里,kong li
分身,hun sin
公事,kong su
中和,tiong ho
內底,lai te
公所,kong soo
不服,put hok
分明,hun bing
不法,put huat
六法全書,liok huat tsuan su
公的,kang e
分的,pun e
五金,ngoo kim
五金行,ngoo kim hang
中指,tiong tsainn
內政,lue tsing
五柳居,ngoo liu ki
中毒,tiong tok
丹毒,tan tok
冇炭,phann thuann
分派,hun phai
中秋,tiong tshiu
內科,lai kho
中秋節,tiong tshiu tseh
中秋餅,tiong tshiu piann
中計,tiong ke
內衫,lai sann
中風,tiong hong
五香,ngoo hiang
元首,guan siu
內面,lai bin
允准,in tsun
內套,lai tho
元宵,guan siau
內孫,lai sun
內容,lue iong
公家,kong ka
公家,kong ke
不時,put si
六書,liok su
元氣,guan khi
六畜,liok thiok
元神,guan sin
中脊,tiong tsit
分配,hun phue
不動產,put tong san
公婆,kong po
五彩,ngoo tshai
分張,pun tiunn
不得了,put tik liau
不得已,put tik i
內情,lue tsing
中晝,tiong tau
中晝時,tiong tau si
中晝飯,tiong tau png
中晝頓,tiong tau tng
公眾,kong tsiong
介紹,kai siau
中途,tiong too
內部,lue poo
冗剩,liong siong
內場,lai tiunn
公寓,kong gu
分散,hun suann
不敢當,put kam tong
分發,hun huat
中等,tiong ting
勾結,kau kiat
不答不七,put tap put tshit
五筋膎,goo kin ke
公費,kong hui
中間,tiong kan
公開,kong khai
公開,kong khui
分開,hun khui
中傷,tiong siong
內傷,lai siong
公債,kong tse
公園,kong hng
內媽,lai ma
公媽,kong ma
中意,ting i
仁愛,jin ai
仁慈,jin tsu
凶煞,hiong suah
不義,put gi
仁義,jin gi
內裡,lai li
勼跤,kiu kha
五路,ngoo loo
公路,kong loo
公道,kong to
不滿,put buan
五福,ngoo hok
不管時,put kuan si
內閣,lue koh
冇數,phann siau
分數,hun soo
五穀,ngoo kok
中學,tiong hak
公學校,kong hak hau
公親,kong tshin
分錢,pun tsinn
公館,kong kuan
冇蟳,phann tsim
中醫,tiong i
分類,hun lui
分鐘,hun tsing
分攤,hun thuann
五臟,ngoo tsong
化,hua
化,hua
匹,phit
升,tsin
升,sing
午,goo
午,ngoo
厄,eh
友,iu
反,huan
反,ping
壬,jim
天,thian
天,thinn
太,thai
夫,hu
少,tsio
尺,tshe
尺,tshioh
廿,jiap
引,in
心,sim
戶,hoo
手,tshiu
支,ki
文,bun
斗,tau
斤,kin
方,hng
方,hong
日,jit
月,guat
月,gueh
木,bak
木,bok
欠,khiam
止,tsi
歹,phainn
毋,m
比,pi
毛,mng
毛,moo
氏,si
水,tsui
水,sui
歹𤆬頭,phainn tshua thau
手䘼,tshiu ng
廿一,jiap it
夫人,hu jin
歹人,phainn lang
天九牌,thian kiu pai
天下,thian ha
天才,thian tsai
少女,siau li
戶口,hoo khau
手下,tshiu ha
手工,tshiu kang
日子,jit tsi
木工,bak kang
毋才,m tsiah
水土,tsui thoo
孔子公,khong tsu kong
手巾仔,tshiu kin a
戶口名,hoo khau mia
月下老人,guat ha noo jin
戶口抄本,hoo khau tshau pun
天井,thinn tsenn
天公,thinn kong
月中,gueh tiong
月內,gueh lai
水井,tsui tsenn
天公生,thinn kong senn
月內房,gueh lai pang
天公金,thinn kong kim
月內風,gueh lai hong
天公祖,thinn kong tsoo
反天,huan thinn
天文,thian bun
太太,thai thai
文化,bun hua
月日,gueh jit
歹天,phainn thinn
歹心,phainn sim
歹手爪,phainn tshiu jiau
文文仔笑,bun bun a tshio
天反地亂,thinn huan te luan
木心枋,bok sim pang
日月蚶,jit guat ham
日月蟶,jit guat than
反爿,ping ping
心火,sim hue
手爪,tshiu jiau
水牛,tsui gu
斗仔,tau a
歹代,phainn tai
水仙,tsui sian
支出,tsi tshut
月半,gueh puann
月外日,gueh gua jit
反正,huan tsing
太平,thai ping
文市,bun tshi
文旦,bun tan
水母,tsui bo
反目,huan bok
手目,tshiu bak
木瓜,bok kue
欠用,khiam ing
毋甘,m kam
水田,tsui tshan
太白星,thai pik tshenn
太白粉,thai peh hun
太白酒,thai peh tsiu
毋甘嫌,m kam hiam
反白睚,ping peh kainn
毋甘願,m kam guan
天光,thinn kng
文件,bun kiann
月光暝,gueh kng me
日光燈,jit kong ting
手印,tshiu in
方向,hong hiong
木匠,bak tshiunn
歹囝,phainn kiann
天地,thinn te
少年,siau lian
文字,bun ji
方式,hong sik
欠安,khiam an
毋好,m ho
水圳,tsui tsun
歹年冬,phainn ni tang
少年家,siau lian ke
毋好勢,m ho se
手曲,tshiu khiau
歹死,phainn si
毋成,m tsiann
毋成人,m tsiann lang
手扞仔,tshiu huann a
毋成囝,m tsiann kiann
毋成物,m tsiann mih
毋成猴,m tsiann kau
毋成樣,m tsiann iunn
天色,thinn sik
心血,sim hiat
心行,sim hing
月色,gueh sik
木耳,bok ni
欠血,khiam hueh
止血,tsi hueh
毋但,m na
毋免,m bian
夫君,hu kun
手尾,tshiu bue
月尾,gueh bue
手尾力,tshiu bue lat
毛尾仔,mng bue a
手尾錢,tshiu bue tsinn
歹扭搦,phainn liu lak
反抗,huan khong
夭折,iau tsiat
木材,bok tsai
反肚,ping too
心肝,sim kuann
手肚,tshiu too
水災,tsui tsai
心狂火著,sim kong hue toh
心肝仔囝,sim kuann a kiann
反肚痧,ping too sua
心肝窟仔,sim kuann khut a
歹育飼,phainn io tshi
心肝頭,sim kuann thau
化身,hua sin
反車,ping tshia
天良,thian liong
文言,bun gian
文身,bun sin
方言,hong gian
水車,tsui tshia
水芋仔,tsui oo a
心事,sim su
比並,pi phing
反來反去,ping lai ping khi
月來香,gueh lai hiong
月初,gueh tshe
歹命,phainn mia
毛呼,moo honn
歹命人,phainn mia lang
太妹,thai mue
夫妻,hu tshe
手底,tshiu te
文官,bun kuann
歹性地,phainn sing te
毋拄好,m tu ho
文明,bun bing
水果,tsui ko
孔明車,khong bing tshia
方法,hong huat
比武,pi bu
歹物,phainn mih
水疱,tsui pha
天狗熱,thian kau jiat
友的,iu e
太空,thai khong
歹空,phainn khang
毋知,m tsai
毋知人,m tsai lang
毋知死,m tsai si
毋知影,m tsai iann
手股,tshiu koo
木蝨,bak sat
水門,tsui mng
方便,hong pian
太保,thai po
歹剃頭,phainn thi thau
日後,jit au
手指,tshiu tsi
支持,tsi tshi
毋挃,m tih
毋是,m si
水拹仔,tsui hiap a
毋是勢,m si se
手指頭仔,tshiu tsing thau a
止枵,tsi iau
手段,tshiu tuann
水泉,tsui tsuann
反省,huan sing
月眉,gueh bai
歹看,phainn khuann
歹看相,phainn khuann siunn
反背,huan pue
水紅仔色,tsui ang a sik
巴郎,pa lang
手面,tshiu bin
方面,hong bin
歹食,phainn tsiah
手風琴,tshiu hong khim
月俸,gueh hong
毋值,m tat
毋准,m tsun
反倒轉,huan to tng
月娘,gueh niu
木屐,bak kiah
水庫,tsui khoo
反悔,huan hue
天庭,thian ting
午時,goo si
及時,kip si
天時,thian si
日時,jit si
毋捌,m bat
午時水,goo si tsui
日時仔,jit si a
及格,kip keh
反桌,ping toh
文書,bun su
月桃,geh tho
天氣,thinn khi
水氣,tsui khi
反症,huan tsing
止疼,tsi thiann
毛病,moo penn
水珠,tsui tsu
歹症頭,phainn tsing thau
天秤,thian ping
心神,sim sin
少缺,tsio khueh
手耙,tshiu pe
欠缺,khiam khueh
引起,in khi
記持,ki ti
手骨,tshiu kut
天堂,thian tong
夫婦,hu hu
反常,huan siong
日常,jit siong
心情,sim tsing
毋情願,m tsing guan
手液,tshiu sioh
水梨仔,tsui lai a
心爽,sim song
天理,thian li
心理,sim li
手痕,tshiu hun
水產,tsui san
支票,tsi phio
文章,bun tsiong
反船,ping tsun
手術,tshiu sut
毋通,m thang
水貨,tsui hue
天頂,thinn ting
孔雀,khong tshiok
木魚,bok hi
木麻黃,bok mua hong
歹喙,phainn tshui
歹喙斗,phainn tshui tau
止喙焦,tsi tshui ta
比喻,pi ju
心悶,sim bun
支援,tsi uan
毋敢,m kann
水晶,tsui tsinn
日期,jit ki
木棉,bok mi
引渡,in too
歹款,phainn khuan
毛毯,moo than
天然,thian jian
月琴,gueh khim
天窗,thinn thang
歹睏,phainn khun
巴結,pa kiat
手筆,tshiu pit
月給,gueh kip
水筆仔,tsui pit a
手碗,tshiu uann
手碗骨,tshiu uann kut
毋著,m tioh
文雅,bun nga
手勢,tshiu se
欠債,khiam tse
歹勢,phainn se
天意,thinn i
心意,sim i
歹意,phainn i
月暗暝,gueh am me
斗概,tau kai
水準,tsui tsun
水溝,tsui kau
太極拳,thai kik kun
水源頭,tsui guan thau
少爺,siau ia
月經,gueh king
反腹,ping pak
心腸,sim tng
心腹,sim pak
歹腹肚,phainn pak too
歹話,phainn ue
毛跤,mng kha
手路,tshiu loo
歹路,phainn loo
歹運,phainn un
毋過,m koh
比較,pi kau
水道,tsui to
水道水,tsui to tsui
手路菜,tshiu loo tshai
水道頭,tsui to thau
手銃,tshiu tshing
水閘,tsui tsah
水電,tsui tian
手電仔,tshiu tian a
反僥,huan hiau
止嗽,tsi sau
夭壽,iau siu
夭壽仔,iau siu a
夭壽短命,iau siu te mia
反對,huan tui
手摺簿仔,tshiu tsih phoo a
太監,thai kam
毋管,m kuan
毛管,mng kng
水管,tsui kong
水蜜桃,tsui bit tho
引誘,in iu
日誌,jit tsi
心酸,sim sng
水銀,tsui gin
歹銅舊錫,phainn tang ku siah
引魂,in hun
月餅,gueh piann
水餃,tsui kiau
少數,tsio soo
欠數,khiam siau
水槽,tsui tso
手數料,tshiu soo liau
手模,tshiu boo
手盤,tshiu puann
化緣,hua ian
比論,pi lun
心適,sim sik
化學,hua hak
文學,bun hak
手擋,tshiu tong
文憑,bun ping
天橋,thian kio
心機,sim ki
戶橂,hoo ting
手橐仔,tshiu lok a
手機仔,tshiu ki a
水燈,tsui ting
歹積德,phainn tsik tik
手錶仔,tshiu pio a
心頭,sim thau
戶頭,hoo thau
手頭,tshiu thau
日頭,jit thau
月頭,gueh thau
水頭,tsui thau
日頭花,jit thau hue
允頭路,in thau loo
水鴨,tsui ah
水龍,tsui ling
水龜,tsui ku
水龍車,tsui ling tshia
水鴛鴦,tsui uan iunn
反應,huan ing
手環,tshiu khuan
天篷,thian pong
水蕹菜,tsui ing tshai
歹聲嗽,phainn siann sau
水螺,tsui le
歹講,phainn kong
比賽,pi sai
水觳仔,tsui khok a
反輾轉,ping lian tng
水櫃,tsui kui
歹癖,phainn phiah
水薸,tsui phio
水薰吹,tsui hun tshue
水雞,tsui ke
水雞泅,tsui ke siu
水獺,tsui thuah
手藝,tshiu ge
文藝,bun ge
毛蟹,moo he
心願,sim guan
毋願,m guan
文獻,bun hian
戶籍,hoo tsik
手續,tshiu siok
手囊,tshiu long
心臟,sim tsong
斗籠,tau lang
歹聽,phainn thiann
心臟病,sim tsong penn
化驗,hua giam
毋驚,m kiann
心驚膽嚇,sim kiann tann hiannh
火,hue
爪,jiau
父,hu
爿,ping
片,phinn
牙,ga
牙,ge
牛,gu
王,ong
牛𡳞脬檨,gu lan pha suainn
火大,hue tua
火山,hue suann
爪仔,jiau a
父兄,hu hing
牛仔囝,gu a kiann
牛仔褲,gu a khoo
父母,hu bio
牛奶,gu ling
牛母,gu bo
牛奶色,gu ling sik
牛奶喙仔,gu ling tshui a
牛奶糖,gu ling thng
火石仔,hue tsioh a
王后,ong hio
火舌,hue tsih
父老,hu lo
火夾,hue ngeh
牛杙仔,gu khit a
火災,hue tsai
牛牢,gu tiau
牛肚,gu too
火車,hue tshia
牛角,gu kak
牛角花,gu kak hue
火車站,hue tshia tsam
火車路,hue tshia loo
火金蛄,hue kim koo
火屎,hue sai
牛屎色,gu sai sik
牛屎鳥仔,gu sai tsiau a
牛屎龜,gu sai ku
火星,hue tshenn
火炭,hue thuann
牛郎,gu nng
王哥柳哥,ong ko liu ko
火氣,hue khi
火烌,hue hu
牛索,gu soh
牛捽仔,gu sut a
王梨,ong lai
牛陵,gu nia
牛喙罨,gu tshui am
牛犅,gu kang
王爺,ong ia
王爺債,ong ia tse
王祿仔,ong lok a
牛腩,gu lam
火鉗,hue khinn
牛頓草,gu tun tshau
火鼠,hue tshi
火種,hue tsing
火管,hue kng
火箸,hue ti
牛種仔,gu tsing a
火腿,hue thui
牛鼻圈,gu phinn khian
牙槽,ge tso
牙槽骨,ge tso kut
火熥,hue thang
火箭,hue tsinn
牛擔,gu tann
火燒,hue sio
火燒山,hue sio suann
火燒厝,hue sio tshu
火燒埔,hue sio poo
牛螕,gu pi
牛頭,gu thau
火鍋,hue ko
火薰,hue hun
火雞,hue ke
火雞母,hue ke bo
世,se
世,si
丙,piann
主,tsu
丼,tom
乍,tsann
乎, honnh
乏,hat
仔,a
仕,su
付,hu
仙,sian
仙,sian
仝,kang
代,tai
代,te
代,tai
令,ling
以,i
兄,hiann
冊,tsheh
主人,tsu lang
仙人,sian jin
仙女,sian li
仙丹,sian tan
充公,tshiong kong
充分,tshiong hun
以及,i kip
世代,se tai
冊包,tsheh pau
主任,tsu jim
代先,tai sing
充血,tshiong hiat
兄弟,hiann ti
兄弟姊妹,hiann ti tsi mue
主見,tsu kian
主角,tsu kak
充足,tshiong tsiok
世事,se su
仙姑,sian koo
冊店,tsheh tiam
冊房,tsheh pang
仙拚仙,sian piann sian
仝爸各母,kang pe koh bu
代表,tai piau
兄長,hing tiong
世俗,se siok
以前,i tsing
世俗人,se siok lang
以後,i au
主持,tsu tshi
冊架仔,tsheh ke a
仙洞,sian tong
世界,se kai
世紀,se ki
主要,tsu iau
兄哥,hiann ko
主席,tsu sik
仙桃,sian tho
代書,tai su
仙草,sian tshau
主動,tsu tong
主婚,tsu hun
主婦,tsu hu
主張,tsu tiunn
世情,se tsing
代理,tai li
代替,tai the
仝款,kang khuan
代筆,tai pit
世間,se kan
世間人,se kan lang
兄嫂,hiann so
主意,tsu i
主義,tsu gi
且慢,tshiann ban
充滿,tshiong buan
主管,tsu kuan
代誌,tai tsi
主辦,tsu pan
代辦,tai pan
冊櫥,tsheh tu
主顧,tsu koo
主權,tsu khuan
冬,tang
凹,nah
出,tshut
刊,khan
功,kong
加,ka
加,ka
加,ke
包,pau
北,pak
半,puan
半,puann
卌,siap
占,tsiam
卡,khah
卡,khah
卯,bau
卯,bau
卯,mauh
去,khi
古,koo
句,ku
叨,lo
叩,khau
只,tsi
只,tsi
叫,kio
叮,ting
叮,ting
可,kho
台,tai
囚,siu
四,si
四,su
外,gua
央,iang
半䖙倒,puann the to
出丁,tshut ting
出入,tshut jip
出力,tshut lat
外人,gua lang
去了了,khi liau liau
出口,tshut khau
出土,tshut thoo
出山,tshut suann
加工,ke kang
半子,puan tsu
半工,puann kang
外口,gua khau
半小死,puann sio si
央三託四,iang sann thok si
司公,sai kong
外公,gua kong
半中站,puann tiong tsam
司公鈃,sai kong giang
司公壇,sai kong tuann
冬天,tang thinn
出手,tshut tshiu
出水,tshut tsui
半日,puann jit
另日,ling jit
可比,kho pi
四方,si hng
半月日,puann gueh jit
叫毋敢,kio m kann
半天筍,puan thian sun
北爿,pak ping
卡片,khah phinn
四爿,si ping
四片仔,si phinn a
出世,tshut si
包仔,pau a
半仙,puan sian
古冊,koo tsheh
半世人,puann si lang
出外,tshut gua
另外,ling gua
外外,gua gua
可可仔,khoo khoo ah
四句聯,si ku lian
司奶,sai nai
四正,si tsiann
冬瓜,tang kue
冬瓜茶,tang kue te
半生熟,puann tshenn sik
外交,gua kau
出名,tshut mia
出帆,tshut phang
只好,tsi ho
古早,koo tsa
卯死矣,bau si ah
出色,tshut sik
外行,gua hang
四色牌,su sik pai
外位,gua ui
冬尾,tang bue
出巡,tshut sun
四序,su si
四秀仔,si siu a
出身,tshut sin
加車,ka tshia
半身,puann sin
卡車,khah tshia
出來,tshut lai
北京,ak kiann
四季,su kui
可怕,kho pha
古板,koo pan
司法,su huat
加油站,ka iu tsam
出版,tshut pan
四物仔,su but a
半空中,puann khong tiong
四肢,su ki
出門,tshut mng
叫門,kio mng
半信半疑,puan sin puan gi
叫客,kio kheh
只是,tsi si
叫是,kio si
四界,si ke
四界趖,si ke so
外科,gua kho
叫苦,kio khoo
只要,tsi iau
外衫,gua sann
叩首,khio siu
四面,si bin
外面,gua bin
出風頭,tshut hong thau
加倍,ka pue
外套,gua tho
出家,tshut ke
出差,tshut tshai
出師,tshut sai
出席,tshut sik
外孫,gua sun
外家,gua ke
功效,kong hau
古書,koo tsu
出氣,tshut khui
四海,su hai
出珠,tshut tsu
四破,si phua
出租,tshut tsoo
四神湯,su sin thng
可能,kho ling
出酒,tshut tsiu
出馬,tshut ma
四配,su phue
叫做,kio tso
外國,gua kok
出張,tshut tiunn
加強,ka kiong
四常,su siong
可惜,kho sioh
半晡,puann poo
半桶屎,puann thang sai
半桶師仔,puann thang sai a
加添,ka thiam
四淋垂,si lam sui
出現,tshut hian
出產,tshut san
外痔,gua ti
出脫,tshut thuat
四通八達,su thong pat tat
北部,pak poo
半陰陽仔,puann iam iunn a
出喙,tshut tshui
功勞,kong lo
卯喙,mauh tshui
出場,tshut tiunn
包圍,pau ui
外場,gua tiunn
可惡,kho onn
可惱,kho nau
四散,si suann
加減,ke kiam
出港,tshut kang
外甥,gue sing
冬菜,tang tshai
叫菜,kio tshai
包袱巾,pau hok kin
包袱仔,pau hok a
包飯,pau png
召集,tiau tsip
出勤,tshut khin
去傷解鬱,khi siong kai ut
出嫁,tshut ke
外媽,gua ma
古意,koo i
可愛,kho ai
古意人,koo i lang
出業,tshut giap
北極,pak kik
半節,puann tsat
冬節圓,tang tseh inn
凹落去,nah loh khi
古董,koo tong
包裝,pau tsong
加話,ke ue
四跤仔,si kha a
四跤仔泅,si kha a siu
四跤杜定,si kha too ting
出路,tshut loo
出運,tshut un
半路,puann loo
外路仔,gua loo a
半路師,puann loo sai
包飼的,pau tshi e
半暝,puann me
可疑,kho gi
北管,pak kuan
半精白,puann tsiann peh
包種茶,pau tsiong te
四箍圍仔,si khoo ui a
四箍輾轉,si khoo lian tng
加網魚,ka bang hi
包裹,pau ko
包領,pau nia
凹鼻,nah phinn
出價,tshut ke
半價,puann ke
司儀,su gi
功德,kong tik
可憐,kho lian
可憐代,kho lian tai
半樓仔,puann lau a
功課,kong kho
出賣,tshut be
可靠,kho kho
加擔,ka tann
司機,su ki
半燒冷,puann sio ling
包辦,pau pan
古錐,koo tsui
出頭,tshut thau
包餡,pau ann
叩頭,khau thau
外頭,gua thau
出頭天,tshut thau thinn
出聲,tshut siann
出膿,tshut lang
加薦仔,ka tsi a
叩謝,khau sia
加講話,ke kong ue
出癖,tshut phiah
包穡頭,pau sit thau
古蹟,koo tsik
加轆仔,ka lak a
包穩,pau un
四邊,si pinn
召鏡,tiau kiann
加鵻,ka tsui
包贏,pau iann
句讀,ku tau
外觀,gua kuan
包贌,pau pak
夯,gia
失,sit
奴,loo
奶,ling
奶,nai
巧,kha
巧,khiau
市,tshi
布,poo
平,penn
平,piann
平,ping
幼,iu
戊,boo
扒,pe
扒,pe
打,tann
旦,tuann
未,bi
未,bue
本,pun
正,tsiann
正,tsing
母,bio
母,bo
母,bu
民,bin
汁,tsiap
本人,pun lang
失人禮,sit lang le
奴才,loo tsai
尻川,kha tshng
本土,pun thoo
尻川䫌,kha tshng phue
未亡人,bi bong jin
尻川口,kha tshng khau
尻川斗,kha tshng tau
尻川後,kha tshng au
尻川骨,kha tshng kut
尻川溝,kha tshng kau
市內,tshi lai
平仄,piann tseh
平分,penn pun
失手,sit tshiu
打扎,tann tsah
正手,tsiann tshiu
正月,tsiann gueh
民心,bin sim
正手爿,tsiann tshiu ping
正月正時,tsiann gueh tsiann si
正爿,tsiann ping
民主,bin tsu
母仔囝,bu a kiann
左右,tso iu
奶母,ling bu
市民,tshi bin
平平,penn penn
末末,buah buah
正本,tsiann pun
布市仔,poo tshi a
奶母車,ling bu tshia
布目,poo bak
本份,pun hun
幼囝,iu kiann
母囝椅,bu kiann i
平地,penn te
平安,ping an
本地,pun te
正式,tsing sik
失收,sit siu
本成,pun tsiann
未免,bi bian
平均,ping kin
母妗,bu kim
失志,sit tsi
打扮,tann pan
幼秀,iu siu
失言,sit gian
布身,poo sin
本身,pun sin
正身,tsiann sin
母身,bo sin
失事,sit su
未來,bi lai
本事,pun su
本來,pun lai
民事,bin su
失味,sit bi
本命錢,pun mia tsinn
尼姑,ni koo
尼姑庵,ni koo am
本底,pun te
奶帕仔,ling phe a
本性,pun sing
失明,sit bing
母的,bo e
市長,tshi tiunn
正門,tsiann mng
母金,bo kim
失信,sit sin
民俗,bin siok
夯枷,gia ke
正派,tsing phai
失約,sit iok
失重,sit tang
必要,pit iau
正面,tsiann bin
正音,tsiann im
平埔,penn poo
平埔番,enn poo huan
市容,tshi iong
布料,poo liau
母校,bu hau
失眠,sit bin
失神,sit sin
尻脊,kha tsiah
市草,tshi tshau
尻脊後,kha tsiah au
尻脊骿,kha tsiah phiann
幼骨,iu kut
打馬膠,ta ma ka
打馬膠路,ta ma ka loo
失常,sit siong
平常,ping siong
平常時,ping siong si
失敗,sit pai
打探,tann tham
失望,sit bong
打桶,tann thang
民族,bin tsok
民眾,bin tsiong
正統,tsing thong
布袋,poo te
布袋戲,poo te hi
幼貨,iu hue
正途,tsing too
失陪,sit pue
奶喙仔,ling tshui a
市場,tshi tiunn
布景,poo king
打揲,tann tiap
未曾,bue tsing
未曾未,bue tsing bue
正港,tsiann kang
必然,pit jian
平等,ping ting
本等,pun ting
正著時,tsiann tioh si
民間,bin kan
平順,ping sun
扒飯,pe png
本意,pun i
民意,bin i
失敬,sit king
失業,sit giap
正當,tsing tong
正當時,tsiann tong si
幼稚園,iu ti hng
佈置,poo ti
正經,tsing king
正義,tsing gi
母舅,bu ku
母舅公,bu ku kong
幼路,iu loo
正路,tsiann loo
失電,sit tian
正頓,tsiann tng
失算,sit sng
失誤,sit goo
永遠,ing uan
本領,pun ling
市價,tshi ke
失德,sit tik
布鞋,poo e
幼齒,iu khi
布機,poo kui
母親,bu tshin
平靜,ping tsing
本錢,pun tsinn
母錢,bu tsinn
奶頭,ling thau
布頭,poo thau
布頭布尾,poo thau poo bue
扒龍船,pe ling tsun
打擊,tann kik
民營化,bin ing hua
奶癌,ling gam
布篷,poo phang
失聲,sit siann
幼聲,iu siann
民謠,bin iau
打擾,tann jiau
失禮,sit le
失蹤,sit tsong
扒癢,pe tsiunn
失覺察,sit kak tshat
幼麵麵,iu mi mi
失戀,sit luan
母體,bu the
失體面,sit the bin
犯,huan
玉,gik
玉,giok
瓜,kue
瓦,hia
甘,kam
生,tshenn
生,senn
生,sing
用,ing
用,iong
田,tshan
由,iu
甲,kah
甲,kah
申,sin
白,peh
白,pik
皮,phi
皮,phue
目,bak
目,bok
石,tsioh
石,sik
示,si
穴,hiat
立,lip
目𥍉仔,bak nih a
犯人,huan lang
瓜子,kue tsi
甲子,kah tsi
石工,tsioh kang
白仁,peh jin
白內障,peh lai tsiang
甘心,kam sim
生日,senn jit
用心,iong sim
白木耳,peh bok ni
玉仔,gik a
瓜仔,kue a
生仔,senn a
石仔,tsioh a
瓜仔哖,kue a ni
用功,iong kong
白包,peh pau
皮包仔,phue pau a
白白,peh peh
皮皮,phi phi
生份,senn hun
生份人,senn hun lang
生囝,senn kiann
由在,iu tsai
生囡仔,senn gin a
生存,sing tsun
田庄,tshan tsng
目地,bak te
生成,senn sing
生死,senn si
白肉,peh bah
白色,peh sik
目色,bak sik
石灰,tsioh hue
生冷,tshenn ling
田佃,tshan tian
生卵,senn nng
石坎,tsioh kham
立志,lip tsi
白汫無味,peh tsiann bo bi
生狂,tshenn kong
由來,iu lai
田岸,tshan huann
白帖仔,peh thiap a
田岸路,tshan huann loo
石枋,tsioh pang
瓦杮仔,hia phue a
犯法,huan huat
目油,bak iu
石油,tsioh iu
目狗針,bak kau tsiam
目的,bok tik
目空,bak khang
生長,sing tiong
目前,bok tsian
田契,tshan khe
目屎,bak sai
目屎膏,bak sai ko
白柚,peh iu
石柱,tsioh thiau
石洞,tsioh tong
生活,sing uah
生相,senn siunn
玉皇大帝,giok hong tai te
目眉,bak bai
矛盾,mau tun
白食,peh tsiah
白韭菜,peh ku tshai
申冤,sin uan
瓦厝,hia tshu
生時日月,senn si jit gueh
立案,lip an
田租,tshan tsoo
甘草,kam tsho
甲馬,kah be
目針,bak tsiam
生做,senn tso
白帶,peh tai
皮帶,phue tua
白帶魚,peh tua hi
甘甜,kam tinn
生理,sing li
生產,sing san
生疏,tshenn soo
生理人,sing li lang
生理場,sing li tiunn
生粒仔,senn liap a
白翎鷥,peh ling si
石舂臼,tsioh tsing khu
皮蛋,phi tan
目蚶,bak ham
用途,iong too
白麻,peh mua
白麻油,peh mua iu
白喉,peh au
立場,lip tiunn
白斑,peh pan
石敢當,tsioh kam tong
生湠,senn thuann
石牌,tsioh pai
皮猴戲,phue kau hi
生番,tshenn huan
生菇,senn koo
生菜,tshenn tshai
白菜,peh tshai
犯著,huan tioh
申訴,sin soo
田蛤仔,tshan kap a
白飯,peh png
田園,tshan hng
用意,iong i
白煠,peh sah
石獅,tsioh sai
目睭,bak tsiu
目睭仁,bak tsiu jin
目睫毛,bak tsiah mng
目睭毛,bak tsiu mng
目睭皮,bak tsiu phue
石碑,tsioh pi
石碖,tsioh lun
犯罪,huan tsue
生腸,senn tng
白腹仔,peh pak a
生話,senn ue
白話,peh ue
白賊,peh tshat
白賊七仔,peh tshat tshit a
白賊話,peh tshat ue
白跤蹄,peh kha te
生路,senn loo
生鉎,senn sian
田僑仔,tshan kiau a
石榴,siah liu
白滾水,peh kun tsui
目箍,bak khoo
石膏,tsioh ko
目標,bok piau
瓦窯,hia io
皮箱,phue siunn
石碾,tsioh lian
甲箬笠,kah hah leh
皮膚,phue hu
甘蔗,kam tsia
甘蔗粕,kam tsia phoh
白蔥蔥,peh tshang tshang
申請,sin tshing
白醋,peh tshoo
皮鞋,phue e
石磨,tsioh bo
白糖,peh thng
白糖蔥,peh thng tshang
目錄,bok lok
目頭,bak thau
石頭仔,tsioh thau a
白頭鵠仔,peh thau khok a
田嬰,tshan enn
生檨仔,senn suainn a
田螺,tshan le
白講,peh kong
生鍋,senn ue
白癜,peh tio
白蟻,peh hia
目鏡,bak kiann
石鏨,tsioh tsam
目鏡仁,bak kiann jin
甘願,kam guan
白鯧,peh tshiunn
玉蘭花,giok lan hue
生鐵,senn thih
白鐵仔,peh thih a
白鶴,peh hoh
生癬,senn sian
白癬,peh sian
生驚,tshenn kiann
立體,lip the
白鑠鑠,peh siak siak
交,ka
交,kau
交,kiau
亥,hai
亦,ik
件,kiann
任,jim
份,hun
仿,hong
伊,i
伐,huah
休,hiu
伨,thin
兆,tiau
先,sian
先,sing
光,kng
光,kong
全,tsuan
交代,kau tai
仿仔雞,hong a ke
先生,sian sinn
先生娘,sian sinn niu
先生媽,sian sinn ma
兇狂,hiong kong
交往,kau ong
交易,kau ik
交易,ka iah
光明,kong bing
先知,sian ti
交流,kau liu
伙食,hue sit
光面,kng bin
休息,hiu sik
交涉,kau siap
交情,kau tsing
交接,kau tsiap
交通,kau thong
交陪,kau pue
交割,kau kuah
光復,kong hok
交插,kau tshap
交換,kau uann
光景,kong king
交替,kau the
交椅,kau i
全然,tsuan jian
交結,kau kiat
先進,sian tsin
份量,hun liong
企業,khi giap
交落,ka lauh
光榮,kong ing
交際,kau tse
先輩,sian pue
休學,hiu hak
交懍恂,ka lun sun
光頭,kng thau
份額,hun giah
交關,kau kuan
先覺,sian kak
共,ka
共,kang
共,kiong
再,tsai
冰,ping
刐,tainn
刑,hing
划,ko
列,liat
匠,tshiunn
印,in
合,hah
合,hap
合,kap
吉,kiat
吊,tiau
同,tong
名,bing
名,mia
吐,thoo
吐,thoo
向,ann
向,hiann
向,hiong
向,ng
囝,kiann
回,hue
囟,sin
因,in
在,tsai
各人,kok lang
合力,hap lik
在人,tsai lang
再三,tsai sann
吐大氣,thoo tua khui
吊大筒,tiau tua tang
吉凶,kiat hiong
吉日,kiat jit
同心,tong sim
回心轉意,hue sim tsuan i
名片,bing phinn
印仔,in a
名冊,mia tsheh
囡仔,gin a
在世,tsai se
囡仔人,gin a lang
囡仔工,gin a kang
囡仔兄,gin a hiann
囡仔囝,gin a kiann
囡仔疕,gin a phi
囡仔性,gin a sing
囡仔栽,gin a tsai
囡仔款,gin a khuan
囡仔歌,gin a kua
囡仔嬰,gin a enn
合用,hah ing
吐目,thoo bak
在生,tsai senn
吉兆,kiat tiau
吐吐,thoo thoo
向向,hiann hiann
同年,tang ni
名字,mia ji
在地,tsai te
在地人,tsai te lang
吊死,tiau si
印色,in sik
吐舌,thoo tsih
吐血,thoo hueh
吐肉箭,thoo bah tsinn
各位,kok ui
名利,bing li
同志,tong tsi
回批,hue phue
冰角,ping kak
列車,liat tshia
吊車,tiau tshia
吊車尾,tiau tshia bue
刑事,hing su
合併,hap ping
同事,tong su
在來米,tsai lai bi
印刷,in suat
囝兒,kiann ji
同姒仔,tang sai a
同居,tong ki
冰枝,ping ki
因果,in ko
合法,hap huat
再版,tsai pan
合股,hap koo
同門,tang mng
向前,hiong tsian
合奏,hap tsau
在室女,tsai sik li
危急,gui kip
因為,in ui
合約,hap iok
同胞,tong pau
合倚,hap ua
合家,hap ka
囝孫,kiann sun
在座,tsai tso
同時,tong si
向時,hiang si
合格,hap keh
吐氣,thoo khui
吊鬼仔,tiau kui a
合唱,hap tshiunn
印堂,in tong
同情,tong tsing
名望,bing bong
向望,ng bang
共產,kiong san
合理,hap li
名產,bing san
吉祥,kiat siong
划船,ko tsun
吊脰,tiau tau
在野,tsai ia
合喙,hap tshui
向善,hiong sian
名單,mia tuann
囝婿,kiann sai
合掌,hap tsiong
吉普,ji puh
吊猴,tiau kau
同窗,tong tshong
回答,hue tap
印象,in siong
吊傷,tiau siong
同意,tong i
同感,tong kam
再會,tsai hue
向腰,ann io
吐腸頭,thoo tng thau
吊鼎,tiau tiann
吊槔,tiau oo
各種,kok tsiong
合算,hap sng
因端,in tuann
刑罰,hing huat
吊膏,tiau ko
各馝,kok pih
回魂,hue hun
同齊,tang tse
吐憐涎,thoo lian sian
各樣,koh iunn
冰箱,ping siunn
同學,tong hak
危機,gui ki
吊橋,tiau kio
冰糖,ping thng
合辦,hap pan
危險,gui hiam
吊頷,tiau am
回頭,hue thau
吊癀,tiau hong
吐穗,thoo sui
名聲,mia siann
在職,tsai tsit
回覆,hue hok
合軀,hah su
名額,mia giah
在額,tsai giah
名簿,mia phoo
吊籃,tiau na
在欉黃,tsai tsang ng
印鑑,in kam
地,te
圳,tsun
多,to
奸,kan
好,ho
好,honn
如,ju
妃,hui
字,ji
存,tsun
宅,theh
守,tsiu
守,siu
安,an
寺,si
尖,tsiam
州,tsiu
帆,huan
帆,phang
年,lian
年,ni
庄,tsng
地下,te ha
安土,an thoo
年久月深,ni ku gueh tshim
地下道,te ha to
地支,te tsi
地方,te hng
好天,ho thinn
好心,ho sim
好歹,ho phainn
存心,tsun sim
安心,an sim
如夫人,ju hu jin
字爿,ji ping
地牛翻身,te gu huan sin
地主,te tsu
好兄弟,ho hiann ti
年冬,ni tang
奸巧,kan khiau
字母,ji bu
帆布,phang poo
地皮,te phue
安份,an hun
好囝,ho kiann
存在,tsun tsai
安宅,an theh
好好人,ho ho lang
好年冬,ho ni tang
好死,ho si
如此,ju tshu
存死,tshun si
如此如此,ju tshu ju tshu
奸臣,kan sin
好色,honn sik
地位,te ui
地址,te tsi
年尾,ni bue
年尾囡仔,ni bue gin a
地形,te hing
安床,an tshng
地步,te poo
好育飼,ho io tshi
安身,an sin
多事,to su
如來佛祖,ju lai put tsoo
好佳哉,ho ka tsai
字典,ji tian
好奇,honn ki
年底,ni te
好性地,ho sing te
好空,ho khang
守空房,tsiu khang pang
好客,honn kheh
年度,ni too
存後步,tshun au poo
地界,te kai
好看,ho khuann
安胎,an thai
年紀,ni ki
年限,ni han
安家,an ka
安眠,an bin
地租,te tsoo
好笑神,ho tshio sin
字紙,ji tsua
字紙籠,ji tsua lang
好酒,ho tsiu
年兜,ni tau
地動,te tang
地基,te ki
地基主,te ki tsu
好彩頭,ho tshai thau
多情,to tsing
安排,an pai
地理,te li
字眼,ji gan
地理師,te li su
奸細,kan se
帆船,phang tsun
存貨,tsun hue
好喙,ho tshui
好喙斗,ho tshui tau
尖喙夾仔,tsiam tshui ngeh a
尖喙掘仔,tsiam tshui kut a
安插,an tshah
地毯,te than
好款,ho khuan
存款,tsun khuan
好量,ho liong
奸雄,kan hiong
好勢,ho se
好意,ho i
安搭,an tah
圳溝,tsun kau
年歲,ni hue
守節,siu tsiat
年節,ni tseh
字號,ji ho
安葬,an tsong
地號名,te ho mia
奸詭,kan kui
好話,ho ue
庄跤,tsng kha
尖跤幼手,tsiam kha iu tshiu
好運,ho un
字運,ji un
字劃,ji ueh
守寡,tsiu kua
安寧,an ling
守暝,tsiu me
好漢,ho han
地獄,te gak
好鼻獅,ho phinn sai
地價,te ke
好價,ho ke
安慰,an ui
地盤,te puann
存範,tshun pan
安養,an iong
字據,ji ki
奸險,kan hiam
安靜,an tsing
地頭,te thau
年頭,ni thau
庄頭,tsng thau
好膽,ho tann
多謝,to sia
地點,te tiam
好禮,ho le
好額,ho giah
好額人,ho giah lang
安穩,an un
年關,ni kuan
安靈,an ling
尖鑽,tsiam tsng
戌,sut
成,tsiann
成,siann
成,sing
托,thuh
扛,kng
扞,huann
扣,khau
扣,khau
扦,tshuann
收,siu
早,tsa
曲,khiau
曲,khik
有,iu
有,u
朱,tsu
次,tshu
此,tshu
死,si
死,su
有一日,u tsit jit
有一無兩,u tsit bo nng
成人,tsiann lang
成人,sing jin
收入,siu jip
有力,u lat
死人,si lang
死人面,si lang bin
死人款,si lang khuan
有人緣,u lang ian
收山,siu suann
收工,siu kang
死亡,si bong
收心,siu sim
收水,siu tsui
早日,tsa jit
死心,si sim
成月日,tsiann gueh jit
成功,sing kong
收冬,siu tang
早冬,tsa tang
曲去,khiau khi
成本,sing pun
成立,sing lip
死目,si bak
成全,sing tsuan
有名,u mia
死刑,si hing
死囡仔,si gin a
死囡仔䖙,si gin a the
死囡仔脯,si gin a poo
成年,sing lian
早年,tsa ni
收成,siu sing
死肉,si bah
有耳無喙,u hinn bo tshui
死坐活食,si tse uah tsiah
收尾,siu bue
有孝,iu hau
收束,siu sok
有身,u sin
托兒所,thok ji soo
有底,u te
死忠,si tiong
死性,si sing
扣押,khau ah
死板,si pan
收泔,siu am
成物,tsiann mih
有的無的,u e bo e
有空無榫,u khang bo sun
早前,tsa tsing
收拾,siu sip
死泉,si tsuann
死活,si uah
朱紅,tsu ang
有限,iu han
有要緊,u iau kin
收音機,siu im ki
成家,sing ka
扞家,huann ke
早起時仔,tsa khi si a
有時仔,u si a
有時有陣,u si u tsun
有時陣,u si tsun
早晏,tsa uann
扣留,khau liu
收留,siu liu
曲痀,khiau ku
死症,si tsing
收租,siu tsoo
有神,u sin
早起,tsa khi
早起頓,tsa khi tng
扣除,khau tu
成做,tsiann tso
有夠,u kau
有情,u tsing
成敗,sing pai
早產,tsa san
有通,u thong
收喙,siu tshui
收場,siu tiunn
成就,sing tsiu
有款,u khuan
早睏,tsa khun
死結,si kat
死絕,si tseh
有量,u liong
有閒,u ing
收集,siu tsip
有雄,u hing
早暗,tsa am
死會,si hue
有歲,u hue
有當時仔,u tang si a
死窟仔水,si khut a tsui
死罪,si tsue
有聖,u siann
曲跤,khiau kha
收跤洗手,siu kha se tshiu
死路,si loo
有路用,u loo ing
死路旁,si loo pong
早頓,tsa tng
扞鼎灶,huann tiann tsau
託夢,thok bang
樸實,phoh sit
早慢,tsa ban
死趖,si so
有影,u iann
扞數,huann siau
收數,siu siau
扞盤,huann puann
收盤,siu puann
曲盤,khik puann
死諍,si tsenn
死豬仔價,si ti a ke
收擔,siu tann
收據,siu ki
有擋頭,u tong thau
有膭,u kui
成親,sing tshin
死賴人,si lua lang
死錢,si tsinn
有錢人,u tsinn lang
扞頭,huann thau
有頭有尾,u thau u bue
有應公,iu ing kong
收縮,siu sok
成績,sing tsik
早齋,tsa tsai
收藏,siu tsong
有額,u giah
扛轎,kng kio
收瀾,siu nua
收驚,siu kiann
汗,kuann
江,kang
池,ti
百,pah
竹,tik
米,bi
羊,iunn
老,lau
老,lau
考,kho
耳,hinn
耳,ni
聿,ut
肉,bah
肉,jiok
臣,sin
自,tsu
舌,tsih
色,sik
艾,hiann
艾,ngai
血,hiat
血,hueh
行,hang
行,hing
行,kiann
米𧉟,bi tai
竹䈄,tik ham
百二,pah ji
老人,lau lang
老人目,lau lang bak
老人斑,lau lang pan
老大,lau tua
自己,tsu ki
老大人,lau tua lang
老大公,lau tua kong
肉丸仔,bah uan a
老公仔,lau kong a
老不修,lau put siu
百日,pah jit
米斗,bi tau
羊毛,iunn mng
至少,tsi tsio
色水,sik tsui
百日紅,pah jit ang
羊毛衫,iunn mng sann
百日嗽,pah jit sau
竹仔,tik a
羊仔,iunn a
老兄,lau hiann
而且,ji tshiann
耳仔,hinn a
羊仔目,iunn a bak
竹仔枝,tik a ki
米仔麩,bi a hu
老去,lau khi
肉包,bah pau
米奶,bi ling
羊母,iunn bo
老本,lau pun
老母,lau bu
耳扒仔,hinn pe a
竹目,tik bak
老生,lau sing
耳目,ni bok
肉皮,bah phue
自由,tsu iu
自立,tsu lip
自在,tsu tsai
竹扦,tik tshuann
老早,lau tsa
米色,bi sik
肉色,bah sik
血色,hueh sik
百百空,pah pah khang
自作自受,tsu tsok tsu siu
自作孽,tsu tsok giat
自我,tsu ngoo
行李,hing li
老步定,lau poo tiann
百步蛇,pah poo tsua
自私,tsu su
肉豆,bah tau
老芋仔,lau oo a
羊角豆仔,iunn kak tau a
自來水,tsu lai tsui
考卷,kho kng
老命,lau mia
百姓,peh senn
老姑婆,lau koo po
米店,bi tiam
考官,kho kuann
自底,tsu te
肉拊,bah hu
竹披仔,tik phi a
老板,lau pan
老爸,lau pe
老的,lau e
耳空,hinn khang
色盲,sik bong
耳空重,hinn khang tang
耳空鬼仔,hinn khang kui a
耳空輕,hinn khang khin
米芳,bi phang
老阿伯,lau a peh
老阿婆,lau a po
自信,tsu sin
血型,hueh hing
耳屎,hinn sai
行後尾門,kiann au bue mng
行春,kiann tshun
行為,hing ui
行軍,hing kun
行郊,hang kau
自首,tsu siu
自修,tsu siu
老倒勼,lau to kiu
老師,lau su
肉桂,jiok kui
血氣,hueh khi
行氣,kiann khi
耳珠,hinn tsu
羊眩,iunn hin
肉砧,bah tiam
米粉,bi hun
老神在在,lau sin tsai tsai
米粉炒,bi hun tsha
竹耙,tik pe
色素,sik soo
米酒,bi tsiu
肉骨,bah kut
米酒頭仔,bi tsiu thau a
肉乾,bah kuann
自動,tsu tong
行動,hing tong
灰匙仔,hue si a
自動車,tsu tong tshia
老婆仔,lau po a
老娼頭,lau tshang thau
自強,tsu kiong
色彩,sik tshai
老康健,lau khong kian
行徙,kiann sua
行情,hang tsing
肉脯,bah poo
行船,kiann tsun
血蚶,hueh ham
肉豉仔,bah sinn a
百貨,pah hue
百貨公司,pah hue kong si
行透透,kiann thau thau
肉魚仔,bah hi a
自尊心,tsu tsun sim
竹棑,tik pai
行棋,kiann ki
江湖,kang oo
羊犅,iunn kang
老牌,lau pai
老猴,lau kau
自然,tsu jian
老牌子,lau pai tsu
老番顛,lau huan tian
老硞硞,lau khok khok
行短路,kiann te loo
竹筅,tik tshing
竹筍,tik sun
竹筒,tik tang
米粟,bi tshik
米絞,bi ka
肉絲,bah si
血筋,hueh kin
自費,tsu hui
米間,bi king
肉酥,bah soo
肉圓,bah uan
肉感,bah kam
自新,tsu sin
老歲仔,lau hue a
行經,kiann king
百萬,pah ban
竹葉,tik hioh
考試,kho tshi
竹跤,tik kha
肉跤仔,bah kha a
血路,hueh loo
行路,kiann loo
行運,kiann un
行路工,kiann loo kang
耳鉤,hinn kau
老實,lau sit
考察,kho tshat
竹箍,tik khoo
竹管,tik kong
肉粽,bah tsang
血管,hueh kng
肉粽角,bah tsang kak
肉粽節,bah tsang tseh
竹蓆,tik tshioh
肉餅,bah piann
米價,bi ke
考慮,kho li
百樣,pah iunn
米漿,bi tsiunn
米潘,bi phun
肉瘤,bah liu
灰窯,hue io
竹箬,tik hah
老練,lau lian
色緻,sik ti
竹膜,tik mooh
行踏,kiann tah
竹篙,tik ko
米篩,bi thai
米糕,bi ko
米糕𣻸,bi ko siunn
竹篙叉,tik ko tshe
米篩目,bi thai bak
米糕糜,bi ko mue
至親,tsi tshin
自頭,tsu thau
米龜,bi ku
血壓,hueh ap
耳環,hinn khuan
米糠,bi khng
竹篾仔,tik bih a
自謙,tsu khiam
米甕,bi ang
行禮,kiann le
耳甕仔,hinn ang a
米糧,bi niu
米蟲,bi thang
自轉車,tsu tsuan tshia
行醫,hing i
竹雞仔,tik ke a
肉雞仔,bah ke a
肉鯽仔,bah tsit a
肉羹,bah kenn
竹蟶,tik than
耳鏡,hinn kiann
老顛倒,lau thian thoh
米攕,bi tshiam
米籃,bi na
自覺,tsu kak
考驗,kho giam
米籮,bi lua
米粩,bi lau
百襇裙,pah king kun
衣,i
衣,ui
西,sai
西,se
西刀舌,sai to tsih
西天,se thian
西方,se hong
西爿,sai ping
西北,sai pak
西北雨,sai pak hoo
西瓜,si kue
西式,se sik
西門町,se mng ting
西洋,se iunn
西洋人,se iunn lang
西秦王爺,se tsin ong ia
西照日,sai tsio jit
西裝,se tsong
西醫,se i
西藥,se ioh
西藥房,se ioh pang
串,tshng
串,tshuan
伯,peh
估,koo
伴,phuann
伸,tshun
伸,sin
伻,phenn
佇,ti
佈,poo
位,ui
何,ho
佗,to
佗,toh
佛,hut
佛,ut
作,tsoh
作,tsok
你,li
克,khik
兌,tue
兌,tui
免,bian
兵,ping
冷,ling
佗一个,to tsit e
何乜苦,ho mi khoo
伯公,peh kong
伸勻,tshun un
伸勼,tshun kiu
伴手,phuann tshiu
伸手,tshun tshiu
佃戶,tian hoo
住戶,tsu hoo
作文,tsok bun
佛手瓜,hut tshiu kue
串仔,tshng a
佛仔,put a
兵仔,ping a
何必,ho pit
作用,tsok iong
作田,tsoh tshan
作田人,tsoh tshan lang
佛寺,hut si
佗位,to ui
冷吱吱,ling ki ki
住址,tsu tsi
作弄,tsok long
作怪,tsok kuai
住所,tsu soo
克服,khik hok
何況,ho hong
作法,tsok huat
作物,tsok but
古物商,koo but siong
作者,tsok tsia
佛門,hut mng
伸長手,tshun tng tshiu
伶俐,ling li
佇咧,ti leh
作品,tsok phin
伴奏,phuann tsau
但是,tan si
作為,tsok ui
何苦,ho khoo
作家,tsok ka
冷氣,ling khi
佛祖,ut tsoo
伴娶,phuann tshua
佛堂,hut tng
佛教,hut kau
串通,tshuan thong
伯勞仔,pit lo a
兌換,tui uann
免稅,bian sue
免費,bian hui
作亂,tsok luan
伴嫁,phuann ke
作業,tsok giap
位置,ui ti
伸跤,tshun kha
佛像,hut siong
作弊,tsok pe
估價,koo ke
免數想,bian siau siunn
作戰,tsok tsian
冷靜,ling tsing
免錢飯,bian tsinn png
克虧,khik khui
串講,tshuan kong
作穡,tsoh sit
作穡人,tsoh sit lang
作孽,tsok giat
佛龕,put kham
免驚,bian kiann
刜,phut
刣,thai
判,phuann
別,pat
別,piat
利,lai
助,tsoo
劫,kiap
卵,nng
君,kun
吞,thun
吟,gim
吠,pui
含,kam
含,kann
吭,khngh
吭,khong
吮,tshng
吱,ki
吵,tsha
吶,na
吸,khip
吹,tshue
吼,hau
別人,pat lang
努力,loo lik
別个,pat e
君子,kun tsu
卵仁,nng jin
別日,pat jit
別日仔,pat jit a
君王,kun ong
卵包,nng pau
利用,li iong
吸石,khip tsioh
刣死,thai si
別位,pat ui
吞忍,thun lun
吵抐,tsha la
判決,phuann kuat
吩咐,huan hu
判官,phuann kuann
吹狗螺,tshue kau le
利便,li pian
吹風,tshue hong
吹風機,tshue hong ki
含冤,ham uan
吵家抐宅,tsha ke la theh
吵家抐計,tsha ke la ke
利息,li sik
即時,tsik si
利益,li ik
利純,li sun
助教,tsoo kau
含梢,ham sau
卵清,nng tshing
助產士,tsoo san su
別莊,piat tsong
別款,pat khuan
別項,pat hang
別搭,pat tah
判罪,phuann tsue
吭跤翹,khong kha khiau
劫數,kiap soo
吵鬧,tsha nau
刣頭,thai thau
判斷,phuann tuan
刣雞教猴,thai ke ka kau
呃,eh
呆,tai
告,ko
囤,tun
囥,khng
囫,hut
囮,bue
坉,thun
坎,kham
坐,tse
坐,tshe
坑,khenn
夾,ngeh
坎仔,kham a
夾仔,ngeh a
坉平,thun penn
告示,ko si
坐向,tse hiong
坐位,tse ui
坎坎坷坷,kham kham khiat khiat
囥步,khng poo
呂洞賓,li tong pin
困苦,khun khoo
坑崁,khenn kham
坐桌,tse toh
坎站,kham tsam
坐清,tse tshing
告訴,ko soo
坉塗,thun thoo
囥歲,khng hue
坑溝,khenn kau
坐監,tse kann
坐數,tshe siau
坐禪,tse sian
困難,khun lan
妖,iau
妗,kim
妙,miau
妝,tsng
孝,hau
宋,song
完,uan
尪,ang
尾,bue
尿,jio
局,kiok
屁,phui
巡,sun
尾二指,bue ji tsainn
妓女,ki li
孝女,hau li
孝子,hau tsu
完工,uan kang
孝心,hau sim
尾手,bue tshiu
尿斗,jio tau
尾牙,bue ge
妗仔,kim a
尪仔,ang a
尾仔,bue a
尪仔冊,ang a tsheh
尾仔囝,bue a kiann
尪仔物,ang a mih
尪仔面,ang a bin
尪仔標,ang a phiau
尪仔頭,ang a thau
完全,uan tsuan
完成,uan sing
宋米仔,song bi a
宋江陣,song kang tin
孝呆,hau tai
孝杖,ha thng
孝男,hau lam
孝孤,hau koo
尿帕仔,jio phe a
妖怪,iau kuai
尪姨,ang i
尾後,bue au
尾指,bue tsainn
巡查,sun tsa
尪架桌,ang ke toh
宋盼的,song phan e
尿苴仔,jio tsu a
尿苴仔𩛩,jio tsu a kauh
孝衫,ha sann
局面,kiok bin
妨害,hong hai
尾胴骨,bue tang kut
妗婆,kim po
完婚,uan hun
尿桶,jio thang
尿桸,jio hia
希望,hi bang
屁窒仔,phui that a
妖術,iau sut
尿壺,jio oo
完結,uan kiat
完結篇,uan kiat phinn
尾脽,bue tsui
巡視,sun si
局勢,kiok se
孝敬,hau king
尾溜,bue liu
妥當,tho tong
妖道,iau to
尿道,jio to
妖精,iau tsiann
妖嬌,iau kiau
尾蝶,bue iah
尾幫車,bue pang tshia
尾聲,bue siann
妨礙,hong gai
妖孽,iau giat
床,tshng
床,sng
序,su
弄,lang
弟,te
弟,ti
形,hing
忌,khi
忍,jim
忍,lun
志,tsi
忘,bong
快,khuai
我,gua
我,ngoo
扭,ngiu
扭,lau
扮,pan
扯,tshe
扱,khip
扲,gim
扳,pian
扴,keh
扶,hu
扶,phoo
扷,io
扶𡳞脬,phoo lan pha
床巾,tshng kin
序大,si tua
弟子,te tsu
序大人,si tua lang
忌日,ki jit
扮仙,pan sian
床母,tshng bu
扭尻川,ngiu kha tshng
形式,hing sik
庇佑,pi iu
扶助,hu tsoo
忌床,khi tshng
快車,khuai tshia
扴味,keh bi
形狀,hing tsong
弄狗相咬,long kau sio ka
扶持,hu tshi
快活,khuinn uah
忍耐,jim nai
弄風,lang hong
形容,hing iong
扶挺,phoo thann
忍氣,lun khi
志氣,tsi khi
扮笑面,pan tshio bin
忤逆,ngoo gik
弟婦仔,te hu a
扭掠,liu liah
序細,si se
忌喙,khi tshui
弄喙花,lang tshui hue
扶插,hu tshah
形勢,hing se
扭搦,liu lak
弄新娘,lang sin niu
弄獅,lang sai
扳過來,pian kue lai
形影,hing iann
扶養,hu iong
弄龍,lang ling
志願,tsi guan
弄鐃,lang lau
批,phue
找,tsau
技,ki
抄,tshau
抉,kuat
把,pe
抌,tim
抐,la
抑,iah
抓,jiau
抔,put
投,tau
折,tsiat
折,tsih
改,kai
攻,kong
旱,han
旱,huann
旱,uann
更,kenn
杆,kuainn
杆,kuann
李,li
杏,hing
材,tsai
村,tshun
杓,siah
杙,khit
技工,ki kang
杏仁,hing jin
杏仁茶,hing jin te
杉仔,sam a
李仔,li a
杓仔,siah a
杙仔,khit a
杉仔柴,sam a tsha
李仔鹹,li a kiam
杜伯仔,too peh a
改良,kai liong
杜定,too ting
批信,phue sin
抑是,iah si
投胎,tau thai
投降,tau hang
改革,kai kik
批准,phue tsun
技師,ki su
材料,tsai liau
批紙,phue tsua
抓耙仔,jiau pe a
杜蚓仔,too kun a
改酒,kai tsiu
批桶,phue thang
投票,tau phio
改途,kai too
把握,pa ak
改換,kai uann
批殼,phue khak
杜猴,too kau
批筒,phue tang
批評,phue phing
改裝,kai tsong
投資,tau tsu
改運,kai un
抄寫,tshau sia
投標,tau pio
投稿,tau ko
投靠,tau kho
投機,tau ki
找錢,tsau tsinn
把戲,pa hi
攻擊,kong kik
折舊,tsiat ku
改薰,kai hun
杜鵑,too kuan
抗議,khong gi
批囊,phue long
抄襲,tshau sip
改變,kai pian
束,sok
步,poo
每,mui
求,kiu
汫,tsiann
汰,thai
汰,thua
沃,ak
沉,tim
沐,bak
沕,bit
沖,tshiang
沖,tshiong
沙,sua
灶,tsau
每日,mui jit
決心,kuat sim
汽水,khi tsui
沃水,ak tsui
沐手,bak tshiu
沐水,bak tsui
沖水,tshiang tsui
沖犯,tshiong huan
每年,mui ni
沒收,but siu
沙沙,sua sua
沐沐泅,bok bok siu
沖沖滾,tshiang tshiang kun
沉底,tim te
沙拉油,sa la iu
沃肥,ak pui
沃花,ak hue
沃雨,ak hoo
沙挑,sua thio
汰衫,thua sann
沉重,tim tang
沙埔,sua poo
沙屑,sua sap
求神問佛,kiu sin mng put
沙茶,sa te
沙崙,sua lun
求情,kiu tsing
束結,sok kiat
沙微,sa bui
束腰,sok io
灶跤,tsau kha
沙漠,sua bok
步數,poo soo
沙線,sua suann
步輦,poo lian
沃澹,ak tam
束縛,sok pak
灶頭,tsau thau
沙龍巴斯,sa long pa suh
災,tsai
災,tse
牢,tiau
狂,kong
男,lam
疔,ting
疕,phi
皂,tso
矣, ah
私,su
系,he
罕,han
肚,too
肚,too
肝,kan
肝,kuann
育,io
肝𦟪,kuann lian
男女,lam li
男子,lam tsu
私下,su ha
男子漢,lam tsu han
牡丹,boo tan
災厄,tsai eh
私心,su sim
疔仔,ting a
災民,tsai bin
私立,su lip
私交,su kau
育囝,io kiann
育囡仔,io gin a
育囡仔歌,io gin a kua
罕行,han kiann
私利,su li
罕見,han kian
私事,su su
私奇,sai khia
肝炎,kuann iam
災害,tsai hai
秀氣,siu khi
秀梳仔,siu se a
肚胿仔,too kuai a
罕得,han tit
私情,su tsing
系統,he thong
私通,su thong
肚脹,too tiong
肚腸,too tng
育飼,io tshi
災禍,tsai ho
肚綰,too kuann
禿頭,thut thau
肚臍,too tsai
禿額,thuh hiah
災難,tsai lan
芋,oo
見,kian
見,kinn
角,kak
言,gian
豆,tau
赤,tshiah
走,tsau
足,tsiok
身,sian
身,sin
車,tshia
辛,sin
辰,sin
那,na
邪,sia
酉,iu
里,li
阮,guan
防,hong
走山,tsau suann
良心,liong sim
車心,tshia sim
車手,tshia tshiu
赤牛,tshiah gu
芋仔,oo a
豆仔,tau a
身世,sin se
車仔,tshia a
車仔針,tshia a tsiam
車仔線,tshia a suann
豆仔薯,tau a tsi
見本,kian pun
豆奶,tau ling
豆皮,tau phue
赤目,tshiah bak
芋冰,oo ping
防守,hong siu
角色,kak sik
赤肉,tshiah bah
走色,tsau sik
走江湖,tsau kang oo
身材,sin tsai
豆沙,tau se
走私,tsau su
豆乳,tau ju
走味,tsau bi
身命,sin mia
見怪,kian kuai
豆油,tau iu
豆油膏,tau iu ko
芋泥,oo ni
走狗,tsau kau
防空壕,hong khong ho
豆花,tau hue
身屍,sin si
車後斗,tshia au tau
走相掠,tsau sio liah
走相逐,tsau sio jiok
赤砂,tshiah sua
見若,kian na
辛苦,sin khoo
見面,kinn bin
走音,tsau im
走桌的,tsau toh e
見笑,kian siau
車站,tshia tsam
見笑代,kian siau tai
見笑草,kian siau tshau
走袂開跤,tsau be khui kha
走袂離,tsau be li
走閃,tsau siam
走馬燈,tsau be ting
豆乾,tau kuann
豆乾糋,tau kuann tsinn
走唱,tsau tshiunn
車票,tshia phio
見習,kian sip
豆粕,tau phoh
芋莖,oo huainn
豆莢,tau ngeh
豆豉,tau sinn
走赦馬,tsau sia be
防備,hong pi
辛勞,sin lo
車單,tshia tuann
車掌,tshia tsiong
走揣,tsau tshue
芋稈,oo kuainn
豆菜,tau tshai
豆菜底的,tau tshai te e
走街仔仙,tsau ke a sian
言詞,gian su
角勢,kak si
走傱,tsau tsong
芋圓,oo inn
見解,kian kai
赤跤,tshiah kha
赤跤仙仔,tshiah kha sian a
走路,tsau loo
走跳,tsau thiau
角鼓,kak koo
車鼓戲,tshia koo hi
芋粿,oo kue
豆箍,tau khoo
走精,tsau tsing
芋粿曲,oo kue khiau
豆腐,tau hu
防腐劑,hong hu tse
豆腐鯊,tau hu sua
言語,gian gi
豆酺,tau poo
豆餅,tau piann
身價,sin ke
言論,gian lun
車輪,tshia lian
角齒,kak khi
車擋,tshia tong
車錢,tshia tsinn
角頭,kak thau
豆頭,tau thau
豆餡,tau ann
車頭,tshia thau
車幫,tshia pang
見擺,kian pai
身軀,sin khu
身軀邊,sin khu pinn
豆醬,tau tsiunn
豆醬湯,tau tsiunn thng
豆簽,tau tshiam
豆藤,tau tin
赤鯮,tshiah tsang
身懸,sin kuan
豆鹹,tau kiam
身體,sin the
並,ping
並,phing
乖,kuai
事,su
佬,lau
佮,kah
佮,kap
佯,tenn
使,sai
使,su
來,lai
例,le
供,king
供,king
佳人,ka jin
佯毋知,tenn m tsai
事主,su tsu
佬仔,lau a
來世,lai se
來去,lai khi
例外,le gua
乖巧,kuai kha
佯生,tenn tshenn
使用人,su iong lang
使目尾,sai bak bue
使目箭,sai bak tsinn
事件,su kiann
乳名,ju mia
使弄,sai long
來來去去,lai lai khi khi
享受,hiang siu
來往,lai ong
使性地,sai sing te
佩服,pue hok
佳哉,ka tsai
事後,su au
來洗,lai se
佳音,ka im
侍候,su hau
依倚,i ua
事務,su bu
事務所,su bu soo
事理,su li
佮喙,kah tshui
佳期,ka ki
佯痟,tenn siau
佮意,kah i
事業,su giap
來路,lai loo
亞鉛,a ian
亞鉛鉼,a ian phiann
亞鉛線,a ian suann
事實,su sit
享福,hiang hok
來賓,lai pin
來歷,lai lik
依賴,i nai
京戲,kiann hi
佯顛佯戇,tenn tian tenn gong
供體,king the
佯戇,tenn gong
侗戇,tong gong
兔,thoo
兩,liong
兩,niu
兩,nng
其,ki
具,khu
典,tian
初,tshe
初,tshoo
刮,kueh
刮,khe
到,kau
制,tse
券,kng
券,kuan
刺,tshi
刺,tshiah
刻,khik
剁,tok
匼,khap
卒,tsut
卦,kua
卷,kng
卷,kuan
卸,sia
叔,tsik
取,tshu
受,siu
刺䲅,tshi kui
初一,tshe it
初一,tshoo it
協力,hiap lik
其中,ki tiong
到今,kau tann
到分,kau hun
叔公,tsik kong
刺毛蟲,tshi moo thang
兩爿,nng ping
兔仔,thoo a
其他,ki thann
刺仔,tshi a
卒仔,tsut a
兔仔尾,thoo a bue
卸世眾,sia si tsing
刺瓜仔,tshi kue a
兩光,liong kong
協同,hiap tong
刻印仔,khik in a
到地,kau te
刺字,tshiah ji
刺竹,tshi tik
刺竹筍,tshi tik sun
到位,kau ui
叔伯兄弟,tsik peh hiann ti
叔伯姊妹,tsik peh tsi mue
叔伯的,tsik peh e
協助,hiap tsoo
初步,tshoo poo
初見面,tshoo kinn bin
初初,tshoo tshoo
到底,tau te
制定,tse ting
卷宗,kuan tsong
制服,tse hok
刺波,tshi pho
刺花,tshiah hue
制度,tse too
刺查某,tshiah tsa boo
刺疫,tshiah iah
協約,hiap iok
受苦,siu khoo
卸面皮,sia bin phue
叔孫,tsik sun
受害,siu hai
到時,kau si
受氣,siu khi
取消,tshu siau
卸祖公,sia tsoo kong
到站,kau tsam
初級,tshoo kip
刺耙耙,tshiah pe pe
受袂起,siu be khi
刺探,tshi tham
卸貨,sia hue
卸責任,sia tsik jim
卸貨底,sia hue te
到期,kau ki
受債,siu tse
協會,hiap hue
受當袂起,siu tong be khi
受罪,siu tsue
其實,ki sit
刺酸,tshiah sng
卑鄙,pi phi
取締,tshu te
協調,hiap tiau
卑賤,pi tsian
刺激,tshi kik
刺膨紗,tshiah phong se
協辦,hiap pan
典禮,tian le
刺繡,tshiah siu
協議,hiap gi
具體,ku the
刺鑿,tshi tshak
呢, nih
呢, neh
味,bi
呸,phui
呻,tshan
呼,hoo
呼,khoo
命,bing
命,mia
呾,tann
咂,tsap
和,ham
和,ho
咒,tsiu
囷,khun
坩,khann
坪,penn
坯,phue
命令,bing ling
坩仔,khann a
和平,ho ping
坦白,than pik
周全,tsiu tsuan
周至,tsiu tsi
呸血,phui hueh
周到,tsiu to
咂咂叫,tsap tsap kio
咇咇掣,phih phih tshuah
呿呿嗽,khuh khuh sau
和尚,hue siunn
固定,koo ting
坦直,than tit
呵咾,o lo
呸面,phui bin
呼音,hoo im
坦倒,than to
咖哩,ka li
咖哩嗹囉,ka li lian lo
命案,mia an
和氣,ho khi
味素,bi soo
味素粉,bi soo hun
咖啡,ka pi
咖啡色,ka pi sik
固執,koo tsip
周密,tsiu bit
坦徛,than khia
呼蛋,khoo tuann
周圍,tsiu ui
坦敧,than khi
坦敧身,than khi sin
和順,ho sun
呸痰,phui tham
和睦,ho bok
和解,ho kai
命運,mia un
咒誓,tsiu tsua
呼噎仔,khoo uh a
呼噓仔,khoo si a
咒罵,tsiu me
坦橫,than huainn
呼觱仔,khoo pi a
坦覆,than phak
命題,bing te
呸瀾,phui nua
咒讖,tsiu tsham
呼籲,hoo iok
坱,ing
坵,khu
夜,ia
奅,phann
奇,ki
奇,khia
妹,mue
妻,tshe
妾,tshiap
姆,m
姊,tse
姊,tsi
姑,koo
姓,senn
姓,sing
姑丈,koo tiunn
姑不而將,koo put ji tsiong
姊夫,tsi hu
姆仔,m a
姊仔,tsi a
夜市,ia tshi
奇巧,ki kha
姐母,tsia bo
委任,ui jim
垃圾,lah sap
垃圾鬼,lah sap kui
垃圾話,lah sap ue
奇妙,ki miau
姊妹,tsi mue
姊妹仔伴,tsi mue a phuann
奇怪,ki kuai
姑表,koo piau
姑姨,koo i
委員,ui uan
坱埃,ing ia
姑娘,koo niu
奉茶,hong te
奉送,hong sang
委託,ui thok
夜婆,ia po
姆婆,m po
姑婆,koo po
姑情,koo tsiann
妹婿,mue sai
夜景,ia king
姑換嫂,koo uann so
夜間部,ia kan poo
夜勤,ia khin
姑爺,koo ia
妻舅,tshe ku
奇數,khia soo
奇蹟,ki tsik
垃儳,la sam
季,kui
孤,koo
官,kuan
官,kuann
定,tiann
定,ting
屆,kai
屈,khut
岫,siu
岸,huann
帕,phe
帖,thiap
幸,hing
底,te
底,ti
店,tiam
孤𣮈,koo khut
孤𣮈絕種,koo khut tseh tsing
孤毛絕種,koo moo tseh tsing
底片,te phinn
帕仔,phe a
帖仔,thiap a
底代,ti tai
店主,tiam tsu
店仔,tiam a
官司,kuann si
定去,tiann khi
孤囝,koo kiann
宗旨,tsong tsi
底系,te he
孤兒,koo ji
定定,tiann tiann
定性,ting sing
定金,tiann kim
店面,tiam bin
官員,kuann uan
店員,tiam uan
底時,ti si
定案,ting an
宗祠,tsong su
定做,tiann tso
宗教,tsong kau
底細,te se
孤單,koo tuann
官場,kuann tiunn
定期,ting ki
宛然,uan jian
定著,tiann tioh
底當時,ti tang si
季節,kui tseh
定罪,ting tsue
底蒂,te ti
店號,tiam ho
官話,kuann ue
幸運,hing un
官僚,kuann liau
幸福,hing hok
定銀,tiann gin
定價,ting ke
孤獨,koo tak
孤獨,koo tok
宗親,tsong tshin
店頭,tiam thau
店頭家,tiam thau ke
官職,kuann tsit
庚,kenn
庚,king
府,hu
延,tshian
彼,he
彼,hit
往,ing
往,ong
忝,thiam
忠,tiong
念,liam
怙,koo
性,sing
怪,kuai
怪,kue
戽,hoo
彼一日,hit tsit jit
怪人,kuai lang
怪人,kuai lang
彼个,hit e
往日,ong jit
怪手,kuai tshiu
戽斗,hoo tau
戽水,hoo tsui
戽斗的,hoo tau e
彼爿,hit ping
往生,ong sing
往回的,ong hue e
往年,ong ni
性地,sing te
戽杓,hoo siah
怪事,kuai su
念咒,liam tsiu
性命,senn mia
延延,ian tshian
往往,ing ing
怐怐,khoo khoo
怦怦喘,phenn phenn tshuan
忠直,tiong tit
忠厚,tiong hoo
府城,hu siann
彼時,hit si
往時,ing si
性格,sing keh
念珠,liam tsu
彼站,hit tsam
彼陣,hit tsun
往復,ong hok
彼款,hit khuan
忽然,hut jian
彼搭,hit tah
念經,liam king
彼號,hit lo
彼跡,hit jiah
往過,ing kue
性質,sing tsit
延遲,ian ti
彼頭,hit thau
忝頭,thiam thau
彼擺,hit pai
往擺,ing pai
性癖,sing phiah
怪癖,kuai phiah
房,pang
房,pong
所,soo
承,sin
承,sing
抨,phiann
披,phi
抱,pho
抹,buah
押,ah
抽,thiu
抾,khioh
抿,bin
拂,hut
拄,tu
拆,thiah
拈,liam
拈,ni
拊,hu
拋,pha
拋,phau
拌,puann
拍,phah
拍,phik
拎,ling
拐,kuai
拐,kuainn
拑,khinn
拔,puah
拔,pueh
拖,thua
拗,au
拚,piann
招,tsiau
招,tsio
放,hong
放,pang
旺,ong
拄䢢,tu tshiang
抹刀,buah to
放刁,pang tiau
拄才,tu tsiah
放工,pang kang
放冗,pang ling
承水,sin tsui
抾水,khioh tsui
拍手,phah tshiu
拍歹,phah phainn
放手,pang tshiu
拆日仔,thiah jit a
拍毋見,phah m kinn
拍手銃,phah tshiu tshing
放水燈,pang tsui ting
放火,pang hue
所以,soo i
披仔,phi a
抿仔,bin a
拄仔好,tu a ho
拍尻川,phah kha tshng
拍石,phah tsioh
招生,tsio sing
拚生死,piann senn si
拍石師,phah tsioh sai
拚生理,piann sing li
拈田嬰,liam tshan enn
拍生驚,phah tshenn kiann
拍交落,phah ka lauh
所在,soo tsai
抾囡仔,khioh gin a
抾囝母,khioh kiann bu
招囝婿,tsio kiann sai
拄好,tu ho
拆字,thiah ji
抾字紙的,khioh ji tsua e
拍字機,phah ji ki
所有,soo iu
所有,soo u
拆扦,thiah tshuann
拚血,piann hiat
放血,pang hueh
放卵,pang nng
拍呃,phah eh
放屁,pang phui
放屁豆,pang phui tau
拐弄,kuai long
抵抗,ti khong
拍折,phah tsiat
拖沙,thua sua
拘束,khu sok
拑牢牢,khinn tiau tiau
拖身拖命,thua sin thua mia
拋捙輪,pha tshia lin
承受,sing siu
拖命,thua mia
拚命,piann mia
招呼,tsio hoo
放帖仔,pang thiap a
拍官司,phah kuann si
拚性命,piann senn mia
抵押,ti ah
拍拍,phah phik
拍拚,phah piann
放放,hong hong
拋拋走,pha pha tsau
拍抐涼,phah la liang
抱的,pho e
拆股,thiah koo
抽長,thiu tng
拍金仔,phah kim a
拋近路,pha kin loo
拚俗,piann siok
拍咳啾,phah kha tshiunn
拍咯雞,phah kok ke
房屋,pang ok
抾客,khioh kheh
放屎,pang sai
拖屎連,thua sai lian
押後,ah au
抾恨,khioh hin
招待,tsiau thai
抾拾,khioh sip
拍某菜,phah boo tshai
放毒,pang tok
拍派,phah phai
抾紅點仔,khioh ang tiam a
披衫,phi sann
放重利,pang tang lai
抹面,buah bin
拈香,liam hiunn
拆食落腹,thiah tsiah loh pak
放風聲,pang hong siann
拑家,khinn ke
拍拳,phah kun
拍拳頭,phah kun thau
抾捔,khioh kak
放捒,pang sak
抾柴,khioh tsha
抽疼,thiu thiann
拘留,khu liu
拆破,thiah phua
拍破,phah phua
抹粉,buah hun
放粉鳥,pang hun tsiau
拗紙,au tsua
招翁,tsio ang
放臭屁,pang tshau phui
拋荒,pha hng
押送,ah sang
抽退,thiu the
放送,hong sang
抾骨,khioh kut
拉圇仔燒,la lun a sio
所得,soo tik
所得稅,soo tik sue
拔桶,puah thang
拄欲,tu beh
放棄,hong khi
拍球,phah kiu
拆票,thiah phio
放符仔,pang hu a
拖累,thua lui
拍通關,phah thong kuan
拋魚,pha hi
拍麻雀,phah mua tshiok
拍喙鼓,phah tshui koo
拆單,thiah tuann
拆散,thiah suann
拖棚,thua penn
拍殕仔光,phah phu a kng
招牌,tsiau pai
拍無去,phah bo khi
抽稅,thiu sue
抾稅,khioh sue
拍結,phah kat
拒絕,ki tsuat
拍結毬,phah kat kiu
抾著,khioh tioh
拄著,tu tioh
所費,soo hui
房間,pang king
拆開,thiah khui
拚勢,piann se
招募,tsio boo
放債,pang tse
拄搪,tu tng
拍損,phah sng
招會仔,tsio hue a
放煙火,pang ian hue
拍滂泅,phah phong siu
拋碇,pha tiann
放肆,hong su
拗裒,au poo
放裒,pang poo
放榜,hong png
拚暝工,piann me kang
抱歉,pho khiam
放盡磅,pang tsin pong
拍種,phah tsing
拍算,phah sng
拍算盤,phah sng puann
拆腿,thiah thui
拋網,pha bang
承認,sing jin
招認,tsiau jin
招魂,tsiau hun
拍噗仔,phah phok a
放寬,hong khuan
拄數,tu siau
放數,pang siau
招標,tsio pio
拍賣,phah be
抽豬母稅,thiu ti bo sue
抹壁,buah piah
承擔,sing tam
拖磨,thua bua
放蕩,hong tong
拍醒,phah tshenn
拚輸贏,piann su iann
抾錢,khioh tsinn
房頭,pang thau
抽頭,thiu thau
斧頭,poo thau
斧頭櫼仔,poo thau tsinn a
放聲,pang siann
拋輾斗,pha lian tau
拍斷,phah tng
拍獵,phah lah
拍翸,phah phun
抵額,ti giah
放鬆,pang sang
拆藥仔,thiah ioh a
押韻,ah un
拐騙,kuai phian
拋麒麟,pha ki lin
拌蠓仔,puann bang a
拍觸衰,phah tshik sue
拍鐵,phah thih
拍鐵仔師,phah thih a sai
拍鐵仔褲,phah thih a khoo
拗彎,au uan
抽籤,thiu tshiam
拍鱗,phah lan
抹鹽,buah iam
拗蠻,au ban
抽鬮,thiu khau
拈鬮,liam khau
拗鬱,au ut
抾襇,khioh king
抽躼,thiu lo
昏,hun
服,hok
杮,phue
杯,pue
東,tang
東,tong
板,pan
枇,pi
枋,pang
林,lim
林,na
果,ko
枝,ki
果子,kue tsi
果子猫,kue tsi ba
果子園,kue tsi hng
朋友,ping iu
東爿,tang ping
杯仔,pue a
板仔,pan a
枋仔,pang a
明仔日,bin a jit
枝仔冰,ki a ping
明仔早起,bin a tsa khi
明仔暗,bin a am
明仔載,bin a tsai
昏去,hun khi
明白,bing pik
明年,me ni
枉死,ong si
東西南北,tang sai lam pak
林投,na tau
林投姊仔,na tau tsi a
服侍,hok sai
明呼,bing hoo
枉屈,ong khut
明明,bing bing
枇杷,pi pe
明知,bing tsai
明星,bing tshenn
東洋,tang iunn
東風,tang hong
昏倒,hun to
東倒西歪,tang to sai uai
東海,tang hai
松茸,siong jiong
昏迷,hun be
服務,hok bu
枋堵,pang too
服從,hok tsiong
松梧,siong ngoo
明理,bing li
果然,ko jian
東筊,tong kiau
林菝仔,na puat a
枉費,ong hui
易經,i̍k king
服裝,hok tsong
板膋,pan la
板嘹,pan liau
枋模,pang boo
松膠,siong ka
枕頭囊,tsim thau long
明瞭,bing liau
明講,bing kong
明顯,bing hian
武,bu
沓,tauh
沫,phueh
沬,bi
河,ho
油,iu
治,ti
沾,tsam
沿,ian
泅,siu
泏,tsuh
泏,tsuah
泏,tsuat
泔,am
法,huat
法力,huat lik
油水,iu tsui
泅水,siu tsui
法令,huat ling
武市,bu tshi
武生,bu sing
治安,ti an
油車,iu tshia
油車間,iu tshia king
法官,huat kuann
油抽,iu thiu
沓沓仔,tauh tauh a
沓沓滴滴,tap tap tih tih
油肭肭,iu leh leh
油垢,iu kau
法度,huat too
法律,huat lut
治枵,ti iau
油洗洗,iu se se
油炸粿,iu tsiah kue
法師,huat su
沿海,ian hai
治病,ti penn
油紙,iu tsua
法術,huat sut
油魚,iu hi
法場,huat tiunn
油筒仔,iu tang a
油菜,iu tshai
油飯,iu png
河溪,ho khe
油滓,iu tai
欣羨,him sian
治罪,ti tsue
沿路,ian loo
沓滴,tap tih
油漏仔,iu lau a
油蔥,iu tshang
油蔥粿,iu tshang kue
欣賞,him siong
武器,bu khi
治療,ti liau
泔糜仔,am mue a
油臊,iu tsho
法醫,huat i
武藝,bu ge
疱,pha
泡,phau
泡,pho
泡,pho
波,pho
注,tsu
注,tu
炊,tshue
炎,iam
炒,tsha
炕,khong
爬,pe
爭,tsenn
爸,pa
爸,pe
版,pan
物,but
物,mih
狀,tsng
狗,kau
狗𩸶仔,kau gam a
狀元,tsiong guan
狗公,kau kang
狗公腰,kau kang io
注文,tsu bun
炊斗,tshue tau
狗牙,kau ge
狗仔,kau a
爸母,pe bu
狗母,kau bo
狗母魚,kau bo hi
狗母鍋,kau bo ue
注目,tsu bok
物件,mih kiann
炕肉,khong bah
爸老囝幼,pe lau kiann iu
炕肉飯,khong bah png
炊床,tshue sng
狗岫,kau siu
狗空,kau khang
注音,tsu im
物食,mih tsiah
注射,tsu sia
牧師,bok su
狐狸,hoo li
狐狸精,hoo li tsiann
泡茶,phau te
物配,mih phue
物理,but li
牧場,bok tiunn
炕菜頭,khong tshai thau
注意,tsu i
炊粿,tshue kue
物價,but ke
炕窯,khong io
狗蝨,kau sat
爭論,tsing lun
狗蟻,kau hia
狗蟻碟仔,kau hia tih a
泡麵,phau mi
的, e
的,e
盲,bong
直,tit
知,tsai
知,ti
矸,kan
社,sia
祀,tshai
空,khang
空,khong
知己,ti ki
空手,khang tshiu
矸仔,kan a
空地,khang te
知死,tsai si
知位,tsai ui
知足,ti tsiok
空房,khang pang
直直,tit tit
知苦,tsai khoo
空厝間,khang tshu king
直接,tit tsiap
直透,tit thau
空喙,khang tshui
空喙哺舌,khang tshui poo tsih
空殼,khang khak
空殼支票,khang khak tsi phio
空間,khong kan
社會,sia hue
直溜溜,tit liu liu
盲腸,moo tng
空腹,khang pak
盲腸炎,moo tng iam
直腸直肚,tit tng tit too
空榫,khang sun
玫瑰花,mui kui hue
知輕重,tsai khin tang
知影,tsai iann
的確,tik khak
社頭,sia thau
空頭,khang thau
空縫,khang phang
空襲,khong sip
糾,kiu
罔,bong
羌,kiunn
者,tsia
股,koo
肢,ki
肥,pui
肯,khing
肺,hi
芟,sing
芡,khian
花,hua
花,hue
芳,phang
芳水,phang tsui
羌仔,kiunn a
花仔布,hue a poo
股本,koo pun
肨奶,hang ling
花旦,hue tuann
芳瓜,phang kue
罔行,bong kiann
肥肉,pui bah
罔育,bong io
花身仔,hue sin a
花坩,hue khann
芳味,phang bi
肯定,khing ting
股東,koo tong
花枝,hue ki
肺炎,hi iam
花矸,hue kan
芡芳,khian phang
花花仔,hue hue a
罔度,bong too
肩胛,king kah
肩胛頭,king kah thau
芥末,kai buah
花莓,hue m
芳料,phang liau
花栽,hue tsai
芳粉,phang hun
花草,hue tshau
花袂牢枝,hue be tiau ki
糾帶,kiu tua
花瓶,hue pan
股票,koo phio
芫荽,ian sui
肥軟,pui nng
糾筋,kiu kin
芥菜,kua tshai
花菜,hue tshai
罔飼,bong tshi
芡滷,khian loo
肺管,hi kng
花箍,hue khoo
花磚,hue tsng
花蕊,hue lui
花巴哩貓,hue pa li niau
肩頭,king thau
肺癆,hi lo
花環,hue khuan
花鮡,hue thiau
芥藍仔,ke na a
花轎,hue kio
花籃,hue na
花欉,hue tsang
芽,ge
虎,hoo
虯,khiu
表,piau
表,pio
軋,kauh
迎,ngia
近,kin
迒,hann
金,kim
長,tiong
長,tiunn
長,tng
門,bun
門,mng
阿,a
雨,hoo
雨,u
青,tshenn
青,tshing
長䘼,tng ng
金山,kim suann
長工,tng kang
門口,mng khau
阿丈,a tiunn
表小弟,piau sio ti
表小妹,piau sio mue
阿公,a kong
阿不倒仔,a put to a
虯毛,khiu mng
金斗,kim tau
門戶,mng hoo
門斗,mng tau
阻止,tsoo tsi
雨水,hoo tsui
雨毛仔,hoo mng a
金斗甕仔,kim tau ang a
表兄,piau hiann
金仔,kim a
阿兄,a hiann
表兄弟,piau hiann ti
金仔店,kim a tiam
門市,mng tshi
阿母,a bu
長尻川,tng kha tshng
虎皮,hoo phue
表示,piau si
金瓜,kim kue
虱目魚,sat bak hi
金囝,kim kiann
青年,tshing lian
長年菜,tng ni tshai
金色,kim sik
長老,tiunn lo
青色,tshenn sik
青竹絲,tshenn tik si
阿西,a se
雨衣,hoo i
阿伯,a peh
金含,kim kam
阿妗,a kim
長尾星,tng bue tshenn
阿沙不魯,a sa puh luh
長男,tiong lam
金言,kim gian
金身,kim sin
阿里不達,a li put tat
近來,kin lai
雨來天,hoo lai thinn
阿叔,a tsik
阿叔仔,a tsik a
長命,tng mia
表姊,piau tsi
阿姆,a m
阿姊,a tsi
阿姑,a koo
虎姑婆,hoo koo po
阿爸,a pah
表的,piau e
青盲,tshenn me
青盲牛,tshenn me gu
阿舍,a sia
阿舍囝,a sia kiann
虯虯,khiu khiu
金金,kim kim
金金看,kim kim khuann
阿姨,a i
青恂恂,tshenn sun sun
青春,tshing tshun
青紅燈,tshenn ang ting
青苔,tshenn thi
長衫,tng sann
門閂,mng tshuann
雨衫,hoo sann
表面,piau bin
門風,mng hong
青面獠牙,tshenn bin liau ge
金香燭,kim hiunn tsik
近倚,kin ua
金剛石,kim kong tsioh
阿娘,a nia
金庫,kim khoo
門扇,mng sinn
阿桑,a sang
長株形,tng tu hing
金桔仔,kim kiat a
阿爹,a tia
阿祖,a tsoo
迎神,ngia sin
金粉,kim hun
門神,mng sin
金紙,kim tsua
青耆,tshenn ki
金紙店,kim tsua tiam
青草仔店,tshenn tshau a tiam
青草仔茶,tshenn tshau a te
虎豹母,hoo pa bu
金針,kim tsiam
虎骨酒,hoo kut tsiu
金針菇,kim tsiam koo
阿啄仔,a tok a
金婚,kim hun
阿婆,a po
表情,piau tsing
迎接,ging tsiap
金條,kim tiau
表現,piau hian
門圈,mng khian
門票,mng phio
長途,tng too
金魚,kim hi
雨傘,hoo suann
雨傘節,hoo suann tsat
金棗,kim tso
長短,tng te
長短跤話,tng te kha ue
青菜,tshenn tshai
近視,kin si
門診,mng tsin
長進,tiong tsin
阿媽,a ma
阿嫂,a so
迎新棄舊,ngia sin khi ku
長歲壽,tng hue siu
金滑,kim kut
阿舅,a ku
門跤口,mng kha khau
門路,mng loo
金鼎,kim tiann
長壽,tng siu
雨幔,hoo mua
金榜,kim png
表演,piau ian
金箔,kim poh
青翠,tshenn tshui
虎鼻師,hoo phinn sai
虯儉,khiu khiam
近廟欺神,kin bio khi sin
青磅白磅,tshenn pong peh pong
金線蓮,kim suann lian
長輩,tiong pue
迎鬧熱,ngia lau jiat
阻擋,tsoo tong
迎燈,ngia ting
表親,piau tshin
近親,kin tshin
雨霎仔,hoo sap a
虎頭夾仔,hoo thau ngeh a
虎頭柑,hoo thau kam
長頷鹿,tng am lok
虎頭蜂,hoo thau phang
金龜,kim ku
金龜綠,kim ku lik
阿彌陀佛,oo mi too hut
金鍊仔,kim lian a
阿嬸,a tsim
阻礙,tsoo gai
門簾,mng li
金蠅,kim sin
金爐,kim loo
虎鬚,hoo tshiu
長躼埽,tng lo so
非,hui
非法,hui huat
亭,ting
侵,tshim
侹,thiann
便,pian
促,tshik
亭仔,ting a
亭仔跤,ting a kha
侵犯,tshim huan
便衣,pian i
便宜,pan gi
便所,pian soo
便服,pian hok
便便,pian pian
便看,pian khuann
便衫,pian sann
侮辱,bu jiok
便媒人,pian mue lang
便菜,pian tshai
便菜飯,pian tshai png
便飯,pian png
促歲壽,tshik hue siu
便當,pian tong
便當篋仔,pian tong kheh a
便藥仔,pian ioh a
俏,tshio
俗,siok
保,po
信,sin
冠,kuan
剃,thi
剉,tsho
削,siah
剋,khik
前,tsian
前,tsing
勇,iong
南,lam
卻,khiok
厘,li
前人囝,tsing lang kiann
信心,sin sim
前日,tsing jit
南爿,lam ping
前世,tsing si
保正,po tsiann
信用,sin iong
保生大帝,o sing tai te
信仰,sin giong
信任,sin jim
俗名,siok mia
前因後果,tsian in hio ko
保存,po tsun
保守,po siu
前年,tsun ni
保庇,po pi
前身,tsian sin
俗物,siok mih
前金,tsian kim
削削叫,siah siah kio
前後,tsing au
卻是,khiok si
前某,tsing boo
南洋,lam iunn
前科,tsian kho
保重,po tiong
冠軍,kuan kun
保家,po ke
信徒,sin too
剉柴,tsho tsha
勇氣,iong khi
保留,po liu
前翁,tsing ang
勇健,iong kiann
勉強,bian kiong
俗貨,siok hue
前途,tsian too
勇敢,iong kam
南極,lam kik
保溫杯,po un pue
信號,sin ho
南路鷹,lam loo ing
保管,po kuan
南管,lam kuan
俗語,siok gi
俗語話,siok gi ue
俗價,siok ke
保衛,po ue
俗賣,siok be
前輩,tsian pue
保養場,po iong tiunn
信篤,sin tau
保險,po hiam
冒險,moo hiam
剃頭,thi thau
剃頭刀,thi thau to
剃頭店,thi thau tiam
勉勵,bian le
前謝,tsing sia
前擴,tsing khok
保證,po tsing
保證人,po tsing jin
保鏢,po pio
保護,po hoo
前驛,tsing iah
厚,kau
咧, leh
咧,teh
咩,meh
咬,ka
咯,kok
咯,khak
咱,lan
咻,hiu
哀,ai
品,phin
哈,ha
哎, aih
垂,sui
厚子,kau tsi
厚工,kau kang
厚行,kau hing
咯血,khak hueh
品行,phin hing
厚尿,kau jio
哀求,ai kiu
厚沙屑,kau sua sap
厚性地,kau sing te
品明,phin bing
哀爸叫母,ai pe kio bu
垂肩,sue king
咻咻叫,hiu hiu kio
厚屎,kau sai
厚屎尿,kau sai jio
哀怨,ai uan
厚重,kau tang
厚面皮,kau bin phue
哈唏,hah hi
厚紙坯,kau tsua phue
厚酒,kau tsiu
咧欲,teh beh
咬喙,ka tshui
哈啾,hah tshiunn
咬喙齒根,ka tshui khi kin
哎喲喂,ai io ue
咯痰,khak tham
厚話,kau ue
厚話屎,kau ue sai
咳嗽,ka sau
品質,phin tsit
厚薄,kau poh
厚禮數,kau le soo
厚薰,kau hun
厚譴損,kau khian sng
城,siann
城,sing
奏,tsau
契,khe
奒,hai
奕,i
姦,kan
姨,i
姨丈,i tiunn
契兄,khe hiann
姨仔,i a
姪仔,tit a
姼仔,tshit a
姼仔詼,tshit a khue
城市,siann tshi
契母,khe bu
契囝,khe kiann
姿色,tsu sik
契爸,khe pe
姨表,i piau
威風,ui hong
威脅,ui hiap
姨婆,i po
姦情,kan tsing
城隍,sing hong
城隍廟,sing hong bio
姿勢,tsu se
姦撟,kan kiau
奏樂,tsau gak
姻緣,in ian
威嚴,ui giam
孩,hai
客,kheh
室,sik
封,hong
封,pang
屍,si
屎,sai
峇,ba
巷,hang
帝,te
度,too
客人,kheh lang
度小月,too sio gueh
客戶,kheh hoo
巷仔,hang a
宣佈,suan poo
建立,kian lip
封肉,hong bah
屎尾,sai bue
屎尿,sai jio
建材行,kian tsai hang
宣言,suan gian
幽幽仔疼,iu iu a thiann
客氣,kheh khi
封釘,hong ting
度針,too tsiam
屎桶,sai thang
屎桮齒,sai pue khi
封條,hong tiau
建設,kian siat
客鳥,kheh tsiau
封喙,hong tshui
度晬,too tse
客棧,kheh tsan
度量,too liong
幽雅,iu nga
宣傳,suan thuan
峇微,ba bui
建置,kian ti
客話,kheh ue
客運,kheh un
宣戰,suan tsian
建築,kian tiok
屎礐仔,sai hak a
屎礐仔蟲,sai hak a thang
建議,kian gi
客廳,kheh thiann
待,thai
律,lut
後,au
思,su
急,kip
怨,uan
恨,hun
恬,tiam
扁,pinn
拜,pai
括,kuah
拭,tshit
拜一,pai it
後山,au suann
拜公媽,pai kong ma
後手,au tshiu
後斗,au tau
後日,au jit
後日,au jit
後月日,au gueh jit
後代,au tai
拭仔,tshit a
後世人,au si lang
恬去,tiam khi
後出世,au tshut si
後母,au bu
拭尻川,tshit kha tshng
後母面,au bu bin
後生,hau senn
後年,au ni
拜年,pai ni
思考,su kho
拜佛,pai put
後坐,au tse
後尾,au bue
怨妒,uan too
後尾門,au bue mng
後步,au poo
扁豆,pinn tau
後來,au lai
後叔,au tsik
後岫,au siu
思念,su liam
急性,kip sing
後爸,au pe
怨恨,uan hun
恬恬,tiam tiam
拜拜,pai pai
後某,au boo
後面,au bin
扁食,pian sit
後個月,au ko gueh
拜候,pai hau
律師,lut su
後悔,hio hue
急症,kip tsing
拜託,pai thok
拜堂,pai tng
拜訪,pai hong
扁魚,pinn hi
後場,au tiunn
恢復,khue hok
後鈕,au liu
後嗣,hio su
思想,su siong
後跤,au kha
待遇,thai gu
怨嘆,uan than
思慕,su boo
怨慼,uan tsheh
怎樣,tsuann iunn
後輩,hio pue
後壁,au piah
扁擔,pun tann
恬靜,tiam tsing
後頭,au thau
後頭厝,au thau tshu
後擴,au khok
後擺,au pai
急難,kip lan
後驛,au iah
後齻,au tsan
拹,hiap
挂,kui
挃,tih
指,tsainn
指,tsi
指,ki
按,an
挌,keh
挑,thio
挓,tha
挔,hiannh
挕,hinn
挖,oo
政,tsing
故,koo
施,si
星,tshenn
星,sing
春,tshun
是,si
曷,ah
拹水,hiap tsui
春天,tshun thinn
昨日,tsoh jit
挑手爿,thio tshiu ping
挖心肝,oo sim kuann
挓火,tha hue
春牛圖,tshun gu too
春仔花,tshun a hue
指甲,tsing kah
指示,tsi si
指甲扦,tsing kah tshuann
指甲花,tsing kah hue
政見,tsing kian
故事,koo su
曷使,ah sai
按呢,an ne
政府,tsing hu
昨昏,tsa hng
政治,tsing ti
挖空,oo khang
是非,si hui
挑俍,thiau lang
政客,tsing kheh
按怎,an tsuann
按怎樣,an tsuann iunn
指指,ki tsainn
施政,si tsing
是按怎,si an tsuann
指指揬揬,ki ki tuh tuh
春風,tshun hong
指紋,tsi bun
挂紙,kui tsua
按脈,an meh
春假,tshun ka
星宿,sing siu
施捨,si sia
指教,tsi kau
挕掉,hinn tiau
指揮,tsi hui
既然,ki jian
政策,tsing tshik
曷著,ah tioh
故鄉,koo hiong
春飯,tshun png
挖塗,oo thoo
昨暗,tsa am
按照,an tsiau
春節,tshun tseh
指腹為婚,tsi pak ui hun
昨暝,tsa me
按算,an sng
故障,koo tsiong
指導,tsi to
挑戰,thiau tsian
挑選,thiau suan
指頭仔,tsing thau a
指頭拇公,tsing thau bu kong
春聯,tshun lian
指點,tsi tiam
按額,an giah
政黨,tsing tong
政權,tsing khuan
枴,kuai
枵,iau
架,ke
架,khue
枷,ke
柄,penn
某,boo
柑,kam
染,jiam
染,ni
柙,kah
柚,iu
查,tsha
柯,kua
柱,thiau
柿,khi
某人,boo lang
柳丁,liu ting
某乜人,boo mi lang
柳丁汁,liu ting tsiap
某大姊,boo tua tsi
枴仔,kuai a
架仔,ke a
柑仔,kam a
柚仔,iu a
柱仔,thiau a
柿仔,khi a
柑仔色,kam a sik
柱仔跤,thiau a kha
柑仔蜜,kam a bit
染布,ni poo
某囝,boo kiann
染色,ni sik
枸杞,koo ki
查某,tsa boo
查某𡢃,tsa boo kan
查某人,tsa boo lang
查某囝,tsa boo kiann
查某囡仔,tsa boo gin a
查某雨,tsa boo hoo
查某孫,tsa boo sun
查某祖,tsa boo tsoo
查某間,tsa boo king
查某體,tsa boo the
查埔,tsa poo
查埔人,tsa poo lang
查埔囝,tsa poo kiann
查埔囡仔,tsa poo gin a
查埔祖,tsa poo tsoo
染料,ni liau
枵鬼,iau kui
架跤,khue kha
柔道,jiu to
枵飽吵,iau pa tsha
柿粿,khi kue
柿餅,khi piann
查數,tsha siau
枵饞,iau sai
歪,uai
段,tuann
毒,tok
毒,thau
泉,tsuan
泉,tsuann
洋,iunn
洒,se
洗,se
洘,kho
洞,tong
津,tin
洩,siap
洲,tsiu
毒手,tok tshiu
泉水,tsuann tsui
洩水,siap tsui
洗石仔,se tsioh a
洘旱,kho huann
洗汰,se thua
洗身軀,se sin khu
洗身軀間,se sin khu king
洞房,tong pong
洋服,iunn hok
洗門風,se mng hong
洘流,kho lau
毒計,tok ke
洗衫,se sann
洗衫店,se sann tiam
洗衫枋,se sann pang
洗面,se bin
歪哥,uai ko
洗浴,se ik
洘秫秫,kho tsut tsut
歪斜,uai tshuah
歪喙,uai tshui
洗喙,se tshui
津貼,tin thiap
泉源,tsuan guan
洋裝,iunn tsong
歪膏揤斜,uai ko tshih tshuah
洋樓,iunn lau
洋蔥,iunn tshang
洘頭糜,kho thau mue
洗盪,se tng
洞簫,tong siau
毒藥,tok ioh
活,uah
派,phai
流,lau
流,liu
炤,tshio
炭,thuann
炮,phau
炰,pu
炱,te
炸,tsa
炸,tsuann
為,ui
為,ui
活水,uah tsui
流水,lau tsui
炮仔,phau a
炮台,phau tai
派出所,phai tshut soo
流目屎,lau bak sai
流血,lau hueh
流行,liu hing
狡怪,kau kuai
炸油,tsuann iu
炭空,thuann khang
炭屎,thuann sai
流凊汗,lau tshin kuann
流浪,liu long
活動,uah tang
活欲,uah beh
流產,liu san
流湯,lau thng
活結,uah kat
活會,uah hue
玲瑯鼓,lin long koo
活路,uah loo
活跳跳,uah thiau thiau
流鼻,lau phinn
流鼻水,lau phinn tsui
炸彈,tsa tuann
活潑,huat phuat
炭窯,thuann io
流糍,lau tsi
流豬哥瀾,lau ti ko nua
活錢,uah tsinn
派頭,phai thau
炸藥,tsa ioh
為難,ui lan
流瀾,lau nua
炭礦,thuann khong
牲醴,sing le
畏,ui
疤,pa
疥,ke
疧,khi
癸,kui
皆,kai
盆,phun
相,sann
相,sio
相,siong
相,siong
相,siunn
盹,tuh
相𫝛,sio siang
相干,siong kan
相公,siong kong
相欠債,sio khiam tse
相片,siong phinn
相仝,sio kang
盼仔,phan a
相出路,sio tshut loo
相交插,sio kau tshap
相好,siong ho
甚至,sim tsi
相刣,sio thai
相告,sio ko
相見,sio kinn
相佮,sann kap
相卸代,sio sia tai
相命,siong mia
相命仙,siong mia sian
相拄,sio tu
相拍,sio phah
相招,sio tsio
相拍電,sio phah tian
相拍雞仔,sio phah ke a
相爭,sio tsenn
相信,siong sin
相剋,sio khik
相姦,sio kan
皇帝,hong te
皇帝豆,hong te tau
相思仔,siunn si a
相約,sio iok
界限,kai han
相倚,sio ua
相借問,sio tsioh mng
相唚,sio tsim
皇宮,hong kiong
相挨相𤲍,sio e sio kheh
相捌,sio bat
相迵,sio thang
相送,sio sang
相閃身,sio siam sin
相閃車,sio siam tshia
相偃,sio ian
珍惜,tin sioh
相舂,sio tsing
相連紲,sio lian sua
畏寒,ui kuann
相尋,sio siam
相換,sio uann
相愛,siong ai
相會,siong hue
相楗,sio king
珊瑚,suan oo
相當,siong tong
盆跤骨,phun kha kut
玻璃,po le
畏熱,ui juah
盹瞌睡,tuh ka tsue
相罵,sio me
相褒歌,sio po kua
相請,sio tshiann
相諍,sio tsenn
相激,sio kik
相瞞,sio mua
相親,siong tshin
相輸,sio su
相隨,siong sui
盹龜,tuh ku
相簿,siong phoo
相辭,sio si
珍寶,tin po
相嚷,sio jiang
相觸,sio tak
相攬,sio lam
相讓,sio niu
省,sing
眉,bai
眉,bi
看,khan
看,khuann
砂,sua
砉,huah
研,ging
秋,tshiu
科,kho
秒,bio
穿,tshing
穿,tshng
省力,sing lat
看人無,khuann lang bo
省工,sing kang
看日,khuann jit
看出出,khuann tshut tshut
省立,sing lip
砂石,sua tsioh
科目,kho bok
砂石仔車,sua tsioh a tshia
看有,khuann u
看有起,khuann u khi
祈求,ki kiu
研究,gian kiu
看見,khuann kinn
省事,sing su
看命仙,khuann mia sian
科長,kho tiunn
看重,khuann tiong
看風水,khuann hong sui
秋凊,tshiu tshin
科員,kho uan
看病,khuann penn
看破,khuann phua
看衰,khuann sue
看袂起,khuann be khi
看現現,khuann hian hian
研缽,ging puah
看覓,khuann mai
穿插,tshing tshah
看款,khuann khuan
看無,khuann bo
突然,tut jian
看無起,khuann bo khi
看會起,khuann e khi
研槌,ging thui
看輕,khuann khin
研槽,ging tso
看樣,khuann iunn
科學,kho hak
省錢,sing tsinn
看頭,khuann thau
砒霜,phi sng
看醫生,khuann i sing
祈禱,ki to
秒鐘,bio tsing
看護婦,khan hoo hu
看顧,khuann koo
約,iok
紅,ang
紅,hong
缸,kng
美,bi
耍,sng
耎,luan
耐,nai
胃,ui
背,pue
胎,thai
胎,the
胘,kian
胚,phue
致,ti
美人,bi jin
胃口,ui khau
胃下垂,ui ha sui
耐心,nai sim
胛心肉,kah sim bah
紅毛塗,ang mng thoo
紅牙,ang ge
背冊,pue tsheh
紅包,ang pau
胃出血,ui tshut hueh
紅目,ang bak
耐用,nai iong
紅目墘,ang bak kinn
紅目鰱,ang bak lian
紅色,ang sik
紅肉李,ang bah li
紅尾冬,ang bue tang
紅豆仔,ang tau a
致身命,ti sin mia
致使,ti su
紅帖仔,ang thiap a
耐性,nai sing
紅柿,ang khi
背約,pue iok
紅面,ang bin
紅面鴨,ang bin ah
美容,bi iong
胃病,ui penn
致病,ti penn
胎神,thai sin
紅茶,ang te
紅記記,ang ki ki
紅酒,ang tsiu
紅莧菜,ang hing tshai
美術,bi sut
背景,pue king
紅棗,ang tso
胡椒,hoo tsio
紅絳絳,ang kong kong
紅菜,ang tshai
紅菜頭,ang tshai thau
紅塗,ang thoo
致意,ti i
約會,iok hue
紅綵,ang tshai
紅膏赤蠘,ang ko tshiah tshih
美德,bi tik
胃潰瘍,ui khui iong
致蔭,ti im
紅蔥仔頭,ang tshang a thau
紅燒,ang sio
耶穌,ia soo
紅魽,ang kam
紅龜,ang ku
紅龜粿,ang ku kue
紅嬰仔,ang enn a
胃癌,ui gam
紅糟,ang tsau
紅蟳,ang tsim
胡蠅,hoo sin
紅藥水,ang ioh tsui
胡蠅拍仔,hoo sin phah a
胡蠅虎,hoo sin hoo
胡蠅屎痣,hoo sin sai ki
胡蠅紙,hoo sin tsua
胡蠅黐,hoo sin thi
美麗,bi le
紅露酒,ang loo tsiu
紅鰱魚,ang lian hi
美觀,bi kuan
苛,kho
若,na
若,na
苦,khoo
苴,tsu
茂,om
茄,kio
虹,khing
苦力,ku li
苦工,khoo kang
苦心,khoo sim
苦毛仔,khoo mng a
苧仔,te a
茄仔色,kio a sik
茅仔草,hm a tshau
苦旦,khoo tuann
苦瓜,khoo kue
苦甘,khoo kam
若有若無,na u na bo
若是,na si
苦毒,khoo tok
苦苦,khoo khoo
茄苳,ka tang
茄茉菜,ka buah tshai
苦海,khoo hai
茉草,buah tshau
舢舨仔,sam pan a
苦茶油,khoo te iu
虼蚤,ka tsau
苦情,khoo tsing
茉莉花,bak ni hue
若無,na bo
英雄,ing hiong
苦楝仔,khoo ling a
若準,na tsun
若像,na tshiunn
苳蒿,tang o
若親像,na tshin tshiunn
苛頭,kho thau
苦勸,khoo khng
虼蚻,ka tsuah
衫,sann
訂,ting
計,ke
負,hu
赴,hu
軍,kun
迫,pik
郎,long
重,tang
重,ting
重,tiong
重,tiong
閂,tshuann
降,hang
降,kang
限,an
限,han
重大,tiong tai
重手,tang tshiu
重手頭,tang tshiu thau
衫仔弓,sann a king
衫仔裾,sann a ki
衫仔褲,sann a khoo
衫仔櫥,sann a tu
郊外,kau gua
重句,ting ku
郎君,long kun
重利,tang lai
重巡,ting sun
軍事,kun su
限制,han tse
軍法,kun huat
迫近,pik kin
重穿,tiong tshing
重要,tiong iau
重重疊疊,ting ting thah thah
訃音,hu im
重食,tiong tsiah
重倍,ting pue
迫倚,pik ua
重病,tang penn
重眠,tiong bin
重耽,ting tann
訂婚,ting hun
計智,ke ti
重敧爿,tang khi ping
計畫,ke ue
計程車,ke thing tshia
計策,ke tshik
重視,tiong si
軍隊,kun tui
重陽節,tiong iong tseh
負債,hu tse
重傷,tang siong
重新,tiong sin
降落,kang loh
計較,ke kau
軌道,kui to
計算,ke sng
要緊,iau kin
要領,iau ling
限數,an siau
負擔,hu tam
重擔,tang tann
計謀,ke boo
重錢,tiong tsinn
重頭輕,tang thau khin
重聲,tang siann
降臨,kang lim
要點,iau tiam
軍艦,kun lam
重鹹,tang kiam
面,bian
面,bin
革,kik
音,im
頁,iah
風,hong
飛,hui
飛,pue
食,tsiah
食,sit
香,hiunn
食人,tsiah lang
食力,tsiah lat
面子,bin tsu
面巾,bin kin
面水,bin tsui
風水,hong sui
風火,hong hue
香火,hiunn hue
風火頭,hong hue thau
食外口,tsiah gua khau
面布,bin poo
食奶,tsiah ling
食市,tsiah tshi
面皮,bin phue
食名,tsiah mia
面色,bin sik
食老,tsiah lau
食色,tsiah sik
飛行機,hue ling ki
風吹,hong tshue
風吹輪,hong tshue lian
風尾,hong bue
面形,bin hing
風車,hong tshia
風邪,hong sia
食命,tsiah mia
面油,bin iu
香油,hiang iu
風波,hong pho
食物,sit but
風雨,hong u
食便領現,tsiah pian nia hian
面前,bin tsing
風俗,hong siok
食品,sit phin
風度,hong too
風流,hong liu
面盆,bin phun
食穿,tsiah tshing
食苦,tsiah khoo
食食,tsiah sit
風飛沙,hong pue sua
食倯,tsiah song
面容,bin iong
食家己,tsiah ka ki
食桌,tsiah toh
香案,hiunn uann
風氣,hong khi
飛烏,pue oo
香烌,hiunn hu
食祖,tsiah tsoo
風神,hong sin
食秤頭,tsiah tshin thau
食堂,sit tng
面桶,bin thang
食晝,tsiah tau
食清領便,tsiah tshing nia pian
飛船,pue tsun
香袋仔,hiunn te a
食軟驚硬,tsiah nng kiann nge
面頂,bin ting
飛鳥,pue tsiau
風喙口,hong tshui khau
風湧,hong ing
香港跤,hiong kang kha
風琴,hong khim
風筒,hong tang
香菇,hiunn koo
香菇肉糜,hiunn koo bah mue
韭菜,ku tshai
食菜,tsiah tshai
韭菜花,ku tshai hue
風評,hong phing
食飯桌,tsiah png toh
食飯廳,tsiah png thiann
風勢,hong se
面會,bian hue
食暗,tsiah am
香煙,hiunn ian
食補,tsiah poo
食補,sit poo
風鼓,hong koo
飛鼠,pue tshi
食福,tsiah hok
面貌,bin mau
風颱,hong thai
首領,siu ling
風颱尾,hong thai bue
風颱雨,hong thai hoo
飛彈,hui tuann
面憂面結,bin iu bin kat
食漿,tsiah tsiunn
面模仔,bin boo a
面熟,bin sik
風蔥,hong tshang
音調,im tiau
食褒,tsiah po
風調雨順,hong tiau u sun
食醋,tsiah tshoo
面積,bin tsik
食膨餅,tsiah phong piann
食錢,tsiah tsinn
食錢官,tsiah tsinn kuann
風頭,hong thau
面頭前,bin thau tsing
食頭路,tsiah thau loo
風溼,hong sip
風聲,hong siann
食臊,tsiah tsho
風聲嗙影,hong siann pong iann
食虧,tsiah khui
風霜,hong song
風櫃,hong kui
食薰,tsiah hun
香爐,hiunn loo
風騷,hong so
風灌,hong kuan
修,siu
俺,an
倉,tshng
個,ko
倌,kuann
倍,pue
修正,siu tsing
修行,siu hing
修改,siu kai
修面,siu bin
倉庫,tshng khoo
修理,siu li
修補,siu poo
俱樂部,khu lok poo
修養,siu iong
修整,siu tsing
倒,to
倒,to
倖,sing
倚,ua
借,tsioh
倩,tshiann
倯,song
值,tat
值,tit
兼,kiam
冤,uan
准,tsun
凊,tshin
凍,tang
凍,tong
剔,thak
剝,pak
借人,tsioh lang
冤仇,uan siu
冤仇人,uan siu lang
倒反,to ping
倒手,to tshiu
凊心,tshin sim
倒手爿,to tshiu ping
倒爿,to ping
倒去,to khi
借用,tsioh iong
剝皮,pak phue
兼任,kiam jim
倒吊,to tiau
倒向,to hiann
倚年,ua ni
凊汗,tshin kuann
凍舌,tang tsih
倒店,to tiam
冤屈,uan khut
冤枉,uan ong
凌治,ling ti
倩的,tshiann e
倚近,ua kin
倒面,to bin
冤家,uan ke
冤家量債,uan ke niu tse
值班,tit pan
候脈,hau meh
倒退,to the
借問,tsioh mng
冥婚,bing hun
值得,tat tit
凊彩,tshin tshai
倚晝,ua tau
倫理,lun li
凍喙齒,tang tshui khi
倒貼,to thiap
凊飯,tshin png
倒剾,to khau
倒會仔,to hue a
候補,hau poo
借過,tsioh kue
倒摔向,to siang hiann
冤魂,uan hun
倒彈,to tuann
倒數,to siau
倒踏,to tah
倚靠,ua kho
倚壁,ua piah
倒擔,to tann
凌遲,ling ti
候選人,hau suan jin
借錢,tsioh tsinn
值錢,tat tsinn
倒頭,to thau
倒頭行,to thau kiann
倒頭栽,to thau tsai
凊糜,tshin mue
凍霜,tang sng
兼職,kiam tsit
倒覆,to phak
倒轉,to tng
借蹛,tsioh tua
凍露水,tang loo tsui
兼顧,kiam koo
勍,khiang
匪,hui
厝,tshu
員,uan
哥,ko
哩, lih
哩,mai
哪,na
哭,khau
哹,pu
哺,poo
哼,hainn
哼, hngh
哽,kenn
唅, hannh
唉,haih
唔,onn
唚,tsim
唐山,tng suann
原子筆,guan tsu pit
厝內,tshu lai
哪毋,na m
勍仔,khiang a
厝主,tshu tsu
原本,guan pun
哪未,na bue
厝瓦,tshu hia
原在,guan tsai
厝地,tshu te
厝宅,tshu theh
原早,guan tsa
原位,guan ui
原告,guan ko
原形,guan hing
厝角鳥仔,tshu kak tsiau a
厝角頭,tshu kak thau
哭呻,khau tshan
原底,guan te
哭爸,khau pe
哭爸哭母,khau pe khau bu
原則,guan tsik
厝契,tshu khe
哭枵,khau iau
哥哥,ko koh
哼哼叫,hainn hainn kio
唔唔睏,onn onn khun
哩哩囉囉,li li lo lo
原料,guan liau
原理,guan li
厝頂,tshu ting
唚喙,tsim tshui
厝稅,tshu sue
哪著,na tioh
哽著,kenn tioh
哪會,na e
厝跤,tshu kha
哭路頭,khau loo thau
原價,guan ke
哭調仔,khau tiau a
原諒,guan liong
原頭,guan thau
厝頭家,tshu thau ke
厝邊,tshu pinn
厝邊頭尾,tshu pinn thau bue
匪類,hui lui
唷, ioh
垺,pu
埋,bai
埋,tai
埔,poo
埕,tiann
夏,ha
套,tho
娘,nia
娘,niu
娘𡢃,niu kan
埕斗,tiann tau
娘仔,niu a
娘仔絲,niu a si
娘仔葉,niu a hioh
娘仔樹,niu a tshiu
夏令營,ha ling iann
娘仔繭,niu a kian
埔姜,poo kiunn
娘娘,niu niu
套話,tho ue
娘嬭,niu le
孫,sun
宮,king
宮,kiong
害,hai
家,ka
家,ke
容,iong
射,sia
屑,sut
展,tian
展,thian
屘,ban
島,to
崁,kham
差,tsuah
差,tsha
差,tshe
師,sai
師,su
席,sik
座,tso
庫,khoo
害了了,hai liau liau
宮女,kiong li
家己,ka ki
家己人,ka ki lang
容允,iong in
差不多,tsha put to
師父,su hu
孫仔,sun a
屘仔,ban a
師仔,sai a
師兄,su hiann
害去,hai khi
師母,su bio
家甲,ke kah
家伙,ke hue
屘囝,ban kiann
家私,ke si
家事,ka su
宵夜,siau ia
師姑,su koo
庫房,khoo pang
家長,ka tiunn
家門,ka mng
展威,tian ui
家後,ke au
展風神,tian hong sin
家婆,ke po
家教,ka kau
差教,tshe ka
崁頂,kham ting
師傅,sai hu
孫婿,sun sai
展開,thian khui
宴會,ian hue
崁跤,kham kha
師資,su tsu
崁蓋,kham kua
容貌,iong mau
庫銀,khoo gin
宮廟,king bio
射箭,sia tsinn
師範的,su huan e
差錯,tsha tsho
庫錢,khoo tsinn
崁頭崁面,kham thau kham bin
展翼,thian sit
害蟲,hai thang
差額,tsha giah
家譜,ka phoo
展寶,tian po
展覽,tian lam
弱,jiok
徒,too
恁,lin
恥,thi
恩,in
恩,un
恭,kiong
扇,sinn
拳,kun
挈,kheh
挐,ju
挨,e
挩,thuah
挨米,e bi
徒弟,too te
恐怖,khiong poo
挩枋,thuah pang
恁爸,lin pe
挩門,thuah mng
扇面,sinn bin
恁娘,lin nia
恥笑,thi tshio
恩情,un tsing
挨推,e the
挨絃仔,e hian a
恭喜,kiong hi
挩窗,thuah thang
恩愛,un ai
挨粿,e kue
挐氅氅,ju tshang tshang
拳頭,kun thau
拳頭拇,kun thau bu
拳頭師,kun thau sai
恐驚,khiong kiann
挵,long
挺,thann
挼,jue
挽,ban
挾,giap
挾,ngeh
捀,phang
捅,thong
捆,khun
捋,luah
捋,luah
捌,bat
捎,sa
捏,liap
捏,tenn
捒,sak
捗,poo
捘,tsun
捙,tshia
揤,tshih
敆,kap
效,hau
料,liau
旅,li
時,si
晃,huann
效力,hau lik
捀斗,phang tau
捀水,phang tsui
捋仔,luah a
時代,si tai
車布邊,tshia poo pinn
挽回,ban hue
捌字,bat ji
旅行,li hing
時行,si kiann
敆作,kap tsoh
捒走,sak tsau
時辰,si sin
捙拚,tshia piann
旅社,li sia
挽花,ban hue
挵門,long mng
旅客,li kheh
挽面,ban bin
時候,si hau
時時,si si
時時刻刻,si si khik khik
捙畚斗,tshia pun tau
挵破,long phua
挽脈,ban meh
挽茶,ban te
挽草,ban tshau
捀茶,phang te
時陣,si tsun
捒做堆,sak tso tui
振動,tin tang
時常,si siong
挽救,ban kiu
挵球,long kiu
效率,hau lut
敆痕,kap hun
料理,liau li
捌貨,bat hue
敆逝,kap tsua
挽喙齒,ban tshui khi
旅費,li hui
捙跋反,tshia puah ping
時間,si kan
時勢,si se
捌想,bat siunn
料想,liau siong
料想袂到,liau siong be kau
時運,si un
揤電鈴,tshih tian ling
挵鼓,long koo
挹墓粿,ip bong kue
鍤箕,tshiah ki
料算,liau sng
時價,si ke
捙盤,tshia puann
時機,si ki
捆縛,khun pak
捎錢,sa tsinn
捅頭,thong thau
旅館,li kuan
捋頭毛,luah thau mng
敆縫,kap phang
捙輾斗,tshia lian tau
敆藥仔,kap ioh a
挵鐘,long tsing
時鐘,si tsing
捏麵尪仔,liap mi ang a
晏,uann
晟,tshiann
書,tsu
書,su
朕,tim
柴,tsha
栓,sng
校,hau
栱,kong
核,hut
根,kin
格,keh
栽,tsai
桃,tho
框,khing
框,khong
案,an
桌,toh
柴㷮,tsha tsau
柴刀,tsha to
栗子,lat tsi
校工,hau kang
校友,hau iu
栓仔,sng a
格仔,keh a
桃仔,tho a
桌仔,toh a
根本,kin pun
桌布,toh poo
案件,an kiann
桂竹,kui tik
桂竹筍,kui tik sun
柴杙,tsha khit
桑材,sng tsai
根底,kin te
案底,an te
書房,tsu pang
桐油,tang iu
校舍,hau sia
桂花,kui hue
桃花,tho hue
柴門,tsha mng
校長,hau tiunn
書架仔,tsu ke a
柴屐,tsha kiah
桌崁,toh kham
柴柴,tsha tsha
柴梳,tsha se
柴砧,tsha tiam
柴耙,tsha pe
柴草,tsha tshau
核能,hik ling
晏起來,uann khi lai
栽培,tsai pue
桌屜,toh thuah
桌帷,toh ui
案情,an tsing
柴桶,tsha thang
桌頂,toh ting
柴魚,tsha hi
根節,kin tsat
桌裙,toh kun
桌跤,toh kha
校對,kau tui
柴寮,tsha liau
晟養,tshiann iong
根據,kin ki
柴頭,tsha thau
桌頭,toh thau
柴頭尪仔,tsha thau ang a
柴鍥,tsha keh
桌櫃,toh kui
書櫥,tsu tu
桔,kiat
梳,se
欱,hap
氣,khi
氣,khui
浡,phu
浮,phu
海,hai
浸,tsim
氣力,khui lat
氣口,khui khau
浪子,long tsu
海口,hai khau
海口腔,hai khau khiunn
浮冇,phu phann
海水浴場,hai tsui ik tiunn
桔仔,kiat a
桔仔汁,kiat a tsiap
桔仔餅,kiat a piann
浮石,phu tsioh
海瓜子,hai kue tsi
浮沉,phu tim
海沙埔,hai sua poo
氣身惱命,khi sin loo mia
氣味,khi bi
海味,hai bi
海和尚,hai hue siunn
海岸,hai huann
海底,hai te
氣怫怫,khi phut phut
氣氛,khi hun
海狗,hai kau
浸柿,tsim khi
海洋,hai iunn
海虼蚻,hai ka tsuah
海面,hai bin
海風,hai hong
海埔,hai poo
海島,hai to
海峽,hai kiap
海海,hai hai
海翁,hai ang
海豹,hai pa
浮動,phu tang
海參,hai sim
泰國菝仔,thai kok puat a
浮崙,phu lun
海帶,hai tua
浴桶,ik thang
海產,hai san
海產糜,hai san mue
海蛇,hai tsua
海棠,hai tong
海湧,hai ing
海菜,hai tshai
氣象,khi siong
浪費,long hui
海量,hai liong
浴間仔,ik king a
氣概,khi khai
海賊,hai tshat
氣運,khi un
海墘,hai kinn
海漲,hai tiong
海綿,hai mi
氣數,khi soo
海線,hai suann
海豬,hai ti
氣魄,khi phik
浪蕩,long tong
梳頭,se thau
海龍王,hai ling ong
氣壓,khi ap
海獺,hai thuah
海鰻,hai mua
海鱺仔,hai le a
消,siau
烈,liat
烌,hu
烏,oo
烘,hang
爹,tia
狹,eh
烏𪐞紅,oo too ang
烏㽎㽎,oo sim sim
烏人,oo lang
烏仁,oo jin
烏仁目鏡,oo jin bak kiann
消化,siau hua
消水,siau tsui
烏手,oo tshiu
烏毛,oo moo
烏心石,oo sim tsioh
烏心肝,oo sim kuann
烏天暗地,oo thinn am te
烘火,hang hue
消失,siau sit
烏市,oo tshi
烏白,oo peh
烏白來,oo peh lai
烏名單,oo mia tuann
烏有,oo iu
烏色,oo sik
烘肉,hang bah
特色,tik sik
烏耳鰻,oo hinn mua
烏西,oo se
特別,tik piat
消災解厄,siau tsai kai eh
烏豆,oo tau
消防隊,siau hong tui
消定,siau tiann
烏枋,oo pang
烏枋拭仔,oo pang tshit a
烏油,oo iu
烏狗,oo kau
烏狗兄,oo kau hiann
烏金,oo kim
烏青,oo tshenn
烏青凝血,oo tshenn ging hueh
消毒,siau tok
消風,siau hong
烏面抐桮,oo bin la pue
消息,siau sit
特效藥,tik hau ioh
烏格仔,oo keh a
特殊,tik su
烏真珠,oo tsin tsu
消除,siau tu
烏骨雞,oo kut ke
烏梅仔酒,oo mue a tsiu
烏甜仔菜,oo tinn a tshai
烏笛仔,oo tat a
烏陰,oo im
烏陰天,oo im thinn
烏魚,oo hi
烏魚子,oo hi tsi
烏麻油,oo mua iu
烏魚鰾,oo hi pio
烏喙筆仔,oo tshui pit a
烏斑,oo pan
烏棗,oo tso
狸猫,li ba
烏焦瘦,oo ta san
烏痣,oo ki
消費,siau hui
消費者,siau hui tsia
烏雲,oo hun
烏塗,oo thoo
烏暗,oo am
烏暗眩,oo am hin
消極,siau kik
消滅,siau biat
烏煙,oo ian
烏滓血,oo lai hueh
烏煙黗,oo ian thun
烏道,oo to
烏漚,oo au
烏漉肚,oo lok too
烏趖趖,oo so so
消遣,siau khian
烏墨,oo bak
烏影,oo iann
烏璇石,oo suan tsioh
消瘦落肉,siau san loh bah
烏蝛,oo bui
烏醋,oo tshoo
烏鴉,oo a
烏魯木齊,oo loo bok tse
烏鴉喙,oo a tshui
烏糖,oo thng
烏糖粿,oo thng kue
烏貓,oo niau
烏貓姊仔,oo niau tsi a
烏頭仔車,oo thau a tshia
烏龜,oo ku
烏龜,oo kui
烏龍仔,oo liong a
烏龍茶,oo liong te
烏甕串,oo ang tshng
烏鯧,oo tshiunn
烘爐,hang loo
烏鶖,oo tshiu
特權,tik khuan
狼,long
珠,tsu
班,pan
留,lau
留,liu
畜,thik
泄,tshua
疶,tshuah
疼,thiann
痀,ku
病,penn
症,tsing
病人,penn lang
畚斗,pun tau
珠仔,tsu a
畜生,thik senn
泄尿,tshua jio
病床,penn tshng
班長,pan tiunn
疶屎,tshuah sai
疼某菜,thiann boo tshai
狼毒,long tok
病相思,penn siunn si
狼狽,long pue
病疼,penn thiann
病院,penn inn
疼惜,thiann sioh
病情,penn tsing
珠淚,tsu lui
疲勞,phi lo
疼痛,thiann thang
畚箕,pun ki
疳瘡,kam tshng
珠蔥,tsu tshang
疳積,kam tsik
症頭,tsing thau
珠螺,tsu le
珠螺膎,tsu le ke
珠寶,tsu po
留戀,liu luan
病體,penn the
盍,khah
真,tsin
眠,bin
眩,hin
砧,tiam
破,pho
破,phua
祖,tsoo
眠一下,bin tsit e
祖公,tsoo kong
真心,tsin sim
祕方,pi hng
破少年,phua siau lian
真正,tsin tsiann
破布子,phua poo tsi
砧皮鞋,tiam phue e
眠床,bin tshng
眠床枋,bin tshng pang
眩車,hin tshia
真拄好,tsin tu ho
破空,phua khang
破相,phua siunn
祖厝,tsoo tshu
破柴,phua tsha
破格,phua keh
祕書,pi su
破格喙,phua keh tshui
真珠,tsin tsu
破病,phua penn
眨眨𥍉,tshap tshap nih
真情,tsin tsing
真理,tsin li
破產,pho san
眩船,hin tsun
祕結,pi kiat
破費,pho hui
破開,phua khui
破傷風,pho siong hong
祖傳祕方,tsoo thuan pi hng
祖媽,tsoo ma
破腹,phua pak
真誠,tsin tsiann
眠夢,bin bang
真實,tsin sit
祖廟,tsoo bio
破膽,phua tann
破雞筅,phua ke tshing
破壞,pho huai
祝,tsiok
神,sin
祠,su
租,tsoo
秤,tshin
秧,ng
站,tsam
笑,tshio
粉,hun
納,lap
秤仔,tshin a
秧仔,ng a
秮仔,tai a
秤仔花,tshin a hue
神主牌仔,sin tsu pai a
神去,sin khi
秫米,tsut bi
秫米飯,tsut bi png
神位,sin ui
粉肝,hun kuann
笑咍咍,tshio hai hai
神明,sin bing
站長,tsam tiunn
笑面虎,tshio bin hoo
租厝,tsoo tshu
笑容,tshio iong
神桌,sin toh
神神,sin sin
笑桮,tshio pue
粉條,hun tiau
秧船,ng tsun
粉鳥,hun tsiau
納稅,lap sue
粉筆,hun pit
祝賀,tsiok ho
粉圓,hun inn
神經,sin king
站節,tsam tsat
粉腸,hun tshiang
粉腸仔,hun tng a
笑話,tshio ue
笑詼,tshio khue
神像,sin siong
祝福,tsiok hok
粉粿,hun kue
紋銀,bun gin
神魂,sin hun
粉餅,hun piann
笑談,tshiau tam
秤頭,tshin thau
笑頭笑面,tshio thau tshio bin
秤錘,tshin thui
粉蟯,hun gio
神轎,sin kio
純,sun
紗,se
紙,tsua
級,kip
素,soo
紡,phang
索,soh
缺,khih
缺,khuat
缺,khueh
罟,koo
翁,ang
耙,pe
耙,pe
胮,hang
胸,hing
紗仔,se a
索仔,soh a
罟仔,koo a
耙仔,pe a
紗仔衫,se a sann
胳下空,koh e khang
胸坎,hing kham
胸坎骨,hing kham kut
紡車,phang tshia
缺角,khih kak
紙坯,tsua phue
紙枋,tsua pang
純金,sun kim
翁某,ang boo
耙柫,pe put
素面,soo bin
素食,soo sit
紙厝,tsua tshu
紙扇,tsua sinn
紡紗,phang se
胭脂,ian tsi
胸掛骨,hing kua kut
紙條,tsua tiau
紙票,tsua phio
紙袋仔,tsua te a
缺喙,khih tshui
翁婿,ang sai
純然,sun jian
紙牌,tsua pai
紗窗,se thang
紙篋仔,tsua kheh a
素質,soo tsit
紙橐仔,tsua lok a
紙燈,tsua ting
紙錢,tsua tsinn
缺點,khuat tiam
能,ling
胿,kui
脆,tshe
脈,meh
臭,tshau
舀,iunn
舐,tsinn
茈,tsinn
茫,bang
茫,bong
茶,te
草,tshau
草,tsho
臭人,tshau lang
草人,tshau lang
臭丸,tshau uan
茶山,te suann
舀水,iunn tsui
茶心,te sim
茶心茶,te sim te
茶心粕,te sim phoh
臭火焦,tshau hue ta
臭火燒,tshau hue sio
臭火薰,tshau hue hun
草仔,tshau a
茶仔油,te a iu
臭奶呆,tshau ling tai
茭白筍,kha peh sun
草地,tshau te
草地人,tshau te lang
臭老,tshau lau
茶米,te bi
臭汗酸,tshau kuann sng
臭耳甕仔,tshau hinn ang a
臭耳聾,tshau hinn lang
臭屁,tshau phui
臭屁仙,tshau phui sian
臭尿薟,tshau jio hiam
臭豆腐,tshau tau hu
茶店仔,te tiam a
茶杯,te pue
臭油,tshau iu
茶油,te iu
臭油垢,tshau iu kau
航空,hang khong
舀肥,iunn pui
臭腥仔,tshau tshenn a
脆柿,tshe khi
臭柿仔,tshau khi a
茯苓糕,hok ling ko
臭面,tshau bin
臭風,tshau hong
草厝仔,tshau tshu a
草埔,tshau poo
草索仔,tshau soh a
茭荖仔,ka lo a
草窒仔,tsho that a
茶莊,te tsng
草魚,tshau hi
臭喙角,tshau tshui kak
臭殕,tshau phu
臭焦,tshau ta
草猴,tshau kau
草絪,tshau in
草菇,tshau koo
茶園,te hng
臭塗味,tshau thoo bi
臭溝仔,tshau kau a
茶滓,te tai
臭煬,tshau iang
臭腥,tshau tshenn
臭腥公,tshau tshenn kong
茶葉,te hioh
臭跤液,tshau kha sioh
茶鈷,te koo
茶箍,te khoo
草蓆,tshau tshioh
草蜢公,tshau meh kong
草蜢仔,tshau meh a
臭酸,tshau sng
臭彈,tshau tuann
草寮仔,tshau liau a
茶盤,te puann
草蔬,tshau se
草蝦,tshau he
臭賤,tshau tsian
草鞋,tshau e
草橄欖,tsho kan na
茶甌,te au
臭頭,tshau thau
茶館,te kuan
臭頭雞仔,tshau thau ke a
臭臊,tshau tsho
茈薑,tsinn kiunn
臭薟薟,tshau hiam hiam
草鍥仔,tshau keh a
臭羶,tshau hian
草藥,tshau ioh
臭藥丸仔,tshau ioh uan a
草霸王,tshau pa ong
茶欉,te tsang
茶罐,te kuan
荏,lam
荒,hng
衰,sue
袂,be
衰䆀,sue bai
袂䆀,be bai
袂歹,be phainn
袂用得,be ing tit
袂合,be hah
袂收山,be siu suann
衰尾,sue bue
衰尾道人,sue bue to jin
荏身,lam sin
袂見笑,be kian siau
袂使,be sai
袂使得,be sai tit
袂和,be ho
荔枝,nai tsi
袂直,be tit
袂按算,be an sng
袂赴,be hu
袂食袂睏,be tsiah be khun
荒埔,hng poo
袂記得,be ki tit
袂得通,be tit thang
袂得過,be tit kue
袂堪得,be kham tit
袂當,be tang
衰運,sue un
荒廢,hong hui
衰潲,sue siau
袂曉,be hiau
袂輸,be su
袂輸講,be su kong
袂講得,be kong tit
袂伸捙,be tshun tshia
荏懶,lam nua
荖藤,lau tin
討,tho
記,ki
豹,pa
財,tsai
起,khi
迵,thang
迷,be
迸,piang
追,tui
退,the
送,sang
逃,to
逆,gik
起𪁎,khi tshio
財力,tsai lik
討人情,tho jin tsing
貢丸,kong uan
逃亡,to bong
逆子,gik tsu
送上山,sang tsiunn suann
財子壽,tsai tsu siu
起手,khi tshiu
起毛,khi moo
逆天,gik thinn
起毛䆀,khi moo bai
送日仔,sang jit a
起毛婸,khi moo giang
起火,khi hue
退火,the hue
財主,tsai tsu
追加,tui ka
逃犯,to huan
討皮疼,tho phue thiann
退伍,the ngoo
退休,the hiu
起因,khi in
退冰,the ping
豈有此理,khi iu tshu li
起色,khi sik
起行,khi kiann
退色,the sik
逃兵,to ping
起床,khi tshng
追求,tui kiu
退步,the poo
起狂,khi kong
追究,tui kiu
逃走,to tsau
起事,khi su
起來,khi lai
討命,tho mia
逃命,to mia
起呸面,khi phui bin
退定,the tiann
送定,sang tiann
記性,ki sing
起性地,khi sing te
財物,tsai but
記者,ki tsia
退股,the koo
訕削,suan siah
迷信,be sin
討契兄,tho khe hiann
退後,the au
財政,tsai tsing
討食,tho tsiah
起風,khi hong
起凊瘼,khi tshin mooh
起厝,khi tshu
起家,khi ke
討海,tho hai
討海人,tho hai lang
財神,tsai sin
送神,sang sin
財神爺,tsai sin ia
退酒,the tsiu
退婚,the hun
財產,tsai san
起無空,khi bo khang
起痟,khi siau
起程,khi thing
起童,khi tang
退童,the tang
起訴,khi soo
討趁,tho than
起雄,khi hiong
討債,tho tse
迷亂,be luan
討債囝,tho tse kiann
送嫁,sang ke
財源,tsai guan
起碇,khi tiann
起落,khi loh
記號,ki ho
起跤動手,khi kha tang tshiu
迵過,thang kue
起鼓,khi koo
討厭,tho ia
財團,tsai thuan
追認,tui jin
起價,khi ke
討數,tho siau
記數,ki siau
訕潲,suan siau
退熱,the jiat
起碼,khi ma
討論,tho lun
退學,the hak
記憶,ki ik
討錢,tho tsinn
起頭,khi thau
退癀,the hong
逃避,to pi
送禮,sang le
起雞母皮,khi ke bo phue
起藥蛆,khi ioh tshi
財寶,tsai po
貢獻,kong hian
迷戀,be luan
配,phue
酒,tsiu
釘,ting
針,tsiam
閃,siam
院,inn
陣,tsun
陣,tin
除,ti
除,tu
隻,tsiah
飢,ki
馬,be
馬,ma
骨,kut
高,ko
鬥,tau
鬼,kui
馬力,be lat
骨力,kut lat
馬上,ma siong
高女,ko li
高中,ko tiong
高手,ko tshiu
酒仙,tsiu sian
釘仔,ting a
馬仔,be a
鬼仔,kui a
釘仔鉗,ting a khinn
鬥句,tau ku
酒母,tsiu bu
配合,phue hap
除名,tu mia
骨肉,kut jiok
高血壓,ko hueh ap
馬西馬西,ma se ma se
針灸,tsiam ku
配角,phue kak
針車,tsiam tshia
高見,ko kian
高尚,ko siong
釘孤枝,ting koo ki
馬拉松,ma la song
酒杯,tsiu pue
高明,ko bing
酒矸,tsiu kan
針空,tsiam khang
鬥空,tau khang
酒矸窒仔,tsiu kan that a
鬥股,tau koo
陣雨,tsun hoo
鬼門,kui mng
鬼門關,kui mng kuan
除非,tu hui
鬼剃頭,kui thi thau
針指,tsiam tsainn
鬥相共,tau sann kang
閃風,siam hong
馬面,be bin
配料,phue liau
釘根,ting kin
骨格,kut keh
骨氣,kut khi
骨烌,kut hu
陣疼,tsun thiann
鬼神,kui sin
高級,ko kip
飢荒,ki hng
酒配,tsiu phue
鬥陣,tau tin
馬馬虎虎,ma ma hu hu
鬥做伙,tau tso hue
酒瓶,tsiu pan
鬥無閒,tau bo ing
配給,phue kip
閃著,siam tioh
高貴,ko kui
閃開,siam khui
酒開仔,tsiu khui a
針黹,tsiam tsi
酒窟仔,tsiu khut a
高粱酒,kau liang tsiu
鬥跤手,tau kha tshiu
馬鈴薯,ma ling tsi
鬥夥計,tau hue ki
鬥榫頭,tau sun thau
酒漏仔,tsiu lau a
鬼精,kui tsiann
馬褂,be kua
針鼻,tsiam phinn
酒樓,tsiu lau
高潮,ko tiau
酒醉,tsiu tsui
骨輪,kut lun
馬鞍,be uann
馬齒豆,be khi tau
鬥鬧熱,tau lau jiat
酒甌,tsiu au
配頭,phue thau
陣頭,tin thau
馬頭,be thau
骨頭烌,kut thau hu
鬼頭鬼腦,kui thau kui nau
馬戲,be hi
鬥幫贊,tau pang tsan
酒糟,tsiu tsau
閃避,siam pi
馬鮫,be ka
釘點,ting tiam
酒甕,tsiu ang
酒癖,tsiu phiah
馬薺,be tsi
馬鞭,be pinn
閃爍,siam sih
高麗,ko le
高麗參,ko le sim
高麗菜,ko le tshai
高麗菜穎仔,ko le tshai inn a
乾,kuann
乾,kan
乾,khian
偃,ian
假,ka
假,ke
偌,gua
偏,phian
偏,phinn
做,tso
停,thing
偝,ainn
偷,thau
兜,tau
剪,tsian
副,hu
假𠢕,ke gau
做人,tso lang
做人,tso lang
做人情,tso jin tsing
偉大,ui tai
做工,tso kang
偝巾,ainn kin
做大水,tso tua tsui
偷工減料,thau kang kiam liau
偏心,phian sim
做歹,tso phainn
停手,thing tshiu
停止,thing tsi
副手,hu tshiu
做月內,tso gueh lai
做牙,tso ge
假仙,ke sian
乾仔孫,kan a sun
假仙假觸,ke sian ke tak
假包,ke pau
做司公,tso sai kong
做功德,tso kong tik
剪布,tsian poo
副本,hu pun
做生日,tso senn jit
偷生的,thau senn e
做生理,tso sing li
做伙,tso hue
健丟,kian tiu
健全,kian tsuan
偏名,phian mia
假好衰,ke ho sue
假死,ke si
做旬,tso sun
假死假活,ke si ke uah
做色,tso sik
做忌,tso ki
假使,ka su
偷來暗去,thau lai am khi
做店面,tso tiam bin
偷拈,thau ni
做法,tso huat
偷咬雞仔,thau ka ke a
做客,tso kheh
偷看,thau khuann
偷食,thau tsiah
偷食步,thau tsiah poo
做風颱,tso hong thai
偃倒,ian to
做臭人,tso tshau lang
做陣,tso tin
做鬼,tso kui
假鬼假怪,ke kui ke kuai
偏偏,phian phian
偏偏仔,phian phian a
健康,kian khong
偷掠,thau liah
做莊,tso tsong
假喙齒,ke tshui khi
偷提,thau theh
偷揜,thau iap
假無意,ke bo i
假痟,ke siau
做痢,tso li
停睏,thing khun
副業,hu giap
停跤,thing kha
停電,thing tian
偌爾,gua ni
剪綹仔,tsian liu a
假銀票,ke gin phio
偏僻,phian phiah
假影,ke iann
做瘦氣,tso san khui
做親情,tso tshin tsiann
偏頭,phinn thau
做頭,tso thau
做戲,tso hi
偌濟,gua tse
做醮,tso tsio
做議量,tso gi niu
做譴損,tso khian sng
偷聽,thau thiann
勒,lik
動,tang
動,tong
務,bu
匏,pu
匙,si
匾,pian
區,khu
參,tsham
唌,siann
唬,hoo
唱,tshiang
唱,tshiunn
唸,liam
啄,tok
啉,lim
啊, ah
問,mng
啖,tam
唯一,ui it
唌人,siann lang
唬人,hoo lang
動土,tang thoo
動工,tang kang
啞口,e kau
區公所,khu kong soo
動手,tang tshiu
啉水,lim tsui
匏仔,pu a
參仔,sim a
參加,tsham ka
啟示,khe si
商行,siong hang
參考冊,tsham kho tsheh
動作,tong tsok
區別,khu piat
商店,siong tiam
動物,tong but
商品,siong phin
動員,tong uan
商展,siong tian
唬秤頭,hoo tshin thau
參茸,sim jiong
啉茶,lim te
啉酒,lim tsiu
區域,khu hik
匏桸,pu hia
動產,tong san
商船,siong tsun
商場,siong tiunn
啉湯,lim thng
啟發,khe huat
商量,siong liong
動搖,tong iau
商業,siong giap
參詳,tsham siong
動箸,tang ti
啄鼻仔,tok phinn a
商標,siong phiau
動機,tong ki
動靜,tong tsing
啄龜,tok ku
啖糝,tam sam
唱聲,tshiang siann
勘驗,kham giam
啥,siann
啦, lah
圇,lun
國,kok
埠,poo
埤,pi
培,pue
堂,tng
堂,tong
堅,kian
堆,tui
堵,too
夠,kau
娶,tshua
啥人,siann lang
夠工,kau kang
國中,kok tiong
國內,kok lai
堅巴,kian pa
夠水,kau tsui
基本,ki pun
夠本,kau pun
國立,kok lip
夠用,kau ing
基地,ki te
執行,tsip hing
堅疕,kian phi
國防,kok hong
堅固,kian koo
堅定,kian ting
國法,kok huat
執法,tsip huat
啥物,siann mih
堂的,tong e
堆肥,tui pui
基金,ki kim
堅持,kian tshi
娶某,tshua boo
堅凍,kian tang
圈套,khuan tho
夠氣,kau khui
堅乾,kian kuann
堂堂,tong tong
夠夠,kau kau
啥貨,siann hue
啥款,siann khuan
奢華,tshia hua
娶新娘,tshua sin niu
娶新婦,tshua sin pu
執照,tsip tsiau
基督,ki tok
基督教,ki tok kau
培墓,pue bong
國歌,kok kua
國語,kok gi
國際,kok tse
啥潲,siann siau
培養,pue iong
埠頭,poo thau
基礎,ki tshoo
夠額,kau giah
奢颺,tshia iann
國寶,kok po
國籍,kok tsik
婆,po
婚,hun
婦,hu
寄,kia
寅,in
密,bat
將,tsiong
將,tsiong
專,tsuan
婦人人,hu jin lang
婦女,hu li
將才,tsiong tsai
專工,tsuan kang
專心,tsuan sim
婆仔,po a
寄付,kia hu
寄生仔,kia senn a
寄生蟲,kia senn thang
婊囝,piau kiann
密告,bit ko
寄批,kia phue
將來,tsiong lai
婆姐,o tsia
將近,tsiong kin
專門,tsuan bun
寄金簿仔,kia kim phoo a
宿怨,siok uan
婚約,hun iok
將軍,tsiong kun
寄託,kia thok
密婆,bit po
密密,bat bat
密喌喌,bat tsiuh tsiuh
婊間,piau king
寄話,kia ue
寂寞,tsik bok
密實,bat tsat
婊頭,piau thau
婚禮,hun le
寄藥包,kia ioh pau
專權,tsuan khuan
屜,thuah
崎,kia
崩,pang
帶,tai
帶,tua
張,tiunn
張,tng
強,kiong
得,tik
得,tit
得人疼,tit lang thiann
得人惜,tit lang sioh
崩山,pang suann
帶手,tua tshiu
屜仔,thuah a
崎仔,kia a
崙仔,lun a
得失,tik sit
常在,tshiang tsai
張老,tiunn lau
彩色,tshai sik
強壯,kiong tsong
帶孝,tua ha
帶身命,tai sin mia
張身勢,tiunn sin se
強制,kiong tse
帶念,tai liam
強押,kiong ah
崇拜,tsong pai
張持,tiunn ti
帶桃花,tai tho hue
帶病,tai penn
帶衰,tai sue
康健,khong kian
常常,siong siong
強強,kiong kiong
張掇,tiunn tuah
強欲,kiong beh
張鳥鼠,tng niau tshi
強盜,kiong to
強硬,kiong nge
張等,tng tan
得勢,tit se
得意,tik i
強搶,kiong tshiunn
強摃,kiong kong
得罪,tik tsue
帶領,tua nia
帶膭,tua kui
彩頭,tshai thau
強辯,kiong pian
徙,sua
徛,khia
從,tsing
從,tsiong
悾,khong
情,tsing
惜,sioh
惝,tshing
戛,khiat
挲,so
捥,ng
捧,phong
情人,tsing jin
戛火,khiat hue
惜皮,sioh phue
徛名,khia mia
惜囝,sioh kiann
徙位,sua ui
情形,tsing hing
自來,tsu lai
從到今,tsing kau tann
惜命命,sioh mia mia
徛泅,khia siu
患者,huan tsia
徛屏,khia pin
捨施,sia si
徛眉,khia bai
情面,tsing bin
惜面皮,sioh bin phue
徛家,khia ke
徙栽,sua tsai
挲草,so tshau
徛起,khia khi
悾悾,khong khong
情理,tsing li
徛票,khia phio
情報,tsing po
徛黃,khia ng
情勢,tsing se
挲圓,so inn
挲圓仔湯,so inn a thng
情意,tsing i
悾歁,khong kham
情義,tsing gi
徙跤,sua kha
徛壽,khia siu
悽慘,tshi tsham
悽慘落魄,tshi tsham lok phik
惜福,sik hok
徛算,khia sng
徛算講,khia sng kong
情緒,tsing su
徛衛兵,khia ue ping
徙鋪,sua phoo
徛燈篙,khia ting ko
徛頭,khia thau
悾闇,khong am
徛鵝,khia go
悾顛,khong tian
情願,tsing guan
徛靈,khia ling
挲鹽,so iam
捲,kng
捷,tsiap
捻,liam
捻,liam
捽,sut
捾,kuann
掀,hian
掂,tim
掃,sau
掉,tiau
排,pai
掖,ia
掘,kut
掛,kua
掛,khua
掜,tau
掠,liah
採,tshai
探,tham
接,tsiap
接,tsih
控,khang
推,the
推,thui
掩,am
掩,iam
掩,ng
掩,om
掮,khainn
救,kiu
敗,pai
教,ka
教,kau
接力,tsih lat
救人,kiu lang
捾水,kuann tsui
掛心,khua sim
接手,tsiap tshiu
捲心白,kng sim peh
救火,kiu hue
捽仔,sut a
掘仔,kut a
教冊,ka tsheh
救世主,kiu se tsu
掠包,liah pau
排斥,pai thik
敗市,pai tshi
採用,tshai iong
教示,ka si
捽目尾,sut bak bue
掠交替,liah kau the
排列,pai liat
掛名,kua mia
推行,thui hing
救兵,kiu ping
救助,kiu tsoo
掠沙筋,liah sua kin
掠狂,liah kong
教育,kau iok
敏豆,bin tau
接受,tsiap siu
掠兔仔,liah thoo a
掠坦橫,liah than huainn
掃帚,sau tshiu
教官,kau kuann
掃帚星,sau tshiu tshenn
接枝,tsiap ki
掠直,liah tit
掠長補短,liah tng poo te
掩咯雞,ng kok ke
接待,tsiap thai
救星,kiu tshenn
教員,kau uan
掩崁,am kham
敗害,pai hai
敗家,pai ke
教師,kau su
掃梳,sau se
掃梳笒仔,sau se gim a
接納,tsiap lap
掖秧仔,ia ng a
教訓,kau hun
接骨,tsiap kut
排骨酥,pai kut soo
掠做,liah tso
教務,kau bu
捷捷,tsiap tsiap
接接,tsih tsiap
敏捷,bin tsiat
教授,kau siu
掩掩揜揜,ng ng iap iap
捾桶仔,kuann thang a
排球,pai kiu
探訪,tham hong
接喙,tsiap tshui
救援,kiu uan
推測,thui tshik
掛牌,kua pai
掠猴,liah kau
掠無頭摠,liah bo thau tsang
掠痧,liah sua
掠筋,liah kin
敗腎,pai sin
推進,thui tsin
排隊,pai tui
掃塗跤,sau thoo kha
掛意,kua i
掠準,liah tsun
排解,pai kai
接跤,tsiap kha
捷運,tsiat un
接載,tsih tsai
掃墓,sau bong
探墓厝,tham bong tshu
掠漏,liah lau
掖種,ia tsing
敗價,pai ke
推廣,thui kong
掛慮,kua li
推撨,tshui tshiau
推論,thui lun
推銷,thui siau
教學,kau hak
掠篙泅,liah ko siu
探親,tham tshin
探頭,tham thau
掠龍,liah ling
掠龜走鱉,liah ku tsau pih
掠龍的,liah ling e
捲螺仔風,kng le a hong
捲螺仔旋,kng le a tsng
採購,tshai koo
捲薰,kng hun
掛礙,kua gai
推辭,the si
接觸,tsiap tshiok
接續,tsiap siok
救護,kiu hoo
敗露,pai loo
救護車,kiu hoo tshia
探聽,tham thiann
斜,tshia
斜,tshuah
旋,tsng
旋,suan
族,tsok
晝,tau
晡,poo
望,bang
望,bong
桮,pue
桱,kenn
桶,thang
桷,kak
桸,hia
桿,kuainn
梅,mue
桱仔,kenn a
桶仔,thang a
桷仔,kak a
梅仔,mue a
梅仔餅,mue a piann
斜目,tshia bak
斜角,tshuah kak
梅花,mui hue
桶柑,thang kam
梁柱,niu thiau
梅毒,mui tok
桶捾,thang kuann
桶筍,thang sun
斜視,sia si
桶箍,thang khoo
桶蓋,thang kua
桶盤,thang puann
族親,tsok tshin
旋藤,suan tin
族譜,tsok phoo
條,liau
條,tiau
梢,sau
梨,lai
梯,thui
欲,beh
欶,suh
欸, eh
殺,sat
液,sioh
涼,liang
欶水,suh tsui
殺手,sat tshiu
涼水,liang tsui
梨仔,lai a
棄世,khi se
欶奶,suh ling
殺生,sat sing
條件,tiau kiann
欲死欲活,beh si beh uah
欲呢,beh ni
條直,tiau tit
欲知,beh tsai
涵空,am khang
涼亭,liang ting
條約,tiau iok
涼風,liang hong
殺害,sat hai
梧桐,ngoo tong
殺氣,sat khi
梢梢,sau sau
涼傘,niu suann
條款,tiau khuan
梟雄,hiau hiong
涼勢,liang se
棄嫌,khi hiam
欲暗仔,beh am a
涵溝,am kau
欶管,suh kong
梢聲,sau siann
棄權,khi khuan
淋,lam
淘,to
淚,lui
深,tshim
淹,im
淺,tshian
添,thiam
添,thinn
清,tshing
烰,phu
添丁,thiam ting
淑女,siok li
淮山,huai san
淹大水,im tua tsui
深井,tshim tsenn
淋水,lam tsui
淡水,tam tsui
淹水,im tsui
清心,tshing sim
清水,tshing tsui
清火,tshing hue
清白,tshing pik
深交,tshim kau
混合,hun hap
淹死,im si
淺色,tshian sik
深坑,tshim khenn
清秀,tshing siu
淺見,tshian kian
深刻,tshim khik
深夜,tshim ia
淺拖仔,tshian thua a
添油香,thiam iu hiunn
清芳,tshing phang
淋雨,lam hoo
深度,tshim too
清幽,tshing iu
淨香,tsing hiunn
清氣,tshing khi
清氣相,tshing khi siunn
淺眠,tshian bin
清茶,tshing te
清酒,tshing tsiu
深淺,tshim tshian
清淨,tshing tsing
深造,tshim tso
淪陷,lun ham
清單,tshing tuann
清寒,tshing han
添粧,thiam tsng
清閒,tshing ing
添飯,thinn png
淫亂,im luan
混亂,hun luan
淺想,tshian siunn
清廉,tshing liam
添話,thinn ue
添福壽,thiam hok siu
清數,tshing siau
清潔,tshing kiat
清糜,tshing mue
淡薄仔,tam poh a
焐,u
爽,song
牽,khan
圈,khian
犁,le
猛,bing
猛,me
猜,tshai
現,hian
現,hian
球,kiu
牽亡,khan bong
牽公,khan kong
牽手,khan tshiu
牽牛,khan gu
猛火,me hue
圈仔,khian a
現世,hian si
現代,hian tai
犁田,le tshan
牽成,khan sing
現此時,hian tshu si
牽尪姨,khan ang i
爽快,song khuai
牽車,khan tshia
牽抾,khan khioh
牽拖,khan thua
現拄現,hian tu hian
牽的,khan e
現金,hian kim
現流仔,hian lau a
牽師仔,khan sai a
牽挽,khan ban
牽核仔,khan hat a
牽粉,khan hun
牽罟,khan koo
現胸,hian hing
猛將,bing tsiong
球桮,kiu pue
現現,hian hian
牽連,khan lian
現場,hian tiunn
球場,kiu tiunn
牽猴仔,khan kau a
牽絲,khan si
現象,hian siong
球間,kiu king
猜想,tshai siong
現實,hian sit
猜疑,tshai gi
球箠,kiu tshue
牽線,khan suann
牽豬哥,khan ti ko
球鞋,kiu e
猛醒,me tshenn
球賽,kiu sai
猛獸,bing siu
牽羹,khan kenn
牽羅經,khan lo kenn
牽藤,khan tin
理,li
瓶,pan
瓷,hui
甜,tinn
產,san
疏,se
疏,soo
痔,ti
痕,hun
盒,ah
盒,ap
盛,sing
眯,bi
眵,tshuh
眷,kuan
眼,gan
眼力,gan lik
眾人,tsing lang
瓷仔,hui a
略仔,lioh a
盒仔,ap a
瓷仔店,hui a tiam
盒仔餅,ap a piann
甜瓜,tinn kue
眵目,tshuh bak
眼光,gan kong
產地,san te
甜豆,tinn tau
甜言蜜語,tinn gian bit gi
理事,li su
異性,i sing
疏忽,soo hut
眼前,gan tsian
眼科,gan kho
硃砂痣,tsu se ki
眼神,gan sin
甜粅粅,tinn but but
甜茶,tinn te
理財,li tsai
產婆,san po
產婦,san hu
眵眵,tshuh tshuh
略略仔,lioh lioh a
甜湯,tinn thng
疏開,soo khai
產業,san giap
理解,li kai
痕跡,hun jiah
甜路,tinn loo
甜粿,tinn kue
甜蜜,tinn bit
疏遠,soo uan
痔瘡,ti tshng
理論,li lun
疏櫳,se lang
眷屬,kuan siok
票,phio
祭,tse
窒,that
章,tsiong
章,tsiunn
笠,leh
符,hu
笨,pun
第,te
笱,ko
第一,te it
祭文,tse bun
窒仔,that a
笠仔,leh a
符仔,hu a
祧仔內,thiau a lai
移民,i bin
符合,hu hap
符咒,hu tsiu
祭孤,tse koo
祭祀,tse su
窒倒街,that to ke
祭祖,tse tsoo
移動,i tong
窒喙空,that tshui khang
竟然,king jian
章程,tsiong thing
符號,hu ho
硫磺,liu hong
祭獻,tse hian
粒,liap
粕,phoh
粗,tshoo
紩,thinn
紬,thiu
紮,tsah
紮,tsat
細,se
紲,sua
紺,khong
絃,hian
組,tsoo
絆,puann
缽,puah
羞,tshiu
統一,thong it
粗人,tshoo lang
粗工,tshoo kang
紳士,sin su
紹介,siau kai
紲手,sua tshiu
粒仔,liap a
絃仔,hian a
粗布,tshoo poo
紮布,tsah poo
粗用,tshoo ing
細囝,se kiann
組合,tsoo hap
紺色,khong sik
細位,se ui
終身,tsiong sin
細叔,se tsik
粗坯,tshoo phue
紲拍,sua phah
粗俗,tshoo siok
粗勇,tshoo iong
粗俗物仔,tshoo siok mih a
粗俗貨,tshoo siok hue
細姨,se i
粗穿,tshoo tshing
粗重,tshoo tang
紩衫,thinn sann
統計,thong ke
粗紙,tshoo tsua
粗桶,tshoo thang
粗瓷,tshoo hui
粕粕,phoh phoh
細粒子,se liap tsi
紲喙,sua tshui
紲喙尾,sua tshui bue
細菌,se khun
粗菜便飯,tshoo tshai pian png
紲落去,sua loh khi
粗飽,tshoo pa
習慣,sip kuan
細漢,se han
粗魯,tshoo loo
粒積,liap tsik
累積,lui tsik
細膩,se ji
紹興酒,siau hing tsiu
紮錢,tsah tsinn
組頭,tsoo thau
粗糠,tshoo khng
細聲,se siann
組織,tsoo tsit
脣,tun
脫,thuat
脫,thut
脯,poo
舂,tsing
船,tsun
莊,tsng
舵公,tai kong
脫手,thuat tshiu
耞仔,kenn a
船主,tsun tsu
船仔,tsun a
荷包,ha pau
舂米,tsing bi
舂臼,tsing khu
船尾,tsun bue
脫走,thuat tsau
脫身,thuat sin
船員,tsun uan
脯脯,poo poo
聊聊仔,liau liau a
船期,tsun ki
脫種,thuat tsing
船廠,tsun tshiunn
脫箠,thut tshue
脫線,thuat suann
脫輪,thut lun
船艙,tsun tshng
船頭,tsun thau
脫離,thuat li
莊嚴,tsong giam
荷蘭豆,hue lian tau
莢,ngeh
莫,bok
莫,mai
蚵,o
蚶,ham
蛀,tsiu
蛆,tshi
蛇,tsua
處方,tshu hng
蚵仔,o a
蚶仔,ham a
蚵仔煎,o a tsian
蚵仔麵線,o a mi suann
蛇瓜,tsua kue
處份,tshu hun
莫怪,bok kuai
莫非,bok hui
蚵炱,o te
處理,tshu li
莧菜,hing tshai
處置,tshu ti
處罰,tshu huat
蛀鼻,tsiu phinn
蛀齒,tsiu khi
蛀龜仔,tsiu ku a
莫講,mai kong
蛀蟲,tsiu thang
術,sut
術,sut
袋,te
袚,phuah
被,pi
被,phue
規,kui
覓,ba
覓,mai
訣,kuat
設,siat
豉,sinn
規个,kui e
規千萬,kui tshing ban
規心,kui sim
規爿,kui ping
袋仔,te a
規世人,kui si lang
許可,hi kho
設立,siat lip
規年迵天,kui ni thang thinn
歸尾,kui bue
設局,siat kiok
規身軀,kui sin khu
規定,kui ting
規則,kui tsik
規律,kui lut
設施,siat si
設計,siat ke
規面,kui bin
規氣,kui khi
規矩,kui ki
規陣,kui tin
訪問,hong bun
規堆,kui tui
設備,siat pi
被單,phue tuann
設想,siat siong
規腹火,kui pak hue
規路,kui loo
豉膎,sinn ke
規模,kui boo
設緣投,siat ian tau
鴟鴞,ba hioh
袚鍊,phuah lian
被囊,phue long
豉鹽,sinn iam
貨,hue
販,huan
販,phuann
貪,tham
貫,kng
赦,sia
趼,lan
跂,kue
軟,nng
透,thau
逐,jiok
逐,tak
途,too
這,tse
這,tsit
通,thang
通,thong
逝,tsua
逞,thing
造,tso
連,lian
軟𩛩𩛩,nng kauh kauh
軟㽎㽎,nng sim sim
逐个,tak e
透中晝,thau tiong tau
貪心,tham sim
軟心,nng sim
透日,thau jit
逐日,tak jit
造化,tso hua
造反,tso huan
透心涼,thau sim liang
貨主,hue tsu
販仔,huan a
透世人,thau si lang
這世人,tsit si lang
販仔白,huan a peh
通用,thong iong
責任,tsik jim
通光,thang kng
連回,lian hue
透年,thau ni
逐年,tak ni
透早,thau tsa
貧血,pin hiat
貨色,hue sik
赦免,sia bian
貨尾,hue bue
透尾,thau bue
通批,thong phue
軟汫,nng tsiann
貨底,hue te
貪官汙吏,tham kuann u li
通知,thong ti
透雨,thau hoo
通姦,thong kan
速度,sok too
透流,thau lau
貪食,tham tsiah
透風,thau hong
通風,thang hong
販厝,huan tshu
逐家,tak ke
軟弱,luan jiok
通書,thong su
這站,tsit tsam
貨草,hue tshau
軟荍荍,nng sio sio
貪財,tham tsai
貫針,kng tsiam
軟骨,nng kut
這陣,tsit tsun
這馬,tsit ma
通常,thong siong
軟晡,nng poo
連累,lian lui
連紲,lian sua
貨船,hue tsun
販貨,phuann hue
責備,tsik pi
通報,thong po
貧惰,pin tuann
貧惰骨,pin tuann kut
軟絲仔,nng si a
軟塗深掘,nng thoo tshim kut
這搭,tsit tah
透暗,thau am
逐暗,tak am
赦罪,sia tsue
跂跤,kue kha
軟跤,nng kha
造話,tso ue
軟跤蝦,nng kha he
貧道,pin to
這過,tsit kue
通過,thong kue
造路,tso loo
通鼓,thong koo
透暝,thau me
造福,tso hok
軟膏膏,nng ko ko
逍遙,siau iau
貨樣,hue iunn
通緝,thong tsip
販賣,huan be
貨頭,hue thau
連環,lian khuan
這聲,tsit siann
這點仔,tsit tiam a
逐擺,tak pai
連鞭,liam mi
軟轎,nng kio
通譯,thong ik
連續,lian siok
貪戀,tham luan
部,poo
部,pho
都,to
野,ia
釣,tio
釧,tshuan
閉,pi
陪,pue
陰,im
陵,nia
陷,ham
雪,seh
雪,suat
頂,ting
頂𦜆,ting ham
部下,poo ha
頂下,ting e
陳三五娘,tan sann goo niu
部份,poo hun
頂勻,ting un
野心,ia sim
雪文,sap bun
頂手,ting tshiu
頂日,ting jit
頂月,ting gueh
頂月日,ting gueh jit
頂日仔,ting jit a
雪文粉,sap bun hun
頂世人,ting si lang
雪仔柑,seh a kam
頂冬,ting tang
頂司,ting si
頂半身,ting puann sin
頂半暝,ting puann me
都市,too tshi
野生,ia sing
都合,too hap
陰地,im te
部位,poo ui
陪伴,pue phuann
陷坑,ham khenn
野味,ia bi
野性,ia sing
頂肱骨,ting kong kut
部長,poo tiunn
閉思,pi su
頂面,ting bin
陷害,ham hai
陷眠,ham bin
頂真,ting tsin
野馬,ia be
陳情,tin tsing
陰桮,im pue
頂晡,ting poo
野球,ia kiu
粟鳥仔,tshik tsiau a
釣魚翁,tio hi ang
雀斑,tshiok pan
頂替,ting the
頂港,ting kang
陰間,im kan
陰陽,im iong
部落,poo lok
頂落,ting loh
頂腹蓋,ting pak kua
頂過,ting kue
釣鉤,tio kau
陪綴,pue tue
釣餌,tio ji
陰魂,im hun
陰德,im tik
頂層,ting tsan
頂輩,ting pue
陰鴆,im thim
陰曆,im lik
陸橋,liok kio
陰謀,im boo
頂頭,ting thau
頂幫,ting pang
頂擺,ting pai
野雞仔車,ia ke a tshia
野獸,ia siu
頂懸,ting kuan
野蠻,ia ban
魚,hi
鳥,tsiau
鹿,lok
麥,beh
麻,ba
麻,mua
魚丸,hi uan
魚子,hi tsi
麥片,beh phinn
鳥仔,tsiau a
鹿仔,lok a
麥仔,beh a
魚仔市,hi a tshi
鳥仔岫,tsiau a siu
麥仔茶,beh a te
麥仔酒,beh a tsiu
鳥仔踏,tsiau a tah
麻布,mua poo
魚池,hi ti
麻竹,mua tik
麻竹筍,mua tik sun
魚肝油,hi kuann iu
鹿角,lok kak
魚刺,hi tshi
魚拊,hi hu
麻油,mua iu
麻油酒,mua iu tsiu
麻虱目,mua sat bak
麥芽膏,beh ge ko
麥芽糖,beh ge thng
麻衫,mua sann
麻射,ba sia
魚栽,hi tsai
魚翅,hi tshi
麻索,mua soh
鹿茸,lok jiong
鳥梨仔,tsiau lai a
魚脯,hi poo
麻袋,mua te
麻雀,mua tshiok
麻雀子仔,mua tshiok ji a
魚釣仔,hi tio a
魚塭,hi un
麻痺,ba pi
鳥銃,tsiau tshing
鳥鼠,niau tshi
鳥鼠仔冤,niau tshi a uan
鳥鼠仔症,niau tshi a tsing
鳥鼠張,niau tshi tng
鳥鼠擗仔,niau tshi phiak a
鳥鼠觸仔,niau tshi tak a
魚網,hi bang
魚餌,hi ji
麻糍,mua tsi
麻醉,ba tsui
鳥擗仔,tsiau phiak a
魚頭,hi thau
魚臊,hi tsho
魚鮮,hi tshinn
魚藤,hi tin
麻藥,ba ioh
魚鰓,hi tshi
魚鰾,hi pio
魚鱗,hi lan
魚鱗𤺅仔,hi lan tshe a
麻粩,mua lau
傍,png
傘,suann
傑出,kiat tshut
備查,pi tsa
傀儡,ka le
傀儡戲,ka le hi
割,kuah
創,tshong
創,tshong
勞,lo
博,phok
啼,thi
喀,khennh
喂, eh
喂, ueh
喃,nauh
善,sian
喈,kainn
喊,hiam
喋,thih
喌,tsu
喓,iaunn
喔, ooh
喘,tshuan
喙,tshui
喝,huah
喢,sannh
喙䫌,tshui phue
勞力,loo lat
勞力,lo lik
勞工,lo kang
博士,phok su
喙口,tshui khau
喙下斗,tshui e tau
喘大氣,tshuan tua khui
勞心,lo sim
喙斗,tshui tau
喙水,tshui sui
割包,kuah pau
喇叭,la pah
喙白,tshui peh
割肉,kuah bah
喙舌,tshui tsih
勝利,sing li
喙尾,tshui bue
善男信女,sian lam sin li
善良,sian liong
喙角,tshui kak
喜帖,hi thiap
創治,tshong ti
博物,phok but
博物館,phok but kuan
創空,tshong khang
喙空,tshui khang
喙花,tshui hue
割金,kuah kim
喝咻,huah hiu
喝玲瑯,huah lin long
割香,kuah hiunn
啼哭,thi khau
喝拳,huah kun
喘氣,tshuan khui
割耙,kuah pe
喙臭,tshui tshau
喜酒,hi tsiu
勞動,lo tong
喙脣,tshui tun
喙脣皮,tshui tun phue
割貨,kuah hue
創造,tshong tso
喝魚仔,huah hi a
割喉,kuah au
啼啼哭哭,thi thi khau khau
創景,tshong king
喙殘,tshui tsuann
喙焦,tshui ta
博愛,phok ai
創業,tshong giap
喉滇,au tinn
勞煩,lo huan
喀痰,khennh tham
喙罨,tshui am
喙箍,tshui khoo
割價,kuah ke
喜劇,hi kiok
喑噁,inn onn
割稻仔,kuah tiu a
割稻仔尾,kuah tiu a bue
喙齒,tshui khi
喙齒根,tshui khi kin
創辦,tshong pan
創舉,tshong ki
喉韻,au un
喙瀾,tshui nua
喉鐘,au tsing
喙鬚,tshui tshiu
喨,liang
單,tuann
圍,ui
堪,kham
報,po
場,tiunn
壺,hoo
壺,oo
圍巾,ui kin
單元,tan guan
報仇,po siu
喨仔,liang a
喪失,song sit
場合,tiunn hap
單位,tan ui
報告,po ko
單身,tuann sin
喪事,song su
報到,po to
場所,tiunn soo
場面,tiunn bin
報冤,po uan
報恩,po un
單純,tan sun
報紙,po tsua
報馬仔,po be a
單逝,tuann tsua
報復,po hok
圍棋,ui ki
報答,po tap
單跤手,tuann kha tshiu
報數,po siau
報銷,po siau
單獨,tan tok
報頭,po thau
圍牆,ui tshiunn
圍軀裙,ui su kun
圍爐,ui loo
媌,ba
媠,sui
富,pu
寒,kuann
寒,gan
尊,tsun
尋,siam
就,tsiu
就,to
媒人,mue lang
寒人,kuann lang
媒人公,mue lang kong
媒人婆,mue lang po
媒人喙,mue lang tshui
媒人禮,mue lang le
富戶,hu hoo
寒天,kuann thinn
媌仔,ba a
媠色,sui sik
尊長,tsun tiong
就近,tsiu kin
就是,to si
就按呢,tsiu an ne
寒流,han liu
寒衫,kuann sann
尊重,tsun tiong
媠氣,sui khui
富強,hu kiong
寒著,kuann tioh
富貴,hu kui
尊貴,tsun kui
尊敬,tsun king
富裕,hu ju
尊稱,tsun tshing
寒熱,kuann juah
寒熱仔,kuann jiat a
媠噹噹,sui tang tang
尊嚴,tsun giam
帽,bo
幅,pak
幾,kui
循,sun
幾工,kui kang
帽仔,bo a
悲哀,pi ai
幾若,kui na
幾若工,kui na kang
復原,hok guan
復習,hok sip
悶悶,bun bun
悲傷,pi siong
悲慘,pi tsham
悲劇,pi kiok
復興,hok hing
循環,sun khuan
復職,hok tsit
悲觀,pi kuan
惡,ok
惱,loo
愖,sim
愣,gang
捶,tui
掌,tsiong
掌,tsiunn
掔,khian
掣,tshuah
掰,pue
揀,king
揈,hong
揉,jiu
擗,phiak
揌,sai
揍,bok
描,bio
提,the
提,theh
插,tshah
插,tshap
插一跤,tshap tsit kha
惡人,ok lang
插手,tshap tshiu
捶心肝,tui sim kuann
掰手面,pue tshiu bin
插代誌,tshap tai tsi
提出,the tshut
提名,the mia
提防,the hong
提供,the kiong
惡性,ok sing
提拔,the puat
插枝,tshah ki
插花,tshah hue
插花仔,tshah hue a
惡毒,ok tok
掣流,tshuah lau
揀食,king tsiah
提案,the an
惱氣,loo khi
插班,tshah pan
插胳,tshah koh
揀茶,king te
提起,the khi
惡馬,ok be
插喙,tshap tshui
插喙插舌,tshap tshui tshap tsih
惡報,ok po
掌握,tsiong ak
插牌,tshap pai
揀菜,king tshai
掰開,pue khui
插話,tshah ue
描寫,bio sia
插潲,tshap siau
惡確確,ok khiak khiak
提親,the tshin
提醒,the tshenn
提頭,the thau
插頭,tshah thau
插雜,tshap tsap
提議,the gi
惡霸,ok pa
掌權,tsiong khuan
換,uann
揜,iap
握,ak
揣,tshue
揬,tuh
揲,tiap
揹,phainn
摒,piann
敢,kam
敢,kann
散,san
散,san
散,suann
散,suann
敧,khi
敨,thau
景,king
散工,suann kang
散工,suann kang
散凶,san hiong
散凶人,san hiong lang
敨中氣,thau tiong khui
換手,uann tshiu
握手,ak tshiu
散文,suann bun
斯文,su bun
敢毋是,kam m si
散仙,suann sian
摒本,piann pun
敢有,kam u
敢死,kann si
景色,king sik
援助,uan tsoo
揜尾狗,iap bue kau
散形,suann hing
散赤,san tshiah
換帖的,uann thiap e
換紅,uann ang
敢若,kann na
散食人,san tsiah lang
敨氣,thau khui
景氣,king khi
散陣,suann tin
散鬼,san kui
斑馬,pan be
斑馬線,pan ma suann
換做,uann tso
摒掃,piann sau
散票,suann phio
敢通,kam thang
普通,phoo thong
摒貨底,piann hue te
普普仔,phoo phoo a
普渡,phoo too
敨開,thau khui
散會,san hue
換準,uann tsun
斑節蝦,pan tsat he
普遍,phoo phian
智慧,ti hui
景緻,king ti
散賣,suann be
換鋪,uann phoo
散學,suann oh
揣頭路,tshue thau loo
敢講,kam kong
斑鴿,pan kah
智識,ti sik
晾,ne
替,the
朝,tiau
期,ki
棉,mi
棋,ki
棕,tsang
棗,tso
棚,penn
棟,tong
椅,i
棋子,ki ji
替手,the tshiu
棺木,kuan bok
朝代,tiau tai
棉仔,mi a
棍仔,kun a
棗仔,tso a
椅仔,i a
棑仔頭,pai a thau
替身,the sin
最後,tsue au
期待,ki thai
椅苴,i tsu
期限,ki han
棺柴,kuann tsha
椅桌,i toh
棉紗,mi se
暑假,su ka
椅條,i liau
棒球,pang kiu
替換,the uann
棕筅仔,tsang tshing a
期間,ki kan
棉裘,mi hiu
椅墊仔,i tiam a
棕蓑,tsang sui
棋盤,ki puann
椅頭仔,i thau a
棉襀,mi tsioh
棉襀被,mi tsioh phue
椅轎,i kio
棕鑢仔,tsang lu a
椏,ue
欺,khi
款,khuan
款,khuann
殕,phu
殼,khak
毯,than
減,kiam
渡,too
渧,te
渡口,too khau
毯仔,than a
殼仔絃,khak a hian
殕色,phu sik
殘忍,tsan jim
減法,kiam huat
植物,sit but
款待,khuan thai
椪柑,phong kam
減省,kiam sing
欺負,khi hu
渡船,too tsun
殕殕,phu phu
殘酷,tsan khok
欺瞞,khi mua
渡頭,too thau
款勸,khuan khng
港,kang
渴,khuah
湖,oo
湠,thuann
湧,ing
湯,thng
湳,lam
湳田,lam tshan
湯匙仔,thng si a
湯匙仔菜,thng si a tshai
測量,tshik liong
湠開,thuann khui
港路,kang loo
港墘,kang kinn
湠種,thuann tsing
湯頭,thng thau
測驗,tshik giam
焙,pue
焠,tshuh
無,bo
無,bu
焦,ta
煮,tsu
牌,pai
牚,thenn
犅,kang
猌,gin
猴,kau
猶,iau
無一定,bo it ting
無了時,bo liau si
無人緣,bo lang ian
牌子,pai tsu
猴山仔,kau san a
無大無細,bo tua bo se
無下落,bo he loh
無心肝,bo sim kuann
無心情,bo sim tsing
無天理,bo thinn li
無毋著,bo m tioh
猶毋過,iau m koh
犀牛,sai gu
無仝,bo kang
牌仔,pai a
無代無誌,bo tai bo tsi
無去,bo khi
無去,bo khi
無半步,bo puann poo
無可奈何,bu kho nai ho
無半絲,bo puann si
無半項,bo puann hang
無半撇,bo puann phiat
猶未,iau bue
無打緊, bo tann kin
猴囡仔,kau gin a
猶有,iau u
無尾巷,bo bue hang
無步,bo poo
無良心,bo liong sim
無事使,bo su sai
無依無倚,bo i bo ua
滋味,tsu bi
無奈,bo nai
無奈何,bo ta ua
無定著,bo tiann tioh
無拄好,bo tu ho
無所謂,bu soo ui
無法伊,bo huat i
無法度,bo huat too
無法無天,bu huat bu thian
無空,bo khang
無的確,bo tik khak
然後,jian au
猶是,iau si
無某無猴,bo boo bo kau
焦洗,ta se
無相干,bo siong kan
無限,bu han
無要無緊,bo iau bo kin
無要緊,bo iau kin
煮食,tsu tsiah
煮食裙仔,tsu tsiah kun a
猶原,iu guan
無差,bo tsha
焦料,ta liau
無氣,bo khui
無眠,bo bin
無神,bo sin
焙茶,pue te
無偌久,bo gua ku
無夠月,bo kau gueh
無啥物,bo siann mih
無夠重,bo kau tang
無啥貨,bo siann hue
無彩,bo tshai
無彩工,bo tshai kang
無張持,bo tiunn ti
無情,bo tsing
無望,bo bang
焦涸涸,ta khok khok
無細膩,bo se ji
無通,bo thong
無辜,bu koo
無量,bo liong
無閒,bo ing
無傳,bo thng
無愛,bo ai
無意中,bo i tiong
無意無思,bo i bo su
牌照,pai tsiau
無路,bo loo
無路用,bo loo ing
無路來,bo loo lai
無較縒,bo khah tsuah
無暝無日,bo me bo jit
無疑,bo gi
無疑悟,bo gi ngoo
無精差,bo tsing tsha
牚腿,thenn thui
猶閣,iau koh
猶閣咧,iau koh teh
猴齊天,kau tse thian
無影,bo iann
無影無跡,bo iann bo tsiah
無線電,bo suann tian
無論,bo lun
無銷,bo siau
滋養,tsu iong
無錯,bo tsho
牚頭,thenn thau
無頭神,bo thau sin
猴戲,kau hi
焦燥,ta so
無膽,bo tann
無聲無說,bo siann bo sueh
無講無呾,bo kong bo tann
無禮,bo le
焦鬆,ta sang
無礙著,bo gai tioh
牚懸,thenn kuan
無議量,bo gi niu
無鹹無纖,bo kiam bo siam
無攬無拈,bo lam bo ne
琴,khim
番,huan
畫,ue
痚,he
痟,siau
痠,sng
痣,ki
痧,sua
發,huat
發,puh
痟人,siau lang
痡心,poo sim
番仔,huan a
番仔火,huan a hue
番仔油,huan a iu
番仔幔,huan a mua
番仔樓,huan a lau
番仔薑,huan a kiunn
發出,huat tshut
發生,huat sing
發行,huat hing
發作,huat tsok
畫巡,ue sun
畫尪仔,ue ang a
發狂,huat kong
發角,huat kak
痚呴,he ku
痚呴嗽,he ku sau
發性地,huat sing te
痠抽疼,sng thiu thiann
發明,huat bing
痟狗,siau kau
發炎,huat iam
痟狗症,siau kau tsing
痟狗湧,siau kau ing
番社,huan sia
痟的,siau e
發芽,puh ge
發表,huat piau
痛苦,thong khoo
發展,huat tian
痠疼,sng thiann
發粉,huat hun
登記,ting ki
發起,huat khi
發動,huat tong
番婆,huan po
發現,huat hian
畫符仔,ue hu a
痟貪,siau tham
痠軟,sng nng
番麥,huan beh
發喙齒,huat tshui khi
發揚,huat iong
發揮,huat hui
琵琶,pi pe
痟痟,siau siau
番黍,huan se
發落,huat loh
番號,huan ho
痟話,siau ue
發達,huat tat
發粿,huat kue
發酵,huat kann
發燒,huat sio
發穎,huat inn
畫糖尪仔,ue thng ang a
番鴨,huan ah
發癀,huat hong
番薯,han tsi
番薑仔,huan kiunn a
番薯粉,han tsi hun
番薯箍,han tsi khoo
番薯簽,han tsi tshiam
番顛,huan tian
發願,huat guan
發覺,huat kak
睏,khun
短,te
短,tuan
硞,khok
硩,teh
硬,nge
硯,hinn
稅,sue
窗,tshong
窗,thang
童,tang
童,tong
短䘼,te ng
窗仔,thang a
窗仔門,thang a mng
窗仔框,thang a khing
童乩,tang ki
程序,thing su
短命,te mia
睏坦敧,khun than khi
稀奇,hi ki
硩定,teh tiann
睏房,khun pang
硬押,nge ah
硬拄硬,nge tu nge
硩枝,teh ki
稅金,sue kim
程度,thing too
硩扁,teh pinn
睏衫,khun sann
稅厝,sue tshu
硬氣,nge khi
睏眠,khun bin
硬迸迸,nge piang piang
硬骨,nge kut
硬掙,nge tsiann
睏晝,khun tau
短期,te ki
硞著,khok tioh
稀微,hi bi
短歲壽,te hue siu
硩落去,teh loh khi
短路,te loo
短銃,te tshing
硩嗽,teh sau
硬篤,nge tau
睏褲,khun khoo
短褲,te khoo
睏醒,khun tshenn
童謠,tong iau
硩驚,teh kiann
筅,tshing
筆,pit
等,tan
等,ting
筊,kiau
筋,kin
筍,sun
筐,khing
筒,tang
粞,tshe
粟,tshik
粧,tsng
結,kat
結,kiat
絕,tseh
絕,tsuat
絚,an
絞,ka
絨,jiong
絲,si
等一下,tan tsit e
結子,kiat tsi
筅仔,tshing a
筊仙,kiau sian
筍仔,sun a
筐仔,khing a
粟仔,tshik a
絨仔布,jiong a poo
筒仔米糕,tang a bi ko
絲仔襪,si a bueh
筊本,kiau pun
絕交,tsuat kau
結冰,kiat ping
結合,kiat hap
絞肉,ka bah
結局,kiat kiok
結束,kiat sok
筊岫,kiau siu
等於,ting i
筊東,kiau tong
結果,kiat ko
粟青,tshik tshenn
等咧,tan leh
等待,tan thai
結怨,kiat uan
結拜,kiat pai
粟倉,tshik tshng
等候,tan hau
結冤,kiat uan
答案,tap an
結案,kiat an
絕氣,tsuat khui
筊鬼,kiau kui
筋骨,kin kut
筍乾,sun kuann
絕情,tsuat tsing
絕望,tsuat bong
結趼,kiat lan
答喙鼓,tap tshui koo
筋絡,kin le
筍絲,sun si
紫菜,tsi tshai
筊間,kiau king
筋節,kin tsat
筆跡,pit tsik
筊跤,kiau kha
等路,tan loo
絕路,tsuat loo
結實,kiat sit
絕對,tsuat tui
結算,kiat sng
絕種,tseh tsing
結綵,kat tshai
結數,kiat siau
結論,kiat lun
急燒仔,kip sio a
結親,kiat tshin
答應,tah ing
紫檀,tsi tuann
結穗,kiat sui
答謝,tap sia
翕,hip
翕,hip
脹,tiong
脹,tiunn
脾,pi
腎,sin
腔,khiunn
舒,tshu
菇,koo
脾土,pi thoo
腔口,khiunn khau
菁仔,tshenn a
菁仔欉,tshenn a tsang
翕死,hip si
脹肚,tiunn too
菅芒,kuann bang
翕豆菜,hip tau tshai
翕相,hip siong
翕相機,hip siong ki
翕相館,hip siong kuan
脾胃,pi ui
莿桐,tshi tong
脹氣,tiunn khi
脾氣,phi khi
脹胿,tiunn kui
菅草,kuann tshau
舒被,tshu phue
菅蓁,kuann tsin
翕熱,hip juah
翕甌,hip au
肅靜,siok tsing
脹膿,tiunn lang
腌臢,a tsa
菊,kiok
菜,tshai
萎,ui
菜刀,tshai to
菜子,tshai tsi
菜子油,tshai tsi iu
菜心,tshai sim
菝仔,puat a
菝仔票,pat a phio
菜包,tshai pau
菜市仔,tshai tshi a
菜瓜,tshai kue
菜瓜布,tshai kue poo
菜瓜摖,tshai kue tshe
菜瓜蒲,tshai kue poo
菜尾,tshai bue
菜豆,tshai tau
菱角,ling kak
菜姑,tshai koo
菜底,tshai te
菜店,tshai tiam
菜店查某,tshai tiam tsa boo
菜油,tshai iu
菊花,kiok hue
菜花,tshai hue
菜架仔,tshai ke a
菜桌,tshai toh
菜配,tshai phue
菜堂,tshai tng
菜脯,tshai poo
菜脯米,tshai poo bi
菜脯簽,tshai poo tshiam
菜鳥仔,tshai tsiau a
菜單,tshai tuann
菩提樹,phoo the tshiu
菜湯,tshai thng
菜園,tshai hng
菜粽,tshai tsang
菖蒲,tshiong poo
菜蔬,tshai se
菜燕,tshai ian
菜頭,tshai thau
菜館,tshai kuan
菜頭粿,tshai thau kue
菜鴨,tshai ah
菠薐仔,pue ling a
菜擴,tshai khok
菩薩,phoo sat
菜蟳,tshai tsim
菜櫥,tshai tu
菜礤,tshai tshuah
菜籃,tshai na
著,tioh
著,toh
虛,hi
街,ke
裁,tshai
裂,liah
裂,lih
覕,bih
訴,soo
裁刀,tshai to
視力,si lik
著水蛆,tioh tsui tshi
著火,toh hue
虛火,hi hue
蛤仔,kap a
街仔,ke a
街仔路,ke a loo
街市,ke tshi
著生驚,tioh tshenn kiann
裁決,tshai kuat
著災,tioh tse
診所,tsin soo
訴狀,soo tsng
覕雨,bih hoo
著咳嗾,tioh ka tsak
著急,tioh kip
覕相揣,bih sio tshue
虛弱,hi jiok
著時,tioh si
著病,tioh penn
覕喙,bih tshui
著寒熱仔,tioh kuann jiat a
著猴,tioh kau
著痧,tioh sua
虛華,hi hua
裂開,lih khui
著傷,tioh siong
著賊偷,tioh tshat thau
著銃,tioh tshing
診察,tsin tshat
著頭,tioh thau
街頭,ke thau
蛟龍,kau liong
裁縫,tshai hong
裁縫店,tshai hong tiam
診斷,tsin tuan
著蟲,tioh thang
著驚,tioh kiann
註,tsu
詈,le
評,phing
詞,su
象,tshiunn
貯,te
貴,kui
貶,pian
買,be
買,mai
貺,hing
費,hui
貼,tah
貼,thiap
貿,bau
趁,than
越,uat
貴人,kui jin
貼人食,thiap lang tsiah
貿工,bau kang
貼心,tah sim
註冊,tsu tsheh
買主,be tsu
貼本,thiap pun
費用,hui iong
超生,tshiau sing
註生娘娘,tsu senn niu niu
註好好,tsu ho ho
註死,tsu si
買收,be siu
趁早,than tsa
評判,phing phuann
趁私奇,than sai khia
買命,be mia
註定,tsu tiann
貼底,tah te
貴庚,kui kenn
註明,tsu bing
貿易,boo ik
超度,tshiau too
趁流水,than lau tsui
貴重,kui tiong
趁食,than tsiah
趁食人,than tsiah lang
趁食查某,than tsiah tsa boo
趁食間,than tsiah king
貴氣,kui khi
費氣,hui khi
費氣費觸,hui khi hui tak
費神,hui sin
超級,tshiau kip
貴參參,kui som som
象桮,siunn pue
買票,be phio
象棋,tshiunn ki
詐欺,tsa khi
貸款,tai khuan
貼貼,tah tah
貯飯,te png
註解,tsu kai
超過,tshiau kue
貴賓,kui pin
評論,phing lun
買賣,be be
註銷,tsu siau
趁燒,than sio
趁錢,than tsinn
貿頭,bau thau
越頭,uat thau
跋,puah
跍,khu
跑,phau
跔,ku
跙,tshu
跛,pai
進,tsin
跙一倒,tshu tsit to
進口,tsin khau
鄉土,hiong thoo
進化,tsin hua
郵件,iu kiann
進行,tsin hing
郵局,iu kiok
鄉村,hiong tshun
進步,tsin poo
鄉里,hiunn li
鄉長,hiong tiunn
郵便局,iu pian kiok
進前,tsin tsing
郵政,iu tsing
辜負,koo hu
進香,tsin hiunn
跋倒,puah to
跙倒,tshu to
郵差,iu tshai
進退,tsin the
跑馬,phau be
跋桮,puah pue
郵票,iu phio
跋牌仔,puah pai a
跋筊,puah kiau
郵筒,iu tang
跛跤,pai kha
鄉親,hiong tshin
鄉鎮,hiong tin
酥,soo
量,liong
量,liong
量,niu
量,niu
鈃,giang
鈍,tun
鈍,tun
鈍,tun
鈕,liu
開,khai
開,khui
閏,jun
閒,ing
間,kan
間,king
陽,iong
隊,tui
鈍刀,tun to
開刀,khui to
閒人,ing lang
開口,khai khau
閒工,ing kang
閏月,jun gueh
量仔,niu a
鈃仔,giang a
鈕仔,liu a
鈗仔,ng a
間仔,king a
閒仙仙,ing sian sian
鈕仔空,liu a khang
閒仔話,ing a ue
開市,khui tshi
開正,khui tsiann
開用,khai ing
隊伍,tui ngoo
開車,khui tshia
量其約,liong ki iok
開拆,khui thiah
開放,khai hong
開花,khui hue
隊長,tui tiunn
開查某,khai tsa boo
開面,khui bin
隊員,tui uan
開桌,khui toh
開破,khui phua
開基,khai ki
開基祖,khai ki tsoo
開張,khai tiong
開喙,khui tshui
開單,khui tuann
開發,khai huat
開脾,khui pi
開開,khui khui
開開,khui khui
閒間,ing king
鈕鈕仔,liu liu a
開會,khui hue
開業,khai giap
酥腰,soo io
開跤褲,khui kha khoo
開路,khui loo
開幕,khai boo
開裾,khui ki
開價,khui ke
開盤,khui puann
開銷,khai siau
開墾,khai khun
開學,khai hak
陽曆,iong lik
開錢,khai tsinn
閒錢,ing tsinn
開臊,khui tsho
開講,khai kang
開闊,khui khuah
開竅,khui khiau
開藥仔,khui ioh a
開關,khai kuan
雁,gan
雄,hing
雄,hiong
集,tsip
雲,hun
韌,jun
項,hang
順,sun
飫,ui
飯,png
飲,im
黃,ng
黍,se
飯丸,png uan
集中,tsip tiong
順手,sun tshiu
順月,sun gueh
飯斗,png tau
黃牛,ng gu
黍仔,se a
飯包,png pau
項目,hang bok
集合,tsip hap
黃色,ng sik
順利,sun li
雲尪,hun ang
順序,sun si
飯杓,png siah
飯疕,png phi
黃豆,ng tau
飯坩,png khann
飯店,png tiam
黃昏,hong hun
黃昏市仔,hong hun tshi a
黃金,ng kim
階段,kai tuann
黃泉,hong tsuan
順風,sun hong
順風耳,sun hong ni
雅氣,nga khi
黃疸,ng than
階級,kai kip
黃酒,ng tsiu
飯匙,png si
飯匙骨,png si kut
飯匙銃,png si tshing
順從,sun tsiong
飯桶,png thang
順眼,sun gan
飯盒仔,png ah a
順紲,sun sua
黃連,ng ni
黃魚,ng hi
飫喙,ui tshui
飯湯,png thng
飯菜,png tshai
雅量,nga liong
雄雄,hiong hiong
雄黃,hiong hong
雄黃酒,hiong hong tsiu
順勢,sun se
飯碗,png uann
順路,sun loo
飯頓,png tng
集團,tsip thuan
黃酸,ng sng
飯篋仔,png kheh a
黃錦錦,ng gim gim
飯篱,png le
頇顢,han ban
亂,luan
催,tshui
傱,tsong
傳,thng
傳,thuan
債,tse
傷,siong
傷,siunn
剷,thuann
剺,leh
剺,li
剾,khau
剿,tsau
募,boo
勢,se
勢,si
勥,khiang
匯,hue
嗄,sa
剾刀,khau to
勢力,se lik
剾刀花,khau to hue
傷口,siong khau
傷心,siong sim
傷天害理,siong thian hai li
亂世,luan se
債主,tse tsu
剾仔,khau a
傷本,siong pun
催生,tshui sing
剾皮,khau phue
剺肚,leh too
亂使,luan su
亂來,luan lai
債券,tse kng
剾削,khau siah
傳後嗣,thng hio su
傳染,thuan jiam
剾洗,khau se
傷重,siong tiong
剾風,khau hong
勢面,se bin
傷風敗俗,siong hong pai siok
傷害,siong hai
募捐,boo kuan
剺破,li phua
剷草,thuann tshau
債務,tse bu
勤務,khin bu
傳授,thuan siu
傷痕,siong hun
傳票,thuan phio
匯票,hue phio
募集,boo tsip
傷腦筋,siong nau kin
傷跡,siong jiah
勥跤,khiang kha
傳種,thng tsing
勤儉,khin khiam
亂彈,lan than
亂操操,luan tshau tshau
傱錢,tsong tsinn
勢頭,se thau
亂講,luan kong
亂鐘仔,luan tsing a
債權,tse khuan
嗙,phngh
嗚,onn
園,hng
圓,inn
塊,te
塌,thap
塔,thah
塗,thoo
塚,thiong
塞,sat
填,thiam
塭,un
塚山,thiong suann
塗水,thoo tsui
塗水師,thoo tsui sai
圓仔,inn a
塭仔,un a
圓仔花,inn a hue
塚仔埔,thiong a poo
圓仔湯,inn a thng
圓仔粞,inn a tshe
塌本,thap pun
填本,thiam pun
塗色,thoo sik
塗尪仔,thoo ang a
塗沙,thoo sua
塗豆,thoo tau
塗豆仁,thoo tau jin
塗豆油,thoo tau iu
塗豆糖,thoo tau thng
嗚呼,oo hoo
塌底,lap te
塌空,thap khang
塗虱,thoo sat
塗炭,thoo thuann
塗墼,thoo kat
塗墼厝,thoo kat tshu
塗捀,thoo phang
圓栱門,uan kong mng
填海,thiam hai
塗粉,thoo hun
圓圓,inn inn
塌落,lap loh
塌跤,thap kha
塗跤,thoo kha
圓滿,uan buan
圓箍仔,inn khoo a
嗤舞嗤呲,tshi bu tshih tshu
塗魠,thoo thoh
塞鼻,sat phinn
塑膠,sok ka
塑膠桶,sok ka thang
塑膠袋仔,sok ka te a
塌錢,thap tsinn
塗龍,thoo liong
圓環,inn khuan
塗礱,thoo lang
媽,ma
嫁,ke
嫂,so
嫌,hiam
幌,hainn
嫁查某囝,ke tsa boo kiann
媽祖,ma tsoo
嫁翁,ke ang
嫁娶,ke tshua
嫁粧,ke tsng
媽媽,ma mah
嫌疑,hiam gi
幌頭仔,hainn thau a
幌韆鞦,hainn tshian tshiu
幹,kan
想,siong
想,siunn
惹,jia
愁,tshiu
愈,ju
意,i
愛,ai
感,kam
戥,ting
揫,tshiu
愛人仔,ai jin a
感化,kam hua
感心,kam sim
戥仔,ting a
惹代誌,jia tai tsi
意外,i gua
意向,i hiong
意志,i tsi
意見,i kian
幹事,kan su
惹事,jia su
想東想西,siunn tang siunn sai
想空想縫,siunn khang siunn phang
感冒,kam moo
意思,i su
感染,kam jiam
慎重,sin tiong
愛哭,ai khau
感恩,kam un
意氣,i khi
感動,kam tong
愛情,ai tsing
感情,kam tsing
慈善,tsu sian
愛媠,ai sui
慈悲,tsu pi
愛睏,ai khun
愛睏藥仔,ai khun ioh a
感著,kam tioh
意愛,i ai
感想,kam siong
慈愛,tsu ai
微微仔,bi bi a
慄慄掣,lak lak tshuah
意義,i gi
愛嬌,ai kiau
感激,kam kik
感應,kam ing
感謝,kam sia
意願,i guan
感覺,kam kak
意麵,i mi
損,sng
損,sun
搐,tiuh
搖,io
搙,jiok
搜,tshiau
搝,khiu
搟,hian
搢,tsinn
搣,me
搤,iah
浞,tshiok
搦,lak
搧,sam
搧,sian
搩,kiat
搪,tng
搬,puann
搭,tah
搵,un
搶,tshiunn
摃,kong
敬,king
斟,thin
新,sin
新人,sin lang
搧大耳,sian tua hinn
搝大索,khiu tua soh
搖手,io tshiu
搵水,un tsui
損失,sun sit
新正,sin tsiann
新年,sin ni
搶劫,tshiunn kiap
搖尾,io bue
搵豆油,un tau iu
搜身軀,tshiau sin khu
新奇,sin ki
搶孤,tshiunn koo
搭油,tah iu
搤空,iah khang
搦屎搦尿,lak sai lak jio
新春,sin tshun
搭架,tah ke
敬重,king tiong
新郎,sin long
搢風,tsinn hong
搧風,sian hong
搬厝,puann tshu
新娘,sin niu
新娘房,sin niu pang
損害,sun hai
損神,sng sin
斟茶,thin te
敬酒,king tsiu
斟酌,tsim tsiok
斟酒,thin tsiu
搢做前,tsinn tso tsing
新婚,sin hun
新婦,sin pu
新婦仔,sin pu a
搬徙,puann sua
搖笱,io ko
搧喙䫌,sian tshui phue
新款,sin khuan
搪著,tng tioh
新進,sin tsin
損傷,sun siong
搝搝搦搦,khiu khiu lak lak
搬話,puann ue
搬運,puann un
搭鉤仔,tah kau a
搖鼓瑯,io koo long
摃槌仔,kong thui a
新聞,sin bun
搬請,puann tshiann
新曆,sin lik
新興,sin hing
損蕩,sng tng
搖頭,io thau
搶頭香,tshiunn thau hiunn
搶頭標,tshiunn thau pio
摃龜,kong ku
搭嚇,tah hiannh
搬戲,puann hi
新鮮,sin sian
新點點,sin tiam tiam
搖櫓,io loo
搖籃,io na
摃鐘,kong tsing
搦權,lak khuan
暗,am
會,e
會,hue
椰,ia
楓,png
楔,seh
楗,king
楞,gong
楠,lam
楦,hun
業,giap
椰子,ia tsi
暗中,am tiong
楔手縫,seh tshiu phang
會仔,hue a
楓仔,png a
楠仔,lam a
楬仔,at a
楓仔樹,png a tshiu
暗示,am si
會用得,e ing tit
暗光鳥,am kong tsiau
會合,hue hap
會同,hue tong
暗色,am sik
暗行,am hing
暗步,am poo
會使,e sai
會使得,e sai tit
會社,hue sia
楔空,seh khang
楔後手,seh au tshiu
會計,kue ke
暗崁,am kham
暗時,am si
楊桃,iunn to
暗班,am pan
暗眠摸,am bin bong
會做得,e tso tit
業務,giap bu
業務員,giap bu uan
會得,e tit
會得通,e tit thang
暗殺,am sat
暗淡,am tam
暗訪,am hong
暗袋仔,am te a
會場,hue tiunn
會堪得,e kham tit
暗間仔,am king a
暗飯,am png
業債,giap tse
會當,e tang
暗號,am ho
暗路,am loo
暗頓,am tng
暗暝,am me
暗漠漠,am bok bok
暗趖趖,am so so
暗毿,am sam
暗毿病,am sam penn
暗學仔,am oh a
會曉,e hiau
會頭,hue thau
會館,hue kuan
暗頭仔,am thau a
楔縫,seh phang
會議,hue gi
歁,kham
歇,hioh
歲,hue
歲,sue
毀,hui
準,tsun
溜,liu
溝,kau
溡,tshi
溢,ik
溪,khe
歇工,hioh kang
概尺,kai tshioh
楹仔,enn a
溝仔,kau a
溪仔,khe a
溪仔墘,khe a kinn
歇冬,hioh tang
溢奶,ik ling
溢刺酸,ik tshiah sng
準拄好,tsun tu ho
溫柔,un jiu
溫泉,un tsuann
溪哥仔,khe ko a
溪埔,khe poo
準時,tsun si
準做,tsun tso
歇晝,hioh tau
溫習,un sip
準備,tsun pi
歇喘,hioh tshuan
歇寒,hioh kuann
歇睏,hioh khun
歇暗,hioh am
溫暖,un luan
歁歁,kham kham
溪溝,khe kau
歁話,kham ue
溫馴,un sun
歲壽,hue siu
歇暝,hioh me
極端,kik tuan
準算,tsun sng
歇熱,hioh juah
概論,kai lun
歲頭,hue thau
歁頭歁面,kham thau kham bin
流籠,liu long
溫罐,un kuan
溶,iunn
滅,biat
滇,tinn
滑,kut
滒,ko
滓,tai
煎,tsian
煎,tsuann
煏,piak
煙,ian
煞,suah
煞,sannh
煠,sah
煡,khit
滅亡,biat bong
煞心,sannh sim
煙火,ian hue
煙仔魚,ian a hi
煞去,suah khi
煞尾,suah bue
煏油,piak iu
煏空,piak khang
滑倒,kut to
煏桌,piak toh
煞神,suah sin
煎茶,tsuann te
煎匙,tsian si
煙筒,ian tang
煞著,suah tioh
滑溜溜,kut liu liu
煙腸,ian tshiang
煞鼓,suah koo
煙黗,ian thun
煞戲,suah hi
煎藥仔,tsuann ioh a
照,tsiau
照,tsio
煨,ue
煩,huan
爺,ia
獅,sai
獅仔鼻,sai a phinn
照步來,tsiau poo lai
照呼照行,tsiau hoo tsiau kiann
照起工,tsiau khi kang
照常,tsiau siong
煩惱,huan lo
照實,tsiau sit
照辦,tsiau pan
照講,tsiau kong
照鏡,tsio kiann
照顧,tsiau koo
當,tng
當,tng
痰,tham
痲,mua
盞,tsuann
睨,gin
矮,e
矮人,e lang
痱仔,pui a
痱仔粉,pui a hun
當地,tong te
當年,tong ni
當事人,tong su jin
當初,tong tshoo
當店,tng tiam
矮肥,e pui
當咧,tng teh
硼砂,phing se
當面,tng bin
當值,tong tit
痴哥,tshi ko
痴哥神,tshi ko sin
當時,tang si
當時,tong si
痴迷,tshi be
當做,tong tso
痴情,tshi tsing
當票,tng phio
當場,tong tiunn
痰壺,tham oo
當然,tong jian
督學,tok hak
當選,tong suan
當頭白日,tng thau peh jit
當頭對面,tng thau tui bin
當歸,tong kui
痰瀾,tham nua
痰罐,tham kuan
碇,tiann
碌,lik
碎,tshui
碑,pi
碗,uann
碰,pong
禁,kim
稗,phe
稜,ling
稟,pin
窟,khut
碗公,uann kong
碗斗,uann tau
禁止,kim tsi
稗仔,phe a
窟仔,khut a
稟告,pin ko
禁忌,kim khi
窞肚,tham too
禁氣,kim khui
碰釘,phong ting
禁屠,kim too
禁喙,kim tshui
碌硞馬,lok khok be
碗箸,uann ti
碗粿,uann kue
碗盤,uann puann
碎糊糊,tshui koo koo
碰壁,pong piah
碗糕,uann ko
碗頭仔,uann thau a
禽獸,khim siu
筧,king
筧,khio
節,tsat
節,tseh
節,tsiat
絹,kin
經,kenn
經,king
罨,am
罩,ta
罩,tau
罪,tsue
群,kun
義,gi
節力,tsat lat
罪人,tsue jin
義子,gi tsu
節日,tseh jit
節目,tsiat bok
節育,tsiat iok
節制,tsiat tse
節省,tsiat sing
節約,tsiat iok
罩衫,ta sann
節氣,tseh khui
義氣,gi khi
節脈,tsat meh
經商,king siong
義務,gi bu
經理,king li
義理,gi li
綁票,pang phio
罪惡,tsue ok
經期,king ki
經絲,kenn si
經費,king hui
罪業,tsue giap
經跤經手,kenn kha kenn tshiu
經過,king kue
罪過,tsue ko
罪過,tse kua
罩雺,ta bong
節儉,tsiat khiam
經線,kenn suann
經歷,king lik
經濟,king tse
經營,king ing
罩霧,ta bu
經驗,king giam
聖,siann
聘,phing
腡,le
腦,nau
腫,tsing
腰,io
腸,tng
腹,pak
舅,ku
萬,ban
落,lak
落,lau
落,loh
落,loh
落,lok
落䈄,lau ham
萬一,ban it
腦力,nau lik
落人的喙,loh lang e tshui
腰子,io tsi
腱子肉,kian tsi bah
落山風,loh suann hong
腰子病,io tsi penn
落下頦,lau e hai
腹內,pak lai
舅公,ku kong
落勾,lau kau
腰內肉,io lai bah
萬不得已,ban put tik i
腰尺,io tshioh
落手,loh tshiu
落水,loh tsui
腸仔,tng a
舅仔,ku a
萬世,ban se
萬代,ban tai
腸仔𣻸,tng a siunn
腸仔炎,tng a iam
舅仔探房,ku a tham pang
萵仔菜,ue a tshai
腸仔熱,tng a jiat
落去,loh khi
聖母,sing bo
落本,loh pun
萬全,ban tsuan
落伍,lok ngoo
落吐症,lau thoo tsing
萬年筆,ban lian pit
聖旨,sing tsi
落成,lok sing
落色,lak sik
落尾,loh bue
落尾手,loh bue tshiu
落杓,lau siah
腸肚,tng too
腹肚,pak too
腹肚尾,pak too bue
腹肚枵,pak too iau
落車,loh tshia
萬事,ban su
落來,loh lai
萬幸,ban hing
聖拄聖,siann tu siann
萬物,ban but
落注,loh tu
落空逝,lau khang tsua
落肥,loh pui
聘金,phing kim
落雨,loh hoo
落雨天,loh hoo thinn
落南,loh lam
落屎,lau sai
落屎星,lau sai tshenn
落屎馬,lau sai be
落後日,loh au jit
落後年,loh au ni
落昨日,loh tsoh jit
落胎,lau the
落風,lau hong
聘書,phing su
落氣,lau khui
落眠,loh bin
萬能,ban ling
萬般,ban puann
腰脊骨,io tsiah kut
落衰,loh sue
腰骨,io kut
腰帶,io tua
落崎,loh kia
腰桶,io thang
落第,lok te
落船,loh tsun
落軟,loh nng
腦貧血,nau pin hiat
落雪,loh seh
落喉,loh au
落湳,loh lam
萬無一失,ban bu it sit
腦筋,nau kin
落跑,lau phau
萬項,ban hang
落塗,loh thoo
聖經,sing king
萬萬,ban ban
落落,lau lau
落葬,loh tsong
落跤氣,loh kha khi
落價,loh ke
腳數,kioh siau
腦膜炎,nau mooh iam
聘請,phing tshiann
落魄,lok phik
落褲,lau khoo
落選,lok suan
腫頷,tsing am
腥臊,tshenn tshau
落臉,lak lian
落翼仔,lau sit a
落霜,loh sng
聘禮,phing le
落難,loh lan
腦髓,nau tshue
葉,hioh
葩,pha
葬,tsong
蒂,ti
號,ho
葉仔,hioh a
號名,ho mia
董事,tang su
葵扇,khue sinn
號做,ho tso
瓜笠仔,kue leh a
葡萄,phu to
葡萄酒,phu to tsiu
號碼,ho be
葫蘆,hoo loo
蜂,phang
裒,poo
裘,hiu
裙,kun
補,poo
裝,tsng
裝,tsong
裡,li
裡, li
解,kai
試,tshi
詩,si
解厄,kai eh
解心悶,kai sim bun
蛾仔,iah a
蜊仔,la a
裘仔,hiu a
補充,poo tshiong
補冬,poo tang
補血,poo hueh
補助,poo tsoo
解決,kai kuat
蜂岫,phang siu
衙門,ge mng
解毒,kai tok
試看,tshi khuann
試看覓,tshi khuann mai
解約,kai iok
詭計,kui ke
補破網,poo phua bang
蜈蚣,gia kang
解酒,kai tsiu
解除,kai tu
試探,tshi tham
補添,poo thiam
補紩,poo thinn
補習,poo sip
解脫,kai thuat
補喙齒,poo tshui khi
解圍,kai ui
解悶,kai bun
解散,kai san
裝痟的,tsng siau e
解答,kai tap
補貼,poo thiap
解愁,kai tshiu
裌裘,kiap hiu
詬詬唸,kau kau liam
補運,poo un
補運錢,poo un tsinn
補鼎,poo tiann
詩歌,si kua
蜂蜜,phang bit
蜈蜞,ngoo khi
蜈蜞釘,ngoo khi ting
解說,kai sueh
裝潢,tsong hong
補藥,poo ioh
解釋,kai sik
試鹹汫,tshi kiam tsiann
試驗,tshi giam
話,ue
該,kai
詼,khue
誠,tsiann
賊,tshat
趒,tio
跟,kin
跡,jiah
跤,kha
跩,tsuainn
跪,kui
跤刀,kha to
誇口,khua khau
跤手,kha tshiu
跤斗,kha tau
跤爪,kha jiau
賊仔,tshat a
跤仔,kha a
賊仔市,tshat a tshi
賊仔貨,tshat a hue
話母,ue bo
資本,tsu pun
跤目,kha bak
跤尖手幼,kha tsiam tshiu iu
該死,kai si
跤曲,kha khiau
話尾,ue bue
跤尾,kha bue
跤尾飯,kha bue png
跤步,kha poo
跤肚,kha too
跤肚骨,kha too kut
跤來手來,kha lai tshiu lai
跤帛,kha peh
跤底,kha te
話蝨,ue sat
畫虎𡳞,ue hoo lan
話屎,ue sai
跪拜,kui pai
跤後肚,kha au too
跤後蹬,kha au tenn
跤指頭仔,kha tsing thau a
話柄,ue penn
跤枷,kha ke
資料,tsu liau
資格,tsu keh
跤胴骨,kha tang kut
話骨,ue kut
跤骨,kha kut
跤兜,kha tau
詳情,siong tsing
跤桶,kha thang
跤梢,kha sau
跤液,kha sioh
跤梢間仔,kha sau king a
跤球,kha kiu
資產,tsu san
詳細,siong se
賊船,tshat tsun
該然,kai jian
跤筋,kha kin
誠意,sing i
該當,kai tong
跤跡,kha jiah
趒跤頓蹄,tio kha tng te
誠實,tsiann sit
誠實,sing sit
跟綴,kin tue
跤腿,kha thui
跤鼻臁,kha phinn liam
跤數,kha siau
跤模,kha boo
跤模手印,kha boo tshiu in
跤盤,kha puann
跤踏仔,kha tah a
跤踏車,kha tah tshia
跤擋,kha tong
跤蹄,kha te
跟隨,kin sui
話頭,ue thau
賊頭,tshat thau
跤頭趺,kha thau u
誠懇,sing khun
話縫,ue phang
跤縫,kha phang
路,loo
跳,thiau
較,kah
較,khah
載,tsai
載,tsainn
農,long
逼,pik
遇,gu
遊,iu
運,un
遍,pian
過,ko
過,kue
遏,at
遐,hia
遐,hiah
道,to
道士,to su
較大面,khah tua bin
過分,kue hun
跳水,thiau tsui
過心,kue sim
過戶,kue hoo
過手,kue tshiu
過日,kue jit
過水,kue tsui
道友,to iu
違反,ui huan
遏手把,at tshiu pa
過火,kue hue
較加,khah ke
過去,kue khi
跳加冠,thiau ka kuan
農民,long bin
過失,kue sit
農民曆,long bin lik
路用,loo ing
運用,un iong
過目,kue bak
過名,kue mia
跳年,thiau ni
過年,kue ni
較早,khah tsa
道行,to hing
農作物,long tsok but
較快,khah khuai
農村,long tshun
路沖,loo tshiong
較車,ka tshia
過身,kue sin
農具,long ku
運命,un mia
過往,kue ong
過房,kue pang
運河,un ho
遏泔,at am
遐的,hia e
過門,kue mng
過度,kue too
過後,kue au
違背,ui pue
過面,kue bin
過時,kue si
路旁屍,loo pong si
運氣,un khi
過氣,kue khui
跳索仔,thiau soh a
運送,un sang
跳針,thiau tsiam
較停仔,khah thing a
運動,un tong
運動埕,un tong tiann
運動會,un tong hue
道教,to kau
道理,to li
路祭,loo tse
路途,loo too
跳逝,thiau tsua
運途,un too
過喙,kue tshui
農場,long tiunn
過渡,kue too
跳港,thiau kang
路程,loo ting
跳童,thiau tang
遇著,gu tioh
路費,loo hui
過意,kue i
農業,long giap
道義,to gi
道路,to loo
遐爾,hiah ni
遐爾仔,hiah ni a
跳舞,thiau bu
道德,to tik
過數,kue siau
過磅,kue pong
過橋,kue kio
路燈,loo ting
較輸,khah su
運輸,un su
路頭,loo thau
過頭,kue thau
較講,khah kong
過謙,koo khiam
運轉,un tsuan
運轉手,un tsuan tshiu
路邊,loo pinn
路邊擔仔,loo pinn tann a
過爐,kue loo
遊覽車,iu lam tshia
過癮,kue gian
逼籤詩,pik tshiam si
鈴,ling
鈷,koo
鉎,sian
鉗,khinn
鉛,ian
鉤,kau
銃,tshing
閘,tsah
鉛子,ian tsi
銃子,tshing tsi
銃手,tshing tshiu
閘日,tsah jit
鈴仔,ling a
鉗仔,khinn a
鉤仔,kau a
閘光,tsah kng
鉤耳,kau hinn
閘車,tsah tshia
銃空,tshing khang
閘屏,tsah pin
閘風,tsah hong
鉛桶,ian thang
銃殺,tshing sat
鉛筆,ian pit
鉛筆絞仔,ian pit ka a
鉛筆剾,ian pit khau
閘路,tsah loo
鉛鉼,ian phiann
鉛線,ian suann
隔,keh
雷,lui
雹,phauh
雺,bong
電,tian
靴,hia
頓,tng
飼,tshi
飽,pa
髡,khun
電力,tian lik
電子,tian tsu
雷公,lui kong
飽仁,pa jin
雷公性,lui kong sing
隔日,keh jit
頓手,tun tshiu
飽水,pa tsui
電火,tian hue
電火布,tian hue poo
電火泡仔,tian hue phok a
電火柱,tian hue thiau
電火球仔,tian hue kiu a
飼奶,tshi ling
電光,tian kong
頓印,tng in
電冰箱,tian ping siunn
隔年,keh ni
電池,tian ti
飽呃,pa eh
電車,tian tshia
飽足,pa tsiok
電信,tian sin
電信局,tian sin kiok
零星,lan san
零星錢,lan san tsinn
飼查某,tshi tsa boo
隔界,keh kai
電風,tian hong
飼料,tshi liau
電氣,tian khi
飽眠,pa bin
電梯,tian thui
預備,i pi
電報,tian po
頓椅頓桌,tng i tng toh
飽脹,pa tiunn
電視,tian si
隔開,keh khui
隔間,keh king
電塗,tian thoo
飽滇,pa tinn
隔腹,keh pak
電腦,tian nau
電話,tian ue
電鈴,tian ling
隔暝,keh me
電影,tian iann
電影戲園,tian iann hi hng
電線,tian suann
隔壁,keh piah
飽膭,pa kui
電錶,tian pio
電頭毛,tian thau mng
電頭鬃店,tian thau tsang tiam
頓龜,tng ku
飽穗,pa sui
電鍋,tian ko
隔轉工,keh tng kang
隔轉日,keh tng jit
隔轉年,keh tng ni
雉雞,thi ke
雺霧,bong bu
電爐,tian loo
電罐,tian kuan
鼎,tiann
鼓,koo
鼠,tshi
鼓井,koo tsenn
鼎仔,tiann a
鼓仔燈,koo a ting
鼓吹,koo tshue
鼓吹,koo tshui
鼓吹花,koo tshue hue
鼎疕,tiann phi
鼎崁,tiann kham
鼎摖,tiann tshe
鼓槌,koo thui
鼎蓋,tiann kua
鼓勵,koo le
鼎邊趖,tiann pinn so
鼠麴草,tshi khak tshau
鼠麴粿,tshi khak kue
像,tshiunn
像,siong
僥,hiau
僫,oh
劃,ueh
厭,ia
嗽,sau
嗾,tsak
呲,tshu
嘆,than
嘔,au
嘖, tsheh
嘛,ma
嘛, mah
厭𤺪,ia sian
僥心,hiau sim
嘔心血,au sim hiat
嘔血,au hueh
僭位,tsiam ui
嘛是,ma si
嘔紅,au hong
僥倖,hiau hing
僥倖錢,hiau hing tsinn
厭氣,ian khi
僫做,oh tso
嘛欲,ma beh
嘓魚,khok hi
嗾著,tsak tioh
僭話,tsiam ue
嘛嘛吼,ma ma hau
嘈嘈滴,tshauh tshauh tih
嘐潲,hau siau
嘐潲話,hau siau ue
嘉獎,ka tsiong
僫講,oh kong
嘉鱲,ka lah
圖,too
團,thuan
境,king
墊,tiam
墓,bong
墘,kinn
壽,siu
夢,bang
夢,bong
奪,tuat
墓仔埔,bong a poo
墓地,bong te
壽衣,siu i
壽命,siu mia
壽板,siu pan
壽金,siu kim
嫖客,phiau kheh
境界,king kai
夥計,hue ki
墓埕,bong tiann
嫦娥,siong ngoo
圖書,too su
圖書館,too su kuan
墓牌,bong pai
團結,thuan kiat
團圓,thuan inn
墓龜,bong ku
壽龜,siu ku
墓壙,bong khong
孵,pu
寡,kua
實,tsat
實,sit
寨,tse
對,tui
對,ui
幔,mua
幕,boo
廕,im
實力,sit lik
對分,tui pun
對不住,tui put tsu
對反,tui huan
對手,tui tshiu
寧可,ling kho
對半,tui puann
對立,tui lip
實在,sit tsai
實地,sit te
對年,tui ni
實行,sit hing
孵卵,pu nng
對抗,tui khong
對沖,tui tshiong
孵岫,pu siu
對拄,tui tu
對拗,tui au
寢室,tshim sik
對待,tui thai
實施,sit si
對指,tui tsi
對看,tui khuann
對面,tui bin
對時,tui si
寡婦,kua hu
實情,sit tsing
實現,sit hian
實習,sit sip
對喙,tui tshui
對換,tui uann
對答,tui tap
對策,tui tshik
對象,tui siong
對照,tui tsiau
實腹,tsat pak
實話,sit ue
實際,sit tse
實鼻,tsat phinn
實價,sit ke
對數,tui siau
對調,tui tiau
實踐,sit tsian
對頭,tui thau
孵膿,pu lang
對襟仔,tui khim a
對襟仔衫,tui khim a sann
實櫼,tsat tsinn
實驗,sit giam
慒,tso
慘,tsham
慢,ban
摔,siak
摔,siang
摖,tshe
摘,tiah
摠,tsang
摧,tshui
慒心,tso sim
慢火,ban hue
慢且,ban tshiann
慢且是,ban tshiann si
慢冬,ban tang
慢行,ban kiann
慢車,ban tshia
慢性,ban sing
態度,thai too
摔倒,siak to
摔桶,siak thang
慷慨,khong khai
摔粟,siak tshik
慣勢,kuan si
慢慢仔,ban ban a
慢慢仔是,ban ban a si
摠頭,tsang thau
摳,khaunnh
摵,tshik
摸,bong
摺,tsih
摻,tsham
摻,tsham
撇,phiat
敱,khainn
敲,kha
敲,khau
斡,uat
旗,ki
暝,me
暢,thiong
榕,tshing
榫,sun
暝工,me kang
暝日,me jit
榕仔,tshing a
摵仔麵,tshik a mi
暝尾,me bue
暝車,me tshia
榮幸,ing hing
敲油,kha iu
榫空,sun khang
敲門,kha mng
摺衫,tsih sann
摸飛,moo hui
暝時,me si
摺紙,tsih tsua
撤退,thiat the
旗魚,ki hi
摸無路,bong bo loo
榨菜,tsa tshai
敲電話,kha tian ue
榫頭,sun thau
槌,thui
槍,tshiunn
槓,kng
歌,ko
歌,kua
滯,tu
滲,siam
滴,tih
滷,loo
滾,kun
滿,buan
滿,mua
歌手,kua tshiu
滾水,kun tsui
滿月,mua gueh
滾水罐,kun tsui kuan
槌仔,thui a
槓仔,kng a
歌仔,kua a
歌仔戲,kua a hi
滿四界,mua si ke
歌曲,kua khik
滷肉,loo bah
滷肉飯,loo bah png
滷卵,loo nng
滲尿,siam jio
滿足,buan tsiok
滲屎,siam sai
滲屎尿,siam sai jio
滿面,mua bin
滾笑,kun tshio
漁港,hi kang
滾絞,kun ka
滿意,mua i
滿腹,mua pak
槌槌,thui thui
滯滯,tu tu
滿滿,buan buan
滿滿是,mua mua si
歌舞團,kua bu thuan
榴槤,liu lian
歌謠,kua iau
滷麵,loo mi
漂,phiau
漆,tshat
漉,lok
漏,lau
演,ian
漖,ka
漚,au
漚,au
漢,han
漩,suan
漲,tiong
漲,tiunn
熁,hannh
熄,sit
漢文,han bun
漂白,phio peh
漂白粉,phio peh hun
漢字,han ji
漚色,au sik
漩尿,suan jio
演奏,ian tsau
漚客,au kheh
漚屎面,au sai bin
漏洩,lau siap
演員,ian uan
漢草,han tshau
煽動,sian tong
漩桶,suan thang
演習,ian sip
漚貨,au hue
漉喙,lok tshui
漏稅,lau sue
演義,ian gi
漸漸,tsiam tsiam
漉糊糜,lok koo mue
演戲,ian hi
演講,ian kang
漢醫,han i
漢藥,han ioh
漢藥店,han ioh tiam
漲懸價,tiunn kuan ke
漚鹹菜,au kiam tshai
演變,ian pian
漚鬱熱,au ut juah
熊,him
熔,iunn
熗,tshing
疑,gi
疑心,gi sim
疑神疑鬼,gi sin gi kui
疑問,gi bun
瑪瑙,be lo
爾爾,nia nia
熊膽,him tann
盡,tsin
監,kann
碭,thng
碳,thuann
禍,e
禍,ho
福,hok
盡力,tsin lik
碩士,sik su
碟仔,tih a
監囚,kann siu
福利,hok li
福杉,hok sam
監牢,kann lo
盡忠,tsin tiong
福相,hok siong
福氣,hok khi
福眼,hok ging
盡量,tsin liong
監督,kam tok
監禁,kam kim
監獄,kann gak
盡磅,tsin pong
種,tsing
種,tsing
種,tsiong
箅,pin
箍,khoo
箔,poh
算,sng
算,suan
管,kng
管,kong
管,kuan
箸,ti
粽,tsang
精,tsiann
精,tsing
精,tsinn
粿,kue
綠,lik
精力,tsing lik
種子,tsing tsi
箅仔,pin a
粿仔,kue a
綢仔,tiu a
箍半,khoo puann
端正,tuan tsing
精光,tsing kong
粿印,kue in
綜合,tsong hap
精肉,tsiann bah
綠竹,lik tik
綠色,lik sik
綠竹筍,lik tik sun
種作,tsing tsoh
綠豆仔,lik tau a
綠豆鬼,lik tau kui
稱呼,tshing hoo
算命,sng mia
算法,sng huat
管待,kuan thai
管待伊,kuan thai i
精牲,tsing senn
管家,kuan ke
精差,tsing tsha
管家婆,kuan ke po
種珠,tsing tsu
精神,tsing sin
算袂和,sng be ho
算做,sng tso
管區的,kuan khu e
精密,tsing bit
管理,kuan li
精通,tsing thong
算無盤,sng bo puann
箍絡,khoo loh
粿粞,kue tshe
粿葉,kue hioh
種種,tsiong tsiong
粿粽,kue tsang
算數,sng siau
管數,kuan siau
算盤,sng puann
粽箬,tsang hah
管轄,kuan hat
算額,sng giah
種類,tsiong lui
管顧,kuan koo
箸籠,ti lang
網,bang
網,bong
綴,tue
綵,tshai
綹,liu
綿,mi
緊,kin
罰,huat
腿,thui
綴人走,tue lang tsau
緊手,kin tshiu
腐化,hu hua
網仔,bang a
綿仔紙,mi a tsua
綿死綿爛,mi si mi nua
緊行,kin kiann
膁肚,liam too
緊事寬辦,kin su khuann pan
緊性,kin sing
罰金,huat kim
綴前綴後,tue tsing tue au
維持,i tshi
腿庫,thui khoo
膀胱,phong kong
緊張,kin tiunn
罰徛,huat khia
罰單,huat tuann
罰款,huat khuan
綴會仔,tue hue a
綴路,tue loo
緊慢,kin ban
綾羅綢緞,ling lo tiu tuan
綴轎後的,tue kio au e
綿爛,mi nua
膎,ke
膏,ko
舞,bu
蒜,suan
蓄,hak
蓆,tshioh
蓋,kah
蓋,kai
蓋,kua
舞女,bu li
蒜仔,suan a
蒜仔花,suan a hue
舞台,bu tai
膏肓,koo bong
蓄厝,hak tshu
蒜茸,suan jiong
蓋被,kah phue
蓄嫁粧,hak ke tsng
膏膏纏,ko ko tinn
蒜頭,suan thau
膏藥,koo ioh
舞廳,bu thiann
蜜,bit
蜷,khun
蝕,sih
蜜月,bit guat
蝕日,sit jit
蝕月,sit gueh
蝕本,sih pun
蝕重,sih tang
蜘蛛,ti tu
蜘蛛網,ti tu bang
裾,ki
認,jin
誓,tsua
誓,se
誘,iu
語,gi
語,gu
誡,kai
誤,goo
說,suat
說,sue
說,sueh
賒,sia
趕,kuann
趖,so
趕工,kuann kang
誓不兩立,se put liong lip
賒欠,sia khiam
認份,jin hun
認同,jin tong
說多謝,sueh to sia
賑災,tsin tsai
語言,gi gian
認定,jin ting
說明,suat bing
語法,gi huat
說客,sue kheh
認真,jin tsin
製造,tse tso
誤會,goo hue
認罪,jin tsue
誦經,siong king
誤解,goo kai
認路,jin loo
趕路,kuann loo
趕緊,kuann kin
賒數,sia siau
誣賴,bu lua
認輸,jin su
認錯,jin tsho
說謝,sueh sia
踅,seh
輕,khin
辣,luah
遛,liu
遠,hng
遠,uan
鄙,phi
酵,kann
酸,sng
酺,poo
鉸,ka
鉼,pin
鉼,phiann
銀,gin
鉸刀,ka to
鉸刀爿,ka to ping
輕手,khin tshiu
遛手,liu tshiu
輕可,khin kho
酵母,kann bo
遛皮,liu phue
酸甘甜,sng kam tinn
酷刑,khok hing
銀色,gin sik
銀行,gin hang
輔助,hu tsoo
遛疕仔,liu phi a
遠足,uan tsiok
銀角仔,gin kak a
輕便,khin pian
踅玲瑯,seh lin long
輕重,khin tang
踅神,seh sin
輕秤,khin tshin
銀紙,gin tsua
鉼針,pin tsiam
鉸剪,ka tsian
銀票,gin phio
酸筍,sng sun
踅街,seh ke
輕視,khin si
輕銀,khin gin
踅踅唸,seh seh liam
輔導,hu to
遠親,uan tshin
輓聯,buan lian
輕薄,khin poh
輕聲細說,khin siann se sueh
踅螺梯,seh le thui
踅輾轉,seh lian tng
輕鬆,khin sang
銅,tang
銎,khing
銬,khau
閣,koh
閣,koh
隙,khiah
閣再,koh tsai
閣較,koh khah
銅管仔,tang kong a
銅線,tang suann
銅錢,tang tsinn
頕,tam
領,ling
領,nia
餅,piann
餌,ji
魂,hun
鳳,hong
頕低,tam ke
領土,ling thoo
骰仔,tau a
餅幼仔,piann iu a
領受,nia siu
餅店,piann tiam
駁岸,poh huann
頕垂,tam sue
鳳凰,hong hong
鳳凰木,hong hong bok
領帶,nia tua
領教,ling kau
頗略仔,pho liok a
領袖,ling siu
魂魄,hun phik
頕頭,tam thau
骱邊,kai pinn
鼻,phinn
齊,tse
齊,tsiau
齊勻,tsiau un
鼻水,phinn tsui
鼻仔,phinn a
鼻目喙,phinn bak tshui
齊全,tse tsuan
鼻空,phinn khang
鼻空風,phinn khang hong
鼻芳,phinn phang
鼻屎,phinn sai
鼻屎膏,phinn sai ko
鼻音,phinn im
齊備,tse pi
鼻頭,phinn thau
齊頭,tse thau
鼻龍,phinn liong
鼻翼,phinn sit
價,ke
億,ik
儉,khiam
劇,kiok
劌,kui
劍,kiam
劍竹,kiam tik
價值,ke tat
厲害,li hai
劇場,kiok tiunn
劍筍,kiam sun
儉腸凹肚,khiam tng neh too
儉儉仔用,khiam khiam a ing
價數,ke siau
價錢,ke tsinn
僻靜,phiah tsing
儉錢,khiam tsinn
嘹,liau
嘿, heh
噓,si
噗,pok
噗,phok
噗,phok
噴,phun
墜,tui
墟,hi
墨,bak
墨斗,bak tau
墨水,bak tsui
噴水池,phun tsui ti
墜仔,tui a
增加,tsing ka
墨汁,bak tsiap
噓尿,si jio
嘹拍,liau phik
噴射機,phun sia ki
墜落,tui loh
墨賊仔,bak tsat a
墜跤氣,tui kha khi
噴漆,phun tshat
嘻嘻嘩嘩,hi hi hua hua
墨盤,bak puann
噴點,phun tiam
噗薰,pok hun
墜繩,tui tsin
嬈,hiau
嬌,kiau
審,sim
寫,sia
寮,liau
層,tsan
層,tsan
屧,siap
幡,huan
廟,bio
廠,tshiunn
廢,hui
廣,kong
彈,tuann
彈,tuann
影,iann
德,tik
廚子,too tsi
廟公,bio kong
廢止,hui tsi
屧手縫,siap tshiu phang
影片,iann phinn
寮仔,liau a
幡仔,huan a
廟仔,bio a
影目,iann bak
影印,iann in
寫字,sia ji
廟寺,bio si
徵收,ting siu
審判,sim phuann
廣告,kong ko
廚房,tu pang
廢物,hui but
嬈花,hiau hue
審查,sim tsa
寬限,khuan han
廟埕,bio tiann
審問,sim mng
彈琴,tuann khim
屧貼,siap thiap
廢話,hui ue
幢幡,tong huan
寬寬仔,khuann khuann a
寬寬仔是,khuann khuann a si
廣播劇,kong poo kiok
影戲,iann hi
影響,ing hiong
慼,tsheh
憂,iu
戮,lak
撆,pih
撈,hoo
撋,nua
撏,jim
撐,the
撒,suah
撓,ngiau
撚,lian
撞,tong
撟,kiau
撠,giah
慼心,tsheh sim
撆手䘼,pih tshiu ng
撒豆油,suah tau iu
撠刺,giah tshi
撚匼笑,lian khap tshio
戮空,lak khang
撞突,tong tut
撒胡椒,suah hoo tsio
撞破,tong phua
慶祝,khing tsiok
慰問,ui bun
撞球,tong kiu
撆紮,pih tsah
撐船,the tsun
慰勞,ui lo
憂悶,iu bun
憤慨,hun khai
憂結結,iu kat kat
撞著,tong tioh
慶賀,khing ho
憂愁,iu tshiu
撙節,tsun tsat
憢疑,giau gi
撚骰仔,lian tau a
憐憫,lian bin
撐篙,the ko
撆褲跤,pih khoo kha
憂頭苦面,iu thau khoo bin
憂頭結面,iu thau kat bin
撚寶,lian po
撒鹽,suah iam
戮鑽,lak tsng
撚鑽,lian tsng
撥,puah
撨,tshiau
撩,liau
撩,lio
撫,hu
撬,kiau
播,poo
撮,tshok
數,siau
數,soo
暫,tsiam
槳,tsiunn
槽,tso
樂,gak
樂,lok
敵人,tik jin
撥工,puah kang
敵手,tik tshiu
暴牙,pok ge
暫且,tsiam tshiann
槳仔,tsiunn a
佈田,poo tshan
數目,siau bak
佈田管,poo tshan kong
數字,soo ji
數念,siau liam
數房,siau pang
撩油,lio iu
暫度,tsiam too
播音,poo im
暫時,tsiam si
撨時鐘,tshiau si tsing
播送,poo sang
數單,siau tuann
撥開,puah khui
數量,soo liong
樂隊,gak tui
樂園,lok hng
數想,siau siunn
撨摵,tshiau tshik
樂暢,lok thiong
佈稻仔,poo tiu a
撥駕,puah ka
撫養,bu iong
數學,soo hak
暴穎,pok inn
槽頭,tso thau
數櫃,siau kui
數額,siau giah
數簿,siau phoo
暴露,pok loo
樂觀,lok kuan
樓,lau
標,piau
標,pio
樟,tsiunn
樠,mia
模,boo
樣,iunn
漿,tsiunn
潑,phuah
潘,phun
潘水,phun tsui
樓仔,lau a
樟仔,tsiunn a
樓仔厝,lau a tshu
標本,piau pun
樓尾頂,lau bue ting
漿泔,tsiunn am
潘泔,phun am
潑雨,phuah hoo
漿洗,tsiunn se
標致,phiau ti
漿衫,tsiunn sann
潘桶,phun thang
樓梯,lau thui
樓頂,lau ting
標會仔,pio hue a
標準,piau tsun
樟腦,tsiunn lo
樓跤,lau kha
模樣,boo iunn
模範,boo huan
標頭,phiau thau
標頭,pio thau
潤,jun
潭,tham
潲,siau
澍,tshu
濆,bun
熟,sik
熥,thng
熨,ut
熬,go
熟手,sik tshiu
熨斗,ut tau
潭仔,tham a
熟似,sik sai
熟似人,sik sai lang
熨金,ut kim
潮流,tiau liu
潦草,lo tsho
澄清,ting tshing
澎湖菜瓜,henn oo tshai kue
潤餅𩛩,jun piann kauh
熟鐵,sik thih
熱,jiat
熱,juah
獎,tsiong
瘡,tshng
瘤,liu
瘦,san
皺,jiau
盤,puann
熱人,juah lang
熱天,juah thinn
熱心,jiat sim
盤仔,puann a
盤古,huan koo
璇石,suan tsioh
瘦田,san tshan
瘦肉,san bah
盤車,puann tshia
瘦卑巴,san pi pa
瘦抽,san thiu
獎狀,tsiong tsng
獎金,tsiong kim
熱毒,jiat tok
瘟疫,un ik
熱帶,jiat tai
皺痕,jiau hun
盤喙錦,puann tshui gim
瘦猴,san kau
璇筆,suan pit
熱著,juah tioh
盤話,puann ue
熱嗽,jiat sau
盤撋,puann nua
盤數,puann siau
獎勵,tsiong le
皺襞襞,jiau phe phe
瞌,kheh
磅,pong
磕,khap
稻,tiu
稿,ko
窮,king
窮,kiong
窮,khing
窯,io
箠,tshue
箬,hah
箭,tsinn
箱,siunn
磅子,pong tsi
窮分,khing hun
磅仔,pong a
箠仔,tshue a
箱仔,siunn a
磅皮,pong phue
磅米芳,pong bi phang
確定,khak ting
磅空,pong khang
磅重,pong tang
稻埕,tiu tiann
稻草,tiu tshau
稻草人,tiu tshau lang
磕袂著,khap be tioh
磕著,khap tioh
確實,khak sit
磅錶,pong pio
碼頭,be thau
磕頭,khap thau
稻穗,tiu sui
箱籠,siunn lang
篇,phinn
篋,kheh
糊,koo
糋,tsinn
線,suann
緟,thong
緣,ian
編,pian
緩,uan
練,lian
罵,ma
罵,me
糊人,koo lang
篋仔,kheh a
糊仔,koo a
練字,lian ji
編曲,pian khik
緣投,ian tau
緣故,ian koo
線香,suann hiunn
線索,suann soh
練習,lian sip
範圍,huan ui
寸棗,tshun tso
練痟話,lian siau ue
範勢,pan se
糊塗,hoo too
線路,suann loo
糊瘰瘰,hoo lui lui
編輯,pian tsip
線頭,suann thau
罷,pa
膚,hu
膜,mooh
膠,ka
膣,tsi
舖,phoo
蓬,phong
罷工,pa kang
蓮子,lian tsi
蓬心,pong sim
罷市,pa tshi
膣屄,tsi bai
蓮花,lian hue
蓮花金,lian hue kim
蓪草,thong tsho
蓬萊米,hong lai bi
蓮蕉花,lian tsiau hue
蓬鬆,phong song
蓮藕,lian ngau
蓮霧,lian bu
蔗,tsia
蔥,tshang
蔫,lian
蔭,im
蔭,ng
蝝,ian
蝦,he
蝨,sat
蝦仁,he jin
蔥仔,tshang a
蝦仔,he a
蝨母,sat bo
蝦米,he bi
蔭身,im sin
蝦卑,he pi
蝦蛄,he koo
蝦蛄擗仔,he koo phiak a
蔭豉仔,im sinn a
蝦猴,he kau
蝦膎,he ke
蔗箬,tsia hah
蝨篦,sat pin
蔥頭,tshang thau
蝒蟲,bin thang
衝,tshing
衝,tshiong
褒,po
褙,pue
誰,tsui
課,kho
調,tiau
調,tiau
談,tam
課文,kho bun
蝶仔,iah a
課本,kho pun
衛生,ue sing
衛生紙,ue sing tsua
談判,tam phuann
衛星,ue tshenn
調查,tiau tsa
衝突,tshiong tut
調停,tiau thing
衝動,tshiong tong
調動,tiau tong
課程,kho ting
褒嗦,po so
衝碰,tshong pong
調解,tiau kai
褒歌,po kua
褒獎,po tsiong
蝴蝶,oo tiap
談論,tam lun
調養,tiau iong
調整,tiau tsing
誹謗,hui pong
複雜,hok tsap
請,tshiann
請,tshing
諍,tsenn
論,lun
豬,ti
賜,su
賞,siunn
賠,pue
賢,hian
賣,be
賣,mai
賤,tsian
質,tsit
賭,too
踏,tah
踢,that
請人客,tshiann lang kheh
豬公,ti kang
豬公,ti kong
論文,lun bun
豬心,ti sim
賞月,siunn gueh
踏斗,tah tau
豬仔,ti a
豬仔囝,ti a kiann
豬母,ti bo
豬母奶仔,ti bo ling a
豬母菜,ti bo tshai
請示,tshing si
請安,tshing an
豬肉,ti bah
豬舌,ti tsih
豬血,ti hueh
請坐,tshiann tse
請求,tshing kiu
豬灶,ti tsau
豬牢,ti tiau
豬肚,ti too
豬肝,ti kuann
豬肝色,ti kuann sik
賣身,be sin
請命,tshing bing
賣命,be mia
趣味,tshu bi
請帖,tshiann thiap
踏枋,tah pang
豬油,ti iu
豬油粕仔,ti iu phoh a
賞狀,siunn tsng
豬狗精牲,ti kau tsing senn
豬肺,ti hi
賞金,siunn kim
豬胚仔,ti phue a
豬哥,ti ko
豬哥牙,ti ko ge
豬哥神,ti ko sin
踏差,tah tsha
請桌,tshiann toh
賭氣,too khi
豬砧,ti tiam
請神,tshiann sin
請假,tshing ka
請問,tshiann mng
質問,tsit mng
賭強,too kiong
請教,tshing kau
踢被,that phue
諍喙,tsenn tshui
踏硬,tah nge
豬菜,ti tshai
質量,tsit liong
踢毽子,that kian tsi
請罪,tshing tsue
豬腸仔,ti tng a
諒解,liong kai
質詢,tsit sun
豬跤,ti kha
豬跤箍,ti kha khoo
踏話頭,tah ue thau
豬跤麵線,ti kha mi suann
賞罰,siunn huat
賢慧,hian hue
豬槽,ti tso
賞賜,siunn su
豬鋪,ti phoo
賞錢,siunn tsinn
賠錢,pue tsinn
豬頭爿,ti thau ping
豬頭皮,ti thau phue
豬頭肥,ti thau pui
賠償,pue siong
賤蟲,tsian thang
踏蹺,tah khiau
踮,tiam
輦,lian
輩,pue
輪,lian
輪,lun
遨,go
遮,tsia
遮,tsiah
遮,jia
遷,tshian
鄰,lin
醃,am
醉,tsui
醋,tshoo
遮日,jia jit
輪仔,lian a
醃瓜,am kue
適合,sik hap
遷居,tshian ki
遮的,tsia e
遮雨,jia hoo
醃缸,am kng
遮風,jia hong
輪值,lun tit
輪框,lian khing
輪班,lun pan
輪迴,lun hue
遷徙,tshian sua
醋桶,tshoo thang
踩街,tshai ke
適當,sik tong
遭遇,tso gu
遮閘,jia tsah
遮爾,tsiah ni
遮爾仔,tsiah ni a
遮瞞,jia mua
輦轎仔,lian kio a
輪鬮,lun khau
銷,siau
鋏,giap
鋩,me
鋪,phoo
閬,lang
閬工,lang kang
閬月,lang gueh
鋩角,me kak
鋪面蟶,phoo bin than
銷售,siau siu
鋪排,phoo pai
鋪排話,phoo pai ue
鋪棉裘,phoo mi hiu
銷路,siau loo
鋤頭,ti thau
閬縫,lang phang
霆,tan
靠,kho
靠,khua
鞋,e
鞍,uann
鞏,khong
養,iong
養,iunn
餓,go
駐,tu
駛,sai
靠山,kho suann
養女,iong li
養子,iong tsu
霆水螺,tan tsui le
養母,iunn bu
餓死,go si
駐死,tu si
養老,iong lo
養育,iong iok
駛車,sai tshia
靠岸,kho huann
鞋抿仔,e bin a
鞋拔仔,e pueh a
鞋油,e iu
養爸,iunn pe
養的,iong e
靠俗,kho siok
鞋苴,e tsu
養神,iong sin
鞋帶,e tua
駛船,sai tsun
靠著,kho tioh
靠勢,kho se
養飼,iong tshi
霆雷公,tan lui kong
駕駛,ka su
鬧,nau
魄,phik
魯,loo
麩,hu
麩,phoo
齒,khi
齒𣻸,khi siunn
鴉片,a phian
鴉片仙,a phian sian
魩仔魚,but a hi
鬧台,nau tai
齒包,khi pau
齒岸,khi huann
鬧房,nau pang
齒抿仔,khi bin a
齒杯,khi pue
齒科,khi kho
齒粉,khi hun
魬魚,puann hi
魴魚,hang hi
齒膏,khi ko
鬧熱,lau jiat
齒縫,khi phang
齒觳仔,khi khok a
齒戳仔,khi thok a
鬧廳,nau thiann
儑,gam
凝,ging
器,khi
噪人耳,tsho lang hinn
凝心,ging sim
凝血,ging hueh
器具,khi ku
器官,khi kuan
器重,khi tiong
儑面,gam bin
噤喙,khiunn tshui
噭噭叫,kiau kiau kio
儑頭儑面,gam thau gam bin
噯,aih
壁,piah
壅,ing
壇,tuann
學,hak
學,oh
學人,oh lang
學力,hak lik
學士,hak su
學工夫,oh kang hu
噯仔,ai a
學仔,oh a
學仔仙,oh a sian
壅田,ing tshan
學生,hak sing
學位,hak ui
壁空,piah khang
壅肥,ing pui
學校,hak hau
奮鬥,hun tau
學問,hak bun
壁堵,piah too
學堂,oh tng
學理,hak li
學習,hak sip
學術,hak sut
學期,hak ki
學費,hak hui
學業,hak giap
學話,oh ue
學寮,hak liau
噷噷,hmh hmh
壁櫥,piah tu
憑,pin
憲,hian
懍,lun
戰,tsian
撼,ham
擂,lui
擇,tik
擉,tiak
擋,tong
操,tshau
操,tsho
擒,khim
擔,tam
擔,tann
擔,tann
據,ki
擛,iat
整,tsing
擔工,tann kang
操心,tshau sim
擔水,tann tsui
擛手,iat tshiu
擔仔麵,tann a mi
擔任,tam jim
據在,ki tsai
憲兵,hian ping
操作,tshau tsok
戰車,tsian tshia
憑良心,pin liong sim
憲法,hian huat
戰爭,tsian tsing
擔肥,tann pui
擔保,tam po
擋咧,tong leh
擔屎,tann sai
擛風,iat hong
戰鬥,tsian tau
整理,tsing li
擂缽,lui puah
戰術,tsian sut
操勞,tshau lo
懍場,lun tiunn
戰場,tsian tiunn
懊惱,au nau
戰亂,tsian luan
憑準,pin tsun
操煩,tshau huan
擔當,tam tng
整頓,tsing tun
擂鼓,lui koo
懊嘟嘟,au tu tu
擂槌,lui thui
擉算盤,tiak sng puann
整齊,tsing tse
擔憂,tam iu
操練,tshau lian
憑據,pin ki
擔輸贏,tam su iann
擋頭,tong thau
擔頭,tann thau
擁護,iong hoo
樹,tshiu
橋,kio
橐,lok
橐,lop
橛,kueh
樹子,tshiu tsi
曆日,lah jit
樹木,tshiu bak
樹仔,tshiu a
橐仔,lok a
樹奶,tshiu ling
樹奶糖,tshiu ling thng
樹尾,tshiu bue
樹豆,tshiu tau
樹身,tshiu sin
樹林,tshiu na
樹枝,tshiu ki
樹根,tshiu kin
樹栽,tshiu tsai
機密,ki bit
機械,ki hai
橐袋仔,lak te a
橋頂,kio ting
機場,ki tiunn
樹椏,tshiu ue
樹絡,tshiu le
機會,ki hue
橋跤,kio kha
橋墩,kio tun
樹蔭,tshiu ng
機器,ki khi
機器桶,ki khi thang
樹頭,tshiu thau
橋頭,kio thau
樹薯,tshiu tsi
機關,ki kuan
機關銃,ki kuan tshing
橄欖,kan na
橫,huainn
歕,pun
澹,tam
激,kik
濁,lo
激力,kik lat
激五仁,kik ngoo jin
激心,kik sim
歕火,pun hue
歷史,lik su
激外外,kik gua gua
橫扴,huainn keh
激怐怐,kik khoo khoo
橫直,huainn tit
激空,kik khang
激屎,kik sai
激派頭,kik phai thau
歕風,pun hong
激面腔,kik bin tshiunn
激氣,kik khi
激氣,kik khui
激烈,kik liat
橫財,huainn tsai
橫逆,hing gik
激酒,kik tsiu
激骨,kik kut
激腦,kik lo
澹漉漉,tam lok lok
澹糊糊,tam koo koo
歕觱仔,pun pi a
歕雞胿,pun ke kui
歕雞胿仔,pun ke kui a
橫霸霸,huainn pa pa
燃,hiann
燈,ting
燉,tun
燒,sio
燕,inn
燖,tim
燙,thng
燜,bun
甌,au
甍,bong
燈心,ting sim
燒水,sio tsui
燃火,hiann hue
燈火,ting hue
燕仔,inn a
甌仔,au a
獨立,tok lip
燒肉,sio bah
獨身,tok sin
燒金,sio kim
燒香,sio hiunn
燈座,ting tso
燃柴,hiann tsha
燒烙,sio lo
燒酒,sio tsiu
燒酒螺,sio tsiu le
燒酒雞,sio tsiu ke
燈猜,ting tshai
燒著,sio tioh
獨裁,tok tshai
燜飯,bun png
燈塔,ting thah
燒滾滾,sio kun kun
燕窩,ian o
燒熱,sio juah
獨獨,tok tok
燖鍋,tim ue
瘸,khue
瞞,mua
磚,tsng
磨,bo
磨,bua
積,tsik
穎,inn
瘸手,khue tshiu
瞞天過海,mua thinn kue hai
磚仔,tsng a
磨坩,bua khann
磟碡,lak tak
瘸跤,khue kha
磨粿,bo kue
積德,tsik tik
瞞騙,mua phian
篙,ko
篡,tshuan
篦,pin
篩,thai
糕,ko
糖,thng
縋,lui
縖,ha
縛,pak
縣,kuan
糖丹,thng tan
篩斗,thai tau
糖水,thng tsui
篩仔,thai a
糕仔,ko a
糕仔餅,ko a piann
糖仔餅,thng a piann
糕仔頭,ko a thau
縣立,kuan lip
糖甘蜜甜,thng kam bit tinn
糖含仔,thng kam a
糖尿病,thng jio penn
縣長,kuan tiunn
糖粉,thng hun
窸倏,si sua
窸窣叫,sih sut kio
縖裙,ha kun
縛跤,pak kha
縛粽,pak tsang
糖膏,thng ko
糖廠,thng tshiunn
糖蔥,thng tshang
窸窸窣窣,si si sut sut
糖霜,thng sng
糖廍,thng phoo
膨,phong
膭,kui
興,hing
興,hing
蕊,lui
膭水,kui tsui
膨皮,phong phue
膨床,phong tshng
膨肚短命,phong too te mia
興旺,hing ong
膨疱,phong pha
膨風,phong hong
膨風龜,phong hong ku
膨粉,phong hun
膨紗,phong se
膨紗衫,phong se sann
興衰,hing sue
興酒,hing tsiu
膨椅,phong i
膨獅獅,phong sai sai
膨鼠,phong tshi
膨餅,phong piann
興趣,hing tshu
翱翱輾,ko ko lian
興頭,hing thau
膩瓤,ji nng
蝹,un
褪,thng
褫,thi
褲,khoo
褪皮,thng phue
褪赤跤,thng tshiah kha
褪衫,thng sann
褲帶,khoo tua
褲袋仔,khoo te a
褪殼,thng khak
褫開,thi khui
褪腹裼,thng pak theh
褲跤,khoo kha
褪齒,thng khi
褪褲,thng khoo
褪褲𡳞,thng khoo lan
蕨貓,kueh niau
褲頭,khoo thau
親,tshin
諞,pian
諾, hioh
謔,gioh
貓,niau
賰,tshun
賴,lua
蹁,phin
蹄,te
親人,tshin lang
親切,tshin tshiat
親友,tshin iu
親手,tshin tshiu
觱仔,pi a
貓仔,niau a
諞仙仔,pian sian a
親生,tshin senn
親目,tshin bak
親身,tshin sin
親事,tshin su
貓兒竹,ba ji tik
親姆,tshenn m
親姆婆,tshenn m po
賰的,tshun e
親近,tshin kin
貓咪,niau bi
貓面,niau bin
親家,tshin ke
親家公,tshin ke kong
謀財害命,boo tsai hai bing
親骨肉,tshin kut jiok
親堂,tshin tong
親密,tshin bit
親情,tshin tsiann
親戚,tshin tshik
親情五十,tshin tsiann goo tsap
親族,tshin tsok
親喙,tshin tshui
親愛,tshin ai
親像,tshin tshiunn
貓貓,niau niau
賰錢,tshun tsinn
貓頭鳥,niau thau tsiau
貓霧仔光,ba bu a kng
貓霧光,ba bu kng
躽,nua
輸,su
辦,pan
選,suan
遹,ut
遺,i
醒,tshenn
鋸,ki
鋼,kng
錄,lok
輸入,su jip
辦公,pan kong
扮公伙仔,pan kong hue a
選手,suan tshiu
鋸仔,ki a
輸出,su tshut
遵守,tsun siu
輸血,su hueh
遺言,ui gian
遵命,tsun bing
辦法,pan huat
輸面,su bin
錄音,lok im
錄音機,lok im ki
醒悟,sing ngoo
辦桌,pan toh
遺書,ui su
辦理,pan li
遺產,ui san
選票,suan phio
辦貨,pan hue
鋼琴,kng khim
鋼筆,kng pit
鋸齒,ki khi
選擇,suan tik
遺憾,ui ham
選舉,suan ki
輸贏,su iann
鋼鐵,kng thih
鋸鑢仔,ki le a
遺囑,ui tsiok
錚,tshann
錢,tsinn
錫,siah
錶,pio
閹,iam
隨,sui
險,hiam
雕,tiau
靜,tsenn
靜,tsing
錯手,tsho tshiu
錶仔,pio a
隨在,sui tsai
隨在你,sui tsai li
閻君,giam kun
靜坐,tsing tso
隨身,sui sin
雕刻,tiau khik
隨便,sui pian
隨後,sui au
隨時,sui si
錢根,tsinn kin
錢桌仔,tsinn toh a
錢財,tsinn tsai
錢鬼,tsinn kui
錢莊,tsinn tsng
錦蛇,gim tsua
錢袋仔,tsinn te a
錢筒仔,tsinn tang a
錢項,tsinn hang
錯亂,tsho luan
隨意,sui i
錢鼠,tsinn tshi
錯誤,tsho goo
隨緣,sui ian
靜養,tsing iong
隨機應變,sui ki ing pian
險險,hiam hiam
錢櫃,tsinn kui
閹雞,iam ke
閻羅王,giam lo ong
錢關,tsinn kuan
錢鰻,tsinn mua
鞘,siu
頭,thau
頷,am
餡,ann
館,kuan
髻,kue
頭七,thau tshit
頭人,thau lang
頷巾,am kin
頭上仔,thau tsiunn a
頭手,thau tshiu
頭毛,thau mng
頭水,thau tsui
骿支骨,phiann ki kut
頭毛菜,thau mng tshai
頭毛鋏仔,thau mng giap a
頭牙,thau ge
頭仔,thau a
髻仔鬃,kue a tsang
頭目,thau bak
頭目鳥,thau bak tsiau
頭先,thau sing
頭名,thau mia
頭旬,thau sun
頭尾,thau bue
頭到,thau kau
頭帛,thau peh
頭拄仔,thau tu a
頭前,thau tsing
頷垂,am se
頭胎,thau the
頭面,thau bin
頭家,thau ke
頭家娘,thau ke niu
頭疼,thau thiann
頭眩目暗,thau hin bak am
頷胿,am kui
頭起先,thau khi sing
頭陣,thau tin
骿條骨,phiann liau kut
頭殼,thau khak
頭殼碗,thau khak uann
頭殼額仔,thau khak hiah a
頭殼髓,thau khak tshue
頭腦,thau nau
頷腮,am tshi
頭路,thau loo
頷領,am nia
餡餅,ann piann
駱駝,lok to
頭麩,thau phoo
骿條,phiann liau
頷頸,am kun
頭摠,thau tsang
頭擺,thau pai
頭額,thau hiah
頭鬃,thau tsang
頭鬃尾,thau tsang bue
頭鬃箍仔,thau tsang khoo a
鴨,ah
黗,thun
龍,ling
龍,liong
龜,ku
龜毛,ku moo
鴨仔,ah a
鴨仔囝,ah a kiann
鴨仔癉,ah a tan
鴨母,ah bo
鴨母喙,ah bo tshui
鴨母蹄,ah bo te
鴨卵,ah nng
鴨咪仔,ah bi a
龜祟,ku sui
龍脈,liong meh
龍骨,liong kut
龍眼,ling ging
龍眼乾,ling ging kuann
龍船,ling tsun
鮑魚,pau hi
鴨掌,ah tsiunn
龜殼,ku khak
龜殼花,ku khak hue
鴨雄仔,ah hing a
龜跤,ku kha
龜精,ku tsiann
龍鳳,liong hong
龍蝦,ling he
鴛鴦,uan iunn
鴨鵤,ah kak
鴨羶,ah hian
龜蠅,ku sin
鴨鯗,ah siunn
鮕鮘,koo tai
嚇,hann
嚇,heh
嚓,tshiak
優先,iu sian
優秀,iu siu
優待,iu thai
優美,iu bi
嚓嚓趒,tshiak tshiak tio
優點,iu tiam
嚇驚,heh kiann
壓,ah
嶺,nia
幫,pang
幫,png
應,in
戲,hi
戴,ti
擘,peh
擠,tsik
擢,tioh
擤,tshing
擦,tshat
擠𤶃仔,tsik thiau a
壓力,ap lik
應公仔,ing kong a
戲文,hi bun
嬰仔,enn a
應付,ing hu
嬰母仔,inn bo a
應用,ing iong
幫忙,pang bang
戲曲,hi khik
擢舌根,tioh tsih kin
幫助,pang tsoo
戲弄,hi lang
懇求,khun kiu
壓味,ah bi
擘金,peh kim
壓迫,ap pik
應效,ing hau
戲班,hi pan
戲院,hi inn
應喙,in tshui
應喙應舌,in tshui in tsih
戲棚,hi penn
擘開,peh khui
戲園,hi hng
彌補,mi poo
應話,in ue
應該,ing kai
應該然,ing kai jian
應酬,ing siu
擤鼻,tshing phinn
戲劇,hi kiok
懂嚇,tang hiannh
應聲,in siann
幫贊,pang tsan
戲齣,hi tshut
壓霸,ah pa
應驗,ing giam
檀,tuann
檔,tong
檠,kiann
檨,suainn
檨仔,suainn a
檨仔青,suainn a tshenn
檢定,kiam ting
檢采,kiam tshai
殭屍,khiong si
曖昧,ai mai
檢查,kiam tsa
檔案,tong an
檢討,kiam tho
檢察官,kiam tshat kuann
檢舉,kiam ki
檢點,kiam tiam
檢驗,kiam giam
澀,siap
溼,sip
濟,tse
濫,lam
營,iann
營,ing
燥,so
燭,tsik
燭,tsiok
牆,tshiunn
濟少,tse tsio
燥水,so tsui
牆仔,tshiunn a
燭台,tsik tai
濫使,lam su
牆圍,tshiunn ui
營業,ing giap
濟話,tse ue
營養,ing iong
澩澩,haunnh haunnh
溼溼,sip sip
濟濟,tse tse
濫糝,lam sam
燦爛,tshan lan
環,khuan
癀,hong
癉,tan
癌,gam
盪,tng
瞪,tenn
瞭,lio
礁,ta
禪,sian
瞪力,tenn lat
磺水,hong tsui
磺火,hong hue
瞪屎,tenn sai
環境,khuan king
療養,liau iong
穗,sui
篷,phang
篾,bih
糜,muai
糝,sam
糞,pun
糠,khng
縫,pang
縫,phang
縮,sok
總,tsong
糠𧉟,khng tai
糞口,pun khau
糞口蟲,pun khau thang
篾仔,bih a
總共,tsong kiong
糙米,tsho bi
總是,tsong si
縫衫,pang sann
總計,tsong ke
糝粉,sam hun
縮茶心,sok te sim
總務,tsong bu
糞埽,pun so
糞堆,pun tui
糞埽市場,pun so tshi tiunn
糞埽車,pun so tshia
糞埽桶,pun so thang
糞埽籠,pun so lang
縫紩,pang thinn
總統,tsong thong
總裁,tsong tshai
總貿,tsong bau
糜飯,mue png
總經理,tsong king li
總算,tsong sng
總管,tsong kuan
篾蓆,bih tshioh
總數,tsong siau
總舖師,tsong phoo sai
總鋪,tsong phoo
糜糜卯卯,mi mi mauh mauh
總講,tsong kong
總額,tsong giah
繃,penn
罾,tsan
翼,sit
聯,lian
聲,siann
聲,sing
聳,tshang
膽,tam
膽,tann
膿,lang
臆,ioh
臊,tsho
臨,lim
臨,lim
薄,poh
薅,khau
罾仔,tsan a
臆出出,ioh tshut tshut
聯合,lian hap
舉行,ki hing
聰明,tshong bing
聲明,sing bing
薄板,poh pan
薄板仔,poh pan a
翼股,sit koo
臨急,lim kip
艱苦,kan khoo
艱苦人,kan khoo lang
艱苦罪過,kan khoo tse kua
聲音,siann im
臨時,lim si
薅草,khau tshau
舉荐,ki tsian
舉動,ki tong
薄情,pok tsing
聲望,sing bong
臨終,lim tsiong
薄荷,pok ho
罾魚,tsan hi
聯絡,lian lok
臊菜,tsho tshai
蕹菜,ing tshai
膽量,tam liong
聲勢,siann se
聳勢,sang se
聲嗽,siann sau
聯對,lian tui
聲說,siann sueh
聲調,siann tiau
臨機應變,lim ki ing pian
蕗蕎,loo gio
薁蕘,o gio
膽頭,tann thau
臨檢,lim kiam
薄縭絲,poh li si
膽膽,tam tam
臨臨仔,lim lim a
聲聲句句,siann siann ku ku
艱難,kan lan
聳鬚,tshang tshiu
薑,kiunn
薟,hiam
薯,tsi
螺,le
薏仁,i jin
薪水,sin sui
虧心,khui sim
虧欠,khui khiam
螺仔,le a
薑母,kiunn bo
薑母鴨,kiunn bo ah
虧空,khui khong
薟椒仔,hiam tsio a
薑絲,kiunn si
螺絲,loo si
螺絲釘,loo si ting
螺絲絞,loo si ka
虧損,khui sng
螿蜍,tsiunn tsi
薟薑仔,hiam kiunn a
蟋蟀仔,sih sut a
觳,khok
講,kang
講,kong
謝,sia
趨,tshu
講大聲話,kong tua siann ue
觳仔,khok a
觳仔炱,khok a te
講古,kong koo
謄本,thing pun
講白賊,kong peh tshat
講好,kong ho
講究,kang kiu
謠言,iau gian
謙卑,khiam pi
講和,kong ho
講明,kong bing
謝金,sia kim
賺食,tsuan tsiah
講師,kang su
講破,kong phua
講笑,kong tshio
謝神,sia sin
講笑詼,kong tshio khue
講起,kong khi
講堂,kang tng
講情,kong tsing
謎猜,bi tshai
講習,kang sip
謝絕,sia tsuat
謙虛,khiam hi
謝罪,sia tsue
講話,kong ue
蹌跤雞,tshiang kha ke
講嘐潲話,kong hau siau ue
講演,kang ian
蹌箍螺,tshiang khoo le
講價,kong ke
講親情,kong tshin tsiann
謝禮,sia le
蹊蹺,khi khiau
謝願,sia guan
輾,lian
避,pi
還,hing
還,huan
還,huan
錘,thui
鍊,lian
鍋,ko
鍋,ue
鍤,tshiah
鍥,keh
鍊仔,lian a
鍋仔,ue a
鍥仔,keh a
避免,pi bian
還俗,huan siok
還數,hing siau
邀請,iau tshiann
還錢,hing tsinn
輾轉,lian tng
鍾,tsing
闊,khuah
隱,un
霜,sng
霜,song
隱弓蕉,un king tsio
隱居,un ki
霜風,sng hong
隱痀,un ku
闊莽莽,khuah bong bong
霜雪,sng seh
闊喙,khuah tshui
雖然,sui jian
闊腹,khuah pak
闊閬閬,khuah long long
隱瞞,un mua
鮮,tshinn
鮮沢,tshinn tshioh
黏,liam
黜,thuh
甪,lut
黜,thut
點,tiam
鼾,konn
鼾,huann
齋,tsai
點心,tiam sim
點心擔,tiam sim tann
黜仔,thuh a
點穴,tiam hiat
點名,tiam mia
黜破,thuh phua
點破,tiam phua
黜臭,thuh tshau
點眼,tiam gan
點痣,tiam ki
黏塗,liam thoo
黜塗機,thuh thoo ki
鼢鼠,bun tshi
黏膠,liam ka
點醒,tiam tshenn
鵁鴒,ka ling
鼾鼾叫,huann huann kio
點鐘,tiam tsing
黏黐黐,liam thi thi
嚙,ge
壘,lui
壘,lui
壙,khong
嬸,tsim
戳,thok
擲,tan
擸,ba
擺,pai
擽,ngiau
攄,lu
斷,tng
斷,tuan
斷,tuan
擲㧒捔,tan hiat kak
攄仔,lu a
檫仔,tshat a
斷奶,tng ling
擽呧,ngiau ti
斷根,tng kin
斷氣,tng khui
嬸婆,tsim po
斷掌,tng tsiunn
斷絕,tuan tsuat
擾亂,jiau luan
攄塗機,lu thoo ki
斷腦筋,tng nau kin
斷路,tng loo
斷種,tng tsing
擴頭,khok thau
攄頭毛,lu thau mng
擴擴,khok khok
櫃,kui
歸,kui
濺,tsuann
濾,li
瀉,sia
爁,nah
濺水,tsuann tsui
爁日,nah jit
檳榔,pin nng
檸檬,le bong
瀉藥仔,sia ioh a
甓,phiah
甕,ang
癖,phiah
癖,phiah
癗,lui
礐,hak
禮,le
穡,sit
穢人,ue lang
甕仔,ang a
甕肚,ang too
癖性,phiah sing
禮服,le hok
禮物,le but
禮拜,le pai
禮拜日,le pai jit
禮拜堂,le pai tng
穢涗,ue sue
禮堂,le tng
禮貌,le mau
禮儀,le gi
禮數,le soo
穡頭,sit thau
簫,siau
糧,niu
繏,sng
繐,sui
織,tsit
繚,liau
繡,siu
翸,phun
翹,khiau
翻,huan
職,tsit
臍,tsai
舊,ku
薰,hun
薸,phio
織女,tsit li
舊年,ku ni
舊式,ku sik
職位,tsit ui
薰吹,hun tshue
翻身,huan sin
繡房,siu pang
翻版,huan pan
繡花,siu hue
薰屎,hun sai
翻厝,huan tshu
職員,tsit uan
翻案,huan an
繚索,liau soh
糧草,niu tshau
翻草,huan tshau
職務,tsit bu
繡球,siu kiu
繡球花,siu kiu hue
薰喙仔,hun tshui a
簡單,kan tan
翻新,huan sin
職業,tsit giap
繏腰,sng io
舊數,ku siau
舊曆,ku lik
翻頭,huan thau
薰頭,hun thau
翻點,huan tiam
翹翹,khiau khiau
繏嚨喉,sng na au
翻譯,huan ik
職權,tsit khuan
藃,hiauh
藍,na
藏,tshang
蟬,sian
蟯,gio
蟯,ngiauh
蟲,thang
蟲,thiong
蟳,tsim
覆,phak
藏水沬,tshang tsui bi
蟬仔,sian a
蟯仔,gio a
蟳仔,tsim a
藍色,na sik
蟯桮,gio pue
蟲豸,thang thua
覆菜,phak tshai
藐視,biau si
蟧蜈,la gia
蟧蜈車,la gia tshia
蟳管,tsim kong
藃藃,hiauh hiauh
蟮蟲仔,sian thang a
蟯蟯趖,ngiauh ngiauh so
藃蟶,hiauh than
謼,hooh
蹔,tsam
蹛,tua
軀,su
軁,nng
軁,nng
轉,tsuan
轉,tsuan
轉,tng
轉大人,tng tua lang
轉世,tsuan se
轉去,tng khi
轉外家,tng gua ke
豐年,hong ni
豐收,hong siu
豐沛,phong phai
轉來,tng lai
軁狗空仔,nng kau khang a
轉後頭,tng au thau
轉骨,tng kut
轉喙,tng tshui
豐富,hong hu
謹慎,kin sin
蹔跤步,tsam kha poo
轉斡,tng uat
轉踅,tng seh
轉輪,tng lun
轉學,tsuan hak
軁錢空,nng tsinn khang
轉聲,tng siann
轉臍,tng tsai
蹧躂,tsau that
轉彎,tng uan
轉彎踅角,tng uan seh kak
轉變,tsuan pian
軁鑽,nng tsng
醫,i
醬,tsiunn
鎖,so
鎮,tin
闔,khah
雙,siang
雜,tsap
雞,ke
離,li
雞𧉟,ke tai
雙叉路,siang tshe loo
雞公,ke kang
雙手,siang tshiu
雙方,siang hong
離手,li tshiu
雞毛筅,ke mng tshing
雙爿,siang ping
雞仔,ke a
雞仔目,ke a bak
雞仔囝,ke a kiann
雞母,ke bo
雞母皮,ke bo phue
雞母蟲,ke bo thang
醫生,i sing
醬瓜仔,tsiunn kue a
雙生仔,siang senn a
醫生館,i sing kuan
鎮地,tin te
鎮位,tin ui
雞卵,ke nng
離別,li piat
雞卵卷,ke nng kng
雞卵糕,ke nng ko
雞尾脽,ke bue tsui
雞牢,ke tiau
雞鵤仔車,ke kak a tshia
雞卷,ke kng
醫治,i ti
鎖門,so mng
雞屎運,ke sai un
雞胘,ke kian
雙重,siang ting
雙面,siang bin
雙面刀鬼,siang bin to kui
雜差仔工,tsap tshe a kang
醬料,tsiunn liau
雞桃仔,ke tho a
雞胸,ke hing
雞胿,ke kui
雞胿仔,ke kui a
雞酒,ke tsiu
鎖匙,so si
雜唸,tsap liam
離婚,li hun
雜細,tsap se
醫術,i sut
雜貨,tsap hue
雜插,tsap tshap
雙棚鬥,siang penn tau
雞筅,ke tshing
醬菜,tsiunn tshai
離開,li khui
雞僆仔,ke nua a
雞榆,ke jiu
鎮煞,tin suah
雞罩,ke ta
雞腹內,ke pak lai
雞跤爪,ke kha jiau
鎮路,tin loo
雞摸,ke bong
雜種仔,tsap tsing a
雜種仔囝,tsap tsing a kiann
雜誌,tsap tsi
雞箠,ke tshue
離緣,li ian
醫學,i hak
鎮靜劑,tin tsing tse
鎖頭,so thau
雙頭,siang thau
雞髻,ke kue
鎮壓,tin ap
雞翼,ke sit
離離,li li
離離落落,li li lak lak
雞鵤,ke kak
離譜,li phoo
醬鹹,tsiunn kiam
雞籠,ke lam
鞭,pian
鞭,pinn
題,te
額,giah
額,hiah
顏,gan
颺,tshiunn
颺,iann
餾,liu
騎,khia
鬃,tsang
鬆,sang
鬆,song
題目,te bok
颺風,tshiunn hong
颺粟,tshiunn tshik
餾粿,liu kue
題緣,te ian
額頭,hiah thau
颺颺飛,iann iann pue
鯽,tsit
鵝,go
鵤,kak
鯽仔魚,tsit a hi
鮸魚,bian hi
鯉魚,li hi
鯊魚,sua hi
鯊魚煙,sua hi ian
嚨喉,na au
嚨喉空,na au khang
嚨喉蒂仔,na au ti a
懶,lan
攀,phan
攏,lang
攏,long
曝,phak
櫓,loo
櫥,tu
曝日,phak jit
懵仙,bong sian
櫥仔,tu a
曠床,khong tshng
懷念,huai liam
懶屍,lan si
攏是,long si
懷胎,huai thai
寵倖,thing sing
曝乾,phak kuann
曝粟,phak tshik
懷疑,huai gi
攏褲,lang khoo
懵懂,bong tong
攏總,long tsong
懶懶,lan lan
攏權,lang khuan
曝鹽,phak iam
瀨,lua
爍,sih
瓣,ban
礙,gai
礙目,gai bak
瓊花,khing hue
爆炸,pok tsa
礙虐,gai gioh
礙著,gai tioh
爍爁,sih nah
獸醫,siu i
穩,un
簸,pua
簽,tshiam
簾,li
簾,liam
簿,phoo
繩,tsin
繭,kian
繭,king
繳,kiau
羶,hian
羹,kenn
穩心仔,un sim a
簽仔,tshiam a
簿仔,phoo a
簿仔紙,phoo a tsua
簽名,tshiam mia
簽字,tshiam ji
臘肉,lah bah
穩定,un ting
簽約,tshiam iok
穩當,un tang
羅經,lo kenn
羅漢跤仔,lo han kha a
簸箕,pua ki
簸箕甲,pua ki kah
簾簷,ni tsinn
簾簷跤,ni tsinn kha
穩觸觸,un tak tak
藝,ge
藤,tin
藥,ioh
蟶,than
藥丸,ioh uan
藥丹,ioh tan
藥方,ioh hng
藥水,ioh tsui
藥片,ioh phinn
藥仔,ioh a
蠍仔,giat a
藥包,ioh pau
藝旦,ge tuann
藥局,ioh kiok
藥材,ioh tsai
藥房,ioh pang
藥洗,ioh se
藥粉,ioh hun
藥茶,ioh te
藥草,ioh tshau
藥酒,ioh tsiu
藥粕,ioh phoh
藝術,ge sut
藥單,ioh tuann
藥渣,ioh tse
藥鈷仔,ioh koo a
藥膏,ioh ko
藥劑,ioh tse
藥劑師,ioh tse su
藥頭仔,ioh thau a
藥櫥,ioh tu
譀,ham
證,tsing
識,sik
譜,phoo
蹺,khiau
轎,kio
辭,si
辭,su
邊,pian
邊,pinn
證人,tsing jin
邊仔,pinn a
譀古,ham koo
贊同,tsan tong
贊成,tsan sing
贊助,tsan tsoo
辭別,si piat
轎車,kiau tshia
證券,tsing kuan
辭典,su tian
譀呱呱,ham kua kua
證明,tsing bing
證書,tsing su
譀浡,ham phuh
贈送,tsing sang
譀話,ham ue
證據,tsing ki
辭頭路,si thau loo
贊聲,tsan siann
辭職,si tsit
譀譀,ham ham
譀鏡,ham kiann
鏡,kiann
鏢,pio
鏨,tsam
關,kuainn
關,kuan
難,lan
霧,bu
關刀,kuan to
關心,kuan sim
鏨仔,tsam a
鏡台,kiann tai
難免,lan bian
關門,kuainn mng
關係,kuan he
關帝爺,kuan te ia
鏡框,kiann khing
難得,lan tit
關稅,kuan sue
關童,kuan tang
霧嗄嗄,bu sa sa
關節,kuan tsat
關節炎,kuan tsat iam
關落陰,kuan loh im
鏡箱仔,kiann siunn a
鏡頭,kiann thau
鏨頭,tsam thau
霧霧,bu bu
韻,un
願,guan
類,lui
騙,phian
鬍,hoo
騙囡仔,phian gin a
騙局,phian kiok
顛倒,tian to
顛倒,thian thoh
騙鬼,phian kui
願望,guan bong
騙術,phian sut
願意,guan i
饅頭,ban tho
鯪鯉,la li
鬍鬚,hoo tshiu
麴,khak
齁,honn
龐,phiang
鯰魚,liam hi
麒麟,ki lin
勸,khng
勸,khuan
嚴,giam
嚷,jiang
寶,po
孽子,giat tsu
寶貝,po pue
勸和,khng ho
嚴重,giam tiong
嚴格,giam keh
寶惜,po sioh
勸善,khuan sian
嚴肅,giam siok
寶貴,po kui
勸解,khuan kai
寶劍,po kiam
孽潲,giat siau
孽譎仔話,giat khiat a ue
懸,kuan
攔,ann
攕,tshiam
櫳,lang
瀳,tshinn
瀾,nua
爐,loo
獻,hian
癢,tsiunn
懸低,kuan ke
懸山,kuan suann
爐丹,loo tan
攕仔,tshiam a
櫳仔,long a
爐主,loo tsu
櫳仔內,long a lai
瀾垂,nua se
懸度,kuan too
獻計,hian ke
獻敬,hian king
懸價,kuan ke
攕擔,tshiam tann
礤,tshuah
礦,khong
礪,le
礬,huan
籃,na
籃仔,na a
礤冰,tshuah ping
蘆竹,loo tik
礦物,khong but
競爭,king tsing
礦泉水,khong tsuann tsui
籃球,na kiu
籍貫,tsik kuan
籌備,tiu pi
蘆筍,loo sun
蘆黍,loo se
礦業,khong giap
籃層,na tsan
蘆薈,loo hue
礤簽,tshuah tshiam
蘆藤,loo tin
繼續,ke siok
蠓,bang
觸,tak
贏,iann
躄,phih
辮,pinn
蠓仔,bang a
蠘仔,tshih a
蠓仔水,bang a tsui
蠓仔香,bang a hiunn
觸犯,tshiok huan
觸舌,tak tsih
警告,king ko
警戒,king kai
蘋果,phong ko
蘋果檨,phong ko suainn
議長,gi tiunn
譬相,phi siunn
贏面,iann bin
議員,gi uan
覺悟,kak ngoo
議案,gi an
蠓捽仔,bang sut a
警報,king po
譬喻,phi ju
議場,gi tiunn
蘑菇,moo koo
議會,gi hue
蠓罩,bang ta
警察,king tshat
警察局,king tshat kiok
議論,gi lun
譬論講,phi lun kong
覺醒,kak tshenn
蠓蟲,bang thang
鐘,tsing
釋迦,sik khia
飄,phiau
饒,jiau
鰓,tshi
饒命,jiau mia
饒赦,jiau sia
鰇魚,jiu hi
鰇魚羹,jiu hi kenn
飄撇,phiau phiat
鰗鰡,hoo liu
鹹,kiam
麵,mi
黨,tong
齣,tshut
麵包,mi pau
鹹卵,kiam nng
鹹汫,kiam tsiann
麵炙,mi tsia
黨派,tong phai
麵桃,mi tho
麵粉,mi hun
麵茶,mi te
鹹淡,kiam tann
鹹焗雞,kiam kok ke
鹹魚,kiam hi
麵猴,mi kau
鹹菜,kiam tshai
鹹酥雞,kiam soo ke
鹹圓仔,kiam inn a
麵摵仔,mi tshik a
鹹粿,kiam kue
鹹酸甜,kiam sng tinn
麵線,mi suann
麵線糊,mi suann koo
麵擔仔,mi tann a
鹹篤篤,kiam tok tok
麵頭,mi thau
齣頭,tshut thau
麵龜,mi ku
鹹糜,kiam mue
麵麶,mi thi
鹹鰱魚,kiam lian hi
嚾,uang
攑,giah
攝,liap
櫼,tsinn
欄,nua
灇,tsang
灌,kuan
爛,nua
癩𰣻,thai ko
癩𰣻鬼,thai ko kui
癩𰣻爛癆,thai ko nua lo
攑手,giah tshiu
灌水,kuan tsui
欄杆,lan kan
櫻花,ing hue
攝屎,liap sai
犧牲,hi sing
灌風,kuan hong
囂俳,hiau pai
櫻桃,ing tho
爛塗,nua thoo
爛塗糜,nua thoo mue
灌腸,kuan tshiang
灌腸,kuan tng
攑箸,giah ti
爛糊糊,nua koo koo
攑頭,giah thau
攑懸,giah kuan
爛癬,nua sian
攝襇,liap king
纏,tinn
蘭,lan
蠟,lah
襪,bueh
襪仔,bueh a
纏身,tinn sin
蘭花,lan hue
蠟紙,lah tsua
籐條,tin tiau
蠟條,lah tiau
蠟筆,lah pit
纏跤絆手,tinn kha puann tshiu
纏綴,tinn tue
纏線,tinn suann
蠟燭,lah tsik
辯,pian
鐵,thih
露,loo
霸,pa
鐵人,thih lang
護士,hoo su
辯士,pian su
鐵工,thih kang
露水,loo tsui
霸王,pa ong
鐵牛仔,thih gu a
霸占,pa tsiam
鐵甲,thih kah
護身符,hoo sin hu
鐵枋,thih pang
鐵枝,thih ki
鐵枝路,thih ki loo
護法,hoo huat
鐵釘,thih ting
鐵馬,thih be
鐵釘仔,thih ting a
鐵骨仔生,thih kut a senn
鐵桶,thih thang
護理,hoo li
譴責,khian tsik
護照,hoo tsiau
辯解,pian kai
鐵鉎,thih sian
鐵槌,thih thui
辯論,pian lun
鐵齒,thih khi
鐵齒銅牙槽,thih khi tang ge tso
護龍,hoo ling
露營,loo iann
露螺,loo le
鐵櫃,thih kui
躊躇,tiu tu
辯護,pian hoo
辯護士,pian hoo su
響,hiang
顧,koo
鬖,sam
鶴,hoh
顧人怨,koo lang uan
顧三頓,koo sann tng
鬖毛鬼,sam mng kui
鰮仔魚,un a hi
顧門,koo mng
響亮,hiang liang
顧客,koo kheh
顧厝,koo tshu
顧家,koo ke
魔神仔,moo sin a
魔鬼,moo kui
顧問,koo bun
魔術,moo sut
響應,hiang ing
齧,khe
麝香,sia hiunn
囉,lo
囉, looh
囊,long
囊,long
彎,uan
攢,tshuan
攤,thuann
欉,tsang
權,khuan
權力,khuan lik
彎曲,uan khiau
權利,khuan li
彎來斡去,uan lai uat khi
歡迎,huan ging
權威,khuan ui
權限,khuan han
歡送,huan sang
攤販,thuann huan
歡喜,huann hi
囉嗦,lo so
歡頭喜面,huann thau hi bin
歡歡喜喜,huann huann hi hi
彎彎斡斡,uan uan uat uat
灘,thuann
瓤,nng
疊,thah
疊,thiap
癬,sian
癮,gian
籗,khah
籠,lam
籠,lang
籠,lang
籠,lang
籠,lang
籠,long
糴,tiah
聽,thiann
聽,thing
讀,thak
讀,thok
籗仔,khah a
籠仔,lang a
讀冊,thak tsheh
讀冊人,thak tsheh lang
癮仙哥,gian sian ko
讀死冊,thak si tsheh
糴米,tiah bi
籠床,lang sng
讀者,thok tsia
聽香,thiann hiunn
聽候,thing hau
聽喙,thiann tshui
聽著,thiann tioh
癮頭,gian thau
聽講,thiann kong
贖,siok
鑄,tsu
顫,tsun
鬚,tshiu
贖身,siok sin
鑑定,kam ting
驕傲,kiau ngoo
鰱,lian
鰻,mua
鰾,pio
鱉,pih
齪,tsak
鰱魚,lian hi
鱈魚,suat hi
齪嘈,tsak tso
鷓鴣菜,tsia koo tshai
攪,kiau
癰,ing
籤,tshiam
癰仔,ing a
攪吵,kiau tsha
攪絞,kiau ka
籤筒,tshiam tang
戀愛,luan ai
籤詩,tshiam si
攪擾,kiau jiau
纓纏,inn tinn
變,pian
變,pinn
躘,liong
鑢,lu
顯,hian
顯,hiann
驗,giam
驚,kiann
驛,iah
髓,tshue
體,the
驚人,kiann lang
驚人,kiann lang
體力,the lat
變化,pian hua
變心,pian sim
鑢仔,lu a
顯目,hiann bak
驚生份,kiann senn hun
驚死,kiann si
驚死,kiann si
驚死人,kiann si lang
變色,pian sik
驗血,giam hueh
變更,pian king
變步,pian poo
體育,the iok
驚見笑,kiann kian siau
變卦,pian kua
變空,pinn khang
驗屍,giam si
驚某,kiann boo
變面,pinn bin
體面,the bin
體格,the keh
變鬼,pinn kui
變鬼變怪,pinn kui pinn kuai
體統,the thong
躘被,liong phue
變通,pian thong
驚惶,kiann hiann
變款,pian khuan
變猴弄,pinn kau lang
體貼,the thiap
驗傷,giam siong
體會,the hue
顯聖,hian sing
體諒,the liong
體操,the tshau
顯頭,hiann thau
變竅,pian khiau
體驗,the giam
鱖,kue
鱗,lan
鱙仔魚,jiau a hi
鱔魚,sian hi
鱖魚,kue hi
攬,lam
罐,kuan
讓,niu
讖,tsham
靈,ling
靈丹,ling tan
讓手,niu tshiu
罐仔,kuan a
箅仔骨,pin a kut
讓位,niu ui
靈位,ling ui
讓步,niu poo
蠶豆,tshan tau
靈芝,ling tsi
靈厝,ling tshu
靈通,ling thong
讓渡,jiong too
靈感,ling kam
靈聖,ling siann
靈魂,ling hun
罐頭,kuan thau
韆鞦,tshian tshiu
靈驗,ling giam
鱟,hau
鷹,ing
鹼,kinn
鹽,iam
齆,ang
齴,giang
鱟𣁳仔,hau khat a
齴牙,giang ge
鹼仔粿,kinn a kue
鬢角,pin kak
鹽花仔,iam hue a
鹽埕,iam tiann
鱟桸,hau hia
鬢跤,pin kha
鹼粽,kinn tsang
鹽酸,iam sng
齆鼻,ang phinn
齆鼻聲,ang phinn siann
齆聲,ang siann
鹽甕仔,iam ang a
鬢繐,pin sui
鬢邊,pin pinn
齷齪,ak tsak
廳,thiann
灣,uan
糶,thio
糶米,thio bi
籬笆,li pa
廳堂,thiann tng
廳頭,thiann thau
襻,phan
跕,liam
躡,neh
鑱,tshim
饞,sai
鑱仔,tshim a
蠻皮,ban phue
蠻皮癬,ban phue sian
觀光,kuan kong
觀念,kuan liam
觀前顧後,kuan tsing koo au
觀音,kuan im
饞食,sai tsiah
觀音竹,kuan im tik
躡跤尾,neh kha bue
觀察,kuan tshat
讚,tsan
驢,li
鬮,khau
驢仔,li a
鑼,lo
鑽,tsng
鱸,loo
鑽仔,tsng a
鑽耳,tsng hinn
鑽空,tsng khang
鱷魚,khok hi
鱸魚,loo hi
鑼鼓,lo koo
鸕鶿,loo tsi
鱸鰻,loo mua
戇,gong
鑿,tshak
戇人,gong lang
戇大呆,gong tua tai
鑿仔,tshak a
鑿目,tshak bak
戇呆,gong tai
戇的,gong e
戇直,gong tit
鸚哥,ing ko
鸚哥鼻,ing ko phinn
戇神,gong sin
戇猴,gong kau
戇想,gong siunn
戇話,gong ue
戇錢,gong tsinn
戇頭戇面,gong thau gong bin
戇膽,gong tann
戇戇,gong gong
鑿鑿,tshak tshak
鬱,ut
鬱卒,ut tsut
鬱傷,ut siong
鬱歲,ut hue
廍,phoo
揻,ui
砛,gim
砛仔,gim a
砛簷,gim tsinn
硓𥑮石,loo koo tsioh
粩,lau
襇,king
贌,pak
贌田,pak tshan
蹽,liau
蹽溪仔,liau khe a
蹽落去,liau loh khi
躼,lo
躼跤,lo kha
躼跤仔,lo kha a
㧎,khe
㧣,tu
㨂,tang
㨨,liu
𠯗,tsip
𠯗一下,tsip tsit e
㤉,ge
㤉潲,ge siau
䀐,siam
㾀,khiap
㾀勢,khiap si
㾀勢命,khiap si mia
㧻,tok
𧉟,tai
䘥仔,kah a
𢯾,mooh
𢯾壁鬼,mooh piah kui
𠞩,tsui
𠞭,lio
𠢕,gau
𠢕人,gau lang
𠢕早,gau tsa
𠢕吮食,gau tshng tsiah
𠢕開,gau khai
㔂,lan
㔂甘蔗,lan kam tsia
𢲸,loo
𨂿,uainn
𨂿著,uainn tioh
䫌,phue
𢼌,pa
𣮈頭山,khut thau suann
𩑾,tshih
𡳞,lan
𡳞𦉎,lan sui
𡳞核,lan hut
𡳞神,lan sin
𡳞脬,lan pha
𡳞鳥,lan tsiau
𡳞蔓,lan mua
𩵱,ngoo
𩵱仔,ngoo a
𪁎,tshio
𪁎哥,tshio ko
𪁎趒,tshio tio
𪁎雞,tshio ke
𩛩,kauh
𩛩肥,kauh pui
𥐵,phiat
𥐵仔,phiat a
𡢃,kan
𥰔,phin
𥰔仔,phin a
𥴊,kam
𥴊仔,kam a
𥴊仔店,kam a tiam
𥴊壺,kam oo
䖙,the
䖙椅,the i
𤆬,tshua
𤆬路,tshua loo
𤆬路雞,tshua loo ke
𤆬頭,tshua thau
䘼,ng
䆀,bai
䆀才,bai tsai
䆀手,bai tshiu
䆀味,bai bi
䆀指,bai tsainn
䆀猴,bai kau
𨑨迌,tshit tho
𨑨迌人,tshit tho lang
𨑨迌囡仔,tshit tho gin a
𨑨迌物,tshit tho mih
𨑨迌物仔,tshit tho mih a
𨑨迌查某,tshit tho tsa boo
𥍉,liap
𥍉,nih
𥍉𥍉看,nih nih khuann
𥍉目,nih bak
𤉙,kun
㨑,tsang
𣛮,siann
𣛮籃,siann na
𤶃,thiau
𤶃仔,thiau a
𧮙,tshoh
𪐞,too
𪐞紙,too tsua
𤲍,kheh
𤲍燒,kheh sio
𦊓,ling
㴘,bau
㴘麵,bau mi
䖳,the
𩸙,tai
𩸙仔,tai a
㧒,hiat
䠡,tshe
𩚨,khiu
𩚨嗲嗲,khiu teh teh
㧌,mau
𣁳,khat
𣁳仔,khat a
㨻,tsann
㨻魚,tsann hi
𧿳𧿳跳,phut phut thiau
𧌄蜅蠐,am poo tse
必,pit
必叉,pit tshe
必痕,pit hun
必開,pit khui
䢢拄䢢,tshiang tu tshiang
㴙㴙落,tshap tshap loh
㴙㴙滴,tshap tshap tih
𪜶,in
𠕇,ting
𠕇硞硞,ting khok khok
𠕇篤,ting tauh
𤺪,sian
𧿬,thun
𧿬踏,thun tah
𢪱,but
𣻸,siunn
㽎,sim
𦜆,ham
寢,tshim
𨂾,lam
𫝏,gan
𫝏水,gan tsui
𫝏鋼,gan kng
𫝺,hiu
𫞼,tshai
𫝻,hue
𫟂,han
霧水,bu tsui
𫝛,siang
𫝛人,siang lang
𫝛勻,siang un
𫝛年,siang ni
𫝛時,siang si
𫝛途,siang too
𫝛款,siang khuan
𬦰,peh
𬦰山,peh suann
𬦰樓梯,peh lau thui
𬦰懸𬦰低,peh kuan peh ke
黃梔仔花,ng ki a hue
塌,lap
娘囝,niu kiann
揜貼,iap thiap
腥,tshenn
撇步,phiat poo
跤,kha
嫣,ian
中央,tiong ng
託,thok
奶,ne
物仔,mih a
袂翻捙,be huan tshia
坦笑,than tshio
水沖,tsui tshiang
肥朒朒,pui tsut tsut
一口灶,tsit khau tsau
一大拖,tsit tua thua
大伯仔,tua peh a
大端,tai tuan
小食,sio tsiah
山空,suann khang
山球,suann kiu
山腹,suann pak
五四三,goo si sann
內山斗底,lai suann tau te
內籬仔,lai li a
公道人,kong to lang
勼跤勼手,kiu kha kiu tshiu
反起反倒,huan khi huan to
心內話,sim lai ue
手形,tshiu hing
手捗,tshiu poo
手梳攑懸,tshiu se giah kuan
月內人,gueh lai lang
毋是款,m si khuan
水崩山,tsui pang suann
水跤,tsui kha
火引,hue in
王見王,ong kian ong
冬筍,tang sun
枷車藤,kha tshia tin
半中央,puann tiong ng
半晝,puann tau
外才,gua tsai
布棚,poo penn
平階,penn kai
必巡,pit sun
本居地,pun ki te
白墨,peh bak
交仗,kau tiong
伨頭,thin thau
先的,sian e
好得,ho tit
字姓,ji senn
竹管仔飯,tik kong a png
考試單,kho tshi tuann
自本,tsu pun
卵殼,nng khak
含血霧天,kam hueh bu thinn
扳仔,pan a
抑無,iah bo
汫水,tsiann tsui
沙耙,sua pe
牢鼎,tiau tiann
芒種雨,bong tsing hoo
事事項項,su su hang hang
佮股,kap koo
奉待,hong thai
孤查某囝,koo tsa boo kiann
定親,ting tshin
抾丁錢,khioh ting tsinn
拊仔,hu a
拍火車,phah hue tshia
明品,bing phin
肥底,pui te
芥辣,kai luah
門栱,mng kong
門擋仔,mng tong a
雨撇仔,hoo phiat a
前世人,tsing si lang
厚操煩,kau tshau huan
巷仔口,hang a khau
後過,au kue
怨天怨地,uan thinn uan te
拜六,pai lak
拜請,pai tshiann
按呢生,an ne senn
挕捒,hinn sak
活魚栽,huat hi tsai
活賣,uah be
相𤆬,sio tshua
相罵本,sio me pun
胃慒慒,ui tso tso
重本,tang pun
食好料,tsiah ho liau
個外月,ko gua gueh
倒退攄,to the lu
厝邊兜,tshu pinn tau
厝邊隔壁,tshu pinn keh piah
原性,guan sing
捀場,phang tiunn
捎無摠,sa bo tsang
海坪,hai phiann
烏點,oo tiam
疼心,thiann sim
疼命命,thiann mia mia
納數,lap siau
紙敬,tsua king
臭香,tshau hiunn
草仔粿,tshau a kue
袂赴市,be hu tshi
袂得,be tit
起帆,khi phang
起磅,khi pong
起戇,khi gong
高長,kau tshiang
鬥榫,tau sun
唸謠,liam iau
啉酒醉,lim tsiu tsui
帶身人,tai sin lang
徛台,khia tai
捽繩,sut tsin
接神,tsih sin
晚冬,mng tang
涼的,liang e
淋碭,lam thng
淘井,to tsenn
深山林內,tshim suann na lai
淺緣,tshian ian
猛掠,me liah
終其尾,tsiong ki bue
透抽,thau thiu
通人知,thong lang tsai
鹿角龜,lok kak ku
喝起喝倒,huah khi huah to
媠面,sui bin
尊存,tsun tshun
掣一趒,tshuah tsit tio
插濫,tshap lam
棧間,tsan king
欹空,khia khang
湢,pih
無天良,bo thian liong
無捨施,bo sia si
無盤,bo puann
猫仔,ba a
琴子,khim ji
番薯稜,han tsi ling
發財仔車,huat tsai a tshia
發輦,huat lian
睏一醒,khun tsit tshenn
睏中晝,khun tiong tau
短站,te tsam
短褲節仔,te khoo tsat a
硩年錢,teh ni tsinn
窗仔簾,thang a li
筊場,kiau tiunn
筍龜,sun ku
菜販仔,tshai huan a
開仔,khui a
開聲,khui siann
閒身,ing sin
黃酸雨,ng sng hoo
剾痧,khau sua
塗州,thoo tsiu
塗沙粉,thoo sua hun
塗豆麩,thoo tau hu
塗質,thoo tsit
塗糜,thoo mue
搝票,khiu phio
搶市,tshiunn tshi
新正年頭,sin tsiann ni thau
會失禮,hue sit le
會記得,e ki tit
煙暈,ian ng
煞尾仔囝,suah bue a kiann
照電光,tsio tian kong
禁薰,kim hun
萬事通,ban su thong
落人,lau lang
落台,loh tai
賊仔車,tshat a tshia
跤尾紙,kha bue tsua
跤後曲,kha au khiau
跤捗,kha poo
跤麻手痺,kha ba tshiu pi
路尾,loo bue
過路人,kue loo lang
過暝,kue me
電火線,tian hue suann
電光片,tian kong phinn
電眼,tian gan
靴管,hia kong
鼎筅,tiann tshing
嘔酸水,au sng tsui
實䈄,tsat ham
實頭,tsat thau
對相,tui siong
對頭親,tui thau tshin
歌詩,kua si
滾耍笑,kun sng tshio
滾絞疼,kun ka thiann
漚肥,au pui
漚屎,au sai
漢學仔先,han oh a sian
算會和,sng e ho
管仔粿,kong a kue
粿模,kue boo
綠豆膨,lik tau phong
網仔門,bang a mng
網紗油,bang se iu
認命,jin mia
踅頭,seh thau
銅管仔車,tang kong a tshia
影跡,iann tsiah
撐渡,the too
樂跎,lok to
樓栱,lau kong
磅針,pong tsiam
箭竹仔筍,tsinn tik a sun
蔭瓜仔,im kue a
蝦笱,he ko
衛生箸,ue sing ti
調羹仔,thau king a
豬血粿,ti hueh kue
餒志,lue tsi
擔仔,tann a
擔罪,tann tsue
澹水地,tam tsui te
糖粿,thng kue
貓貓相,niau niau siong
頭轉客,thau tng kheh
麭,phang
䆀空,bai khang
嚇嚇叫,heh heh kio
戲台,hi tai
糞埽市仔,pun so tshi a
總講一句,tsong kong tsit ku
總攬,tsong lam
趨冰,tshu ping
繞境,jiau king
舊漚舊臭,ku au ku tshau
雜菜麵,tsap tshai mi
離跤手,li kha tshiu
懶性,nua sing
曠闊,khong khuah
羹飯,kenn png
藥水布,ioh tsui poo
顛倒反,tian to ping
觸纏,tak tinn
鰇魚鬚,jiu hi tshiu
鹹水,kiam tsui
鹹水魚,kiam tsui hi
鹹光餅,kiam kong piann
鹹梅,kiam mue
鹹膎,kiam ke
攑頭香,giah thau hiunn
譴損,khian sng
聽筒,thiann tang
罐頭開仔,kuan thau khui a
戇工,gong kang
鬱拗,ut au
鬱熱,ut juah
𤺪雨,sian hoo
𫝏錢,gan tsinn
酒甜,tsiu tinn
菜鹹,tshai kiam
羹麵,kenn mi
山崎,suann kia
一疕仔,tsit phi a
一必一中,it pit it tiong
七月半,tshit gueh puann
七晏八晏,tshit uann peh uann
人額,lang giah
人懸漢大,lang kuan han tua
入心,jip sim
刀鋩,to me
力草,lat tshau
三角六肩,sann kak lak king
上尾,siong bue
上教,tsiunn ka
上無,siong bo
下晝頓,e tau tng
久年,ku ni
大人大種,tua lang tua tsing
大水柴,tua tsui tsha
大出,tua tshut
大出手,tua tshut tshiu
大目孔,tua bak khong
大百,tua pah
大灶,tua tsau
大身大命,tua sin tua mia
大注,tua tu
大肥,tua pui
大張的,tua tiunn e
大細腎,tua se sian
大漢囝,tua han kiann
大翻頭,tua huan thau
大嚨喉空,tua na au khang
砂馬仔,sua be a
中中仔,tiong tiong a
中範,tiong pan
五子直,goo ji tit
仁仁仁,jin jin jin
冇粟,phann tshik
反口供,huan khau king
反形,huan hing
反種,huan tsing
反變,ping pinn
天公地道,thinn kong te to
天公伯仔,thinn kong peh a
天平,thian ping
天狗食日,thian kau tsiah jit
少年人,siau lian lang
少歲,tsio hue
引𤆬,in tshua
心狂火熱,sim kong hue jiat
心花開,sim hue khui
心慒慒,sim tso tso
手爪賤,tshiu jiau tsian
手股頭,tshiu koo thau
手後曲,tshiu au khiau
手面趁食,tshiu bin than tsiah
手賤,tshiu tsian
手蹄仔,tshiu te a
手縫櫳,tshiu phang lang
月圍箍,gueh ui khoo
歹日,phainn jit
歹吉兆,phainn kiat tiau
歹物仔,phainn mih a
歹看面,phainn khuann bin
歹面,phainn bin
歹面相看,phainn bin sio khuann
歹紡,phainn phang
歹價,phainn ke
毋成囡仔,m tsiann gin a
水尺,tsui tshioh
水泱,tsui iann
水租,tsui tsoo
水脈,tsui meh
水碓,tsui tui
水窟仔,tsui khut a
水鉎,tsui sian
水濺仔,tsui tsuann a
火母,hue bo
火車母,hue tshia bo
火車頭,hue tshia thau
火金星,hue kim tshenn
火烌性,hue hu sing
火珠仔,hue tsu a
牛角𨂿仔,gu kak uainnh a
牛貫,gu kng
牛聲馬喉,gu siann be au
王梨酥,ong lai soo
主顧客,tsu koo kheh
仝心,kang sim
仝沿,kang ian
冊局,tsheh kiok
冊疊仔,tsheh thiap a
冬粉,tang hun
出擢,tshut tioh
半丁,puann ting
半奸忠,puann kan tiong
半老老,puann lo lau
半遂,puan sui
去倒,khi to
可取,kho tshu
司公仔象桮,sai kong a siunn pue
外埠頭,gua poo thau
央倩,iang tshiann
央教,iang kah
布幼仔,poo iu a
布攄仔,poo lu a
平洋,penn iunn
正範,tsiann pan
生本,senn pun
生真,tshenn tsin
生張,senn tiunn
生頭凊面,tshenn thau tshin bin
白目,peh bak
白虎湯,peh hoo thng
白菜滷,peh tshai loo
白話字,eh ue ji
目孔,bak khong
目空赤,bak khang tshiah
目睭遮,bak tsiu jia
石花,tsioh hue
石降,tsioh kang
石磨仔心,tsioh bo a sim
交落身,ka lauh sin
交落枕,ka lauh tsim
交繃,kau penn
交纏,kau tinn
冰礤,ping tshuah
合該,hap kai
囡仔頭王,gin a thau ong
在室的,tsai sik e
在膽,tsai tann
在欉的,tsai tsang e
地陷,te ham
好日,ho jit
好代,ho tai
好玄,honn hian
好份,ho hun
好死毋死,ho si m si
好看頭,ho khuann thau
好唯是,ho bi si
字勻,ji un
安太歲,an thai sue
成格,tshiann kik
收煞,siu suah
有路無厝,u loo bo tshu
有賰,u tshun
死殗殗,si gian gian
死鹹,si kiam
死體,si the
百百款,pah pah khuan
百面,pah bin
竹田嬰,tik tshan enn
竹模,tik boo
竹篙厝,tik ko tshu
竹雞仔車,tik ke a tshia
老孤𣮈,lau koo khut
肉幼仔,bah iu a
肉糋,bah tsinn
肉繭仔,bah kian a
自早,tsu tsa
自作自專,tsu tsok tsu tsuan
自家用的,tsu ka iong e
血崩山,hueh pang suann
行去,kiann khi
行袂開跤,kiann be khui kha
行船人,kiann tsun lang
行跤花,kiann kha hue
伸捙,tshun tshia
低路師,ke loo sai
占贏,tsiam iann
佗落,to loh
佛手柑,hut tshiu kam
冷嗽,ling sau
卵白質,nng peh tsit
呔會,thai e
囤貨,tun hue
囥話,khng ue
坉錢,thun tsinn
坐毋著,tshe m tioh
坐底,tshe te
妝娗,tsng thann
孝尾囝,ha bue kiann
孝男面,hau lam bin
尾來,bue lai
尿滓,jio tai
忘恩背義,bong un pue gi
李仔攕,li a tshiam
汫水魚,tsiann tsui hi
牢腹,tiau pak
罕罕仔,han han a
育𤆬,io tshua
見效,kian hau
角蜂,kak phang
豆仔魚,tau a hi
赤焱焱,tshiah iann iann
走水,tsau tsui
街路,ke loo
走無路,tsau bo loo
走腹,tsau pak
走標,tsau pio
走學,tsau oh
走縒,tsau tsuah
辛苦病疼,sin khoo penn thiann
車斗,tshia tau
車母,tshia bu
車前草,ki tsian tshau
車路,tshia loo
到手芳,to tshiu phang
到尾,kau bue
卸世卸眾,sia si sia tsing
呼請,hoo tshiann
咇噗跳,phih phok thiau
和齊,ho tse
孤佬,koo lau
孤鳥,koo tsiau
孤跤手,koo kha tshiu
宕,thong
定貨,tiann hue
彼當陣,hit tang tsun
往診,ong tsin
抹烏,buah oo
抽懸,thiu kuan
抾肉幼仔,khioh bah iu a
拄咧,tu teh
拆白講,thiah peh kong
拍火,phah hue
拍速,phah sok
拍鳥帽,phah tsiau bo
放目,pang bak
放伴,pang phuann
放紙虎,pang tsua hoo
放送頭,hong sang thau
放銃,pang tshing
果子栽,kue tsi tsai
武車,bu tshia
炊粉,tshue hun
狀元粿,tsiong guan kue
狗鯊,kau sua
直目,tit bak
空思夢想,khong su bong siong
空殼厝,khang khak tshu
股仔囝,koo a kiann
花眉,hue bi
花飛,hue hui
花條馬,hue tiau be
花蛤仔,hue kap a
金光黨,kim kong tong
金金相,kim kim siong
金絲猴,kim si kau
金鑠鑠,kim siak siak
長志,tsiang tsi
長篙形,tng ko hing
門口埕,mng khau tiann
文光尺,bun kong tshioh
門後臼,mng au khu
𤆬領,tshua nia
𨑨迌印仔,tshit tho in a
侵門踏戶,tshim mng tah hoo
俗麭,siok phang
保領,po nia
南北二路,lam pak ji loo
咬舌,ka tsih
咱人,lan lang
品並,phin phing
客滿,kheh buan
封頭壁,hong thau piah
屎面,sai bin
巷仔內的,hang a lai e
後壁山,au piah suann
後謝,au sia
硩墓紙,teh bong tsua
指甲眉,tsing kah bai
指模,tsi boo
挑花刺繡,thio hue tshiah siu
是講,si kong
枵飢失頓,iau ki sit tng
枵過飢,iau kue ki
枵燥,iau so
柝仔頭,khok a thau
查某囝日,tsa boo kiann jit
柿霜,khi sng
流汗流洘,lau kuann lau kho
為非糝做,ui hui sam tso
相伨,sio thin
相揣,sio tshue
看口,khuann khau
看命,khuann mia
看破跤手,khuann phua kha tshiu
看袂上目,khuann be tsiunn bak
突顯,tut hian
紀年,khi ni
紅霞,ang he
美國仙丹,bi kok sian tan
美國時間,bi kok si kan
美國塗豆,bi kok thoo tau
背骨,pue kut
苦瓜封,khoo kue hong
苦花,khoo hue
苦齣,khoo tshut
迫促,pik tshik
郊,kau
限時批,han si phue
面冊,bin tsheh
面腔,bin tshiunn
面漚面臭,bin au bin tshau
面模,bin boo
風雷,hong lui
食人夠夠,tsiah lang kau kau
食老出癖,tsiah lau tshut phiah
食重鹹,tsiah tang kiam
食風,tsiah hong
食茶,tsiah te
食罪,tsiah tsue
食認,tsiah jin
食銅食鐵,tsiah tang tsiah thih
食餐廳,tsiah tshan thiann
食聲,tsiah siann
香櫞瓜,hiunn inn kue
倒吊子,to tiau tsi
倒拗,to au
倒頭槌,to thau thui
倒轉去,to tng khi
倚意,ua i
倚蹛,ua tua
凌勒,ling lik
厝尾頂,tshu bue ting
厝場,tshu tiunn
原全,guan tsuan
哪通,na thang
哽胿,kenn kui
套頭話,tho thau ue
師仔工,sai a kang
挨磨,e bo
挩鍊仔,thuah lian a
挽瓜揫藤,ban kue tshiu tin
挽筋,ban kin
捙倒,tshia to
料小,liau siau
時計果,si ke ko
柴目,tsha bak
柴箍,tsha khoo
梳妝打扮,se tsng tann pan
氣掣掣,khi tshuah tshuah
氣暢忍,khi thiong lun
消敨,siau thau
烏子仔菜,oo tsi a tshai
烏白切,oo peh tshiat
烏尾冬,oo bue tang
烏面賊,oo bin tshat
烏鉎,oo sian
珠仔龜,tsu a ku
病母,penn bo
病囝,penn kiann
眩車丹,hin tshia tan
破功,pho kong
破豆,pho tau
破鼎,phua tiann
祖公仔產,tsoo kong a san
笑微微,tshio bi bi
笑詼齣,tshio khue tshut
納錢,lap tsinn
罟寮,koo liau
臭油餲,tshau iu ai
茫茫渺渺,bong bong biau biau
茶米茶,te bi te
茶洗,te se
茶籗,te khah
草仔子,tshau a tsi
草地倯,tshau te song
草囷,tshau khun
草笠仔,tshau leh a
荏身命,lam sin mia
袂拄好,be tu ho
袂做得,be tso tit
袂博假博,be phok ke phok
袂磕得,be khap tit
袂曉衰,be hiau sue
記認,ki jin
貢糖,kong thng
起豹飆,khi pa pio
起酒痟,khi tsiu siau
起蛟龍,khi kau ling
迵海,thang hai
退流,the lau
退時,the si
酒矸仔嫂,tsiu kan a so
馬花糋,be hue tsinn
鬥搭,tau tah
鬼頭刀,kui thau to
㨂甲,tang kah
偌久,gua ku
做水,tso tsui
做囮,tso bue
做竅,tso khio
剪仔龜,tsian a ku
剪絨仔花,tsian jiong a hue
剪蟲,tsian thang
參仔氣,sim a khui
國校,kok hau
夠月,kau gueh
宿題,siok te
寄罪,kia tsue
寄跤,kia kha
密密是,bat bat si
徙岫,sua siu
徛秋,khia tshiu
徛家厝,khia ke tshu
惜花連盆,sioh hue lian phun
捾定,kuann tiann
推捒,the sak
敗馬,pai be
梅仔茶,mue a te
欲晝仔,beh tau a
涵空龜,am khang ku
涼腔,liang khiang
深目,tshim bak
深緣,tshim ian
清彩,tshing tshai
清飯,tshing png
爽歪歪,song uainn uainn
牽龜落湳,khan ku loh lam
窒車,that tshia
笨跤笨手,pun kha pun tshiu
粗殘,tshoo tshan
紲落來,sua loh lai
規工,kui kang
規家伙仔,kui ke hue a
規碗捀,kui uann phang
規嚾規黨,kui uang kui tong
設使,siat su
豚母,thun bu
軟市,nng tshi
透底,thau te
透濫,thau lam
逐工,tak kang
頂下歲,ting e hue
魚酥,hi soo
鳥隻,tsiau tsiah
鳥鼠仔色,niau tshi a sik
鳥鼠仔糖,niau tshi a thng
備辦,pi pan
博士博,phok su phok
喊,han
喋詳,thih siong
喙笑目笑,tshui tshio bak tshio
喙桮,tshui pue
喙齒縫,tshui khi phang
報戶口,po hoo khau
報鳥鼠仔冤,po niau tshi a uan
寒酸,han suan
惡人無膽,ok lang bo tann
惡質,ok tsit
提囡仔,theh gin a
敢是,kam si
敢是,kann si
敨放,thau pang
斑芝,pan tsi
智覺,ti kak
棉仔枝,mi a ki
欺貧重富,khi pin tiong hu
殘殘,tshan tshan
湠根,thuann kin
湳仔地,lam a te
湳塗,lam thoo
無才,bo tsai
無品,bo phin
番薯仔囝,han tsi a kiann
痛疼,thang thiann
痟狗病,siau kau penn
發爐,huat loo
睏尾,khun bue
睏癖,khun phiah
硩注,teh tu
硩番薯,teh han tsi
硬拗,nge au
硬插,nge tshah
筅黗,tshing thun
粟埕,tshik tiann
粟種,tshik tsing
翕汗,hip kuann
菜市仔名,tshai tshi a mia
菜宅,tshai theh
菜砧,tshai tiam
菜蟲,tshai thang
著獎,tioh tsiong
著觸,tioh tak
覕鬚,bih tshiu
詞彙,su lui
買手,be tshiu
貿貨底,bau hue te
跋感情,puah kam tsing
跙流籠,tshu liu long
鈍目,tun bak
閒煩,ing huan
韌命,jun mia
順行,sun kiann
黃目子,ng bak tsi
催油,tshui iu
剾刀蔫,khau to lian
塗石流,thoo tsioh lau
塗肉,thoo bah
媽祖婆,ma tsoo po
幌頭,hainn thau
想欲,siunn beh
搝後跤,khiu au kha
搭胸坎,tah hing kham
搵料,un liau
摁,hmh
摃球,kong kiu
摃鼓,kong koo
暗安,am an
暗唸,am liam
暗會,am hue
會毋著,hue m tioh
會得過,e tit kue
會跤,hue kha
極加,kik ke
歇涼,hioh liang
歇睏日,hioh khun jit
歇睏時仔,hioh khun si a
準拄煞,tsun tu suah
溜旋,liu suan
煎粿,tsian kue
煙筒管,ian tang kong
煞煞去,suah suah khi
矮仔冬瓜,e a tang kue
矮鼓,e koo
矮頓,e tng
碎鹽鹽,tshui iam iam
禁尿,kim jio
腰痠背疼,io sng pue thiann
腹腸,pak tng
萬丈深坑,ban tng tshim khenn
萬不幸,ban put hing
落山,loh suann
落貨,loh hue
落漆,lak tshat
便若,pian na
香芳,hiunn phang
倚山食山,ua suann tsiah suann
哭賴,khau lua
恩情人,un tsing lang
挨挨陣陣,e e tin tin
浮浪貢,phu long kong
蒂頭,ti thau
號頭,ho thau
蜂蝦,phang he
話仙,ue sian
詼諧,khue hai
詼諧,khue hai
跤胴,kha tang
路草,loo tshau
跳踢,thiau thah
過鹹水的,kue kiam tsui e
閘雨棚,tsah hoo penn
隔工,keh kang
電子批,tian tsu phue
電頭毛店,tian thau mng tiam
頓蹬,tun tenn
飽漿,pa tsiunn
𠞭花,lio hue
嗺,sui
墓紙,bong tsua
寢頭,tshim thau
對同,tui tang
對重,tui tiong
對頭風,tui thau hong
對頭誤,tui thau goo
摔大眠,siang tua bin
斡角,uat kak
歌仔冊,kua a tsheh
歌仔先,kua a sian
滸苔,hoo thi
漚古,au koo
漚步,au poo
漚屎步,au sai poo
漚戲拖棚,au hi thua penn
漳泉濫,tsiang tsuan lam
粿路,kue loo
粿酺,kue poo
綿精,mi tsinn
緊氣,kin khui
緊縒慢,kin tsuah ban
蓋蠟,kai lah
認捌,jin bat
趖跤趖手,so kha so tshiu
輕便車,khing pian tshia
噗仔聲,phok a siann
墜腸,tui tiong
撨徙,tshiau sua
佈田花,poo tshan hue
步頻,poo pin
槺榔,khong long
稽考,khe kho
練仙,lian sian
蓮花頭,lian hue thau
蔥仔餅,tshang a piann
蝦卷,he kng
蝦蛄頭,he koo thau
諒情,liong tsing
論真,lun tsin
豬母癲,ti bo tian
豬屠,ti too
閬雨縫,lang hoo phang
閬港,lang kang
靠傷,kho siong
駐水,tu tsui
鬧猜猜,nau tshai tshai
噪耳,tsho hinn
噸,tong
樹奶束仔,tshiu ling sok a
樹梅,tshiu m
激骨話,kik kut ue
燃水,hiann tsui
燈仔花,ting a hue
燒烘烘,sio hong hong
燒唿唿,sio hut hut
燖補,tim poo
磚仔窯,tsng a io
糖仔,thng a
縛跤縛手,pak kha pak tshiu
聬儱,ang lang
褪毛,thng mng
親疊親,tshin thah tshin
賴賴趖,lua lua so
鋸屑烌,ki sut hu
錢貫,tsinn kng
踮沬,tiam bi
擇,toh
無底代,bo ti tai
霎霎仔雨,sap sap a hoo
頭兄,thau hiann
頭較大身,thau khah tua sin
頭旗,thau ki
頭篩仔,thau thai a
頷頸珠,am kun tsu
鴨雄仔聲,ah hing a siann
龜龜鱉鱉,ku ku pih pih
䆀豆仔,bai tau a
䆀氣,bai khui
戲籠,hi lang
戴小鬼仔殼,ti siau kui a khak
簇,tshok
總的,tsong e
臨時臨曜,lim si lim iau
蹓,lau
隱痀橋,un ku kio
鮢鱖,tsu kue
點拄,tiam tuh
擺撥,pai puah
舊底,ku te
舊症頭,ku tsing thau
薰觳仔,hun khok a
藏鏡人,tsong kiann jin
蟳膏,tsim ko
蹛院,tua inn
轉錢空,tng tsinn khang
雙糕潤,siang ko jun
雜貨仔店,tsap hue a tiam
離經,li king
緣金,ian kim
懵膽,bong tann
藥頭,ioh thau
鏨頭短命,tsam thau te mia
麒麟鹿,ki lin lok
懸頂,kuan ting
蠓仔薰,bang a hun
鹹酸苦汫,kiam sng khoo tsiann
攑香綴拜,giah hiunn tue pai
攑旗軍仔,giah ki kun a
灇水,tsang tsui
爛𤶃仔,nua thiau a
癩𰣻病,thai ko penn
癩𰣻蛾仔,thai ko iah a
雞豚仔,ke thun a
鐵釘挽,thih ting ban
鐵掃帚,thih sau tshiu
鐵鉼,thih phiann
鐵撬,thih kiau
鐵鍤,thih tshiah
顧暝,koo me
儼硬,giam nge
籠面,lang bin
聽好,thing ho
變工藝,pinn kang ge
變弄,pinn lang
變相,pian siong
變啥魍,pinn siann bang
變無魍,pinn bo bang
鑢卡,lu khah
豔色,iam sik
鷹仔目,ing a bak
鹽桑仔,iam sng a
鹽酸仔,iam sng a
鑽水沬,tsng tsui bi
戇目,gong bak
𣻸塌塌,siunn lap lap
食飯會,tsiah png hue
金言玉語,kim gian giok gi
好食睏,ho tsiah khun
隨人食,sui lang tsiah
渡鳥,too tsiau
喙䫌肉,tshui phue bah
大趁錢,tua than tsinn
狗肉數,kau bah siau
落空車,lau khang tshia
做肉餅,tso bah piann
無局,bo kiok
水浸粿,tsui tsim kue
天公仔囝,thinn kong a kiann
一時仔,tsit si a
入去,jip khi
入來,jip lai
大水,tua tsui
大的,tua e
細的,se e
山內,suann lai
心內,sim lai
毋就,m to
以早,i tsa
出在,tshut tsai
巧神,khiau sin
目尾,bak bue
好好仔,ho ho a
好命,ho mia
有時,u si
官廳,kuann thiann
拄拄,tu tu
爸仔囝,pe a kiann
相𤆬走,sio tshua tsau
食飽,tsiah pa
厝裡,tshu li
翁仔某,ang a boo
做伴,tso phuann
偷偷仔,thau thau a
唸歌,liam kua
堅心,kian sim
通人,thong lang
逐項,tak hang
無夠,bo kau
著愛,tioh ai
想講,siunn kong
膽肝,tam kuann
雞卵面,ke nng bin
雞卵清,ke nng tshing
面肉,bin bah
苧,te
稈,kuainn
稜,ling
騰,thing
㧣風,tu hong
袂爽,be song
小使仔,siau su a
大細聲,tua se siann
大墓公,tua bong kong
歹鬼𤆬頭,phainn kui tshua thau
歹過,phainn kue
另工,ling kang
出破,tshut phua
半精肥,puann tsiann pui
巧氣,khiau khi
仿仔,hong a
交定,kau tiann
字目,ji bak
伸輪,tshun lun
別工,pat kang
呔,thai
走斜,tsau tshuah
坦斜,than tshuah
姑不將,koo put tsiong
怪奇,kuai ki
拄仔,tu a
抾金,khioh kim
花貓貓,hue niau niau
花彔彔,hue lok lok
花哩囉,hue li lo
後日仔,au jit a
後改,au kai
家私頭仔,ke si thau a
挐絞絞,ju ka ka
缺欠,khueh khiam
紙條仔,tsua tiau a
臭礬,tshau huan
滇流,tinn lau
細漢的,se han e
船桮,tsun pue
頂回,ting hue
頂改,ting kai
喜事,hi su
散食,san tsiah
猴死囡仔,kau si gin a
塗牛翻身,thoo gu huan sin
塌縫,thap phang
痲仔,mua a
幔被仔,mua phue a
廟口,bio khau
講耍笑,kong sng tshio
霜仔枝,sng a ki
擲捒,tan sak
轉成,tng tsiann
襟胸,khim hing
騙痟的,phian siau e
譬論,phi lun
顧更,koo kenn
後回,au hue
會和,e ho
偷走學,thau tsau oh
倒勼,to kiu
祖公仔屎,tsoo kong a sai
結嚾結黨,kiat uang kiat tong
準若,tsun na
準講,tsun kong
著等,tioh ting
萬不二,ban put ji
鹹水貨,kiam tsui hue
窮真,khing tsin
大紅花,tua ang hue
變無撚,pian bo lian
桑椹,sng sui
鹹草,kiam tshau
中盤,tiong puann
水筧,tsui king
失氣,sit khui
母仔,bu a
交葛,kau kat
石距,tsioh ki
利劍劍,lai kiam kiam
狗母鮻,kau bo so
相放伴,sio pang phuann
骨目,kut bak
骨節,kut tsat
術仔,sut a
規半晡,kui puann poo
規晡,kui poo
當初時,tong tshe si
斯當時,su tong si
無閒𩑾𩑾,bo ing tshih tshih
裂獅獅,lih sai sai
歇假,hioh ka
雞災,ke tse
乞龜,khit ku
拗痕,au hun
滾躘,kun liong
朗讀,long thok
端的,tuan tiah
稻稿,tiu ko
頭幫車,thau pang tshia
蜂仔炮,phang a phau
線頂,suann ting
為著,ui tioh
大姊頭仔,tua tsi thau a
轉來去,tng lai khi
奶齒,ling khi
拍莓,phah m
消蝕,siau sih
這號,tsit lo
搜揣,tshiau tshue
經布,kenn poo
雖罔,sui bong
合仔趁,hap a than
孫新婦,sun sin pu
末趁,buat than
大妗喙,tua kim tshui
著囝甘,tioh kiann kam
輪火鬮,lun hue khau
平棒,penn pang
四伨,si thin
擋恬,tong tiam
死無人,si bo lang
躼跤蠓,lo kha bang
銃藥,tshing ioh
過冬鳥,kue tang tsiau
細姑仔,se koo a
新娘花,sin niu hue
傍官靠勢,png kuann kho se
掩來扯去,am lai tshe khi
採花蜂,tshai hue phang
捲螺仔水,kng le a tsui
徛馬勢,khia be se
做木的,tso bak e
起番,khi huan
放外外,pang gua gua
加圇,ka nng
上童,tsiunn tang
娘仔豆,niu a tau
塑膠橐仔,sok ka lok a
珠仔釘,tsu a ting
平正,penn tsiann
相接,sio tsiap
號令,ho ling
暗摸摸,am bong bong
才閣,tsiah koh
出代誌,tshut tai tsi
險仔,hiam a
絞螺仔風,ka le a hong
出外人,tshut gua lang
塗窯,thoo io
錢水,tsinn tsui
菜股,tshai koo
假做,ke tso
牛奶粉,gu ling hun
單仔,tuann a
上陸,tsiunn liok
掠枵,liah iau
止飢,tsi ki
成樣,tsiann iunn
痴哥草,tshi ko tshau
勇壯,iong tsong
摒盪,piann tng
老長壽,lau tiong siu
流擺,lau pai
龜仔,ku a
敗欉,pai tsang
健欉,kiann tsang
跤尾錢,kha bue tsinn
香跤,hiunn kha
放雨白,pang hoo peh
尻川後話,kha tshng au ue
圓棍棍,inn kun kun
芳貢貢,phang kong kong
圓輾輾,inn lian lian
業命,giap mia
巷路,hang loo
三不等,sam put ting
女中,li tiong
目神,bak sin
孤毛,koo moo
孔明燈,khong bing ting
相疼痛,sio thiann thang
有範,u pan
花仔和尚,hue a hue siunn
喙焦喉渴,tshui ta au khuah
食死死,tsiah si si
蔥仔珠,tshang a tsu
出來去,tshut lai khi
嚨喉管,na au kng
在室男,tsai sik lam
大水蟻,tua tsui hia
受教,siu kau
心肝穎仔,sim kuann inn a
爍爍顫,sih sih tsun
破糊糊,phua koo koo
水蛆,tsui tshi
牌匾,pai pian
七爺八爺,tshit ia eh ia
跳懸,thiau kuan
茶湯,te thng
烏水溝,oo tsui kau
新劇,sin kiok
媽孫仔,ma sun a
芳雪文,phang sap bun
龍銀,liong gin
內角,lai kak
激頭腦,kik thau nau
佛祖生,ut tsoo senn
雨傘樹,hoo suann tshiu
望冬,bang tang
鼓箸,koo ti
三時有陣,sam si iu tsun
孤棚,koo penn
上腳,tsiunn kioh
牽教,khan ka
犒軍,kho kun
九降風,kau kang hong
國姓爺,kok sing ia
觸鈕仔,tak liu a
變撚,pian lian
制煞,tse suah
辟邪,phik sia
百歲年老,pah hue ni lau
規山坪,kui suann phiann
講通和,kong thong ho
貫捾,kng kuann
光炎炎,kng iam iam
光映映,kng iann iann
熱翕翕,juah hip hip
好狗運,ho kau un
魚漿,hi tsiunn
合味,hah bi
無命,bo mia
無價,bo ke
青苔仔,tshenn ti a
頭喙,thau tshui
暗報,am po
燒燙燙,sio thng thng
相疊,sio thah
消磨,siau moo
楓仔葉,png a hioh
烏寒,oo kuann
鰻仔栽,mua a tsai
洛神花,lok sin hue
硞硞,khok khok
出日,tshut jit
冰櫥,ping tu
運搬,un puann
盤山過嶺,puann suann kue nia
磚仔角,tsng a kak
僭權,tsiam khuan
七里香,tshit li hiong
對千,tui tshian
千拄千,tshian tu tshian
青蘢蘢,tshenn ling ling
臭腥龜仔,tshau tshenn ku a
相袚,sio phuah
山尖,suann tsiam
歹囝症,phainn kiann tsing
毛繐,mng sui
正中晝,tsiann tiong tau
生理虎,sing li hoo
白死殺,peh si sat
奸臣仔笑,kan sin a tshio
坐罪,tse tsue
拆箬,thiah hah
芹菜珠,khin tshai tsu
苦無,khoo bo
風幔,hong mua
㾀屎,khiap sai
倒匼,to khap
借字,tsioh ji
烏汁汁,oo tsiap tsiap
烏麻仔,oo mua a
眠眠,bin bin
臭老羶,tshau lau hian
肚臍空,too tsai khang
綴手,tue tshiu
理路,li loo
蓮蕉,lian tsiau
激皮皮,kik phi phi
激槌槌,kik thui thui
霜仔,sng a
萬年久遠,ban ni kiu uan
欲死,beh si
海水倒激,hai tsui to kik
好料的,ho liau e
虛荏,hi lam
勇跤,iong kha
韌布布,jun poo poo
徛騰騰,khia thing thing
徛叉仔,khia tshe a
苦湯,khoo thng
起去,khi khi
釉,iu
爸仔,pa a
小盤,sio puann
死好,si ho
跋歹筊,puah phainn kiau
剪筊,tsian kiau
整筊,tsing kiau
親戽戽,tshin hoo hoo
有親,u tshin
食清,tsiah tshing
跕跤,liam kha
好枝骨,ho ki kut
烏昏,oo hng
服藥,hok ioh
掠中和,liah tiong ho
纘袂牢,tsan be tiau
雞喙變鴨喙,ke tshui pian ah tshui
抱心,pho sim
心適興,sim sik hing
割引,kuah in
大圓,tua inn
大晡日,tua poo jit
笑色,tshio sik
半身不隨,puan sin put sui
半仿仔,puann hong a
淺現,tshian hian
軟蜞,nng khi
過家,kue ke
老風騷,lau hong so
理家,li ke
白直,peh tit
乒乓,phin phong
皮皮仔,phue phue a
稻草囷,tiu tshau khun
貓神,niau sin
喙凊,tshui tshin
笑粉,tshio hun
相換工,sio uann kang
慢手,ban tshiu
拍雄,phah hing
邊頭,pinn thau
土符仔,thoo hu a
素料,soo liau
目彩,bak tshai
輕兩想,khin niu siunn
掂篤,tim tau
現仔,hian a
做鬧熱,tso lau jiat
便貨,pian hue
現貨,hian hue
三不服,sam put hok
起底,khi te
窞倕,tham thui
時景,si king
粗幼,tshoo iu
偷走厝,thau tsau tshu
款勢,khuan se
挐頭,ju thau
退悔,the hue
帕尾,phe bue
圇痀,lun ku
是年是節,si ni si tseh
紅筋,ang kin
錦痀,gim ku
雞毛管仔,ke mng kong a
搭粒,tah liap
無時無陣,bo si bo tsun
閹雞行,iam ke kiann
漚搭,au tah
鐵衫,thih sann
攢辦,tshuan pan
攘,jiang
閬站,lang tsam
璇石喙,suan tsioh tshui
熱底,jiat te
鼻刀,phinn to
照原,tsiau guan
嗤噌,tshih tshn̍gh
摘名摘姓,tiah mia tiah senn
慢分,ban hun
嶄然,tsam jian
過通關,kue thong kuan
詼仙,khue sian
超磅,tshiau pong
著吊,tioh tiau
目降鬚聳,bak kang tshiu tshang
近兜,kin tau
強徒,kiong too
致心,ti sim
路長,loo tng
內家,lai ke
數佻,siau tiau
無底,bo te
爸公業,pe kong giap
曷有一个,ah u tsit e
無掛,bo khua
定當,ting tong
現交關,hian kau kuan
漏仔,lau a
饒裕,jiau ju
食路,tsiah loo
鼻趖,phinn so
線屎,suann sai
拚汗,piann kuann
厚味,kau bi
無因無端,bo in bo tuann
下日仔,e jit a
卜面,poh bin
相借喙,sio tsioh tshui
整本,tsing pun
辯話骨,pian ue kut
輕蠓蠓,khin bang bang
抾風水,khioh hong sui
押尾,ah bue
押尾手,ah bue tshiu
慢鈍,ban tun
慢死趖,ban si so
𫞼諍王,tshai tsenn ong
弄家散宅,long ke suann theh
死訣,si kuat
結果擲捒,kiat ko tan sak
懊嘟面,au tu bin
憶著,it tioh
起跤,khi kha
恐喝,khiong hat
苦楝舅,khoo ling ku
苦衷,khoo thiong
過風,kue hong
做得來,tso tit lai
壓落底,ah loh te
天跤下,thinn kha e
趕狂,kuann kong
懸踏,kuan tah
門喙,mng tshui
貓徙岫,niau sua siu
歹星,phainn tshenn
公族仔,kong tsok a
懸低坎,kuan ke kham
卵蛋,nng tuann
省本,sing pun
探,tham
坦橫生,than huainn senn
出眾,tshut tsing
大箍把,tua khoo pe
愛睏神,ai khun sin
喝救人,huah kiu lang
石鼓,tsioh koo
掰會,pue hue
𢯾鼻,mooh phinn
食鹼,tsiah kinn
不三時,put sam si
卸衰,sia sue
呔討,thai tho
臭奶羶,tshau ling hian
厝蓋,tshu kua
一下手,tsit e tshiu
一半擺仔,tsit puann pai a
起致,khi ti
起造,khi tso
叨錢,lo tsinn
平素時,ping soo si
相向,sio hiong
當當,tng tong
厝內人,tshu lai lang
翁仔姐,ang a tsia
好禮仔,ho le a
喝聲,huah siann
會仔錢,hue a tsinn
內裾,lai ki
涼冷,liang ling
軟床,nng tshng
燈膋,ting la
樹箍,tshiu khoo
字條仔,ji tiau a
空身,khang sin
公廳,kong thiann
麵粉粿仔,mi hun kue a
邊仔角,pinn a kak
得定,tik tiann
臭尿破味,tshau jio phua bi
大通,tua thong
兄妹仔,hiann mue a
干證,kan tsing
根頭,kin thau
平埔族,enn poo tsok
透機,thau ki
偷走,thau tsau
天年,thinn ni
推軟仔,thui nng a
實實,tsat tsat
走徙,tsau sua
姐弟仔,tsia te a
水鏡,tsui kiann
顫悶,tsun bun
注心,tsu sim
大色貨,tua sik hue
案桌,an toh
花血,hue hiat
會見眾,e kinn tsing
袂見眾,be kinn tsing
老頹,lau the
省事事省,sing su su sing
新嫣,sin ian
惜略,sioh lioh
四壯,si tsang
著味,tioh bi
手肚仁,tshiu too jin
對扴,tui keh
酸雨,sng hoo
無底止,bo ti tsi
囡仔伴,gin a phuann
合該然,hap kai jian
好頭喙,ho thau tshui
牽磕,khan khap
牽闔,khan khah
筋肉,kin bah
斧頭銎,poo thau khing
相倚傍,sio ua png
草踏,tshau tah
青筋,tshenn kin
精英,tsing ing
話關,ue kuan
暗殕,am phu
肉燥,bah so
梨仔瓜,lai a kue
焦蔫,ta lian
幼工,iu kang
跤肚仁,kha too jin
氣絲仔,khui si a
枯焦,koo ta
古早味,koo tsa bi
媽祖生,ma tsoo senn
補眠,poo bin
新娘桌,sin niu toh
酸微,sng bui
銅仙,tang sian
有法度,u huat too
案內,an nai
無定,bo tiann
現時,hian si
屈勢,khut se
破爿,phua ping
臺票,tai phio
顛倒頭,tian to thau
吊䘥仔,tiau kah a
著力,tioh lat
欲死盪幌,beh si tong hainn
棺柴枋,kuann tsha pang
落名,loh mia
麻穎,mua inn
擘腹,peh pak
平波波,penn pho pho
壁角,piah kak
跋臭,puah tshau
半病仔,puan penn a
紲話,sua ue
肉燥飯,bah so png
事,tai
蜊,la
賞,siong
總,tsang
乜,mi
刁,thiau
力,li
丈,tiong
丈,tiunn
三,sam
上,siong
上,siang
下,e
久,kiu
口,kau
口,khio
夕,siah
夕,sik
川,tshng
川,tshuan
工,khang
己,ki
已,i
巳,su
弓,kiong
不,puh
云,un
互,hoo
井,tsing
仇,kiu
今,kim
今,kin
介,kai
元,guan
分,hun
切,tshe
勿,but
及,kip
夭,iau
孔,khang
孔,khong
少,siau
少,siau
尺,tshik
屯,tun
巴,pa
幻,huan
弔,tiau
手,siu
扎,tsah
支,tsi
斗,too
方,png
曰,uat
歹,tai
毛,moo
火,honn
爻,ngau
片,phian
牛,giu
犬,khian
且,tshiann
丘,khiu
丘,khu
丙,ping
乏,huat
仔,tsu
他,thann
仗,tiong
仟,tshian
代,tai
兄,hing
充,tshiong
冬,tong
凹,neh
功,kang
包,pau
匆,tshong
北,pok
占,tsiam
另,ling
叩,khio
召,tiau
叭,pah
可,khua
可,khoo
史,sai
史,su
右,iu
司,sai
司,si
司,su
外,gue
央,iong
央,ng
孕,in
尻,kha
尼,ni
左,tso
巧,khau
巨,ki
弘,hong
必,pit
扑,phok
打,ta
斥,thik
旦,tan
末,buah
末,buat
本,png
札,tsat
正,tsiann
永,ing
玄,hian
瓜,kua
瓦,ua
田,tian
甲,kap
皮,pi
矛,mau
矛,moo
矢,si
石,siah
禾,ho
丟,tiu
乩,ki
仰,giong
仰,iong
仲,tiong
仵,ngoo
任,jim
企,khi
伍,ngoo
伏,hok
伐,huat
伙,hue
兇,hiong
先,sin
全,tsng
劣,luat
危,gui
危,ui
各,koh
各,kok
合,kah
吉,ji
吋,tshun
同,tang
后,au
后,hio
后,hoo
吏,li
向,hiang
囡,gin
圭,kui
地,te
地,ti
夷,i
妄,bong
存,tshun
宅,thik
宇,u
安,uann
式,sik
式,sit
忖,tshun
忙,bang
忙,bong
扛,kong
旨,tsi
早,tsai
旬,sun
旭,hiok
曲,khiok
朴,phoh
朽,hiu
汗,han
汙,u
汙,u
灰,hue
百,peh
百,pik
竹,tiok
羊,iong
羽,u
老,lo
老,noo
而,ji
肉,hik
肋,lik
肌,ki
至,tsi
臼,khu
舌,siat
舟,tsiu
行,hing
行,ling
西,si
亨,hing
伯,pik
伯,pit
伯,phik
伴,phuan
伶,ling
似,sai
佃,tian
但,tan
但,na
住,tsu
佐,tso
佑,iu
何,ua
冶,ia
刪,san
努,loo
即,tsik
卵,luan
吝,lin
吠,hui
否,honn
否,phi
吩,huan
吩,hun
含,ham
吳,ngoo
吵,tshau
吹,tshui
吻,bun
吾,ngoo
呂,li
呂,lu
呈,thing
困,khun
圾,sap
址,tsi
均,kin
坊,hng
坊,hong
坐,tso
坑,khing
壯,tsong
妍,gian
妒,too
妓,ki
妥,tho
妨,hong
孜,tsu
孝,ha
宏,hong
希,hi
庇,pi
床,tshong
序,si
序,si
廷,ting
弄,long
彷,hong
役,ik
忌,ki
忤,ngoo
快,khuinn
戒,kai
扭,liu
批,phi
扼,ik
把,pa
把,pa
抗,khong
折,tsik
更,king
更,king
杆,kan
杉,sam
杖,tiong
杖,thng
杜,too
杞,ki
決,kuat
汽,khi
沈,sim
沌,tun
沐,bok
沒,but
沙,sa
沙,se
沛,phai
沢,tshioh
灶,tso
灸,ku
牡,boo
牢,lo
甫,hu
町,ting
禿,thuh
禿,thut
秀,siu
私,sai
私,si
究,kiu
肓,bong
肖,siau
肘,tiu
肛,kong
育,iok
良,liong
芋,u
芍,tsiok
芎,kiong
芒,bang
芒,bong
谷,kok
豸,thua
貝,pue
赤,tshik
走,tsoo
車,ki
迅,sin
邑,ip
邦,pang
阮,ng
乳,ju
亞,a
享,hiang
享,hiong
京,kiann
京,king
佩,phue
佩,pue
佬,lo
佳,ka
併,ping
使,sai
使,su
侍,sai
侍,su
侗,tong
供,kiong
依,i
兒,ji
具,ku
函,ham
刮,kuat
到,tau
到,to
刷,suat
卑,pi
卓,toh
卓,tok
協,hah
協,hiap
卷,kng
叔,siok
呢,ne
呢,ni
呧,ti
周,tsiu
呱,kua
呴,ku
呵,o
呻,sin
呼,honn
呿,khuh
和,ho
和,hue
咍,hai
咎,kiu
咐,hu
咖,ka
固,koo
坡,pho
坤,khun
坦,than
坪,phiann
坪,phing
坷,khiat
垃,la
垃,lah
奈,nai
奈,ta
奉,hong
奔,phun
妮,ni
妲,than
始,si
姐,tsia
姒,sai
委,ui
孟,bing
宗,tsong
宙,tiu
宛,uan
宜,gi
尚,siong
尚,siong
尚,siunn
屄,bai
居,ki
居,ku
岡,kong
岩,gam
岩,giam
岳,gak
岸,gan
帙,tiat
帚,tshiu
帛,peh
帛,pik
延,ian
弦,hian
弧,hoo
彼,pi
彿,hut
征,tsing
忽,hut
忿,hun
怏,ng
怐,khoo
怕,pha
怖,poo
怡,i
怦,phenn
性,senn
怫,phut
怯,khiap
或,hik
戾,le
抱,phau
抱,po
抵,te
抵,ti
押,ap
拇,bu
拈,ne
拉,la
拉,la
拒,ki
拒,ku
拓,thok
拔,puat
拘,khu
拙,tsuat
斧,hu
斧,poo
於,i
昂,gong
昆,khun
昇,sing
昊,ho
昌,tshiong
明,bin
明,bing
明,me
明,mia
昏,hng
昏,hun
易,i
易,iah
易,ik
昔,sik
朋,ping
杭,hang
杰,kiat
杵,thu
杷,pe
松,tshing
松,siong
松,song
枉,ong
析,sik
枕,tsim
果,kue
枝,tsi
欣,him
歧,ki
沓,tap
沸,hui
況,hong
泄,siat
泊,pok
泊,phik
泌,pi
泓,hong
泛,huan
泛,huan
泡,phok
泣,khip
泥,ni
泱,iong
泳,ing
炙,tsia
爭,tsing
爸,pah
牧,bok
物,mih
狀,tsiong
狀,tsong
狎,ap
狐,hoo
狗,koo
玩,guan
玩,uan
玫,mui
的,tik
的,tik
盲,me
盲,moo
祀,sai
祀,su
秉,ping
穹,kiong
空,khong
空,khang
空,khong
竺,tiok
羌,kiong
肥,hui
肨,hang
肩,kian
肩,king
肴,ngau
臥,ngoo
舍,sia
芙,hu
芙,phu
芝,tsi
芟,san
芡,khiam
芥,kai
芥,ke
芥,kua
芫,ian
芬,hun
芭,pa
芳,hong
芷,tsi
芹,khin
芽,ga
虎,hu
虱,sat
迌,tho
迎,gia
迎,ging
返,huan
邸,ti
采,tshai
長,tsiong
長,tiong
阻,tsoo
阿,o
阿,oo
陀,too
附,hu
亮,liang
亮,liong
侮,bu
侯,hau
侯,hoo
便,pan
係,he
促,tshiok
俄,go
俄,ngoo
俊,tsun
俍,lang
俏,tshiau
俐,li
俘,hu
俚,li
俞,ju
俠,kiap
冒,moo
則,tsik
削,siat
前,tsun
勁,king
勁,king
勃,put
勉,bian
厚,hoo
叛,puan
咪,bi
咫,tsi
咬,ngau
咯,lok
咳,ka
咳,kha
咽,ian
咾,lo
哈,hah
哉,tsai
垂,se
垂,sue
型,hing
垢,kau
垣,uan
姚,iau
姚,io
姜,kiong
姜,khiong
姜,khiunn
姜,kiunn
姦,kan
姪,tsit
姪,tit
姻,in
姼,tshit
姿,tsu
威,ui
娃,ua
客,khik
宣,suan
宥,iu
宦,huan
屋,ok
屎,su
屏,pin
屏,ping
峇,ba
帥,sui
帥,sue
幽,iu
度,tok
建,kian
彥,gan
彥,gian
待,tai
後,hau
後,hio
後,hoo
怎,tsuann
怒,noo
思,si
思,su
恂,sun
恆,hing
恍,hong
恍,huann
恢,hue
恢,khue
恨,hin
扁,pian
扁,pun
括,kuat
拯,tsin
拱,kiong
拼,phing
拾,sip
持,tshi
持,ti
指,tsing
按,an
挑,thiau
挑,thiau
既,ki
星,san
映,ing
映,iong
昧,mai
昨,tsa
昨,tsoh
昭,tsiau
昱,iok
枯,koo
枴,kuainn
架,ka
枷,ka
枸,koo
柄,ping
柏,peh
柏,pik
某,boo
柔,jiu
查,tsa
查,tsa
柩,kiu
柫,put
柬,kan
柯,kho
柱,tsu
柳,liu
柵,tshik
柵,sa
殃,iong
段,tuan
洋,iong
洛,lok
津,tsin
洪,ang
洪,hong
活,huat
炫,hian
炳,ping
炸,tsiah
牲,senn
牲,sing
狡,kau
玲,ling
玲,lin
玻,po
珊,suan
珍,tsin
珍,tin
甚,sim
界,kai
界,ke
疫,iah
疫,ik
皇,hong
盈,ing
相,siunn
盼,phan
盾,tun
矜,king
矜,khim
砂,se
砌,kih
砍,kham
砒,phi
研,gian
祈,ki
祉,tsi
禹,u
秒,biau
穿,tshuan
突,tut
竿,kuann
紀,ki
紂,tiu
缸,kong
耶,ia
背,pue
胖,phang
胛,kah
胞,pau
胡,hoo
胡,oo
舢,sam
苑,uan
苒,jiam
苓,ling
苔,thai
苔,thi
苗,biau
苛,kho
苞,pau
苟,koo
若,jiok
苦,ku
苧,thu
英,ing
苳,tang
莓,m
茂,boo
范,huan
茄,ka
茅,hm
茅,mau
茉,bak
茉,buah
虐,gik
虐,gioh
虐,giok
虼,ka
要,iau
要,iau
訃,hu
計,ki
貞,tsing
軌,kui
迦,khia
迪,tik
迭,tiat
述,sut
郁,hiok
郎,lang
郎,nng
酋,siu
陋,loo
陌,bik
韋,ui
韭,ku
飛,hue
首,siu
香,hiang
香,hiong
乘,sing
乘,sing
俯,hu
俱,khu
俳,pai
俳,pai
俸,hong
倆,liong
倉,tshong
倒,thoh
倖,hing
候,hau
倚,i
借,tsia
倡,tshiong
倡,tshiong
倦,kuan
倫,lun
倭,e
冥,bing
凊,tshing
凋,tiau
凌,ling
剔,thik
剖,phoo
剛,kong
剝,pok
卿,khing
原,guan
員,inn
哥,koh
哨,sau
哨,siau
哩,li
哩,li
哲,tiat
唆,so
唆,so
唏,hi
唐,tong
唐,tng
埃,ai
埃,ia
埆,kak
埒,luah
夏,he
娉,phing
娘,liong
娛,gu
娛,ngoo
娜,na
娟,kuan
娥,ngoo
娩,bian
宰,tsainn
宴,ian
宵,siau
屐,kiah
屑,sap
峰,hong
峻,tsun
峽,kiap
差,tshai
庭,tiann
庭,ting
徐,tshi
徑,king
恐,khiong
恕,su
息,sik
息,sit
悅,uat
悅,iat
悔,hue
悔,hui
悖,pue
悟,ngoo
扇,sian
拳,kuan
拿,na
挨,ai
挫,tsho
振,tsin
振,tin
挹,ip
挺,thing
捉,tshiok
捏,liap
捐,kuan
捔,kak
捕,poo
旁,pong
旅,lu
晉,tsin
晏,an
朔,sok
朗,lang
朗,long
栓,tshng
栗,lat
栗,lik
校,kau
株,tsu
株,tu
栱,kong
核,hat
核,hik
格,kik
桀,kiat
桂,kui
桃,to
桅,ui
案,uann
桐,tang
桐,tong
桑,sng
桑,song
桑,sang
殉,sun
殊,su
殷,in
殷,un
氧,iong
泰,thai
浙,tsiat
浡,phuh
浦,phoo
浩,ho
浪,long
浮,hu
浴,ik
浴,iok
涂,too
涂,thoo
涉,siap
涗,sue
烏,u
烘,hong
烙,lo
烙,lok
特,tik
狸,li
狹,hiap
狽,pue
珮,pue
琉,liu
畔,puan
畚,pun
畚,pun
畜,thiok
畝,boo
疲,phi
疳,kam
疸,than
疹,tsin
疾,tsik
疾,tsit
病,ping
益,iah
益,ik
眠,bian
眨,tshap
矩,ki
砲,phau
祐,iu
祕,pi
祚,tsa
祟,sui
秘,pi
秤,ping
秦,tsin
秧,iang
秧,iong
秩,tiat
秪,te
秫,tsut
秮,tai
窄,tsik
窈,iau
笆,pa
笑,tshiau
笑,siau
笒,gim
粅,but
紋,bun
紐,liu
紗,sa
紛,hun
紡,hong
索,sik
羓,pa
羔,ko
翁,ong
翅,tshi
耆,ki
耕,king
耘,un
耽,tann
胭,ian
胰,i
胱,kong
胳,koh
胸,hiong
脂,tsi
脅,hiap
脆,tshui
脈,bik
脊,tsiah
脊,tsik
脊,tsit
舨,pan
航,hang
般,pan
般,puann
茭,ka
茭,kha
茯,hok
茱,tsu
茵,in
茸,jiong
荀,sun
荇,hing
荊,king
荍,sio
荐,tsian
荒,hong
荔,nai
荖,lau
荖,lo
虔,khian
蚊,bun
蚌,pang
蚓,kun
蚣,kang
蚤,tsau
衲,lap
衷,thiong
訊,sin
訓,hun
訕,suan
豈,khi
貢,kong
躬,kiong
軒,hian
軒,ian
辱,jiok
迴,hue
送,song
郡,kun
酌,tsiok
釘,ting
陛,pe
陝,siam
陞,sing
隻,tsik
馬,ma
高,kau
鬥,too
倏,sua
偉,ui
偕,kai
健,kian
健,kiann
側,tshik
偵,tsing
偶,ngoo
偽,gui
凰,hong
勘,kham
勘,kham
匿,lik
參,sim
參,som
售,siu
唯,ui
唱,tshiong
商,siong
問,bun
啖,tam
啞,a
啞,e
啟,khe
啡,pi
圇,lun
圈,khuan
域,ik
埠,poo
執,tsip
培,pue
基,ke
基,ki
埽,so
奢,tshia
娼,tshang
娼,tshiong
婉,uan
婊,piau
婢,pi
婦,pu
宿,siok
宿,siu
宿,sok
寂,tsik
寂,siok
寄,ki
密,bit
屠,too
崇,tsong
崔,tshui
崖,gai
崗,kang
崗,kong
崙,lun
崩,ping
巢,tsau
帳,tiong
帳,tiunn
帷,ui
常,tshiang
常,siong
庵,am
康,khng
康,khong
庸,iong
張,tiong
強,kiong
強,kiong
彗,hui
彩,tshai
彪,piu
彬,pin
徘,pai
從,tshiong
御,gu
悉,sik
悠,iu
患,huan
悽,tshi
情,tsiann
惘,bong
惜,sik
惟,ui
惟,i
戚,tshik
捨,sia
捷,tsiat
掃,so
掇,tuah
掇,tuah
授,siu
掙,tsiann
掠,liok
控,khong
推,tshui
敏,bin
敘,su
敝,pe
敝,pe
斜,sia
斬,tsam
斬,tsann
晚,buan
晚,mng
晝,tiu
晨,sin
曹,tso
曼,ban
梁,niu
梅,mui
梗,kenn
梗,king
梟,hiau
梧,ngoo
梨,le
梭,so
梯,the
械,hai
梵,huan
棄,khi
欲,iok
毫,ho
毫,hoo
毬,kiu
涎,sian
涯,gai
液,ik
涵,am
涵,ham
涸,khok
涼,niu
淇,ki
淋,lim
淑,siok
淒,tshe
淡,tam
淡,tann
淨,tsing
淪,lun
淫,im
淮,huai
淵,ian
混,hun
淺,khin
清,tshinn
烹,phing
焗,kok
爽,sng
牽,khian
猊,ji
猖,tshiong
率,lut
率,sut
畢,pit
略,lioh
略,liok
異,i
疏,soo
疵,tshu
盔,khue
盛,siann
眼,ging
眾,tsing
眾,tsiong
硃,tsu
硫,liu
祥,siong
祧,thiau
票,phiau
移,i
窕,thiau
竟,king
笙,sing
笛,tat
笛,tik
笠,lip
粕,phok
紮,tsap
累,lui
累,lui
紳,sin
紹,siau
終,tsiong
絆,puan
統,thong
缽,puat
羞,siu
翎,ling
習,sip
聆,ling
聊,liau
唇,sun
唇,tun
脫,thuah
脬,pha
脰,tau
舵,tai
舵,to
舵,tua
舷,hian
荳,too
荷,ha
荷,ho
荷,hue
荽,sui
莉,ni
莊,tsong
莎,sa
莎,so
莖,king
莖,huainn
莧,hing
莽,bong
處,tshu
處,tshu
蛀,tsu
蛄,koo
蛇,sia
蛋,tan
蛋,tuann
袈,ka
袋,tai
袍,phau
袖,siu
覓,bik
訟,siong
訪,hong
許,hi
許,khoo
豚,thun
貧,pin
貨,ho
貫,kuan
責,tsik
趺,u
趾,tsi
軟,luan
逍,siau
透,tho
逐,tiok
速,sok
逢,hong
連,liam
連,ni
郭,kok
郭,kueh
都,too
釣,tiau
釵,tshai
釵,the
陰,iam
陳,tan
陳,tin
陵,ling
陶,to
陸,liok
陸,lok
陸,lak
雀,tshik
雀,tshiok
雪,sap
頃,khing
頃,khing
魚,gu
鳥,niau
麻,ma
傀,ka
傀,khui
傅,hu
傅,poo
傍,pong
傑,kiat
傘,san
備,pi
凱,khai
剩,sin
剩,sing
剩,siong
割,kat
勝,sing
勝,sing
勞,loo
勞,lo
唾,tho
啾,tshiunn
喂,ue
喇,la
喉,au
喌,tsiuh
喑,inn
喚,huan
喜,hi
喝,hat
喧,suan
喪,sng
喪,song
喬,kiau
單,tan
喲,io
喳,tsha
喻,ju
圍,u
堡,po
堤,the
堯,giau
場,tshiang
奠,tian
婷,ting
婸,giang
婿,sai
婿,se
媒,mue
媒,mui
媚,bi
媧,o
富,hu
寐,bi
寒,han
寓,gu
寓,u
尋,sim
嵐,lam
幅,hok
幾,ki
廁,tshe
廂,siunn
廊,long
彭,phenn
彭,phing
復,hok
循,sun
悲,pi
悶,bun
惑,hik
惠,hui
惡,onn
惰,to
惰,tuann
惱,lo
惱,nau
惶,hiann
惻,tshik
愉,ju
愕,gok
慨,khai
戟,kik
掌,tsiang
揀,kan
描,biau
揚,iong
握,ap
握,ok
揭,kiat
揭,khiat
揮,hui
援,uan
敦,tun
斌,pin
斐,hui
斐,hui
斑,pan
斯,su
斯,suh
晬,tse
普,phoo
普,puh
晴,tsenn
晴,tsing
晶,tsing
晶,tsinn
智,ti
暑,su
曾,tsan
曾,tsing
曾,tsing
朝,tiau
期,ki
棉,bian
棍,kun
棑,pai
棒,pang
棚,ping
棠,tong
棧,tsan
森,sim
棲,tshe
棺,kuan
棺,kuann
植,tit
植,sit
椒,tsiau
椒,tsio
椪,phong
欽,khim
殖,sik
殖,sit
殘,tsan
殘,tsuann
殘,tshan
殼,khok
渝,ju
渝,u
渣,tse
測,tshik
渴,khat
游,iu
渺,biau
渾,hun
湘,siong
湧,iong
湯,thong
溉,kai
滋,tsu
焦,tsiau
焰,iam
焱,iann
然,jian
犀,sai
犀,se
猩,sing
猫,ba
猶,iu
琢,tok
琦,ki
琪,ki
琳,lim
琵,pi
琶,pa
琶,pe
甥,sing
番,han
痘,tau
痘,too
痛,thang
痛,thong
痞,phi
痟,siau
痡,poo
痢,li
登,ting
發,huat
皓,ho
皓,hoo
盜,to
硝,siau
硞,khok
硬,ging
稀,hi
程,ting
程,thiann
程,thing
窘,khun
筐,khong
答,tah
答,tap
策,tshik
粟,siok
粧,tsong
紫,tsi
絞,kau
絡,loh
絡,lok
絡,le
絢,sun
給,kip
絪,in
絮,su
絳,kong
翔,siong
肅,siok
脽,tsui
脾,phi
腋,ik
腌,a
腎,sian
腑,hu
腔,khiong
腔,tshiunn
腕,uan
腕,uann
舒,soo
舒,su
舜,sun
莿,tshi
菁,tshenn
菅,kuann
菊,kak
菖,tshiong
菝,puat
菝,pat
菠,po
菠,pue
菩,phoo
華,hua
華,hua
菱,ling
菲,hui
菲,hui
萄,to
萊,lai
萍,phing
萎,ui
著,tiok
著,tu
虛,hu
蛙,ua
蛛,tu
蛟,kau
蛤,kap
袱,hok
裂,liat
視,si
診,tsin
詐,tsa
詔,tsiau
象,siong
象,siong
象,siong
象,siunn
貂,tiau
貯,thu
貳,ji
貸,tai
貿,boo
賀,ho
超,tshiau
超,thiau
跋,puat
跌,tiat
跑,phau
距,ki
軸,tik
辜,koo
逮,tai
週,tsiu
逸,it
逸,ik
逸,iat
郵,iu
鄉,hiong
鄉,hiunn
鈔,tshau
鈗,ng
鈞,kun
閒,han
間,kan
閔,bin
陽,iunn
隆,liong
隍,hong
階,kai
雅,nga
雅,nge
雇,koo
雯,bun
頇,han
須,su
飯,huan
黃,hong
黑,hik
黹,tsi
亂,lan
傲,ngoo
傳,tuan
傾,khing
僆,nua
勤,khin
嗙,pong
嗚,oo
嗝,keh
嗣,su
嗣,su
嗤,tshi
嗦,so
嗲,te
嗲,teh
園,uan
圓,uan
塑,sok
塗,too
塘,tng
塘,tong
塞,sai
奧,o
媳,sik
媽,ma
媽,mah
嫁,ka
嵯,tshu
廉,liam
微,bi
微,bui
愍,bian
愚,gu
愧,khui
慄,lak
慄,lik
慈,tsu
慌,hong
慍,un
慎,sin
搏,phok
搖,iau
搬,puan
搭,tap
搶,tshiong
斟,tsim
暇,ha
暈,un
暉,hui
暖,luan
會,kue
棰,tshue
楊,tshiunn
楊,iong
楊,iunn
楓,hong
楚,tsho
楝,lian
楝,ling
楣,bai
楬,at
極,kik
楷,khai
楹,enn
楹,ing
概,kai
概,khai
榆,jiu
榔,long
榔,nng
歆,him
殿,tian
毽,kian
源,guan
溫,un
溯,soo
溶,iong
溺,lik
滂,phong
滄,tshong
滇,tian
滓,tsainn
滓,lai
煉,lian
煌,hong
煞,sat
煤,mue
煥,huan
煬,iang
煬,iong
牒,tiap
猾,kut
瑋,ui
瑕,ha
瑙,lo
瑚,oo
瑛,ing
瑜,u
瑜,ju
瑞,sui
瑟,sit
瑟,sik
瑯,long
當,tang
當,tang
當,tong
當,tong
痱,pui
痴,tshi
痹,pi
痺,pi
盞,tsan
盟,bing
睚,kainn
睛,tsing
督,tok
睦,bok
睫,tsiah
睭,tsiu
睹,too
硼,phing
碇,ting
碌,lok
碓,tui
碖,lun
碡,tak
碰,phong
祺,ki
祿,lok
禽,khim
稚,ti
稠,tiu
窞,tham
窣,sut
筠,un
筧,kian
粱,liang
綁,pang
罪,tse
置,ti
署,su
署,su
羨,sian
聖,sing
肆,su
腥,tshenn
腦,lo
腩,lam
腮,tshi
腰,iau
腱,kian
腱,kian
腳,kioh
腳,kiok
腸,tshian
腸,tshiang
腸,tiong
腹,hok
舅,kiu
艇,thing
萵,ue
落,lauh
葉,iap
葛,kat
葛,kuah
葡,phu
董,tang
董,tong
葫,hoo
葵,kui
葵,khue
號,lo
蛻,thui
蛾,iah
蜀,siok
蜂,hong
蜅,poo
蜈,gia
蜈,goo
蜈,ngoo
蜍,tsi
衙,ge
裌,kiap
裏,li
裔,e
裔,i
裕,ju
裟,se
解,ke
詢,sun
詣,ge
詬,kau
詭,khui
詭,kui
詮,tshuan
詰,khiat
詳,siong
詹,tsiam
誇,khua
誠,sing
貉,ho
賂,loo
賄,hue
資,tsu
賈,ka
賈,koo
賊,tsat
賊,tsik
跡,tsik
較,ka
較,kau
辟,phik
遁,tun
遂,sui
運,in
遍,phian
過,koo
過,kua
過,koh
達,tat
違,ui
酬,siu
鈸,puah
鈸,puat
鉈,to
鉗,khiam
隔,kik
隘,ai
雉,thi
零,lan
零,ling
靖,tsing
靶,pe
預,i
預,u
頑,guan
頒,pan
頓,tun
飽,pau
飾,sik
馳,ti
馴,sun
鳩,khiu
鼎,ting
鼠,tshu
僑,kiau
僕,pok
僚,liau
僧,sing
僧,tsing
僭,tsiam
厭,ian
嗹,lian
嘈,tso
嘈,tshauh
嘉,ka
嘐,hau
嘓,gok
嘓,kok
嘔,oo
嘛,ma
嘟,tu
塵,tin
塾,siok
墓,boo
夥,hue
嫖,phiau
嫡,tik
嫦,siong
孵,hu
寞,bok
察,tshat
寢,tshim
寢,khim
寥,liau
寧,ling
屢,li
嶄,tsam
幣,pe
廖,liau
弊,pe
弊,piah
彰,tsiong
徹,thiat
態,thai
態,thai
慣,kuan
慳,kian
慷,khong
截,tsiat
摘,tik
摸,moo
撤,thiat
暨,ki
榕,iong
榛,tsin
榜,pong
榜,png
榨,tsa
榮,ing
榴,liu
榻,thah
榻,thap
構,koo
槐,huai
槔,oo
歉,khiam
歉,khiam
滬,hoo
滯,ti
滴,tik
滸,hoo
漁,gu
漁,hi
漂,phiau
漂,phio
漉,lok
漏,loo
漚,au
漠,bok
漫,ban
漳,tsiang
漸,tsiam
澈,thiat
煽,sian
熇,ho
熏,hun
熔,iong
爾,ni
爾,nia
犒,kho
獄,gak
獄,gik
瑣,so
瑪,be
瑪,ma
瑰,kui
瘋,hong
瘍,iong
監,kam
監,kam
睡,tsue
睡,sui
碟,tiap
碟,tih
碧,phik
碩,sik
碩,sik
磁,tsu
禎,tsing
種,tsiong
稱,tshing
窩,o
端,tuan
端,tuann
筵,ian
箋,tsian
箏,tsing
箕,ki
粹,tshui
綜,tsong
綠,liok
綢,tiu
維,i
綰,kuann
綱,kong
綴,tuat
綸,lun
綸,kuan
綺,khi
綽,tshiok
綾,ling
綿,bian
緒,su
翠,tshui
聚,tsu
聞,bun
肇,tiau
腐,hu
腐,hu
膀,phong
膁,liam
膈,keh
膋,la
膏,ko
膏,koo
臺,tai
與,u
蒙,bong
蒲,poo
蒸,tsing
蒼,tshong
蒿,o
蓄,thiok
蓉,iong
蓑,sui
蜘,ti
蜞,khi
蜢,meh
蝕,sit
裱,piau
裹,ko
裼,theh
製,tse
褂,kua
誌,tsi
誓,se
誣,bu
誦,siong
豪,ho
貌,mau
賑,tsin
賓,pin
趙,tio
輓,buan
輔,hu
輔,phoo
輕,khing
遙,iau
遜,sun
遞,te
遣,khian
酷,khok
酸,suan
銘,bing
閩,ban
際,tse
障,tsiang
障,tsiong
障,tsiong
需,su
鞅,iong
頗,pho
颱,thai
餃,kiau
餉,hiong
馝,pih
駁,poh
駁,pok
骰,tau
骱,kai
魁,khue
魠,thoh
鳴,bing
僵,khiong
價,ka
僻,phiah
儀,gi
劇,kik
劈,phik
劉,lau
厲,le
厲,li
嘩,hua
嘮,lo
嘯,siau
嘻,hi
噁,onn
噎,uh
增,tsing
墨,bik
墩,tun
墮,tui
墳,hun
墳,phun
嬉,hi
寬,khuan
寬,khuann
履,li
幢,tong
廚,too
廚,tu
廣,kng
彈,tan
彈,tan
彈,than
影,ing
徵,tin
徵,ting
慕,boo
慧,hui
慧,hue
慮,li
慰,ui
慶,khing
慼,tshik
慾,iok
憐,lian
憐,lin
憚,tan
憢,giau
憤,hun
憫,bin
戮,liok
摩,moo
摯,tsi
摹,boo
摹,boo
撒,sat
撙,tsun
撥,puat
撫,bu
撫,hu
撮,tsuat
撰,tsuan
敵,tik
敷,hu
暮,boo
暱,lit
暱,lik
暴,po
暴,pok
暴,pok
槤,lian
樂,ngau
樑,liong
樑,niu
標,phiau
樞,tshu
樟,tsiong
樣,iong
歎,than
歐,au
歐,io
毅,ge
毅,gi
毿,sam
漿,tsiong
潑,phuat
潔,kiat
潘,phuan
潘,phuann
潛,tsiam
潦,lo
潮,tiau
潮,tiau
潺,tshan
澄,ting
澎,phenn
熟,siok
熥,thang
獠,liau
瑩,ing
璃,le
璃,li
璇,suan
瘟,un
瘡,tshong
瘦,soo
盤,puan
盤,phuan
瞌,ka
確,khak
確,khiak
碼,be
碼,ma
碾,lian
磊,lui
磋,tsho
稷,tsik
稻,to
穀,kok
箠,sui
箭,tsian
箱,siong
箴,tsim
範,huan
範,pan
篇,phian
糊,hoo
糍,tsi
緝,tsip
緝,tship
緞,tuan
締,te
編,pinn
緯,ui
緻,ti
緻,ti
羯,kiat
翩,phian
膝,tshik
膝,sit
蓪,thong
蓬,hong
蓬,pong
蓮,lian
蓮,lian
蔑,biat
蔓,ban
蔓,mua
蔚,ui
蔡,tshua
蔬,se
蔬,soo
蔽,pe
蝒,bin
蝛,bui
蝴,hoo
蝴,oo
蝶,iah
蝶,tiap
衛,ue
衝,tshong
複,hok
褙,pe
誕,tan
誕,tan
誰,sui
課,khue
誹,hui
誼,gi
誼,gi
調,tiau
調,tiau
諍,tsing
諒,liong
諸,tsu
豍,pi
豎,su
賦,hu
趣,tshu
踏,tap
踐,tsian
踔,tshik
踢,thik
踩,tshai
輛,liong
輛,liong
輝,hui
輪,lin
遨,ngoo
適,sik
遭,tso
鄧,ting
鄭,tenn
鄭,ting
醇,sun
銲,huann
銳,jue
鋁,lu
鋁,lu
鋒,hong
鋤,ti
閬,long
閱,iat
霆,ting
震,tsin
鞋,hai
鞍,an
鞏,kiong
頡,khiat
頦,hai
頦,huai
餘,u
駐,tsu
駕,ka
駛,su
駝,to
髮,huat
魩,but
魬,puann
魯,luh
魴,hang
鴆,thim
鴉,a
黎,le
儒,ju
儘,tsin
儘,tsin
劑,tse
劑,tse
勳,hun
叡,jue
噤,khiunn
噪,tsho
噭,kiau
噷,hmh
噹,tang
圜,huan
墾,khun
壁,pik
壇,tan
奮,hun
導,to
徼,khio
憑,ping
憶,ik
憾,ham
懊,au
擁,iong
擅,sian
操,tsho
曆,lah
曆,lik
曉,hiau
樵,tsiau
樸,phok
樹,su
樺,hua
樺,hua
橂,ting
橄,kam
橄,kan
橄,kann
橋,kiau
橐,lak
機,ki
機,kui
橫,hing
歷,lik
澡,tso
澤,tik
澳,o
澳,u
濁,tak
濁,tok
濃,long
燃,jian
燄,iam
燕,ian
獨,tak
獨,tok
璞,phok
瓢,phio
瘰,lui
瘼,mooh
磚,tsuan
磟,lak
磨,moo
禦,gu
穌,soo
窵,tiau
窸,si
窸,si
窸,sih
窺,khui
築,tiok
篤,tau
篤,tauh
篤,tok
縐,tso
縒,tsuah
翰,han
翱,ko
膩,ji
艙,tshng
艙,tshong
蕃,huan
蕉,tsiau
蕉,tsio
蕎,gio
蕘,gio
蕨,kueh
蕩,tng
蕩,tong
蕭,siau
蕭,sio
融,hiong
融,iong
螕,pi
螟,bing
螢,ing
螢,hing
衡,hing
褥,jiok
褥,liok
親,tshenn
觱,pi
諜,tiap
諦,te
諧,hai
諭,ju
諳,am
諾,lok
謀,boo
謂,ui
謔,giok
豫,u
貓,ba
賴,nai
踴,iong
輯,tsip
輯,tship
輻,hok
辨,pian
遲,ti
遵,tsun
遺,ui
遼,liau
醒,sing
鋼,kong
錄,liok
錄,lik
錐,tsui
錠,tiann
錠,ting
錢,tsian
錢,tshian
錦,gim
錦,kim
錦,gim
錫,sik
錯,tsho
錯,tshok
閻,giam
隧,sui
霎,sap
霎,tiap
頭,thio
頭,thoo
頸,kun
頸,king
頹,tue
頻,pin
餐,tshan
餞,tsian
駱,lok
骸,hai
骿,phiann
魽,kam
鮑,pau
鮑,pau
鮕,koo
鴒,ling
鴛,uan
鴞,hioh
鴟,tshi
鴟,lai
鴣,koo
鴦,iong
鴦,iunn
默,bik
龍,ging
龍,long
龜,kui
償,siong
償,siong
儡,le
優,iu
儲,tu
勵,le
嚇,hiannh
壓,ap
壕,ho
嬭,le
嬰,enn
嬰,ing
嬰,inn
嶺,ling
嶼,su
嶽,gak
彌,mi
彌,ni
懂,tang
懂,tong
懇,khun
應,ing
應,ing
懦,noo
戴,tai
戴,te
擊,kik
擎,khing
擎,king
擬,gi
斂,liam
斃,pe
曖,ai
檀,tan
檜,kue
檢,kiam
殭,khiong
殮,liam
氈,tsinn
澩,haunnh
濟,tse
濤,to
濤,too
濱,pin
燦,tshan
爵,tsik
爵,tsiok
環,huan
療,liau
癆,lo
盪,tong
瞬,sun
瞭,liau
瞭,liau
瞳,tong
矯,kiau
磺,hong
礁,tsiau
禪,sian
篠,siau
篠,siau
篱,le
篷,pong
篷,hong
篾,biat
簇,tshok
糙,tsho
糜,mi
糞,hun
糟,tsau
糠,khong
縫,hong
縭,li
縮,siok
縱,tshiong
縱,tshiong
縱,tshiong
績,tseh
績,tsik
繁,huan
繆,biu
翳,e
翳,i
翼,ik
聰,tshong
聳,sang
膿,long
臁,liam
臆,ik
臉,liam
臉,lian
臊,tshau
舉,ki
艚,tso
艱,kan
蕗,loo
蕹,ing
蕾,lui
薁,o
薄,pok
薇,bi
薈,hue
薏,i
薐,ling
薔,tshiunn
薦,tsi
薪,sin
薯,tsu
虧,khui
螺,loo
螿,tsiunn
蟀,sut
蟄,tit
蟋,sih
蟋,sik
蟒,bang
蟒,bong
襀,tsioh
襄,siong
謄,thing
謊,hong
謊,hong
謎,bi
謗,pong
謙,khiam
謝,tsia
謠,iau
賺,tsuan
購,kang
購,koo
賽,sai
賽,se
蹈,to
蹉,tsho
蹊,khi
蹌,tshiang
輾,tian
轄,hat
邀,iau
邀,io
邁,mai
醜,tshiu
錨,ba
錨,biau
鍍,too
鍘,tsah
鍵,kian
鍼,tsiam
鍾,tsiong
闆,pan
闇,am
雖,sui
霞,ha
鞠,kiok
駿,tsun
鮡,thiau
鮫,ka
鮮,sian
鮮,sian
鴻,hong
鴿,kah
鴿,kap
鵁,ka
黛,tai
鼢,bun
齋,tse
叢,tsong
嚮,hiong
嬸,sim
擴,khok
擾,jiau
檫,tshat
檬,bong
檳,pin
檸,le
獵,lah
獵,liap
璿,suan
癜,tio
瞻,tsiam
礎,tshoo
穡,sik
穢,ue
竄,tshuan
竅,khiau
竅,khio
簡,kan
簪,tsiam
罈,tham
臍,tse
舊,kiu
薩,sat
薺,tsi
藉,tsiah
藉,tsik
藉,tsioh
藍,lam
藏,tsong
藏,tsong
藐,biau
蟧,la
蟮,sian
蟯,jiau
覆,hok
謬,biu
謳,oo
謹,kin
豐,hong
豐,phong
贅,tsue
蹟,tsik
蹤,tsong
蹧,tsau
軀,khu
轆,lak
轆,lok
轍,tiat
釐,li
鎔,iunn
闔,hap
闕,khuat
闖,tshuang
離,li
鞦,tshiu
鞭,mi
額,gik
顎,kok
餾,liu
騎,khi
魍,bang
鮸,bian
鯉,li
鯊,sua
鵑,kuan
鵝,ngoo
鵠,khok
儳,sam
嚨,long
嚨,na
壞,huai
壟,long
壢,lik
寵,thing
寵,thiong
懲,ting
懵,bong
懵,bong
懶,nua
懷,huai
曝,phok
曠,khong
瀘,lu
瀚,han
瀟,siau
爆,pok
牘,tok
犢,tok
獸,siu
獺,thuah
瓊,khing
瓊,khiong
疆,kiong
癡,tshi
矇,bong
禱,to
穫,hik
簷,tsinn
簷,liam
簾,ni
簿,phok
繩,sing
繪,hue
羅,lo
羹,king
臘,lah
臘,liap
藕,ngau
藤,ting
藥,iok
藩,huan
藩,phuan
蟹,hai
蟹,he
蟻,gi
蟻,hia
蟾,siam
蠅,sin
蠍,giat
襞,phe
襟,khim
譁,hua
譎,khiat
譏,ki
譚,tam
贈,tsing
贊,tsan
贊,tsan
蹬,tenn
蹲,tsun
躇,tu
轎,kiau
轎,kiau
醮,tsiau
醮,tsio
鏃,tsok
鏘,tshiong
難,lan
顛,thian
顛,tian
饅,ban
饅,ban
鯗,siunn
鯧,tshiunn
鯪,la
鯮,tsang
鯰,liam
鵪,ian
鵬,ping
鵬,phing
鵰,tiau
鵻,tsui
鶉,tshun
鶉,tun
麒,ki
麗,le
麗,le
龐,pang
嚶,inn
孀,song
孽,giat
懸,hian
懺,tsham
攔,lan
攔,nua
攕,tshiam
櫳,long
瀾,lan
癢,iong
竇,too
競,king
籃,lam
籌,tiu
籍,tsik
繼,ke
耀,iau
艦,kam
艦,lam
藹,ai
蘆,loo
蘇,soo
蘋,phong
蘑,moo
蠐,tse
蠕,ju
蠕,lun
蠘,tshih
襤,lam
覺,kak
觸,tshik
觸,tshiok
警,king
譬,phi
譯,ik
議,gi
贏,ing
躂,that
醴,le
釋,sik
鏽,siu
鐃,lau
鐃,na
鐐,liau
闡,tshian
顢,ban
馨,hiong
馨,hing
騷,so
鰇,jiu
鰗,hoo
鶖,tshiu
鶿,tsi
麵,bian
齡,ling
囂,hiau
屬,tsiok
屬,siok
懼,ku
攜,he
櫻,ing
欄,lan
爛,lan
犧,hi
癩,thai
礱,lang
籐,tin
續,siok
纏,tian
蘭,lian
蠟,lap
襪,buat
覽,lam
譴,khian
譴,khian
護,hoo
譽,u
贐,tsin
贓,tsng
贓,tsong
躊,tiu
躍,iok
轟,hong
鐳,lui
鐵,thiat
闢,pik
露,lok
霹,phik
響,hiong
飆,phiau
饗,hiang
驅,khu
魔,moo
鰡,liu
鰮,un
鶯,ing
鶴,hok
麝,sia
黯,am
囉,lo
囉,lo
懿,i
攤,than
歡,huan
歡,huann
灑,sa
灘,than
瓤,jiong
癮,in
籠,long
糴,tik
聽,thing
聾,lang
聾,long
臟,tsng
臟,tsong
襲,sip
讀,tau
讀,too
鑑,kam
驍,hiau
驕,kiau
鬚,su
鱈,suat
鱉,piat
鷓,tsia
鷗,oo
麶,thi
龕,kham
戀,luan
竊,tshiat
竊,tshiap
纓,enn
纓,iann
纓,ing
纓,inn
纖,siam
臢,tsa
鑠,siak
鑢,le
驚,kenn
驚,king
驛,ik
髓,tshui
體,thai
鱔,sian
鱗,lin
鱙,jiau
鷥,si
麟,lin
黐,thi
囑,tsiok
壩,pa
壩,pe
蠶,tsham
蠶,tham
讓,jiong
釀,jiong
鑫,him
靂,lik
韆,tshian
鬢,pin
鷺,loo
鹼,kiam
齷,ak
廳,thing
欖,na
灣,uan
籬,li
籮,lo
籮,lua
糶,thiau
蠻,ban
觀,kuan
觀,kuan
鑰,ioh
鑰,iok
齻,tsan
讚,tsan
鱲,lah
纜,lam
纜,lam
蚻,tsuah
鑽,tsuan
顴,kuan
鱷,khok
鸕,loo
豔,iam
鑿,tshok
鸚,ing
鱺,le
鸞,luan
籲,iok
硓,loo
鮘,tai
䘥,kah
𣮈,khut
𦉎,sui
𥑮,koo
𨑨,tshit
㷮,tsau
䈄,ham
𦟪,lian
𤺅,tshe
𧿳,phut
𧌄,am
䢢,tshiang
㴙,tshap
䲅,kui
𩸶,gam
𰣻,ko
諺,gan
焦,na
哖,ni
胿,kuai
哉,tsai
蓋,kap
梔,ki
林,na
鬧,lau
跡,tsiah
猶,iu
妝,tsong
成,tshiann
悼,to
旋,suan
頌,siong
戀,luan
欖,lam
憔,tsiau
悴,tsui
薦,tsian
蘊,un
最,tsue
尤,iu
似,su
趨,tshu
溝,koo
嘗,siong
維,ui
措,tshoo
饋,kui
污,u
莓,mui
綜,tsong
嚇,hik
繫,he
鍛,tuan
始,su
掣,tshiat
霞,he
妣,pi
圇,ng
筒,tong
霖,lim
鑾,luan
域,hik
磐,phuan
磐,puann
坦,thann
紀,ki
扭,niu
離,li
嗇,sik
嗇,siah
魅,bi
與,i
餘,i
可,khoo
佔,tsiam
吧,pa
汪,ong
附,hu
咇,phih
侷,kiok
哎,ai
衍,ian
娛,goo
探,than
脫,thut
耞,kenn
喪,song
焚,hun
菁,tsing
搜,soo
撇,phiat
甄,tsin
翡,hui
潰,khui
閱,uat
噯,ai
樸,phoh
諮,tsu
遴,lin
鴕,to
鴟,ba
韓,han
檯,tai
殯,pin
邏,lo
蠶,tshan
蝕,sik
棟,tang
沉,tiam
晟,sing
施,si
叢,tsang
絢,hian
役,iah
長,tshiang
墼,kat
托,thok
餒,lue
楚,tshoo
胴,tang
劃,ik
假,ka
假,ke
仔,ah
柝,khok
殗,gian
利,li
枷,kha
苔,ti
𨂿,uainnh
栱,kong
儱,lang
𡳞神氣,lan sin khui
𡳞鳥頭,lan tsiau thau
𩵱仔魚,ngoo a hi
𪁎雞鵤,tshio ke kak
𡢃婢,kan pi
𤆬頭的,tshua thau e
䆀火,bai hue
𦊓仔,ling a
𩸙魚,tai hi
𣁳仔車,khat a tshia
㴙㴙唸,tshap tshap liam
𤺪𤺪,sian sian
𤺪頭,sian thau
𫝏喙齒,gan tshui khi
𬦰崎,peh kia
一心,it sim
一目𥍉,tsit bak nih
一個月,tsit ko gueh
一晡,tsit poo
一絲仔,tsit si a
十八仔,sip pat a
九月重陽,kau gueh tiong iong
九芎仔柴,kiu kiong a tsha
九芎仔樹,kiu kiong a tshiu
大手面,tua tshiu bin
子仔,tsi a
下沿,e ian
山剌,suann luah
大割,tua kuah
糋棗仔,tsinn tso a
山藥薯,suann ioh tsi
上墓,tshiunn bong
大頭狗母,tua thau kau bo
歹代誌,phainn tai tsi
月仔錢,gueh a tsinn
歹去,phainn khi
天欲光,thinn beh kng
水滇,tsui tinn
月薪,gueh sin
半肥瘦,puann pui san
外家厝,gua ke tshu
本地人,pun te lang
失面子,sit bin tsu
巧骨,khiau kut
幼糠,iu khng
犯人欹,huan lang khia
玉米,giok bi
石兵仔,tsioh ping a
瓦杮,hia phue
白魚,peh hi
份會仔,hun hue a
合口味,hah khau bi
冰水,ping tsui
各心,koh sim
在手,tsai tshiu
在先,tsai sian
冰枕,ping tsim
好代誌,ho tai tsi
好字運,ho ji un
年老,ni lau
好消息,ho siau sit
好報,ho po
好報應,ho po ing
早時,tsa si
早起時,tsa khi si
有錢,u tsinn
肉丸,bah uan
行山,kiann suann
老指,lo tsainn
肉食,bah sit
老歲仔目,lau hue a bak
含仔糖,kam a thng
呃刺酸,eh tshiah sng
扲手,gim tshiu
批橐仔,phue lok a
抄錄,tshau lik
私偏,su phian
秀箠仔,siu tshue a
芋仔冰,oo a ping
那卡西,na ga sih
車鼓,tshia koo
拄拄仔好,tu tu a ho
拉圇燒,la lun sio
油渣,iu tse
花斑馬,hue pan be
金斗公,kim tau kong
雨白,hoo peh
便條紙,pian tiau tsua
便當盒仔,pian tong ap a
勇將,iong tsiong
屏風,pin hong
挂紙錢,kui tsua tsinn
硞仔,khok a
玲瑯仔,lin long a
相紲,sio sua
致到,ti kau
紅鳳菜,ang hong tshai
衫弓仔,sann king a
衫仔架,sann a ke
衫架仔,sann ke a
面框,bin khing
香案桌,hiunn an toh
倒栽,to tsai
哭齣,khau tshut
娘仔觳,niu a khok
捌代誌,bat tai tsi
桑仔樹,sng a tshiu
書架,tsu ke
狹櫼櫼,eh tsinn tsinn
祖公屎,tsoo kong sai
祖公產,tsoo kong san
笑面,tshio bin
笊籬,tsuann li
紙字,tsua ji
耽誤,tann goo
草坪,tshau penn
脆氣,tshe khui
草場,tshau tiunn
袂和盤,be ho puann
衰旺,sue ong
衰潲運,sue siau un
送上山頭,sang tsiunn suann thau
起毛管,khi mng kng
送葬,sang tsong
高長大漢,ko tshiang tua han
偷做手,thau tso tshiu
堅痡,kian poo
寄喙,kia tshui
戛仔頭,khiat a thau
掛念,kua liam
掛軸,kua tik
望遠鏡,bong uan kiann
斬稻仔尾,tsann tiu a bue
淡薄,tam poh
笛仔,tat a
移徙,i sua
祭墓,tse bong
粗牙,tshoo ge
細食,se tsiah
粗跤粗手,tshoo kha tshoo tshiu
規大堆,kui tua tui
規日,kui jit
覓頭路,ba thau loo
連相紲,lian sio sua
頂沿,ting ian
魚乾,hi kuann
喀喀嗽,khennh khennh sau
善報,sian po
報冤仇,po uan siu
換喙齒,uann tshui khi
無按怎,bo an tsuann
無面子,bo bin tsu
無理,bu li
無關係,bo kuan he
琴鐘仔,khim tsing a
短工,te kang
絕囝絕孫,tseh kiann tseh sun
絕嗣,tsuat su
量其約仔,liong ki iok a
傳香煙,thng hiunn ian
債挩,tse thuah
媽姨,ma i
微微仔笑,bi bi a tshio
揫墓,tshiu bong
摃電話,kong tian ue
搖鼓,io koo
搧緣投,sian ian tau
會和盤,e ho puann
會通,e thong
暗墨墨,am bak bak
萬姓公,ban senn kong
萬善公,ban sian kong
葛薯,kuah tsi
試覓,tshi mai
試鹹淡,tshi kiam tann
跤頭腕,kha thau uann
過定,kue tiann
運將,un tsiang
零星的,lan san e
鴣黃,koo ng
鼓電話,koo tian ue
漚翕熱,au hip juah
熁燒,hannh sio
熇熱,ho juah
銅人,tang lang
齊心,tse sim
樟腦丸,tsiunn lo uan
瘦疕疕,san phi phi
蝻蛇,lam tsua
褒囉嗦,po lo so
齒抿,khi bin
鬧鐘仔,nau tsing a
橫痃,huainn hian
燒水袋,sio tsui te
燒水罐,sio tsui kuan
獨身仔,tok sin a
燈油,ting iu
燒罐,sio kuan
興敗,hing pai
頭擴,thau khok
觳仔餅,khok a piann
講嘐潲,kong hau siau
講戇話,kong gong ue
霜仔角,sng a kak
擲挕捒,tan hinn sak
礐仔蟲,hak a thang
翻流,huan lau
醬瓜,tsiunn kue
雜色牌,tsap sik pai
雜差仔,tsap tshe a
雜貨仔,tsap hue a
嚨喉鐘仔,na au tsing a
歹消息,phainn siau sit
獻紙,hian tsua
觸喙,tak tshui
鹹閣澀,kiam koh siap
鹹澀,kiam siap
總舖,tsong phoo
暗挲挲,am so so
無聊無賴,bo liau bo le
纏跤纏手,tinn kha tinn tshiu
搭椅搭桌,tah i tah toh
磕未著,khap bue tioh
倒轉來,to tng lai
喙瀾水,tshui nua tsui
出箠,tshut tshue
粉腸,hun tng
魚鰡,hi liu
碣仔,khiat a
大段,tai tuan
半上路下,puann tsiunn loo e
半中途,puann tiong too
本居,pun ki
本籍,pun tsik
含血噴天,kam hueh phun thinn
夾鼎,kiap tiann
夾鍋,kiap ue
擦仔,tshat a
石拭仔,tsioh tshit a
明呼明唱,bing hoo bing tshiang
雨捽仔,hoo sut a
會赴,e hu
高長四壯,ko tshiang si tsang
穿榫,tshing sun
接尪,tsih ang
穩仔冬,un a tang
下冬,e tang
冰的,ping e
敆釉,kap iu
無捨無施,bo sia bo si
筊窟,kiau khut
坐不是,tshe put si
會不是,hue put si
實頭實腦,tsat thau tsat nau
跙冰,tshu ping
懶相,nua siunn
徼兆,khiau tiau
漚熱,au juah
漚熱,au juah
齷齪熱,ak tsak juah
鹹淘,kiam tua
空間,khang king
一大片,tsit tua phinn
三角肩,sann kak king
大母人大母種,tua bu lang tua bu tsing
大身命,tua sin mia
大聲野喉,tua siann ia au
反供,huan king
翻口供,huan khau king
心狂燥熱,sim kong so jiat
手縫疏,tshiu phang se
月戴笠,gueh ti leh
歹彩頭,phainn tshai thau
歹頭彩,phainn thau tshai
好吉兆,ho kiat tiau
好頭彩,ho thau tshai
水秤,sui tshin
水窟,tsui khut
水垢,tsui kau
牛角𨂿,gu kak uainnh
水牛,sui gu
水牛犅,tsui gu kang
山牛犅,suann gu kang
牛鼻環,gu phinn khuan
牛鼻圈仔,gu phinn khian a
𫝛心,siang sim
仝勻,kang un
仝輩,kang pue
書店,tsu tiam
司公象桮結相黏,sai kong siunn pue kat sio liam
童乩桌頭,tang ki toh thau
褲帶結相黏,khoo tua kat sio liam
外庄頭,gua tsng thau
本埠,pun poo
假範,ke pan
目睭掩,bak tsiu iam
走胎,tsau thai
冰絞,ping ka
歹事,phainn su
間格,king keh
造作,tso tsok
合作,kap tsoh
竹部,tik pho
肉屑,bah sut
零星肉,lan san bah
肉卷,bah kng
香櫞,hiunn inn
凊嗽,tshin sau
盍會,khah e
孝尾,ha bue
見功效,kinn kong hau
鬥走,tau tsau
走書,tsau tsu
卸世上,sia si tsiunn
孤孀,koo sng
向陣仔,hiang tsun a
拍鳥帽仔,phah tsiau bo a
痟貓,siau niau
金閃閃,kim siam siam
金爍爍,kim sih sih
門下臼,mng e khu
門下栿,mng e hok
品寶,phin po
滿員,buan uan
歹面腔,phainn bin khiunn
硩紙,teh tsua
挂墓紙,kui bong tsua
竭仔頭,kiat a thau
竭仔哥,kiat a ko
柿霜粉,khi song hun
為非作歹,ui hui tsok tai
相揣坐,sio tshue tse
平信,ping sin
時鐘瓜,si tsing kue
滷熟肉,loo siok bah
笑吻吻,tshio bun bun
草垺,tshau pu
虛身荏底,hi sin lam te
起豹風,khi pa hong
水退,tsui the
做旱,tso uann
剪蚻,tsian tsuah
跋馬,puah be
跋落馬,puah loh be
踮空龜,tiam khang ku
跤手慢鈍,kha tshiu ban tun
跤手扭掠,kha tshiu liu liah
利市,li tshi
摻濫,tsham lam
博土,phok thoo
毒心,tak sim
墮胎,tui thai
有塊,u te
耐命,nai mia
寬行,khuann kiann
黃目樹,ng bak tshiu
扶後跤,phoo au kha
越唸,uat liam
暗記,am ki
準煞,tsun suah
煞了代,suah liau tai
忍尿,lun jio
疊貨,thiap hue
落殼,lak khak
凡若,huan na
挨挨𤲍𤲍,e e kheh kheh
雨閘,hoo tsah
雨棚,hoo penn
剺花,leh hue
相耽誤,sann tann goo
歌仔簿,kua a phoo
綿綿精精,mi mi tsinn tsinn
慢氣,ban khui
輕便,khing pian
大𡳞脬,tua lan pha
滿山紅,mua suann ang
報春花,po tshun hue
無張無持,bo tiunn bo ti
究勘,kiu kham
蓮苞頭,lian poo thau
蝦繭,he kian
究真,kiu tsin
窮實,khing sit
閬蹘,lang liau
辟走,phiah tsau
孽畜仔話,giat thiok a ue
燈籃仔花,ting na a hue
抾菜,khioh tshai
雄骨,hiong kut
臨時臨陣,lim si lim tsun
圓栱橋,uan kong kio
相趁相喊,sio than sio han
鐵釘夾,thih ting ngeh
變無路,pian bo loo
變無空,pian bo khang
變魍,pinn bang
豔麗,iam le
菜鴿目,tshai kap bak
醡母草,tsa bu tshau
醡漿草,tsa tsiunn tshau
𣻸肭肭,siunn leh leh
分食,pun tsiah
無藝,bo ge
無俗,bo sioh
山裡,suann li
㾀命,khiap mia
拄拄仔,tu tu a
頭先仔,thau sing a
暗靜,am tsinn
可以,kho i
如果,ju ko
因此,in tshu
公司,kong si
問題,bun te
使用,su iong
不過,put ko
開始,khai si
已經,i king
必須,pit su
報導,po to
指出,tsi tshut
產品,san phin
如何,ju ho
需要,su iau
認為,jin ui
大陸,tai liok
包括,pau kuat
非常,hui siong
功能,kong ling
攝影,liap iann
業者,giap tsia
成為,sing ui
任何,jim ho
成長,sing tiong
要求,iau kiu
容易,iong i
國家,kok ka
個人,ko jin
股市,koo tshi
決定,kuat ting
地區,te khu
推出,thui tshut
能力,ling lik
了解,liau kai
產生,san sing
加上,ka siong
進入,tsin jip
技術,ki sut
情況,tsing hong
資訊,tsu sin
廠商,tshiunn siong
原因,guan in
最近,tsue kin
效果,hau ko
造成,tso sing
音樂,im gak
不斷,put tuan
傳統,thuan thong
顯示,hian si
資金,tsu kim
相關,siong kuan
網路,bang loo
尤其,iu ki
女性,lu sing
過程,kue ting
中國,tiong kok
軟體,nng the
警方,king hong
透過,thau kue
強調,kiong tiau
人士,jin su
狀況,tsong hong
專業,tsuan giap
程式,ting sik
並且,ping tshiann
需求,su kiu
演出,ian tshut
兩岸,liong huann
員工,uan kang
因素,in soo
安全,an tsuan
加入,ka jip
改善,kai sian
合作,hap tsok
此外,tshu gua
系列,he liat
球員,kiu uan
一切,it tshe
減少,kiam tsio
網站,bang tsam
創作,tshong tsok
吸引,khip in
長期,tng ki
控制,khong tse
醫師,i su
觀眾,kuan tsiong
呈現,thing hian
購買,koo be
訓練,hun lian
積極,tsik kik
導演,to ian
家庭,ka ting
清楚,tshing tsho
針對,tsiam tui
提升,the sing
所謂,soo ui
媒體,mui the
提高,the ko
筆者,pit tsia
不可,put kho
有關,iu kuan
負責,hu tsik
風險,hong hiam
製作,tse tsok
附近,hu kin
金融,kim iong
品牌,phin pai
面對,bin tui
訊息,sin sit
多少,to siau
分析,hun sik
規畫,kui ue
利率,li lut
舉辦,ki pan
專家,tsuan ka
球隊,kiu tui
共同,kiong tong
股價,koo ke
降低,kang ke
參與,tsham u
不再,put tsai
或者,hik tsia
不管,put kuan
主題,tsu te
感受,kam siu
表達,piau tat
策略,tshik liok
終於,tsiong i
預算,i suan
快速,khuai sok
科技,kho ki
達到,tat kau
民國,bin kok
再度,tsai too
形成,hing sing
角度,kak too
指數,tsi soo
原來,guan lai
多數,to soo
房地產,pang te san
畫面,ue bin
正常,tsing siong
相對,siong tui
推動,thui tong
擔心,tam sim
汽車,khi tshia
人類,jin lui
理想,li siong
女人,lu jin
工具,kang ku
立委,lip ui
風格,hong keh
機構,ki koo
類似,lui su
正是,tsiann si
正確,tsing khak
狀態,tsong thai
資源,tsu guan
趨勢,tshu se
立法院,lip huat inn
模式,boo sik
整體,tsing the
不足,put tsiok
關鍵,kuan kian
保持,po tshi
帶來,tua lai
公尺,kong tshioh
亞洲,a tsiu
重點,tiong tiam
投入,tau jip
從事,tsiong su
設定,siat ting
業績,giap tsik
不論,put lun
金額,kim giah
財務,tsai bu
等等,ting ting
前往,tsian ong
題材,te tsai
全部,tsuan poo
面臨,bian lim
參考,tsham kho
期貨,ki hue
之間,tsi kan
營運,ing un
比例,pi le
完整,uan tsing
男性,lam sing
結構,kiat koo
硬碟,nge tiap
網際網路,bang tse bang loo
餐廳,tshan thiann
擴大,khok tai
有效,u hau
展現,tian hian
成員,sing uan
陸續,liok siok
強烈,kiong liat
情感,tsing kam
藝術家,ge sut ka
變成,pian sing
大眾,tai tsiong
如今,ju kim
形象,hing siong
差異,tsha i
溝通,koo thong
才能,tsai ling
中央,tiong iong
全球,tsuan kiu
看法,khuann huat
團體,thuan the
對方,tui hong
不如,put ju
個性,ko sing
董事長,tang su tiunn
大約,tai iok
小組,sio tsoo
來自,lai tsu
想像,siong siong
遊客,iu kheh
首先,siu sian
引進,in tsin
以往,i ong
時期,si ki
財富,tsai hu
國外,kok gua
辦公室,pan kong sik
優勢,iu se
人口,jin khau
外資,gua tsu
促銷,tshiok siau
旅遊,li iu
教練,kau lian
學者,hak tsia
估計,koo ke
院長,inn tiunn
意識,i sik
藥物,ioh but
投手,tau tshiu
接近,tsiap kin
採取,tshai tshu
興建,hing kian
以免,i bian
扮演,pan ian
良好,liong ho
居民,ki bin
空氣,khong khi
突破,tut phua
售價,siu ke
紀錄,ki lok
造型,tso hing
報名,po mia
營收,ing siu
安裝,an tsong
快樂,khuai lok
不只,put tsi
休閒,hiu han
行業,hang giap
創意,tshong i
運作,un tsok
樂團,gak thuan
屬於,siok i
外界,gua kai
任務,jim bu
年代,ni tai
業界,giap kai
黨團,tong thuan
技巧,ki kha
型態,hing thai
紛紛,hun hun
球迷,kiu be
想法,siunn huat
人體,jin the
食用,sit iong
設置,siat ti
連線,lian suann
評估,phing koo
預測,i tshik
領導,ling to
調降,tiau kang
大師,tai su
大概,tai khai
心態,sim thai
手法,tshiu huat
全面,tsuan bin
深入,tshim jip
理由,li iu
焦點,tsiau tiam
螢幕,ing boo
年齡,ni ling
具備,ku pi
保障,po tsiong
架構,ka koo
透露,thau loo
魅力,bi lik
之外,tsi gua
只有,tsi u
依據,i ki
參觀,tsham kuan
這種,tsit tsiong
會員,hue uan
競選,king suan
西元,se guan
爭議,tsing gi
研發,gian huat
浪漫,long ban
海軍,hai kun
配備,phue pi
唱片,tshiunn phinn
推薦,thui tsian
腸病毒,tng penn tok
寫真集,sia tsin tsip
體重,the tang
升級,sing kip
引發,in huat
以為,i ui
出生,tshut senn
社區,sia khu
特質,tik tsit
達成,tat sing
包含,pau ham
車款,tshia khuan
供應,kiong ing
爭取,tsing tshu
族群,tsok kun
通訊,thong sin
慢慢,ban ban
潛力,tsiam lik
一向,it hiong
召開,tiau khui
成熟,sing sik
行銷,hing siau
預定,i ting
譬如,phi ju
互動,hoo tong
心靈,sim ling
失去,sit khi
性能,sing ling
促進,tshiok tsin
指標,tsi piau
英文,ing bun
素描,soo bio
措施,tshoo si
異常,i siong
過敏,kue bin
預防,i hong
領域,ling hik
主機板,tsu ki pan
外銷,gua siau
交友,kau iu
利潤,li jun
信託,sin thok
科系,kho he
海外,hai gua
整合,tsing hap
歹徒,phainn too
早期,tsa ki
行程,hing ting
究竟,kiu king
金錢,kim tsinn
密切,bit tshiat
描述,biau sut
概念,kai liam
話題,ue te
衝擊,tshiong kik
加速,ka sok
好好,ho ho
彷彿,hong hut
東南亞,tang lam a
記錄,ki lok
象徵,siong ting
進一步,tsin tsit poo
熱門,jiat mng
機率,ki lut
親自,tshin tsu
錄音帶,lok im tua
環保,khuan po
吸收,khip siu
身上,sin siong
取代,tshu tai
初期,tshoo ki
音響,im hiong
偵辦,tsing pan
帶動,tai tong
畢業,pit giap
組成,tsoo sing
飲食,im sit
當代,tong tai
裝置,tsong ti
管道,kuan to
分享,hun hiong
反映,huan ing
成果,sing ko
身份,sin hun
空軍,khong kun
指定,tsi ting
展出,tian tshut
規格,kui keh
畫家,ue ka
奧運,Ò un
網友,bang iu
領先,ling sian
層次,tsan tshu
播出,poo tshut
大型,tua hing
臺商,tai siong
迅速,sin sok
版本,pan pun
美好,bi ho
核心,hik sim
特效,tik hau
連結,lian kiat
質疑,tsit gi
上升,siong sing
上師,siong su
介入,kai jip
元件,guan kiann
付出,hu tshut
行政,hing tsing
來源,lai guan
時刻,si khik
探討,tham tho
互相,hoo siong
反彈,huan tuann
方案,hong an
生態,sing thai
全力,tsuan lik
完美,uan bi
抗生素,khong sing soo
定位,ting ui
為何,ui ho
家屬,ka siok
病患,penn huan
景觀,king kuan
森林,sim lim
結婚,kiat hun
障礙,tsiong gai
議題,gi te
不良,put liong
比率,pi lut
出任,tshut jim
平衡,ping hing
因應,in ing
防止,hong tsi
忽略,hut liok
國民,kok bin
實質,sit tsit
認知,jin ti
績效,tsik hau
類型,lui hing
化妝,hua tsong
水彩,tsui tshai
出去,tshut khi
出發,tshut huat
車輛,tshia liong
依照,i tsiau
取得,tshu tit
要道,iau to
家族,ka tsok
特性,tik sing
排名,pai mia
現今,hian kim
幅度,hok too
晶片,tsing phinn
幹部,kan poo
落實,lok sit
澈底,thiat te
歌劇,kua kiok
數據,soo ki
確保,khak po
器材,khi tsai
機種,ki tsiong
競爭力,king tsing lik
人選,jin suan
下降,ha kang
主委,tsu ui
金屬,kim siok
盈餘,ing u
看出,khuann tshut
原先,guan sian
高層,ko tsan
國王,kok ong
理念,li liam
畢竟,pit king
細胞,se pau
就業,tsiu giap
超越,tshiau uat
證實,tsing sit
關於,kuan i
人力,jin lik
上下,siong ha
上班,siong pan
大樓,tua lau
中文,tiong bun
平交道,ping kau to
企圖,khi too
明確,bing khak
重複,tiong hok
球團,kiu thuan
部門,poo mng
硬體,nge the
當中,tang tiong
標示,piau si
熱烈,jiat liat
縣府,kuan hu
錄取,lok tshu
寵物,thiong but
不利,put li
不幸,put hing
他人,thann jin
共識,kiong sik
決議,kuat gi
性別,sing piat
服飾,hok sik
物質,but tsit
客語,kheh gi
持有,tshi iu
軍方,kun hong
展示,tian si
案例,an le
記憶體,ki ik the
密碼,bit be
專案,tsuan an
教科文,kau kho bun
現任,hian jim
眾多,tsiong to
提昇,the sing
經建會,king kian hue
層面,tsan bin
主導,tsu to
平時,ping si
回應,hue ing
好處,ho tshu
血液,hueh ik
抗爭,khong tsing
事物,su but
協商,hiap siong
定義,ting gi
訂單,ting tuann
衰退,sue the
排除,pai tu
惡化,ok hua
路線,loo suann
對話,tui ue
演唱,ian tshiunn
醫療,i liau
體系,the he
中部,tiong poo
外匯,gua hue
困擾,khun jiau
材質,tsai tsit
服用,hok iong
炒作,tsha tsok
皇后,hong hio
美食,bi sit
背後,pue au
英語,ing gi
原住民,guan tsu bin
高音,ko im
國會,kok hue
專用,tsuan iong
強化,kiong hua
期望,ki bong
減肥,kiam pui
傳說,thuan suat
跳票,thiau phio
構想,koo siong
廣泛,kong huan
模組,boo tsoo
閱讀,uat thok
轉換,tsuan uann
競賽,king sai
大會,tai hue
女子,lu tsu
公佈,kong poo
水質,tsui tsit
外表,gua piau
回饋,hue kui
如同,ju tong
決策,kuat tshik
車主,tshia tsu
物品,but phin
保養,po iong
指令,tsi ling
首長,siu tiunn
效益,hau ik
效應,hau ing
特定,tik ting
追蹤,tui tsong
眷村,kuan tshun
細節,se tsiat
報酬,po siu
視覺,si kak
飲料,im liau
維護,ui hoo
樂器,gak khi
頻頻,pin pin
講義,kang gi
贈與,tsing u
邊緣,pian ian
大盤,tua puann
主流,tsu liu
冷戰,ling tsian
紀念,ki liam
娛樂,goo lok
差別,tsha piat
差距,tsha ki
動力,tong lik
從此,tsiong tshu
產能,san ling
場地,tiunn te
訴求,soo kiu
節奏,tsiat tsau
經銷,king siau
農會,long hue
輕易,khin i
儀式,gi sik
確認,khak jin
歡樂,huan lok
公頃,kong khing
以上,i siong
在野黨,tsai ia tong
成份,sing hun
成交,sing kau
車型,tshia hing
券商,kuan siong
受傷,siu siong
法人,huat jin
前衛,tsian ue
約診,iok tsin
美金,bi kim
家具,ka ku
氣候,khi hau
貨幣,hue pe
單曲,tuann khik
傳達,thuan tat
管制,kuan tse
精英,tsing ing
網球,bang kiu
播放,poo hong
賣場,be tiunn
選購,suan koo
癌症,gam tsing
鎖定,so ting
觀點,kuan tiam
一再,it tsai
分紅,pun ang
比重,pi tang
牛肉,gu bah
主機,tsu ki
出貨,tshut hue
必需,pit su
名稱,mia tshing
行庫,hang khoo
助益,tsoo ik
其次,ki tshu
典型,tian hing
延伸,ian sin
飛行,hui hing
個別,ko piat
校園,hau hng
素材,soo tsai
婚姻,hun in
專輯,tsuan tsip
規範,kui huan
部隊,poo tui
朝野,tiau ia
進度,tsin too
開店,khui tiam
溫和,un ho
溫度,un too
滑鼠,kut tshi
營造,ing tso
聯盟,lian bing
變動,pian tong
不得,put tik
文宣,bun suan
主力,tsu lik
代價,tai ke
出血,tshut hueh
地面,te bin
安定,an ting
行使,hing su
否認,honn jin
告知,ko ti
私人,su jin
延長,ian tng
承諾,sing lok
近日,kin jit
近期,kin ki
附設,hu siat
南部,lam poo
持股,tshi koo
施工,si kang
突出,tut tshut
郊遊,kau iu
重心,tiong sim
風景,hong king
修憲,siu hian
原始,guan si
時數,si soo
氣質,khi tsit
能量,ling liong
航線,hang suann
動畫,tong ue
排氣,pai khi
敘述,su sut
產量,san liong
通路,thong loo
連接,lian tsiap
麻煩,ma huan
單一,tan it
復甦,hok soo
等級,ting kip
園區,hng khu
違規,ui kui
預料,i liau
劃撥,ueh puah
團員,thuan uan
舞蹈,bu to
縣市,kuan tshi
選戰,suan tsian
優良,iu liong
屬性,siok sing
顯著,hian tu
大自然,tai tsu jian
刊登,khan ting
外型,gua hing
生物,sing but
生涯,sing gai
用來,iong lai
安打,an tann
住宅,tsu theh
改進,kai tsin
威力,ui lik
庫存,khoo tsun
國產,kok san
強大,kiong tai
理性,li sing
評審,phing sim
進駐,tsin tsu
農藥,long ioh
預賽,i sai
團隊,thuan tui
認養,jin iong
履歷表,li lik pio
談話,tam ue
學員,hak uan
據點,ki tiam
整個,tsing ko
總部,tsong poo
櫃台,kui tai
權益,khuan ik
一片,it phian
人間,jin kan
口味,khau bi
比如,pi ju
出國,tshut kok
半導體,puann to the
古老,koo lo
巨蛋,ki tan
市面,tshi bin
回升,hue sing
存取,tsun tshu
折扣,tsiat khau
身邊,sin pinn
車廠,tshia tshiunn
法案,huat an
青光眼,tshenn kong gan
建造,kian tso
指責,tsi tsik
負面,hu bin
飛安,hui an
員警,uan king
核武,hik bu
氣勢,khi se
神壇,sin tuann
祕密,pi bit
納入,lap jip
強力,kiong lik
票房,phio pang
描繪,biau hue
港口,kang khau
登錄,ting lok
塑造,sok tso
當局,tong kiok
試辦,tshi pan
資深,tsu tshim
圖像,too siong
遠離,uan li
增添,tsing thiam
數位,soo ui
暴力,po lik
樂章,gak tsiong
熱情,jiat tsing
熱量,jiat liong
優惠,iu hui
擺脫,pai thuat
爆發,pok huat
魔法,moo huat
一貫,it kuan
人數,jin soo
上場,tsiunn tiunn
大批,tua phue
不孕,put in
不安,put an
不宜,put gi
介面,kai bin
支付,tsi hu
王子,ong tsu
主演,tsu ian
以來,i lai
半年,puann ni
石頭,tsioh thau
回憶,hue ik
多媒體,to mui the
年級,ni kip
兩性,liong sing
周邊,tsiu pinn
往來,ong lai
忽視,hut si
性愛,sing ai
拓展,thok tian
拆除,thiah tu
放大,hong tua
注重,tsu tiong
肢體,ki the
股權,koo khuan
近年,kin ni
革命,kik bing
風味,hong bi
風潮,hong tiau
展望,tian bong
時段,si tuann
配樂,phue gak
商機,siong ki
國軍,kok kun
從來,tsiong lai
敏感,bin kam
眼壓,gan ap
被害人,pi hai jin
部屬,poo siok
陰影,im iann
創新,tshong sin
提早,the tsa
華人,hua jin
華文,hua bun
傳輸,thuan su
過濾,kue li
圖形,too hing
精彩,tsing tshai
認證,jin tsing
模擬,boo gi
賣出,be tshut
適用,sik iong
戰機,tsian ki
機師,ki su
觀賞,kuan siong
一時,tsit si
下面,e bin
下載,ha tsai
不解,put kai
公克,kong khik
公噸,kong tun
收益,siu ik
自從,tsu tsiong
位元,ui guan
局部,kiok poo
更加,king ka
更新,king sin
東方,tang hong
法院,huat inn
宣導,suan to
珍貴,tin kui
風貌,hong mau
涉嫌,siap hiam
特徵,tik ting
高峰,ko hong
動態,tong thai
情歌,tsing kua
登陸,ting liok
發佈,huat poo
集體,tsip the
傳送,thuan sang
經由,king iu
裝備,tsong pi
電機,tian ki
零件,ling kiann
構成,koo sing
說服,sue hok
廣播,kong poo
誕生,tan sing
選民,suan bin
幫派,pang phai
檢方,kiam hong
轉移,tsuan i
額度,giah too
聽說,thiann sueh
變數,pian soo
體制,the tse
分手,hun tshiu
分泌,hun pi
代號,tai ho
功力,kong lik
民調,bin tiau
甲板,kah pan
地球,te kiu
有意,iu i
有線,iu suann
困境,khun king
快門,khuai mng
攻勢,kong se
和諧,ho hai
固然,koo jian
底部,te poo
延續,ian siok
法則,huat tsik
便利,pian li
保齡球,po ling kiu
星座,sing tso
相容,sio iong
看來,khuann lai
面試,bian tshi
音效,im hau
風情,hong tsing
核准,hik tsun
淘汰,to thai
淨化,tsing hua
被告,pi ko
連任,lian jim
減輕,kiam khin
無力,bo lat
評分,phing hun
進出,tsin tshut
傳遞,thuan te
歲月,sue guat
實用,sit iong
監視,kam si
算是,sng si
緊急,kin kip
廣大,kong tai
獎項,tsiong hang
論壇,lun tuann
適應,sik ing
戰力,tsian lik
優異,iu i
薪資,sin tsu
人身,jin sin
人潮,jin tiau
大選,tai suan
女士,lu su
子女,tsu lu
今後,kim au
公賣局,kong be kiok
方針,hong tsiam
水墨,tsui bak
外在,gua tsai
市區,tshi khu
平面,penn bin
本質,pun tsit
民選,bin suan
合成,hap sing
作風,tsok hong
形態,hing thai
役男,ik lam
改編,kai pian
車商,tshia siong
車體,tshia the
事項,su hang
念頭,liam thau
放牧,pang bok
制憲,tse hian
芭蕾,pa le
研判,gian phuann
夏日,ha jit
桌球,toh kiu
留意,liu i
財經,tsai king
配置,phue ti
除了,tu liau
停留,thing liu
區分,khu hun
國小,kok sio
基層,ki tsan
強勢,kiong se
授權,siu khuan
移送,i sang
景象,king siong
殘障,tsan tsiong
發言,huat gian
發票,huat phio
象牙,tshiunn ge
開拓,khai thok
匯市,hue tshi
嫌犯,hiam huan
照明,tsio bing
碎片,tshui phinn
經貿,king boo
農委會,long ui hue
漢聲,han sing
劇情,kiok tsing
模型,boo hing
線條,suann tiau
機車,ki tshia
親屬,tshin siok
優雅,iu nga
縮小,sok sio
臨床,lim tshng
雙人,siang lang
關懷,kuan huai
體質,the tsit
觀測,kuan tshik
一日,tsit jit
人性,jin sing
入股,jip koo
不便,put pian
切換,tshiat uann
心得,sim tik
水平,tsui ping
代工,tai kang
出面,tshut bin
出院,tshut inn
用地,iong te
立院,lip inn
任意,jim i
冰山,ping suann
有機,iu ki
老太太,lau thai thai
行列,hang liat
行星,hing tshenn
占用,tsiam iong
佈滿,poo mua
改造,kai tso
男士,lam su
供給,kiong kip
弦樂,hian gak
波動,pho tong
法規,huat kui
社團,sia thuan
股利,koo li
長久,tng ku
促使,tshiok su
宣稱,suan tshing
拜會,pai hue
流失,liu sit
流星,liu tshenn
流通,liu thong
活力,uah lik
看待,khuann thai
秋冬,tshiu tang
美化,bi hua
美妙,bi miau
家電,ka tian
師生,su sing
時差,si tsha
書評,su phing
浴場,ik tiunn
秩序,tiat su
脆弱,tshui jiok
記載,ki tsai
酒精,tsiu tsing
高雅,ko nga
動人,tong jin
婦產科,hu san kho
專機,tsuan ki
教室,kau sik
教導,kau to
敗血症,pai hueh tsing
涵蓋,ham kai
現況,hian hong
異物,i but
統治,thong ti
船長,tsun tiunn
貨櫃,hue kui
釣魚,tio hi
就職,tsiu tsit
棉花,mi hue
稅賦,sue hu
視野,si ia
路面,loo bin
漁船,hi tsun
漁網,hi bang
維修,ui siu
增進,tsing tsin
憤怒,hun noo
激勵,kik le
聯想,lian siong
擴張,khok tiong
藝文,ge bun
贈品,tsing phin
難忘,lan bong
類別,lui piat
顯現,hian hian
人際,jin tse
下班,ha pan
干擾,kan jiau
不該,put kai
不變,put pian
分局,hun kiok
分離,hun li
戶外,hoo gua
主因,tsu in
刊物,khan but
用戶,iong hoo
石板,tsioh pan
示威,si ui
光線,kng suann
先發,sian huat
回收,hue siu
回顧,hue koo
地檢署,te kiam su
好笑,ho tshio
曲線,khiok suann
西部,se poo
忍受,jim siu
改組,kai tsoo
車身,tshia sin
典雅,tian nga
知名度,ti mia too
勇士,iong su
宣示,suan si
宣告,suan ko
美感,bi kam
哲學,tiat hak
捐款,kuan khuan
特區,tik khu
留學,liu hak
真愛,tsin ai
神祕,sin pi
純粹,sun tshui
院士,inn su
假日,ka jit
假設,ka siat
國產車,kok san tshia
堅強,kian kiong
基因,ki in
探索,tham soh
探測,tham tshik
採訪,tshai hong
啟明,khe bing
深深,tshim tshim
球季,kiu kui
都會,too hue
陳列,tin liat
圍標,ui pio
惡意,ok i
游泳,iu ing
無形,bu hing
無線,bo suann
發育,huat iok
童年,tong lian
華裔,hua e
郵購,iu koo
間諜,kan tiap
傾向,khing hiong
業餘,giap u
概況,kai hong
路段,loo tuann
運行,un hing
電器,tian khi
零售,ling siu
鼓舞,koo bu
對比,tui pi
質感,tsit kam
壁畫,piah ue
機能,ki ling
融合,iong hap
頭獎,thau tsiong
檢索,kiam sik
繁榮,huan ing
擴充,khok tshiong
釋放,sik hong
靈活,ling uah
下旬,ha sun
士氣,su khi
天線,thian suann
引用,in iong
心中,sim tiong
加盟,ka bing
古代,koo tai
外商,gua siong
外勞,gua lo
平日,ping jit
用品,iong phin
示範,si huan
交叉,kau tshe
地產,te san
守備,siu pi
寺院,si inn
收容,siu iong
收錄,siu lok
有利,iu li
自身,tsu sin
局長,kiok tiunn
扭曲,niu khiok
改建,kai kian
車禍,tshia ho
版畫,pan ue
金牌,kim pai
屍體,si the
後果,hio ko
後者,hio tsia
流程,liu ting
衍生,ian sing
訂做,ting tso
重量,tang liong
病房,penn pang
神父,sin hu
虔誠,khian sing
高溫,ko un
問卷,bun kuan
專櫃,tsuan kui
得票率,tik phio lut
情結,tsing kat
清查,tshing tsa
清理,tshing li
現成,hian sing
造勢,tso se
頂尖,ting tsiam
創下,tshong ha
勞基法,lo ki huat
敦煌,tun hong
普及,phoo kip
棉被,mi phue
無數,bu soo
結盟,kiat bing
隊友,tui iu
傳播,thuan poo
匯率,hue lut
會長,hue tiunn
會期,hue ki
精華,tsing hua
製品,tse phin
輕快,khin khuai
影視,iann si
課題,kho te
調度,tiau too
震盪,tsin tong
學院,hak inn
戰績,tsian tsik
融資,iong tsu
諮商,tsu siong
諮詢,tsu sun
頻率,pin lut
頻繁,pin huan
療程,liau ting
總理,tsong li
舉例,ki le
購併,koo ping
簡稱,kan tshing
攀岩,phan giam
藝人,ge jin
藥師,ioh su
關切,kuan tshiat
聽眾,thiann tsiong
入主,jip tsu
刀具,to ku
公告,kong ko
幻想,huan siong
手中,tshiu tiong
手冊,tshiu tsheh
日劇,jit kiok
出爐,tshut loo
平台,penn tai
打壓,tann ap
生動,sing tong
石化,tsioh hua
光碟,kong tiap
列印,liat in
同仁,tong jin
名詞,mia su
地板,te pan
字樣,ji iunn
宇宙,u tiu
成效,sing hau
有心,u sim
自治,tsu ti
含量,ham liong
完善,uan sian
技能,ki ling
投注,tau tsu
身心,sin sim
來電,lai tian
底價,te ke
承辦,sing pan
服役,hok ik
物種,but tsiong
花粉,hue hun
保育,po iok
派系,phai he
疫情,ik tsing
美軍,bi kun
降價,kang ke
音色,im sik
校方,hau hong
海龜,hai ku
特價,tik ke
神奇,sin ki
祝壽,tsiok siu
追查,tui tsa
陣容,tin iong
殺人,sat jin
清新,tshing sin
貪汙,tham u
透明,thau bing
博覽會,phok lam hue
報價,po ke
幾何,ki ho
智力,ti lik
焚化爐,hun hua loo
無尾熊,bo bue him
發光,huat kng
稅制,sue tse
進攻,tsin kong
暗房,am pang
當前,tong tsian
農林,long lim
圖案,too an
監控,kam khong
精品,tsing phin
豪華,ho hua
寫作,sia tsok
廠房,tshiunn pang
撰寫,tsuan sia
樂曲,gak khik
範例,huan le
衛浴,ue ik
遭受,tso siu
劑量,tse liong
憑證,pin tsing
整治,tsing ti
選出,suan tshut
頻道,pin to
頻寬,pin khuan
聯招,lian tsiau
擴展,khok tian
繳稅,kiau sue
關注,kuan tsu
一連串,it lian tshuan
大地,tai te
大多數,tua to soo
大門,tua mng
不等,put ting
不實,put sit
之中,tsi tiong
仇恨,siu hun
公車,kong tshia
心性,sim sing
木星,bok tshenn
水面,tsui bin
出廠,tshut tshiunn
功夫,kang hu
古典,koo tian
幼兒,iu ji
必定,pit ting
民航,bin hang
白人,peh lang
名牌,mia pai
回歸,hue kui
收聽,siu thiann
肉體,bah the
批判,phue phuann
村民,tshun bin
汽油,khi iu
車牌,tshia pai
併發症,ping huat tsing
東區,tang khu
東部,tang poo
武士,bu su
油畫,iu ue
空戰,khong tsian
空難,khong lan
金星,kim tshenn
前景,tsian king
南方,lam hong
客觀,kheh kuan
後座,au tso
政局,tsing kiok
毒品,tok phin
皇上,hong siong
面膜,bin mooh
時空,si khong
時報,si po
海邊,hai pinn
神通,sin thong
神聖,sin sing
起初,khi tshoo
退稅,the sue
閃電,siam tian
停車,thing tshia
偵測,tsing tshik
剪輯,tsian tsip
區運,khu un
國界,kok kai
密度,bit too
密集,bit tsip
專人,tsuan jin
專注,tsuan tsu
情節,tsing tsiat
排水,pai tsui
排出,pai tshut
教堂,kau tng
清真寺,tshing tsin si
淨利,tsing li
產銷,san siau
移交,i kau
粒子,liap tsu
連動,lian tong
連署,lian su
連鎖,lian so
殘骸,tsan hai
答覆,tap hok
視訊,si sin
週邊,tsiu pinn
開設,khai siat
傳奇,thuan ki
傳記,tuan ki
會勘,hue kham
極力,kik lik
經典,king tian
群體,kun the
補償,poo siong
過來,kue lai
對應,tui ing
網際,bang tse
聚會,tsu hue
領錢,nia tsinn
增長,tsing tiong
影迷,iann be
暴動,po tong
熱潮,jiat tiau
噪音,tsho im
學歷,hak lik
操控,tshau khong
錄製,lok tse
頭等艙,thau ting tshng
應邀,ing iau
縮短,sok te
績優股,tsik iu koo
糧食,niu sit
轉化,tsuan hua
轉播,tsuan poo
簽證,tshiam tsing
關機,kuainn ki
礦石,khong tsioh
警員,king uan
警廣,king kong
釋出,sik tshut
驅動,khu tong
體能,the ling
一邊,tsit pinn
上台,tsiunn tai
士兵,su ping
大海,tua hai
小提琴,sio the khim
不可思議,put kho su gi
內在,lue tsai
內涵,lue ham
公投,kong tau
公關,kong kuan
分子,hun tsu
分佈,hun poo
分解,hun kai
分辨,hun pian
化解,hua kai
友善,iu sian
反射,huan sia
天體,thian the
心智,sim ti
日產,jit san
月份,gueh hun
水位,tsui ui
主治,tsu ti
可見,kho kian
臺海,tai hai
外來,gua lai
外殼,gua khak
外債,gua tse
平凡,ping huan
平方,ping hong
平穩,ping un
全體,tsuan the
同業,tong giap
地圖,te too
多角化,to kak hua
存活,tsun uah
安詳,an siong
年初,ni tshe
扣抵,khau ti
扣掉,khau tiau
此時,tshu si
死因,si in
汙染,u jiam
考核,kho hik
肉品,bah phin
技藝,ki ge
車殼,tshia khak
巡禮,sun le
來回,lai hue
坪數,penn soo
忠實,tiong sit
抽出,thiu tshut
拖吊,thua tiau
放心,hong sim
注入,tsu jip
河川,ho tshuan
油脂,iu tsi
肺癌,hi gam
表彰,piau tsiong
金曲,kim khik
型錄,hing lok
契約,khe iok
建商,kian siong
春夏,tshun ha
紅利,ang li
軍人,kun jin
面紙,bin tsua
容積率,iong tsik lut
效能,hau ling
書法,su huat
病變,penn pian
退出,the tshut
退燒,the sio
陣營,tin iann
除權,tu khuan
停火,thing hue
偶像,ngoo siong
副理,hu li
堅決,kian kuat
專利,tsuan li
專題,tsuan te
專欄,tsuan nua
強權,kiong khuan
情境,tsing king
接收,tsiap siu
推展,thui tian
教材,kau tsai
族人,tsok jin
現有,hian iu
設法,siat huat
連帶,lian tai
連續劇,lian siok kiok
釣友,tio iu
勞保,lo po
就醫,tsiu i
悲情,pi tsing
提示,the si
無比,bu pi
評價,phing ke
買進,be tsin
階層,kai tsan
群眾,kun tsiong
聖火,sing hue
聖誕,sing tan
電源,tian guan
對不起,tui put khi
旗下,ki ha
監工,kam kang
管弦,kuan hian
精選,tsing suan
誘惑,iu hik
儀器,gi khi
價差,ke tsha
審核,sim hik
履歷,li lik
廢棄物,hui khi but
適量,sik liong
鄰近,lin kin
學分,hak hun
機身,ki sin
燃料,jian liau
辦案,pan an
優質,iu tsit
壓縮,ap sok
瞬間,sun kan
隱私,un su
轉載,tsuan tsai
櫥窗,tu thang
簽訂,tshiam ting
關卡,kuan khah
韻律,un lut
嚴謹,giam kin
歡呼,huan hoo
邏輯,lo tsip
讚美,tsan bi
一流,it liu
入侵,jip tshim
三通,sam thong
大將,tai tsiong
山區,suann khu
中生代,tiong sing tai
中年,tiong lian
中音,tiong im
公主,kong tsu
公營,kong ing
切片,tshiat phinn
太平洋,thai ping iunn
心力,sim lik
文建會,bun kian hue
毛利率,moo li lut
水份,tsui hun
外用,gua iong
外形,gua hing
外流,gua lau
巧合,kha hap
平原,ping guan
民法,bin huat
民政局,bin tsing kiok
民營,bin ing
申報,sin po
皮件,phue kiann
企管,khi kuan
光芒,kong bong
全委會,tsuan ui hue
再見,tsai kian
收視,siu si
百分之百,pah hun tsi pah
老化,noo hua
自殺,tsu sat
佛珠,hut tsu
免疫,bian ik
抗體,khong the
更改,king kai
肝癌,kuann gam
身為,sin ui
車庫,tshia khoo
車廂,tshia siunn
巡迴,sun hue
享有,hiang iu
使命,su bing
受刑人,siu hing jin
奇幻,ki huan
季軍,kui kun
定存,ting tsun
定時,ting si
拓寬,thok khuan
抽象,thiu siong
玫瑰,mui kui
空中,khong tiong
肥料,pui liau
花樣,hue iunn
長官,tiong kuann
長度,tng too
門號,mng ho
阻力,tsoo lik
信奉,sin hong
信賴,sin nai
侵入,tshim jip
故意,koo i
施行,si hing
流入,lau jip
疫苗,ik biau
紅燈,ang ting
風暴,hong po
套裝,tho tsong
家家戶戶,ke ke hoo hoo
校區,hau khu
核發,hik huat
海內外,hai lai gua
海協會,hai hiap hue
特派員,tik phai uan
病例,penn le
純淨,sun tsing
財稅,tsai sue
起身,khi sin
迷宮,be kiong
院會,inn hue
高階,ko kai
高檔,ko tong
停損,thing sun
培育,pue iok
專長,tsuan tiong
接任,tsiap jim
接管,tsiap kuan
救災,kiu tsai
旋律,suan lut
牽涉,khan siap
理智,li ti
異動,i tong
異議,i gi
累計,lui ke
設廠,siat tshiunn
通行,thong hing
造林,tso lim
部會,poo hue
野狼,ia long
陳皮,tin phi
陸軍,liok kun
備份,pi hun
創立,tshong lip
報案,po an
散發,san huat
畫廊,ue long
發音,huat im
發射,huat sia
稅務,sue bu
賀卡,ho khah
量產,liong san
開朗,khai long
傳聞,thuan bun
傳藝中心,thuan ge tiong sim
傾銷,khing siau
極度,kik too
賄選,hue suan
電動,tian tong
預告,i ko
頒獎,pan tsiong
夢幻,bong huan
榮耀,ing iau
疑惑,gi hik
種田,tsing tshan
聞名,bun bing
製成,tse sing
銅鑼,tang lo
層級,tsan kip
影壇,iann tuann
數值,soo tit
熱線,jiat suann
編列,pian liat
請辭,tshing si
學年度,hak ni too
戰役,tsian ik
戰艦,tsian lam
機型,ki hing
融券,iong kuan
親子,tshin tsu
辨識,pian sik
鴕鳥,to tsiau
償還,siong huan
檔期,tong ki
檢測,kiam tshik
禪師,sian su
擴建,khok kian
禮品,le phin
簡化,kan hua
簡報,kan po
職籃,tsit na
藍圖,na too
騎士,khi su
穩健,un kian
顛覆,tian hok
寶石,po tsioh
繼承,ke sing
警政,king tsing
黨籍,tong tsik
驚喜,kiann hi
體委會,the ui hue
觀看,kuan khuann
不知不覺,put ti put kak
中正,tiong tsing
公務,kong bu
分裂,hun liat
引述,in sut
文物,bun but
日記,jit ki
主體,tsu the
加油,ka iu
去除,khi tu
古厝,koo tshu
奶水,ling tsui
打造,tann tso
民代,bin tai
民航局,bin hang kiok
白痴,peh tshi
皮椅,phue i
目光,bak kng
立法,lip huat
交響曲,kau hiong khik
任職,jim tsit
再生,tsai sing
刑警,hing king
同行,tong hang
名義,bing gi
守法,siu huat
年薪,ni sin
成品,sing phin
收費,siu hui
次要,tshu iau
自願,tsu guan
佛典,hut tian
何時,ho si
災區,tsai khu
災情,tsai tsing
車況,tshia hong
車隊,tshia tui
事宜,su gi
事蹟,su tsik
亞太,a thai
亞運,a un
受限,siu han
呼叫,hoo kio
官方,kuann hong
店長,tiam tiunn
所長,soo tiunn
放假,pang ka
武力,bu lik
法門,huat mng
空調,khong tiau
糾紛,kiu hun
侷限,kiok han
客家,kheh ka
柔軟,jiu nng
查詢,tsha sun
段落,tuann loh
毒性,tok sing
為主,ui tsu
相差,siong tsha
研討,gian tho
秋天,tshiu thinn
美商,bi siong
美景,bi king
致詞,ti su
重播,ting poo
重整,tiong tsing
音量,im liong
首頁,siu iah
修訂,siu ting
捕手,poo tshiu
格式,keh sik
格調,keh tiau
海上,hai siong
海域,hai hik
海報,hai po
海關,hai kuan
浮現,phu hian
浮游,phu iu
特點,tik tiam
班級,pan kip
缺失,khuat sit
迷人,be lang
酒吧,tsiu pa
針頭,tsiam thau
馬路,be loo
骨頭,kut thau
高速,ko sok
高樓,ko lau
鬥爭,tau tsing
假期,ka ki
偏見,phian kian
國發會,kok huat hue
國稅局,kok sue kiok
常識,siong sik
排卵,pai luan
教職,kau tsit
清除,tshing tu
現身,hian sin
產房,san pang
祥和,siong ho
移轉,i tsuan
處境,tshu king
造就,tso tsiu
景點,king tiam
款式,khuan sik
發包,huat pau
虛擬,hi gi
評比,phing pi
進展,tsin tian
開播,khai poo
間接,kan tsiap
傳球,thuan kiu
感性,kam sing
損益,sun ik
毀滅,hui biat
禁區,kim khu
跳脫,thiau thuat
農曆,long lik
違法,ui huat
隔離,keh li
摘要,tiah iau
構造,koo tso
歌迷,kua be
歌舞,kua bu
歌壇,kua tuann
種族,tsing tsok
精心,tsing sim
精確,tsing khak
維生素,ui sing soo
聚集,tsu tsip
與會,u hue
舞池,bu ti
領隊,ling tui
劇本,kiok pun
廣電,kong tian
廠牌,tshiunn pai
暴君,po kun
複賽,hok sai
談起,tam khi
鄭重,ting tiong
魄力,phik lik
整修,tsing siu
選用,suan iong
選項,suan hang
頭盔,thau khue
餐點,tshan tiam
擬定,gi ting
檢視,kiam si
營建,ing kian
聲援,siann uan
聯軍,lian kun
邀集,iau tsip
點選,tiam suan
翻唱,huan tshiunn
釋憲,sik hian
黨部,tong poo
人命,lang mia
入口,jip khau
入圍,jip ui
上櫃,tsiunn kui
口服,khau hok
夕陽,sik iong
女神,lu sin
山水,san sui
工商,kang siong
才女,tsai lu
公署,kong su
分工,hun kang
分店,hun tiam
升旗,sing ki
主教,tsu kau
以外,i gua
出動,tshut tong
出擊,tshut kik
古堡,koo po
任期,jim ki
全民,tsuan bin
共鳴,kiong bing
列舉,liat ki
印證,in tsing
各地,kok te
合計,hap ke
回郵,hue iu
回想,hue siong
在場,tsai tiunn
守護,siu hoo
死海,si hai
羊肉,iunn bah
自律,tsu lut
自排,tsu pai
兵役,ping ik
冷淡,ling tam
判定,phuann ting
改用,kai iong
改選,kai suan
更生,king sing
事故,su koo
享用,hiang iong
依附,i hu
兩棲,liong tshe
受託人,siu thok jin
受訓,siu hun
坦然,than jian
奔波,phun pho
定居,ting ki
延後,ian au
往事,ong su
怪物,kuai but
性感,sing kam
承攬,sing lam
枕頭,tsim thau
歧視,ki si
法治,huat ti
油煙,iu ian
直徑,tit king
直覺,tit kak
社長,sia tiunn
空姐,khong tsia
空虛,khang hi
初選,tshoo suan
保安,po an
保健,po kian
封閉,hong pi
度過,too kue
建材,kian tsai
拯救,tsin kiu
春暉,tshun hui
架設,ka siat
相比,sio pi
背影,pue iann
重建,tiong kian
重疊,ting thah
飛舞,hui bu
原油,guan iu
時光,si kong
時裝,si tsong
柴油,tsha iu
真相,tsin siong
祕訣,pi kuat
紡織,phang tsit
能源,ling guan
航運,hang un
逃生,to sing
追溯,tui soo
骨骼,kut keh
做出,tso tshut
參選,tsham suan
國安局,kok an kiok
堆積,tui tsik
執政,tsip tsing
宿舍,sok sia
彩妝,tshai tsong
控訴,khong soo
接替,tsiap the
採集,tshai tsip
啟事,khe su
清運,tshing un
深色,tshim sik
理所當然,li soo tong jian
盛會,sing hue
細部,se poo
莫名其妙,bok bing ki miau
訪客,hong kheh
貨物,hue but
透支,thau tsi
野外,ia gua
報稅,po sue
媒介,mui kai
復仇,hok siu
期刊,ki khan
游牧,iu bok
無效,bo hau
無聊,bo liau
發電,huat tian
稅收,sue siu
菁英,tsing ing
華僑,hua kiau
街舞,ke bu
貴族,kui tsok
開辦,khai pan
飲用,im iong
傳出,thuan tshut
匯入,hue jip
匯出,hue tshut
感慨,kam khai
敬意,king i
會談,hue tam
源頭,guan thau
準則,tsun tsik
準確,tsun khak
經文,king bun
義診,gi tsin
腦部,nau poo
詩人,si jin
路標,loo piau
跳遠,thiau hng
農地,long te
雷射,lui sia
寧靜,ling tsing
對付,tui hu
演說,ian suat
演練,ian lian
甄試,tsin tshi
網址,bang tsi
製片,tse phinn
語音,gi im
語調,gi tiau
劇烈,kik liat
劇團,kiok thuan
寬恕,khuan su
徵召,ting tiau
徵詢,ting sun
徵選,ting suan
模仿,boo hong
獎學金,tsiong hak kim
編織,pian tsit
調製,tiau tse
輪流,lun liu
導覽,to lam
機房,ki pang
應對,ing tui
營利,ing li
聲稱,sing tshing
襄理,siong li
瀉藥,sia ioh
醫護,i hoo
鏡片,kiann phinn
關聯,kuan lian
議程,gi ting
護盤,hoo puann
鐵路,thih loo
人質,jin tsit
下鄉,ha hiong
凡事,huan su
子民,tsu bin
小學生,sio hak sing
小鎮,sio tin
山地,suann te
才華,tsai hua
不明,put bing
中式,tiong sik
中校,tiong hau
元素,guan soo
內銷,lai siau
公安,kong an
公信力,kong sin lik
公會,kong hue
切除,tshiat tu
天生,thian sing
天真,thian tsin
心愛,sim ai
支應,tsi ing
日出,jit tshut
日程,jit ting
比照,pi tsiau
比對,pi tui
出團,tshut thuan
包袱,pau hok
北區,pak khu
司令,su ling
市政,tshi tsing
平和,ping ho
民歌,bin kua
田野,tian ia
白宮,ik kiong
任命,jim bing
光源,kng guan
先天,sian thian
全身,tsuan sin
全國,tsuan kok
共通,kiong thong
多樣,to iunn
安置,an ti
收支,siu tsi
收看,siu khuann
次長,tshu tiunn
老鳥,lau tsiau
自責,tsu tsik
自稱,tsu tshing
血緣,hiat ian
私密,su bit
良性,liong sing
車號,tshia ho
巡邏,sun lo
防水,hong tsui
事先,su sian
佳作,ka tsok
函數,ham soo
刻板,khik pan
奇美,ki bi
底盤,te puann
拉丁,la ting
旺盛,ong sing
武裝,bu tsong
法文,huat bun
油桐花,iu tang hue
物資,but tsu
物體,but the
直升機,tit sing ki
社交,sia kau
糾正,kiu tsing
附加,hu ka
信件,sin kiann
信息,sin sit
信眾,sin tsiong
勇者,iong tsia
客機,kheh ki
指南,tsi lam
指派,tsi phai
流感,liu kam
洗淨,se tsing
研習,gian sip
約談,iok tam
美女,bi lu
美方,bi hong
英商,ing siong
要素,iau soo
訂定,ting ting
軍火,kun hue
軍官,kun kuann
食材,sit tsai
食療,sit liau
個案,ko an
原文,guan bun
家鄉,ka hiong
席次,sik tshu
振興,tsin hing
效忠,hau tiong
旁聽,pong thiann
泰山,thai san
海拔,hai puat
特有,tik iu
純真,sun tsin
起源,khi guan
逃脫,to thuat
骨質,kut tsit
高齡,ko ling
務實,bu sit
參展,tsham tian
商家,siong ka
商圈,siong khuan
國內外,kok lai gua
國府,kok hu
培訓,pue hun
寄望,kia bang
專科,tsuan kho
常用,siong iong
掃描,sau biau
推舉,thui ki
理工,li kang
理化,li hua
現狀,hian tsong
盛大,sing tai
票券,phio kng
處女,tshu lu
被迫,pi pik
訪查,hong tsa
這時,tsit si
連長,lian tiunn
速率,sok lut
部編本,oo pian pun
陸委會,liok ui hue
陷阱,ham tsenn
備註,pi tsu
報表,po pio
插畫,tshah ue
散戶,suann hoo
景物,king but
欺騙,khi phian
殘留,tsan liu
渡假,too ka
減免,kiam bian
無能,bu ling
發放,huat hong
短線,te suann
稅額,sue giah
著作,tu tsok
視線,si suann
超音波,tshiau im pho
開動,khai tong
傳真,thuan tsin
傷亡,siong bong
愛人,ai jin
搶案,tshiunn an
敬佩,king pue
照射,tsio sia
當今,tong kim
碑文,pi bun
路況,loo hong
電纜,tian lam
預先,i sian
預報,i po
圖片,too phinn
圖表,too pio
夢境,bang king
弊案,pe an
構圖,koo too
歌聲,kua siann
演技,ian ki
福音,hok im
福壽螺,hok siu le
精美,tsing bi
語氣,gi khi
誘因,iu in
賓館,pin kuan
銀幕,gin boo
鼻炎,phinn iam
寫真,sia tsin
廟會,bio hue
影音,iann im
影帶,iann tua
標記,piau ki
熱愛,jiat ai
締造,te tso
編譯館,pian ik kuan
膚質,hu tsit
調派,tiau phai
輝煌,hui hong
養樂多,iong lok to
學名,hak mia
學年,hak ni
學界,hak kai
學科,hak kho
戰神,tsian sin
戰略,tsian liok
機長,ki tiunn
機動,ki tong
機緣,ki ian
濃度,long too
激情,kik tsing
獨自,tok tsu
縣民,kuan bin
踴躍,iong iok
辨認,pian jin
鋼釘,kng ting
餐飲,tshan im
矯正,kiau tsing
謝意,sia i
斷電,tng tian
檯面,tai bin
轉型,tsuan hing
雞排,ke pai
簽到,tshiam to
簽署,tshiam su
繳納,kiau lap
艦隊,lam tui
轟動,hong tong
變形,pian hing
顯露,hian loo
體溫,the un
人心,jin sim
人文,jin bun
人次,jin tshu
人為,jin ui
人壽,jin siu
土星,thoo tshenn
土風舞,thoo hong bu
大雨,tua hoo
大戰,tai tsian
小型,sio hing
山坡地,suann pho te
不比,put pi
不肖,put siau
中型,tiong hing
中研院,tiong gian inn
中樞,tiong tshu
內幕,lue boo
公益,kong ik
升遷,sing tshian
反駁,huan pok
天使,thinn sai
少將,siau tsiong
心思,sim su
戶名,hoo mia
支配,tsi phue
文山,bun san
文具,bun ku
文案,bun an
日月潭,jit guat tham
月台,guat tai
木雕,bok tiau
毛利,moo li
火力,hue lik
主宰,tsu tsainn
付費,hu hui
仙境,sian king
充實,tshiong sit
包容,pau iong
北方,pak hong
半數,puann soo
古都,koo too
史學,su hak
台斤,tai kin
外力,gua lik
失調,sit tiau
弘法,hong huat
本能,pun ling
生效,sing hau
用語,iong gi
田地,tshan te
交談,kau tam
先民,sian bin
全新,tsuan sin
冰淇淋,ping ki lim
同伴,tong phuann
合輯,hap tsip
回流,hue liu
回響,hue hiong
地下室,te ha sik
地表,te piau
收回,siu hue
死者,si tsia
考生,kho sing
肉質,bah tsit
自保,tsu po
自傳,tsu tuan
自認,tsu jin
行車,hing tshia
兵力,ping lik
冷漠,ling bok
刪除,san tu
卵巢,nng tsau
呈報,thing po
志工,tsi kang
投保,tau po
投影,tau iann
投籃,tau na
改制,kai tse
男裝,lam tsong
走訪,tsau hong
身影,sin iann
車門,tshia mng
邪惡,sia ok
防範,hong huan
受害者,siu hai tsia
周轉,tsiu tsuan
夜色,ia sik
姓名,senn mia
定速,ting sok
定額,ting giah
延誤,ian goo
征服,tsing hok
性情,sing tsing
房市,pang tshi
承接,sing tsiap
抽脂,thiu tsi
抽獎,thiu tsiong
放款,hong khuan
放開,pang khui
河流,ho liu
波浪,pho long
法辦,huat pan
法警,huat king
沿途,ian too
爭執,tsing tsip
版圖,pan too
直銷,tit siau
直選,tit suan
股長,koo tiunn
表決,piau kuat
金主,kim tsu
附帶,hu tai
信箱,sin siunn
侵略,tshim liok
保全,po tsuan
保密,po bit
保費,po hui
促成,tshiok sing
俘虜,hu loo
品種,phin tsing
型式,hing sik
城堡,siann po
姿態,tsu thai
建物,kian but
施展,si tian
查出,tsha tshut
流向,lau hiong
流動,liu tong
派駐,phai tsu
英吋,ing tshun
英鎊,ing pong
軍力,kun lik
限量,han liong
音符,im hu
音質,im tsit
風向,hong hiong
風行,hong hing
風采,hong tshai
食譜,sit phoo
原版,guan pan
家扶中心,ka hu tiong sim
宮殿,kiong tian
弱點,jiok tiam
益處,ik tshu
粉紅,hun ang
紗布,se poo
草莓,tshau m
訊號,sin ho
退化,the hua
酒會,tsiu hue
配方,phue hng
配件,phue kiann
配額,phue giah
閃光燈,siam kong ting
馬車,be tshia
鬼月,kui gueh
偽造,gui tso
假象,ke siong
偵探,tsing tham
偏遠,phian uan
參見,tsham kian
參照,tsham tsiau
參賽,tsham sai
唱歌,tshiunn kua
問政,bun tsing
國庫,kok khoo
執意,tsip i
密室,bit sik
專訪,tsuan hong
強迫,kiong pik
情愛,tsing ai
接掌,tsiap tsiong
排版,pai pan
清代,tshing tai
清算,tshing suan
猛禽,bing khim
第三者,te sann tsia
統合,thong hap
終結,tsiong kiat
通告,thong ko
通車,thong tshia
野牛,ia gu
備用,pi iong
單調,tan tiau
痛恨,thong hun
登機,ting ki
善心,sian sim
善意,sian i
肅貪,siok tham
菜鳥,tshai tsiau
評選,phing suan
評鑑,phing kam
貼紙,tah tsua
費率,hui lut
超市,tshiau tshi
週期,tsiu ki
進軍,tsin kun
匯款,hue khuan
微波,bi pho
搶奪,tshiunn tuat
新陳代謝,sin tin tai sia
楷模,khai boo
源自,guan tsu
罪犯,tsue huan
罪嫌,tsue hiam
義賣,gi be
群島,kun to
聘約,phing iok
補足,poo tsiok
補救,poo kiu
試射,tshi sia
誠心,sing sim
運算,un suan
遊行,iu hing
遊說,iu sue
遊輪,iu lun
過量,kue liong
過關,kue kuan
預言,i gian
僑胞,kiau pau
實務,sit bu
實體,sit the
對白,tui peh
慣例,kuan le
漁民,hi bin
管教,kuan ka
精油,tsing iu
綜藝,tsong ge
網頁,bang iah
輔選,hu suan
領標,nia pio
寫實,sia sit
履行,li hing
影本,iann pun
暫停,tsiam thing
標誌,piau tsi
標題,piau te
獎助金,tsiong tsoo kim
編制,pian tse
編號,pian ho
複利,hok li
質地,tsit te
戰士,tsian su
戰國,tsian kok
獨一無二,tok it bu ji
輻射,hok sia
輸送,su sang
辦事處,pan su tshu
選區,suan khu
選情,suan tsing
優越,iu uat
優選,iu suan
檢調,kiam tiau
溼疹,sip tsin
環島,khuan to
環球,khuan kiu
斷交,tuan kau
歸屬,kui siok
轉向,tsuan hiong
醫界,i kai
鎮長,tin tiunn
類股,lui koo
嚴密,giam bit
寶藏,po tsong
贖回,siok hue
變換,pian uann
觀望,kuan bong
力學,lik hak
上車,tsiunn tshia
上校,siong hau
口譯,khau ik
大火,tua hue
大本營,tua pun iann
大同,tai tong
大局,tai kiok
大事,tai su
大理石,tai li tsioh
女將,lu tsiong
女裝,lu tsong
小兒,siau ji
工地,kang te
不平,put ping
中油,tiong iu
公正,kong tsing
公式,kong sik
分行,hun hang
分機,hun ki
天命,thian bing
引言,in gian
心聲,sim siann
文革,bun kik
文筆,bun pit
日間,jit kan
月刊,gueh khan
月光,gueh kng
水手,tsui siu
水源,tsui guan
王妃,ong hui
王國,ong kok
主觀,tsu kuan
代言人,tai gian jin
代碼,tai be
代謝,tai sia
出獄,tshut gak
加班,ka pan
包商,pau siong
外圍,gua ui
失效,sit hau
平民,ping bin
平行,ping hing
平坦,penn thann
幼稚,iu ti
生平,sing ping
生根,senn kin
交織,kau tsit
兇手,hiong siu
先鋒,sian hong
列出,liat tshut
刑法,hing huat
印花,in hue
各行各業,kok hang kok giap
地帶,te tai
地下鐵,te ha thih
如意,ju i
年終,ni tsiong
年會,ni hue
年資,ni tsu
有史以來,iu su i lai
百科,pah kho
自主,tsu tsu
色情,sik tsing
行蹤,hing tsong
西岸,se huann
西進,se tsin
西歐,se au
伴唱,phuann tshiunn
佛經,hut king
伸出,tshun tshut
冷凍,ling tong
助攻,tsoo kong
助陣,tsoo tin
助理,tsoo li
否定,honn ting
壯觀,tsong kuan
戒嚴,kai giam
投射,tau sia
改正,kai tsing
更年期,king lian ki
步入,poo jip
求婚,kiu hun
私校,su hau
車位,tshia ui
車迷,tshia be
車價,tshia ke
防衛,hong ue
防禦,hong gu
依法,i huat
典範,tian huan
協定,hiap ting
取景,tshu king
呼聲,hoo siann
命理,mia li
夜總會,ia tsong hue
定律,ting lut
忠誠,tiong sing
所有權,soo iu khuan
拍戲,phah hi
昇華,sing hua
東北,tang pak
東亞,tang a
林業,lim giap
武林,bu lim
武俠,bu kiap
法庭,huat ting
法務,huat bu
肺部,hi poo
芭蕉,pa tsio
花車,hue tshia
表揚,piau iong
表層,piau tsan
附屬,hu siok
非凡,hui huan
信念,sin liam
南北,lam pak
度數,too soo
建言,kian gian
待命,thai bing
後衛,hoo ue
急救,kip kiu
施壓,si ap
染色體,ni sik the
查扣,tsha khau
查封,tsha hong
流竄,liu tshuan
流露,liu loo
省略,sing liok
相逢,siong hong
紀元,ki guan
美編,bi pian
美學,bi hak
虐待,gik thai
要件,iau kiann
郊區,kau khu
面談,bian tam
革新,kik sin
風扇,hong sinn
修復,siu hok
修護,siu hoo
凍結,tong kiat
哲理,tiat li
宮廷,kiong ting
容積,iong tsik
師長,su tiunn
弱者,jiok tsia
弱勢,jiok se
旅途,li too
書面,su bin
核子,hik tsu
氣溫,khi un
消基會,siau ki hue
海基會,hai ki hue
病菌,penn khun
炮彈,phau tuann
祖先,tsoo sian
祖國,tsoo kok
租車,tsoo tshia
紛擾,hun jiau
缺陷,khuat ham
起點,khi tiam
送醫,sang i
逆境,gik king
迷惑,be hik
追隨,tui sui
配股,phue koo
陣地,tin te
骨折,kut tsih
高職,ko tsit
高鐵,ko thih
假定,ka ting
假想,ka siong
健身,kian sin
偏差,phian tsha
剪裁,tsian tshai
區段,khu tuann
商用,siong iong
國宅,kok theh
國科會,kok kho hue
專攻,tsuan kong
屠殺,too sat
情景,tsing king
情網,tsing bang
情懷,tsing huai
控管,khong kuan
救治,kiu ti
教改,kau kai
教法,ka huat
教科書,kau kho su
教條,kau tiau
教會,kau hue
欲望,iok bong
深遠,tshim uan
票價,phio ke
組長,tsoo tiunn
船隻,tsun tsiah
連繫,lian he
造形,tso hing
傑作,kiat tsok
單打,tan tann
報警,po king
就任,tsiu jim
插座,tshah tso
散步,san poo
無味,bo bi
無聲,bo siann
發車,huat tshia
稅率,sue lut
筆錄,pit lok
紫外線,tsi gua suann
絲絨,si jiong
善惡,sian ok
菜色,tshai sik
裁判,tshai phuann
評語,phing gi
診療,tsin liau
週刊,tsiu khan
開戶,khui hoo
開創,khai tshong
隆重,liong tiong
傳言,thuan gian
傳來,thuan lai
傳承,thuan sing
微妙,bi miau
意料,i liau
想起,siunn khi
愛心,ai sim
新知,sin ti
署長,su tiunn
聘任,phing jim
補正,poo tsing
解體,kai the
詩詞,si su
路口,loo khau
遊學,iu hak
違約,ui iok
過份,kue hun
電波,tian pho
電壓,tian ap
圖樣,too iunn
境內,king lai
對外,tui gua
幕僚,boo liau
撤離,thiat li
歌詞,kua su
漁村,hi tshun
精進,tsing tsin
精誠,tsing sing
網域,bang hik
語文,gi bun
輕輕鬆鬆,khin khin sang sang
遠東,uan tong
遠景,uan king
閣員,koh uan
駁回,pok hue
寬頻,khuan pin
寫照,sia tsiau
廢水,hui tsui
廢除,hui tu
慾望,iok bong
暴民,po bin
樂壇,gak tuann
潛能,tsiam ling
獎品,tsiong phin
確立,khak lip
編排,pian pai
編譯,pian ik
複合,hok hap
複習,hok sip
課長,kho tiunn
賣掉,be tiau
銷量,siau liong
養生,iong sing
壁紙,piah tsua
戰火,tsian hue
戰備,tsian pi
操守,tshau siu
機制,ki tse
歷代,lik tai
燈光,ting kng
獨家,tok ka
親和力,tshin ho lik
遺蹟,ui tsik
頭皮,thau phue
應當,ing tong
檔名,tong mia
薪傳,sin thuan
講述,kang sut
講授,kang siu
賽程,sai ting
韓戰,han tsian
職責,tsit tsik
轉入,tsuan jip
轉任,tsuan jim
轉進,tsuan tsin
藥效,ioh hau
證件,tsing kiann
證照,tsing tsiau
關連,kuan lian
騙人,phian lang
寶座,po tso
警覺,king kak
黨員,tong uan
黨務,tong bu
鐵道,thih to
變遷,pian tshian
驗證,giam tsing
觀感,kuan kam
一模一樣,it boo it iunn
了不起,liau put khi
人種,jin tsiong
入獄,jip gak
下場,ha tiunn
上路,tsiunn loo
大手筆,tua tshiu pit
大獎,tua tsiong
女方,lu hong
工讀生,kang thok sing
不准,put tsun
不盡,put tsin
中性,tiong sing
中區,tiong khu
中期,tiong ki
中鋒,tiong hong
內陸,lai liok
公墓,kong bong
公認,kong jin
公德心,kong tik sim
分居,hun ki
升學,sing hak
友邦,iu pang
友情,iu tsing
反制,huan tse
天份,thian hun
天后,thian hio
天性,thian sing
天鵝,thian go
太極,thai kik
少校,siau hau
心動,sim tong
手動,tshiu tong
手稿,tshiu ko
日文,jit bun
日式,jit sik
水池,tsui ti
火藥,hue ioh
牛舌餅,gu tsih piann
王朝,ong tiau
主唱,tsu tshiunn
主講,tsu kang
以下,i ha
包皮,pau phue
北美,ak bi
占地,tsiam te
古怪,koo kuai
召喚,tiau huan
叮嚀,ting ling
外文,gua bun
外向,gua hiong
外地,gua te
左派,tso phai
佈局,poo kiok
幼教,iu kau
必修,pit siu
打動,tann tong
未婚,bi hun
正視,tsing si
民生,bin sing
犯錯,huan tsho
瓜果,kua ko
瓦解,ua kai
生育,sing iok
用具,iong ku
白米,peh bi
白雲,peh hun
光滑,kng kut
全職,tsuan tsit
共存,kiong tsun
共有,kiong iu
冰河,ping ho
同僚,tong liau
各界,kok kai
名勝,bing sing
名醫,bing i
回國,hue kok
回程,hue ting
地利,te li
地段,te tuann
地質,te tsit
多元,to guan
好人,ho lang
好聽,ho thiann
字體,ji the
存檔,tsun tong
守則,siu tsik
年份,ni hun
收割,siu kuah
收發,siu huat
有形,iu hing
有緣,u ian
江山,kang san
江南,kang lam
百分比,pah hun pi
百般,pah puann
自卑,tsu pi
血統,hiat thong
西餐,se tshan
佛法,hut huat
冷水,ling tsui
冷門,ling mng
冷清,ling tshing
利尿,li jio
助力,tsoo lik
助手,tsoo tshiu
助選,tsoo suan
告白,ko peh
告別,ko piat
吟唱,gim tshiunn
妥協,tho hiap
攻打,kong tann
步調,poo tiau
沙畫,sua ue
汪洋,ong iong
沖銷,tshiong siau
男方,lam hong
育幼院,iok iu inn
言行,gian hing
走廊,tsau long
車頂,tshia ting
車窗,tshia thang
車道,tshia to
車燈,tshia ting
里民,li bin
來函,lai ham
典藏,tian tsong
刺殺,tshi sat
制式,tse sik
受困,siu khun
受理,siu li
呼應,hoo ing
奉勸,hong khng
奇異,ki i
孤立,koo lip
官兵,kuann ping
延期,ian ki
怪異,kuai i
招考,tsio kho
拍片,phah phinn
拖延,thua ian
放學,pang oh
東歐,tang au
果汁,ko tsiap
林木,lim bok
河床,ho tshng
波長,pho tng
沿岸,ian huann
炎熱,iam juah
爭奪,tsing tuat
版面,pan bin
版權,pan khuan
直線,tit suann
社員,sia uan
社論,sia lun
空大,khong tai
空白,khang peh
空服,khong hok
空運,khong un
股份,koo hun
初試,tshoo tshi
初稿,tshoo ko
表格,pio keh
近代,kin tai
金幣,kim pe
長城,tng siann
雨鞋,hoo e
青山,tshing san
南區,lam khu
威嚇,ui hik
宣判,suan phuann
宣揚,suan iong
封建,hong kian
帝國,te kok
思維,su ui
拜票,pai phio
按時,an si
指引,tsi in
指控,tsi khong
政戰,tsing tsian
柔美,jiu bi
流傳,liu thuan
流會,liu hue
流線,liu suann
洗髮精,se huat tsing
相符,siong hu
祈福,ki hok
約束,iok sok
美式,bi sik
美規,bi kui
英才,ing tsai
英里,ing li
訂貨,ting hue
軍團,kun thuan
迫害,pik hai
限度,han too
限電,han tian
首相,siu siong
借款,tsioh khuan
個體,ko the
原子,guan tsu
原有,guan iu
原作,guan tsok
原著,guan tu
原廠,guan tshiunn
原點,guan tiam
套房,tho pang
家用,ka iong
家扶,ka hu
家產,ka san
家境,ka king
時速,si sok
書寫,su sia
桌巾,toh kin
烏龍,oo liong
特技,tik ki
特務,tik bu
特產,tik san
特種,tik tsiong
破碎,pho tshui
純益,sun ik
航行,hang hing
航班,hang pan
草案,tsho an
起飛,khi pue
逃難,to lan
追思,tui su
配音,phue im
配套,phue tho
配送,phue sang
院校,inn hau
骨髓,kut tshue
高等,ko ting
剪綵,tsian tshai
動用,tong iong
動脈,tong meh
參訪,tsham hong
唱出,tshiunn tshut
國土,kok thoo
國有,kok iu
國旗,kok ki
國賠,kok pue
專制,tsuan tse
專線,tsuan suann
彩券,tshai kuan
情治,tsing ti
情誼,tsing gi
控告,khong ko
探望,tham bong
接見,tsiap kian
接送,tsiap sang
掃除,sau tu
掛號,kua ho
推算,thui sng
排行,pai hang
排練,pai lian
救命,kiu mia
教具,kau ku
條例,tiau le
淡化,tam hua
清涼,tshing liang
清爽,tshing song
清醒,tshing tshenn
異鄉,i hiong
祭典,tse tian
祭拜,tse pai
脫衣舞,thuat i bu
莫名,bok bing
處長,tshu tiunn
規章,kui tsiong
訪談,hong tam
貨車,hue tshia
貨運,hue un
閉幕,pi boo
陸地,liok te
勞改,lo kai
圍觀,ui kuan
報刊,po khan
報考,po kho
復健,hok kian
惡夢,ok bang
散佈,san poo
港都,kang too
渡過,too kue
減弱,kiam jiok
減稅,kiam sue
無心,bo sim
童話,tong ue
策畫,tshik ue
筆友,pit iu
筆記,pit ki
結晶,kiat tsinn
絕食,tsuat sit
視察,si tshat
評量,phing liong
跑車,phau tshia
週年,tsiu ni
進修,tsin siu
郵資,iu tsu
開展,khai tian
開除,khai tu
開採,khai tshai
開戰,khai tsian
開機,khui ki
亂象,luan siong
傷者,siong tsia
園地,uan te
圓形,inn hing
感念,kam liam
感嘆,kam than
愛國,ai kok
愛惜,ai sioh
愛護,ai hoo
新生,sin sing
會務,hue bu
毽子,kian tsi
滄桑,tshong song
照護,tsiau hoo
禁令,kim ling
罪名,tsue mia
腦海,nau hai
解放,kai hong
試車,tshi tshia
試飛,tshi pue
試題,tshi te
話語,ue gi
資政,tsu tsing
運費,un hui
運鈔車,un tshau tshia
運勢,un se
道場,to tiunn
逼近,pik kin
違建,ui kian
鉛管,ian kong
電訊,tian sin
電極,tian kik
頒發,pan huat
僑生,kiau sing
嘉惠,ka hui
圖示,too si
對岸,tui huann
幕後,boo au
構思,koo su
歌星,kua tshenn
演化,ian hua
滿漢全席,buan han tsuan sik
漫遊,ban iu
漁場,hi tiunn
精良,tsing liong
綠化,lik hua
綿羊,mi iunn
綿延,bian ian
翡翠,hui tshui
舞男,bu lam
製藥,tse ioh
輕型,khin hing
遙遠,iau uan
銅牌,tang pai
銅像,tang siong
審理,sim li
影星,iann tshenn
影展,iann tian
憂傷,iu siong
樂手,gak tshiu
樂迷,gak be
熱切,jiat tshiat
熱戀,jiat luan
獎助,tsiong tsoo
篇幅,phian hok
練球,lian kiu
衛教,ue kau
論述,lun sut
論戰,lun tsian
質料,tsit liau
遷入,tshian jip
鄰長,lin tiunn
養份,iong hun
駕照,ka tsiau
學區,hak khu
導航,to hang
導遊,to iu
憲政,hian tsing
整型,tsing hing
整建,tsing kian
機票,ki phio
濃縮,long sok
激動,kik tong
縣政,kuan tsing
遴選,lin suan
選罷法,suan pa huat
遲到,ti to
遺傳,ui thuan
遺體,ui the
雕塑,tiau sok
雕像,tiau siong
靜電,tsing tian
靜態,tsing thai
餐會,tshan hue
優勝,iu sing
應變,ing pian
擬訂,gi ting
檢疫,kiam ik
檢警,kiam king
溼地,sip te
營隊,iann tui
總隊,tsong tui
繁華,huan hua
聯手,lian tshiu
聯考,lian kho
聯隊,lian tui
聯誼,lian gi
鍛鍊,tuan lian
黏膜,liam mooh
點播,tiam poo
點點滴滴,tiam tiam tih tih
歸納,kui lap
禮遇,le gu
簡介,kan kai
簡體字,kan the ji
醫藥,i ioh
鎮民,tin bin
雜草,tsap tshau
雙層,siang tsan
雞精,ke tsing
騎車,khia tshia
騎馬,khia be
藝壇,ge tuann
藥品,ioh phin
邊界,pian kai
競標,king pio
籌辦,tiu pan
籃板,na pan
議事,gi su
警匪,king hui
黨旗,tong ki
贓物,tsong but
聽力,thiann lik
變革,pian kik
變態,pian thai
驗收,giam siu
體內,the lai
體型,the hing
體積,the tsik
體檢,the kiam
讚揚,tsan iong
人世,jin se
人群,jin kun
入伍,jip ngoo
三軍,sam kun
下令,ha ling
下台,ha tai
下課,ha kho
上岸,tsiunn huann
上將,siong tsiong
上網,tsiunn bang
亡國,bong kok
千辛萬苦,tshian sin ban khoo
口號,khau ho
大王,tai ong
大衣,tua i
大西洋,tai se iunn
大炮,tua phau
大專,tai tsuan
大麻,tua mua
大牌,tua pai
大筆,tua pit
大綱,tai kong
大體,tai the
山羊,suann iunn
山莊,san tsong
山路,suann loo
山歌,san ko
工資,kang tsu
中止,tiong tsi
中選會,tiong suan hue
中藥,tiong ioh
互助,hoo tsoo
互惠,hoo hui
五星級,goo tshenn kip
內戰,lai tsian
公報,kong po
公演,kong ian
公爵,kong tsiok
公職,kong tsit
分化,hun hua
分支,hun tsi
分貝,hun pue
分級,hun kip
分區,hun khu
分割,hun kuah
分隊,hun tui
分擔,hun tam
切開,tshiat khui
切斷,tshiat tng
化石,hua tsioh
升等,sing ting
反感,huan kam
反轉,huan tsuan
天平,thian ping
天災,thian tsai
天際,thian tse
天價,thian ke
太子,thai tsu
幻滅,huan biat
引領,in ling
心跳,sim thiau
心境,sim king
戶政,hoo tsing
戶數,hoo soo
手排,tshiu pai
手語,tshiu gi
手銬,tshiu khau
支流,tsi liu
文人,bun jin
文教,bun kau
方位,hong ui
日夜,jit ia
日語,jit gi
月租費,gueh tsoo hui
水利,tsui li
水域,tsui hik
水費,tsui hui
片商,phinn siong
牛車,gu tshia
牛排,gu pai
王牌,ong pai
主將,tsu tsiong
主菜,tsu tshai
主編,tsu pian
付款,hu khuan
代名詞,tai bing su
代步,tai poo
代勞,tai lo
代銷,tai siau
出刊,tshut khan
出品,tshut phin
出風口,tshut hong khau
出海,tshut hai
加護,ka hoo
功用,kong iong
功臣,kong sin
功利,kong li
包涵,pau ham
北二高,ak ji ko
北美洲,ak bi tsiu
北美館,ak bi kuan
半徑,puann king
司長,su tiunn
台長,tai tiunn
台詞,tai su
外移,gua i
外部,gua poo
外貌,gua mau
失意,sit i
奶茶,ling te
平手,penn tshiu
平直,penn tit
本業,pun giap
本體,pun the
未知,bi ti
正宗,tsiann tsong
母語,bu gi
永久,ing kiu
永續,ing siok
犯規,huan kui
生力軍,sing lik kun
生計,sing ke
申辦,sin pan
白金,peh kim
交付,kau hu
交保,kau po
交會,kau hue
交響樂,kau hiong gak
休館,hiu kuan
份子,hun tsu
光彩,kong tshai
全程,tsuan ting
共犯,kiong huan
再造,tsai tso
刑期,hing ki
危害,gui hai
同樂,tong lok
名號,mia ho
回報,hue po
地名,te mia
地雷,te lui
好用,ho ing
好事,ho su
字幕,ji boo
存戶,tsun hoo
守衛,siu ue
有志,iu tsi
次序,tshu su
死去,si khi
死角,si kak
羽毛,u moo
老兵,lau ping
考場,kho tiunn
考證,kho tsing
耳機,hinn ki
血跡,hueh jiah
西南,se lam
估算,koo sng
免疫力,bian ik lik
即刻,tsik khik
否決,honn kuat
吧台,pa tai
壯大,tsong tai
妙方,miau hng
完備,uan pi
局限,kiok han
床頭,tshng thau
快感,khuai kam
戒備,kai pi
抗藥性,khong ioh sing
折磨,tsiat bua
投案,tau an
更正,king tsing
決標,kuat pio
決賽,kuat sai
秀麗,siu le
系所,he soo
肝病,kuann penn
良知,liong ti
見識,kian sik
見證,kian tsing
身段,sin tuann
車行,tshia hang
車種,tshia tsiong
巡航,sun hang
邦交,pang kau
里長,li tiunn
防治,hong ti
防空,hong khong
防疫,hong ik
防盜,hong to
亞軍,a kun
刻薄,khik pok
制裁,tse tshai
協理,hiap li
卸任,sia jim
受難,siu lan
周刊,tsiu khan
奔走,phun tsau
定論,ting lun
屈服,khut hok
岩石,gam tsioh
底薪,te sin
怪罪,kuai tsue
承包,sing pau
抵制,ti tse
林務局,lim bu kiok
武術,bu sut
法會,huat hue
油漆,iu tshat
沿線,ian suann
盲點,bong tiam
社教,sia kau
空位,khang ui
芹菜,khin tshai
花花公子,hua hua kong tsu
初學者,tshoo hak tsia
表明,piau bing
金字塔,kim ji thah
長年,tng ni
長褲,tng khoo
阻隔,tsoo keh
青天,tshing thian
信義,sin gi
侵害,tshim hai
保固,po koo
前任,tsing jim
前言,tsian gian
前鋒,tsian hong
厚度,kau too
叛亂,puan luan
哀傷,ai siong
威權,ui khuan
室內,sik lai
室溫,sik un
客房,kheh pang
客源,kheh guan
封殺,hong sat
封鎖,hong so
建構,kian koo
急診,kip tsin
怨言,uan gian
政壇,tsing tuann
流汗,lau kuann
流動性,liu tong sing
流轉,liu tsuan
洗牌,se pai
洗禮,se le
界定,kai ting
界線,kai suann
盆栽,phun tsai
研讀,gian thok
紅豆,ang tau
美洲,bi tsiu
美籍,bi tsik
致辭,ti su
苦悶,khoo bun
訂戶,ting hoo
軍用,kun iong
軍備,kun pi
迫切,pik tshiat
重現,tiong hian
重劃區,tiong ueh khu
風塵,hong tin
首席,siu sik
首都,siu too
冥想,bing siong
原味,guan bi
原動力,guan tong lik
原意,guan i
唐詩,tong si
家園,ka hng
座談,tso tam
旁觀,pong kuan
校慶,hau khing
核定,hik ting
氣流,khi liu
消防,siau hong
涉案,siap an
特約,tik iok
病毒,penn tok
病理,penn li
病態,penn thai
病歷,penn lik
真空,tsin khong
破滅,pho biat
破解,pho kai
神話,sin ue
租金,tsoo kim
索引,sik in
純潔,sun kiat
紙盒,tsua ap
缺席,khuat sik
航站,hang tsam
茶包,te pau
衰弱,sue jiok
起先,khi sing
起步,khi poo
送交,sang kau
退票,the phio
退場,the tiunn
追捕,tui poo
追殺,tui sat
追趕,tui kuann
酒家,tsiu ka
配發,phue huat
配對,phue tui
馬桶,be thang
高壓,ko ap
假釋,ka sik
健保,kian po
偵查,tsing tsa
副總,hu tsong
區長,khu tiunn
區間,khu kan
參數,tsham soo
問答,bun tap
國度,kok too
國營,kok ing
基準,ki tsun
執業,tsip giap
專才,tsuan tsai
崩盤,pang puann
強求,kiong kiu
強弱,kiong jiok
情緣,tsing ian
排放,pai hong
排班,pai pan
排演,pai ian
救贖,kiu siok
教養,kau iong
教職員,kau tsit uan
梵文,huan bun
毫米,ho bi
毫克,ho khik
液體,ik the
清洗,tshing se
清掃,tshing sau
淵源,ian guan
深沉,tshim tim
球友,kiu iu
球技,kiu ki
球類,kiu lui
產物,san but
眾生,tsiong sing
被動,pi tong
規費,kui hui
貫穿,kuan tshuan
通勤,thong khin
通盤,thong puann
連日,lian jit
連連,lian lian
造船,tso tsun
野餐,ia tshan
鳥類,tsiau lui
創刊,tshong khan
勝地,sing te
勝算,sing suan
喜宴,hi ian
喪生,song sing
單字,tan ji
報社,po sia
報業,po giap
寒冷,han ling
寒假,han ka
復工,hok kang
惡魔,ok moo
掌管,tsiong kuan
掌聲,tsiong siann
提煉,the lian
智商,ti siong
殖民,sit bin
港區,kang khu
減產,kiam san
滋潤,tsu jun
無非,bu hui
無常,bu siong
無邊,bu pian
畫筆,ue pit
發財,huat tsai
發送,huat sang
發源地,huat guan te
稅源,sue guan
童軍,tong kun
筆法,pit huat
結石,kiat tsioh
華府,hua hu
虛構,hi koo
越戰,uat tsian
超人,tshiau jin
超速,tshiau sok
跑道,phau to
鄉民,hiong bin
開庭,khui ting
開票,khui phio
開標,khui pio
開課,khui kho
陽春,iong tshun
雅房,nga pang
雄心,hiong sim
亂七八糟,luan tshi pa tsau
傳神,thuan sin
傷勢,siong se
募款,boo khuan
奧妙,o miau
意念,i liam
意涵,i ham
意圖,i too
意境,i king
感官,kam kuan
感傷,kam siong
感觸,kam tshiok
新型,sin hing
新舊,sin ku
會商,hue siong
業主,giap tsu
溪水,khe tsui
溪流,khe lau
煙霧,ian bu
照樣,tsiau iunn
當紅,tng ang
禁用,kim iong
聖戰,sing tsian
落幕,loh boo
補強,poo kiong
裝甲,tsong kah
解嚴,kai giam
解讀,kai thok
試用,tshi iong
詩意,si i
資歷,tsu lik
遊民,iu bin
遊覽,iu lam
違憲,ui hian
雷達,lui tat
電聯車,tian lian tshia
預約,i iok
預訂,i ting
預留,i liu
預產期,i san ki
預設,i siat
預警,i king
團長,thuan tiunn
境地,king te
壽險,siu hiam
實例,sit le
對談,tui tam
弊端,pe tuan
截止,tsiat tsi
撤銷,thiat siau
榮譽,ing u
漁會,hi hue
滷味,loo bi
監聽,kam thiann
管線,kong suann
精裝,tsing tsong
舞步,bu poo
舞團,bu thuan
趕往,kuann ong
輕柔,khin jiu
輕傷,khin siong
遙控,iau khong
銀器,gin khi
銅管,tang kong
增資,tsing tsu
審定,sim ting
審議,sim gi
廢棄,hui khi
廢標,hui pio
影集,iann tsip
徵文,ting bun
慶典,khing tian
撥付,puah hu
敵意,tik i
暴亂,po luan
標點,piau tiam
歐式,au sik
歐盟,au bing
熱誠,jiat sing
編舞,pian bu
編劇,pian kiok
線材,suann tsai
罷免,pa bian
請願,tshing guan
課堂,kho tng
課業,kho giap
論點,lun tiam
踏入,tap jip
輪椅,lun i
養成,iong sing
奮戰,hun tsian
學長,hak tiunn
學說,hak suat
戰況,tsian hong
戰區,tsian khu
操盤,tshau puann
整數,tsing soo
樹葉,tshiu hioh
機電,ki tian
歷來,lik lai
歷練,lik lian
燈罩,ting ta
積分,tsik hun
積水,tsik tsui
辨別,pian piat
辦事,pan su
選定,suan ting
錯失,tsho sit
錯覺,tsho kak
館長,kuan tiunn
壓制,ap tse
溼度,sip too
療法,liau huat
縮影,sok iann
總督,tsong tok
總價,tsong ke
總體,tsong the
聲浪,siann long
聯邦,lian pang
聯招會,lian tsiau hue
聯席會,lian sik hue
講解,kang kai
避難,pi lan
鮮花,tshinn hue
殯儀館,pin gi kuan
禮盒,le ap
簡便,kan pian
簡章,kan tsiong
豐年祭,hong ni tse
轉送,tsuan sang
轉運站,tsuan un tsam
雙打,siang tann
雙向,siang hiong
雙門,siang mng
證交所,tsing kau soo
關愛,kuan ai
難題,lan te
警力,king lik
警官,king kuann
警長,king tiunn
警衛,king ue
黨職,tong tsit
轟炸,hong tsa
霹靂,phik lik
顧慮,koo li
權勢,khuan se
聽友,thiann iu
聽見,thiann kinn
聽話,thiann ue
戀情,luan tsing
罐裝,kuan tsng
靈骨塔,ling kut thah
靈敏,ling bin
鷹架,ing ke
一大堆,tsit tua tui
一心一意,it sim it i
一夜情,tsit ia tsing
一體,it the
了結,liau kiat
二手貨,ji tshiu hue
二氧化碳,ji iong hua thuann
人事局,jin su kiok
人和,jin ho
人道,jin to
入會,jip hue
入境,jip king
三國,sam kok
三溫暖,sam un luan
下垂,ha sui
千古,tshian koo
口才,khau tsai
士官,su kuann
大戶,tua hoo
大略,tai liok
大寫,tua sia
大賣場,tua be tiunn
女王,lu ong
小便,siau pian
小島,sio to
山坡,suann pho
山脈,suann meh
工研院,kang gian inn
工商界,kang siong kai
工期,kang ki
才藝,tsai ge
中西,tiong se
中南美,tiong lam bi
中南海,tiong lam hai
中美,tiong bi
中原,tiong guan
互信,hoo sin
互補,hoo poo
五官,ngoo kuan
元老,guan lo
內分泌,lai hun pi
內勤,lai khin
內褲,lai khoo
六輕,lak khin
公子,kong tsu
公立,kong lip
公有,kong iu
公私,kong su
公約,kong iok
公厘,kong li
公然,kong jian
公轉,kong tsuan
分歧,hun ki
分校,hun hau
分組,hun tsoo
化工,hua kang
反攻,huan kong
反問,huan mng
天王,thian ong
天涯,thian gai
天賦,thian hu
引入,in jip
心目中,sim bok tiong
心胸,sim hing
手心,tshiu sim
手套,tshiu tho
手錶,tshiu pio
文法,bun huat
文壇,bun tuann
日商,jit siong
比數,pi soo
毛筆,moo pit
水床,tsui tshng
水鳥,tsui tsiau
水量,tsui liong
水溫,tsui un
水壓,tsui ap
火光,hue kng
火警,hue king
片廠,phinn tshiunn
牛油,gu iu
世上,se siong
世家,se ka
主食,tsu sit
主播,tsu poo
充電,tshiong tian
出庭,tshut ting
出境,tshut king
刊載,khan tsai
加分,ka hun
功率,kong lut
北半球,ak puann kiu
北歐,ak au
占有率,tsiam iu lut
占領,tsiam nia
可貴,kho kui
古今,koo kim
古物,koo but
史料,su liau
臺胞,tai pau
臺鐵,tai thih
句點,ku tiam
四輪,si lian
囚犯,siu huan
外包,gua pau
外海,gua hai
外野,gua ia
外傷,gua siong
外籍,gua tsik
失真,sit tsin
失落,sit loh
奴隸,loo le
孕育,in iok
平反,ping huan
本文,pun bun
本金,pun kim
本票,pun phio
本壘,pun lui
民怨,bin uan
犯案,huan an
玉山,giok san
生化,sing hua
用法,iong huat
交貨,kau hue
交戰,kau tsian
任內,jim lai
光臨,kong lim
兇惡,hiong ok
全文,tsuan bun
全能,tsuan ling
共和,kiong ho
冰涼,ping liang
列席,liat sik
同性,tong sing
各國,kok kok
名次,mia tshu
名條,mia tiau
名譽,bing u
合資,hap tsu
因緣,in ian
回教,hue kau
地層,te tsan
地標,te piau
好感,ho kam
如來,ju lai
字型,ji hing
尖刀,tsiam to
年金,ni kim
年費,ni hui
年鑑,ni kam
成因,sing in
收件,siu kiann
收押,siu ah
死傷,si siong
汗水,kuann tsui
百年,pah ni
肉類,bah lui
自用,tsu iong
自助,tsu tsoo
自衛,tsu ue
血癌,hueh gam
行文,hing bun
行事曆,hing su lik
行員,hang uan
西區,se khu
串聯,tshuan lian
佛學,hut hak
伸長,tshun tng
免不了,bian put liau
免除,bian tu
判刑,phuann hing
利害,li hai
劫機,kiap ki
吳郭魚,ngoo kueh hi
告辭,ko si
含意,ham i
壯麗,tsong le
宏觀,hong kuan
序幕,su boo
床鋪,tshng phoo
忍者,jim tsia
戒心,kai sim
抗衡,khong hing
投球,tau kiu
改寫,kai sia
攻讀,kong thok
村長,tshun tiunn
求職,kiu tsit
決戰,kuat tsian
私底下,su te ha
走漏,tsau lau
車展,tshia tian
防火,hong hue
防毒,hong tok
防護,hong hoo
兩難,liong lan
受益,siu ik
受騙,siu phian
味覺,bi kak
周詳,tsiu siong
夜間,ia kan
奉獻,hong hian
奈何,nai ho
委屈,ui khut
季刊,kui khan
定點,ting tiam
岸邊,huann pinn
底線,te suann
延燒,ian sio
怪怪,kuai kuai
所致,soo ti
抽換,thiu uann
抽驗,thiu giam
拖吊車,thua tiau tshia
放任,hong jim
放空,pang khang
放射,hong sia
明朗,bing long
明智,bing ti
東岸,tang huann
武功,bu kong
武將,bu tsiong
法定,huat ting
法網,huat bang
法寶,huat po
油性,iu sing
油門,iu mng
油價,iu ke
油罐車,iu kuan tshia
直系,tit he
直播,tit poo
知音,ti im
社教館,sia kau kuan
空前,khong tsian
空隙,khang khiah
花店,hue tiam
花茶,hue te
花園,hue hng
表白,piau pik
表態,piau thai
迎戰,ging tsian
金黃,kim ng
長桌,tng toh
長裙,tng kun
長線,tng suann
附錄,hu lok
青草,tshenn tshau
信物,sin but
保戶,po hoo
保送,po sang
保單,po tuann
保額,po giah
俗諺,siok gan
前程,tsian ting
前線,tsian suann
南亞,lam a
南海,lam hai
品管,phin kuan
宣誓,suan se
宣讀,suan thok
室外,sik gua
客串,kheh tshuan
帝王,te ong
建照,kian tsiau
後台,au tai
後勤,au khin
按下,an ha
指認,tsi jin
政界,tsing kai
政務,tsing bu
故宮,koo kiong
柔情,jiu tsing
架勢,ke se
查明,tsha bing
查證,tsha tsing
毒害,tok hai
毒素,tok soo
流動率,liu tong lut
流域,liu hik
流速,liu sok
流量,liu liong
流標,liu pio
活性,uah sing
為止,ui tsi
皇室,hong sik
相配,siong phue
相通,siong thong
相連,sio lian
相傳,siong thuan
相隔,siong keh
相貌,siong mau
相識,siong sik
突發,tut huat
突變,tut pian
紅十字會,ang sip ji hue
紅外線,ang gua suann
紅牌,ang pai
紅塵,hong tin
紀律,ki lut
約定,iok ting
美工,bi kang
美色,bi sik
美夢,bi bang
美滿,bi buan
耶誕,ia tan
胃藥,ui ioh
致謝,ti sia
苦難,khoo lan
英尺,ing tshioh
訂製,ting tse
軍階,kun kai
重生,tiong sing
重來,ting lai
重型,tang hing
限定,han tiann
限期,han ki
面目,bin bok
風力,hong lik
風風雨雨,hong hong u u
風華,hong hua
風雲,hong hun
風範,hong huan
倍數,pue soo
倚重,i tiong
倒會,to hue
個展,ko tian
修法,siu huat
修剪,siu tsian
修習,siu sip
修練,siu lian
修辭,siu su
剝削,pak siah
原木,guan bok
原狀,guan tsong
原型,guan hing
原訂,guan ting
原創,guan tshong
原裝,guan tsong
埋伏,bai hok
埋怨,bai uan
家務,ka bu
家禽,ka khim
宴請,ian tshiann
宵禁,siau kim
射門,sia mng
射程,sia ting
島嶼,to su
恐龍,khiong liong
恩怨,un uan
捐助,kuan tsoo
效法,hau huat
旁觀者,pong kuan tsia
時日,si jit
書刊,su khan
書展,su tian
校正,kau tsing
根基,kin ki
根源,kin guan
桌面,toh bin
氣功,khi kong
氣色,khi sik
氣派,khi phai
氣體,khi the
氧化,iong hua
海水,hai tsui
海馬,hai be
海運,hai un
海灣,hai uan
浮雕,phu tiau
特使,tik sai
特例,tik le
特首,tik siu
病史,penn su
破除,pho tu
祖產,tsoo san
神態,sin thai
租約,tsoo iok
祕笈,pi kip
笑聲,tshio siann
紋理,bun li
紋路,bun loo
素養,soo iong
紛亂,hun luan
紛雜,hun tsap
缺憾,khuat ham
能耐,ling nai
航程,hang ting
航權,hang khuan
茶藝館,te ge kuan
託付,thok hu
起草,khi tsho
起駕,khi ka
迷失,be sit
迷思,be su
退還,the hing
迴避,hue pi
追擊,tui kik
酒店,tsiu tiam
配色,phue sik
閃光,siam kng
院區,inn khu
骨架,kut ke
高地,ko te
高架,ko ke
停工,thing kang
停刊,thing khan
停靠,thing kho
做為,tso ui
偵察,tsing tshat
偏重,phian tiong
副刊,hu khan
動亂,tong luan
商務,siong bu
商隊,siong tui
唱法,tshiunn huat
唱盤,tshiunn puann
問話,mng ue
國手,kok tshiu
國文,kok bun
國父,kok hu
國片,kok phinn
國安會,kok an hue
國情,kok tsing
國道,kok to
堅信,kian sin
執筆,tsip pit
執勤,tsip khin
宿命,siok bing
專任,tsuan jim
專政,tsuan tsing
專員,tsuan uan
專書,tsuan su
專精,tsuan tsing
專職,tsuan tsit
將士,tsiong su
常務,siong bu
帶狀,tai tsong
強姦,kiong kan
強度,kiong too
彩繪,tshai hue
得票,tik phio
探究,tham kiu
接班,tsiap pan
接單,tsiap tuann
掩護,iam hoo
掃黃,sau ng
推案,thui an
推翻,thui huan
授課,siu kho
採納,tshai lap
救濟,kiu tse
教廷,kau ting
教宗,kau tsong
敗壞,pai huai
敘事,su su
晚安,buan an
梯次,the tshu
條文,tiau bun
淡薄,tam poh
淒涼,tshe liang
深情,tshim tsing
深層,tshim tsan
牽引,khan in
理監事,li kam su
異國,i kok
疏散,soo san
眾神,tsiong sin
票據,phio ki
票選,phio suan
祭品,tse phin
移居,i ku
移師,i su
第二春,te ji tshun
第四台,te si tai
符碼,hu ma
粗淺,tshoo tshian
組件,tsoo kiann
組別,tsoo piat
終年,tsiong ni
終點,tsiong tiam
脫水,thuat tsui
貨款,hue khuan
通信,thong sin
通俗,thong siok
通航,thong hang
通關,thong kuan
連貫,lian kuan
透天,thau thinn
透視,thau si
野台戲,ia tai hi
野花,ia hue
陳設,tin siat
陰暗,im am
章節,tsiong tsiat
魚群,hi kun
魚類,hi lui
創始,tshong si
勞委會,lo ui hue
勞苦,lo khoo
勞資,lo tsu
勝訴,sing soo
喜氣,hi khi
圍捕,ui poo
圍堵,ui too
復古,hok koo
復發,hok huat
提報,the po
景況,king hong
景致,king ti
暑期,su ki
智能,ti ling
港灣,kang uan
渡海,too hai
湖面,oo bin
無妨,bu hong
無知,bu ti
無緣,bo ian
猩猩,sing sing
畫法,ue huat
畫展,ue tian
畫像,ue siong
畫圖,ue too
畫質,ue tsit
發函,huat ham
發病,huat penn
發聲,huat siann
盜版,to pan
硬化,nge hua
窗外,thang gua
等到,tan kau
筆試,pit tshi
結交,kiat kau
結業,kiat giap
結緣,kiat ian
紫色,tsi sik
裁示,tshai si
裁定,tshai ting
裁員,tshai uan
評定,phing ting
詐領,tsa nia
超凡,tshiau huan
超收,tshiau siu
超然,tshiau jian
進用,tsin iong
進貨,tsin hue
進階,tsin kai
鄉愁,hiong tshiu
開門,khui mng
開端,khai tuan
雅緻,nga ti
雄偉,hiong ui
集會,tsip hue
集權,tsip khuan
飲用水,im iong tsui
飲品,im phin
黃絲帶,ng si tua
亂源,luan guan
亂碼,luan be
傳回,thuan hue
傳單,thuan tuann
傳媒,thuan mui
傳話,thuan ue
催眠,tshui bin
傷寒,siong han
匯集,hue tsip
園遊會,uan iu hue
園藝,uan ge
塑身,sok sin
微弱,bi jiok
意象,i siong
搜救,soo kiu
搶救,tshiunn kiu
新任,sin jim
新式,sin sik
新增,sin tsing
會報,hue po
溪頭,khe thau
煎餅,tsian piann
煩心,huan sim
當日,tong jit
盟友,bing iu
節稅,tsiat sue
義工,gi kang
聖嬰,sing ing
落入,loh jip
落下,loh ha
號外,ho gua
補校,poo hau
補給,poo kip
補選,poo suan
補繳,poo kiau
解析,kai sik
解套,kai tho
解救,kai kiu
解碼,kai ma
詳盡,siong tsin
詩句,si ku
詩作,si tsok
話劇,ue kiok
路上,loo siong
路徑,loo king
跳動,thiau tong
跳棋,thiau ki
跳樓,thiau lau
載入,tsai jip
載客,tsai kheh
運量,un liong
遊樂,iu lok
過剩,kue sing
遍佈,pian poo
鉛球,ian kiu
電阻,tian tsoo
電流,tian liu
電路,tian loo
電磁,tian tsu
預知,i ti
頒佈,pan poo
飽滿,pa mua
嘉賓,ka pin
團費,thuan hui
圖騰,too thing
夢見,bang kinn
實況,sit hong
實戰,sit tsian
對焦,tui tsiau
對準,tui tsun
彰顯,tsiong hian
慘烈,tsham liat
截稿,tsiat ko
榮民,ing bin
演進,ian tsin
演藝,ian ge
漢人,han jin
漫談,ban tam
漁業,hi giap
疑點,gi tiam
疑難,gi lan
盡頭,tsin thau
監理,kam li
精子,tsing tsu
精巧,tsing kha
綠卡,lik khah
罰球,huat kiu
腐敗,hu pai
腐爛,hu nua
臺電,tai tian
舞曲,bu khik
舞動,bu tong
舞會,bu hue
製法,tse huat
製播,tse poo
認領,jin nia
說唱,suat tshiunn
遠見,uan kian
酵素,kann soo
銀樓,gin lau
銅環,tang khuan
閣樓,koh lau
領軍,nia kun
劇院,kiok inn
噴射,phun sia
噴墨,phun bak
增生,tsing sing
寬容,khuan iong
審視,sim si
寫生,sia sing
廢氣,hui khi
廣義,kong gi
廠長,tshiunn tiunn
彈奏,tuann tsau
徵求,ting kiu
慧眼,hui gan
摩西,moo se
撥款,puah khuan
撫慰,hu ui
敵對,tik tui
樣式,iunn sik
標明,piau bing
樓層,lau tsan
樂界,gak kai
樂音,gak im
潰瘍,khui iong
熟練,sik lian
熱火,jiat hue
熱度,jiat too
熱舞,jiat bu
獎牌,tsiong pai
稿費,ko hui
緣份,ian hun
衛兵,ue ping
調和,tiau ho
調配,tiau phue
調理,tiau li
調頻,tiau pin
論調,lun tiau
賞花,siunn hue
賞畫,siunn ue
踏出,tah tshut
鋪路,phoo loo
震動,tsin tong
駐軍,tsu kun
黎明,le bing
儒家,ju ka
學府,hak hu
學會,hak hue
導師,to su
戰事,tsian su
橫向,huainn hiong
機油,ki iu
燈具,ting ku
磨練,bua lian
親和,tshin ho
親筆,tshin pit
親善,tshin sian
謀取,boo tshu
謀殺,boo sat
遵照,tsun tsiau
選務,suan bu
選單,suan tuann
鋼牙,kng ge
鋼筋,kng kin
鋼絲,kng si
錄用,lok iong
錄影,lok iann
錦標,kim piau
隨機,sui ki
靜音,tsing im
頭頂,thau ting
應急,ing kip
應徵,ing ting
擊退,kik the
燭光,tsik kng
環節,khuan tsiat
總結,tsong kiat
聯播,lian poo
膽識,tam sik
舉出,ki tshut
講求,kang kiu
講座,kang tso
邀約,iau iok
鞠躬,kiok kiong
斷定,tuan ting
斷訊,tng sin
斷頭,tng thau
歸類,kui lui
職災,tsit tsai
職缺,tsit khueh
職能,tsit ling
職訓,tsit hun
藍調,na tiau
轉手,tsuan tshiu
轉折,tsuan tsiat
轉接,tsuan tsiap
轉速,tng sok
鎮靜,tin tsing
離奇,li ki
離散,li san
離職,li tsit
雜音,tsap im
雜質,tsap tsit
雙腿,siang thui
雙親,siang tshin
雙贏,siang iann
雞肉,ke bah
題庫,te khoo
鬆軟,sang nng
穩重,un tiong
繳款,kiau khuan
繳費,kiau hui
藝品,ge phin
藥廠,ioh tshiunn
關照,kuan tsiau
難民,lan bin
難關,lan kuan
韻味,un bi
顛峰,tian hong
嚴峻,giam tsun
寶典,po tian
寶島,po to
獻身,hian sin
競技,king ki
籌募,tiu boo
籃框,na khing
警局,king kiok
警車,king tshia
警界,king kai
警消,king siau
譯者,ik tsia
贏球,iann kiu
飄揚,phiau iong
黨工,tong kang
黨政,tong tsing
黨章,tong tsiong
欄位,nua ui
灌注,kuan tsu
護航,hoo hang
護膚,hoo hu
護欄,hoo lan
鐵門,thih mng
鐵質,thih tsit
霸權,pa khuan
魔力,moo lik
讀物,thok but
鑑賞,kam siong
竊盜,tshiap to
變異,pian i
變速,pian sok
變質,pian tsit
顯出,hian tshut
顯微鏡,hian bi kiann
體悟,the ngoo
靈巧,ling kha
鹼性,kinn sing
鹽份,iam hun
鹽水,iam tsui
觀想,kuan siong
觀照,kuan tsiau
觀摩,kuan moo
口語,khau gi
大部份,tua poo hun
工錢,kang tsinn
天邊,thinn pinn
水底,tsui te
水缸,tsui kng
他鄉,thann hiong
全家,tsuan ke
冷風,ling hong
冷盤,ling puann
含笑,ham tshiau
吟詩,gim si
稀罕,hi han
忍心,jim sim
和好,ho ho
河邊,ho pinn
油菜花,iu tshai hue
花燈,hue ting
初戀,tshoo luan
拼音,phing im
相思,siunn si
軍師,kun su
音樂聲,im gak siann
員外,uan gue
純情,sun tsing
胸前,hing tsing
乾杯,kan pue
做官,tso kuann
動詞,tong su
情份,tsing hun
惜別,sioh piat
探戈,than goo
殖民者,sit bin tsia
等號,ting ho
華語,hua gi
傳教,thuan kau
傳道,thuan to
傷風,siong hong
微波爐,bi pho loo
電台,tian tai
夢中,bang tiong
盡心,tsin sim
福利社,hok li sia
語義,gi gi
獎券,tsiong kuan
戰後,tsian au
親情,tshin tsing
閻王,giam ong
羅馬字,lo ma ji
讀書,thak tsu
變做,pian tso
掃地,sau te
內野,lai ia
滿壘,mua lui
全壘打,tsuan lui tann
界外球,kai gua kiu
短打,tuan tann
做對,tso tui
立春,lip tshun
雨水,u sui
驚蟄,kenn tit
春分,tshun hun
清明,tshing bing
穀雨,kok u
立夏,lip he
小滿,sio buan
芒種,bong tsing
夏至,he tsi
小暑,siau su
大暑,tai su
立秋,lip tshiu
處暑,tshu su
白露,peh loo
秋分,tshiu hun
寒露,han loo
霜降,sng kang
立冬,lip tang
小雪,siau suat
大雪,tai suat
冬節,tang tseh
小寒,siau han
大寒,tai han
九份二山,kau hun ji suann
八卦山,at kua suann
七星山,tshit tshenn suann
八通關大山,at thong kuan tua suann
大屯山,tua tun suann
大肚山,tua too suann
大武山,tai bu suann
大雪山,tua suat suann
大霸尖山,tua pa tsiam suann
小觀音山,sio kuan im suann
丹大山,tan tua suann
中央山脈,tiong iong suann meh
中央尖山,tiong iong tsiam suann
五指山,ngoo tsi suann
木瓜山,bok kue suann
巴陵,a ling
太魯閣大山,thai loo kooh tua suann
火炎山,hue iam suann
北合歡山,ak hap huan suann
半屏山,uann ping suann
北插天山,ak tshah thian suann
玉山,giok san
向天湖山,hiong thian oo suann
竹仔山,tik a suann
秀姑巒山,siu koo luan suann
角板山,kak pan suann
卑南主山,i lam tsu suann
奇萊主山北峰,ki lai tsu suann pak hong
拉拉山,la la san
阿里山,a li san
虎頭山,hoo thau suann
南仁山,lam jin suann
南胡大山,lam oo tua suann
紅葉山,ang hioh suann
紅頭山,ang thau suann
柴山,tsha suann
祝山,tsiok suann
紗帽山,se bo suann
草山,tshau suann
基隆山,ke lang suann
雪山,suat suann
陽明山,iunn bing suann
獅頭山,sai thau suann
壽山,siu san
旗尾山,ki bue suann
龜山島山,ku suann to suann
廬山,loo san
關山,kuan san
關仔嶺,kuan a nia
觀音山,kuan im suann
二二八公園,ji ji pat kong hng
大安森林公園,tai an sim lim kong hng
大稻埕偶戲館,tua tiu tiann ngoo hi kuan
天文臺,thian bun tai
天文館,thian bun kuan
木柵動物園,bak sa tong but hng
臺北二二八紀念館,tai pak ji ji pat ki liam kuan
臺北市立天文科學教育館,tai pak tshi lip thian bun kho hak kau iok kuan
臺北市兒童交通博物館,tai pak tshi ji tong kau thong hok but kuan
臺北故事館,tai pak koo su kuan
臺北海洋館,tai pak hai iunn kuan
臺北探索館,tai pak tham soh kuan
臺北當代藝術館,tai pak tong tai ge sut kuan
北投溫泉博物館,ak tau un tsuann hok but kuan
臺灣民俗北投文物館,tai uan bin siok ak tau bun but kuan
臺灣林業陳列館,tai uan lim giap tin liat kuan
自來水博物館,tsu lai tsui hok but kuan
佛光緣臺北美術館,hut kong ian tai pak bi sut kuan
李石樵美術館,li tsioh tsiau bi sut kuan
育樂園,iok lok hng
林安泰古厝民俗文物館,lim an thai koo tshu bin siok bun but kuan
林語堂紀念館,lim gu tong ki liam kuan
玩石家博石館,guan sik ka hok sik kuan
故宮博物院,koo kiong hok but inn
科學博物館,kho hak hok but kuan
美術館,bi sut kuan
海洋生物館,hai iunn sing but kuan
海關博物館,hai kuan hok but kuan
琉園水晶博物館,liu uan tsui tsinn hok but kuan
草山行館,tshau suann hing kuan
國父史蹟紀念館,kok hu su tsik ki liam kuan
國立臺灣科學教育院,kok lip tai uan kho hak kau iok inn
國立臺灣博物館,kok lip tai uan hok but kuan
國立臺灣藝術教育館,kok lip tai uan ge sut kau iok kuan
國軍歷史文物館,kok kun lik su bun but kuan
張大千紀念館,tiunn tai tshian ki liam kuan
袖珍博物館,siu tin hok but kuan
郭元益糕餅博物館,kueh guan ik ko piann hok but kuan
凱達格蘭文化館,ke ta ga lan bun hua kuan
郵政博物館,iu tsing hok but kuan
順益臺灣原住民博物館,sun ik tai uan guan tsu bin hok but kuan
新公園,sin kong hng
楊英風美術館,iunn ing hong bi sut kuan
鳳甲文化館,hong kah bun hua kuan
樹火紀念紙博物館,su hue ki liam tsua hok but kuan
歷史博物館,lik su hok but kuan
錢穆紀念館,tsinn bok ki liam kuan
總統府衙,tsong thong hu ge
鴻禧美術館,hong hi bi sut kuan
西部幹線,se poo kan suann
山線,suann suann
臺北,tai pak
萬華,ban hua
板橋,ang kio
樹林,tshiu na
山佳,suann kha
鶯歌,ing ko
桃園,tho hng
內壢,lai lik
中壢,tiong lik
埔心,oo sim
楊梅,iunn mui
富岡,hu kong
湖口,oo khau
新豐,sin hong
竹北,tik pak
新竹,sin tik
香山,hiong san
崎頂,kia ting
竹南,tik lam
造橋,tso kio
豐富,hong hu
苗栗,biau lik
南勢,lam si
銅鑼,tang lo
三義,sam gi
泰安,thai an
后里,au li
豐原,hong guan
潭子,tham tsu
臺中,tai tiong
大慶,tai khing
烏日,oo jit
成功,sing kong
彰化,tsiang hua
花壇,hue tuann
員林,uan lim
永靖,ing tsing
社頭,sia thau
田中,tian tiong
二水,ji tsui
林內,na lai
斗六,tau lak
斗南,tau lam
石龜,tsioh ku
大林,tua na
民雄,bin hiong
嘉義,ka gi
水上,tsui siong
南靖,lam tsing
後壁,au piah
新營,sin iann
柳營,liu iann
林鳳營,lim hong iann
隆田,liong tian
拔仔林,at a na
善化,sian hua
新市,sin tshi
永康,ing khong
臺南,tai lam
保安,o an
中洲,tiong tsiu
大湖,tua oo
路竹,loo tik
岡山,kong san
橋仔頭,kio a thau
楠梓,lam tsu
左營,tso iann
高雄,ko hiong
海線,hai suann
談文,tam bun
大山,tua suann
後龍,au lang
龍港,ling kang
白沙屯,eh sua tun
新埔,sin poo
通霄,thong siau
苑裡,uan li
日南,jit lam
大甲,tai kah
臺中港,tai tiong kang
清水,tshing tsui
沙鹿,sua lak
龍井,liong tsinn
大肚,tua too
追分,tui hun
屏東線,in tong suann
鳳山,hong suann
後庄,au tsng
九曲堂,kiu khiok tong
六塊厝,lak te tshu
屏東,in tong
歸來,kui lai
麟洛,lin lok
西勢,sai si
竹田,tik tshan
潮州,tio tsiu
崁頂,kham ting
南州,lam tsiu
鎮安,tin an
林仔邊,na a pinn
佳冬,ka tang
東海,tang hai
枋寮,ang liau
東部幹線,tang poo kan suann
四城,si siann
林榮新光,lim ing sin kong
豐田,hong tian
七堵,tshit too
八堵,eh too
基隆,ke lang
暖暖,luan luan
四腳亭,si kha ting
瑞芳,sui hong
猴硐仔,kau tong a
三貂嶺,sam tiau nia
牡丹,boo tan
雙溪,siang khe
貢寮,kong liau
福隆,hok liong
石城,tsioh siann
大里,tai li
大溪,tai khe
龜山,ku suann
外澳,gua o
頭城,thau siann
頂埔,ting poo
礁溪,ta khe
宜蘭,gi lan
二結,ji kiat
中里,tiong li
羅東,lo tong
冬山,tang suann
新馬,sin ma
蘇澳新站,soo o sin tsam
蘇澳,soo o
永樂,ing lok
東澳,tang o
南澳,lam o
武塔,bu thah
漢本,han pun
和平,ho ping
和仁,ho jin
崇德,tsong tik
新城,sin siann
景美,king bi
北埔,ak poo
花蓮,hua lian
吉安,kiat an
志學,tsi hak
平和,ing ho
壽豐,siu hong
南平,lam ping
鳳林,hong lim
萬榮,ban ing
光復,kong hok
大富,tai ho
富源,hu guan
瑞穗,tsui bue
三民,sam bin
玉里,giok li
東里,tang li
東竹,tang tik
富里,hu li
池上,ti siong
海端,hai tuan
關山,kuan san
瑞和,sui ho
瑞源,sui guan
鹿野,lok ia
山里,san li
臺東,tai tang
南迴鐵路,lam hue thih loo
加祿,ka lok
內獅,lai sai
枋山,ang suann
大武,tai bu
瀧溪,liong khe
金崙,kim lun
太麻里,thai ma li
知本,ti pun
康樂,khong lok
平溪線,ing khe suann
大華,tai hua
十分,tsap hun
望古,bong koo
嶺腳,nia kha
平溪,ing khe
菁桐,tshinn tong
內灣線,lai uan suann
竹中,tik tiong
上員,siong guan
竹東,tik tang
橫山,huainn suann
九讚頭,kau tsan thau
合興,hap hing
榮華,ing hua
內灣,lai uan
集集線,tsip tsip suann
源泉,guan tsuann
濁水,lo tsui
龍泉,ling tsuann
集集,tsip tsip
水里,tsui li
車埕,tshia tiann
北門,ak mng
竹崎,tik kia
木屐寮,bak kiah liau
樟腦寮,tsiunn noo liau
獨立山,tok lip suann
梨園寮,le hng liau
交力坪,ka lik penn
水社寮,tsui sia liau
奮起湖,un ki oo
多林,to lim
十字路,sip ji loo
屏遮那,he sen na
對高岳,tui ko gak
二萬坪,ji ban penn
神木,sin bok
阿里山,a li san
沼平,tsau ping
臺北市,tai pak tshi
松山區,siong san khu
信義區,sin gi khu
大安區,tai an khu
中山區,tiong san khu
中正區,tiong tsing khu
大同區,tai tong khu
萬華區,ban hua khu
文山區,bun san khu
南港區,lam kang khu
內湖區,lai oo khu
士林區,su lim khu
北投區,ak tau khu
高雄市,ko hiong tshi
鹽埕區,iam tiann khu
鼓山區,koo san khu
左營區,tso iann khu
楠梓區,lam tsu khu
三民區,sam bin khu
新興區,sin hing khu
前金區,tsian kim khu
苓雅區,ling nga khu
前鎮區,tsian tin khu
旗津區,ki tin khu
小港區,sio kang khu
新北市,sin pak tshi
板橋區,ang kio khu
三重區,sam tiong khu
中和區,tiong ho khu
永和區,ing ho khu
新莊區,sin tsng khu
新店區,sin tiam khu
樹林區,tshiu na khu
鶯歌區,ing ko khu
三峽區,sam kiap khu
淡水區,tam tsui khu
汐止區,sik tsi khu
瑞芳區,sui hong khu
土城區,thoo siann khu
蘆洲區,loo tsiu khu
五股區,goo koo khu
泰山區,thai san khu
林口區,na khau khu
深坑區,tshim khinn khu
石碇區,tsioh ting khu
坪林區,inn na khu
三芝區,sam tsi khu
石門區,tsioh mng khu
八里區,at li khu
平溪區,ing khue khu
雙溪區,siang khe khu
貢寮區,kong liau khu
金山區,kim san khu
萬里區,ban li khu
烏來區,u lai khu
宜蘭縣,gi lan kuan
宜蘭市,gi lan tshi
羅東鎮,lo tong tin
蘇澳鎮,soo o tin
頭城鎮,thau siann tin
礁溪鄉,ta khe hiong
壯圍鄉,tsong ui hiong
員山鄉,inn suann hiong
冬山鄉,tang suann hiong
五結鄉,goo kiat hiong
三星鄉,sam sing hiong
大同鄉,tai tong hiong
南澳鄉,lam o hiong
桃園市,tho hng tshi
桃園區,tho hng khu
中壢區,tiong lik khu
大溪區,tai khe khu
楊梅區,iunn mui khu
蘆竹區,loo tik khu
大園區,tua hng khu
龜山區,ku suann khu
八德區,at tik khu
龍潭區,liong tham khu
平鎮區,ing tin khu
新屋區,sin ok khu
觀音區,kuan im khu
復興區,hok hing khu
新竹縣,sin tik kuan
竹北市,tik pak tshi
竹東鎮,tik tang tin
新埔鎮,sin poo tin
關西鎮,kuan se tin
湖口鄉,oo khau hiong
新豐鄉,sin hong hiong
芎林鄉,kiong na hiong
橫山鄉,huainn suann hiong
北埔鄉,ak poo hiong
寶山鄉,o san hiong
峨眉鄉,ngoo bi hiong
尖石鄉,tsiam tsioh hiong
五峰鄉,ngoo hong hiong
苗栗縣,biau lik kuan
苗栗市,biau lik tshi
苑裡鎮,uan li tin
通霄鎮,thong siau tin
竹南鎮,tik lam tin
頭份鎮,thau hun tin
後龍鎮,au lang tin
卓蘭鎮,toh lan tin
大湖鄉,tua oo hiong
公館鄉,kong kuan hiong
銅鑼鄉,tang lo hiong
南庄鄉,lam tsng hiong
頭屋鄉,thau ok hiong
三義鄉,sam gi hiong
西湖鄉,se oo hiong
造橋鄉,tso kio hiong
三灣鄉,sam uan hiong
獅潭鄉,sai tham hiong
泰安鄉,thai an hiong
豐原區,hong guan khu
東勢區,tang si khu
大甲區,tai kah khu
清水區,tshing tsui khu
沙鹿區,sua lak khu
梧棲區,goo tshe khu
后里區,au li khu
神岡區,sin kong khu
潭子區,tham tsu khu
大雅區,tai nge khu
新社區,sin sia khu
石岡區,tsioh kng khu
外埔區,gua poo khu
大安區,tai an khu
烏日區,oo jit khu
大肚區,tua too khu
龍井區,liong tsinn khu
霧峰區,bu hong khu
太平區,thai ping khu
大里區,tai li khu
和平區,ho ping khu
彰化縣,tsiong hua kuan
彰化市,tsiong hua tshi
鹿港鎮,lok kang tin
和美鎮,ho bi tin
線西鄉,suann sai hiong
伸港鄉,sin kang hiong
福興鄉,hok hing hiong
秀水鄉,siu tsui hiong
花壇鄉,hue tuann hiong
芬園鄉,hun hng hiong
員林市,uan lim tshi
溪湖鎮,khe oo tin
田中鎮,tian tiong tin
大村鄉,tai tshuan hiong
埔鹽鄉,oo iam hiong
埔心鄉,oo sim hiong
永靖鄉,ing tsing hiong
社頭鄉,sia thau hiong
二水鄉,ji tsui hiong
北斗鎮,ak tau tin
二林鎮,ji lim tin
田尾鄉,tshan bue hiong
埤頭鄉,i thau hiong
芳苑鄉,hong uan hiong
大城鄉,tua siann hiong
竹塘鄉,tik tng hiong
溪州鄉,khe tsiu hiong
南投縣,lam tau kuan
南投市,lam tau tshi
埔里鎮,oo li tin
草屯鎮,tshau tun tin
竹山鎮,tik san tin
集集鎮,tsip tsip tin
名間鄉,bing kan hiong
鹿谷鄉,lok kok hiong
中寮鄉,tiong liau hiong
魚池鄉,hi ti hiong
國姓鄉,kok sing hiong
水里鄉,tsui li hiong
信義鄉,sin gi hiong
仁愛鄉,jin ai hiong
雲林縣,hun lim kuan
斗六市,tau lak tshi
斗南鎮,tau lam tin
虎尾鎮,hoo bue tin
西螺鎮,sai le tin
土庫鎮,thoo khoo tin
北港鎮,ak kang tin
古坑鄉,koo khenn hiong
大埤鄉,tua pi hiong
莿桐鄉,tshi tong hiong
林內鄉,na lai hiong
二崙鄉,ji lun hiong
崙背鄉,lun pue hiong
麥寮鄉,beh liau hiong
東勢鄉,tang si hiong
褒忠鄉,o tiong hiong
臺西鄉,tai se hiong
元長鄉,guan tsiong hiong
四湖鄉,si oo hiong
口湖鄉,khau oo hiong
水林鄉,tsui na hiong
嘉義縣,ka gi kuan
太保市,thai po tshi
朴子市,hoh tsu tshi
布袋鎮,oo te tin
大林鎮,tua na tin
民雄鄉,bin hiong hiong
溪口鄉,khe khau hiong
新港鄉,sin kang hiong
六腳鄉,lak kha hiong
東石鄉,tang tsioh hiong
義竹鄉,gi tik hiong
鹿草鄉,lok tshau hiong
水上鄉,tsui siang hiong
中埔鄉,tiong poo hiong
竹崎鄉,tik kia hiong
梅山鄉,mui san hiong
番路鄉,huan loo hiong
大埔鄉,tua poo hiong
阿里山鄉,a li san hiong
新營區,sin iann khu
鹽水區,kiam tsui khu
白河區,eh ho khu
柳營區,liu iann khu
後壁區,au piah khu
東山區,tong san khu
麻豆區,mua tau khu
下營區,e iann khu
六甲區,lak kah khu
官田區,kuann tian khu
大內區,tua lai khu
佳里區,ka li khu
學甲區,hak kah khu
西港區,sai kang khu
七股區,tshit koo khu
將軍區,tsiong kun khu
北門區,ak mng khu
新化區,sin hua khu
善化區,sian hua khu
新市區,sin tshi khu
安定區,an ting khu
山上區,san siong khu
玉井區,giok tsenn khu
楠西區,lam se khu
南化區,lam hua khu
左鎮區,tso tin khu
仁德區,jin tik khu
歸仁區,kui jin khu
關廟區,kuan bio khu
龍崎區,liong kia khu
永康區,ing khong khu
鳳山區,hong suann khu
林園區,lim hng khu
大寮區,tua liau khu
大樹區,tua tshiu khu
大社區,tua sia khu
仁武區,jin bu khu
鳥松區,tsiau tshing khu
岡山區,kong san khu
橋頭區,kio thau khu
燕巢區,ian tsau khu
田寮區,tshan liau khu
阿蓮區,a lian khu
路竹區,loo tik khu
湖內區,oo lai khu
茄萣區,ka tiann khu
永安區,ing an khu
彌陀區,mi to khu
梓官區,tsu kuann khu
旗山區,ki san khu
美濃區,bi long khu
六龜區,lak ku khu
甲仙區,kah sian khu
杉林區,sam na khu
內門區,lai bun khu
茂林區,boo lim khu
桃源區,tho guan khu
那瑪夏區,na ma siah khu
屏東縣,in tong kuan
屏東市,in tong tshi
潮州鎮,tio tsiu tin
東港鎮,tang kang tin
恆春鎮,hing tshun tin
萬丹鄉,ban tan hiong
長治鄉,tiong ti hiong
麟洛鄉,lin lok hiong
九如鄉,kiu ju hiong
里港鄉,li kang hiong
鹽埔鄉,iam poo hiong
高樹鄉,ko tshiu hiong
萬巒鄉,ban ban hiong
內埔鄉,lai poo hiong
竹田鄉,tik tshan hiong
新埤鄉,sin pi hiong
枋寮鄉,ang liau hiong
新園鄉,sin hng hiong
崁頂鄉,kham ting hiong
林邊鄉,na pinn hiong
南州鄉,lam tsiu hiong
佳冬鄉,ka tang hiong
琉球鄉,liu khiu hiong
車城鄉,tsha siann hiong
滿州鄉,buan tsiu hiong
枋山鄉,ang suann hiong
三地門鄉,sam te mng hiong
霧臺鄉,bu tai hiong
瑪家鄉,ma ka hiong
泰武鄉,thai bu hiong
來義鄉,lai gi hiong
春日鄉,tshun jit hiong
獅子鄉,sai a hiong
牡丹鄉,boo tan hiong
臺東縣,tai tang kuan
臺東市,tai tang tshi
成功鎮,sing kong tin
關山鎮,kuan san tin
卑南鄉,i lam hiong
鹿野鄉,lok ia hiong
池上鄉,ti siong hiong
東河鄉,tong ho hiong
長濱鄉,tiong pin hiong
太麻里鄉,thai ma li hiong
大武鄉,tai bu hiong
綠島鄉,lik to hiong
海端鄉,hai tuan hiong
延平鄉,ian ping hiong
金峰鄉,kim hong hiong
達仁鄉,tat jin hiong
蘭嶼鄉,lan su hiong
花蓮縣,hua lian kuan
花蓮市,hua lian tshi
鳳林鎮,hong lim tin
玉里鎮,giok li tin
新城鄉,sin siann hiong
吉安鄉,kiat an hiong
壽豐鄉,siu hong hiong
光復鄉,kong hok hiong
豐濱鄉,hong pin hiong
瑞穗鄉,sui sui hiong
富里鄉,hu li hiong
秀林鄉,siu lim hiong
萬榮鄉,ban ing hiong
卓溪鄉,toh khe hiong
澎湖縣,hinn oo kuan
馬公市,ma king tshi
湖西鄉,oo sai hiong
白沙鄉,eh sua hiong
西嶼鄉,sai su hiong
望安鄉,bang uann hiong
七美鄉,tshit bi hiong
基隆市,ke lang tshi
中正區,tiong tsing khu
七堵區,tshit too khu
暖暖區,luan luan khu
仁愛區,jin ai khu
中山區,tiong san khu
安樂區,an lok khu
信義區,sin gi khu
新竹市,sin tik tshi
東區,tang khu
北區,ak khu
香山區,hiong san khu
臺中市,tai tiong tshi
中區,tiong khu
東區,tang khu
南區,lam khu
西區,sai khu
北區,ak khu
西屯區,sai tun khu
南屯區,lam tun khu
北屯區,ak tun khu
嘉義市,ka gi tshi
東區,tang khu
西區,sai khu
臺南市,tai lam tshi
東區,tang khu
南區,lam khu
北區,ak khu
中西區,tiong se khu
安南區,an lam khu
安平區,an ping khu
金門縣,kim mng kuan
金城鎮,kim siann tin
金沙鎮,kim sua tin
金湖鎮,kim oo tin
金寧鄉,kim ling hiong
烈嶼鄉,liat su hiong
烏坵鄉,oo khiu hiong
連江縣,lian kang kuan
南竿鄉,lam kan hiong
北竿鄉,ak kan hiong
莒光鄉,ki kong hiong
東引鄉,tang in hiong
東沙,tang sua
南沙,lam sua
釣魚台,tio hi tai
中山國中,tiong san kok tiong
南京復興,lam kiann hok hing
忠孝復興,tiong hau hok hing
大安,tai an
科技大樓,kho ki tua lau
六張犁,lak tiunn le
麟光,lin kong
辛亥,sin hai
萬芳醫院,ban hong enn inn
萬芳社區,ban hong sia khu
木柵,bak sa
動物園,tong but hng
紅樹林,ang tshiu na
竹圍仔,tik ui a
關渡,kan tau
忠義,tiong gi
復興崗,hok hing kong
北投,ak tau
奇岩,ki giam
唭哩岸,ki li gan
石牌仔,tsioh pai a
明德,bing tik
芝山,tsi san
士林,su lim
劍潭,kiam tham
圓山仔,inn suann a
民權西路,bin kuan se loo
雙連,siang lian
中山,tiong san
臺北車站,tai pak tshia tsam
臺大醫院,tai tai enn inn
中正紀念堂,tiong tsing ki liam tng
古亭,koo ting
臺電大樓,tai tian tua lau
公館,kong kuan
萬隆,ban liong
景美,king bue
大坪林,tua pinn na
七張,tshit tiunn
新店區公所,sin tiam khu kong soo
新店,sin tiam
頂溪,ting khe
永安市場,ing an tshi tiunn
景安,king an
南勢角,lam si kak
昆陽,khun iong
後山埤,au suann pi
永春,ing tshun
市政府,tshi tsing hu
國父紀念館,kok hu ki liam kuan
忠孝敦化,tiong hau tun hua
善導寺,sian to si
西門,se mng
龍山寺,liong san si
江子翠,kang a tshui
新埔,sin poo
板橋,ang kio
府中,hu tiong
亞東醫院,a tang enn inn
海山,hai san
土城,thoo siann
永寧,ing ling
小南門,sio lam mng
新北投,sin pak tau
小碧潭,sio phik tham
西子灣,se a uan
鹽埕埔,iam tiann poo
市議會,tshi gi hue
信義國小,sin gi kok sio
文化中心,bun hua tiong sim
五塊厝,goo te tshu
技擊館,ki kik kuan
衛武營,ue bu iann
鳳山西站,hong suann sai tsam
鳳山,hong suann
大東,tai tang
鳳山國中,hong suann kok tiong
大寮,tua liau
小港,sio kang
高雄國際機場,ko hiong kok tse ki tiunn
草衙,tshau ge
前鎮高中,tsian tin ko tiong
凱旋,khai suan
獅甲,sai kah
三多商圈,sam to siong khuan
中央公園,tiong iong kong hng
美麗島,bi le to
高雄車站,ko hiong tshia tsam
後驛,au iah
凹子底,lap a te
巨蛋,ki tan
生態園區,sing thai hng khu
左營,tso iann
世運,se un
油廠國小,iu tshiunn kok sio
楠仔梓科技園區,lam a khenn kho ki hng khu
後勁,au nge
都會公園,too hue kong hng
青埔,tshenn poo
橋頭糖廠,kio thau thng tshiunn
橋頭火車站,kio thau hue tshia tsam
岡山高醫,kong san ko i
大直,tai tit
劍南路,kiam lam loo
西湖,se oo
港墘,kang kinn
文德,bun tik
內湖,lai oo
大湖公園,tua oo kong hng
葫洲,oo tsiu
東湖,tang oo
南港軟體園區,lam kang nng the hng khu
南港,lam kang
南港展覽館,lam kang tian lam kuan
松山機場,siong san ki tiunn
輔大,hu tai
新莊,sin tsng
頭前庄,thau tsing tsng
先嗇宮,sian sik kiong
三重埔,sann ting poo
菜寮,tshai liau
臺北橋,tai pak kio
大橋頭,tua kio thau
中山國小,tiong san kok sio
行天宮,hing thian kiong
松江南京,siong kang lam kiann
忠孝新生,tiong hau sin sing
東門,tang mng
蘆洲,loo tsiu
三民高中,sam bin ko tiong
徐匯中學,tshi hue tiong hak
三和國中,sam ho kok tiong
三重國小,sam tiong kok sio
淡水,tam tsui
基隆港,ke lang kang
臺中港,tai tiong kang
高雄港,ko hiong kang
蘇澳港,soo o kang
花蓮港,hua lian kang
蘭陽溪,lan iang khe
羅東溪,lo tong khe
宜蘭河,gi lan ho
大礁溪,tua ta khe
小礁溪,sio ta khe
淡水河,tam tsui ho
三峽河,sam kiap ho
大漢溪,tai han khe
新店溪,sin tiam khe
基隆河,ke lang ho
北勢溪,ak si khe
景美溪,king be khe
鳳山溪,hong suann khe
頭前溪,thau tsing khe
油羅溪,iu lo khe
上坪溪,siong ping khe
中港溪,tiong kang khe
後龍溪,au lang khe
老田寮溪,lau tshan liau khe
大安溪,tai an khe
景山溪,king suann khe
大甲溪,tai kah khe
烏溪,oo khe
貓羅溪,bau lo khe
眉溪,bai khe
北港溪,ak kang khe
大里溪,tai li khe
旱溪,han khe
頭汴坑溪,thau pan khenn khe
濁水溪,lo tsui khe
清水溪,tshing tsui khe
陳有蘭溪,tan iu lan khe
東埔蚋溪,tong poo lak khe
朴子溪,hoh tsu khe
八掌溪,at tsiang khe
急水溪,kip tsui khe
曾文溪,tsan bun khe
後堀溪,au khut khe
官田溪,kuann tian khe
鹽水溪,kiam tsui khe
二仁溪,ji jin khe
阿公店溪,a kong tiam khe
高屏溪,ko pin khe
旗山溪,ki san khe
美濃溪,bi long khe
荖濃溪,lau long khe
濁口溪,lo khau khe
隘寮溪,ai liau khe
武洛溪,bu lok khe
東港溪,tang kang khe
四重溪,si ting khe
卑南溪,i lam khe
鹿野溪,lok ia khe
鹿寮溪,lok liau khe
秀姑巒溪,siu koo luan khe
紅葉溪,ang hioh khe
富源溪,hu guan khe
豐坪溪,hong penn khe
樂樂溪,lok lok khe
花蓮溪,hua lian khe
木瓜溪,bok kue khe
壽豐溪,siu hong khe
萬里溪,ban li khe
光復溪,kong hok khe
馬太鞍溪,ma tai an khe
和平溪,ho ping khe
十八王公廟,tsap peh ong kong bio
三山國王廟,sam san kok ong bio
大仙寺,tai sian si
大興宮,tai hin kiong
仁和宮,jin ho kiong
五福宮,ngoo hok kiong
孔子廟,khong tsu bio
水仙宮,tsui sian kiong
天后宮,thian hio kiong
文武廟,bun bu bio
仙公廟,sian kong bio
代天府,tai thian hu
北極殿,ak kik tian
行天宮,hing thian kiong
佛光山,hut kong san
沙東宮,sua tong kiong
奉天宮,hong thian kiong
定光佛廟,ting kong hut bio
武聖廟,bu sing bio
祀典武廟,su tian bu bio
青山國王廟,tshing san kok ong bio
長和宮,tiong ho kiong
保安宮,o an kiong
南瑤宮,lam iau kiong
指南宮,tsi lam kiong
昭應宮,tsiau ing kiong
恩主公廟,un tsu kong bio
祖師廟,tsoo su bio
清水巖,tshing tsui giam
都城隍廟,too sing hong bio
惠濟宮,hui tse kiong
景福宮,king hok kiong
朝天宮,tiau thian kiong
開元寺,khai guan si
開化寺,khai hua si
集應廟,tsip ing bio
媽祖宮,ma tsoo king
媽祖廟,ma tsoo bio
慈天宮,tsu thian kiong
慈濟宮,tsu tse kiong
義民廟,gi bin bio
萬和宮,ban ho kiong
福佑宮,hok iu kiong
碧霞宮,hik ha kiong
德化堂,tik hua tng
廣福宮,kong hok kiong
慶安宮,khing an kiong
褒忠亭,o tiong ting
鄧公廟,ting kong bio
鄭氏家廟,tenn si ka bio
龍山寺,liong san si
總趕宮,tsong a king
齋明寺,tsai bing si
鎮瀾宮,tin lan kiong
懷忠祠,huai tiong si
關渡宮,kan tau king
觀音寺,kuan im si
二八水,ji pat tsui
二竹圍,ji tik ui
八里坌,at li hun
九芎林,kiu kiong na
七股寮,tshit koo liau
八芝蘭,at tsi lan
二崙仔,ji lun a
九塊厝,kau te tshu
八塊厝,eh te tshu
三叉河,sam tshe ho
山仔頂,suann a ting
山仔跤,suann a kha
大目降,tua bak kang
大安,tai an
大庄,tua tsng
山地門,suann te mng
大里杙,tai li khit
三角店,sann kak tiam
三角湧,sann kak ing
大佳臘,tua ka lah
大坵園,tua khu hng
下林仔,e na a
大社,tua sia
三重埔,sann ting poo
大埔心,tua poo sim
大埔林,tua poo na
下埤頭,e pi thau
大嵙崁,tua khoo kham
大嵙陷,tua khoo ham
大湖,tua oo
大湖口,tua oo khau
大隘,tua ai
大樹跤,tua tshiu kha
大龍泵,tua long pong
大嶼,tua su
大壩仔,tua pa a
五叉水路,goo tshe tsui loo
五股坑,goo koo khenn
五城堡,goo siann po
內埔,lai poo
公埔,kong poo
六根莊,lak kin tsng
元掌,guan tsiong
五間厝,goo king tshu
六跤佃莊,lak kha tian tsng
六龜里社,lak ku li sia
斗六門,tau lak mng
木瓜村,bok kue tshuan
水尾,tsui bue
水返腳,tsui tng kha
月津港,guat tin kang
月眉,gueh bai
水堀頭,tsui khut thau
水裡坑,tsui li khenn
水燦林,tsui tshan na
巴壟衛,a long ue
火山巖,hue suann giam
牛罵頭,gu ma thau
火燒島,hue sio to
他里霧,ta li bu
冬瓜山,tang kue suann
加走灣,ka tsau uan
北門嶼,ak mng su
臺南府,tai lam hu
凹浪,au lang
四湖,si oo
半路竹,uann loo tik
半路店,uann loo tiam
半線,uann suann
民壯圍,bin tsong ui
打狗,ta kau
打馬武窟,tann ma bu khut
布袋喙,oo te tshui
平湖,inn oo
打貓,tann niau
田中央,tshan tiong ng
目加溜,bak ka liu
石硿仔,tsioh kng a
石觀音,tsioh kuan im
吉野,kiat ia
尖山,tsiam suann
安平鎮,an ping tin
朴仔跤,hoh a kha
竹塹,tik tsham
竹頭崎,tik thau kia
老懂,loo tong
西港仔,sai kang a
吧哩嘓,a li kok
吞霄,thun siau
沙轆,sua lak
牡丹坑,boo tan khenn
牡丹社,boo tan sia
豆仔埔,tau a poo
角板山,kak pan suann
赤崁,tshiah kham
𥴊仔賴,kam a lua
來社,lai sia
卑南,i lam
和尚洲,hue siunn tsiu
坪林尾,inn na be
奇武卒,ki bu tsut
店仔口,tiam a khau
官佃,kuann tian
承天府,sing thian hu
林仔邊,na a pinn
林杞埔,lim ki poo
東勢角,tang si kak
東勢厝,tang si tshu
枋橋頭,ang kio thau
武士林,bu su na
武溜灣,bu liu uan
直加弄,tit ka long
羌仔寮,kiunn a liau
芝蘭三堡,tsi lan sam po
阿公店,a kong tiam
金包里,kim pau li
阿里港,a li kang
阿里壟,a li long
阿里關,a li kuan
金崙,kim lun
阿猴,a kau
阿罩霧,a ta bu
阿嗹社,a lian sia
南莊,lam tsng
前溝尾,tsing kau bue
哈馬星,ha ma sing
哆囉滿,to lo buan
後壁厝,au piah tshu
後壟,au lang
查畝營,tsa boo iann
洄瀾,hue lian
玲珞社,lin lok sia
菅蓁林,kuann tsin na
紅毛田,ang moo tshan
紅毛港,ang mng kang
紅瓦厝仔,ang hia tshu a
紅頭嶼,ang thau su
苓仔寮,ling a liau
茄拔,ka puat
茄苳萣仔,ka tang tiann a
茄苳跤,ka tang kha
茄苳跤,ka tang kha
風櫃,hong kui
埔姜崙,oo kiunn lun
埔姜頭,oo kiunn thau
崁仔跤,kham a kha
桃仔園,tho a hng
柴城,tsha siann
海口,hai khau
海墘營,hai kinn iann
畚箕港,un ki kang
新廣,sin kong
草山,tshau suann
臭水,tshau tsui
臭水庄,tshau tsui tsng
草鞋墩,tshau e tun
蚊蟀,bang sut
馬大安,ma tai an
馬里勿,ma li but
高樹跤,ko tshiu kha
乾溪,ta khe
唭哩岸,ki li gan
國姓埔,kok sing poo
將軍莊,tsiong kun tsng
崩山,ang suann
庵古坑,am koo khenn
梅仔坑,mue a khenn
犁頭店,le thau tiam
笨港,un kang
鹿仔草庄,lok a tshau tsng
鹿仔港,lok a kang
麻里折口,ba li tsik khau
鳥松跤,tsiau tshing kha
麻荖漏,mua lau lau
鹿麻產,lok mua san
麻園寮,mua hng liau
鹿寮,lok liau
梘尾,king bue
傀儡關,ka le kuan
勞里散,lo li san
圍仔內,ui a lai
富貴角,hu kui kak
嵌頭屋,kham thau ok
援巢右,uan tsau iu
湳仔,lam a
港仔喙,kang a tshui
猴樹港,kau tshiu kang
番仔田,huan a tshan
番仔挖,huan a uat
番仔莊,huan a tsng
番仔路,huan a loo
莿桐巷,tshi tong hang
蛤仔難,kap a lan
象鼻湖,tshiunn phinn oo
噍吧哖,ta pa ni
圓山仔,inn suann a
塗庫莊,thoo khoo tsng
媽宮,ma king
媽祖田,ma tsoo tshan
搭里霧,ta li buh
新厝仔,sin tshu a
新厝莊,sin tshu tsng
新埤頭,sin pi thau
新港,sin kang
新港,sin kang
新港,sin kang
楠仔坑,lam a khenn
楊梅壢,iunn mui lik
溪州,khe tsiu
瑯嶠,long kiau
罩蘭,ta lan
萬里橋,ban li kio
葫蘆墩,hoo loo tun
衙門口,ge mng khau
隘寮下,ai liau e
旗後,ki au
槓仔寮,khong a liau
滬尾,hoo bue
漳和,tsiang ho
瑪鋉,ma sok
網鞍,bang uann
艋舺,bang kah
銅鑼灣,tang lo uan
潭仔墘,tham a kinn
澗仔壢,kan a lik
諸羅山,tsu lo san
噶瑪蘭,kat ma lan
橋仔頭,kio a thau
樹杞林,tshiu ki na
樹林口,tshiu na khau
璞石閣,hok sik koh
興化廍,hing hua phoo
蕃薯寮,han tsi liau
蕭壟,siau lang
貓公,ba kang
貓里,ba li
錫口,sik khau
頭圍,thau ui
龍目井,ling bak tsinn
龜崙社,ku lun sia
彌陀港,bi lo kang
彌濃,bi long
螺陽,le iang
螺絲港,loo si kang
薰園,hun hng
雙溪口,siang khe khau
雞籠,ke lang
鯉魚尾,li hi bue
羅漢內門,lo han lai bun
關帝廟,kuan te bio
關帝廟街,kuan te bio ke
寶斗,o tau
寶桑莊,o song tsng
蘆竹厝,loo tik tshu
鹹埔,kiam poo
鹹菜甕,kiam tshai ang
鶯歌石,ing ko tsioh
靈潭陂,ling tham pi
鷺洲,loo tsiu
鹽埕埔,iam tiann poo
灣里街,uan li ke
蠻蠻,ban ban
丁,ting
九,kau
人,jin
刁,tiau
卜,oh
上官,siong kuan
仇,kiu
仇,siu
元,guan
公羊,kong iong
公孫,kong sun
孔,khong
尤,iu
尹,un
巴,a
戈,ko
戶,hoo
文,bun
方,ng
毛,moo
水,tsui
牛,gu
王,ong
丘,khu
令狐,ling hoo
包,au
古,koo
史,su
右,iu
司,su
司馬,su ma
左,tso
玉,giok
甘,kam
田,tian
申,sin
白,eh
皮,hue
石,tsioh
任,jim
伍,ngoo
伏,hok
匡,khong
吉,kiat
安,an
年,lian
成,tshiann
朱,tsu
江,kang
池,ti
牟,boo
米,bi
羊,iunn
何,ho
佘,sia
余,u
佟,tong
冷,ling
吳,ngoo
呂,li
宋,song
巫,bu
李,li
杜,too
步,oo
汪,ong
沈,sim
沙,sua
狄,tik
谷,kok
貝,ue
辛,sin
辰,sin
阮,ng
卓,toh
周,tsiu
孟,bing
季,kui
尚,siong
岳,gak
房,ang
服,hok
杭,hang
林,lim
果,ko
東方,tong hong
武,bu
狐,hoo
竺,tiok
花,hua
虎,hoo
邱,khu
邵,sio
金,kim
侯,hau
俞,ju
南,lam
南宮,lam kiong
城,siann
姚,iau
姜,khiong
宣,suan
宦,huan
封,hong
施,si
查,tsa
柯,kua
柳,liu
段,tuan
洪,ang
皇,hong
皇甫,hong hu
紀,ki
紅,hong
胡,oo
苗,biau
苻,hu
范,huan
范姜,huan kiong
計,ke
風,hong
倪,ge
凌,ling
原,guan
唐,tng
夏,he
奚,he
姬,ki
夏侯,ha hoo
孫,sun
展,tian
徐,tshi
晁,tiau
晉,tsin
晏,an
柴,tsha
桂,kui
桑,song
殷,un
海,hai
涂,thoo
烏,oo
祝,tsiok
秦,tsin
翁,ang
耿,king
荀,sun
袁,uan
郝,hok
馬,ma
高,ko
區,oo
商,siong
國,kok
婁,loo
寇,khoo
尉遲,ut ti
屠,too
崔,tshui
常,siong
康,khng
庾,ju
張,tiunn
張李,tiunn li
張許,tiunn khoo
張廖,tiunn liau
張簡,tiunn kan
戚,tshik
扈,hoo
曹,tso
梁,niu
梅,mui
畢,it
盛,sing
章,tsiunn
符,hu
莊,tsng
莫,boh
許,khoo
逢,hong
連,lian
郭,kueh
陳,tan
陶,to
陸,liok
陳廖,tan liau
魚,hi
鹿,lok
麥,beh
傅,oo
喬,kiau
彭,henn
智,ti
曾,tsan
游,iu
湯,thng
焦,ta
程,thiann
童,tang
華,hua
費,hui
賀,ho
辜,koo
閔,bin
陽,iunn
項,hang
馮,ang
黃,ng
楊,iunn
楚,tshoo
溫,un
萬,ban
葉,iap
葛,kat
董,tang
虞,gu
詹,tsiam
路,loo
鄒,tsau
鄔,oo
雷,lui
靳,kin
廖,liau
熊,him
甄,tsin
端木,tuan bok
翟,tik
聞,bun
臧,tsong
裴,ue
褚,thu
趙,tio
劉,lau
厲,le
慕容,boo iong
樂,gak
樊,huan
樓,lau
歐,au
潘,huann
歐陽,au iong
練,lian
蔡,tshua
蔣,tsiunn
衛,ue
諸葛,tsu kat
鄧,ting
鄭,tenn
魯,loo
黎,le
燕,ian
盧,loo
穆,bok
蕭,siau
賴,lua
遲,ti
錢,tsinn
閻,giam
霍,hok
駱,loh
鮑,au
龍,ling
嶽,gak
應,ing
戴,te
薄,ok
薛,sih
謝,tsia
鍾,tsing
韓,han
瞿,khu
簡,kan
聶,liap
藍,na
豐,hong
闕,khuat
顏,gan
魏,gui
羅,lo
譚,tham
關,kuan
龐,ang
嚴,giam
竇,too
藺,lin
蘇,soo
釋,sik
鐘,tsing
饒,jiau
酆,hong
鐵,thih
顧,koo
龔,king"""


    main(TL)