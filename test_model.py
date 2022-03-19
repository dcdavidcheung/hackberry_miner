from get_data import get_prices, get_history
from decision import processData, decisionTree, followTree

from time import sleep

# Train model
trainIn = "train_data.csv"
maxDepth = 2

get_history(trainIn)
(trainTree, numAttr) = processData(trainIn)
finalTree = decisionTree(trainTree, maxDepth, numAttr)

# Initialize
prev_btc_price, prev_ltc_price = get_prices()
prev_label = 'btc'

while(1):
    new_btc, new_ltc = get_prices()
    btc_change = 'up' if (float(new_btc['price']) - float(prev_btc_price['price'])) >= 0 else 'down'
    ltc_change = 'up' if (float(new_ltc['price']) - float(prev_ltc_price['price'])) >= 0 else 'down'
    btc_percent_change = (float(new_btc['price']) - float(prev_btc_price['price'])) / float(prev_btc_price['price'])
    ltc_percent_change = (float(new_ltc['price']) - float(prev_ltc_price['price'])) / float(prev_ltc_price['price'])
    label = 'bp'
    infer = [btc_change, ltc_change, label]
    inference = followTree(finalTree, infer, maxDepth)

    if (prev_label == 'btc'):
        if (btc_change == 'up' or (btc_percent_change > ltc_percent_change)):
            guess = 'right'
        else:
            guess = 'wrong'
    else:
        if (ltc_change == 'up' or (ltc_percent_change > btc_percent_change)):
            guess = 'right'
        else:
            guess = 'wrong'

    print(f'Previous guess was {prev_label}, which seems to be {guess}')
    print(f'Mine {inference} now\n')

    prev_btc_price = new_btc
    prev_ltc_price = new_ltc
    prev_label = inference
    sleep(10)