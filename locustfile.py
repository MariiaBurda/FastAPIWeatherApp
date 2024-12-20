from locust import HttpUser, task, between


class WeatherAppUser(HttpUser):
    """
    Simulates a user making GET requests to the /weather endpoint for
    multiple cities with a wait time between 1 and 5 seconds.
    """
    wait_time = between(1, 5)

    @task
    def get_weather(self):
        self.client.get("/weather?city=Kyiv")
        self.client.get("/weather?city=London")
        self.client.get("/weather?city=New York")
