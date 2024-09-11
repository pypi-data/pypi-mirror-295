import jwt
import requests
import httpx
import asyncio

class Whalegistic:

	def __init__(this, public_key, private_key):
		this.pri_key = private_key;
		this.pub_key = public_key;
		this.token = jwt.encode({ "public_key": public_key }, private_key, algorithm="HS256");
		print(f"TOKEN : {this.token}")



	def getBrands(this, send_obj):

		send_url = "https://whalegistic.com/api/get-brands"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		brands_obj = response.json()

		return brands_obj["brands"]



	def getCategories(this, send_obj):

		send_url = "https://whalegistic.com/api/get-categories"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		categories_obj = response.json()

		return categories_obj["categories"]



	def getCollections(this, send_obj):

		send_url = "https://whalegistic.com/api/get-collections"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		collections_obj = response.json()

		return collections_obj["collections"]



	async def asyncPost(this, url, send_obj, send_headers):
	    async with httpx.AsyncClient() as client:
	        return await client.post(url, json = send_obj, headers = send_headers)


	async def getAsyncStore(this, send_obj):

		urls = [
			"https://whalegistic.com/api/get-products",
			"https://whalegistic.com/api/get-brands",
			"https://whalegistic.com/api/get-categories",
			"https://whalegistic.com/api/get-collections"
		]

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		resps = await asyncio.gather(*map(this.asyncPost, urls, [send_obj]*len(urls), [send_headers]*len(urls)))
		data = [resp.json() for resp in resps]

		response_obj = {};
		response_obj["products"] = data[0]["products"]
		response_obj["max_product_price"] = data[0]["max_price"]
		response_obj["number_products"] = data[0]["total_products_count"]
		response_obj["brands"] = data[1]["brands"]
		response_obj["categories"] = data[2]["categories"]
		response_obj["collections"] = data[3]["collections"]

		return response_obj


	def getStore(this, send_obj):

		data = asyncio.run( this.getAsyncStore(send_obj) )

		return data



	def getProducts(this, send_obj):

		send_url = "https://whalegistic.com/api/get-products"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		products_obj = response.json()

		return products_obj["products"]



	def getCollectionProducts(this, send_obj):

		send_url = "https://whalegistic.com/api/get-collections-products"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		products_obj = response.json()

		return products_obj["products"]



	def getRelatedProducts(this, send_obj):

		send_url = "https://whalegistic.com/api/get-related-products"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		products_obj = response.json()

		return products_obj["products"]



	def getProductBySlug(this, send_obj):

		send_url = "https://whalegistic.com/api/get-product-by-products"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		products_obj = response.json()

		return products_obj["product"]


	def getGroupProduct(this, send_obj):

		send_url = "https://whalegistic.com/api/get-group-product"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		products_obj = response.json()

		return products_obj["group_product"]



	def getClient(this, send_obj):

		send_url = "https://whalegistic.com/api/get-client"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		client_obj = response.json()

		return client_obj["client"]



	def createClient(this, send_obj):

		send_url = "https://whalegistic.com/api/create-client"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		client_obj = response.json()

		return client_obj



	def getClientOrders(this, send_obj):

		send_url = "https://whalegistic.com/api/get-client"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		client_orders_obj = response.json()

		return client_orders_obj["orders"]



	async def getAsyncClientProfile(this, send_obj):

		urls = [
			"https://whalegistic.com/api/get-client",
			"https://whalegistic.com/api/get-client-orders"
		]

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		resps = await asyncio.gather(*map(this.asyncPost, urls, [send_obj]*len(urls), [send_headers]*len(urls)))
		data = [resp.json() for resp in resps]

		print(f"\nDATA RESPONSE : {data}\n")

		response_obj = {};
		response_obj["client"] = data[0]["client"]
		response_obj["client_orders"] = data[1]["orders"]

		del response_obj["client"]["ID"];
		del response_obj["client"]["Store_ID"];

		return response_obj


	def getClientProfile(this, send_obj):

		data = asyncio.run( this.getAsyncClientProfile(send_obj) )

		return data



	def createContact(this, send_obj):

		send_url = "https://whalegistic.com/api/create-contact"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		contact_obj = response.json()

		return contact_obj["succ"]



	def createNewsletter(this, send_obj):

		send_url = "https://whalegistic.com/api/create-newsletter"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		newsletter_obj = response.json()

		return newsletter_obj["succ"]



	def getShippingRates(this, send_obj):

		send_url = "https://whalegistic.com/api/get-shipping-rates"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		shipping_obj = response.json()

		return shipping_obj["shipping_costs"]



	def getShippingRate(this, send_obj):

		send_url = "https://whalegistic.com/api/get-shipping-rate"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		shipping_obj = response.json()

		return shipping_obj["shipping"]



	def getPromoCode(this, send_obj):

		send_url = "https://whalegistic.com/api/search-promo-code"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		promo_code_obj = response.json()

		return promo_code_obj["promo_code"]



	def getOrder(this, send_obj):

		send_url = "https://whalegistic.com/api/get-order"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		order_obj = response.json()

		return order_obj["order"]



	def getTotal(this, send_obj):

		send_url = "https://whalegistic.com/api/get-total"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		total_obj = response.json()

		return total_obj



	def createOrder(this, send_obj):

		send_url = "https://whalegistic.com/api/create-order"

		if send_obj == None: 
			send_obj = {}

		send_obj["public_key"] = this.pub_key

		send_headers = { 
			"Content-Type": "application/json", 
			"Authorization": f"Bearer {this.token}" 
		}

		response = requests.post(url = send_url, json = send_obj, headers = send_headers)
		order_obj = response.json()

		return order_obj




