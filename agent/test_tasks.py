from tasks import TaskStore


def test_add_list_complete_delete(tmp_path):
    store = TaskStore(tmp_path / "tasks.json")
    assert store.list() == []

    milk = store.add("Buy milk")
    store.add("Walk dog")
    assert [t["id"] for t in store.list()] == [1, 2]

    assert store.complete(milk["id"])["done"] is True
    assert store.delete(2)["title"] == "Walk dog"
    assert store.list() == [{"id": 1, "title": "Buy milk", "done": True}]


def test_missing_task_returns_none(tmp_path):
    store = TaskStore(tmp_path / "tasks.json")
    assert store.complete(99) is None
    assert store.delete(99) is None


def test_new_id_follows_highest_existing_id(tmp_path):
    store = TaskStore(tmp_path / "tasks.json")
    store.add("a")
    store.add("b")
    store.delete(2)
    assert store.add("c")["id"] == 2
