import unittest
from unittest.mock import MagicMock, call
from handlers import wikipedia_request

class BotCase(unittest.TestCase):
  def test_wiki_0(self):
    word = "самолет"
    text = MagicMock(text=word)
    wikipedia_request.match(text)
    assert text, True
  def test_wiki_1(self):
    word = "hello"
    text = MagicMock(text=word)
    wikipedia_request.match(text)
    assert text, False
  def test_wiki_2(self):
    word = "123"
    text = MagicMock(text=word)
    wikipedia_request.match(text)
    assert text, False

if __name__ == '__main__':
  unittest.main()