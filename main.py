import requests


def processPage(page):
    url = "https://careers.google.com/api/v3/search/"
    params = {
        "page": page,
        "page_size": 100,
    }
    res = requests.get(url, params=params).json()
    for job in res['jobs']:
        description = job['description']
        for location in job['locations']:
            for buildingPin in job['building_pins']:
                print(f"Processing job {job['id']} - {job['title']} - {location['display']}")
                data = {
                    "id": job['id'],
                    "title": job['title'],
                    "categories": ", ".join(job['categories']),
                    "applyUrl": job['apply_url'],
                    "responsibilities": job['responsibilities'],
                    "qualifications": job['qualifications'],
                    "companyId": job['company_id'],
                    "companyName": job['company_name'],
                    "languageCode": job['language_code'],
                    "locationDisplay": location['display'],
                    "locationLat": location['lat'],
                    "locationLon": location['lon'],
                    "locationAddress": ", ".join(location['address_lines']),
                    "locationCity": location['city'],
                    "locationPostCode": location['post_code'],
                    "locationCountry": location['country'],
                    "locationCountryCode": location['country_code'],
                    "locationIsRemote": location['is_remote'],
                    "description": description,
                    "educationLevels": ", ".join(job['education_levels']),
                    "created": job['created'],
                    "modified": job['modified'],
                    "publishDate": job['publish_date'],
                    "applicationInstruction": job['application_instruction'],
                    "locationsCount": job['locations_count'],
                    "additionalInstructions": job['additional_instructions'],
                    "summary": job['summary'],
                    "buildingPinsLat": buildingPin['lat'],
                    "buildingPinsLon": buildingPin['lon'],
                    "hasRemote": job['has_remote'],
                    "minSalary": None,
                    "maxSalary": None,
                }
                if "The US base salary range for this full-time position is " in description:
                    salary = description.split("The US base salary range for this full-time position is ")[1].split(" ")[0]
                    if "-" in salary:
                        minSalary = salary.split("-")[0][1:].replace(",", "")
                        maxSalary = salary.split("-")[1][1:].replace(",", "").replace("+", "")
                        data['minSalary'] = float(minSalary)
                        data['maxSalary'] = float(maxSalary)
                print(data)


def main():
    url = "https://careers.google.com/api/v3/search/"
    res = requests.get(url).json()
    count = res['count']
    print(f"Total number of jobs available in Google: {count} ")
    perPage = 100
    pages = count // perPage
    for i in range(pages):
        processPage(i + 1)


if __name__ == '__main__':
    main()
