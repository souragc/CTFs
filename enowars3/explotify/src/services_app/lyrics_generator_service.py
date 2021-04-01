from urllib import request
from app import app 
from exceptions.LyricsGeneratorExceptions import RequestWebsiteException
import markovify
from bs4 import BeautifulSoup
from parsel import Selector
import base64
class LyricsGeneratorService():
    

    

    def __init__(self):
        self.__default_model = self.__load_default_model()

    def __load_default_model(self):

        model_file = open("model_words/model.txt","r",encoding="utf-8")
        readed_model = model_file.read()
        model = markovify.Text(readed_model)
        model_file.close()
        return model

    def __get_paragraphs_from_html(self,data):
        sel = Selector(data)
        all_text = []

        all_paragraphs_nodes = sel.xpath("//p/text()")
        all_div_nodes = sel.xpath("//div/text()")
        all_a_nodes = sel.xpath("//a/text()")

        all_div = all_div_nodes.extract()
        all_a = all_a_nodes.extract()
        all_paragraphs = all_paragraphs_nodes.extract()

        all_text.extend(all_div)
        all_text.extend(all_a)
        all_text.extend(all_paragraphs)


        return all_text
        

    def __join_paragraphs(self,paragraphs_list):
        return "".join(paragraphs_list)


    def generate_lyrics_from_website(self,website):
        info_website = self.__visit_website_from_link(website)
        test_html = self.__is_html(info_website)
        if test_html:
            decoded_info_website = info_website.decode("utf-8")
            paragraphs = self.__get_paragraphs_from_html(decoded_info_website)
            text = self.__join_paragraphs(paragraphs)
            random_word = self.__generate_random_lyrics(text)
            return base64.b64encode(info_website),random_word,True
        else:
            try:
                decoded_info_website = info_website.decode("utf-8","ignore")
                text = self.__generate_random_lyrics(decoded_info_website)
                return base64.b64encode(info_website),text,True
            except:
                text = self.__generate_from_default_model()
                return base64.b64encode(info_website),text,False

    
    def __generate_random_lyrics(self,text):
        model = markovify.Text(text,state_size=1)
        random_text_generated = model.make_short_sentence(100,1,tries=200)
        return random_text_generated

    def __generate_from_default_model(self):
        random_text = self.__default_model.make_short_sentence(100,1,tries=200)
        return random_text
        

    def __is_html(self,data):
        test = bool(BeautifulSoup(data, "html.parser").find())
        return test

    def __visit_website_from_link(self,link):
        try:
            request_link = request.urlopen(link)
            info = request_link.read()
        except Exception as e:
            app.logger.error(e)
            raise RequestWebsiteException("Trying to request the website info and it failed!")
            
        return info
        


    
