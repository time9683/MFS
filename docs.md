# Definicion de la clase unit

la clase Unit tiene distintas caracteristicas.

el atributo importante es children, que es una lista enlazada que contiene a los hijos de la unidad.

atributos:
- **children** que es una lista enlazada que contiene a los hijos de la unidad.

metodos:

- **append** : agrega un hijo a la unidad.
- **remove** :  elimina un hijo de la unidad.


# Definicion de la ListaEnlazada

la lista solo contiene un atributo, que es el primer nodo de la lista.
dicho atributo se llama **head**.

atributo:
- **head** que es el primer nodo de la lista.


# definicion de NodoL

este el Nodo de la lista enlaza, contiene un atributo que es el valor del nodo y otro que es el siguiente nodo de la lista.

atributos:
- **data** que es el valor del nodo (File,Folder,None).
- **next** que es el siguiente nodo de la lista.





# definicion de Folder

saltando los atributos basicos 
la clase Folder tiene un atributo que es **children** que son los hijos de la carpeta, que es de tipo tree.
atributo adicional:
- **children** que son los hijos de la carpeta, que es de tipo tree.
metodos:
- append : agrega un hijo a la carpeta.
- search : busca un hijo en la carpeta.
- remove : elimina un hijo de la carpeta.
- to_list : retorna una lista con los hijos de la carpeta.


# definicion de tree

la clase tree tiene un atributo que es **root** que es el nodo raiz del arbol, que es de tipo Nodo.
Atributos:
- **root** que es el nodo raiz del arbol, que es de tipo Nodo.


la clase tree tiene los siguientes metodos:
- append : agrega un nodo al arbol.
- search : busca un nodo en el arbol.
- remove : elimina un nodo del arbol.
- get_list : retorna una lista con los nodos del arbol.



# definicion de Nodo

la clase Nodo tiene un atributo que es **data** que es el valor del nodo, que puede ser (Folder,File,None).
ademas tiene los atributos
- **left** que es el hijo izquierdo del nodo, que es de tipo Nodo.
- **right** que es el hijo derecho del nodo, que es de tipo Nodo.
- **data** que es el valor del nodo, que puede ser (Folder,File,None).



## Como iterar sobre la unidad

```python
# obtiene la unidad actual
unit_C = Unit.units["C"]

# obtener el primer nodo de la unidad
root = unit_C.children.head

# si se busca un nombre se puede iterar como termino el nombre o que el nodo sea None
while root.data.name != "Carpeta1":
    # obtenemos el siguiente nodo
    root = root.next

# si no se encontro el nodo, root sera None
if root is None:
    return

# obtenemos la carpeta del atributo data del nodo
carpeta = root.data
print(carpeta.name)
```



## Como iterar sobre la carpeta

```python
# si queremos buscar la ruta C:/Carpeta1/Carpeta2
# obtenemos la carpeta de la unidad

# -- utilizar codigo anterior explicado -- 
#este seria la Carpeta1
carpeta = alguna_carpeta

# buscar la carpeta2 en el arbol de la carpeta1
# esto retornara el Nodo que contiene la carpeta2
carpeta2 = carpeta.search("Carpeta2")
print(carpeta2.data.name)

```

### que falta por implementar
- [x] backup 
- [ ] rmdir (HL)
- [ ] mkdir (HL)
- [ ] type (HL)
- [ ] valid_path (HL)
- [ ] validaciones de las clase Tree





