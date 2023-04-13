import requests
import json
import wanted

class YellowNoticePerson (wanted.NoticePerson):
    def dec(self):
        pass  
            
def take_results(result):
    
    for person in result["_embedded"]["notices"]:
        try:
            oneYellowNoticePerson = YellowNoticePerson(person["forename"], person["date_of_birth"], person["entity_id"], person["nationalities"],
                                    person["name"], person["_links"]["self"]["href"], person["_links"]["images"]["href"], person["_links"]["thumbnail"]["href"]) # KeyError
            
            with open('./img-y-person/' + person["entity_id"].replace('/', '-') + '.jpg','wb') as target: #save img
                a = requests.get(person["_links"]["thumbnail"]["href"])
                target.write(a.content)
        except KeyError:
            oneYellowNoticePerson = YellowNoticePerson(person["forename"], person["date_of_birth"], person["entity_id"], person["nationalities"],
                                    person["name"], person["_links"]["self"]["href"], person["_links"]["images"]["href"], "NULL")
        finally: 
            oneYellowNoticePerson.write_in_file('data-y-person.txt')
    
for nationality in wanted.wanted_by:
    url = 'https://ws-public.interpol.int/notices/v1/yellow?&nationality=' + nationality[0] + '&resultPerPage=160' # by nationality
    result = json.loads(requests.get(url).text)
    if result["total"] <= 160:
        print(nationality[0], " = ", result["total"])
        take_results(result)   
        
    else: # filter by age
        url = 'https://ws-public.interpol.int/notices/v1/yellow?&ageMin=0&ageMax=5&nationality=' + nationality[0] + '&resultPerPage=160' # Country + age from 0 to 25
        result_from_0_to_5 = json.loads(requests.get(url).text)
        print(nationality[0], "0-5 = ", result_from_0_to_5["total"])
        take_results(result_from_0_to_5)
        
        
        url = 'https://ws-public.interpol.int/notices/v1/yellow?&ageMin=65&ageMax=120&nationality=' + nationality[0] + '&resultPerPage=160' # Country + age from 60 to 120
        result_from_65_to_120 = json.loads(requests.get(url).text)
        print(nationality[0], "65-120 = ", result_from_65_to_120["total"])
        take_results(result_from_65_to_120)

        for x in range(6, 64): 
            url = 'https://ws-public.interpol.int/notices/v1/yellow?&ageMin=' + str(x) + '&ageMax=' + str(x) + '&nationality=' + nationality[0] + '&resultPerPage=160' # Country + age from 26 to 59
            result_from_6_to_64 = json.loads(requests.get(url).text)
            print(nationality[0], ' ', str(x) + ' =', result_from_6_to_64["total"])


            if result_from_6_to_64["total"] > 160: # filter by sexId
                url = 'https://ws-public.interpol.int/notices/v1/yellow?&sexId=M&ageMin=' + str(x) + '&ageMax=' + str(x) + '&nationality=' + nationality[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Male
                result_from_6_to_64_M = json.loads(requests.get(url).text)
                take_results(result_from_6_to_64_M)
                print(nationality[0], ' ', str(x) + ' male =', result_from_6_to_64_M["total"])

                url = 'https://ws-public.interpol.int/notices/v1/yellow?&sexId=F&ageMin=' + str(x) + '&ageMax=' + str(x) + '&nationality=' + nationality[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Female
                result_from_6_to_64_F = json.loads(requests.get(url).text)
                print(nationality[0], ' ', str(x) + ' female =', result_from_6_to_64_F["total"])
                take_results(result_from_6_to_64_F)

                if result_from_6_to_64_F["total"] + result_from_6_to_64_M["total"] != result_from_6_to_64["total"]:
                    url = 'https://ws-public.interpol.int/notices/v1/yellow?&sexId=U&ageMin=' + str(x) + '&ageMax=' + str(x) + '&nationality=' + nationality[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Unknown
                    result_from_6_to_64_U = json.loads(requests.get(url).text)
                    print(nationality[0], ' ', str(x) + ' unknown =', result_from_6_to_64_U["total"])
                    take_results(result_from_6_to_64_U)    

            else: take_results(result_from_6_to_64)




