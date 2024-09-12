my_dict = {
    'name': 'fawas',
    'place':'calicut',
    'age':23,
    'hobbies':('games','coding','etc')
}

interchanged = {v:k for k,v in my_dict.items()}

print(interchanged)