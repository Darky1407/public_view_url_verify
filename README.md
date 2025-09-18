This repository contains a machine learning algorithm specifically random forest alogorithm to detect if a given url is a phishing site or not.

Control Flow :
  1. The user inputs a url into the website
  2. The website through the flask api calls the randomforest model and the url_extractor
  3. After the model evaluates the url it returns a confidence score back to the website
  4. The website displays the confidence score as a percentage bar

The url_extractor module takes the given url and checks if the url contains:
| **Feature**                 | **What it Checks**                                                |
| --------------------------- | ----------------------------------------------------------------- |
| having_ip                   | Whether the URL contains an IP address instead of a domain        |
| url_length                  | The total length of the URL                                       |
| shortening_service          | If the URL uses a shortening service (like bit.ly, tinyurl, etc.) |
| having_at_symbol            | Whether the URL contains an `@` symbol                            |
| double_slash_redirect       | If there’s an extra `//` after the protocol                       |
| prefix_suffix               | Whether the domain name contains a hyphen (`-`)                   |
| having_sub_domain           | If the URL has multiple subdomains (other than `www`)             |
| https_token                 | Whether the domain part contains the word “https”                 |
| port                        | If the URL uses an uncommon port (not 80 or 443)                  |
| ssl_final_state             | Whether the URL uses HTTPS (`0`) or HTTP (`1`)                    |
| dns_record                  | If the domain has a valid DNS record                              |
| ssl_certificate             | Placeholder feature (currently always `0` in your code)           |

Random Forest is a machine learning algorithm that works by combining the power of many decision trees. A decision tree is like a flowchart that asks yes/no questions about the data (for example, “Is the URL length greater than 50?”). On its own, a single tree might make mistakes or overfit, but Random Forest builds many such trees on different random parts of the data and features. Each tree gives its own “vote” for the prediction, and the forest takes the majority vote (for classification) or the average (for regression). By using randomness and combining many trees, Random Forest reduces errors, avoids overfitting, and gives more stable and accurate results. It’s called “random” because it randomly picks data samples and features for each tree, and “forest” because it grows many trees together to make a stronger, smarter predictor.
    



