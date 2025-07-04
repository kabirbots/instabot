from instagrapi import Client
import threading
import keyboard

USERNAME = "Choturdp45"
PASSWORD = "rdpfyter"
REPLY_MESSAGE = "tim ki  ma k boor me thappad mar dunga msg kese kiya 😭💗"

stop_flag = False
last_seen = {}
group_threads = set()

def listen_to_ctrl_s():
    global stop_flag
    keyboard.wait("ctrl+s")
    print("🛑 Ctrl + S pressed — stopping all bots...")
    stop_flag = True

def handle_group(cl, thread, my_user_id):
    global last_seen, stop_flag

    thread_id = thread.id
    group_name = ", ".join([u.username for u in thread.users]) or thread_id

    while not stop_flag:
        try:
            messages = cl.direct_messages(thread_id, amount=1)
            if not messages:
                continue

            latest_msg = messages[0]
            msg_id = latest_msg.id
            sender_id = latest_msg.user_id

            if (
                msg_id != last_seen.get(thread_id)
                and sender_id != my_user_id
            ):
                cl.direct_send(REPLY_MESSAGE, thread_ids=[thread_id])
                print(f"📨 Replied instantly in group: {group_name}")
                last_seen[thread_id] = msg_id

        except Exception as e:
            print(f"⚠️ [Group: {group_name}] Error: {e}")

        # ❌ No sleep here — instant re-check loop

def auto_reply():
    global group_threads
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    my_user_id = cl.user_id_from_username(USERNAME)  # Ensure real self ID
    print("✅ Logged in as:", USERNAME)
    print("🤖 Running in MAX SPEED mode (no sleep)... Press Ctrl + S to stop.")

    while not stop_flag:
        try:
            threads = cl.direct_threads(amount=100)

            for thread in threads:
                if not thread.users or len(thread.users) <= 1:
                    continue

                if thread.id not in group_threads:
                    group_threads.add(thread.id)
                    t = threading.Thread(target=handle_group, args=(cl, thread, my_user_id), daemon=True)
                    t.start()
                    group_name = ", ".join([u.username for u in thread.users])
                    print(f"🚀 Listening to group: {group_name}")

        except Exception as e:
            print(f"⚠️ Main Loop Error: {e}")

        # ❌ No sleep — check new groups constantly

# Ctrl+S stop listener
threading.Thread(target=listen_to_ctrl_s, daemon=True).start()

# Start bot
auto_reply()
