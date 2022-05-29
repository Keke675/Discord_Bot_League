import requests
from bs4 import BeautifulSoup


class MmrCheck:
  def __init__(self):
        self.url = 'https://euw.whatismymmr.com/api/v1/summoner?name='

  def key_words_search_words(self, user_message):
    search_words = user_message.split()[1:]
    words = '%20'.join(search_words)
    nick = ' '.join(search_words)
    return words, nick

  def search_mmr(self, words):
    username = self.url+words
    response = requests.get(username)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    return soup             


  def trans_mmr(self, soup):
      soups = str(soup)
      if len(soups) < 120:
          return False, None, None
      else:    
          index_mmr = soups.find('"avg":')
          result_mmr = soups[index_mmr+6:index_mmr+10]
          index_rank = soups.find('<b>')
          index_rank_2 = soups.find('</b>')
          result_rank = soups[index_rank+3:index_rank_2]
          index_sum = soups.find('"summary":')
          summary = soups[index_sum+11:index_rank-1]
          return result_mmr, result_rank, summary