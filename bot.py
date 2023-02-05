from telethon.sync import TelegramClient
import pandas
import pretty_html_table
# Your api_id
app_api_id = 12345
# Your api_hash
app_api_hash = "Your api_hash"
telegram_client = TelegramClient("parser_bot", app_api_id, app_api_hash)
telegram_client.start()
def get_participants_from_chat(limit):
    """
    Найти пользователей одного канала за выбором.
    :param limit:
        Лимит пользователей, которых мы хотим найти.

    """
    all_channels = [i for i in list(telegram_client.iter_dialogs()) if
                    i.title != '' and i.is_channel == True or i.is_group == True]
    for i in range(len(all_channels)):
        print(f"{i} - {all_channels[i].title}")

    ask = int(input("Из какого паблика хотите получить пользователей?: "))
    all_members_with_limit = [i for i in telegram_client.iter_participants(entity=all_channels[ask], limit=limit)]
    members_data = {'id': [], 'username': [], 'firstname': [], 'group': []}
    counter = 1
    for member in all_members_with_limit:
        members_data['id'].append(counter)
        members_data['username'].append(member.username)
        members_data['firstname'].append(member.first_name)
        members_data['group'].append(all_channels[ask].title)
        counter+=1
    with open('index.html', 'w', encoding='utf-8') as html:
        html.write(pretty_html_table.build_table(pandas.DataFrame.from_dict(members_data), 'orange_dark'))
        print('The result is saved in index.html')
    return all_members_with_limit

def get_participants_from_all_possible_chats(limit):
    """
    Найти пользователей со всех возможных каналов.
    :param limit:
        Лимит пользователей с каждого канала.
    """
    all_channels = [i for i in list(telegram_client.iter_dialogs()) if
                    i.title != '' and i.is_channel == True or i.is_group == True]
    members_data = {'id': [], 'username': [], 'firstname': [], 'group': []}
    counter = 1
    for i in all_channels:
        try:
            all_members_with_limit = [k for k in telegram_client.iter_participants(entity=i, limit=limit)]
            for member in all_members_with_limit:
                members_data['id'].append(counter)
                members_data['username'].append(member.username)
                members_data['firstname'].append(member.first_name)
                members_data['group'].append(i.title)
                counter += 1

        except:
            print(f"[Error]: Can't get participants from {i.title}")

    with open('index.html', 'w', encoding='utf-8') as html:
        html.write(pretty_html_table.build_table(pandas.DataFrame.from_dict(members_data), 'orange_dark'))
        print('The result is saved in index.html')

    return members_data

def parse_channel(limit):
    """
    Найти все посты с канала
    :param limit:
        Лимит постов
    """
    all_channels = [i for i in list(telegram_client.iter_dialogs())]
    for i in range(len(all_channels)):
        print(f"{i} - {all_channels[i].title}")

    ask = int(input("Из какого паблика хотите получить сообщения?: "))
    all_messages_with_limit = list(telegram_client.iter_messages(entity=all_channels[ask], limit=limit))
    messages_data = {"Id": [], "Group": [], "Message": [], "Date": []}
    counter = 1
    try:
        for i in all_messages_with_limit:
            messages_data["Id"].append(counter)
            messages_data["Group"].append(all_channels[ask].name)
            messages_data["Message"].append(i.message)
            messages_data["Date"].append(i.date)
            counter += 1

    except:
        print('[Error]')
    with open('index.html', 'w', encoding='utf-8') as html:
        html.write(pretty_html_table.build_table(pandas.DataFrame.from_dict(messages_data), 'orange_dark'))
        print('The result is saved in index.html')

    return all_messages_with_limit[0]

def parse_channel_by_stopwords(limit, words):
    """
    Найти посты за стоп-словами.
    :params:
        limit:
            Лимит сообщений, которые будут просматриваться
        words:
            Строка из стоп-слов, записанных через пробел.
    """
    all_channels = [i for i in list(telegram_client.iter_dialogs())]
    for i in range(len(all_channels)):
        print(f"{i} - {all_channels[i].title}")

    ask = int(input("Из какого паблика хотите получить сообщения за стоп-словами?: "))
    all_messages_with_limit = list(telegram_client.iter_messages(entity=all_channels[ask], limit=limit))
    result_messages = []
    messages_data = {"Id": [], "Group": [], "Message": [], "Date": []}
    stop_words = words.split(' ')
    counter = 1
    try:
        for i in all_messages_with_limit:
            for k in stop_words:
                if k.lower() in i.message.lower():
                    result_messages.append(i)
                    messages_data["Id"].append(counter)
                    messages_data["Group"].append(all_channels[ask].name)
                    messages_data["Message"].append(i.message)
                    messages_data["Date"].append(i.date)
                    counter += 1
                    break

    except:
        print('[Error]')

    with open('index.html', 'w', encoding='utf-8') as html:
        html.write(pretty_html_table.build_table(pandas.DataFrame.from_dict(messages_data), 'orange_dark'))
        print('The result is saved in index.html')
    return result_messages


# print(parse_channel(50))
# get_participants_from_chat(50)
# get_participants_from_all_possible_chats(50)
# parse_channel_by_stopwords(1000, 'я')

