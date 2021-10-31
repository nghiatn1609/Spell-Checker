from chatterbot.logic import LogicAdapter
from flask import Flask, render_template, request
from requests.models import Response

class Covid19Adapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        ().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        words = ['All-Cases', 'all-cases', 'All-cases', 'all-Cases','Covid19', 'covid19', 'Total-Cases', 'total-cases', 'Total-cases', 'total-Cases', 'Today', 'today', 'Daily', 'daily', 'Daily-Cases', 'daily-cases', 'Daily-cases', 'daily-Cases', 'Death', 'death', 'Death-Cases', 'Death-cases', 'death-cases', 'death-Cases', 'Recover', 'recover', 'Recover-Cases', 'Recover-cases', 'recover-Cases', 'recover-cases', 'Active', 'active', 'Active-Cases', 'active-cases', 'Active-cases', 'active-Cases']
        if any(x in statement.text.split() for x in words):
            return True
        else:
            return False
    
    def process(self, input_statement,additional_response_selection_parameters):
        from chatterbot.conversation import Statement
        import requests
        import json as JSON
        from bs4 import BeautifulSoup
        import glob
        import os
        
        # Countries=['argentina', 'spain', 'bangladesh', 'ukraine', 'romania', 'pakistan', 'portugal', 'hungary', 'netherlands', 'aghanistan', 'albania', 'algeria', 'andorra','angola', 'anguilla', 'aruba', 'austria', 'australia', 'benin', 'belgium', 'bolivia', 'canada', 'chile', 'china', 'colombia', 'viet-nam', 'cambodia', 'cuba', 'france', 'india','indonesia', 'iran', 'iraq', 'ireland', 'japan', 'jordan', 'malaysia', 'malta', 'luxembourg', 'mexico', 'myanmar', 'russia', 'south-korea', 'saudi-arabia', 'south-africa', 'sudan', 'uk', 'us', 'uzbekistan', 'vatican-city', 'thailand', 'united-arab-emirates', 'italy', 'germany', 'egypt', 'brunei', 'brazil', 'croatia', 'turkey']
        countri = []
        answer = []
        for filename in glob.glob('C:/Users/Admin/Desktop/Spell Checker/chatbotTest/chatbot/country.txt'): # path of Country.txt in your computer
            with open(os.path.join(os.getcwd(), filename), 'r', encoding='UTF-8') as f:
                lines = f.readlines()
                for line in lines:
                    countri.append(line.replace("\n",""))
        response = requests.get("https://www.worldometers.info/coronavirus/#countries") # path of Web Crawled 
        # blogger = requests.get("https://formatofcountries.blogspot.com/2021/10/blog-post.html") # path of Guide for type countries
        if response.status_code == 200: 
            confidence = 1 
        else:
            confidence = 0
        words = ['All-Cases', 'all-cases', 'All-cases', 'all-Cases','Covid19', 'covid19', 'Total-Cases', 'total-cases', 'Total-cases', 'total-Cases', 'Today', 'today', 'Daily', 'daily', 'Daily-Cases', 'daily-cases', 'Daily-cases', 'daily-Cases', 'Death', 'death', 'Death-Cases', 'Death-cases', 'death-cases', 'death-Cases', 'Recover', 'recover', 'Recover-Cases', 'Recover-cases', 'recover-Cases', 'recover-cases', 'Active', 'active', 'Active-Cases', 'active-cases', 'Active-cases', 'active-Cases']
        countCountry = 0
        if any(x in input_statement.text.split() for x in words):
            if any(y in input_statement.text.split() for y in countri):
                for i in input_statement.text.split():
                    for y in countri:
                        if i == y:
                            country = y
                            countCountry = 1
                        # else:
                        #     response_statement = Statement(text='Oops, You can look up the correct country name syntax to find information about the countries: {}'.format(blogger))
                        #     response_statement.confidence = 1
                        #     return response_statement
        if countCountry == 1:
            news = requests.get("https://www.worldometers.info/coronavirus/country/" + country + "/")
            soup = BeautifulSoup(news.content, "html.parser")
            Country = soup.find("div", class_="label-counter").text[20:]
            # Total Cases
            Total_Ca = soup.find_all("div",class_="maincounter-number")[0].text.replace('\n','')  # replace('\n','') để replace dấu xuống dòng thành dấu ''
            Total_Case = "".join(Total_Ca.split())  #loại bỏ khoảng trắng 
            # Death Cases
            Dead = soup.find_all("div",class_="maincounter-number")[1].text.replace('\n','')
            Death = "".join(Dead.split())
            # Recover Cases
            Reco = soup.find_all("div",class_="maincounter-number")[2].text.replace('\n','')
            Recover = "".join(Reco.split())   # Recover cases
            Da = soup.find_all("script", type ="text/javascript")
                    
                    # Active Cases Total
            for a in Da:
                if a.text.find("Highcharts.chart('graph-active-cases-total'") != -1:
                    B = a.text

            ser = B.find("[{")
            se = B.find("responsive")

            jso1 = B[ser:se-11]

            json1 = JSON.dumps(jso1) # Mã hóa thành các đối tượng JSON
            js = JSON.loads(json1)   #	Giải mã chuỗi JSON
            # tách chuỗi để ra được 1 array chứa data
            count = js.find("[",1)
            co = js.find("]")

            re = js[count+1:co]
            Active = re.split(",")  # res[-1] sẽ là giá trị cần tìm
            Active_cases = Active[-1]   # Active Cases
                    
            #Daily Cases Total
            for a in Da:
                if a.text.find("Highcharts.chart('graph-cases-daily'") != -1:
                    C = a.text

            # find Day in Daily Cases
            
            start = C.find("xAxis: {")
            end = C.find("yAxis:")
            day = C[start+7:end-11]
            man = JSON.dumps(day) # Mã hóa thành các đối tượng JSON
            manly = JSON.loads(man)
            daycount = manly.find("[",1)
            countday = manly.find("]")
            so = manly[daycount+1:countday]
            son = so.split(",")
            Day_ly = son[-2][1:] + son[-1][:5]  # Day in Daily Cases 
            # son[-2][1:] : lấy ngày và tháng  + son[-1][:5] : lấy năm
                    
            ser1 = C.find("[{")
            se1 = C.find("responsive")

            jso11 = C[ser1:se1-11]

            json11 = JSON.dumps(jso11) # Mã hóa thành các đối tượng JSON
            js1 = JSON.loads(json11)   #	Giải mã chuỗi JSON
            count1 = js1.find("[",1)

            co1 = js1.find("]")


            re1 = js1[count1+1:co1]
            Daily = re1.split(",")# res1[-1] sẽ là giá trị cần tìm
            Daily_cases = Daily[-1]   # Daily Cases
            words1 = ['All-Cases', 'all-cases', 'All-cases', 'all-Cases','Covid19', 'covid19', 'Total-Cases', 'total-cases', 'Total-cases', 'total-Cases', 'Today', 'today', 'Daily', 'daily', 'Daily-Cases', 'daily-cases', 'Daily-cases', 'daily-Cases', 'Death', 'death', 'Death-Cases', 'Death-cases', 'death-cases', 'death-Cases', 'Recover', 'recover', 'Recover-Cases', 'Recover-cases', 'recover-Cases', 'recover-cases', 'Active', 'active', 'Active-Cases', 'active-cases', 'Active-cases', 'active-Cases']
            
            for i in input_statement.text.split():
                    
                for abc in words1:
                    
                    if i == abc :
                        ket = abc
                                
                        if ket.lower() == 'total-cases':
                            response_statement = Statement(text='Total cases are: {}'.format(Total_Case))
                            answer.append(str(response_statement))
                            
                        if ket.lower() == 'today' or ket.lower() == 'daily' or ket.lower() == 'daily-cases':
                            response_statement = Statement(text='In {}'.format(Day_ly)) 
                            response1 = Statement(text=' have: {} cases'.format(Daily_cases))
                            answer.append(str(response_statement) + str(response1))
                            
                        if ket.lower() == 'death' or ket.lower() == 'death-cases':
                            response_statement = Statement(text='Total death are: {}'.format(Death))
                            answer.append(str(response_statement))
                            
                        if ket.lower() == 'recover-cases' or ket.lower() == 'recover':
                            response_statement = Statement(text='Recover cases are: {}'.format(Recover))
                            answer.append(str(response_statement))
                                
                        if ket.lower() == 'active-cases' or ket.lower() == 'active':
                            response_statement = Statement(text='Active cases are: {}'.format(Active_cases))
                            answer.append(str(response_statement))
                    
                        if ket.lower() == 'all-cases':
                            #Daily-Cases
                            response_statement1 = Statement(text='In {}'.format(Day_ly)) 
                            response1 = Statement(text=' have: {} cases'.format(Daily_cases))
                            answer.append(str(response_statement1) + str(response1))
                            #Total-Cases
                            response_statement2 = Statement(text='Total cases are: {}'.format(Total_Case))
                            answer.append(str(response_statement2))
                            #Active-Cases
                            response_statement3 = Statement(text='Active cases are: {}'.format(Active_cases))
                            answer.append(str(response_statement3))
                            #Recover-Cases
                            response_statement4 = Statement(text='Recover cases are: {}'.format(Recover))
                            answer.append(str(response_statement4))
                            #Death-Cases
                            response_statement5 = Statement(text='Total death are: {}'.format(Death))
                            answer.append(str(response_statement5))
                                    
                   
        else:
            response_statement6 = Statement(text='Oops, You can look up the correct country name syntax to find information about the countries: {} '.format("https://formatofcountries.blogspot.com/2021/10/blog-post.html"))           
            answer.append(str(response_statement6))
        response_statement = Statement(text='{}'.format(answer))
        response_statement.confidence = confidence
        return response_statement


