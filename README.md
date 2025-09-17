This repository contains a machine learning algorithm specifically random forest alogorithm to detect if a given url is a phishing site or not.

Control Flow :
  1. The user inputs a url into the website
  2. The website through the api calls the url_extractor module
  3. The url_erxtractor module creates an output CSV file which is taken as the input of the algorithm
  4. The algorithm then produces an (filler) output
  5. The output is returned to the website to be displayed

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
| `ssl_certificate`       | 1 if SSL certificate exists, 0 otherwise        |
| `label`                 | Target: 1 = phishing, 0 = legitimate            |


