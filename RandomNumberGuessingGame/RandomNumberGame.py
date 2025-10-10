import random

while True:
    print("\n BẮT ĐẦU TRÒ CHƠI ĐOÁN SỐ ")
    so_bi_mat = random.randint(1, 100)
    so_lan_doan = 0
    gioi_han = 7

    while so_lan_doan < gioi_han:
        du_doan = int(input(f"Lần {so_lan_doan + 1}/{gioi_han} - Nhập số bạn đoán: "))
        so_lan_doan += 1

        if du_doan < so_bi_mat:
            print("🔻 Số bạn đoán nhỏ hơn!")
        elif du_doan > so_bi_mat:
            print("🔺 Số bạn đoán lớn hơn!")
        else:
            print(f"Chính xác! Số bí mật là {so_bi_mat}.")
            print(f"Bạn đoán đúng sau {so_lan_doan} lần!")
            break
    else:
        print(f"Bạn đã hết {gioi_han} lần đoán! Số đúng là {so_bi_mat}.")

    # Hỏi người chơi có muốn chơi lại không
    choi_tiep = input("Bạn có muốn chơi lại không? (y/n): ").lower()
    if choi_tiep != "y":
        print("Cảm ơn bạn đã chơi!")
        break
