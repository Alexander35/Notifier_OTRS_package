from otrs.ticket.template import GenericTicketConnectorSOAP
from otrs.client import GenericInterfaceClient
from otrs.ticket.objects import Ticket, Article, DynamicField, Attachment
from general_server_client import GeneralClient, GeneralMachine
from protobuf_asset import msg_pb2
import argparse
import json

class OTRSNotifier(GeneralClient):
	"""docstring for ClassName"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		try:
			self.client = GenericInterfaceClient(
					self.get_config('OTRS','Url'), 
					tc=GenericTicketConnectorSOAP(self.get_config('OTRS','Webservice'))
					)
			self.client.tc.SessionCreate(
					user_login=self.get_config('OTRS','User'), 
					password=self.get_config('OTRS','Password')
					)
		except Exception  as exc:
			self.logger.error('Unable to init a Notifier {}'.format(exc))	
			quit(1)

	def ticket_search(self, **kwargs):
		try:
			tickets = self.client.tc.TicketSearch(**kwargs)
			combinesd_msgs = [self.ticket_get(t) for t in tickets]
			msgs_to_send = self.prepare_msg(combinesd_msgs)
			self.send(msgs_to_send)

		except Exception as exc:
			self.loger.error('Ticket search errror {}'.fromat(exc))	

	def ticket_get(self, ticket_id, **kwargs):
		try:
			ticket = self.client.tc.TicketGet(ticket_id, **kwargs, 
					get_articles=True, 
					get_dynamic_fields=True, 
					get_attachments=True
				)
			articles = ticket.articles()

			messages = [['Заявка ', ['От', [art.attrs['From']], 'Тема', [ art.attrs['Subject']], 'Текст', [art.attrs['Body']]]] for art in articles]
			jmessages = json.dumps(
						messages, 
						indent=4,
						ensure_ascii=False
					)
			return jmessages
		except Exception as exc:
			self.logger.error('get articles error {}'.format(exc))	

	def prepare_msg(self, raw_data):
		# nothing to send
		if raw_data == []:
			quit(0) 
		Msg = msg_pb2.Msg()
		Msg.title = 'OTRS Notify'
		Msg.text = ''.join('{}'.format(str(r)) for r in raw_data)
		Msg.tagline = '#OTRS'
		
		SM = Msg.SerializeToString()
		self.logger.info('message \n{}\n'.format(SM))
		return SM

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--config", dest="conf", help="configuration file name", default="config.ini")
	parser.add_argument("-l", "--log", dest="log", help="log file name", default="OTRSNotitfier")
	parser.add_argument("--queues",  action='append', default=[], help="--queues one queue --two queue")
	parser.add_argument("--state_type", default=[], help="new, open etc")
	
	args = parser.parse_args()	
	OTRSN = OTRSNotifier(ConfigName=args.conf, LoggerName=args.log)
	OTRSN.ticket_search(Queues=args.queues, StateType=args.state_type)

if __name__ == '__main__':
	main()