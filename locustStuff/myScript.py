import random
import time
from locust import HttpUser, task, between

class HelloWorldUser(HttpUser):
    host = "https://jabiyaerp.flai.com.do"

    user_credentials = [
            "user1",
            "user2",
            "user3",
            "user4",
            "user5",
            "user6",
            "user7",
            "user8",
            "user9",
            "user10",
            "user11",
            "user12",
            "user13",
            "user14",
            "user15",
            "user16",
            "user17",
            "user18",
            "user19",
            "user20"
    ] 
        
    products = [
        "PIM001",
        "PIM004",
        "PIM003",
        "12LAP",
        "PIM005",
        "1",
        "AJF004",
        "1746817866",
        "17468178661018",
        "17468178661077",
        "MAC003",
        "17468178661049",
        "17468178665943",
        "17468178660141"
    ] 
    users = user_credentials.copy()
    
    @task
    def on_start(self):


        if len(self.users) > 0:
            user = self.users.pop()
        else:
            self.users = self.user_credentials.copy()


        response = self.client.post("/api/auth/sign_in", json={"jsonrpc": "2.0", "params": {"login": user, "password":"admin"}})
         
        self.client.headers.update({'Authorization': response.headers.get('token')})

        for x in range(6):
            if x == random.randint(1,5): break
            else:
                productId = random.choice(self.products)
                qty = random.randint(1, 5)
                data = self.client.post("/api/cart", json={ "params": { "product_id": productId, "add_qty": qty } } )
        
        order = data.json()
        orderId = order["result"]["data"]["id"]
        deliveryDate = "2020-03-03 08:00:00"
        info = { "params": { "orderId": orderId,"deliveryDate": deliveryDate, "quantityBoxToReturn": 2 }} 

        self.client.post("/api/cart/confirm", json=info)
       
