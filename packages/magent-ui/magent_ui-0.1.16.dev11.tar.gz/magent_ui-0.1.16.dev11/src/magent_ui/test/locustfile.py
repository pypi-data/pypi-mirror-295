from locust import HttpUser, task


class ApiTestUser(HttpUser):

    # @task(1)
    # def sleep(self):
    #     self.client.get("http://localhost:8888/api/v1/test/sleep")

    # @task(10)
    # def sleep_async(self):
    #     self.client.get("http://localhost:8888/api/v1/test/sleep_async")

    # @task(10)
    # def sleep_async_1(self):
    #     self.client.get("http://localhost:8888/api/v1/test/sleep_async_1")

    @task(100)
    def get_agents(self):
        self.client.get("http://localhost:8888/api/v1/agents")

    @task(1)
    def chant_stream(self):
        self.client.post(
            "http://localhost:8888/api/v1/agents/demo_rag_agent/stream-chat", json={"agent_id": "demo_rag_agent", "session_id": "16d1acec-bd6c-4b46-bb3b-f35351fd11c1", "input": "巴菲特为什么减持苹果股票"})
