from skpy import Skype
from skpy.conn import SkypeConnection
from skpy.user import SkypeUser


class SkypeCustom(Skype):
    def setMood(self, mood, text=None):
        """
        Update the activity message for the current user.

        Args:
            mood (str): new mood message
        """
        self.conn("POST",
                  "{0}/users/{1}/profile/partial".format(SkypeConnection.API_USER,
                                                         self.userId),
                  auth=SkypeConnection.Auth.SkypeToken,
                  json={
                      "payload": {
                          "mood": f"({mood}) {text}" if mood else "",
                          "richMood": f'<ss type="{mood}">({mood})</ss> {text}' if mood else ""
                      },
                  })
        self.user.mood = SkypeUser.Mood(plain=mood) if mood else None


if __name__ == "__main__":
    pass
