import requests

value = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "JACK": 11,
    "QUEEN": 12,
    "KING": 13,
    "ACE": 14
}

def get_new_deck():
    # Get the ID of the new deck
    api_path = "https://deckofcardsapi.com/api/deck"

    get_resp = requests.get(f"{api_path}/new/shuffle/?deck_count=1")

    if get_resp.ok:
        deck_id = get_resp.json()["deck_id"]
        return deck_id
    else:
        print(f"Not able to get ID. Failed with {get_resp.status_code}")
        print(f"Failure body: {get_resp.text}")

def play_cards(deck_id):
    # Draw two cards from the deck provided
    api_path = "https://deckofcardsapi.com/api/deck"
    get_resp = requests.get(f"{api_path}/{deck_id}/draw/?count=2")
    card1_value = value[get_resp.json()["cards"][0]["value"]]
    card2_value = value[get_resp.json()["cards"][1]["value"]]
    if card1_value == card2_value:
        print(f"It's a tie! First card was the {get_resp.json()['cards'][0]['value']} of {get_resp.json()['cards'][0]['suit'].lower()}.")
        print(f"The second card was the {get_resp.json()['cards'][1]['value']} of {get_resp.json()['cards'][1]['suit'].lower()}.")
        print(f"There are {get_resp.json()['remaining']} cards remaining")
    elif card1_value > card2_value:
        print(f"The first card wins!. First card was the {get_resp.json()['cards'][0]['value']} of {get_resp.json()['cards'][0]['suit'].lower()}.")
        print(f"The second card was the {get_resp.json()['cards'][1]['value']} of {get_resp.json()['cards'][1]['suit'].lower()}.")
        print(f"There are {get_resp.json()['remaining']} cards remaining")
    else:
        print(f"Second card wins! First card was the {get_resp.json()['cards'][0]['value']} of {get_resp.json()['cards'][0]['suit'].lower()}.")
        print(f"The second card was the {get_resp.json()['cards'][1]['value']} of {get_resp.json()['cards'][1]['suit'].lower()}.")
        print(f"There are {get_resp.json()['remaining']} cards remaining")

deck_id = get_new_deck()

play_cards(deck_id)