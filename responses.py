import json
from random import choice, randint
import os
import datetime

# File to store the currency data
CURRENCY_FILE = 'currency.json'

# Load the current balances or create a new file if it doesn't exist
if os.path.exists(CURRENCY_FILE):
    with open(CURRENCY_FILE, 'r') as file:
        user_balances = json.load(file)
else:
    user_balances = {}

def save_balances():
    """Save the current balances to the JSON file."""
    with open(CURRENCY_FILE, 'w') as file:
        json.dump(user_balances, file, indent=4)

def betting(messages: str ,user_id: str)-> str: 
    For_bet = messages.split(" ")

    if ((For_bet[0] == "ouou") and (For_bet[1] == "bet") and (len(For_bet) == 3)):
        if not For_bet[2].isdigit():
            return f'Please specify a number that you want to bet <@{user_id}>! i.e ***ouou bet __amount__***'
        else:
            amount_bet = int(For_bet[2])
            current_balance = user_balances[user_id]['balance']
            if current_balance < amount_bet:
                return f'<@{user_id}> The amount you want to bet is greater than your balance!!!!!'
            current_time = datetime.datetime.now()
            last_bet_time = user_balances.get(user_id, {}).get('last_bet_time')
            if last_bet_time:
                time_since_last_bet = current_time - datetime.datetime.fromisoformat(last_bet_time)
                if time_since_last_bet < datetime.timedelta(seconds=12):
                    remaining_time = 12 - time_since_last_bet.seconds
                    return f'<@{user_id}> wait {remaining_time} more seconds before you can bet again.'
                
            Chance_of_win = randint(0,1)
            
            if Chance_of_win == 1:
                user_balances[user_id]['balance'] -= amount_bet
                earnings = (amount_bet * 2)
                user_balances[user_id] = user_balances.get(user_id, {'balance': 0})
                user_balances[user_id]['balance'] += earnings
                user_balances[user_id]['last_bet_time'] = current_time.isoformat()  # Store the current time as the last bet time
                save_balances()  # Save the updated balances
                return f'<@{user_id}>, you won :coin: {earnings}  coins!!'
            else:
                current_balance = user_balances[user_id]['balance']
                earnings = amount_bet 
                user_balances[user_id]['balance'] -= earnings
                user_balances[user_id]['last_bet_time'] = current_time.isoformat()  # Store the current time as the last scab time
                save_balances()  # Save the updated balances
                return f'<@{user_id}>, you lost :coin: {earnings}  coin!! L'
                
    else:
        return f''

def giving_money(messages: str ,user_id: str)-> str:
        give_money_split = [0] * 4
        give_money_split = messages.split(" ")
        recipient_userID = give_money_split[2]
        recipient_userID = recipient_userID.replace('<', '').replace('>', '').replace('@', '')

        if recipient_userID not in user_balances:
            return f'that user has not used an economy command before. ```ouou help for a full list of commands.```'
        else:
            if ((give_money_split[0] == "ouou") and (give_money_split[1] == "give") and (len(give_money_split) == 4)):
                if not give_money_split[3].isdigit():
                    return f'Please specify a number that you want to send <@{user_id}>! i.e ***ouou give user __amount__***'
                else:
                    amount_given = int(give_money_split[3])
                    current_balance = user_balances[user_id]['balance']
                    if current_balance < amount_given:
                        return f'The amount you want to give is greater than your balance <@{user_id}> !!!!!'
                    if amount_given == 0:
                        return f'You cannot send nothing <@{user_id}>'
                    else:
                        user_balances[recipient_userID]['balance'] += amount_given
                        user_balances[user_id]['balance'] -= amount_given
                        save_balances()
                        return f'<@{user_id}> has given <@{recipient_userID}> :coin: {amount_given} coins!'
            else:
                return f''

def get_response(user_input: str, user_id: str) -> str:
    messages: str = user_input.lower()

    if messages == '':
        return 'Well you\'re awfully silent'
    
    elif 'ouou help' in messages:
        return 'This is the full list of commands! \n **Economy :chart:** \n ==================== \n ouou balance, ouou work, ouou bet __*AMOUNT*__ \n \n **Social :tada:** \n ==================== \n This is still being expanded please dont be patient!'
    
    elif 'ouou balance' in messages:
        user_data  = user_balances.get(user_id, 0)
        balance = user_data['balance']
        return f'Your current balance is: __{balance}__ :coin: coins!'
    
    elif 'ouou work' in messages:
        # Get the current time
        current_time = datetime.datetime.now()
        
        # Check if the user has a last work time stored
        last_work_time = user_balances.get(user_id, {}).get('last_work_time')
        
        if last_work_time:
            time_since_last_work = current_time - datetime.datetime.fromisoformat(last_work_time)
            # Check if 12 hours have passed
            if time_since_last_work < datetime.timedelta(hours=12):
                remaining_time = datetime.timedelta(hours=12) - time_since_last_work
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                return f'You need to wait {hours} hours and {minutes} minutes before you can work again <@{user_id}> :('
        
        # If 12 hours have passed, or if the user has never worked before
        earnings = randint(50, 10000)
        user_balances[user_id] = user_balances.get(user_id, {'balance': 0})
        user_balances[user_id]['balance'] += earnings
        user_balances[user_id]['last_work_time'] = current_time.isoformat()  #Store the current time as the last work time
        save_balances()  # Save the updated balances

        return f'You worked and earned :coin: {earnings}  coins! Your new balance is :coin: {user_balances[user_id]["balance"]} coins.'
    
    
    elif 'ouou bet' in messages:
        return betting(messages,user_id)
    
    elif 'ouou give' in messages:
       return giving_money(messages, user_id)

    elif 'ouou' in messages:
        # If the message starts with 'ouou' but doesn't match any known command
        return choice(['My name is Jeff',
                       'Hallo ??',
                       'Low elo'])

    else:
        # Do nothing or return an empty string if 'ouou' is not present
        return ''
