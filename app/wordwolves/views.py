from collections import Counter
import random


from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Room, Player

from .helper import generate_room_name


def top(request):
    return render(request, "wordwolves/top.html")


def create_room(request):
    return render(request, "wordwolves/create_room.html")


def enter_room(request):
    if request.method == "POST":
        input_room_name = request.POST["room_name"]
        if Room.objects.filter(room_name=input_room_name).exists():
            return redirect(reverse("WW:entrance", args=(input_room_name,)))
        else:
            context = {"error_message": "Room {} does not exist. Please try again.".format(input_room_name)}
            return render(request, "wordwolves/enter_room.html", context)

    else:
        return render(request, "wordwolves/enter_room.html")


def fetch_topic():
    # english
    major, minor = random.sample(random.choice([
        ["apple", "orange", "banana", "strawberry", "melon", "kiwi"],
        ["Google", "Facebook", "Netflix", "Amazon"],
        ["Waseda", "Keio", "Tokyo University", "Kyoto University", "Harvard University", "Stanford University"],
        ["shogi", "go (japanese 'igo)", "chess", "Othello"],
        ["Amazon", "Netflix", "hulu", "abema"],
        ["bat", "racket", "ragby ball", "glove"]
    ]), 2)
    # japanese
    major, minor = random.sample(random.choice([
        ["リンゴ", "みかん", "バナナ", "イチゴ", "メロン", "キウイ", "ぶどう", "もも", "パイナップル"],
        ["Google", "Facebook", "Netflix", "Amazon", "Youtube"],
        ["早稲田大学", "慶応大学", "東京大学", "京都大学", "ハーバード大学", "スタンフォード大学", "ケンブリッジ大学"],
        ["将棋", "囲碁", "大富豪", "チェス", "オセロ", "モノポリー", "人狼", "ブラックジャック"],
        ["Amazon", "Netflix", "hulu", "Abema"],
        ["明石家さんま", "今田耕司", "東野幸治", "マツコ・デラックス", "安住紳一郎", "タモリ", "中居正広", "上田晋也", "有吉弘行"],
        ["LINE", "twitter", "instagram", "TikTok", "Youtube", "Facebook"],
        ["カラオケ", "ボーリング", "ダーツ", "卓球"],  # 遊び
        ["顔がタイプ", "年収が高い", "性格の一致", "自分にないものを持っている", "体型", "IQが近い", "声が好み"],  # 異性に求める条件
        ["動物園", "水族館", "映画館", "ディズニーシー", "ディズニーランド", "温泉", "遊園地", "美術館"],  # デートスポット
        ["お台場海浜公園", "日本科学未来館", "大江戸温泉物語", "遊園地よみうりランド",
         "東京スカイツリー", "すみだ水族館", "浅草寺", "上野動物園"],  # 東京・デートスポット
        ["面接", "合コン"],  # 遊び
        ["1億円貰ったら", "10万円貰ったら", "マスク二枚もらったら"]
    ]), 2)

    return major, minor


@require_POST
def room(request):
    room_name = generate_room_name()
    num_members = int(request.POST.get("num_members"))  # TODO validation for num_members
    num_majors = num_members - (num_members // 3)
    # category = request.POST.get("category")
    # player_nickname = request.POST["nickname"]
    category = "dummy_category"
    major, minor = fetch_topic()
    new_room = Room(
        room_name=room_name,
        category=category,
        pub_date=timezone.now(),
        num_players=num_members,
        num_majors=num_majors,
        major=major,
        minor=minor,
    )
    new_room.save()
    # player_nicknames = [player_nickname] + ["not entered" for _ in range(num_members-1)]
    temp_names = ["not entered" for _ in range(num_members)]
    items = [major] * num_majors + [minor] * (num_members - num_majors)
    random.shuffle(items)
    for i in range(num_members):
        each_player = Player(
            room=new_room,
            nickname=temp_names[i],
            item=items[i],
            majority=items[i] == major,
        )
        each_player.save()

    return redirect(reverse('WW:name_notice', args=(room_name,)))


def name_notice(request, room_name):
    context = {"room_name": room_name}
    return render(request, 'wordwolves/notice.html', context)


def entrance(request, room_name):
    context = {"room_name": room_name}
    room_obj = Room.objects.get(room_name=room_name)  # TODO error handling for direct access via url
    if request.method == "POST" and "already_entered" in request.POST:
        print("already_entered")
        player_objs = Player.objects.filter(room=room_obj)
        context = {
            "room_name": room_obj.room_name,
            "players": player_objs,
        }

        return render(request, 'wordwolves/room.html', context)
    # if post and name redirect to pass setting
    elif request.method == "POST" and "nickname" in request.POST:
        player_nickname = request.POST["nickname"]
        if player_nickname in ["not entered", ""]:  # TODO check duplicate name
            error_messages = {"not entered": "please use other name", "": "please enter name"}
            context["error_message"] = error_messages[player_nickname]
        else:
            player_objs = Player.objects.filter(room=room_obj, nickname="not entered")
            if len(player_objs) == 0:
                context["error_message"] = "room is full, have you already_entered the room?"
            else:
                player_obj = player_objs[0]
                player_obj.nickname = player_nickname
                player_obj.save()
                context["nickname"] = player_obj.nickname
                return render(request, "wordwolves/set_pass.html", context)
    # if get or others: let type name
    else:
        return render(request, 'wordwolves/enter_name.html', context)


def set_pass(request, room_name, nickname):
    room_obj = Room.objects.get(room_name=room_name)
    player_obj = Player.objects.get(room=room_obj, nickname=nickname)
    if player_obj.plain_pass:
        return redirect(reverse('WW:top'))  # unexpected
    else:
        context = {
            "nickname": player_obj.nickname,
            "room_name": room_name,

        }
        return render(request, "wordwolves/set_pass.html", context)


def enter_pass(request, room_name, nickname):
    room_obj = Room.objects.get(room_name=room_name)
    player_obj = Player.objects.get(room=room_obj, nickname=nickname)
    if not player_obj.plain_pass:
        return redirect(reverse('WW:top'))  # unexpected
    else:
        context = {
            "nickname": player_obj.nickname,
            "room_name": room_name,

        }
        return render(request, "wordwolves/enter_pass.html", context)


def mypage(request, room_name, nickname):
    room_obj = Room.objects.get(room_name=room_name)
    player_obj = Player.objects.get(room=room_obj, nickname=nickname)
    if request.method == "GET" and player_obj.replay is True:
        pass  # go to mypage
    elif request.method == "GET":
        if player_obj.plain_pass:
            return redirect(reverse("WW:enter_pass", args=(room_name, nickname,)))
        else:
            return redirect(reverse("WW:set_pass", args=(room_name, nickname,)))
    else:
        # not yet set pass
        if not player_obj.plain_pass:
            input_plain_pass = request.POST["plain_pass"]
            if len(input_plain_pass) >= 4:  # TODO move validation to set pass
                context = {"error_message": "Invalid password. please use less than 3 characters"}
                return redirect(reverse("WW:set_pass", args=(room_name, nickname,)))
            else:
                player_obj.plain_pass = input_plain_pass
                player_obj.save()
        # wrong password
        elif request.POST["plain_pass"] != player_obj.plain_pass:
            return redirect(reverse("WW:enter_pass", args=(room_name, nickname,)))
        else:
            # password is ok
            pass
    others = [each_player.nickname for each_player in Player.objects.filter(room=room_obj)]
    # not ready
    if "not entered" in others:
        context = {
            "room_name": room_name,
            "nickname": nickname,
            "plain_pass": player_obj.plain_pass,
            "notready": True,
        }
        return render(request, "wordwolves/mypage.html", context)
    others.remove(player_obj.nickname)
    vote = player_obj.vote
    context = {
        "room_name": room_name,
        "nickname": nickname,
        "item": player_obj.item,
        "vote": vote,
        "others": others,
    }
    return render(request, "wordwolves/mypage.html", context)


@require_POST
def game_res(request, room_name, nickname):
    room_obj = Room.objects.get(room_name=room_name)
    vote = request.POST["vote"]
    player = Player.objects.get(room=room_obj, nickname=nickname)
    player.vote = vote
    player.replay = False
    player.save()

    all_players = Player.objects.filter(room=room_obj)

    context = {
        "room_name": room_name,
        "nickname": nickname,
        "players": all_players,
        "status": "waiting",
        "vote": vote,
    }

    # check if end
    cnts = 0
    votes = []
    for each_player in all_players:
        if each_player.vote:
            cnts += 1
            votes.append(each_player.vote)
    if cnts == len(all_players):
        # decide winner
        results = Counter(votes).most_common(2)
        if results[0][1] > results[1][1]:  # game end
            voted_player_objs = list(filter(lambda x: x.nickname == results[0][0], all_players))
            assert len(voted_player_objs) == 1, ValueError("too many players")
            voted_player_obj = voted_player_objs[0]
            if voted_player_obj.majority:
                winner = room_obj.minor
            else:
                winner = room_obj.major
            context["status"] = "finished"
            context["winner"] = winner
            context["voted"] = voted_player_obj.nickname
        else:  # same vote
            context["status"] = "draw"
    return render(request, "wordwolves/game_res.html", context)


def replay(request, room_name, nickname):
    room_obj = Room.objects.get(room_name=room_name)
    player = Player.objects.get(room=room_obj, nickname=nickname)

    player.replay = True
    player.save()
    all_players = Player.objects.filter(room=room_obj)
    replay_flags = [each_player.replay for each_player in all_players]
    votes = [each_player.vote for each_player in all_players]
    # check if everyone join the new game
    if not all(replay_flags) and any(votes):
        context = {
            "room_name": room_name,
            "nickname": nickname,
        }
        return render(request, "wordwolves/replay.html", context)

    # clear votes, set new topic. only once.
    elif any(votes):
        num_members = room_obj.num_players
        num_majors = num_members - (num_members // 3)
        # set new topic
        major, minor = fetch_topic()
        while room_obj.major in [major, minor] or room_obj.minor in [major, minor]:
            major, minor = fetch_topic()
        # update room
        room_obj.major = major
        room_obj.minor = minor
        room_obj.save()
        # player
        items = [major] * num_majors + [minor] * (num_members - num_majors)
        random.shuffle(items)
        for i, each_player in enumerate(all_players):
            each_player.vote = None
            # new topic
            each_player.item = items[i]
            each_player.majority = items[i] == major
            each_player.save()
        return redirect(reverse("WW:mypage", args=(room_name, nickname,)))
    else:
        return redirect(reverse("WW:mypage", args=(room_name, nickname,)))


# empty line needed
