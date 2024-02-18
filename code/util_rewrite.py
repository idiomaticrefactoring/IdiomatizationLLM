
import copy
def join(string_list,delimiter):
    new_string = delimiter.join(string_list)
    return new_string
'''
Python how to insert a string at the first occurrence of a substring of a string
'''
'''
You can use the `index()` method to find the index of the first occurrence of a substring in a string, and then use string concatenation to insert the new string at that index. Here's an example:

```
original_string = "hello world"
substring = "world"
new_string = "beautiful "

index = original_string.index(substring)
new_string_at_index = original_string[:index] + new_string + original_string[index:]

print(new_string_at_index)  # output: "hello beautiful world"
```

In this example, we first define the original string and the substring we want to find. We then use the `index()` method to find the index of the first occurrence of the substring in the original string. We then use string concatenation to insert the new string at that index, by slicing the original string into two parts (before and after the index) and concatenating the new string in between. Finally, we print the resulting string.
'''
def insert_first_occur(substring,new_string,original_string):

    index = original_string.index(substring)
    new_string_at_index = original_string[:index] + new_string + original_string[index:]
    return new_string_at_index
'''
Python how to insert a string after the first occurrence of a substring of a string
'''

'''
You can use the `replace()` method to replace the first occurrence of a substring with a new string. Here's an example:

```
string = "hello world"
substring = "l"
new_string = "123"

index = string.find(substring) + len(substring)
result = string[:index] + new_string + string[index:]

print(result)
```

Output:
```
hel123lo world
```

Explanation:
- `string.find(substring)` returns the index of the first occurrence of the substring in the string.
- `index = string.find(substring) + len(substring)` calculates the index of the character after the first occurrence of the substring.
- `string[:index]` returns the substring before the first occurrence of the substring.
- `string[index:]` returns the substring after the first occurrence of the substring.
- `result = string[:index] + new_string + string[index:]` concatenates the three substrings with the new string in the middle.
'''
def insert_after_first_occur(substring,new_string,string):

    index = string.find(substring) + len(substring)
    result = string[:index] + new_string + string[index:]
    return result

'''
Python how to replace the first occurrence of a substring within a string with a new substring.  
'''

'''
You can use the `replace()` method with a `count` parameter of 1 to replace only the first occurrence of a substring within a string. Here's an example:

```
string = "hello world"
substring = "l"
new_substring = "z"

new_string = string.replace(substring, new_substring, 1)

print(new_string)  # "hezlo world"
```

In this example, we replace the first occurrence of the substring "l" with the new substring "z" in the string "hello world". The resulting string is "hezlo world".
'''
def replace_first_occur(substring,replace_string,string):
    new_string = string.replace(substring,replace_string,1 )
    return new_string

'''
Python how to replace all occurrences of a substring within a string with a new substring.
'''
'''
You can use the `replace()` method to replace all occurrences of a substring within a string with a new substring. Here's an example:

```
string = "Hello, world! Hello, Python!"
new_string = string.replace("Hello", "Hi")
print(new_string)
```

Output:
```
Hi, world! Hi, Python!
```

In this example, we replaced all occurrences of the substring "Hello" with the new substring "Hi". The `replace()` method returns a new string with the replacements made. Note that the original string is not modified.
'''

def replace(substring,replace_string,string):
    new_string = string.replace(substring,replace_string )
    return new_string
'''
Python how to remove all occurrences of a substring within a string
'''

'''
There are several ways to remove all occurrences of a substring within a string in Python. Here are a few examples:

1. Using the replace() method:

```python
string = "Hello World"
substring = "l"
new_string = string.replace(substring, "")
print(new_string) # Output: Heo Word
```

2. Using the re.sub() method from the re module:

```python
import re

string = "Hello World"
substring = "l"
new_string = re.sub(substring, "", string)
print(new_string) # Output: Heo Word
```

3. Using a loop and string slicing:

```python
string = "Hello World"
substring = "l"
new_string = ""

for i in range(len(string)):
    if string[i:i+len(substring)] != substring:
        new_string += string[i]

print(new_string) # Output: Heo Word
```

All of these methods will remove all occurrences of the specified substring within the original string.
'''
def remove(substring,string):
    new_string = string.replace(substring,'')
    return new_string
real_instruction = '''
Write Python code to check whether a given string starts with a given substring. If it is, remove the given substring
for example,
for the given string: not len(a+b), a given substring is "not "
the given string starts with "not ", so the new string len(a+b)
'''
def remove_starts_substring(string,substring):
    if string.startswith(substring):
        new_string = string[len(substring):]
        return new_string
    return string