import requests
import json
import wanted
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
        with open("data.txt", 'a', encoding='UTF-8') as myfile: 
            try: myfile.write(str(self.forename) + "|" + self.date_of_birth + "|" + self.entity_id + "|" + self.nationalities[0] + "|" + str(self.name) 
                         + "|" + self.selfHref + "|" + self.imagesHref + "|" + self.thumbnailHref + "\n")
            except: myfile.write(str(self.forename) + "|" + self.date_of_birth + "|" + self.entity_id + "|" + "|" + str(self.name) 
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
    


for row in wanted.wantedBy:
#     url = 'https://ws-public.interpol.int/notices/v1/red?&arrestWarrantCountryId=' + row[0]
#     response = requests.get(url)
    url = 'https://ws-public.interpol.int/notices/v1/red?&arrestWarrantCountryId=' + row[0] + '&resultPerPage=160' # Country
    result = json.loads(requests.get(url).text)
    if result["total"] <= 160:
        print(row[0], " = ", result["total"])
        takeResults(result)   
        
    else: # filter by age
        url = 'https://ws-public.interpol.int/notices/v1/red?&ageMin=0&ageMax=25&arrestWarrantCountryId=' + row[0] + '&resultPerPage=160' # Country + age from 0 to 25
        resultFrom0To25 = json.loads(requests.get(url).text)
        print(row[0], "0-25 = ", resultFrom0To25["total"])
        takeResults(resultFrom0To25)
        
        
        url = 'https://ws-public.interpol.int/notices/v1/red?&ageMin=60&ageMax=120&arrestWarrantCountryId=' + row[0] + '&resultPerPage=160' # Country + age from 60 to 120
        resultFrom60To120 = json.loads(requests.get(url).text)
        print(row[0], "60-120 = ", resultFrom60To120["total"])
        takeResults(resultFrom60To120)

        for x in range(26, 59): 
            url = 'https://ws-public.interpol.int/notices/v1/red?&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + row[0] + '&resultPerPage=160' # Country + age from 26 to 59
            resultFrom26To59 = json.loads(requests.get(url).text)
            print(row[0], ' ', str(x) + ' =', resultFrom26To59["total"])


            if resultFrom26To59["total"] > 160: # filter by sexId
                url = 'https://ws-public.interpol.int/notices/v1/red?&sexId=M&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + row[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Male
                resultFrom26To59M = json.loads(requests.get(url).text)
                if  resultFrom26To59M["total"] > 160:# filter by sexId = male give result > 160                
                    for nationalityID in wanted.wantedBy:
                        try:
                            url = 'https://ws-public.interpol.int/notices/v1/red?&nationality='+ str(nationalityID[0]) + '&sexId=M&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + row[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Male + nationalityID
                            resultFrom26To59N = json.loads(requests.get(url).text)
                            takeResults(resultFrom26To59N)
                            print(row[0], ' Nation:', nationalityID, " male = ", resultFrom26To59N["total"])
                        except:
                            continue
                else: 
                    takeResults(resultFrom26To59M)
                    print(row[0], ' ', str(x) + ' male =', resultFrom26To59M["total"])
                url = 'https://ws-public.interpol.int/notices/v1/red?&sexId=F&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + row[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Female
                resultFrom26To59F = json.loads(requests.get(url).text)
                print(row[0], ' ', str(x) + ' female =', resultFrom26To59F["total"])
                takeResults(resultFrom26To59F)
                if resultFrom26To59F["total"] + resultFrom26To59M["total"] != resultFrom26To59["total"]:
                    url = 'https://ws-public.interpol.int/notices/v1/red?&sexId=U&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + row[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Unknown
                    resultFrom26To59U = json.loads(requests.get(url).text)
                    print(row[0], ' ', str(x) + ' unknown =', resultFrom26To59U["total"])
                    takeResults(resultFrom26To59U)    
            else: takeResults(resultFrom26To59)

    #https://ws-public.interpol.int/notices/v1/red?&nationality=RU
    #https://ws-public.interpol.int/notices/v1/red?arrestWarrantCountryId=RU&resultPerPage=20&page=2


