#https://ws-public.interpol.int/notices/v1/red?&arrestWarrantCountryId=RU
#https://ws-public.interpol.int/notices/v1/red?&ageMin=29&ageMax=29&arrestWarrantCountryId=RU
#https://ws-public.interpol.int/notices/v1/red?&sexId=M&ageMin=31&ageMax=31&arrestWarrantCountryId=RU
# 60-120 0-25
from bs4 import BeautifulSoup
import requests
import json

class redBastard:
    forename = ""
    date_of_birth = ""
    entity_id = "",
    nationalities = ""
    name = ""
    selfHref = ""
    imagesHref = ""
    thumbnailHref = ""
    
    def __init__(self, forename, date_of_birth, entity_id, nationalities, name, selfHref, imagesHref, thumbnailHref):
        self.forename = forename
        self.date_of_birth = date_of_birth
        self.entity_id = entity_id
        self.nationalities = nationalities
        self.name = name
        self.selfHref = selfHref
        self.imagesHref = imagesHref
        self.thumbnailHref = thumbnailHref

    def writeCSV(self):
        with open(".\interpol\data.txt", 'a') as myfile: 
            try: myfile.write(self.forename + "|" + self.date_of_birth + "|" + self.entity_id + "|" + self.nationalities[0] + "|" + self.name 
                         + "|" + self.selfHref + "|" + self.imagesHref + "|" + self.thumbnailHref + "\n")
            except: myfile.write(self.forename + "|" + self.date_of_birth + "|" + self.entity_id + "|" + "NULL" + "|" + self.name 
                         + "|" + self.selfHref + "|" + self.imagesHref + "|" + self.thumbnailHref + "\n")
    def prinrBst(self):
        print(self.forename + "|" + self.date_of_birth + "|" + self.entity_id + "|" + self.nationalities[0] + "|" + self.name 
                         + "|" + self.selfHref + "|" + self.imagesHref + "|" + self.thumbnailHref)
            
def takeResults(result):
    
    for bst in result["_embedded"]["notices"]:
        try:
            oneRedBastard = redBastard(bst["forename"], bst["date_of_birth"], bst["entity_id"], bst["nationalities"],
                                    bst["name"], bst["_links"]["self"]["href"], bst["_links"]["images"]["href"], bst["_links"]["thumbnail"]["href"]) # KeyError
        except KeyError:
            oneRedBastard = redBastard(bst["forename"], bst["date_of_birth"], bst["entity_id"], bst["nationalities"],
                                    bst["name"], bst["_links"]["self"]["href"], bst["_links"]["images"]["href"], "NULL")
        finally: 
            oneRedBastard.writeCSV()


# for row in wantedBy:
#     url = 'https://ws-public.interpol.int/notices/v1/red?&arrestWarrantCountryId=' + row[0]
#     response = requests.get(url)
url = 'https://ws-public.interpol.int/notices/v1/red?&arrestWarrantCountryId=RU&resultPerPage=160' # Country
result = json.loads(requests.get(url).text)
if result["total"] <= 160:
    #print(result["_embedded"]["notices"])
    takeResults(result)   
    
else: # filter by age
    url = 'https://ws-public.interpol.int/notices/v1/red?&ageMin=0&ageMax=25&arrestWarrantCountryId=RU&resultPerPage=160' # Country + age from 0 to 25
    resultFrom0To25 = json.loads(requests.get(url).text)
    print("0-25 = ", resultFrom0To25["total"])
    takeResults(resultFrom0To25)
    
    
    url = 'https://ws-public.interpol.int/notices/v1/red?&ageMin=60&ageMax=120&arrestWarrantCountryId=RU&resultPerPage=160' # Country + age from 60 to 120
    resultFrom60To120 = json.loads(requests.get(url).text)
    print("60-120 = ", resultFrom60To120["total"])
    takeResults(resultFrom60To120)

    for x in range(26, 59): 
        url = 'https://ws-public.interpol.int/notices/v1/red?&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=RU&resultPerPage=160' # Country + age from 26 to 59
        resultFrom26To59 = json.loads(requests.get(url).text)
        print(str(x) + ' =', resultFrom26To59["total"])


        if resultFrom26To59["total"] > 160: # filter by sexId
            url = 'https://ws-public.interpol.int/notices/v1/red?&sexId=M&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=RU&resultPerPage=160' # Country + age from 26 to 59 + Male
            resultFrom26To59M = json.loads(requests.get(url).text)
            takeResults(resultFrom26To59M)

            url = 'https://ws-public.interpol.int/notices/v1/red?&sexId=F&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=RU&resultPerPage=160' # Country + age from 26 to 59 + Female
            resultFrom26To59F = json.loads(requests.get(url).text)
            takeResults(resultFrom26To59F)
            if resultFrom26To59F["total"] + resultFrom26To59M["total"] != resultFrom26To59["total"]:
                url = 'https://ws-public.interpol.int/notices/v1/red?&sexId=U&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=RU&resultPerPage=160' # Country + age from 26 to 59 + Unknown
                resultFrom26To59U = json.loads(requests.get(url).text)
                takeResults(resultFrom26To59U)


        else: takeResults(resultFrom26To59)

    # resultFrom60To120_json = json.dumps(resultFrom60To120)
    # with open(".\interpol\capitals.json", "w") as my_file:
    #     my_file.write(resultFrom60To120_json)



#https://ws-public.interpol.int/notices/v1/red?arrestWarrantCountryId=RU&resultPerPage=20&page=2


wantedBy = [ 
    ["AF","Afghanistan"],
    ["AL","Albania"],
    ["DZ","Algeria"],
    ["AS","American Samoa, United States"],
    ["AD","Andorra"],
    ["AO","Angola"],
    ["AI","Anguilla, United Kingdom"],
    ["AG","Antigua and Barbuda"],
    ["AR","Argentina"],
    ["AM","Armenia"],
    ["AU","Australia"],
    ["AT","Austria"],
    ["AZ","Azerbaijan"],
    ["BS","Bahamas"],
    ["BH","Bahrain"],
    ["BD","Bangladesh"],
    ["BB","Barbados"],
    ["BY","Belarus"],
    ["BE","Belgium"],
    ["BZ","Belize"],
    ["BJ","Benin"],
    ["BT","Bhutan"],
    ["BO","Bolivia"],
    ["BA","Bosnia and Herzegovina"],
    ["BW","Botswana"],
    ["BR","Brazil"],
    ["BN","Brunei "],
    ["BG","Bulgaria"],
    ["BF","Burkina Faso"],
    ["BI","Burundi"],
    ["KH","Cambodia"],
    ["CM","Cameroon"],
    ["CA","Canada"],
    ["CV","Cape Verde"],
    ["CF","Central African Republic"],
    ["TD","Chad"],
    ["CL","Chile"],
    ["CN","China"],
    ["CO","Colombia"],
    ["KM","Comoros"],
    ["CG","Congo"],
    ["CD","Congo (Democratic Republic of)"],
    ["CR","Costa Rica"],
    ["HR","Croatia"],
    ["CU","Cuba"],
    ["CY","Cyprus"],
    ["CZ","Czech Republic"],
    ["CI","Côte d'Ivoire"],
    ["DK","Denmark"],
    ["DJ","Djibouti"],
    ["DM","Dominica"],
    ["DO","Dominican Republic"],
    ["EC","Ecuador"],
    ["EG","Egypt"],
    ["SV","El Salvador"],
    ["GQ","Equatorial Guinea"],
    ["ER","Eritrea"],
    ["EE","Estonia"],
    ["SZ","Eswatini"],
    ["ET","Ethiopia"],
    ["FJ","Fiji"],
    ["FI","Finland"],
    ["FR","France"],
    ["GA","Gabon"],
    ["GM","Gambia"],
    ["GE","Georgia"],
    ["DE","Germany"],
    ["GH","Ghana"],
    ["GR","Greece"],
    ["GD","Grenada"],
    ["GT","Guatemala"],
    ["GN","Guinea"],
    ["GW","Guinea Bissau"],
    ["GY","Guyana"],
    ["HT","Haiti"],
    ["HN","Honduras"],
    ["HU","Hungary"],
    ["914","ICC (International Criminal Court)"],
    ["IS","Iceland"],
    ["IN","India"],
    ["ID","Indonesia"],
    ["IR","Iran"],
    ["IQ","Iraq"],
    ["IE","Ireland"],
    ["IL","Israel"],
    ["IT","Italy"],
    ["JM","Jamaica"],
    ["JP","Japan"],
    ["JO","Jordan"],
    ["KZ","Kazakhstan"],
    ["KE","Kenya"],
    ["KI","Kiribati"],
    ["KP","Korea (Democratic People's Republic of)"],
    ["KR","Korea (Republic of)"],
    ["KW","Kuwait"],
    ["KG","Kyrgyzstan"],
    ["LA","Laos"],
    ["LV","Latvia"],
    ["LB","Lebanon"],
    ["LS","Lesotho"],
    ["LR","Liberia"],
    ["LY","Libya"],
    ["LI","Liechtenstein"],
    ["LT","Lithuania"],
    ["LU","Luxembourg"],
    ["MO","Macao, China"],
    ["MG","Madagascar"],
    ["MW","Malawi"],
    ["MY","Malaysia"],
    ["MV","Maldives"],
    ["ML","Mali"],
    ["MT","Malta"],
    ["MH","Marshall Islands"],
    ["MR","Mauritania"],
    ["MU","Mauritius"],
    ["MX","Mexico"],
    ["FM","Micronesia, Federated States of"],
    ["MD","Moldova"],
    ["MC","Monaco"],
    ["MN","Mongolia"],
    ["ME","Montenegro"],
    ["MA","Morocco"],
    ["MZ","Mozambique"],
    ["MM","Myanmar"],
    ["NA","Namibia"],
    ["NR","Nauru"],
    ["NP","Nepal"],
    ["NL","Netherlands"],
    ["NZ","New Zealand"],
    ["NI","Nicaragua"],
    ["NE","Niger"],
    ["NG","Nigeria"],
    ["MK","North Macedonia"],
    ["NO","Norway"],
    ["OM","Oman"],
    ["PK","Pakistan"],
    ["PW","Palau"],
    ["PS","Palestine, State of"],
    ["PA","Panama"],
    ["PG","Papua New Guinea"],
    ["PY","Paraguay"],
    ["PE","Peru"],
    ["PH","Philippines"],
    ["PL","Poland"],
    ["PT","Portugal"],
    ["QA","Qatar"],
    ["RO","Romania"],
    ["RU","Russia"],
    ["RW","Rwanda"],
    ["KN","Saint Kitts and Nevis"],
    ["LC","Saint Lucia"],
    ["VC","Saint Vincent and the Grenadines"],
    ["WS","Samoa"],
    ["SM","San Marino"],
    ["ST","Sao Tome and Principe"],
    ["SA","Saudi Arabia"],
    ["SN","Senegal"],
    ["RS","Serbia"],
    ["SC","Seychelles"],
    ["SL","Sierra Leone"],
    ["SG","Singapore"],
    ["SK","Slovakia"],
    ["SI","Slovenia"],
    ["SB","Solomon Islands"],
    ["SO","Somalia"],
    ["ZA","South Africa"],
    ["SS","South Sudan"],
    ["ES","Spain"],
    ["LK","Sri Lanka"],
    ["916","STL (Special Tribunal for Lebanon)"],
    ["SD","Sudan"],
    ["SR","Suriname"],
    ["SE","Sweden"],
    ["CH","Switzerland"],
    ["SY","Syria"],
    ["TJ","Tajikistan"],
    ["TZ","Tanzania"],
    ["TH","Thailand"],
    ["TL","Timor-Leste"],
    ["TG","Togo"],
    ["TO","Tonga"],
    ["TT","Trinidad and Tobago"],
    ["TN","Tunisia"],
    ["TR","Turkey"],
    ["TM","Turkmenistan"],
    ["TC","Turks and Caicos (Islands), United Kingdom"],
    ["TV","Tuvalu"],
    ["UG","Uganda"],
    ["UA","Ukraine"],
    ["922","UN IRMCT (United Nations International Residual Mechanism for Criminal Tribunals)"],
    ["UNK","under UNMIK mandate (Kosovo)"],
    ["AE","United Arab Emirates"],
    ["GB","United Kingdom"],
    ["US","United States"],
    ["UY","Uruguay"],
    ["UZ","Uzbekistan"],
    ["VU","Vanuatu"],
    ["VA","Vatican City State"],
    ["VE","Venezuela"],
    ["VN","Viet Nam"],
    ["YE","Yemen"],
    ["ZM","Zambia"],
    ["ZW","Zimbabwe"]]