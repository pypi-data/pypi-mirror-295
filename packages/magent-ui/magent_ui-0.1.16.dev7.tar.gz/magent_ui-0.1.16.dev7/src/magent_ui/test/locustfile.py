from locust import HttpUser, task


class ApiTestUser(HttpUser):

    # @task(1)
    # def sleep(self):
    #     self.client.get("http://localhost:8888/api/v1/test/sleep")

    @task(10)
    def sleep_async(self):
        self.client.get("http://localhost:8888/api/v1/test/sleep_async")

    @task(10)
    def sleep_async_1(self):
        self.client.get("http://localhost:8888/api/v1/test/sleep_async_1")
