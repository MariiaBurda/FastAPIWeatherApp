from locust import HttpUser, task, between


class WeatherAppUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_weather(self):
        self.client.get("/weather?city=Kyiv")
        self.client.get("/weather?city=London")
        self.client.get("/weather?city=New York")
