A converter from PlantUML class diagrams to python3 skeleton classes

supported PlantUML class diagram syntax:
========================================

```
uml : "@startuml" decls "@enduml"
decls : ε | decls decl
decl : class | assoc | "skinparam"
class : abs "class" id '{' attribs '}'
class : abs "interface" id '{' attribs '}'
class : enum id '{' ids '}'
ids : ID
ids : ids ',' ID
abs : ε | "abstract"
attribs : ε | attribs attrib
attrib : prot id vec type init
attrib : prot id '(' ')' type
attrib : prot id '(' args ')' type
attrib : prot "static" id '(' ')' type
attrib : prot "static" id '(' args ')' type
attrib : prot "abstract" id '(' ')' type
attrib : prot "abstract" id '(' args ')' type
type : ε | ':' id vec
args : id type | args ',' id type
prot : ε | '+' | '-' | '~' | '#'
vec : ε | '[' ']' | '[' [0-9]+ ']' | '<[_A-Za-z][A-Za-z0-9_]*>'
init : ε | '=' id | '=' str | '=' [0-9]+
assoc : id ('<|--' | '<|..' | '--|>' | '..|>') id
assoc : id card ('*-->' | '--*' | '<--*' | 'o-->' | 'o--' | '<--o' | '--o' | '-->' | '<--' | '--') card id type
card : ε | STR
str : '"([^"\\]|\\.)*"'
id : '[_A-Za-z][A-Za-z0-9_]*'
```

comments start with `#` symbol and end the end of the line.

A simple class example:
=======================

```
@startuml
skinparam classAttributeIconSize 0
skinparam monochrome true
class Tire {
- _pressure: int
- _standard: int
- _flat: bool
--
+ Tire(standard: int , pressure: int)
+ standard() : int
+ pressure() : int
+ flat() : bool
+ pressure(pressure: int) : void
+ empty() : bool
}
@enduml
```

Generate the python3 skeleton code to `stdout` with:

```
python3 -m uml2py tire.uml
```

or save the skeleton code to a file:

```
python3 -m uml2py tire.uml tire.py
```


Use the environment `DEBUG=1` for a verbose output:

```
DEBUG=1 python3 -m uml2py tire.uml
```

Some examples in the `examples/` directory.

(C) prs, IST 2024
