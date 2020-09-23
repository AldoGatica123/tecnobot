import datetime
import json
import logging

import pytz
from boto3.dynamodb.conditions import Attr
from chalicelib import conversations

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CampaignDB(object):
    def add_item(self, item):
        pass

    def list_items(self, new_campaign):
        pass

    def get_item(self, uid):
        pass

    def update_item(self, uid, body):
        pass


class DynamoDBCampaigns(CampaignDB):
    def __init__(self, table_resource):
        self._table = table_resource

    def add_item(self, conversation):
        logger.info('Adding new Campaign')
        new_campaign = conversations.process_conversation(conversation)
        #        if validate_campaign_fields(new_campaign):
        logger.info(f'Inserting conversation: {json.dumps(new_campaign)}')
        self._table.put_item(
            Item=new_campaign
        )
        return new_campaign

    def scan_all_items(self):
        logger.info('Listing all items')
        response = self._table.scan()
        logger.info(response['Items'])
        return response['Items']

    def list_eligible_items(self, psid):
        logger.info('Listing active paid campaign')
        response = self._table.scan(FilterExpression=Attr('psid').eq(psid) & Attr('active').eq(True))
        logger.info(response['Items'])
        return response['Items']

    def get_item(self, uid):
        logger.info(f'Getting Campaign: {uid}')
        item = self._table.get_item(Key={'campaingid': uid})['Item']
        if item is not None:
            return item
        else:
            logger.error(f'Campaign {uid} not found')
            return 404

    def delete_campaign(self, uid):
        logger.info(f'Inactivating Campaign: {uid}')
        item = self._table.get_item(Key={'campaingid': uid})['Item']
        if item is not None:
            now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
            item['modified_timestamp'] = now
            item['active'] = False
            response = self._table.put_item(Item=item)
            return response['ResponseMetadata']
        else:
            logger.error(f'Campaign {uid} not found')
            return 404

    def add_adwords_campaign(self, uid, adwords_campaignid):
        logger.info(f'Adding Adwords CampaignId: {uid}')
        item = self._table.get_item(Key={'campaingid': uid})['Item']
        if item is not None:
            now = str(datetime.datetime.now(pytz.timezone('America/Guatemala')))
            item['modified_timestamp'] = now
            item['adwords_campaignid'] = adwords_campaignid
            response = self._table.put_item(Item=item)
            return response['ResponseMetadata']
        else:
            logger.error(f'Campaign {uid} not found')
            return 404
