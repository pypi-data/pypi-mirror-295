# Details

### Author: Edan
### Version: 1.0.10

A cocoa core data timestamp library

---

# Documentation

## Steps

### 1. Installation

> `pip install cocoa_time`

### 2. Import

> Import cocoa_time as `cocoa` for short `as long as you as you don't have a conflicting package with the same name`.

```python
import cocoa_time as cocoa
```

---

# Samples

> Sample of a cocoa timestamp

`747755750` is a cocoa timestamp that represents the date `Wednesday, September 11, 2024 1:55:50 PM` and is equal to `1726062950` in **unix timestamp**

> Cocoa timestamp can come with 2 more decimals that represent centi seconds this timestamp: `747755750` will be `74775575000` with centi seconds a 9 digit and 11 digit cocoa timestamp

---

# Functions

## Introduction

> There are 4 functions in total

1. to_datetime
2. to_unix_timestamp
3. from_unix_timestamp
4. from_datetime

---

## to_datetime

> returns a conversion of cocoa timestamp to datetime

### Parameters

`timestamp`: **int** | **str**

```python
cocoa.to_datetime(timestamp)
```

---

#### Example

> prints a datetime object converted from a cocoa timestamp

```python
import cocoa_time as cocoa

#cocoa_timestamp = "747755750" # timestamp can also be a string that contains only numbers
timestamp = 747755750
date = cocoa.to_datetime(timestamp)

print(date)
```

**Result**:\
`2024-09-11 13:55:50`

---

## to_unix_timestamp

> returns a conversion of cocoa timestamp to unix timestamp

### Parameters

`timestamp`: **int** | **str**

```python
cocoa.to_unix_timestamp(cocoa_timestamp)
```

---

### Example

> prints an int with the value 1726062950 in this case (a conversion of the cocoa timestamp int to a unix timestamp int)

```python
import cocoa_time as cocoa

#timestamp = "747755750" # cocoa_timestamp can also be a string that contains only numbers
cocoa_timestamp = 747755750
unix_timestamp = cocoa.to_unix_timestamp(cocoa_timestamp)

print(unix_timestamp)
```

**Result**:\
`1726062950`

---

## from_unix_timestamp

> returns a conversion of a unix timestamp to cocoa timestamp

### Parameters

`timestamp`: **int** | **str**\
`centi seconds`: **bool** = **False**

```python
cocoa_timestamp = cocoa.from_unix_timestamp(unix_timestamp)
```

---

### Example #1

> prints a 9 digit int with the value 747755750 in this case (a conversion of the unix timestamp int to a cocoa timestamp int)

```python
import cocoa_time as cocoa

#unix_timestamp = "1726062950" # unix_timestamp can also be a string that contains only numbers
unix_timestamp = 1726062950
cocoa_timestamp = cocoa.from_unix_timestamp(unix_timestamp)

print(cocoa_timestamp)
```

**Result**:\
`747755750`

---

### Example #2

> prints an 11 digit int with the value 74775575000 in this case (a conversion of the unix timestamp int to a cocoa timestamp int)

```python
import cocoa_time as cocoa

#unix_timestamp = "1726062950" # unix_timestamp can also be a string that contains only numbers
unix_timestamp = 1726062950
cocoa_timestamp = cocoa.from_unix_timestamp(unix_timestamp, True)

# Longer version that has the centi seconds parameter name
cocoa_timestamp = cocoa.from_unix_timestamp(unix_timestamp, centiseconds = True)

print(cocoa_timestamp)
```

**Result**:\
`74775575000`

---

## from_datetime

> Converts a datetime object or a string with a provided format string to cocoa timestamp

#### Parameters

`date`: **datetime** | **str**\
`centiseconds`: **bool** = **False**\
`format`: **str** | **None** = **None**

```python
cocoa_timestamp = cocoa.from_datetime(date)
```

```python
cocoa_timestamp = cocoa.from_datetime(date_string, format=date_format)
```

**Note**:

> Format **must be provided** when date is of type **string** otherwise it **must stay None** when **date is a datetime class**

---

### Example #1

> prints a 9 digit int that is the cocoa timestamp of datetime.now() date value can be replaced with another value of type datetime object

```python
from datetime import datetime
import cocoa_time as cocoa

date = datetime.now()
cocoa_timestamp = cocoa.from_datetime(date)

print(cocoa_timestamp)
```

> results varies based on date provided so an example result won't be provided here

---

### Example #2

> prints a 11 digit int that is the cocoa timestamp of datetime.now() date value can be replaced with another value of type datetime object

```python
from datetime import datetime
import cocoa_time as cocoa

# For a centi second 11 digit cocoa timestamp

date = datetime.now()
cocoa_timestamp = cocoa.from_datetime(date, True)

# Longer version that has the centi seconds parameter name
# cocoa_timestamp = cocoa.from_datetime(date, centiseconds = True)

print(cocoa_timestamp)
```

> results varies based on date provided so an example result won't be provided here

---

### Example #3

> prints a 9 digit int that is the cocoa timestamp of the formatted date string a format string must be provided as well

```python
import cocoa_time as cocoa

date_string = "01/01/2002 00:00:00"
cocoa_timestamp = cocoa.from_datetime(date_string, format="%d/%m/%Y %H:%M:%S")

print(cocoa_timestamp)
```

**Result**:\
`31536000`

---

### Example #4

> prints an 11 digit int that is the cocoa timestamp of the formatted date string a format string must be provided as well

```python
import cocoa_time as cocoa

date_string = "01/01/2002 00:00:00"
cocoa_timestamp = cocoa.from_datetime(date_string, format="%d/%m/%Y %H:%M:%S", centiseconds=True)

print(cocoa_timestamp)
```

**Result**:\
`3153600000`