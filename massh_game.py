import tkinter as tk
import tkinter.messagebox as mb
import random as rand
from PIL import Image, ImageTk

class Card:
    def __init__(self,number,element,mark,rule):
        self.number = number
        self.element = element
        self.mark = mark
        self.rule = rule

class Character:
    def __init__(self,name,num,image):
        self.name = name
        self.num = num
        self.image = image


#Labelのカード画像を返す
def create_card_hand(parent, card, w, h):
    filename = "image/" + card + ".png"
    img = Image.open(filename)
    img = img.resize((w, h))
    card_image = ImageTk.PhotoImage(img)
    image_label = tk.Label(parent, image=card_image, bg="white")
    image_label.image = card_image
    return image_label

#Buttonのカード画像を返す
def create_card_field(parent, card, w, h, i, n, text):
    filename = "image/" + card + ".png"
    img = Image.open(filename)
    img = img.resize((w, h))
    card_image = ImageTk.PhotoImage(img)
    image_button = tk.Button(parent, image=card_image, command=lambda: select_field_card(i, n, text))
    image_button.image = card_image
    return image_button

#Labelのキャラクター画像を返す
def create_character_image(number, w, h, type):
    filename = "image/character" + number
    if type == 1:
        filename += "_head"
    filename += ".png"
    img = Image.open(filename)
    img_re = img.resize((w, h))
    image = ImageTk.PhotoImage(img_re)
    return image

#カードの文字を変換 [ 1 -> A ]
def change_N(n):
    cardnum = " "
    if n == 1:
        cardnum = "A"
    elif n == 2:
        cardnum = "B"
    elif n == 3:
        cardnum = "C"
    elif n == 4:
        cardnum = "D"
    elif n == 5:
        cardnum = "E"
    return cardnum

#カードの色をカラーコードに変換 [ 1 -> #a00000 ]
def change_E(n):
    cardcolor = "#000000"
    if n == 1:
        cardcolor = "#a00000"
    elif n == 2:
        cardcolor = "#0000a0"
    elif n == 3:
        cardcolor = "#00a000"
    elif n == 4:
        cardcolor = "#d0d000"
    return cardcolor

#カードの色を文字に変換 [ 1 -> 赤 ]
def change_E_text(n):
    cardcolor = "黒"
    if n == 1:
        cardcolor = "赤"
    elif n == 2:
        cardcolor = "青"
    elif n == 3:
        cardcolor = "緑"
    elif n == 4:
        cardcolor = "黄"
    return cardcolor

#カードの記号を変換 [ 1 -> ● ]
def change_M(n):
    cardmark = " "
    if n == 1:
        cardmark = "●"
    elif n == 2:
        cardmark = "★"
    elif n == 3:
        cardmark = "▲"
    return cardmark

#カードに対応する画像ファイル名に変換
def change_ImageTitle(card, hide):
    title = ""
    if hide == 1:
        title += "Q"
    else:
        title += change_N(card.number)
    if hide == 2:
        title += "_gray"
    else:
        if card.element == 1:
            title += "_red"
        elif card.element == 2:
            title += "_blue"
        elif card.element == 3:
            title += "_green"
        elif card.element == 4:
            title += "_yellow"
    if hide == 3:
        title += "_nothing"
    else:
        if card.mark == 1:
            title += "_circle"
        elif card.mark == 2:
            title += "_star"
        elif card.mark == 3:
            title += "_tri"
    return title

cards = []      #カードを格納する配列
rules = []      #勝利条件を格納する配列

#生成する関数
def game_generate(N,E,M):
    #カード生成
    for i in range(N):
        for j in range(E):
            for k in range(M):
                card = Card(i+1, j+1, k+1, "")
                cards.append(card)
                cards.append(card)
                cards.append(card)
    #勝利条件生成
    while(True):
        for i in range(N):
            rules.append(change_N(i+1) + ":3")
            for j in range(E):
                rules.append(change_E_text(j+1) + ":4")
                rules.append(change_N(i+1) + ":2/" + change_E_text(j+1) + ":3")
                for k in range(M):
                        rules.append(change_M(k+1) + ":5")
                        rules.append(change_E_text(j+1) + ":3/" + change_M(k+1) + ":4")
                        rules.append(change_N(i+1) + ":2/" + change_M(k+1) + ":4")
                        rules.append(change_N(i+1) + ":2/" + change_E_text(j+1) + ":2/" + change_M(k+1) + ":3")
        if len(rules) >= len(cards):
            break

#カードの各要素の種類数
N = 5       #文字
E = 4       #色
M = 3       #記号

#手札<card>
str_hand = []
#フィールド上のカード<int>
str_field = []
str_field_T = []
#フィールド上のカード表示<Label>
str_field_card = []
str_field_card_T = []
str_field_card_confirm = []
#フィールド上の勝利条件<str>
str_rule = []
#フィールド上の勝利条件表示<Label>
str_rule_card = []
#プレイヤーの手札情報の表示<Label>
text_hand = []
#消去する勝利条件の情報
delete_rule = []
# state = [0:State<str>, 1:Players<int>, 2:Turn<int>, 3:Rule<int>, 4:Character(Player), 5,6,7:Character(CPU), 8:Field]
state = ["selectCard", 3, 0, 0, 0, 0, 0, 0, 0]
# [0:ルール, 1:ログ]
state_display = [True, True]
#情報の保存先 [0:選択された手札, 1:選択されたCPU, 2:選択された勝利条件, 3:選択された隠す要素]
select_rec = [0, 0, 0, 0]
winner = []
win_rule = []
limit_skill = []
limit_massh = []


#キャラクターごとの台詞
def character_inst(situation):
    #situation - 1:決定ボタン, 2:カード選択, 3:アクション選択, 4:抹消対象選択, 5:確認対象選択
    if state[4] == 1:       #リドー
        if situation == 1:
            text_inst.config(text="右のボタンで決定だ！")
        elif situation == 2:
            text_inst.config(text="プレイするカードを選ぼう！")
        elif situation == 3:
            text_inst.config(text="使うアクションを選ぼう！")
        elif situation == 4:
            text_inst.config(text="相手の勝利条件を選ぼう！")
        elif situation == 5:
            text_inst.config(text="確認対象のカードを選ぼう！")
    elif state[4] == 2:     #ノア
        if situation == 1:
            text_inst.config(text="右のボタンで決定！")
        elif situation == 2:
            text_inst.config(text="どのカードをプレイする？")
        elif situation == 3:
            text_inst.config(text="どのアクションにしよう？")
        elif situation == 4:
            text_inst.config(text="どの勝利条件を対象にする？")
        elif situation == 5:
            text_inst.config(text="どのカードを確認する？")
    elif state[4] == 3:     #クルス
        if situation == 1:
            text_inst.config(text="")
        elif situation == 2:
            text_inst.config(text="")
        elif situation == 3:
            text_inst.config(text="")
        elif situation == 4:
            text_inst.config(text="")
        elif situation == 5:
            text_inst.config(text="")
    elif state[4] == 4:
        if situation == 1:
            text_inst.config(text="")
        elif situation == 2:
            text_inst.config(text="")
        elif situation == 3:
            text_inst.config(text="")
        elif situation == 4:
            text_inst.config(text="")
        elif situation == 5:
            text_inst.config(text="")
    elif state[4] == 5:
        if situation == 1:
            text_inst.config(text="")
        elif situation == 2:
            text_inst.config(text="")
        elif situation == 3:
            text_inst.config(text="")
        elif situation == 4:
            text_inst.config(text="")
        elif situation == 5:
            text_inst.config(text="")
    elif state[4] == 6:
        if situation == 1:
            text_inst.config(text="")
        elif situation == 2:
            text_inst.config(text="")
        elif situation == 3:
            text_inst.config(text="")
        elif situation == 4:
            text_inst.config(text="")
        elif situation == 5:
            text_inst.config(text="")
    elif state[4] == 7:
        if situation == 1:
            text_inst.config(text="")
        elif situation == 2:
            text_inst.config(text="")
        elif situation == 3:
            text_inst.config(text="")
        elif situation == 4:
            text_inst.config(text="")
        elif situation == 5:
            text_inst.config(text="")
    elif state[4] == 8:
        if situation == 1:
            text_inst.config(text="")
        elif situation == 2:
            text_inst.config(text="")
        elif situation == 3:
            text_inst.config(text="")
        elif situation == 4:
            text_inst.config(text="")
        elif situation == 5:
            text_inst.config(text="")

#プレイするキャラクター選択画面 <最初,配列設定など>
def character_set(players):
    state[1] = players
    for i in range(players):
        str_hand.append([])
        str_field.append([0]*(N+E+M))
        str_field_T.append([])
        str_field_card.append([])
        str_field_card_T.append([])
        str_field_card_confirm.append([])
        str_rule.append([])
        str_rule_card.append([])
        limit_massh.append(2)
    cvs_title.place_forget()
    cvs_character_select.place(x=0, y=0)

#選択中のキャラクター画像取得
current_image = None
def character_select_image(filename, size):
    global current_image
    img = Image.open(filename)
    img = img.resize((size, size))
    current_image = ImageTk.PhotoImage(img)
    text_character_image.config(image=current_image)

#キャラクター選択 main
def character_select(n):
    global current_image
    if n == 0:
        if state[4] == 0:
            return 0
        else:
            randomcharacter = rand.sample(range(1,8), state[1]-1)
            for i in range(state[1]):
                filename = "image/character"
                if i == 0:
                    filename += str(state[4+i]).zfill(2) + ".png"
                    img = Image.open(filename)
                    img = img.resize((120, 120))
                    choiced_image = ImageTk.PhotoImage(img)
                    image_objects.append(choiced_image)
                    image_player_main.config(image=choiced_image)
                    filename = "image/character"
                else:
                    if state[4] <= randomcharacter[i-1]:
                        randomcharacter[i-1] += 1
                    state[4+i] = randomcharacter[i-1]
                filename += str(state[4+i]).zfill(2) + "_head.png"
                img = Image.open(filename)
                img = img.resize((40, 40))
                choice_image = ImageTk.PhotoImage(img)
                image_objects.append(choice_image)
                image_character_top[i].config(image=choice_image)
            if state[4] == 2 or state[4] == 4 or state[4] == 5 or state[4] == 6 or state[4] == 8:
                button_action4.pack_forget()
            game_main()
    elif n == 1:
        state[4] = 1
        text_character_name.config(text="リドー")
        character_select_image("image/character01.png", 350)
        text_character_skill.config(text="~使用可能スキル~\n・勝利条件抹消(1)\n・手札入れ替え(1)\n・隠れている要素確認(2)\n・手札のカードを使用(1)[回数制限:1]")
        button_action1.config(text="抹勝[1]")
        button_action2.config(text="入替[1]")
        button_action3.config(text="要素確認[2]")
        button_action4.config(text="追加使用[1] <制限:1>")
    elif n == 2:
        state[4] = 2
        text_character_name.config(text="ノア")
        character_select_image("image/character02.png", 350)
        text_character_skill.config(text="~使用可能スキル~\n・勝利条件抹消(1)\n・手札入れ替え(1)\n・隠れている要素確認(2)\n・手札のカード枚数+2枚[常時]")
        button_action1.config(text="抹勝[1]")
        button_action2.config(text="入替[1]")
        button_action3.config(text="要素確認[2]")
        button_action4.config(text="")
    elif n == 3:
        state[4] = 3
        text_character_name.config(text="クルス")
        character_select_image("image/character03.png", 350)
        text_character_skill.config(text="~使用可能スキル~\n・勝利条件抹消(1)\n・手札入れ替え(1)\n・隠れている要素確認(2)\n・相手のカードと勝利条件抹消(1)[回数制限:2]")
        button_action1.config(text="抹勝[1]")
        button_action2.config(text="入替[1]")
        button_action3.config(text="要素確認[3]")
        button_action4.config(text="抹勝[1]&入替[1]&要素確認[2] <制限:2>")
    elif n == 4:
        state[4] = 4
        text_character_name.config(text="ルルナ")
        character_select_image("image/character04.png", 350)
        text_character_skill.config(text="~使用可能スキル~\n・相手の勝利条件抹消(1)、隠れている要素確認(1)\n・手札入れ替え(1)\n・隠れている要素確認(2)")
        button_action1.config(text="抹勝[1]&要素確認[1]")
        button_action2.config(text="入替[1]")
        button_action3.config(text="要素確認[2]")
        button_action4.config(text="")
    elif n == 5:
        state[4] = 5
        text_character_name.config(text="ミラ")
        character_select_image("image/character05.png", 350)
        text_character_skill.config(text="~使用可能スキル~\n・相手の勝利条件抹消(1)\n・手札入れ替え(1)、隠れている要素確認(2)\n・隠れている要素確認(4)")
        button_action1.config(text="抹勝[1]")
        button_action2.config(text="入替[1]&要素確認[2]")
        button_action3.config(text="要素確認[4]")
        button_action4.config(text="")
    elif n == 6:
        state[4] = 6
        text_character_name.config(text="トリン")
        character_select_image("image/character06.png", 350)
        text_character_skill.config(text="~使用可能スキル~\n・相手の勝利条件抹消(1)、手札入れ替え(1)\n・手札入れ替え(2)\n・隠れている要素確認(2)")
        button_action1.config(text="抹勝[1]&入替[1]")
        button_action2.config(text="入替[2]")
        button_action3.config(text="要素確認[2]")
        button_action4.config(text="")
    elif n == 7:
        state[4] = 7
        text_character_name.config(text="サタン")
        character_select_image("image/character07.png", 350)
        text_character_skill.config(text="~使用可能スキル~\n・勝利条件抹消(1)\n・手札入れ替え(1)\n・隠れている要素確認(2)\n・勝利条件抹消(1)、勝利条件抹消無効[回数制限:3]")
        button_action1.config(text="抹勝[1]")
        button_action2.config(text="入替[1]")
        button_action3.config(text="要素確認[2]")
        button_action4.config(text="抹勝[1]&抹勝無効 <制限:3>")
    elif n == 8:
        state[4] = 8
        text_character_name.config(text="ゴーレム")
        character_select_image("image/character08.png", 350)
        text_character_skill.config(text="~使用可能スキル~\n・勝利条件抹消(1)、ランダムなカード抹消(1)\n・手札入れ替え(1)\n・隠れている要素確認(2)")
        button_action1.config(text="抹勝[1]&乱カード削除[1]")
        button_action2.config(text="入れ替え[1]")
        button_action3.config(text="要素確認[2]")
        button_action4.config(text="")


#ゲームスタート　描画など
def game_set():
    cvs_character_select.place_forget()
    cvs_playgame.place(x=0, y=0)
    w = int(1200/state[1])
    cvs_playgame.create_line(0,47, 1200,47, fill="white", width=2)
    cvs_playgame.create_line(0,269, 1200,269, fill="white", width=2)
    cvs_playgame.create_line(0,471, 1200,471, fill="white", width=2)
    for i in range(state[1]):
        if state[4+i] == 1:
            limit_skill.append(1)
        elif state[4+i] == 3:
            limit_skill.append(2)
        elif state[4+i] == 7:
            limit_skill.append(3)
        else:
            limit_skill.append(0)
        cvs_playgame.create_line(w*(i+1),0, w*(i+1),471, fill="white", width=2)
        text_name_top[i].place(x=w*i+10, y=3)
        image_character_top[i].place(x=w*i+90, y=2)
        text_limit_count1[i].place(x=w*i+350, y=15, anchor="e")
        if state[4+i] in {1,3,7}:
            text_limit_count2[i].config(text=f"スキル：残り{limit_skill[i]}回")
            text_limit_count2[i].place(x=w*i+350, y=35, anchor="e")
        frame_field_all[i].config(width=w-2, height=220)
        frame_field_all_T[i].config(width=w-2, height=220)
        frame_field_all[i].place(x=w*i+2,y=48)
        frame_rules_all[i].config(width=w-2, height=200)
        frame_rules_all[i].place(x=w*i+2,y=270)
    #カード生成
    game_generate(5,4,3)
    #カードのシャッフル
    rand.shuffle(rules)
    #カードの要素と勝利条件はゲームごとにランダムな組合せ
    for i in range(len(cards)):
        cards[i].rule = rules[i]
    rand.shuffle(cards)
    #PlayerとCPUに手札の配布、回数制限の設定
    for i in range(state[1]):
        for j in range(3):
            str_hand[i].append(cards.pop(0))
        if state[4+i] == 2:
            str_hand[i].append(cards.pop(0))
            str_hand[i].append(cards.pop(0))
    hands_set_start()

#ゲームスタート時のプレイヤー手札設定
def hands_set_start():
    for i in range(len(str_hand[0])):
        #手札のカード情報を取得
        cardtext = change_ImageTitle(str_hand[0][i], 0)
        ruletext = (str_hand[0][i].rule).replace("/", "\n")
        #手札のカード情報を表示
        text_hand.append(create_card_hand(frame_hands[i], cardtext, 60, 60))
        text_hand.append(tk.Label(frame_hands[i], text=ruletext, font=("MSゴシック",12, "bold"), fg="black", bg="white"))
        frame_hands[i].pack(padx=15, side=tk.LEFT)
        frame_hands[i].pack_propagate(False)
        text_hand[2*i].bind("<Button-1>", lambda event, n=i+1: game_select_card_player(event, n))
        text_hand[2*i+1].bind("<Button-1>", lambda event, n=i+1: game_select_card_player(event, n))
        text_hand[2*i].pack(fill=tk.X, side=tk.LEFT)
        text_hand[2*i+1].pack(fill=tk.X, side=tk.LEFT)
    text_inst.config(text="手札のカードを1つ選択\n → 決定ボタン")

#i番目の手札1枚入れ替え
def hands_set_ref(card, i, player):
    if i > 0:
        cardtext = change_ImageTitle(card, 0)
        str_hand[player][i-1] = card
        text_hand[2*(i-1)] = create_card_hand(frame_hands[i-1], cardtext, 60, 60)
        frame_hands[i-1].config(highlightbackground="white", bg="white")
        ruletext = (str_hand[player][i-1].rule).replace("/", "\n")
        text_hand[2*(i-1)+1].config(text=ruletext, fg="black", bg="white")
        text_hand[2*(i-1)].bind("<Button-1>", lambda event, n=i: game_select_card_player(event, n))
        text_hand[2*(i-1)+1].bind("<Button-1>", lambda event, n=i: game_select_card_player(event, n))
        text_hand[2*(i-1)].pack(fill=tk.X, side=tk.LEFT)
        text_hand[2*(i-1)+1].pack(fill=tk.X, side=tk.LEFT)

#隠す要素選択パネル
def game_select_hide(n):
    varA.set(1)
    state[0] = "waiting"
    select_rec[3] = n
    frame_panel_hide.place_forget()

#手札クリック時 "selectCard","selectChange"
def game_select_card_player(event, n):
    if state[0] == "selectCard":
        var.set(1)
        state[0] = "waiting"
        for frame_card in frame_hands:
            frame_card.config(highlightbackground="white")
        select_rec[0] = n
        frame_hands[n-1].config(highlightbackground="red")
        state[0] = "stay"
        frame_panel_hide.place(x=300, y=472)
        text_inst.config(text="隠す要素を1つ選択")
        varA.set(0)  #隠す要素が選択されるまで
        root.wait_variable(varA)
        playcard = str_hand[0][n-1]
        frame_hands[n-1].config(highlightbackground="#108010", bg="#108010")
        text_hand[2*(n-1)].pack_forget()
        text_hand[2*(n-1)+1].pack_forget()
        playcardtext = change_ImageTitle(playcard, select_rec[3])
        playcardtext_T = change_ImageTitle(playcard, 0)
        str_field_T[0].append(playcardtext_T)
        game_field_count(str_field[0], playcard.number, playcard.element, playcard.mark)
        game_card_play1(playcardtext, 0)
        game_card_play2(playcardtext_T, 0)
        game_card_play3(playcard, 0)
        log_card = change_N(playcard.number) + "/" + change_E_text(playcard.element) + "/" + change_M(playcard.mark)
        label = tk.Label(frame_log, text=f"Playerは「{log_card}」,「{playcard.rule}」をフィールドに出しました", bg="white")
        label.pack(padx=5, pady=3, anchor="w")
        update_log()
        select_rec[0] = n
    elif state[0] == "selectChange":
        if n != select_rec[0]:
            varA.set(1)
            state[0] = "waiting"
            text_hand[2*(n-1)].pack_forget()
            text_hand[2*(n-1)+1].pack_forget()
            newcard = cards.pop(0)
            hands_set_ref(newcard, n, 0)

#選択されたカードをフィールド1に出す - card
def game_card_play1(text, n):
    str_field_card[n].append((create_card_field(frame_field_all[n], text, 45, 45, len(str_field_card[n]), n, "a")))
    size = len(str_field_card[n])
    place_col = (size-1) % 6
    place_row = int((size-1) / 6)
    str_field_card[n][-1].grid(row=place_row, column=place_col, padx=5, pady=5)

#選択されたカードをフィールド2に出す - card
def game_card_play2(text, n):
    str_field_card_T[n].append((create_card_field(frame_field_all_T[n], text, 45, 45, len(str_field_card_T[n]), n, str_field_T[n][-1])))
    size = len(str_field_card_T[n])
    place_col = (size-1) % 6
    place_row = int((size-1) / 6)
    str_field_card_T[n][-1].grid(row=place_row, column=place_col, padx=5, pady=5)
    if n == 0:
        str_field_card_confirm[n].append(True)
    else:
        str_field_card_confirm[n].append(False)

#選択されたカードをフィールドに出す - rule
def game_card_play3(card, n):
    str_rule[n].append(card.rule)
    str_rule_card[n].append(tk.Label(frame_rules_all[n], text=card.rule, font=("MSゴシック",12,"bold"), fg="white", bg="#003600"))
    str_rule_card[n][-1].pack(padx=20, pady=3)

#CPUがフィールドにカードを出す関数（現状：完全ランダム）
def game_select_card_cpu():
    for cp in range(1, state[1]):
        hide = rand.randint(1,3)
        playcard = str_hand[cp].pop(0)
        playcardtext = change_ImageTitle(playcard, hide)
        str_field_T[cp].append(change_ImageTitle(playcard, 0))
        game_field_count(str_field[cp], playcard.number, playcard.element, playcard.mark)
        game_card_play1(playcardtext, cp)
        game_card_play2(playcardtext, cp)
        game_card_play3(playcard, cp)
        str_rule_card[cp][-1].bind("<Button-1>", lambda event, n=cp: game_select_rule_player(event, n))
        log_card = ""
        if hide == 1:
            log_card += "？/" + change_E_text(playcard.element) + "/" + change_M(playcard.mark)
        elif hide == 2:
            log_card += change_N(playcard.mark) + "/？/" + change_M(playcard.mark)
        elif hide == 3:
            log_card += change_N(playcard.mark) + "/" + change_E_text(playcard.element) + "/？"
        label = tk.Label(frame_log, text=f"CPU{cp}は「{log_card}」,「{playcard.rule}」をフィールドに出しました", bg="white")
        label.pack(padx=5, pady=3, anchor="w")

#アクション選択パネル (USER:player=0, CPU:player=1~3)
def game_select_action(n, player):
    if state[0] == "selectAction":
        if n == 4 and limit_skill[player] == 0:
            text_inst.config(text="回数上限！ 別のアクションを選択")
        elif limit_massh[player] == 0 and (n == 1 or (n == 4 and (state[4+player] == 3 or state[4+player] == 7))):
            text_inst.config(text="回数上限！ 別のアクションを選択")
        else:
            var.set(1)
            state[0] = "waiting"
            frame_panel_action.place_forget()
            if n == 1:
                text_inst.config(text="消去したい勝利条件を1つ選択")
                game_action_1(player)
                if state[4+player] == 4:
                    display_field(1)
                    text_inst.config(text="確認するカードを1つ選択")
                    game_action_3(player)
                elif state[4+player] == 6:
                    text_inst.config(text="入れ替える手札を1つ選択")
                    game_action_2(player)
                elif state[4+player] == 8:
                    rd = rand.randint(1,20)
                    if rd < 4:
                        pl = 0
                    else:
                        pl = rand.randint(1,state[1])
                    index = rand.randint(1,len(str_rule[pl])) - 1
                    delete_rule.append([pl,index])
                    if pl == 0:
                        log = f"Playerは抹勝対象にPlayerの「{str_rule[pl][index]}」を選択しました"
                    else:
                        log = f"Playerは抹勝対象にCPU{pl}の「{str_rule[pl][index]}」を選択しました"
                    label = tk.Label(frame_log, text=log, bg="white")
                    label.pack(padx=5, pady=3, anchor="w")
                    update_log()
            elif n == 2:
                text_inst.config(text="入れ替える手札を1つ選択")
                game_action_2(player)
                if state[4+player] == 5:
                    loop = 2
                    for i in range(loop):
                        display_field(1)
                        text_inst.config(text=f"確認するカードを{loop-i}つ選択")
                        game_action_3(player)
                elif state[4+player] == 6:
                    text_inst.config(text="入れ替える手札を1つ選択")
                    game_action_2(player)
                button_action1.config(bg="white")
                if state[4+player] in {3, 7}:
                    button_action4.config(bg="white")
                limit_massh[player] += 2
                if limit_massh[player] > 5:
                    limit_massh[player] = 5
            elif n == 3:
                loop = 2
                if state[4+player] == 3:
                    loop = 3
                elif state[4+player] == 5:
                    loop = 4
                for i in range(loop):
                    display_field(1)
                    text_inst.config(text=f"確認するカードを{loop-i}つ選択")
                    game_action_3(player)
                    if varA.get() == -1:
                        break
                limit_massh[player] += 2
                if limit_massh[player] > 5:
                    limit_massh[player] = 5
            elif n == 4:
                game_action_4(0, state[4+player])
                limit_skill[player] -= 1
                if limit_skill[player] == 0:
                    button_action4.config(bg="gray")

#アクション1 : 抹勝(1) standard
def game_action_1(n):
    limit_massh[n] -= 1
    if n == 0:
        state[0] = "selectRule"
        varA.set(0)  #勝利条件がクリックされるまで
        root.wait_variable(varA)
        if limit_massh[n] == 0:
            button_action1.config(bg="gray")
            if state[4+n] in {3, 7}:
                button_action4.config(bg="gray")
    else:
        game_select_rule_cpu(n)

#"selectRule"のときに実行
def game_select_rule_player(event, n):
    if state[0] == "selectRule":
        varA.set(1)
        state[0] = "waiting"
        index = str_rule_card[n].index(event.widget)
        delete_rule.append([n,index])
        log = f"Playerは抹勝対象にCPU{n}の「{str_rule[n][index]}」を選択しました"
        label = tk.Label(frame_log, text=log, bg="white")
        label.pack(padx=5, pady=3, anchor="w")
        update_log()

#アクション2 : 入替(1) standard
def game_action_2(n):
    if n == 0:
        state[0] = "selectChange"
        varA.set(0)  #手札がクリックされるまで
        root.wait_variable(varA)
        log = "Player"
    else:
        log = "CPU" + str(n)
    log += "は手札入れ替えを使用しました"
    label = tk.Label(frame_log, text=log, bg="white")
    label.pack(padx=5, pady=3, anchor="w")
    update_log()

#アクション3 : 確認(1) standard
def game_action_3(n):
    if n == 0:
        state[0] = "selectConfirm"
        varA.set(0)  #カードがクリックされるまで
        root.wait_variable(varA)
        log = "Player"
    else:
        log = "CPU" + str(n)
    log += "は隠された要素の確認を使用しました"
    label = tk.Label(frame_log, text=log, bg="white")
    label.pack(padx=5, pady=3, anchor="w")
    update_log()

#アクション4 : 固有
def game_action_4(n, cha):
    if cha == 1:
        if n == 0:
            log = "Player"
            text_inst.config(text="手札から出すカードを1つ選択")
            state[0] = "selectCard"
            varA.set(0)  #手札のカードがクリックされるまで
            root.wait_variable(varA)
        else:
            log = "CPU" + str(n)
        log += "は追加カード使用権を使用しました"
        label = tk.Label(frame_log, text=log, bg="white")
        label.pack(padx=5, pady=3, anchor="w")
        update_log()
        limit_massh[n] += 2
        if limit_massh[n] > 5:
            limit_massh[n] = 5
    elif cha == 3:
        if n == 0:
            log = "Player"
        else:
            log = "CPU" + str(n)
        log += "は固有アクションを使用しました"
        label = tk.Label(frame_log, text=log, bg="white")
        label.pack(padx=5, pady=3, anchor="w")
        update_log()
        game_action_1(n)
        game_action_2(n)
        game_action_3(n)
        game_action_3(n)
    elif cha == 7:
        game_action_1(n)
        delete_rule.append([n,-1])
        if n == 0:
            log = "Player"
        else:
            log = "CPU" + str(n)
        log += "は抹勝無効を使用しました"
        label = tk.Label(frame_log, text=log, bg="white")
        label.pack(padx=5, pady=3, anchor="w")
        update_log()

#フィールドのカードが選択された時実行
def select_field_card(i, n, text):
    if state[0] == "selectConfirm":
        if str_field_card_confirm[n][i]:
            if any(False in row for row in str_field_card_confirm):
                print("未確認のカードを選択してください")
            else:
                varA.set(-1)
                print("全て公開されています")
        else:
            varA.set(1)
            state[0] = "waiting"
            filename = "image/" + text + ".png"
            img = Image.open(filename)
            img = img.resize((45, 45))
            card_image = ImageTk.PhotoImage(img)
            str_field_card_T[n][i].config(image = card_image)
            str_field_card_confirm[n][i] = True
            image_objects.append(card_image)

def game_select_action_cpu():
    for cp in range(1, state[1]):
        if limit_massh[cp] > 0:
            ac = rand.randint(0,3)
        else:
            ac = rand.randint(2,3)
        if state[4+cp] == 1 and state[2] > 5 and limit_skill[cp] > 0:
            rd = rand.randint(1,4)
            if rd == 1:
                ac = 4
        elif state[4+cp] == 3 and state[2] > 1 and limit_skill[cp] > 0 and limit_massh[cp] > 0:
            rd = rand.randint(1,3)
            if rd == 1:
                ac = 4
        elif state[4+cp] == 7 and state[2] > 4 and limit_skill[cp] > 0 and limit_massh[cp] > 0:
            rd = rand.randint(1,2)
            if rd == 1:
                ac = 4
        if ac in {0,1} or limit_massh[cp] == 5:
            game_action_1(cp)
            if state[4+cp] == 4:
                game_action_3(cp)
            elif state[4+cp] == 6:
                game_action_2(cp)
            elif state[4+cp] == 8:
                rd = rand.randint(1,20)
                if rd < 4:
                    pl = cp
                else:
                    pl = rand.randint(0,state[1]-2)
                    if pl >= cp:
                        pl += 1
                index = rand.randint(1,len(str_rule[pl])) - 1
                delete_rule.append([pl,index])
                if pl == 0:
                    log = f"CPU{cp}は抹勝対象にPlayerの「{str_rule[pl][index]}」を選択しました"
                else:
                    log = f"CPU{cp}は抹勝対象にCPU{pl}の「{str_rule[pl][index]}」を選択しました"
                label = tk.Label(frame_log, text=log, bg="white")
                label.pack(padx=5, pady=3, anchor="w")
        elif ac == 2:
            game_action_2(cp)
            if state[4+cp] == 5:
                for i in range(2):
                    game_action_3(cp)
            elif state[4+cp] == 6:
                game_action_2(cp)
            limit_massh[cp] += 2
            if limit_massh[cp] > 5:
                limit_massh[cp] = 5
        elif ac == 3:
            loop = 2
            if state[4+cp] == 3:
                loop = 3
            elif state[4+cp] == 5:
                loop = 4
            for i in range(loop):
                game_action_3(cp)
            limit_massh[cp] += 2
            if limit_massh[cp] > 5:
                limit_massh[cp] = 5
        elif ac == 4:
            game_action_4(cp, state[4+cp])
            limit_skill[cp] -= 1

#CPUが消去したい勝利条件を選択する関数（現状：完全ランダム）
def game_select_rule_cpu(cp):
    p = rand.randint(0, state[1]-2)
    if p >= cp:
        p += 1
    index = rand.randint(0, len(str_rule[p])-1)
    delete_rule.append([p,index])
    if p == 0:
        log = f"CPU{cp}は抹勝対象にPlayerの「{str_rule[p][index]}」を選択しました"
    else:
        log = f"CPU{cp}は抹勝対象にCPU{p}の「{str_rule[p][index]}」を選択しました"
    label = tk.Label(frame_log, text=log, bg="white")
    label.pack(padx=5, pady=3, anchor="w")
    update_log()

#削除を実行する関数
def game_delete_rule():
    hold = -1
    for i in range(state[1]):
        if state[4+i] == 7:
            if [i,-1] in delete_rule:
                delete_rule.remove([i,-1])
                hold = i
    delete = [list(t) for t in set(tuple(log) for log in delete_rule)]
    already = []
    for log in delete:
        if log[0] != hold:
            target = log[1]
            for i in already:
                if log[0] == i:
                    target -= 1
            if log[0] == 0:
                logt = f"Playerの「{str_rule[log[0]][target]}」が抹勝されました"
            else:
                logt = f"CPU{log[0]}の「{str_rule[log[0]][target]}」が抹勝されました"
            label = tk.Label(frame_log, text=logt, bg="white")
            label.pack(padx=5, pady=3, anchor="w")
            update_log()
            str_rule_card[log[0]][target].pack_forget()
            str_rule_card[log[0]].pop(target)
            str_rule[log[0]].pop(target)
            already.append(log[0])

#フィールドに出ている要素をカウントする関数
def game_field_count(fieldP, n, e, m):
    if (n-1) >= 0:
        fieldP[n-1] += 1
    if (N+e-1) >= 0:
        fieldP[N+e-1] += 1
    if (N+E+m-1) >= 0:
        fieldP[N+E+m-1] += 1

#フィールドに出ている要素を表示する関数
def game_field_state(fieldP):
    text = ""
    for i in range(len(fieldP)):
        if i < N:
            text += change_N(i+1) + ":"
        elif i < (N+E):
            text += change_E_text(i-N+1) + ":"
        else:
            text += change_M(i-N-E+1) + ":"
        text += str(fieldP[i]) + "\n"
    return text

#勝利条件を満たしているか判定する関数(n=0:Player, n=1~3:CPU1~3)
def game_judge():
    for i in range(state[1]):
        jud = False
        rulesP = str_rule[i]
        fieldP = str_field[i]
        for l in range(len(rulesP)):
            rule = [item for part in rulesP[l].split("/") for item in part.split(":")]
            for j in range(int(len(rule)/2)):
                if rule[2*j] == "A":
                    index = 0
                elif rule[2*j] == "B":
                    index = 1
                elif rule[2*j] == "C":
                    index = 2
                elif rule[2*j] == "D":
                    index = 3
                elif rule[2*j] == "E":
                    index = 4
                elif rule[2*j] == "赤":
                    index = 5
                elif rule[2*j] == "青":
                    index = 6
                elif rule[2*j] == "緑":
                    index = 7
                elif rule[2*j] == "黄":
                    index = 8
                elif rule[2*j] == "●":
                    index = 9
                elif rule[2*j] == "★":
                    index = 10
                elif rule[2*j] == "▲":
                    index = 11
                if fieldP[index] >= int(rule[2*j+1]):
                    jud = True
                else:
                    jud = False
                    break
            if jud:
                break
        if jud:
            win_rule.append([i,l])
            winner.append(i)

#ターン終了時の処理
def game_turn_end():
    for i in range(state[1]):
        if len(cards) > 0:
            text_limit_count1[i].config(text=f"抹勝：残り{limit_massh[i]}回")
            if state[4+i] in {1,3,7}:
                text_limit_count2[i].config(text=f"スキル：残り{limit_skill[i]}回")
            if i == 0:
                newcard = cards.pop(0)
                hands_set_ref(newcard, select_rec[0], 0)
                select_rec[0] = 0
                state[0] = "selectCard"
                delete_rule.clear()
                text_inst.config(text="手札のカードを1つ選択 → 決定ボタン")
            else:
                str_hand[i].append(cards.pop(0))
        else:
            cvs_finish.place(x=300,y=100)
            text_winner_rule.config(text="引き分け")

#ゲーム終了時の処理
def game_result():
    cvs_finish.place(x=300,y=200)
    winner_name = "勝者："
    for i in winner:
        if i == 0:
            winner_name += "Player "
        else:
            winner_name += f"CPU{i} "
    text_winner.config(text=winner_name, fg="#0000aa")
    winner_rule = ""
    for R in win_rule:
        winner_rule += "「" + str_rule[R[0]][R[1]] + "」"
    text_winner_rule.config(text=winner_rule)
    frame_finish.place(x=250, y=150, anchor="center")

def game_return():
    game_clear()
    cvs_finish.place_forget()
    cvs_playgame.place_forget()
    cvs_title.place(x=0, y=0)

#初期化
def game_clear():
    def frame_clear(frame):
        for widget in frame.winfo_children():
            widget.destroy()
    for i in range(state[1]):
        str_hand[i].clear()
        str_field_T[i].clear()
        str_field_card[i].clear()
        str_field_card_T[i].clear()
        str_field_card_confirm[i].clear()
        str_rule[i].clear()
        str_rule_card[i].clear()
        for j in range(5+4+3):
            str_field[i][j] = 0
        frame_clear(frame_field_all[i])
        frame_clear(frame_field_all_T[i])
        frame_clear(frame_rules_all[i])
    text_hand.clear()
    delete_rule.clear()
    cards.clear()
    rules.clear()
    winner.clear()
    win_rule.clear()
    limit_skill.clear()
    limit_massh
    state[0] = "waiting"
    state[2] = 0
    state[3] = True
    frame_clear(frame_log)
    for i in range(4):
        select_rec[i] = 0
    for framehand in frame_hands:
        frame_clear(framehand)

#main
def game_main():
    game_set()
    while len(winner) == 0:
        state[2] += 1
        label = tk.Label(frame_log, text=f"{state[2]}ターン目", font=("MSゴシック",12,"bold"), bg="white")
        label.pack(padx=5, pady=3, anchor="w")
        text_inst.config(text="手札から出すカードを1つ選択")
        state[0] = "selectCard"
        var.set(0)  #手札のカードがクリックされるまで
        root.wait_variable(var)
        game_select_card_cpu()
        frame_panel_action.place(x=300, y=472)
        text_inst.config(text="アクションを1つ選択")
        state[0] = "selectAction"
        var.set(0)  #アクションボタンがクリックされるまで
        root.wait_variable(var)
        state[0] = "waiting"
        game_select_action_cpu()
        game_delete_rule()
        game_judge()
        game_turn_end()
    game_result()


#ウィンドウ
root = tk.Tk()
root.title("抹勝")
root.geometry("1252x620")
root.minsize(1252,620)
WIDTH = 1252
HEIGHT = 620
var = tk.IntVar(value=0)
varA = tk.IntVar(value=0)


#タイトル画面
cvs_title = tk.Canvas(root, width=WIDTH, height=HEIGHT)
frame_title = tk.Frame(cvs_title, width=1252, height=620)
frame_title.place(x=0, y=0)
frame_title.pack_propagate(False)
text_title = tk.Label(frame_title, text="抹 勝", font=("MSゴシック",72, "bold"), fg="#003600")
text_title.pack(pady=100)
button_start3 = tk.Button(frame_title, text="3人プレイ", font=("MSゴシック",30, "bold"), command=lambda: character_set(3))
button_start4 = tk.Button(frame_title, text="4人プレイ", font=("MSゴシック",30, "bold"), command=lambda: character_set(4))
button_start3.pack(pady=100)
#button_start4.pack(pady=100)
cvs_title.place(x=0, y=0)


#キャラクター設定画面
cvs_character_select = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#003600")
frame_characters = tk.Frame(cvs_character_select, bg="#006000")
image_objects = []
for i in range(8):
    num = str(i+1).zfill(2)
    image_C = create_character_image(num,100,100,1)
    image_objects.append(image_C)
    button_character = tk.Button(frame_characters, image=image_C, command=lambda i=i: character_select(i+1), bg="#ffffff")
    button_character.grid(column=i%4, row=int(i//4), padx=10, pady=10)
frame_characters.place(x=20, y=70)
button_character_C = tk.Button(cvs_character_select, text="決定", font=("MSゴシック",18,"bold"), command=lambda: character_select(0))
button_character_C.place(x=220, y=400)
text_character_title = tk.Label(cvs_character_select, text="キャラクター選択", font=("MSゴシック",24,"bold"), fg="#ffffdd", bg="#003600")
text_character_title.place(x=30, y=10)
text_character_name = tk.Label(cvs_character_select, text="", font=("MSゴシック",36,"bold"), fg="#ddddff", bg="#003600")
text_character_name.place(x=600, y=50)
text_character_image = tk.Label(cvs_character_select, fg="#ffffdd", bg="#003600")
text_character_image.place(x=700, y=100)
text_character_skill = tk.Label(cvs_character_select, text="", font=("MSゴシック",18,"bold"), fg="#ffffdd", bg="#003600", anchor="w", justify="left")
text_character_skill.place(x=630, y=450)


#ゲーム画面
cvs_playgame = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#003600")
text_name_top = []
text_name_top.append(tk.Label(cvs_playgame, text="Player", font=("MSゴシック",18,"bold"), fg="#ffffdd", bg="#003600"))
text_name_top.append(tk.Label(cvs_playgame, text="CPU-1", font=("MSゴシック",18,"bold"), fg="white", bg="#003600"))
text_name_top.append(tk.Label(cvs_playgame, text="CPU-2", font=("MSゴシック",18,"bold"), fg="white", bg="#003600"))
text_name_top.append(tk.Label(cvs_playgame, text="CPU-3", font=("MSゴシック",18,"bold"), fg="white", bg="#003600"))
image_character_top = []
text_limit_count1 = []
text_limit_count2 = []
for i in range(4):
    image_player = tk.Label(cvs_playgame, fg="#ffffdd", bg="#003600")
    image_character_top.append(image_player)
    text_limit_count1.append(tk.Label(cvs_playgame, text="抹勝：残り2回", font=("MSゴシック",10,"bold"), fg="white", bg="#003600"))
    text_limit_count2.append(tk.Label(cvs_playgame, text="スキル：残り2回", font=("MSゴシック",10,"bold"), fg="white", bg="#003600"))

#フィールド,勝利条件のフレーム
frame_field_all = []
frame_field_all_T = []
frame_rules_all = []
for i in range(4):
    frame_field = tk.Frame(cvs_playgame, width=1200, height=220, bg="#003600", bd=0, highlightthickness=0)
    frame_field_all.append(frame_field)
    frame_field_T = tk.Frame(cvs_playgame, width=1200, height=220, bg="#003600", bd=0, highlightthickness=0)
    frame_field_all_T.append(frame_field_T)
    frame_rules = tk.Frame(cvs_playgame, width=1200, height=200, bg="#003600", bd=0, highlightthickness=0)
    frame_rules_all.append(frame_rules)

#手札全体のフレーム
frame_hand = tk.Frame(cvs_playgame, width=WIDTH, height=95, bg="#108010")
frame_hand.place(x=0, y=525)
frame_hand.pack_propagate(False)
#手札のカードのフレーム 1~5
frame_hands = []
for i in range(5):
    frame_hands.append(tk.Frame(frame_hand, width=110, height=85, bg="white", highlightbackground="white", highlightthickness=3))
    frame_hands[i].bind("<Button-1>", lambda event, idx=i+1: game_select_card_player(event, idx))
image_player_main = tk.Label(frame_hand, fg="#ffffdd", bg="#108010")
image_player_main.place(x=1030,y=0)

#行動台詞ラベル
text_inst = tk.Label(frame_hand, text="", font=("MSゴシック",12,"bold"), fg="black", bg="white", highlightbackground="black", highlightthickness=1)
text_inst.place(x=1000, y=20, anchor="e")

#隠す要素選択フレーム
frame_panel_hide = tk.Frame(root, bg="#108010")
button_hide_N = tk.Button(frame_panel_hide, text="文字", font=("MSゴシック",16,"bold"), fg="black", bg="white", command=lambda: game_select_hide(1))
button_hide_E = tk.Button(frame_panel_hide, text="色", font=("MSゴシック",16,"bold"), fg="black", bg="white", command=lambda: game_select_hide(2))
button_hide_M = tk.Button(frame_panel_hide, text="記号", font=("MSゴシック",16,"bold"), fg="black", bg="white", command=lambda: game_select_hide(3))
button_hide_N.pack(side=tk.LEFT, padx=10, pady=6)
button_hide_E.pack(side=tk.LEFT, padx=10, pady=6)
button_hide_M.pack(side=tk.LEFT, padx=10, pady=6)

#アクション選択フレーム
frame_panel_action = tk.Frame(root, bg="#108010")
button_action1 = tk.Button(frame_panel_action, text="", font=("MSゴシック",16,"bold"), fg="black", bg="white", command=lambda: game_select_action(1, 0))
button_action2 = tk.Button(frame_panel_action, text="", font=("MSゴシック",16,"bold"), fg="black", bg="white", command=lambda: game_select_action(2, 0))
button_action3 = tk.Button(frame_panel_action, text="", font=("MSゴシック",16,"bold"), fg="black", bg="white", command=lambda: game_select_action(3, 0))
button_action4 = tk.Button(frame_panel_action, text="", font=("MSゴシック",16,"bold"), fg="black", bg="white", command=lambda: game_select_action(4, 0))
button_action1.pack(side=tk.LEFT, padx=10, pady=6)
button_action2.pack(side=tk.LEFT, padx=10, pady=6)
button_action3.pack(side=tk.LEFT, padx=10, pady=6)
button_action4.pack(side=tk.LEFT, padx=10, pady=6)


#終了画面
cvs_finish = tk.Canvas(root, width=500, height=300, bg="white")
frame_finish = tk.Frame(cvs_finish, bg="white")
text_winner = tk.Label(frame_finish, text="", font=("MSゴシック",30,"bold"), fg="black", bg="white", highlightbackground="black", highlightthickness=1)
text_winner.pack(pady=30)
text_winner_rule = tk.Label(frame_finish, text="", font=("MSゴシック",18,"bold"), fg="black", bg="white", highlightbackground="black", highlightthickness=1)
text_winner_rule.pack(pady=20)
button_return = tk.Button(frame_finish, text="タイトルに戻る", font=("MSゴシック",16,"bold"), fg="black", bg="white", command=lambda: game_return())
button_return.pack(pady=15)


#ルール説明文表示
def display_rule():
    if state_display[0]:
        button_discribe.config(bg="yellow")
        cvs_discribe.place(x=300, y=50)
        state_display[0] = False
        if state_display[1] == False:
            display_log()
    else:
        button_discribe.config(bg="white")
        cvs_discribe.place_forget()
        state_display[0] = True
def display_discraibe_B():
    if state[3] > 0:
        if state[3] == len(text_discribe)-1:
            button_discribe_next.config(bg="white")
        text_discribe[state[3]].place_forget()
        state[3] -= 1
        text_discribe[state[3]].place(x=25, y=25)
        if state[3] == 0:
            button_discribe_back.config(bg="gray")
def display_discraibe_N():
    if state[3] < len(text_discribe)-1:
        if state[3] == 0:
            button_discribe_back.config(bg="white")
        text_discribe[state[3]].place_forget()
        state[3] += 1
        text_discribe[state[3]].place(x=25, y=25)
        if state[3] == len(text_discribe)-1:
            button_discribe_next.config(bg="gray")
img = Image.open("image/button_rule.png")
img = img.resize((30, 30))
display_rule_image = ImageTk.PhotoImage(img)
image_objects.append(display_rule_image)
button_discribe = tk.Button(root, image=display_rule_image, command=lambda: display_rule())
button_discribe.place(x=1210, y=20)
#ルール表示画面
cvs_discribe = tk.Canvas(root, width=700, height=500, bg="#ddddff")
image_discribe = []
text_discribe = []
for i in range(2):
    title = "image/Rule" + str(i+1) + ".png"
    img = Image.open(title)
    img = img.resize((650, 400))
    img = ImageTk.PhotoImage(img)
    image_discribe.append(img)
    text_discribe.append(tk.Label(cvs_discribe, image=img, bg="white"))
text_discribe[0].place(x=25, y=25)
button_discribe_back = tk.Button(cvs_discribe, text="←", font=("MSゴシック",16,"bold"), bg="gray", command=lambda: display_discraibe_B())
button_discribe_back.place(x=25, y=475, anchor="sw")
button_discribe_next = tk.Button(cvs_discribe, text="→", font=("MSゴシック",16,"bold"), bg="white", command=lambda: display_discraibe_N())
button_discribe_next.place(x=675, y=475, anchor="se")


def display_field(s):
    if state[8] == 0:
        button_field_change.config(bg="yellow")
        w = int(1200/state[1])
        for i in range(state[1]):
            frame_field_all[i].place_forget()
            frame_field_all_T[i].place(x=w*i+2,y=48)
        state[8] = 1
    elif state[8] == 1:
        if s == 0:
            button_field_change.config(bg="white")
            w = int(1200/state[1])
            for i in range(state[1]):
                frame_field_all_T[i].place_forget()
                frame_field_all[i].place(x=w*i+2,y=48)
            state[8] = 0
img = Image.open("image/button_field.png")
img = img.resize((30, 30))
display_field_image = ImageTk.PhotoImage(img)
image_objects.append(display_field_image)
button_field_change = tk.Button(cvs_playgame, image=display_field_image, command=lambda: display_field(0))
button_field_change.place(x=1210, y=80)


#ログ表示
def display_log():
    if state_display[1]:
        button_log.config(bg="yellow")
        cvs_log_frame.place(x=300, y=50)
        state_display[1] = False
        if state_display[0] == False:
            display_rule()
    else:
        button_log.config(bg="white")
        cvs_log_frame.place_forget()
        state_display[1] = True
img = Image.open("image/button_log.png")
img = img.resize((30, 30))
display_log_image = ImageTk.PhotoImage(img)
image_objects.append(display_log_image)
button_log = tk.Button(cvs_playgame, image=display_log_image, command=lambda: display_log())
button_log.place(x=1210, y=140)
#ログ表示画面
cvs_log_frame = tk.Canvas(root, width=700, height=500, bg="#ddddff")
text_log_title = tk.Label(cvs_log_frame, text="ログ", font=("MSゴシック",18,"bold"), fg="black", bg="#ddddff")
text_log_title.place(x=300, y=20)
frame_log_set = tk.Frame(cvs_log_frame)
cvs_log = tk.Canvas(frame_log_set, width=650, height=400, bg="white")
cvs_log_scroll = tk.Scrollbar(frame_log_set, orient="vertical", command=cvs_log.yview)
cvs_log.configure(yscrollcommand=cvs_log_scroll.set)
cvs_log_scroll.pack(side="right", fill="y")
cvs_log.pack(side="left", fill="both", expand=True)
frame_log = tk.Frame(cvs_log, bg="white")
window_id = cvs_log.create_window((0, 0), window=frame_log, anchor="nw")
def on_frame_configure(event):
    cvs_log.config(scrollregion=cvs_log.bbox("all"))
def on_mouse_wheel(event):
    cvs_log.yview_scroll(-1 * (event.delta // 120), "units")
cvs_log.bind("<Configure>", on_frame_configure)
cvs_log.bind("<MouseWheel>", on_mouse_wheel)
def update_log():
    frame_log.update_idletasks()
    cvs_log.config(scrollregion=cvs_log.bbox("all"))
frame_log_set.place(x=20, y=70)


def window_close():
    var.set(1)
    varA.set(1)
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", window_close)


root.mainloop()