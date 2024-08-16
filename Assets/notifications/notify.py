import africastalking

africastalking.initialize(
    username='hkay_mzika',
    api_key='atsk_eeae5eb035f192c93b096b84b6926ac05fe9a5882d8304c0117f121f4521ec0efc10c830'
)

# sms = africastalking.SMS

class send_sms():
    
    def __init__(self) -> None:
        self.sms = africastalking.SMS

    def send(self, recipients, message):
        # recipients = ["+265886654986", "+265994248549"]
        # message = "Phiri, dzukani mukode."
        # sender = "Hkay Mzika"

        try:
            response = self.sms.send(message, recipients)
            print(response)
        except Exception as e:
            print(f'Oops, we have a problem: {e}')

sms = send_sms()
sms.send(["+265992236155"],"Okondedwa akasitomala, pitani pa office yaku mzuzu mukatenge chiphaso cha unzika chanu pa tsiku la ntchito lililonse.") 