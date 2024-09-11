import json
from fastapi import APIRouter
import time
from datetime import datetime, timezone
import os
from pydantic import BaseModel
import asyncio


def router(rank_base_folder='./rank/', check_token=None, int_rank_limit_days=30, int_rank_limit_number=30):
    """
    rank_base_folder[str]: 儲存rank資料的資料夾
    check_token[func]: 判斷user token是否合法的function, 回傳 True, False or raise exception
    int_rank_limit_days[int]: 更新排行榜時超過幾天的玩家會從排行榜中移除
    int_rank_limit_number[int]: 排行榜上會有幾名玩家
    """
    
    str_rank_folder = rank_base_folder
    os.makedirs(str_rank_folder, exist_ok=True)
    
    if check_token is None:
        def check_token(str_user, str_token):
            return True
    

    router = APIRouter()

    class ScoreItem(BaseModel):
        str_user: str = '190041-s090504'
        str_token: str = '99'
        str_game_name: str = "PlantHero"
        str_rank_file: str = 'LevelRank.json'
        str_name: str = 'no'
        int_score: int = 0


    @router.post("/rank/set_rank/")
    async def set_rank(item: ScoreItem):
        try:
            #print('上傳score')
            #print(item.str_name)
            check_token(item.str_user, item.str_token)
            lst_cache = await get_rank_json(item.str_game_name, item.str_rank_file)
            #print('get cache file')
            new_ranking = await update_ranking(lst_cache, item.str_user, item.str_name,
                                        int(item.int_score), int_rank_limit_days,
                                        int_rank_limit_number)
            #print('get new rank ')
            await set_rank_json(item.str_game_name, item.str_rank_file,
                                new_ranking)
            return 'OK'
        except ValueError as e:
            return str(e)


    @router.get('/rank/get_rank/')
    async def get_rank(str_user: str = '190041-s090504',
                str_token: str = '999999999999',
                str_game_name="PlantHero",
                str_rank_file='LevelRank.json'):
        #通用型排行榜，可以用來記錄任何數值，例如分數、時間、等級等，只要是int數值就可以，可以區分不同遊戲的排行榜
        #目前只限於活躍玩家，30天內有登入過的玩家才會出現在排行榜中, 並且只會顯示前30名
        check_token(str_user, str_token)
        lst_cache = await get_rank_json(str_game_name, str_rank_file)
        if lst_cache:
            #print('找到排行榜')
            return lst_cache
        print('找不到排行檔案，改用預設值')

        lst_result = []
        dic_result = {}
        dic_result["user_name"] = "Player0"
        dic_result["user_account"] = "0920-4980"
        dic_result["score"] = 0
        dic_result["timestamp"] = int(time.time())
        lst_result.append(dic_result)
        return lst_result


    async def update_ranking(ranking,
                    user_account,
                    user_name,
                    score,
                    int_date_limit=30,
                    int_rank_limit=30):
        new_ranking = []
        timestamp = int(time.time())
        new_item = {
            'user_name': user_name,
            'score': int(score),
            'timestamp': timestamp,
            'user_account': user_account
        }
        now = datetime.now(timezone.utc)
        # remove old data, and remove user's old data
        for item in ranking:
            item_timestamp = item['timestamp']
            delta = now - datetime.fromtimestamp(item_timestamp, timezone.utc)
            if item['user_account'] != user_account:
                if delta.days < int_date_limit:
                    new_ranking.append(item)
        # add new data
        new_ranking.append(new_item)

        # sort and limit the ranking, considering both score and timestamp
        new_ranking = sorted(new_ranking, key=lambda x: (-x['score'], x['timestamp']))[:int_rank_limit]
        return new_ranking


    async def get_rank_json(str_game_name, str_ranking_file):
        str_path = os.path.join(str_rank_folder, str_game_name, str_ranking_file)
        if os.path.exists(str_path):
            try:
                with open(str_path, 'r', encoding='utf-8') as f:
                    python_obj = json.load(f)

                for item in python_obj:
                    item["score"] = int(item["score"])
                return python_obj
            except Exception as e:
                print(e)
                return []
        else:
            print('找不到檔案')
            print(str_path)
        return []


    file_lock = asyncio.Lock()


    async def set_rank_json(str_game_name, str_ranking_file, lst_ranking):
        str_path = os.path.join(str_rank_folder, str_game_name, str_ranking_file)
        dir_path = os.path.dirname(str_path)
        async with file_lock:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            try:
                with open(str_path, 'w', encoding='utf-8') as f:
                    json.dump(lst_ranking, f, ensure_ascii=False)
                    #print("寫入排行榜成功")
            except Exception as e:
                print('寫入排行榜失敗')
                print(e)
                return 'error:' + str(e)
        return 'OK'

    return router