import requests


class Mattermost:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
    # login and get token from header resp

    def login(self):
        resp = requests.post(
            self.server +
            "/api/v4/users/login",
            json={
                "login_id": self.username,
                "password": self.password})

        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": "Bearer " + resp.headers["Token"]})

    # method custom status set

    def set_status(self, status, emoji, text):
        resp = self.session.put(
            self.server +
            "/api/v4/users/me/status/custom",
            json={
                "status": status,
                "emoji": emoji,
                "text": text})


if __name__ == "__main__":
    pass
