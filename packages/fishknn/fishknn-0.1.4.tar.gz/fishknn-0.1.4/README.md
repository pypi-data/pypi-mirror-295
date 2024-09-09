# fishknn

## Usage - bash
### 예측 및 데이터 저장
```bash
$ t_cmd
```

### 시각화
```bash
$ scat_plot
```
### Result
![Figure_1](https://github.com/user-attachments/assets/e7cc3be0-30a6-4418-a9e7-96d4576f1584)

## Usage - python
```python
from fishknn.what_fish_name import fish_pred

fish_pred(<length>, <weight>, <fish_class>)
# fish_class = 0 : Bream, 1 : Smelt
```

## result
### 데이터가 아예 없을때
```python
# result
학습용 데이터가 없으므로 데이터를 저장합니다. 정답 : Bream
```

### 충분한 데이터가 없을 때
```python
fish_pred(15, 150, 0)

# result
학습용 데이터가 부족하므로 데이터를 추가합니다. 현재 데이터의 수 : 5
```

### 데이터가 충분하다면?
```python
fish_pred(6.7, 9.3, 1)

# result
오답입니다. 정답은 Smelt입니다.
예측값 : Bream
```

### Data Plot
```python
from fishknn.what_fish_name import watch_data
watch_data()
```
