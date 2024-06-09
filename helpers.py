from datetime import datetime
import pandas as pd

from bot import *

def check_user(wl, user_id):
  if user_id == owner:
    return True

  if str(user_id) not in wl.keys():
    return False
  else:
    now = datetime.now(wib)
    exp_time = datetime.strptime(wl[str(user_id)], datetime_format).replace(tzinfo=wib)

    if now > exp_time:
      return False
    else:
      return True

def convert(data):
  numbers = check_number(data['filename'])
  split_number = split(numbers, data['totalc'])

  countc = 0
  countf = 0
  vcf_files = []
  sisa = []
  for numbers in split_number:
    vcard_entries = []
    for number in numbers:
      countc+=1
      vcard_entry = f"BEGIN:VCARD\nVERSION:3.0\nFN:{data['cname']}-{countc}\nTEL;TYPE=CELL:+{number}\nEND:VCARD"
      vcard_entries.append(vcard_entry)

    countf+=1
    if countf > data['totalf']:
      sisa.append(numbers)
    else:
      vcf_name = f"files/{data['name']}_{countf}.vcf"
      vcf_files.append(vcf_name)
      
      with open(vcf_name, 'w', encoding='utf-8') as vcard_file:
        for entry in vcard_entries:
            vcard_file.write(entry + "\n")
  
  if sisa:
    file_txt = "files/sisa.txt"
    vcf_files.append(file_txt)
    
    with open(file_txt, 'w', encoding='utf-8') as file:
      for s in sisa:
        file.write("\n".join(s) + "\n")
    
  return vcf_files

def convert_vcf(data):
  data['filename'] = convert_xlsx_to_txt(data)
  numbers = check_number(data['filename'])
  split_number = split(numbers, data['totalc'])

  countc = 0
  countf = 0
  vcf_files = []
  for numbers in split_number:
    vcard_entries = []
    for number in numbers:
      countc+=1
      vcard_entry = f"BEGIN:VCARD\nVERSION:3.0\nFN:{data['cname']}-{countc}\nTEL;TYPE=CELL:+{number}\nEND:VCARD"
      vcard_entries.append(vcard_entry)

    countf+=1
    vcf_name = f"files/{data['name']}_{countf}.vcf"
    vcf_files.append(vcf_name)
    
    with open(vcf_name, 'w', encoding='utf-8') as vcard_file:
      for entry in vcard_entries:
          vcard_file.write(entry + "\n")
    
    if countf == data['totalf']:
      break

  return vcf_files

def convert_xlsx_to_txt(data):
  df = pd.read_excel(data['filename'])
  file_name = f"files/{data['name']}.txt"
  df.to_csv(file_name, index=False, sep='\t')

  return file_name

def check_number(path):
  numbers = []

  with open(path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

  for line in lines:
    line = line.strip().replace('+', '')
    if line.isdigit():
      numbers.append(line)

  return numbers

def pecah_txt(data):
  numbers = check_number(data['filename'])
  split_number = split(numbers, data['totaln'])
  countf = 0
  files = []

  for numbers in split_number:
    countf+=1
    txt_name = f"files/{data['name']}_{countf}.txt"
    files.append(txt_name)

    with open(txt_name, 'w', encoding='utf-8') as file:
      for number in numbers:
        file.write(number + "\n")

    if countf == data['totalf']:
      break
  
  return files

def pecah_vcf(data):
  with open(data['filename'], 'r', encoding='utf-8') as file:
    lines = file.readlines()

  contacts = []
  current_contact = []

  for line in lines:
    if not line.strip():
      continue

    current_contact.append(line)
    if line.strip() == 'END:VCARD':
      contacts.append(current_contact)
      current_contact = []

  split_contact = split(contacts, data['totalc'])
  countf = 0
  files = []

  for contacts in split_contact:
    countf+=1
    file_name = f"files/{data['name']}_{countf}.vcf"
    files.append(file_name)
    
    with open(file_name, 'w', encoding='utf-8') as file:
      for contact in contacts:
        contact = "".join(contact)
        file.write(contact)

    if countf == data['totalf']:
      break

  return files

def split(arr, num):
  return [arr[x:x+num] for x in range(0, len(arr), num)]