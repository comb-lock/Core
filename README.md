[中文版](/README-CN.md))

## Description of core functions
The core function of Comb Lock consists of two parts: encryption and decryption, save and read.

The specific operation flow is: (select document) -> verify password -> record/read.

Document structure: plain text, one record per line. Separated by a comma, the former is a record, the latter is a note. The last line is the secret text of string `'success'`, used to verify whether the password is correct.

Encryption and decryption method: The unique `root password` is used to encrypt and decrypt the whole document through the `AES-256 CBC` algorithm, followed by the `Base64` encoding process to facilitate the storage and transmission of the encrypted document. The root password can be an arbitrary string and is converted to a 32-bit password by taking the `MD5` hash value.


## Client Rules
In order to ensure security, the following rules are recommended for practical development.

- The root password should be verified each time the client is used again after closing. Status cannot be retained.
- The client should not request any non-essential permissions.
- If an error occurs during recording or reading, the user should be clearly informed of the result of the failed operation.
- If the password is changed, the user should be explicitly prompted and the encrypted document that used the previous password should be deleted.
- When creating a new document, the initial root password should be high strength, which had better contain upper case + lower case + numbers + special symbols, and no fewer than 8 characters.


## Demo (bash test)
The following demonstrates how to `manually` perform the basic encryption and decryption steps. Refer to the provided demo, you can do it yourself in other ways.

#### Using a Python script (tested only on MacOS Python 3.7).

0. Need for pycrypto library
```bash
pip install pycrypto
```

1. add a new record with the root password (an empty Lock document that has been created, the password is `IAMp0ssW@rd` in the example, you can directly add/view the record)

```bash
# Parameter list.
# Root password: any string 
# add: Flags for adding records
# Record to be added: String
# Prompt for record: string
# (Optional) Encrypt document location: defaults to the Lock file in the current directory.

python comb_lock_core.py IAMp0ssW@rd add 'i am a secret' 'i am a note' [. /Lock]
```

2. View records by root password

```bash
# Parameter list. 
# Root password 
# read: flag to read the record
# (Optional) Encrypt document location: defaults to the Lock file in the current directory.

python comb_lock_core.py IAMp0ssW@rd read [. /Lock]
```

3. Creation of new encrypted files

```bash
# Parameter list. 
# Root password
# new: flag for new document
# Encrypted document location: when creating a new document, you must specify the location of the new document, you cannot rename it with an existing file.

python comb_lock_core.py IAMn3wP@ss new . /Lock2
```


### With tools such as online decryption sites

Manually modify and view the encrypted documents, as long as the connection of the document remains unchanged and the password of each line of data is consistent.

But why not use a secure and simple client? :) 