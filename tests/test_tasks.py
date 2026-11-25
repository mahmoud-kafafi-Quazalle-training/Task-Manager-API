from unittest import TestCase

from fastapi.testclient import TestClient

from main import create_app


class TaskApiTests(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(create_app())
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)

    def test_crud_and_ids(self) -> None:
        self.assertEqual(self.client.get("/tasks").json(), [])
        created = self.client.post(
            "/tasks", json={"title": "  Study FastAPI  ", "description": "Read the docs"}
        )
        self.assertEqual(created.status_code, 201)
        self.assertNotIn("X-Process-Time", created.headers)
        expected = {
            "id": 1, "title": "Study FastAPI", "description": "Read the docs",
            "status": "pending",
        }
        self.assertEqual(created.json(), expected)
        self.assertEqual(self.client.get("/tasks").json(), [expected])
        self.assertEqual(self.client.get("/tasks/1").json(), expected)

        deleted = self.client.delete("/tasks/1")
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(deleted.json(), {"message": "Task deleted"})
        self.assertEqual(self.client.get("/tasks/1").status_code, 404)
        self.assertEqual(self.client.get("/tasks").json(), [])
        next_task = self.client.post("/tasks", json={"title": "Next"}).json()
        self.assertEqual(next_task["id"], 2)
        self.assertEqual(next_task["description"], "")

    def test_patch_preserves_omitted_fields(self) -> None:
        original = self.client.post(
            "/tasks", json={"title": "Original", "description": "Notes"}
        ).json()
        expected = dict(original)
        for changes in (
            {"status": "completed"}, {"title": "Updated"}, {"description": ""},
            {"status": "pending", "description": "New notes"}, {},
        ):
            with self.subTest(changes=changes):
                response = self.client.patch("/tasks/1", json=changes)
                expected.update(changes)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), expected)
                self.assertEqual(self.client.get("/tasks/1").json(), expected)

    def test_invalid_input(self) -> None:
        for body in ({}, {"title": "  "}, {"title": 7}, {"title": "Task", "id": 9},
                     {"title": "Task", "status": "completed"}):
            with self.subTest(create=body):
                self.assertEqual(self.client.post("/tasks", json=body).status_code, 422)

        original = self.client.post("/tasks", json={"title": "Keep me"}).json()
        for body in ({"title": "   "}, {"title": None}, {"description": None},
                     {"status": None}, {"status": "done"}, {"id": 7}):
            with self.subTest(update=body):
                self.assertEqual(self.client.patch("/tasks/1", json=body).status_code, 422)
        self.assertEqual(self.client.get("/tasks/1").json(), original)
        self.assertEqual(self.client.get("/tasks/invalid").status_code, 422)

    def test_missing_task(self) -> None:
        for response in (
            self.client.get("/tasks/999"),
            self.client.patch("/tasks/999", json={"title": "Updated"}),
            self.client.delete("/tasks/999"),
        ):
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json(), {"detail": "Task not found"})

    def test_app_instances_have_separate_tasks(self) -> None:
        self.client.post("/tasks", json={"title": "Local task"})
        with TestClient(create_app()) as second_client:
            self.assertEqual(second_client.get("/tasks").json(), [])
        self.assertEqual(len(self.client.get("/tasks").json()), 1)

    def test_swagger_and_openapi(self) -> None:
        docs = self.client.get("/docs")
        self.assertEqual(docs.status_code, 200)
        self.assertIn("Swagger UI", docs.text)
        paths = self.client.get("/openapi.json").json()["paths"]
        self.assertEqual(set(paths["/tasks"]), {"get", "post"})
        self.assertEqual(set(paths["/tasks/{task_id}"]), {"get", "patch", "delete"})
        self.assertEqual(self.client.get("/TEstApi").status_code, 404)
