import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from datetime import datetime
from dateutil.parser import parse
import pytz
import uuid

class ElasticsearchConsumer():
    def __init__(self, index, cluster):


        self.es = Elasticsearch(
            cluster,
            use_ssl=False,
            verify_certs=False
        )
        self.index = index

    def put_in_index(self, doc):
        doc['message_ts'] =  datetime.now(pytz.timezone('US/Eastern'))

        try:
            result = self.es.index(
                self.index,
                doc_type='default',
                body=doc,
                id=str(uuid.uuid4())
            )

            if result.get('_shards').get('successful') > 0:
                return True
        except Exception as e:
            print(e)

    def get_targets(self):
        return scan(
            self.es,
            index=self.index,
            doc_type='default',
            query={"query": { "match_all" : {}}}
        )
