from uuid import uuid4
import csv
# total count = 20689

test = list(range(1, 21967))
token = []
link = []
id = []

for num in test:
    id.append(num)
    rand_token_hex = uuid4().hex
    token.append(rand_token_hex)
    link_with_token = "https://science-it.charite.de/orcid/invitation_link/" + rand_token_hex
    link.append(link_with_token)
    # print(rand_token_hex)
    # print(link_with_token)
    # break

with open('/mnt/u/s-it/orcid_project/test.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'token', 'link'])
    writer.writerows(zip(id, token, link))

