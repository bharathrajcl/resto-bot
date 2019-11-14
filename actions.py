# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
from datetime import datetime
from typing import Text, Dict, Any, List
import json

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ConversationPaused
import pymongo

#
#
class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Hello World!")

        return 


api_link = "mongodb://localhost:27017/"
myclient = pymongo.MongoClient(api_link)
mydb = myclient["mydatabase"]
mycol1 = mydb["business"]
mycol2 = mydb["customer"]

class ActionInfoCity(Action):

    def name(self) -> Text:
        return "action_info_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        

        #myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        #mydb = myclient["mydatabase"]
        #mycol1 = mydb["business"]
        #mycol2 = mydb["customer"]
        myquery = { "city": { "$gt": "C" } }  #Calgary,Charlotte
        mydoc = mycol1.find(myquery)
        temp = []
        for x in mydoc:
          temp.append(x)
        city = [] 
        for x in temp:
          city.append(x['city'])
        data = ','.join(list(set(city)))
        dispatcher.utter_message("We are currently giving services in "+ data)

        return 
 
 
class  ActionInfoCharlotte(Action):
    
    def name(self) -> Text:
        return "action_info_charlotte"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            
        myquery = {"city":"Charlotte", "name": "Queen City Plumbing"}
        mydoc = mycol1.find(myquery)
        
        #print(mydoc)
        data = mydoc[0]['name']
        
        dispatcher.utter_message("We are giving service in City Charlotte is Hotel " + str(data))
        
class  ActionInfoCalgary(Action):
    
    def name(self) -> Text:
        return "action_info_calgary"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            
        myquery = {"city":"Calgary", "name": "Calgary Cycle"}
        mydoc = mycol1.find(myquery)
        
        
        data = mydoc[0]['name']
        #print(data)
        dispatcher.utter_message("We are giving service in City Calgary is Hotel "+ str(data))
        
        
class  ActionTimeCharlotte(Action):
    
    def name(self) -> Text:
        return "action_time_charlotte"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            
        myquery = {"city":"Charlotte", "name": "Queen City Plumbing"}
        mydoc = mycol1.find(myquery)
        
        temp = []
        for x in mydoc:
            temp.append(x)
        tre = temp[0]['hours']['Monday']
        data = tre
        dispatcher.utter_message("The working hours of Hotel Queen City Plumbing is :" + data)

class  ActionTimeCalgary(Action):
    
    def name(self) -> Text:
        return "action_time_calgary"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            
        myquery = {"city":"Calgary", "name": "Calgary Cycle"}
        mydoc = mycol1.find(myquery)
        
        temp = []
        for x in mydoc:
            temp.append(x)
        tre = temp[0]['hours']['Monday']
        data = tre
        dispatcher.utter_message("The working hours of Hotel Calgary Cycle is :" + data)
        
class  ActionAddressCalgary(Action):
    
    def name(self) -> Text:
        return "action_address_calgary"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            
        myquery = {"city":"Calgary", "name": "Calgary Cycle"}
        mydoc = mycol1.find(myquery)
        
        temp = []
        for x in mydoc:
            temp.append(x)
        tre = temp[0]['address']
        data = tre
        dispatcher.utter_message("The Address of Hotel Calgary Cycle is :" + data)


class  ActionAddressCharlotte(Action):
    
    def name(self) -> Text:
        return "action_address_charlotte"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            
        myquery = {"city":"Charlotte", "name": "Queen City Plumbing"}
        mydoc = mycol1.find(myquery)
        
        temp = []
        for x in mydoc:
            temp.append(x)
        tre = temp[0]['address']
        data = tre
        dispatcher.utter_message("The Address of Hotel Queen City Plumbing is :" + data)
 
class ActionChitchat(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self):
        return "action_chitchat"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")

        # retrieve the correct chitchat utterance dependent on the intent
        if intent in [
            "ask_builder",
            "ask_weather",
            "ask_howdoing",
            "ask_whatspossible",
            "ask_whatisrasa",
            "ask_isbot",
            "ask_howold",
            "ask_languagesbot",
            "ask_restaurant",
            "ask_time",
            "ask_wherefrom",
            "ask_whoami",
            "handleinsult",
            "nicetomeeyou",
            "telljoke",
            "ask_whatismyname",
            "ask_howbuilt",
            "ask_whoisit",
        ]:
            dispatcher.utter_template("utter_" + intent, tracker)
        return []
        


class ActionGreetUser(Action):
    """Greets the user with/without privacy policy"""

    def name(self):
        return "action_greet_user"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        shown_privacy = tracker.get_slot("shown_privacy")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        if intent == "greet":
            if shown_privacy and name_entity and name_entity.lower() != "sara":
                dispatcher.utter_template("utter_greet_name", tracker, name=name_entity)
                return []
            elif shown_privacy:
                dispatcher.utter_template("utter_greet_noname", tracker)
                return []
            else:
                dispatcher.utter_template("utter_greet", tracker)
                dispatcher.utter_template("utter_inform_privacypolicy", tracker)
                dispatcher.utter_template("utter_ask_goal", tracker)
                return [SlotSet("shown_privacy", True)]
        elif intent[:-1] == "get_started_step" and not shown_privacy:
            dispatcher.utter_template("utter_greet", tracker)
            dispatcher.utter_template("utter_inform_privacypolicy", tracker)
            dispatcher.utter_template("utter_" + intent, tracker)
            return [SlotSet("shown_privacy", True), SlotSet("step", intent[-1])]
        elif intent[:-1] == "get_started_step" and shown_privacy:
            dispatcher.utter_template("utter_" + intent, tracker)
            return [SlotSet("step", intent[-1])]
        return []
        
        
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:
    
        intent = tracker.latest_message["intent"].get("name")

        # retrieve the correct chitchat utterance dependent on the intent
        if intent in [
            "ask_builder",
            "ask_weather",
            "ask_howdoing",
            "ask_whatspossible",
            "ask_time",
            "ask_wherefrom",
            "ask_whoami",
            "handleinsult",
            "telljoke",
            "ask_whatismyname",
            "ask_howbuilt",
            "ask_whoisit",
            "out_of_scope"
        ]:
            dispatcher.utter_template("utter_" + intent, tracker)

        dispatcher.utter_template("utter_default", tracker)
        return [UserUtteranceReverted()]
        