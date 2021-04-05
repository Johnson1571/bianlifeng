import requests
import json


url = "https://api.blibee.com/product-api/product/search/promotion/list/v3"


headers = {
    "Host" : "api.blibee.com",
    "Connection" : "keep-alive",
    "Content-Length" : "82",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "content-type" : "application/json",
    "Referer" : "https://servicewechat.com/wxc27d6f27afe85d61/663/page-frame.html",
    "Accept-Encoding" : "gzip, deflate, br"
}

ServerJ_Session = os.environ['Session']
shopCode = os.environ['ShopCode']

def main():
	mk = ""
	data = {"page":{"pageSize":100,"pageNo":1},"shopCode":shopCode,"categoryUserCodes":[]}
	response = requests.post(url=url, data=json.dumps(data), headers=headers ,timeout=10).text
	res = json.loads(response)
	try:
		for i in res["data"]["items"]:
			for j in i["products"]["data"]:
				if j['price'] / j['originPrice'] <= 0.69:
					mk += convertMarkdown(j)
		sendServerJ(mk,ServerJ_Session)
	except Exception as e:
		print(e)

def convertMarkdown(res):
	mkdown = "### " + res['productName'] + "\n"
	mkdown += "![{0}]({1})".format(res['productName'],res['headImageUrl']) + "\n"
	mkdown += res['promotionTag'][0] + "\n" 
	mkdown += " 原价" + str(res['originPrice']) + "\n" 
	mkdown += " 现价" + str(res['price']) + "\n\n"
	return mkdown

def sendServerJ(res,session):
	data={
		'text': "便利蜂优惠", 
		'desp': res
	}
	url = "https://sc.ftqq.com/{0}.send".format(session)
	requests.post(url=url,data=data,timeout=10)


if __name__ == '__main__':
	main()

