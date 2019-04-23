import requests
from bs4 import BeautifulSoup
from lxml import etree

header = {
        'Cookie':'guider_quick_search=on; accessID=20190422221154324891; SESSION_HASH=f4e5dae42126f109146117bc674c4b710b582ab8; user_access=1; PHPSESSID=896982a5885aac04180fc89cd69284f1; is_searchv2=1; save_jy_login_name=13516502945; stadate1=204197176; myloc=44%7C4406; myage=21; PROFILE=205197176%3AaShenone%3Am%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_m.jpg%3A1%3A1%3A50%3A10%3A3.0; mysex=m; myuid=204197176; myincome=30; RAW_HASH=NF4g1mxpy-jORuqD45jT08fK5GjtyO%2A3bXlwzuLbb10QKP2EW4P9l3uSrPlTFug3aYax2J4LH6M6y0EiQlay23OIYYiQata7h4JS4KFTh1BelBc.; COMMON_HASH=1b86e07a17d23836a9aff7c4e2d76b8d; sl_jumper=%26cou%3D17%26omsg%3D0%26dia%3D0%26lst%3D2019-04-22; last_login_time=1555942963; upt=geKYxB8G2HkL-rxIMfekQI-hO%2A70pms%2AJ0QI3cI3ersP6nb%2A47SNQvByQcYLI2JbaWR-Icye5VlfMeokP5OjKtc.; user_attr=000000; main_search:205197176=%7C%7C%7C00; pop_avatar=1; pop_time=1555943005734'

}

def url_process(url_string):
    respo = requests.get(url_string,headers=header)
    print(respo.content.decode('utf-8'))
    

if __name__ == "__main__":
    url_path = 'http://search.jiayuan.com/v2/search_v2.php'
    url_process(url_path)