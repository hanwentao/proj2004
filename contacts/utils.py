import hashlib
import re

def unique(list):
    return [x for i, x in enumerate(list) if x not in list[:i]]

def generate_verification_code(student_id, name, secret_key=''):
    m = hashlib.md5()
    m.update(student_id.encode())
    m.update(name.encode())
    m.update(secret_key.encode())
    return m.hexdigest()[:6]

def split_class_name(name, default_grade=None):
    if not name:
        return ('', -1, -1, '')
    parts = re.split(r'(\d+)', name)
    grade = int(parts[1][0])
    if default_grade is not None and grade == default_grade % 10:
        grade = -1
    number = int(parts[1][1:] or '-1')
    return (parts[0], grade, number, parts[2])
