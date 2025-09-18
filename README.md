This repository contains a machine learning algorithm specifically random forest alogorithm to detect if a given url is a phishing site or not.

Control Flow :
  1. The user inputs a url into the website
  2. The website through the flask api calls the randomforest model and the url_extractor
  3. After the model evaluates the url it returns a confidence score back to the website
  4. The website displays the confidence score as a percentage bar

The url_extractor module takes the given url and checks if the url contains:
| Column Name             | Meaning                                         |
| ----------------------- | ----------------------------------------------- |
| `url`                   | The website URL itself                          |
| `having_ip`             | 1 if URL contains an IP address, 0 otherwise    |
| `url_length`            | Length of the URL                               |
| `shortening_service`    | 1 if URL uses a shortening service, 0 otherwise |
| `having_at_symbol`      | 1 if `@` appears in URL, 0 otherwise            |
| `double_slash_redirect` | 1 if `//` appears after protocol, 0 otherwise   |
| `prefix_suffix`         | 1 if URL has `-` in domain, 0 otherwise         |
| `having_sub_domain`     | 1 if URL has subdomain, 0 otherwise             |
| `https_token`           | 1 if HTTPS is present, 0 otherwise              |
| `port`                  | 1 if non-standard port used, 0 otherwise        |
| `ssl_final_state`       | 1 if SSL certificate valid, 0 otherwise         |
| `dns_record`            | 1 if DNS record exists, 0 otherwise             |       



