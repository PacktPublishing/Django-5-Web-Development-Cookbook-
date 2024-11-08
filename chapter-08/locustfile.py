from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def view_articles(self):
        self.client.get("/articles")

    @task(3)
    def create_article(self):
        self.client.post("/articles/new", {
            "title": "Performance Testing",
            "content": "Testing the performance of our Conduit app."
        })
