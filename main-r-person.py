import requests
import json
import wanted

class RedNoticePerson (wanted.NoticePerson):
    def dec(self):
        pass  

def take_results(result):
    
    for bst in result["_embedded"]["notices"]:
        try:
            oneRedNoticePerson = RedNoticePerson(bst["forename"], bst["date_of_birth"], bst["entity_id"], bst["nationalities"],
                                    bst["name"], bst["_links"]["self"]["href"], bst["_links"]["images"]["href"], bst["_links"]["thumbnail"]["href"]) # KeyError
            
            with open('./img-r-person/' + bst["entity_id"].replace('/', '-') + '.jpg','wb') as target: #save img
                a = requests.get(bst["_links"]["thumbnail"]["href"])
                target.write(a.content)
        except KeyError:
            oneRedNoticePerson = RedNoticePerson(bst["forename"], bst["date_of_birth"], bst["entity_id"], bst["nationalities"],
                                    bst["name"], bst["_links"]["self"]["href"], bst["_links"]["images"]["href"], "NULL")
        finally: 
            oneRedNoticePerson.write_in_file('data-r-person.txt')
    
for country_id in wanted.wanted_by:
    url = 'https://ws-public.interpol.int/notices/v1/red?&arrestWarrantCountryId=' + country_id[0] + '&resultPerPage=160' # Country
    result = json.loads(requests.get(url).text)
    if result["total"] <= 160:
        print(country_id[0], " = ", result["total"])
        take_results(result)   
        
    else: # filter by age
        url = 'https://ws-public.interpol.int/notices/v1/red?&ageMin=0&ageMax=25&arrestWarrantCountryId=' + country_id[0] + '&resultPerPage=160' # Country + age from 0 to 25
        result_from_0_to_25 = json.loads(requests.get(url).text)
        print(country_id[0], "0-25 = ", result_from_0_to_25["total"])
        take_results(result_from_0_to_25)
        
        
        url = 'https://ws-public.interpol.int/notices/v1/red?&ageMin=60&ageMax=120&arrestWarrantCountryId=' + country_id[0] + '&resultPerPage=160' # Country + age from 60 to 120
        result_from_60_to_120 = json.loads(requests.get(url).text)
        print(country_id[0], "60-120 = ", result_from_60_to_120["total"])
        take_results(result_from_60_to_120)

        for x in range(26, 59): 
            url = 'https://ws-public.interpol.int/notices/v1/red?&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + country_id[0] + '&resultPerPage=160' # Country + age from 26 to 59
            result_from_26_to_59 = json.loads(requests.get(url).text)
            print(country_id[0], ' ', str(x) + ' =', result_from_26_to_59["total"])


            if result_from_26_to_59["total"] > 160: # filter by sexId
                url = 'https://ws-public.interpol.int/notices/v1/red?&sexId=M&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + country_id[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Male
                result_from_26_to_59_M = json.loads(requests.get(url).text)

                if  result_from_26_to_59_M["total"] > 160:# filter by sexId = male give result > 160                
                    for nationalityID in wanted.wanted_by:
                        try:
                            url = 'https://ws-public.interpol.int/notices/v1/red?&nationality='+ str(nationalityID[0]) + '&sexId=M&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + country_id[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Male + nationalityID
                            result_from_26_to_59_nation = json.loads(requests.get(url).text)
                            take_results(result_from_26_to_59_nation)
                            print(country_id[0], ' Nation:', nationalityID, " male = ", result_from_26_to_59_nation["total"])
                        except:
                            continue
                else: 
                    take_results(result_from_26_to_59_M)
                    print(country_id[0], ' ', str(x) + ' male =', result_from_26_to_59_M["total"])

                url = 'https://ws-public.interpol.int/notices/v1/red?&sexId=F&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + country_id[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Female
                result_from_26_to_59_F = json.loads(requests.get(url).text)
                print(country_id[0], ' ', str(x) + ' female =', result_from_26_to_59_F["total"])
                take_results(result_from_26_to_59_F)

                if result_from_26_to_59_F["total"] + result_from_26_to_59_M["total"] != result_from_26_to_59["total"]:
                    url = 'https://ws-public.interpol.int/notices/v1/red?&sexId=U&ageMin=' + str(x) + '&ageMax=' + str(x) + '&arrestWarrantCountryId=' + country_id[0] + '&resultPerPage=160' # Country + age from 26 to 59 + Unknown
                    result_from_26_to_59_U = json.loads(requests.get(url).text)
                    print(country_id[0], ' ', str(x) + ' unknown =', result_from_26_to_59_U["total"])
                    take_results(result_from_26_to_59_U)    

            else: take_results(result_from_26_to_59)




