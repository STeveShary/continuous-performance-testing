from locust import HttpUser, task, between


class ExampleUser(HttpUser):
    wait_time = between(0.5, 2)

    @task(100)
    def index(self):
        self.client.get("/fast")

    @task(2)
    def about(self):
        self.client.get("/slow")
