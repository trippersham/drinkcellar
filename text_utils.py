def clean_text(text):
    return text.replace('\n','')

def convert_to_camel_case(text):
    return ''.join([w.capitalize() for w in text.split('_')])
