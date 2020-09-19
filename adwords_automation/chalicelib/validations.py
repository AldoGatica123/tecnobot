import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

available_locations = ['Mexico', 'Guatemala', 'El Salvador', 'Honduras', 'Nicaragua', 'Costa Rica', 'Panama',
                       'Colombia']
available_packages = ['MARKETING_COMBO_1', 'MARKETING_COMBO_2', 'MARKETING_COMBO_3']
body_fields = ['business_name', 'description', 'history', 'location', 'marketing_package', 'phone', 'psid',
               'search_terms', 'slogan', 'website']


def validate_body(body):
    if validate_fields(body):
        valid = True
        valid = valid and validate_word_business_name(body['business_name'])
        valid = valid and validate_word_description(body['description'])
        valid = valid and validate_word_slogan(body['slogan'])
        valid = valid and validate_phone_number(body['phone'])
        valid = valid and validate_history(body['history'])
        valid = valid and validate_website(body['website'])
        valid = valid and validate_location(body['location'])
        valid = valid and validate_marketing_package(body['marketing_package'])
        return valid
    else:
        return False


def validate_word_business_name(word):
    result = word and 30 > len(word) > 2
    if not result:
        logger.error('Error bad format on business_name: ' + word)
    return result


def validate_word_description(word):
    result = word and 30 > len(word) > 2
    if not result:
        logger.error('Error bad format on description: ' + word)
    return result


def validate_word_slogan(word):
    result = word and 30 > len(word) > 2
    if not result:
        logger.error('Error bad format on slogan: ' + word)
    return result


def validate_history(word):
    result = word and 90 > len(word) > 2
    if not result:
        logger.error('Error bad format on history: ' + word)
    return result


def validate_phone_number(number):
    if number:
        phone_number = str(number).strip(' ').replace('-', '')
        if phone_number.isdigit() and len(phone_number) > 1:
            return True
    logger.error('Error bad format on phone: ' + number)
    return False


def validate_fields(body):
    for body_key in body_fields:
        if body_key not in body.keys():
            logger.error('Mandatory field missing: ' + body_key)
            return False
        mandatory_value = body[body_key].strip()
        if mandatory_value is None:
            logger.error('Mandatory field is blank: ' + body_key)
            return False
    return True


def validate_website(website):
    result = re.match(
        r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}'
        r'(:[0-9]{1,5})?(\/.*)?$', website, re.IGNORECASE)
    if not result:
        logger.error('Error bad format on website: ' + website)
    return result


def validate_location(location):
    result = location.upper() in available_locations
    if not result:
        logger.error('Error bad format on location: ' + location)
    return result


def validate_marketing_package(marketing_package):
    result = marketing_package.upper() in available_packages
    if not result:
        logger.error('Error bad format on marketing_package: ' + marketing_package)
    return result


def validate_psid(psid):
    result = len(psid) > 1 and psid.isdigit()
    if not result:
        logger.error('Error bad format on psid: ' + psid)
    return result


def validate_search_terms(search_terms):
    result = search_terms is not None and len(search_terms) > 1
    if not result:
        logger.error('Error bad format on search_terms: ' + search_terms)
    return result
