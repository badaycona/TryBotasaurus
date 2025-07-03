import requests
from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO
import get_image
import scrape_steam
import game_requirement
if __name__ == '__main__':

    gamelist = ['1091500','1245620', '730', '413150', '271590','1086940', '1145360', '292030', '1172470', '739630']
    path_list = []
    game_object_list = []
    for game_id in gamelist:
        path = get_image.get_image(game_id)
        path_list.append(path)
        
        str_requirement = scrape_steam.get_structured_game_requirements(game_id)

        str_minimum = str_requirement['minimum']
        str_recommend = str_requirement['recommended']

        object_minimum = scrape_steam.from_str_to_object(str_minimum)
        object_recommmend = scrape_steam.from_str_to_object(str_recommend)
        if not object_recommmend:
            object_recommmend = object_minimum

        game_object = game_requirement.Game('', object_minimum, object_recommmend)
        game_object_list.append(game_object)
    img = Image.open(path_list[0])
    img.show()
    print(path_list)
    print(game_object_list[0])