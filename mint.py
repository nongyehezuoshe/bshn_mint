#! /usr/bin/env python3
import os,random,math,hashlib,sys,sqlite3,time,base64,png,json,sqlite3,subprocess,requests
from PIL import Image,ImageFilter,ImageDraw,ImageFont
requests.packages.urllib3.disable_warnings()

maindata={
	"meta_name":"BSH Number",
	"meta_collection_name":"BSH Number Series NFTs",
	"meta_collection_id":"d8592369-745e-49a5-8c61-324416bcbaa6",
	"git_repo":"nongyehezuoshe/bshn", 
	"f":"1730953628",
	"i":"3",
	"ra":"",
	"ta":"",
	"nft-key":"",

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

bsh_trans_options={
	"defaultstart":0,
	"start":"",
	"wallet_id":"5",
	"to_address":"",
	"headers":{'Content-Type': 'application/json','Accept': 'application/json'},
	"cert":('/root/.chia/mainnet/config/ssl/wallet/private_wallet.crt', '/root/.chia/mainnet/config/ssl/wallet/private_wallet.key'),
	"data":[],
	"xch":[],
	"sellprice":10000
}

nft_trans_options={
	"ta":""
}

def tool_print(line,text):
	print("\033[7;31;47m"+str(line)+" \033[0m",text)

def get_nft_latest():
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

def get_nft_airdropaddr():
	conn = sqlite3.connect('bshn.db')
	cur = conn.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS addr (addr_xch varchar(1000), addr_number INTEGER);""")
	cur.execute("SELECT * FROM addr") 
	_get=cur.fetchall()
	conn.commit()
	cur.close()
	conn.close()
	if(len(_get)==0):
		return False
	_id=random.randint(0,len(_get)-1)
	return _get[_id]

# =========================================

# =====listen BSH transfer=================
def get_bsh_trans():
	def sql_read_start():
		conn = sqlite3.connect('bshn.db')
		cur = conn.cursor()
		cur.execute("""CREATE TABLE IF NOT EXISTS start (trans_start INTEGER);""")
		cur.execute("""select * from start limit 1""")
		_return=""
		_get=cur.fetchall()
		if len(_get)==0:
			cur.execute("""INSERT INTO start VALUES(?);""",(bsh_trans_options["defaultstart"],))
			conn.commit()
			cur.close()
			conn.close()
			_return=bsh_trans_options["defaultstart"]
		else:
			conn.commit()
			cur.close()
			conn.close()
			_return=_get[0][0]
		tool_print(str(sys._getframe().f_lineno)+" "+"get transactions from",_return)
		return _return

	def sql_write_start(start):
		conn = sqlite3.connect('bshn.db')
		cur = conn.cursor()
		cur.execute("""UPDATE start SET trans_start= (?) limit 1;""",(int(start),))
		conn.commit()
		cur.close()
		conn.close()

	def sql_write_addr(addrxch,num):
		conn = sqlite3.connect('bshn.db')
		cur = conn.cursor()
		cur.execute("""CREATE TABLE IF NOT EXISTS addr (addr_xch varchar(1000), addr_number INTEGER);""")
		cur.execute("""INSERT INTO addr VALUES(?,?);""",(addrxch,int(num/bsh_trans_options["sellprice"])))
		conn.commit()
		cur.close()
		conn.close()

	def sql_write_coin(addrxch,coin,amount,time):
		conn = sqlite3.connect('bshn.db')
		cur = conn.cursor()
		cur.execute("""CREATE TABLE IF NOT EXISTS coin (xch varchar(1000), coin varchar(1000), amount INTEGER, time INTEGER);""")
		cur.execute("""INSERT INTO coin VALUES(?,?,?,?);""",(addrxch,coin,amount,time))
		conn.commit()
		cur.close()
		conn.close()

	def get_transactions():
		url = "https://localhost:9256/get_transactions"
		data = '{"wallet_id":'+bsh_trans_options["wallet_id"]+', "start":'+str(bsh_trans_options['start'])+', "end":'+str(bsh_trans_options['start']+1)+',"reverse":false}'
		req=requests.post(url, data=data, headers=bsh_trans_options['headers'], cert=bsh_trans_options['cert'], verify=False).text
		response=json.loads(req)
		print(json.dumps(response, indent=4, sort_keys=True))
		if response["success"] and len(response["transactions"])>0:
			_conf=response["transactions"][0]
			_amount=int(_conf["amount"]/1000)
			_address=_conf["to_address"]
			_time=_conf["created_at_time"]
			_coin=_conf["name"]
			_height=_conf["confirmed_at_height"]

			tool_print(str(sys._getframe().f_lineno)+" " +"amount",_amount)
			tool_print(str(sys._getframe().f_lineno)+" " +"to_address",_address)
			tool_print(str(sys._getframe().f_lineno)+" " +"created_at_time",_time)
			tool_print(str(sys._getframe().f_lineno)+" " +"name",_coin)

			if _address==bsh_trans_options["to_address"]:
				_xch=get_xch(_coin)
				bsh_trans_options["data"].append([_xch,_coin,_amount])
				sql_write_addr(_xch,_amount)
				sql_write_coin(_xch,_coin,_amount,_time)

			bsh_trans_options['start']+=1
			sql_write_start(bsh_trans_options['start'])
			return True
		else:
			return False

	def get_xch(coinname):
		while True:
			r = requests.get("https://api2.spacescan.io/1/xch/coin/"+str(coinname))
			if r.status_code==200:
				r=r.json()
				print(r)
				if r['status']=="success" and r["coin"]:
					while True:
						tool_print(sys._getframe().f_lineno,r["coin"]["from_puzzle_hash"])
						_sub=subprocess.run(['cdv', 'encode', r["coin"]["from_puzzle_hash"]],capture_output=True,text=True)
						if _sub.returncode==0:
							_xch=_sub.stdout.strip()
							tool_print(sys._getframe().f_lineno,_xch)
							bsh_trans_options['xch'].append([_xch,coinname])
							return _xch
						time.sleep(2)
					break
				else:
					time.sleep(500)
			else:
				time.sleep(10)
				continue

	def get_all_trans():
		bsh_trans_options["start"]=sql_read_start()
		while True:
			if get_transactions():
				time.sleep(1)
				continue
			else:
				break
	get_all_trans()

# =====check local nfts before start========
def trans_allnfts():
	def nft_trans(id):
		while True:
			tool_print(sys._getframe().f_lineno,"transfer begain")
			_sub=subprocess.run(['chia', 'wallet', 'nft', 'transfer', '-f', maindata["f"], '-i', maindata["i"], '-ni',id[1],"-ta",nft_trans_options["ta"]],capture_output=True,text=True)
			if _sub.returncode==0:
				_out=_sub.stdout.split("\n")
				for i in range(0,len(_out)):
					if "NFT transferred successfully" in _out[i]:
						tool_print(sys._getframe().f_lineno,"transfer done")
						return True
			time.sleep(5)

	while True:
		_current_nft=get_nft_latest()
		if _current_nft[1]!="NONE":
			nft_trans(_current_nft)
			while True:
				_check_nft=get_nft_latest()
				if _current_nft[0]!=_check_nft[0]:
					tool_print(sys._getframe().f_lineno,"!")
					_current_nft=_check_nft
					break
				else:
					tool_print(sys._getframe().f_lineno,"=")
					time.sleep(5)
		else:
			break

# =====generate image and mint nft==========
def set_nft_img():
	def img_load():
		_style=img_set_style()
		return Image.open("base_img/base_a/base_"+_style+".png").convert("RGBA")
	def img_save(loadedimg):
		if not os.path.exists("tmp"):
			os.makedirs("tmp")
		loadedimg.save("tmp/nft.png")

	def img_set_style():
		path = "base_img/base_a/"
		files= os.listdir(path)
		for file in files:
			if not file.endswith(".png"):
				files.remove(file)
		_index=random.randint(0,len(files)-1)
		_style=files[_index][5:-4]
		maindata["style"]=_style
		tool_print(str(sys._getframe().f_lineno)+" "+"Style",_style)
		return(_style)

	def img_set_material():
		_randnum=random.randint(1,100)
		_type=""
		if _randnum<11:
			_type=0
		elif _randnum>10 and _randnum<41:
			_type=1
		elif _randnum>40:
			_type=2

		_material=["Gold","Silver","Copper"]
		_value=_material[_type]
		maindata["material"]=_value
		tool_print(str(sys._getframe().f_lineno)+" "+"Material",_value)
		return _value

	def img_set_randcolor(loadedimg):
		def pick_color(loadedimg):
			loadedimg=loadedimg.load()
			_color=[]
			_pos=[(2259,1324),(1981,1237),(2535,1219),(2089,2024),(2066,2109),(1895,2217),(1978,2240),(2177,2128),(2031,2286),(2427,2925),(2474,3060),(2490,3283),(1895,3347),(1997,3361),(2165,3311),(2382,3585),(2267,3422),(2344,3471),(1762,3334),(1220,3589),(1442,3577),(1516,3667),(1581,3758),(1787,3798),(2001,3833),(3301,3511),(3166,3201),(2616,2307)]
			for p in range(0,len(_pos),1):
				_the_color=loadedimg[_pos[p][0],_pos[p][1]]
				if _the_color not in _color:
					_color.append(_the_color)
			return _color

		def get_random_color():
			return(random.randint(0,255),random.randint(0,255),random.randint(0,255),255)

		_color_picked=pick_color(loadedimg)
		_color=[]
		for c in range(len(_color_picked)):
			_color.append(get_random_color());

		_pix_img=loadedimg.load()
		maindata["color"]=_color
		tool_print(str(sys._getframe().f_lineno)+" "+"Color",str(_color))
		for x in range(loadedimg.size[0]):
			for y in range(loadedimg.size[1]):
				if math.sqrt(pow((abs(x)-2427),2)+pow((abs(y)-2427-300),2))>2427-16-800:
					_pix_img[x, y] = (0, 0, 0, 0)
					continue
				for z in range(0,len(_color_picked),1):
					if _pix_img[x, y] ==  _color_picked[z]:
						_pix_img[x, y] = _color[z]
						continue
		return loadedimg

	def img_set_bg(loadedimg):
		img_set_material()
		_bg=Image.open("base_img/bg_"+maindata["material"].lower()+".png").convert('RGBA')
		_bg.paste(loadedimg,(0,-300),loadedimg)
		return _bg

	def img_set_bgcolor(loadedimg):
		_color=(random.randint(0,255),random.randint(0,255),random.randint(0,255),32)
		_img_bg=Image.new(mode='RGBA', size=(4854, 4854), color=_color)
		_img_bg.paste(img,(0,0),img)
		maindata["backgroundcolor"]=_color
		tool_print(str(sys._getframe().f_lineno)+" "+"BackgroundColor",str(_color))
		return _img_bg

	def img_set_num(loadedimg):
		def text_border(draw,text, x, y, font, shadowcolor, fillcolor):
			_fillcolor={
				"Gold":(214,170,83,255),
				"Silver":(173,175,187,255),
				"Copper":(245,235,208,255)
			}
			draw.text((x - 1, y), text, font=font, fill=shadowcolor)
			draw.text((x + 1, y), text, font=font, fill=shadowcolor)
			draw.text((x, y - 1), text, font=font, fill=shadowcolor)
			draw.text((x, y + 1), text, font=font, fill=shadowcolor)
			draw.text((x - 1, y - 1), text, font=font, fill=shadowcolor)
			draw.text((x + 1, y - 1), text, font=font, fill=shadowcolor)
			draw.text((x - 1, y + 1), text, font=font, fill=shadowcolor)
			draw.text((x + 1, y + 1), text, font=font, fill=shadowcolor)
			draw.text((x, y), text, font=font, fill=_fillcolor[maindata["material"]])

		def num_check(text):
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

		def num_generate():
			text=str(random.randint(1,100000))
			if num_check(text):
				tool_print(str(sys._getframe().f_lineno)+" "+"Number",text)
				return text
			else:
				return num_generate()

		_text=num_generate()
		maindata["number"]=_text
		_len=len(_text)
		while _len<6:
			_text="0"+_text
			_len=_len+1
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 224)
		text_border(draw,"No."+_text,1725+100, 3600+50+25,font,(255,255,255,255),(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
		return img

	def img_set_text():
		def img_set_words():
			_words=["梦想注定是孤独的旅程，路上少不了质疑和嘲笑，但是那又怎么样，哪怕遍体鳞伤也要勇敢直前。有梦别怕痛，想赢别喊停！Chia的未来不是梦，XCH每枚10万美金。","XCH每枚10万美金，大家都共识起来，让全世界的都知道吧。","不过我还不清楚到底奇亚公司发币流程，我觉得 xch 10万美金一枚是板上钉钉的事情。","我说过xch不到10万我不改。","就像前后几天我设定的140买1个，126买1个，113.4买2个，102.06买4个，91.85买8个，82.66买16个，74.4买32个，这次主力砸到了82.66，一共买到32个，总投资是3200u，只要不贪，这次反弹到102到11之间全部卖了就赚了百分之六左右，那么可以全部卖出，再重新开局。 百分之6就可以完成全年百分之30的5分之一。","下蹲就是为了下一次涨的更高。","这个世界上从来没有一劳永逸的努力，就如没有不劳而获的成功，要想一生过得顺遂，除了一直努力，别无捷径。","未来十万美金一枚，现在70,150,500,2500，买的都是横线一条而已。","坚持很难，放弃可以接着怎么舒服怎么来，但是你会失去你的初中，坚持的过程很痛苦，但是熬过去了会比任何人都要轻松。生活至残酷的，显示是骨感的，生活往往把你逼得无路可退，你需要做的就是逆风翻盘。Chia的未来不是梦。","13年前巴菲特18亿港币买入比亚迪，如今价值670亿港币。巴菲特2008年18亿港币在8元买了2.25亿股一直拿着，现在港股297港币翻了37倍，A股价306元。","群里每人买好1000个XCH以后，大家都出去让你熟悉的亲戚朋友每人都买上100个XCH，大家都出去工作了，这样我们这个群就没有人说话了。","心清明，保持略带发力的紧张； 人踏实，执着坚定肯承载，能抚平，坚信： 世上最正确的事是经过一番努力， 所有的东西会慢慢变成想要的样子。 奇亚的未来不是梦","如果我现在有一个亿，我要全部投资奇亚公司当个小股东。","不需要那么多，500个xch就够了。你会发现，人这一辈子，根本不需要那么多钱。","xch2本身没有风险。xch最大的风险在于，你以为有风险，可能拿不住。","xch涨不需要分析原因。太阳的升起，并不是因为鸡鸣。","几年后再看xch的k线，整个2021年就是一条直线而已。","一个认知，xch没有庄。有人自以为能坐庄。拉上去出完货，上不来了。","上线交易所不是xch的利好。xch上线交易所是交易所的利好。","我并不觉得ETH会成为xch的对手，超越ETH这样的目标，对xch来说显得太小。","未来，你会发现你根本不在乎生活品质，持xch在手就是最高生活品质。","拿出一把车钥匙，不如打开微信，你看，我在xch群。","xch 100的时候看200算什么本事，80块的时候看1万，才是大格局。","各位都是xch币侯，以后持有100个xch就和现在拿着100个ETH一样爽。","我们一定要熬过这3厘米， 我们一定要登上巅峰。 XCH一定会到10万美元一个。 你手里一定要有1000个XCH 。","现在可以入手XCH了，计划把资金分成3批，1:买上1000个等10万美金一个卖，分批买入，这1000个的XCH相当于在银行存死期了。2:分批买入500个，这个当活期理财，有急用钱的时候可以卖这500个，当然我觉得我对这笔钱可能永远用不到了。3:现在再卖一些币圈资产抄XCH，用我的战法每跌百分之10分批买一次（1 1 2 4 6 8 16 32 64 128 256 512 1024），每次买入的总资金有赚百分之6左右就坚决卖掉，再重新开局。我希望我这3不在奇亚路上能有所作为。","社区成员跟十万哥说：“现在chia社区到处是你的传说。”十万哥回复：“10万美金一个XCH很多人心里想要，我只是帮大家说出来而已。至于这个传说也是奇亚社区认可了以前的游击战是不行的，必须把所有可以联合的力量联合起来，奇亚才有未来。”"]
			_get=base64.b64encode(_words[random.randint(0,len(_words)-1)].encode("utf-8")).decode('utf-8')
			tool_print(str(sys._getframe().f_lineno)+" "+"Words",_get)
			maindata["words"]=_get
			return _get

		def img_set_time():
			_time=int(time.time())
			tool_print(str(sys._getframe().f_lineno)+" "+"Timestamp",str(_time))
			maindata["time"]=_time
			return _time

		_num=maindata["number"]
		_material=maindata["material"]
		_style=maindata["style"]
		_bgcolor=maindata["backgroundcolor"]
		_time=img_set_time()

		_words=img_set_words()
		_color=maindata["color"]

		chunk_list = list(png.Reader(filename="tmp/nft.png").chunks())
		chunk_item = tuple([b'tEXt', (" Inserted message<< "+"Number:"+str(_num)+" || Material:"+_material+" || Style:"+str(_style)+" || BackgroundColor:"+str(_bgcolor)+" || Timestamp:"+str(_time)+" || Words:"+str(_words)+" || Color:"+str(_color)+" >>Insert ended ").encode()])
		chunk_list.insert(1, chunk_item)

		with open("tmp/nft.png", 'wb') as dst_file:
			png.write_chunks(dst_file, chunk_list)

	def img_move():
		def get_local():
			_time=time.localtime(int(maindata["time"]))
			_dir=""
			for i in range(0,3):
				_dir=_dir+str(_time[i])
			if not os.path.exists("nft/"+_dir):
				os.makedirs("nft/"+_dir)
			if not os.path.exists("meta/"+_dir):
				os.makedirs("meta/"+_dir)
			maindata["local"]=_dir
			tool_print(str(sys._getframe().f_lineno)+" "+"local",_dir)
			return (_dir)

		def get_hash(url):
			with open(url,'rb') as f:
				sha1obj = hashlib.sha256()
				sha1obj.update(f.read())
				_hash = sha1obj.hexdigest()
				maindata["hash"]=_hash
				tool_print(str(sys._getframe().f_lineno)+" "+"hash",_hash)
				return _hash

		_local=get_local()
		_hash=get_hash("tmp/nft.png")
		subprocess.run(["mv","tmp/nft.png","nft/"+_local+"/"+_hash+".png"],capture_output=True,text=True)

	img=img_load()
	img=img_set_randcolor(img)
	img=img_set_bg(img)
	img=img_set_num(img)
	img=img_set_bgcolor(img)
	img_save(img)
	img_set_text()
	img_move()

def set_nft_meta():
	def get_id():
		conn = sqlite3.connect('bshn.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM bshn") 
		_get=cur.fetchall()
		conn.commit()
		cur.close()
		conn.close()
		_id=len(_get)+1
		maindata["id"]=_id
		tool_print(str(sys._getframe().f_lineno)+" "+"ID",str(_id))
		return _id

	def get_hash(url):
		with open(url,'rb') as f:
			sha1obj = hashlib.sha256()
			sha1obj.update(f.read())
			_hash = sha1obj.hexdigest()
			maindata["hashmeta"]=_hash
			tool_print(str(sys._getframe().f_lineno)+" "+"hashmeta",_hash)
			return _hash

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

	metadata["name"]=metadata["name"]+" #"+base64.b64encode(str(get_id()).encode("utf-8")).decode('utf-8')

	metadata_attr=[]
	_attr_type=["Number","Material","Style"]
	for i in _attr_type:
		_attr={}
		_attr["trait_type"]=i
		if i=="Number":
			_attr["value"]=maindata["number"]
		elif i=="Style":
			_attr["value"]=maindata["style"]
		elif i=="Material":
			_attr["value"]=maindata["material"]
		metadata_attr.append(_attr)

	metadata["attributes"]=metadata_attr
	with open("tmp/meta.json", "w") as outfile: 
		json.dump(metadata, outfile, indent=4, separators=(',', ': '))
	
	_hashmeta=get_hash("tmp/meta.json")
	subprocess.run(["mv","tmp/meta.json","meta/"+maindata["local"]+"/"+_hashmeta+".json"],capture_output=True,text=True)
	return metadata

def set_nft_upload():
	def upload_img():
		url="https://api.nft.storage/upload/"
		files={'file':("nft/"+maindata["local"]+"/"+maindata["hash"]+".png",open("nft/"+maindata["local"]+"/"+maindata["hash"]+".png",'rb'),"image/png")}
		headers = {'accept': 'application/json', 'Authorization': 'Bearer '+maindata["nft-key"]}

		tool_print(str(sys._getframe().f_lineno)+" "+"uploading img","...")
		_flag=1
		while True:
			try:
				r = requests.post(url, files=files, headers=headers)
				if r.status_code==200:
					maindata["nftcid"]=r.json()["value"]["cid"]
					tool_print(str(sys._getframe().f_lineno)+" "+"metacid",maindata["nftcid"])
					break
				else:
					tool_print(sys._getframe().f_lineno,r.status_code)
					_flag=_flag+1
					time.sleep(5)
					continue
			except Exception as e:
				tool_print(sys._getframe().f_lineno,str(e))
				time.sleep(30)
				continue

	def upload_meta():
		url="https://api.nft.storage/upload/"
		files={'file':("meta/"+maindata["local"]+"/"+maindata["hashmeta"]+".json",open("meta/"+maindata["local"]+"/"+maindata["hashmeta"]+".json",'rb'),"application/json")}
		headers = {'accept': 'application/json', 'Authorization': 'Bearer '+maindata["nft-key"]}

		tool_print(str(sys._getframe().f_lineno)+" "+"uploading meta","...")
		_flag=1
		while True:
			try:
				r = requests.post(url, files=files, headers=headers)
				if r.status_code==200:
					maindata["metacid"]=r.json()["value"]["cid"]
					tool_print(str(sys._getframe().f_lineno)+" "+"metacid",maindata["metacid"])
					break
				else:
					tool_print(sys._getframe().f_lineno,r.status_code)
					_flag=_flag+1
					time.sleep(5)
			except Exception as e:
				tool_print(sys._getframe().f_lineno,str(e))
				time.sleep(30)
				continue

	upload_img()
	time.sleep(5)
	upload_meta()

def set_nft_mint():
	def mint_new():
		tool_print(str(sys._getframe().f_lineno)+" "+"minting","...")
		_current_addr=get_nft_airdropaddr()
		_f=maindata["f"]
		_i=maindata["i"]
		_ra=maindata["ra"]
		_ta=maindata["ta"]
		_u="https://"+maindata["nftcid"]+".ipfs.nftstorage.link/"+"nft/"+maindata["local"]+"/"+maindata["hash"]+".png"+","+"https://github.com/"+maindata["git_repo"]+"/raw/main/nft/"+maindata["local"]+"/"+maindata["hash"]+".png"
		_nh=maindata["hash"]
		_mu="https://"+maindata["metacid"]+".ipfs.nftstorage.link/"+"meta/"+maindata["local"]+"/"+maindata["hashmeta"]+".json"+","+"https://github.com/"+maindata["git_repo"]+"/raw/main/meta/"+maindata["local"]+"/"+maindata["hashmeta"]+".json"
		_mh=maindata["hashmeta"]

		while True:
			_mint=subprocess.run(['chia', 'wallet', 'nft', 'mint', '-f', _f, '-i', _i, '-ra', _ra, '-ta', _ta, '-u', _u, '-nh', _nh, '-mu', _mu, '-mh', _mh, '-rp', '1', '-m', '0'],capture_output=True,text=True)
			# print(_mint.stdout.split("\n"))
			if _mint.returncode==0:
				_out=_mint.stdout.split("\n")
				for i in range(0,len(_out)):
					if "NFT minted Successfully" in _out[i]:
						maindata["nftaddr"]=_current_addr[0]
						maindata["current_addr"]=_current_addr
						tool_print(str(sys._getframe().f_lineno)+" "+"mint new" ,"NFT minted Successfully")
						return True
			time.sleep(2)

	def mint_check():
		while True:
			_current_nft=get_nft_latest()
			if _current_nft[0]!="NONE" and maindata["nftid"][0]!=_current_nft[0]:
				tool_print(str(sys._getframe().f_lineno)+" "+"mint checking" ,"!=, last:"+str(maindata["nftid"][0])+" || current:"+str(_current_nft[0]))
				maindata["nftid"]=_current_nft
				return True
			else:
				tool_print(str(sys._getframe().f_lineno)+" "+"mint checking" ,"==, last:"+str(maindata["nftid"][0])+" || current:"+str(_current_nft[0]))
				time.sleep(10)

	def mint_trans():
		while True:
			_sub=subprocess.run(['chia', 'wallet', 'nft', 'transfer', '-f', maindata["f"], '-i', maindata["i"], '-ni',maindata["nftid"][1],"-ta",maindata["current_addr"][0]],capture_output=True,text=True)
			# tool_print(sys._getframe().f_lineno,_sub.returncode)
			if _sub.returncode==0:
				_out=_sub.stdout.split("\n")
				for i in range(0,len(_out)):
					if "NFT transferred successfully" in _out[i]:
						tool_print(str(sys._getframe().f_lineno)+" "+"mint transfer" ,"NFT transferred successfully")
						return True
			time.sleep(5)

	mint_new()
	mint_check()
	mint_trans()

def set_nft_sql():
	tool_print(str(sys._getframe().f_lineno)+" "+"writing database" ,"...")
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

	_catch=['888', '8888', '88888', '666', '6666', '66666', '12345', '54321', '100', '1000', '10000', '100000','1','65535']
	if int(maindata["number"])<100 or int(maindata["number"]) in _catch:
		with open("numcatch","a") as f:
			f.writelines("\nnumber:"+str(maindata["number"])+" nftid:"+str(maindata["nftid"][0]+" nftaddr:"+str(maindata["nftaddr"])))

def set_nft_git():
	_sub_add=subprocess.run(['git', 'add', 'meta', 'nft'])
	_sub_commit=subprocess.run(['git', 'commit', '-am', 'mint_upload'])
	_sub_push=subprocess.run(['git', 'push'])

def set_nft():
	set_nft_img()
	set_nft_meta()
	set_nft_upload()
	set_nft_mint()
	set_nft_sql()
	set_nft_git()

if __name__ == "__main__":
	if get_nft_latest()[0]!="NONE":
		trans_allnfts()

	while True:
		if(get_nft_airdropaddr()):
			while get_nft_airdropaddr():
				set_nft()
		get_bsh_trans()
		tool_print(str(sys._getframe().f_lineno)+" "+"wating transfer" ,"...")
		time.sleep(60)