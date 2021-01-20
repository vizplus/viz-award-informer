import json
import os
import sys
from datetime import datetime

from tvizbase.api import Api

#Loading settings from the json file
with open(os.path.dirname(__file__) + '/settings.json', 'r') as sett_file:
    settings = json.load(sett_file)
viz = Api()
#Getting the head block number from the blockchain
block_num = viz.get_dynamic_global_properties()['head_block_number']
#Number of blocks for energy recovery
block_count = (20 * 60 * 24 / 20) * settings['award_percent']
#Blcok delay for posting in the blockchain
block_count -= 2
#Comparing the head block number with the number of the last operation
if block_num <= settings['last_block_num'] + block_count:
    sys.exit()
#Getting account data
account = viz.get_accounts([settings['viz_account']['login']])[0]
receiver = 'committee'
#Calculating percentage of the award
award_percent = round(settings['award_percent'] * 100 * settings['award_base'] /
                      account['SHARES'])
#Sending award in the blockchain
res = viz.award(settings['viz_account']['login'], 
                receiver, 
                award_percent, 
                settings['viz_account']['key'])
if res == False:
    sys.exit()
#Saving the last operation block number in the json file
settings['last_block_num'] = res['block_num']
with open(os.path.dirname(__file__) + '/settings.json', 'w') as sett_file:
    json.dump(settings, sett_file)
#Getting current award size from the virtual operations
ops = viz.get_ops_in_block(int(res['block_num']))
for op in ops:
    op = op['op']
    if (op[0] == 'receive_award' and 
        op[1]['initiator'] == settings['viz_account']['login'] and 
        op[1]['receiver'] == receiver
    ):
        award_size = round(float(op[1]['shares'].split()[0]) * (100 / settings['award_percent']) / settings['award_base'], 6)
        #Sending new custom operation in the blockchain
        viz.custom(
            'award_informer',
            [
                'award_informer',
                {
                    'time_utc': str(datetime.utcnow()),
                    'award_on_capital': award_size
                }
            ], 
            settings['viz_account']['login'], 
            settings['viz_account']['key']
        )
