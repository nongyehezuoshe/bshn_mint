#! /usr/bin/env python3

import os,random,math,hashlib,sys,sqlite3,time,base64,png,json,sqlite3,subprocess,requests
from PIL import Image,ImageFilter,ImageDraw,ImageFont

maindata={
	"meta_name":"BSH Number",
	"meta_collection_name":"BSH Number Series NFTs",
	"meta_collection_id":"3a6a97e4-7ee2-4e83-bdd2-bcd2f0d7ddb9",
	"git_repo":"nongyehezuoshe/bshn",
	"f":"1730953628",
	"i":"3",
	"ra":"xch17rxqgvq3ffpmfctt8x8etspu8z36v6807du9uhcgp7e75h9fev7qsf4xrd",
	"ta":"xch1rd70g60z4evue390h9chjdsq9f6uqx79h397pf5l3h63r9twwf9q5lf0d9",
	"nft-key":"",# get from nft.storage
	"number":"",
	"material":"",
	"style":"",
	"color":"NONE",
	"words":"",
	"time":"",
	"hash":"",
	"hashmeta":"",
	"nftid":["NONE","NONE"],
	"nftaddr":"NONE",
	"local":"NONE",
	"id":"NONE",
	"mint":"NONE",
	"last_nft":"NONE",
	"current_addr":["NONE",0],
	"nftcid":"NONE",
	"metacid":"NONE",
	"backgroundcolor":"NONE"
}

def get_maindata():
	def get_number():
		# text=str(random.randint(1,100000))
		text="8"
		if sql_check_num(text):
			tool_print(sys._getframe().f_lineno,"Number: "+text)
			return text
		else:
			return get_number()

	def get_material():
		_randnum=random.randint(1,100)
		_type=""
		if _randnum<11:
			_type=0
		elif _randnum>10 and _randnum<41:
			_type=1
		elif _randnum>40:
			_type=2

		# _type=0
		_material=["Gold","Silver","Copper"]
		tool_print(sys._getframe().f_lineno,"Material: "+_material[_type])
		return _material[_type]


	def get_style():
		path = "base_img/base_a/"
		files= os.listdir(path)
		for file in files:
			if not file.endswith(".png"):
				files.remove(file)
		_index=random.randint(0,len(files)-1)
		tool_print(sys._getframe().f_lineno,"Style: "+files[_index][5:-4])
		return(files[_index][5:-4])

	def get_words():
		_words=["梦想注定是孤独的旅程，路上少不了质疑和嘲笑，但是那又怎么样，哪怕遍体鳞伤也要勇敢直前。有梦别怕痛，想赢别喊停！Chia的未来不是梦，XCH每枚10万美金。","XCH每枚10万美金，大家都共识起来，让全世界的都知道吧。","不过我还不清楚到底奇亚公司发币流程，我觉得 xch 10万美金一枚是板上钉钉的事情。","我说过xch不到10万我不改。","就像前后几天我设定的140买1个，126买1个，113.4买2个，102.06买4个，91.85买8个，82.66买16个，74.4买32个，这次主力砸到了82.66，一共买到32个，总投资是3200u，只要不贪，这次反弹到102到11之间全部卖了就赚了百分之六左右，那么可以全部卖出，再重新开局。 百分之6就可以完成全年百分之30的5分之一。","下蹲就是为了下一次涨的更高。","这个世界上从来没有一劳永逸的努力，就如没有不劳而获的成功，要想一生过得顺遂，除了一直努力，别无捷径。","未来十万美金一枚，现在70,150,500,2500，买的都是横线一条而已。","坚持很难，放弃可以接着怎么舒服怎么来，但是你会失去你的初中，坚持的过程很痛苦，但是熬过去了会比任何人都要轻松。生活至残酷的，显示是骨感的，生活往往把你逼得无路可退，你需要做的就是逆风翻盘。Chia的未来不是梦。","13年前巴菲特18亿港币买入比亚迪，如今价值670亿港币。巴菲特2008年18亿港币在8元买了2.25亿股一直拿着，现在港股297港币翻了37倍，A股价306元。","群里每人买好1000个XCH以后，大家都出去让你熟悉的亲戚朋友每人都买上100个XCH，大家都出去工作了，这样我们这个群就没有人说话了。","心清明，保持略带发力的紧张； 人踏实，执着坚定肯承载，能抚平，坚信： 世上最正确的事是经过一番努力， 所有的东西会慢慢变成想要的样子。 奇亚的未来不是梦","如果我现在有一个亿，我要全部投资奇亚公司当个小股东。","不需要那么多，500个xch就够了。你会发现，人这一辈子，根本不需要那么多钱。","xch2本身没有风险。xch最大的风险在于，你以为有风险，可能拿不住。","xch涨不需要分析原因。太阳的升起，并不是因为鸡鸣。","几年后再看xch的k线，整个2021年就是一条直线而已。","一个认知，xch没有庄。有人自以为能坐庄。拉上去出完货，上不来了。","上线交易所不是xch的利好。xch上线交易所是交易所的利好。","我并不觉得ETH会成为xch的对手，超越ETH这样的目标，对xch来说显得太小。","未来，你会发现你根本不在乎生活品质，持xch在手就是最高生活品质。","拿出一把车钥匙，不如打开微信，你看，我在xch群。","xch 100的时候看200算什么本事，80块的时候看1万，才是大格局。","各位都是xch币侯，以后持有100个xch就和现在拿着100个ETH一样爽。","我们一定要熬过这3厘米， 我们一定要登上巅峰。 XCH一定会到10万美元一个。 你手里一定要有1000个XCH 。","现在可以入手XCH了，计划把资金分成3批，1:买上1000个等10万美金一个卖，分批买入，这1000个的XCH相当于在银行存死期了。2:分批买入500个，这个当活期理财，有急用钱的时候可以卖这500个，当然我觉得我对这笔钱可能永远用不到了。3:现在再卖一些币圈资产抄XCH，用我的战法每跌百分之10分批买一次（1 1 2 4 6 8 16 32 64 128 256 512 1024），每次买入的总资金有赚百分之6左右就坚决卖掉，再重新开局。我希望我这3不在奇亚路上能有所作为。","社区成员跟十万哥说：“现在chia社区到处是你的传说。”十万哥回复：“10万美金一个XCH很多人心里想要，我只是帮大家说出来而已。至于这个传说也是奇亚社区认可了以前的游击战是不行的，必须把所有可以联合的力量联合起来，奇亚才有未来。”"]
		_get=base64.b64encode(_words[random.randint(0,len(_words)-1)].encode("utf-8")).decode('utf-8')
		tool_print(sys._getframe().f_lineno,"Words: "+_get)
		return _get

	def get_time():
		_time=int(time.time())
		tool_print(sys._getframe().f_lineno,"Timestamp: "+str(_time))
		return _time

	def get_local():
		_time=time.localtime(time.time())
		_dir=""
		for i in range(0,3):
			_dir=_dir+str(_time[i])
		if not os.path.exists("nft/"+_dir):
			os.makedirs("nft/"+_dir)
		if not os.path.exists("meta/"+_dir):
			os.makedirs("meta/"+_dir)
		tool_print(sys._getframe().f_lineno,_dir)
		return (_dir)

	def get_id():
		conn = sqlite3.connect('bshn.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM bshn") 
		_get=cur.fetchall()
		conn.commit()
		cur.close()
		conn.close()

		tool_print(sys._getframe().f_lineno,"ID: "+str(len(_get)+1))
		return len(_get)+1

	maindata["number"]=get_number()
	maindata["material"]=get_material()
	maindata["style"]=get_style()
	maindata["words"]=get_words()
	maindata["time"]=get_time()
	maindata["local"]=get_local()
	maindata["id"]=get_id()
	maindata["nftid"]=mint_get_current()


def get_hash(url):
	with open(url,'rb') as f:
		sha1obj = hashlib.sha256()
		sha1obj.update(f.read())
		hash = sha1obj.hexdigest()
		return hash

def img_load(img):
	return Image.open(img).convert("RGBA")

def img_save(img):
	img.save("tmp/nft.png")

# split转换
def tool_img2split():
	img = Image.open("base_img/base.png")
	r,g,b,a=img.split()
	# img0 = Image.merge('RGB',(g,g,b))
	color_split=[r,g,b]

	for x in range(3):
		for y in range(3):
			for z in range(3):
				if x==y and y==z:
					continue
				else:
					img0 = Image.merge('RGB',(color_split[x],color_split[y],color_split[z]))
					img0.save("base_img/base_split/base_"+str(x)+str(y)+str(z)+".png")

# 透明背景
def tool_img2a ():
	path = "base_img/base_split"
	files= os.listdir(path)
	for file in files: 
		if not os.path.isdir(file):
			img = Image.open(path+"/"+file).convert("RGBA")
			pixdata = img.load()
			bgcolor = pixdata[1, 1]
			for x in range(img.size[0]):
				for y in range(img.size[1]):
					if pixdata[x, y] ==  bgcolor:
						pixdata[x, y] = (0,0,0, 0)
			print("done")
			img.save("base_img/base_a/"+file)

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def sql_check_num(text):
	conn = sqlite3.connect('bshn.db')
	cur = conn.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS bshn (bshn_id INTEGER, bshn_number INTEGER, bshn_style INTEGER, bshn_color INTEGER, bshn_time INTEGER, bshn_words varchar(1000), bshn_material INTEGER,bshn_hash varchar(1000),bshn_hashmeta varchar(1000),bshn_nftid varchar(1000),bshn_nftaddr varchar(1000),bshn_local INTEGER,bshn_nftcid varchar(1000),bshn_metacid varchar(1000), bshn_bgcolor INTEGER);""")
	cur.execute("SELECT * FROM bshn WHERE bshn_number="+text) 
	get=cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()

	if len(get)>0:
		return False
	else:
		_len=len(text)
		while _len<6:
			text="0"+text
			_len=_len+1
		return True

def sql_write():
	tool_print(sys._getframe().f_lineno,maindata["current_addr"])
	conn = sqlite3.connect('bshn.db')
	cur = conn.cursor()
	cur.execute("""INSERT INTO bshn VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",(maindata['id'],maindata['number'],str(maindata['style']),str(maindata['color']),str(maindata['time']),maindata['words'],maindata['material'],maindata['hash'],maindata['hashmeta'],maindata['nftid'][0],maindata['nftaddr'],maindata["local"],maindata["nftcid"],maindata["metacid"],str(maindata["backgroundcolor"])))

	if maindata["current_addr"][1]==1:
		cur.execute("""DELETE FROM addr WHERE addr_xch=?;""",(maindata["current_addr"][0],))
	else:
		cur.execute("""UPDATE addr SET addr_number=? WHERE addr_xch=?; """,(int(maindata["current_addr"][1])-1,maindata["current_addr"][0]))

	conn.commit()
	cur.close()
	conn.close()

	_catch=['888', '8888', '88888', '666', '6666', '66666', '12345', '54321', '100', '1000', '10000', '100000']
	if int(maindata["number"])<100 or int(maindata["number"]) in _catch:
		with open("numcatch","a") as f:
			f.writelines("\nnumber:"+str(maindata["number"])+" nftid:"+str(maindata["nftid"][0]+" nftaddr:"+str(maindata["nftaddr"])))

	# with open("numcatch","a") as f:
	# 	f.writelines("\nnumber:"+str(maindata["number"])+" nftid:"+str(maindata["nftid"][0]+" nftaddr:"+str(maindata["nftaddr"])))


def meta_set():
	metadata ={
		"format": "CHIP-0007",
		"name": maindata["meta_name"],
		"description": "100,000 NFTs on Chia, from BSH community.",
		"sensitive_content": False,
		"collection": {
			"name": maindata["meta_collection_name"],
			"id": maindata["meta_collection_id"],
			"attributes": [
				{
					"type": "description",
					"value": "100,000 NFTs on Chia, from BSH community."
				},
				{
					"type": "icon",
					"value": "https://bafybeifryvyui4gshimmxl26uec3ol3kummjnuljb34vt7gl7cgml3hnrq.ipfs.nftstorage.link/icon.png"
				},
				{
					"type": "banner",
					"value": "https://bafybeidejaow2lx2t5usgrd6c5p5pq4kleygb3hihlldq2wianx2fifxru.ipfs.nftstorage.link/banner.png"
				},
				{
					"type": "website",
					"value": "https://brothershiwan.com"
				},
				{
					"type": "twitter",
					"value": "@brothershiwan"
				},
				{
					"type":"discord",
					"value":"https://discord.com/invite/J3qJDWbEYb"
				},
				{
					"type":"did",
					"value":"did:chia:1jaax757admslkd6525xyjwz9hc9zk8xcy52l8gp44lgjyed9mztsc3lp6a"
				}
			]
		},
		"attributes": [],
	}

	metadata["name"]=metadata["name"]+" #"+base64.b64encode(str(maindata["id"]).encode("utf-8")).decode('utf-8')

	metadata_attr=[]
	_attr_type=["Number","Material","Style","Words","Color","Timestamp","BackgroundColor"]
	for i in _attr_type:
		_attr={}
		_attr["trait_type"]=i
		if i=="Number":
			_attr["value"]=maindata["number"]
		elif i=="Color":
			_attr["value"]=maindata["color"]
		elif i=="Timestamp":
			_attr["value"]=maindata["time"]
		elif i=="Words":
			_attr["value"]=maindata["words"]
		elif i=="Style":
			_attr["value"]=maindata["style"]
		elif i=="Material":
			_attr["value"]=maindata["material"]
		elif i=="BackgroundColor":
			_attr["value"]=maindata["backgroundcolor"]
		metadata_attr.append(_attr)

	metadata["attributes"]=metadata_attr
	with open("tmp/meta.json", "w") as outfile: 
		json.dump(metadata, outfile, indent=4, separators=(',', ': '))
	
	hashtext=get_hash("tmp/meta.json")
	subprocess.run(["mv","tmp/meta.json","meta/"+maindata["local"]+"/"+hashtext+".json"],capture_output=True,text=True)
	maindata["hashmeta"]=hashtext
	return metadata

def img_randcolor(img):
	def getColorType(img):
		pixdata = img.load()
		_color=[]
		_pos=[(2259,1324),(1981,1237),(2535,1219),(2089,2024),(2066,2109),(1895,2217),(1978,2240),(2177,2128),(2031,2286),(2427,2925),(2474,3060),(2490,3283),(1895,3347),(1997,3361),(2165,3311),(2382,3585),(2267,3422),(2344,3471),(1762,3334),(1220,3589),(1442,3577),(1516,3667),(1581,3758),(1787,3798),(2001,3833),(3301,3511),(3166,3201),(2616,2307)]
		for p in range(0,len(_pos),1):
			_the_color=pixdata[_pos[p][0],_pos[p][1]]
			if _the_color not in _color:
				_color.append(_the_color)
		return _color

	def getRandomColor():
		return(random.randint(0,255),random.randint(0,255),random.randint(0,255),255)

	color_type=getColorType(img)
	pixdata = img.load()
	_color=[]

	for c in range(len(color_type)):
		_color.append(getRandomColor());

	maindata["color"]=_color
	tool_print(sys._getframe().f_lineno,"Color: "+str(_color))

	for x in range(img.size[0]):
		for y in range(img.size[1]):
			if math.sqrt(pow((abs(x)-2427),2)+pow((abs(y)-2427-300),2))>2427-16-800:
				pixdata[x, y] = (0, 0, 0, 0)
				continue
			for z in range(0,len(color_type),1):
				if pixdata[x, y] ==  color_type[z]:
					pixdata[x, y] = _color[z]
					continue
	return img

def img_num(img):
	def text_border(draw,text, x, y, font, shadowcolor, fillcolor):
		draw.text((x - 1, y), text, font=font, fill=shadowcolor)
		draw.text((x + 1, y), text, font=font, fill=shadowcolor)
		draw.text((x, y - 1), text, font=font, fill=shadowcolor)
		draw.text((x, y + 1), text, font=font, fill=shadowcolor)

		draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
		draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
		draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
		draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)

		draw.text((x, y), text, font=font, fill=fillcolor)

	text=maindata["number"]
	_len=len(text)
	while _len<6:
		text="0"+text
		_len=_len+1
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 224)
	text_border(draw,"No."+text,1725+100, 3600+50+25,font,(255,255,255,128),(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
	return img

def img_paste(img):
	img_coin=Image.open("base_img/bg_"+maindata["material"].lower()+".png").convert('RGBA')
	img_coin.paste(img,(0,-300),img)
	return img_coin

def img_randbgcolor(img):
	_color=(random.randint(0,255),random.randint(0,255),random.randint(0,255),32)
	img_bg=Image.new(mode='RGBA', size=(4854, 4854), color=_color)
	img_bg.paste(img,(0,0),img)
	maindata["backgroundcolor"]=_color
	tool_print(sys._getframe().f_lineno,"BackgroundColor: "+str(_color))
	return img_bg

def img_time(img):
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 128)
	draw.text((1800, 4500), base64.b64encode(str(int(time.time())).encode("utf-8")).decode('utf-8'), font=font,fill=(255,0,0,255))
	return img
 
def img_text():
	chunk_list = list(png.Reader(filename="tmp/nft.png").chunks())
	chunk_item = tuple([b'tEXt', (" Inserted message<< "+str(maindata["words"])+" >>Insert ended ").encode()])
	chunk_list.insert(1, chunk_item)

	with open("tmp/nft.png", 'wb') as dst_file:
		png.write_chunks(dst_file, chunk_list)

def img_set():
	maindata["hash"]=get_hash("tmp/nft.png")
	subprocess.run(["mv","tmp/nft.png","nft/"+maindata["local"]+"/"+maindata["hash"]+".png"],capture_output=True,text=True)

def nft():
	img=img_load("base_img/base_a/base_"+maindata["style"]+".png")
	img=img_randcolor(img)
	img.save("tmp/nft00.png")
	img=img_paste(img)
	img=img_num(img)
	img=img_randbgcolor(img)
	img_save(img)
	img_text()

	img_set()
	meta_set()

	# return

	nft_storage()
	meta_storage()

def nft_storage():
	url="https://api.nft.storage/upload/"
	files={'file':("nft/"+maindata["local"]+"/"+maindata["hash"]+".png",open("nft/"+maindata["local"]+"/"+maindata["hash"]+".png",'rb'),"image/png")}
	headers = {'accept': 'application/json', 'Authorization': 'Bearer '+maindata["nft-key"]}
	r = requests.post(url, files=files, headers=headers)
	maindata["nftcid"]=r.json()["value"]["cid"]

def meta_storage():
	url="https://api.nft.storage/upload/"
	files={'file':("meta/"+maindata["local"]+"/"+maindata["hashmeta"]+".json",open("meta/"+maindata["local"]+"/"+maindata["hashmeta"]+".json",'rb'),"application/json")}
	headers = {'accept': 'application/json', 'Authorization': 'Bearer '+maindata["nft-key"]}
	r = requests.post(url, files=files, headers=headers)
	maindata["metacid"]=r.json()["value"]["cid"]


def get_nft_amount():
	conn = sqlite3.connect('bshn.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM addr") 
	_get=cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()

	_amount=0
	for i in range(0,len(_get)):
		_amount=_amount+int(_get[i][1])
	tool_print(sys._getframe().f_lineno,_amount)
	return _amount

def get_nft_addr():
	conn = sqlite3.connect('bshn.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM addr") 
	_get=cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()

	tool_print(sys._getframe().f_lineno,_get)
	_id=random.randint(0,len(_get)-1)
	return _get[_id]

def mint_new_nft(current_addr):
	tool_print(sys._getframe().f_lineno,current_addr)
	# _ta=current_addr[0]			   # target address
	_f=maindata["f"]
	_i=maindata["i"]
	_ra=maindata["ra"]
	_ta=maindata["ta"]

	_u="https://"+maindata["nftcid"]+".ipfs.nftstorage.link/"+"nft/"+maindata["local"]+"/"+maindata["hash"]+".png"+","+"https://github.com/"+maindata["git_repo"]+"/raw/main/nft/"+maindata["local"]+"/"+maindata["hash"]+".png"
	_nh=maindata["hash"]

	_mu="https://"+maindata["metacid"]+".ipfs.nftstorage.link/"+"meta/"+maindata["local"]+"/"+maindata["hashmeta"]+".json"+","+"https://github.com/"+maindata["git_repo"]+"/raw/main/meta/"+maindata["local"]+"/"+maindata["hashmeta"]+".json"
	_mh=maindata["hashmeta"]

	tool_print(sys._getframe().f_lineno,_u)
	tool_print(sys._getframe().f_lineno,_nh)
	tool_print(sys._getframe().f_lineno,_mu)

	while True:
		_mint=subprocess.run(['chia', 'wallet', 'nft', 'mint', '-f', _f, '-i', _i, '-ra', _ra, '-ta', _ta, '-u', _u, '-nh', _nh, '-mu', _mu, '-mh', _mh, '-rp', '1', '-m', '0'],capture_output=True,text=True)
		print(_mint.stdout.split("\n"))
		if _mint.returncode==0:
			_out=_mint.stdout.split("\n")
			for i in range(0,len(_out)):
				if "NFT minted Successfully" in _out[i]:
					maindata["nftaddr"]=current_addr[0]
					maindata["current_addr"]=current_addr
					return True
		time.sleep(5)


def mint_git():
	# _sub_add=subprocess.run(['git', 'add', 'meta', 'nft'])
	# _sub_commit=subprocess.run(['git', 'commit', '-am', 'mint_upload'])
	# _sub_push=subprocess.run(['git', 'push'])

	while True:
		_sub_add=subprocess.run(['git', 'add', 'meta', 'nft'],capture_output=True,text=True)
		print(_sub_add.stdout.split("\n"))
		if _sub_add.returncode==0:
			_sub_commit=subprocess.run(['git', 'commit', '-am', 'mint_upload'],capture_output=True,text=True)
			print(_sub_commit.stdout.split("\n"))
			if _sub_commit.returncode==0:
				_sub_push=subprocess.run(['git', 'push'],capture_output=True,text=True)
				print(_sub_push.stdout.split("\n"))
				if _sub_push.returncode==0:
					tool_print(sys._getframe().f_lineno,"git push done")
					return
				time.sleep(5)
			time.sleep(5)
		time.sleep(5)


def mint_trans():
	while True:
		tool_print(sys._getframe().f_lineno,maindata["nftid"])
		_sub=subprocess.run(['chia', 'wallet', 'nft', 'transfer', '-f', maindata["f"], '-i', maindata["i"], '-ni',maindata["nftid"][1],"-ta",maindata["current_addr"][0]],capture_output=True,text=True)
		print(_sub.stdout.split("\n"))
		tool_print(sys._getframe().f_lineno,_sub.returncode)
		if _sub.returncode==0:
			_out=_sub.stdout.split("\n")
			for i in range(0,len(_out)):
				if "NFT transferred successfully" in _out[i]:
					return True
		time.sleep(5)

def mint_get_current():
	while True:
		_sub=subprocess.run(['chia', 'wallet', 'nft', 'list', '-f', maindata["f"], '-i', maindata["i"]],capture_output=True,text=True)
		_value=["",""]
		if _sub.returncode==0 :
			_out=_sub.stdout.split("\n")
			for i in range(len(_out)-1,0,-1):
				if "NFT identifier" in _out[i]:
					_value[0]=_out[i].split()[2]
				if "Current NFT coin ID" in _out[i]:
					_value[1]=_out[i].split()[4]
				if _value[0] and _value[1]:
					return _value
			return ["NONE","NONE"]
		time.sleep(5)

def mint_done():
	while True:
		_current_nft=mint_get_current()
		tool_print(sys._getframe().f_lineno,_current_nft[0])
		if _current_nft[0]!="NONE" and maindata["nftid"][0]!=_current_nft[0]:
			tool_print(sys._getframe().f_lineno,maindata["nftid"][0])
			tool_print(sys._getframe().f_lineno,"!=")
			maindata["nftid"]=_current_nft
			mint_trans()
			sql_write()
			mint_git()
			return True
		else:
			tool_print(sys._getframe().f_lineno,maindata["nftid"][0])
			tool_print(sys._getframe().f_lineno,"=")
			time.sleep(10)

def mint_nft(mint_amount):
	tool_print(sys._getframe().f_lineno,"start mint, total: "+str(mint_amount))
	while mint_amount>0:
		tool_print(sys._getframe().f_lineno,"START")
		get_maindata()
		nft()
		mint_new_nft(get_nft_addr())
		mint_done()
		mint_amount=mint_amount-1
		tool_print(sys._getframe().f_lineno,"DONE, left: "+str(mint_amount))
		time.sleep(5)
	return

if __name__ == "__main__":
	mint_nft(get_nft_amount())
	# mint_nft(10)

	# mint_git()
	# nft_storage()
	# meta_storage()
